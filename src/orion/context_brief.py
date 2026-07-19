"""Immutable, content-free presentation of one verified context manifest."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any

from .contracts import ContextManifest, ProvenanceRef


CONTEXT_BRIEF_SCHEMA = "orion.context-brief/0.1"


def _digest(value: Any) -> str:
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return sha256(encoded).hexdigest()


def _require_text(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be non-empty text")


def _require_digest(value: str, field_name: str) -> None:
    if not isinstance(value, str) or len(value) != 64 or any(
        character not in "0123456789abcdef" for character in value
    ):
        raise ValueError(f"{field_name} must be a lowercase SHA-256 digest")


@dataclass(frozen=True, slots=True)
class ContextBriefEntry:
    """Content-free presentation metadata for one manifest document."""

    source_ref: str
    repository_path: str
    revision: str
    content_sha256: str
    provenance: ProvenanceRef
    document_length: int
    document_order: int

    def __post_init__(self) -> None:
        if not isinstance(self.provenance, ProvenanceRef):
            raise TypeError("provenance must be a ProvenanceRef")
        for field_name in ("source_ref", "repository_path", "revision"):
            _require_text(getattr(self, field_name), field_name)
        _require_digest(self.content_sha256, "content_sha256")
        if type(self.document_length) is not int or self.document_length < 0:
            raise ValueError("document_length must be a non-negative integer")
        if type(self.document_order) is not int or self.document_order < 0:
            raise ValueError("document_order must be a non-negative integer")
        if self.repository_path != _repository_path(self.source_ref):
            raise ValueError("repository path does not match source reference")
        if self.source_ref != self.provenance.source_ref:
            raise ValueError("source reference and provenance disagree")
        if self.revision != self.provenance.revision:
            raise ValueError("revision and provenance disagree")
        if self.content_sha256 != self.provenance.content_sha256:
            raise ValueError("content hash and provenance disagree")


@dataclass(frozen=True, slots=True)
class ContextBrief:
    """Deterministic backend-facing context metadata without document text."""

    brief_id: str
    request_id: str
    manifest_id: str
    manifest_sha256: str
    entries: tuple[ContextBriefEntry, ...]
    brief_sha256: str
    schema_version: str = CONTEXT_BRIEF_SCHEMA

    @classmethod
    def create(
        cls,
        manifest: ContextManifest,
        entries: tuple[ContextBriefEntry, ...],
    ) -> "ContextBrief":
        manifest.__post_init__()
        frozen_entries = tuple(entries)
        payload = cls._digest_payload(manifest, frozen_entries)
        brief_sha256 = _digest(payload)
        return cls(
            brief_id=f"brief-{brief_sha256[:16]}",
            request_id=manifest.request_id,
            manifest_id=manifest.manifest_id,
            manifest_sha256=manifest.manifest_sha256,
            entries=frozen_entries,
            brief_sha256=brief_sha256,
        )

    @staticmethod
    def _digest_payload(
        manifest: ContextManifest,
        entries: tuple[ContextBriefEntry, ...],
    ) -> dict[str, Any]:
        return {
            "schema_version": CONTEXT_BRIEF_SCHEMA,
            "request_id": manifest.request_id,
            "manifest_id": manifest.manifest_id,
            "manifest_sha256": manifest.manifest_sha256,
            "entries": [
                {
                    "source_ref": entry.source_ref,
                    "repository_path": entry.repository_path,
                    "revision": entry.revision,
                    "content_sha256": entry.content_sha256,
                    "provenance": {
                        "entry_id": entry.provenance.entry_id,
                        "owner": entry.provenance.owner,
                        "source_ref": entry.provenance.source_ref,
                        "revision": entry.provenance.revision,
                        "content_sha256": entry.provenance.content_sha256,
                    },
                    "document_length": entry.document_length,
                    "document_order": entry.document_order,
                }
                for entry in entries
            ],
        }

    def __post_init__(self) -> None:
        frozen_entries = tuple(self.entries)
        object.__setattr__(self, "entries", frozen_entries)
        for field_name in ("brief_id", "request_id", "manifest_id"):
            _require_text(getattr(self, field_name), field_name)
        _require_digest(self.manifest_sha256, "manifest_sha256")
        _require_digest(self.brief_sha256, "brief_sha256")
        if self.schema_version != CONTEXT_BRIEF_SCHEMA:
            raise ValueError(f"unsupported context brief schema: {self.schema_version}")
        if not self.entries:
            raise ValueError("a context brief requires at least one entry")
        entry_ids = tuple(entry.provenance.entry_id for entry in frozen_entries)
        if len(set(entry_ids)) != len(entry_ids):
            raise ValueError("context brief provenance entry IDs must be unique")
        expected_order = tuple(range(len(frozen_entries)))
        actual_order = tuple(entry.document_order for entry in frozen_entries)
        if actual_order != expected_order:
            raise ValueError("context brief document order must be contiguous")
        manifest_view = _ManifestDigestView(
            request_id=self.request_id,
            manifest_id=self.manifest_id,
            manifest_sha256=self.manifest_sha256,
        )
        expected = _digest(self._digest_payload(manifest_view, frozen_entries))
        if self.brief_sha256 != expected:
            raise ValueError("context brief digest mismatch")
        if self.brief_id != f"brief-{expected[:16]}":
            raise ValueError("context brief ID does not match its digest")


@dataclass(frozen=True, slots=True)
class _ManifestDigestView:
    request_id: str
    manifest_id: str
    manifest_sha256: str


@dataclass(frozen=True, slots=True)
class ContextBriefBuilder:
    """Derive a deterministic brief without selecting or reading documents."""

    def build(self, manifest: ContextManifest) -> ContextBrief:
        if not isinstance(manifest, ContextManifest):
            raise TypeError("manifest must be a ContextManifest")
        manifest.__post_init__()
        entries = tuple(
            ContextBriefEntry(
                source_ref=entry.source_ref,
                repository_path=_repository_path(entry.source_ref),
                revision=entry.revision,
                content_sha256=entry.content_sha256,
                provenance=entry.provenance(),
                document_length=len(entry.content.encode("utf-8")),
                document_order=document_order,
            )
            for document_order, entry in enumerate(manifest.entries)
        )
        return ContextBrief.create(manifest, entries)


def _repository_path(source_ref: str) -> str:
    _source_id, separator, path = source_ref.partition(":")
    return path if separator and path else source_ref
