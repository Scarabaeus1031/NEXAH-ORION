"""Immutable contracts for the Phase 1A ORION execution slice."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from typing import Any, Iterable


REQUEST_SCHEMA = "orion.orientation-request/0.1"
CONTEXT_SCHEMA = "orion.context-manifest/0.1"
RESULT_SCHEMA = "orion.reasoning-result/0.1"
RESPONSE_SCHEMA = "orion.orientation-response/0.1"


def _require_text(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be non-empty text")


def _digest(value: Any) -> str:
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return sha256(encoded).hexdigest()


@dataclass(frozen=True, slots=True)
class OrientationRequest:
    """A caller-owned request entering ORION."""

    request_id: str
    objective: str
    requested_by: str
    request_type: str = "review"
    scope: tuple[str, ...] = ()
    schema_version: str = REQUEST_SCHEMA

    def __post_init__(self) -> None:
        for field_name in ("request_id", "objective", "requested_by", "request_type"):
            _require_text(getattr(self, field_name), field_name)
        if self.schema_version != REQUEST_SCHEMA:
            raise ValueError(f"unsupported request schema: {self.schema_version}")
        if any(not isinstance(item, str) or not item.strip() for item in self.scope):
            raise ValueError("scope entries must be non-empty text")
        if len(set(self.scope)) != len(self.scope):
            raise ValueError("scope entries must be unique")


@dataclass(frozen=True, slots=True)
class ContextEntry:
    """One context value with source ownership and a verified content digest."""

    entry_id: str
    owner: str
    source_ref: str
    revision: str
    content: str
    content_sha256: str

    @classmethod
    def create(
        cls,
        *,
        entry_id: str,
        owner: str,
        source_ref: str,
        revision: str,
        content: str,
    ) -> "ContextEntry":
        return cls(
            entry_id=entry_id,
            owner=owner,
            source_ref=source_ref,
            revision=revision,
            content=content,
            content_sha256=sha256(content.encode("utf-8")).hexdigest(),
        )

    def __post_init__(self) -> None:
        for field_name in ("entry_id", "owner", "source_ref", "revision", "content"):
            _require_text(getattr(self, field_name), field_name)
        expected = sha256(self.content.encode("utf-8")).hexdigest()
        if self.content_sha256 != expected:
            raise ValueError(f"content digest mismatch for context entry {self.entry_id}")

    def provenance(self) -> "ProvenanceRef":
        return ProvenanceRef(
            entry_id=self.entry_id,
            owner=self.owner,
            source_ref=self.source_ref,
            revision=self.revision,
            content_sha256=self.content_sha256,
        )


@dataclass(frozen=True, slots=True)
class ProvenanceRef:
    """Content-free provenance copied into the final response."""

    entry_id: str
    owner: str
    source_ref: str
    revision: str
    content_sha256: str

    def __post_init__(self) -> None:
        for field_name in ("entry_id", "owner", "source_ref", "revision"):
            _require_text(getattr(self, field_name), field_name)
        if len(self.content_sha256) != 64 or any(
            character not in "0123456789abcdef" for character in self.content_sha256
        ):
            raise ValueError("content_sha256 must be a lowercase SHA-256 digest")


@dataclass(frozen=True, slots=True)
class ContextManifest:
    """ORION-owned immutable record of the context selected for one request."""

    manifest_id: str
    request_id: str
    entries: tuple[ContextEntry, ...]
    manifest_sha256: str
    schema_version: str = CONTEXT_SCHEMA

    @classmethod
    def create(
        cls,
        request: OrientationRequest,
        entries: Iterable[ContextEntry],
    ) -> "ContextManifest":
        frozen_entries = tuple(entries)
        payload = cls._digest_payload(request.request_id, frozen_entries)
        manifest_sha256 = _digest(payload)
        return cls(
            manifest_id=f"ctx-{manifest_sha256[:16]}",
            request_id=request.request_id,
            entries=frozen_entries,
            manifest_sha256=manifest_sha256,
        )

    @staticmethod
    def _digest_payload(
        request_id: str,
        entries: tuple[ContextEntry, ...],
    ) -> dict[str, Any]:
        return {
            "schema_version": CONTEXT_SCHEMA,
            "request_id": request_id,
            "entries": [asdict(entry.provenance()) for entry in entries],
        }

    def __post_init__(self) -> None:
        _require_text(self.manifest_id, "manifest_id")
        _require_text(self.request_id, "request_id")
        if self.schema_version != CONTEXT_SCHEMA:
            raise ValueError(f"unsupported context schema: {self.schema_version}")
        if not self.entries:
            raise ValueError("a context manifest requires at least one entry")
        entry_ids = [entry.entry_id for entry in self.entries]
        if len(set(entry_ids)) != len(entry_ids):
            raise ValueError("context entry IDs must be unique")
        expected = _digest(self._digest_payload(self.request_id, self.entries))
        if self.manifest_sha256 != expected:
            raise ValueError("context manifest digest mismatch")
        if self.manifest_id != f"ctx-{expected[:16]}":
            raise ValueError("context manifest ID does not match its digest")

    @property
    def provenance(self) -> tuple[ProvenanceRef, ...]:
        return tuple(entry.provenance() for entry in self.entries)


@dataclass(frozen=True, slots=True)
class ReasoningClaim:
    """A backend proposal explicitly bound to context entry IDs."""

    claim_id: str
    text: str
    evidence_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_text(self.claim_id, "claim_id")
        _require_text(self.text, "text")
        if any(not isinstance(ref, str) or not ref.strip() for ref in self.evidence_refs):
            raise ValueError("evidence references must be non-empty text")
        if len(set(self.evidence_refs)) != len(self.evidence_refs):
            raise ValueError("evidence references must be unique")


@dataclass(frozen=True, slots=True)
class ReasoningResult:
    """Untrusted candidate output returned by a ReasoningBackend."""

    result_id: str
    request_id: str
    manifest_id: str
    backend_id: str
    output: str
    claims: tuple[ReasoningClaim, ...]
    schema_version: str = RESULT_SCHEMA

    def __post_init__(self) -> None:
        for field_name in (
            "result_id",
            "request_id",
            "manifest_id",
            "backend_id",
            "output",
        ):
            _require_text(getattr(self, field_name), field_name)
        if self.schema_version != RESULT_SCHEMA:
            raise ValueError(f"unsupported result schema: {self.schema_version}")
        if not self.claims:
            raise ValueError("a reasoning result requires at least one claim")
        claim_ids = [claim.claim_id for claim in self.claims]
        if len(set(claim_ids)) != len(claim_ids):
            raise ValueError("claim IDs must be unique")


@dataclass(frozen=True, slots=True)
class ValidationReport:
    """Validation outcome kept separate from the backend result."""

    valid: bool
    checks: tuple[str, ...]
    errors: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.valid == bool(self.errors):
            raise ValueError("validation status and errors disagree")


@dataclass(frozen=True, slots=True)
class OrientationResponse:
    """Validated boundary response; never a canonical Kernel decision."""

    response_id: str
    request_id: str
    manifest_id: str
    backend_id: str
    backend_result_id: str
    validated: bool
    candidate_output: str | None
    claims: tuple[ReasoningClaim, ...]
    provenance: tuple[ProvenanceRef, ...]
    validation: ValidationReport
    canonical_effects: tuple[str, ...] = ()
    schema_version: str = RESPONSE_SCHEMA

    def __post_init__(self) -> None:
        for field_name in (
            "response_id",
            "request_id",
            "manifest_id",
            "backend_id",
            "backend_result_id",
        ):
            _require_text(getattr(self, field_name), field_name)
        if self.schema_version != RESPONSE_SCHEMA:
            raise ValueError(f"unsupported response schema: {self.schema_version}")
        if self.validated != self.validation.valid:
            raise ValueError("response and validation status disagree")
        if self.validated and self.candidate_output is None:
            raise ValueError("validated response requires candidate output")
        if not self.validated and (self.candidate_output is not None or self.claims):
            raise ValueError("rejected response cannot expose candidate output")
        if self.canonical_effects:
            raise ValueError("Phase 1A responses cannot contain canonical effects")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @property
    def provenance_ids(self) -> tuple[str, ...]:
        return tuple(reference.entry_id for reference in self.provenance)


def response_id_for(result: ReasoningResult, validation: ValidationReport) -> str:
    payload = {
        "result_id": result.result_id,
        "valid": validation.valid,
        "checks": validation.checks,
        "errors": validation.errors,
    }
    return f"rsp-{_digest(payload)[:16]}"


def result_id_for(*, request_id: str, manifest_id: str, backend_id: str) -> str:
    return f"res-{_digest([request_id, manifest_id, backend_id])[:16]}"
