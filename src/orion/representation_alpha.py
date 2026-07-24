"""First executable, deterministic ORION Representation profile.

This module implements exactly one internal Alpha profile:

    confirmed, pre-resolved local text
      -> exact-text projection
      -> immutable text representation
      -> external conformance result

It does not resolve source authority, perform Orientation, create Evidence,
bind reports, or change any Version 1 public contract.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from typing import Any, Mapping

from .contracts import ContextEntry, ProvenanceRef


CONFIRMED_SOURCE_SCHEMA = "orion.confirmed-local-source/0.1-alpha"
EXACT_TEXT_REPRESENTATION_SCHEMA = "orion.representation/exact-text/0.1-alpha"
EXACT_TEXT_PROJECTION_ID = "orion.projection/exact-text"
EXACT_TEXT_PROJECTION_VERSION = "0.1-alpha"
EXACT_TEXT_RENDERER_ID = "orion.renderer/exact-text"
EXACT_TEXT_RENDERER_VERSION = "0.1-alpha"
TEXT_MEDIA_TYPE = "text/plain;charset=utf-8"
TEXT_TARGET_DOMAIN = "orion.representation.text-exact"
WHOLE_FRAGMENT = "whole"
NO_LOSS = ("none",)


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _digest(value: Any) -> str:
    return sha256(_canonical_bytes(value)).hexdigest()


def _content_digest(content: str) -> str:
    return sha256(content.encode("utf-8")).hexdigest()


def _require_text(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be non-empty text")


def _require_digest(value: str, field_name: str) -> None:
    if not isinstance(value, str) or len(value) != 64 or any(
        character not in "0123456789abcdef" for character in value
    ):
        raise ValueError(f"{field_name} must be a lowercase SHA-256 digest")


def _confirmation_digest_payload(
    *,
    entry_id: str,
    revision: str,
    confirmed_by: str,
    confirmed_revision: int,
    fragment_ref: str,
) -> dict[str, object]:
    return {
        "entry_id": entry_id,
        "revision": revision,
        "confirmed_by": confirmed_by,
        "confirmed_revision": confirmed_revision,
        "fragment_ref": fragment_ref,
    }


@dataclass(frozen=True, slots=True)
class ConfirmedLocalSource:
    """Human-confirmed, pre-resolved local text entering the Renderer boundary."""

    orientation_object_id: str
    orientation_object_version: str
    entry: ContextEntry
    confirmed_by: str
    confirmed_revision: int
    confirmation_id: str
    fragment_ref: str = WHOLE_FRAGMENT
    media_type: str = TEXT_MEDIA_TYPE
    schema_version: str = CONFIRMED_SOURCE_SCHEMA

    @classmethod
    def from_resolved(
        cls,
        *,
        orientation_object_id: str,
        orientation_object_version: str,
        entry_id: str,
        source_owner: str,
        source_ref: str,
        source_version: str,
        content: str,
        integrity_sha256: str,
        confirmed_by: str,
        confirmed_revision: int,
        confirmation_id: str,
        fragment_ref: str = WHOLE_FRAGMENT,
    ) -> "ConfirmedLocalSource":
        return cls(
            orientation_object_id=orientation_object_id,
            orientation_object_version=orientation_object_version,
            entry=ContextEntry(
                entry_id=entry_id,
                owner=source_owner,
                source_ref=source_ref,
                revision=source_version,
                content=content,
                content_sha256=integrity_sha256,
            ),
            confirmed_by=confirmed_by,
            confirmed_revision=confirmed_revision,
            confirmation_id=confirmation_id,
            fragment_ref=fragment_ref,
        )

    def __post_init__(self) -> None:
        for field_name in (
            "orientation_object_id",
            "orientation_object_version",
            "confirmed_by",
            "confirmation_id",
            "fragment_ref",
            "media_type",
        ):
            _require_text(getattr(self, field_name), field_name)
        if not isinstance(self.entry, ContextEntry):
            raise TypeError("entry must be a ContextEntry")
        self.entry.__post_init__()
        if type(self.confirmed_revision) is not int or self.confirmed_revision < 1:
            raise ValueError("confirmed_revision must be a positive integer")
        if self.schema_version != CONFIRMED_SOURCE_SCHEMA:
            raise ValueError(f"unsupported confirmed source schema: {self.schema_version}")
        if self.media_type != TEXT_MEDIA_TYPE:
            raise ValueError(f"unsupported confirmed source media type: {self.media_type}")
        expected_revision = f"sha256:{self.entry.content_sha256}"
        if self.entry.revision != expected_revision:
            raise ValueError("source revision must identify the exact UTF-8 content")
        confirmation_sha256 = _digest(
            _confirmation_digest_payload(
                entry_id=self.entry.entry_id,
                revision=self.entry.revision,
                confirmed_by=self.confirmed_by,
                confirmed_revision=self.confirmed_revision,
                fragment_ref=self.fragment_ref,
            )
        )
        if self.confirmation_id != f"confirmation-{confirmation_sha256[:16]}":
            raise ValueError("confirmation identity does not match confirmed source")
        if self.fragment_ref != WHOLE_FRAGMENT:
            raise ValueError("the Alpha profile supports only the whole-text fragment")


@dataclass(frozen=True, slots=True)
class ExactTextProjection:
    """One explicit, lossless Projection profile for confirmed local text."""

    projection_id: str = EXACT_TEXT_PROJECTION_ID
    projection_version: str = EXACT_TEXT_PROJECTION_VERSION
    source_media_type: str = TEXT_MEDIA_TYPE
    target_domain: str = TEXT_TARGET_DOMAIN
    declared_lossiness: tuple[str, ...] = NO_LOSS

    def __post_init__(self) -> None:
        object.__setattr__(self, "declared_lossiness", tuple(self.declared_lossiness))
        for field_name in (
            "projection_id",
            "projection_version",
            "source_media_type",
            "target_domain",
        ):
            _require_text(getattr(self, field_name), field_name)
        if self.source_media_type != TEXT_MEDIA_TYPE:
            raise ValueError("the exact-text Projection accepts only UTF-8 plain text")
        if tuple(self.declared_lossiness) != NO_LOSS:
            raise ValueError("the exact-text Alpha Projection must declare no loss")


@dataclass(frozen=True, slots=True)
class ExactTextPayload:
    """Exact selected text emitted in the named Representation domain."""

    media_type: str
    fragment_ref: str
    content: str
    content_sha256: str

    def __post_init__(self) -> None:
        if self.media_type != TEXT_MEDIA_TYPE:
            raise ValueError("unsupported Representation payload media type")
        _require_text(self.fragment_ref, "fragment_ref")
        _require_text(self.content, "content")
        _require_digest(self.content_sha256, "content_sha256")
        if self.content_sha256 != _content_digest(self.content):
            raise ValueError("Representation payload content digest mismatch")


@dataclass(frozen=True, slots=True)
class RepresentationProvenanceStep:
    """One deterministic, authority-bounded step in Representation provenance."""

    sequence: int
    step_id: str
    step_kind: str
    owner: str
    input_refs: tuple[str, ...]
    output_ref: str
    declared_lossiness: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "input_refs", tuple(self.input_refs))
        object.__setattr__(
            self,
            "declared_lossiness",
            tuple(self.declared_lossiness),
        )
        if type(self.sequence) is not int or self.sequence < 1:
            raise ValueError("provenance sequence must be a positive integer")
        for field_name in ("step_id", "step_kind", "owner", "output_ref"):
            _require_text(getattr(self, field_name), field_name)
        if not self.input_refs or any(
            not isinstance(item, str) or not item.strip() for item in self.input_refs
        ):
            raise ValueError("provenance input_refs must contain non-empty text")
        if not self.declared_lossiness:
            raise ValueError("provenance must declare lossiness")


@dataclass(frozen=True, slots=True)
class ImmutableTextRepresentation:
    """Content-addressed output of the exact-text Renderer."""

    representation_id: str
    representation_version: str
    orientation_object_id: str
    orientation_object_version: str
    source: ProvenanceRef
    fragment_ref: str
    projection: ExactTextProjection
    renderer_id: str
    renderer_version: str
    payload: ExactTextPayload
    provenance: tuple[RepresentationProvenanceStep, ...]
    declared_lossiness: tuple[str, ...]
    representation_sha256: str
    schema_version: str = EXACT_TEXT_REPRESENTATION_SCHEMA

    def __post_init__(self) -> None:
        object.__setattr__(self, "provenance", tuple(self.provenance))
        object.__setattr__(
            self,
            "declared_lossiness",
            tuple(self.declared_lossiness),
        )
        for field_name in (
            "representation_id",
            "representation_version",
            "orientation_object_id",
            "orientation_object_version",
            "fragment_ref",
            "renderer_id",
            "renderer_version",
        ):
            _require_text(getattr(self, field_name), field_name)
        if self.schema_version != EXACT_TEXT_REPRESENTATION_SCHEMA:
            raise ValueError(f"unsupported Representation schema: {self.schema_version}")
        if not isinstance(self.source, ProvenanceRef):
            raise TypeError("source must be a ProvenanceRef")
        self.source.__post_init__()
        if not isinstance(self.projection, ExactTextProjection):
            raise TypeError("projection must be an ExactTextProjection")
        self.projection.__post_init__()
        if not isinstance(self.payload, ExactTextPayload):
            raise TypeError("payload must be an ExactTextPayload")
        self.payload.__post_init__()
        for step in self.provenance:
            if not isinstance(step, RepresentationProvenanceStep):
                raise TypeError("provenance entries must be RepresentationProvenanceStep")
            step.__post_init__()
        if tuple(self.declared_lossiness) != tuple(self.projection.declared_lossiness):
            raise ValueError("Representation and Projection lossiness disagree")
        if not self.provenance:
            raise ValueError("Representation provenance must not be empty")
        if tuple(step.sequence for step in self.provenance) != tuple(
            range(1, len(self.provenance) + 1)
        ):
            raise ValueError("Representation provenance sequence must be contiguous")
        _require_digest(self.representation_sha256, "representation_sha256")
        if self.representation_version != f"sha256:{self.representation_sha256}":
            raise ValueError("Representation version must identify its canonical payload")


@dataclass(frozen=True, slots=True)
class ExactTextRenderer:
    """Read-only deterministic execution of the exact-text Projection."""

    renderer_id: str = EXACT_TEXT_RENDERER_ID
    renderer_version: str = EXACT_TEXT_RENDERER_VERSION
    projection: ExactTextProjection = ExactTextProjection()

    def __post_init__(self) -> None:
        _require_text(self.renderer_id, "renderer_id")
        _require_text(self.renderer_version, "renderer_version")
        if not isinstance(self.projection, ExactTextProjection):
            raise TypeError("projection must be an ExactTextProjection")

    def render(self, source: ConfirmedLocalSource) -> ImmutableTextRepresentation:
        """Project one confirmed source without I/O, inference, or validation claims."""

        if not isinstance(source, ConfirmedLocalSource):
            raise TypeError("source must be a ConfirmedLocalSource")
        source.__post_init__()
        representation_id = self._representation_id(source)
        payload = ExactTextPayload(
            media_type=source.media_type,
            fragment_ref=source.fragment_ref,
            content=source.entry.content,
            content_sha256=source.entry.content_sha256,
        )
        provenance = (
            RepresentationProvenanceStep(
                sequence=1,
                step_id=source.confirmation_id,
                step_kind="human_confirmation",
                owner=source.confirmed_by,
                input_refs=(
                    f"{source.entry.entry_id}@{source.entry.revision}",
                    f"{source.orientation_object_id}@{source.orientation_object_version}",
                ),
                output_ref=f"confirmed:{source.entry.entry_id}@{source.entry.revision}",
                declared_lossiness=NO_LOSS,
            ),
            RepresentationProvenanceStep(
                sequence=2,
                step_id=f"{self.renderer_id}@{self.renderer_version}",
                step_kind="deterministic_projection",
                owner="ORION Representation Boundary",
                input_refs=(
                    f"confirmed:{source.entry.entry_id}@{source.entry.revision}",
                    f"{self.projection.projection_id}@{self.projection.projection_version}",
                ),
                output_ref=representation_id,
                declared_lossiness=self.projection.declared_lossiness,
            ),
        )
        representation_basis = self._representation_basis(
            source=source,
            representation_id=representation_id,
            payload=payload,
            provenance=provenance,
        )
        representation_sha256 = _digest(representation_basis)
        return ImmutableTextRepresentation(
            representation_id=representation_id,
            representation_version=f"sha256:{representation_sha256}",
            orientation_object_id=source.orientation_object_id,
            orientation_object_version=source.orientation_object_version,
            source=source.entry.provenance(),
            fragment_ref=source.fragment_ref,
            projection=self.projection,
            renderer_id=self.renderer_id,
            renderer_version=self.renderer_version,
            payload=payload,
            provenance=provenance,
            declared_lossiness=self.projection.declared_lossiness,
            representation_sha256=representation_sha256,
        )

    def _representation_id(self, source: ConfirmedLocalSource) -> str:
        identity_basis = {
            "orientation_object_id": source.orientation_object_id,
            "source_entry_id": source.entry.entry_id,
            "fragment_ref": source.fragment_ref,
            "projection_id": self.projection.projection_id,
            "renderer_id": self.renderer_id,
            "target_domain": self.projection.target_domain,
        }
        return f"representation-{_digest(identity_basis)[:16]}"

    def _representation_basis(
        self,
        *,
        source: ConfirmedLocalSource,
        representation_id: str,
        payload: ExactTextPayload,
        provenance: tuple[RepresentationProvenanceStep, ...],
    ) -> dict[str, object]:
        return {
            "schema_version": EXACT_TEXT_REPRESENTATION_SCHEMA,
            "representation_id": representation_id,
            "orientation_object_id": source.orientation_object_id,
            "orientation_object_version": source.orientation_object_version,
            "source": asdict(source.entry.provenance()),
            "fragment_ref": source.fragment_ref,
            "projection": asdict(self.projection),
            "renderer_id": self.renderer_id,
            "renderer_version": self.renderer_version,
            "payload": asdict(payload),
            "provenance": [asdict(step) for step in provenance],
            "declared_lossiness": self.projection.declared_lossiness,
        }


@dataclass(frozen=True, slots=True)
class RepresentationConformance:
    """External conformance result; it is not produced by the Renderer."""

    valid: bool
    checks: tuple[str, ...]
    errors: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.valid == bool(self.errors):
            raise ValueError("conformance status and errors disagree")
        if not self.checks:
            raise ValueError("conformance must record executed checks")


def validate_representation(
    source: ConfirmedLocalSource,
    representation: ImmutableTextRepresentation,
    *,
    renderer: ExactTextRenderer | None = None,
) -> RepresentationConformance:
    """Validate identity, traceability, integrity, and deterministic replay."""

    active_renderer = renderer or ExactTextRenderer()
    checks: list[str] = []
    errors: list[str] = []

    def check(name: str, condition: bool, error: str) -> None:
        checks.append(name)
        if not condition:
            errors.append(error)

    try:
        source.__post_init__()
        checks.append("confirmed_source_valid")
    except (TypeError, ValueError) as exc:
        checks.append("confirmed_source_valid")
        errors.append(str(exc))

    try:
        representation.__post_init__()
        checks.append("representation_shape_valid")
    except (TypeError, ValueError) as exc:
        checks.append("representation_shape_valid")
        errors.append(str(exc))

    try:
        expected = active_renderer.render(source)
    except (TypeError, ValueError) as exc:
        expected = None
        errors.append(f"deterministic replay unavailable: {exc}")
    check(
        "deterministic_replay",
        expected is not None and representation == expected,
        "Representation differs from deterministic replay",
    )
    check(
        "source_traceback",
        representation.source == source.entry.provenance()
        and representation.fragment_ref == source.fragment_ref,
        "Representation does not trace to the confirmed source",
    )
    check(
        "orientation_object_preserved",
        (
            representation.orientation_object_id,
            representation.orientation_object_version,
        )
        == (
            source.orientation_object_id,
            source.orientation_object_version,
        ),
        "Orientation Object identity was not preserved",
    )
    check(
        "payload_integrity",
        representation.payload.content_sha256
        == _content_digest(representation.payload.content),
        "Representation payload integrity mismatch",
    )
    check(
        "projection_identity",
        representation.projection == active_renderer.projection,
        "Representation Projection does not match the executing profile",
    )
    check(
        "renderer_identity",
        (
            representation.renderer_id,
            representation.renderer_version,
        )
        == (
            active_renderer.renderer_id,
            active_renderer.renderer_version,
        ),
        "Representation Renderer identity does not match",
    )
    check(
        "lossiness_declared",
        representation.declared_lossiness == NO_LOSS
        and all(step.declared_lossiness for step in representation.provenance),
        "Representation lossiness is absent or inconsistent",
    )
    serialized_shape = asdict(representation)
    forbidden = {
        "evidence_class",
        "relationship",
        "report_id",
        "target_path",
        "traceability",
    }
    check(
        "no_orientation_or_evidence_semantics",
        forbidden.isdisjoint(_nested_keys(serialized_shape)),
        "Representation contains Orientation or Evidence Binding semantics",
    )
    return RepresentationConformance(not errors, tuple(checks), tuple(errors))


def confirmed_source_from_mapping(value: Mapping[str, object]) -> ConfirmedLocalSource:
    """Construct and verify an already resolved declaration without source I/O."""

    if not isinstance(value, Mapping):
        raise ValueError("confirmed source fixture must be a JSON object")
    source_value = value.get("source")
    confirmation_value = value.get("confirmation")
    if not isinstance(source_value, Mapping) or not isinstance(
        confirmation_value, Mapping
    ):
        raise ValueError("fixture source and confirmation must be JSON objects")
    source = ConfirmedLocalSource.from_resolved(
        orientation_object_id=_mapping_text(value, "orientation_object_id"),
        orientation_object_version=_mapping_text(value, "orientation_object_version"),
        entry_id=_mapping_text(source_value, "entry_id"),
        source_owner=_mapping_text(source_value, "source_owner"),
        source_ref=_mapping_text(source_value, "source_ref"),
        source_version=_mapping_text(source_value, "source_version"),
        content=_mapping_text(source_value, "content", allow_whitespace=True),
        integrity_sha256=_mapping_text(source_value, "integrity_sha256"),
        confirmed_by=_mapping_text(confirmation_value, "confirmed_by"),
        confirmed_revision=_mapping_positive_int(
            confirmation_value,
            "confirmed_revision",
        ),
        confirmation_id=_mapping_text(confirmation_value, "confirmation_id"),
        fragment_ref=_mapping_text(source_value, "fragment_ref"),
    )
    if source.schema_version != _mapping_text(value, "schema_version"):
        raise ValueError("fixture schema version does not match the Alpha profile")
    if source.media_type != _mapping_text(source_value, "media_type"):
        raise ValueError("fixture media type does not match the Alpha profile")
    return source


def representation_as_dict(
    representation: ImmutableTextRepresentation,
) -> dict[str, object]:
    """Return the deterministic serialized shape used by the executable proof."""

    return asdict(representation)


def _nested_keys(value: object) -> set[str]:
    if isinstance(value, Mapping):
        return set(value).union(
            *((
                _nested_keys(item)
                for item in value.values()
            )),
        )
    if isinstance(value, (list, tuple)):
        return set().union(*(_nested_keys(item) for item in value))
    return set()


def _mapping_text(
    value: Mapping[str, object],
    field_name: str,
    *,
    allow_whitespace: bool = False,
) -> str:
    item = value.get(field_name)
    if not isinstance(item, str) or (
        not allow_whitespace and not item.strip()
    ) or (allow_whitespace and not item):
        raise ValueError(f"{field_name} must be non-empty text")
    return item


def _mapping_positive_int(value: Mapping[str, object], field_name: str) -> int:
    item = value.get(field_name)
    if type(item) is not int or item < 1:
        raise ValueError(f"{field_name} must be a positive integer")
    return item
