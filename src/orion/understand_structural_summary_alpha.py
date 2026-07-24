"""Deterministic Structural Summary inside UNDERSTAND Stage 2.

The Summary consumes only one accepted immutable Declared Source Element
Inventory. It describes declared organization without source access, parsing,
Projection, Rendering, Statistics, relations, or semantic interpretation.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from typing import Mapping

from orion.understand_source_element_inventory_alpha import (
    ALPHA_ELEMENT_KINDS,
    CANONICAL_STAGE,
    OPERATOR_ID,
    OPERATOR_VERSION,
    DeclaredSourceElementInventoryDiagnostic,
    canonical_inventory_bytes,
)


SUMMARY_DIAGNOSTIC_VERSION = "0.1-alpha"
RESPONSIBILITY = "structural_summary"
INPUT_BOUNDARY = "declared_source_element_inventory"
STOP_AFTER_STRUCTURAL_SUMMARY = "after_structural_summary"
PROFILE_V1_VOCABULARY = ALPHA_ELEMENT_KINDS


def _canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _digest(value: object) -> str:
    return sha256(_canonical_bytes(value)).hexdigest()


def _require_text(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{field_name} must be exact non-empty text")


def _require_sha256_ref(value: str, field_name: str) -> None:
    _require_text(value, field_name)
    prefix = "sha256:"
    digest = value[len(prefix) :] if value.startswith(prefix) else ""
    if len(digest) != 64 or any(
        character not in "0123456789abcdef" for character in digest
    ):
        raise ValueError(f"{field_name} must be a SHA-256 reference")


@dataclass(frozen=True, slots=True)
class DeclaredHeadingSummary:
    """One heading declaration copied from its exact inventory entry."""

    element_id: str
    element_kind: str
    ordinal: int
    level: int

    def __post_init__(self) -> None:
        _require_text(self.element_id, "element_id")
        if self.element_kind not in ("atx_heading", "setext_heading"):
            raise ValueError("heading summary accepts only declared headings")
        if type(self.ordinal) is not int or self.ordinal < 0:
            raise ValueError("heading ordinal must be a non-negative integer")
        maximum_level = 6 if self.element_kind == "atx_heading" else 2
        if (
            type(self.level) is not int
            or self.level < 1
            or self.level > maximum_level
        ):
            raise ValueError("heading level is outside its declared kind")


@dataclass(frozen=True, slots=True)
class StructuralSummaryDiagnostic:
    """Immutable internal synopsis of already-declared document structure."""

    summary_id: str
    diagnostic_version: str
    canonical_stage: str
    operator_id: str
    operator_version: str
    responsibility: str
    input_boundary: str
    input_inventory_ref: str
    orientation_object_id: str
    orientation_object_version: str
    representation_id: str
    representation_version: str
    representation_integrity: str
    source_id: str
    source_revision: str
    source_integrity: str
    source_boundary: str
    total_declared_element_count: int
    ordered_element_kinds: tuple[str, ...]
    declared_headings: tuple[DeclaredHeadingSummary, ...]
    first_canonical_ordinal: int
    final_canonical_ordinal: int
    declared_block_kinds: tuple[str, ...]
    absent_block_kinds: tuple[str, ...]
    profile_v1_vocabulary: tuple[str, ...]
    responsibility_state: str
    canonical_stage_state: str
    stop: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "ordered_element_kinds",
            tuple(self.ordered_element_kinds),
        )
        object.__setattr__(
            self,
            "declared_headings",
            tuple(self.declared_headings),
        )
        object.__setattr__(
            self,
            "declared_block_kinds",
            tuple(self.declared_block_kinds),
        )
        object.__setattr__(
            self,
            "absent_block_kinds",
            tuple(self.absent_block_kinds),
        )
        object.__setattr__(
            self,
            "profile_v1_vocabulary",
            tuple(self.profile_v1_vocabulary),
        )
        for field_name in (
            "summary_id",
            "diagnostic_version",
            "canonical_stage",
            "operator_id",
            "operator_version",
            "responsibility",
            "input_boundary",
            "orientation_object_id",
            "orientation_object_version",
            "representation_id",
            "representation_version",
            "representation_integrity",
            "source_id",
            "source_revision",
            "source_integrity",
            "source_boundary",
            "responsibility_state",
            "canonical_stage_state",
            "stop",
        ):
            _require_text(getattr(self, field_name), field_name)
        _require_sha256_ref(self.input_inventory_ref, "input_inventory_ref")
        if (
            type(self.total_declared_element_count) is not int
            or self.total_declared_element_count < 1
        ):
            raise ValueError("total declared element count must be positive")
        if len(self.ordered_element_kinds) != self.total_declared_element_count:
            raise ValueError("ordered element kinds do not match total count")
        if any(
            kind not in PROFILE_V1_VOCABULARY
            for kind in self.ordered_element_kinds
        ):
            raise ValueError("ordered element kind is outside Profile v1")
        for heading in self.declared_headings:
            if not isinstance(heading, DeclaredHeadingSummary):
                raise TypeError("declared headings must be immutable summaries")
            heading.__post_init__()
        if self.first_canonical_ordinal != 0:
            raise ValueError("first canonical ordinal must be zero")
        if (
            type(self.final_canonical_ordinal) is not int
            or self.final_canonical_ordinal
            != self.total_declared_element_count - 1
        ):
            raise ValueError("final canonical ordinal does not match count")
        if self.profile_v1_vocabulary != PROFILE_V1_VOCABULARY:
            raise ValueError("Summary vocabulary differs from Profile v1")
        if len(set(self.declared_block_kinds)) != len(
            self.declared_block_kinds
        ):
            raise ValueError("declared block coverage contains duplicates")
        if any(
            kind not in PROFILE_V1_VOCABULARY
            for kind in self.declared_block_kinds
        ):
            raise ValueError("declared block coverage is outside Profile v1")
        if self.declared_block_kinds != tuple(
            dict.fromkeys(self.ordered_element_kinds)
        ):
            raise ValueError("declared block coverage must preserve first use")
        if self.absent_block_kinds != tuple(
            kind
            for kind in PROFILE_V1_VOCABULARY
            if kind not in self.declared_block_kinds
        ):
            raise ValueError("absent block coverage does not match Profile v1")


@dataclass(frozen=True, slots=True)
class StructuralSummaryConformance:
    """External field-by-field verification of one Structural Summary."""

    valid: bool
    checks: tuple[str, ...]
    errors: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "checks", tuple(self.checks))
        object.__setattr__(self, "errors", tuple(self.errors))
        if type(self.valid) is not bool:
            raise TypeError("valid must be boolean")
        if any(not isinstance(check, str) or not check for check in self.checks):
            raise ValueError("conformance checks must be non-empty text")
        if any(not isinstance(error, str) or not error for error in self.errors):
            raise ValueError("conformance errors must be non-empty text")
        if self.valid != (not self.errors):
            raise ValueError("conformance validity must match its errors")


def _inventory_ref(
    inventory: DeclaredSourceElementInventoryDiagnostic,
) -> str:
    return f"sha256:{sha256(canonical_inventory_bytes(inventory)).hexdigest()}"


def _summary_identity(input_inventory_ref: str) -> str:
    basis = {
        "diagnostic_version": SUMMARY_DIAGNOSTIC_VERSION,
        "operator_id": OPERATOR_ID,
        "operator_version": OPERATOR_VERSION,
        "responsibility": RESPONSIBILITY,
        "input_inventory_ref": input_inventory_ref,
    }
    return f"structural-summary-{_digest(basis)[:24]}"


def summarize_declared_structure(
    inventory: DeclaredSourceElementInventoryDiagnostic,
) -> StructuralSummaryDiagnostic:
    """Derive only declared organizational fields from one Inventory."""

    if not isinstance(inventory, DeclaredSourceElementInventoryDiagnostic):
        raise TypeError(
            "Structural Summary requires an immutable Source Element Inventory"
        )
    inventory.__post_init__()
    input_inventory_ref = _inventory_ref(inventory)
    ordered_element_kinds = tuple(
        element.element_kind for element in inventory.elements
    )
    declared_headings = tuple(
        DeclaredHeadingSummary(
            element_id=element.element_id,
            element_kind=element.element_kind,
            ordinal=element.ordinal,
            level=element.level,
        )
        for element in inventory.elements
        if element.element_kind in ("atx_heading", "setext_heading")
        and element.level is not None
    )
    declared_block_kinds = tuple(dict.fromkeys(ordered_element_kinds))
    absent_block_kinds = tuple(
        kind
        for kind in PROFILE_V1_VOCABULARY
        if kind not in declared_block_kinds
    )
    summary = StructuralSummaryDiagnostic(
        summary_id=_summary_identity(input_inventory_ref),
        diagnostic_version=SUMMARY_DIAGNOSTIC_VERSION,
        canonical_stage=CANONICAL_STAGE,
        operator_id=OPERATOR_ID,
        operator_version=OPERATOR_VERSION,
        responsibility=RESPONSIBILITY,
        input_boundary=INPUT_BOUNDARY,
        input_inventory_ref=input_inventory_ref,
        orientation_object_id=inventory.orientation_object_id,
        orientation_object_version=inventory.orientation_object_version,
        representation_id=inventory.representation_id,
        representation_version=inventory.representation_version,
        representation_integrity=inventory.representation_integrity,
        source_id=inventory.source_id,
        source_revision=inventory.source_revision,
        source_integrity=inventory.source_integrity,
        source_boundary=inventory.source_boundary,
        total_declared_element_count=inventory.ordered_element_count,
        ordered_element_kinds=ordered_element_kinds,
        declared_headings=declared_headings,
        first_canonical_ordinal=inventory.elements[0].ordinal,
        final_canonical_ordinal=inventory.elements[-1].ordinal,
        declared_block_kinds=declared_block_kinds,
        absent_block_kinds=absent_block_kinds,
        profile_v1_vocabulary=PROFILE_V1_VOCABULARY,
        responsibility_state="completed",
        canonical_stage_state="incomplete",
        stop=STOP_AFTER_STRUCTURAL_SUMMARY,
    )
    summary.__post_init__()
    return summary


def validate_structural_summary(
    inventory: DeclaredSourceElementInventoryDiagnostic,
    summary: StructuralSummaryDiagnostic,
) -> StructuralSummaryConformance:
    """Verify every Summary field against its one immutable input Inventory."""

    checks: list[str] = []
    errors: list[str] = []

    def check(name: str, condition: bool, error: str) -> None:
        checks.append(name)
        if not condition:
            errors.append(error)

    try:
        inventory.__post_init__()
        checks.append("input_inventory_valid")
    except (AttributeError, TypeError, ValueError) as exc:
        checks.append("input_inventory_valid")
        errors.append(str(exc))

    try:
        summary.__post_init__()
        checks.append("summary_shape_valid")
    except (AttributeError, TypeError, ValueError) as exc:
        checks.append("summary_shape_valid")
        errors.append(str(exc))

    try:
        expected = summarize_declared_structure(inventory)
    except (AttributeError, TypeError, ValueError) as exc:
        expected = None
        errors.append(f"deterministic derivation unavailable: {exc}")

    check(
        "deterministic_derivation",
        expected is not None and summary == expected,
        "Summary differs from deterministic Inventory derivation",
    )
    check(
        "diagnostic_identity_and_version",
        summary.summary_id == _summary_identity(summary.input_inventory_ref)
        and summary.diagnostic_version == SUMMARY_DIAGNOSTIC_VERSION,
        "Summary diagnostic identity or version is not deterministic",
    )
    check(
        "responsibility_and_stop",
        summary.canonical_stage == CANONICAL_STAGE
        and summary.operator_id == OPERATOR_ID
        and summary.operator_version == OPERATOR_VERSION
        and summary.responsibility == RESPONSIBILITY
        and summary.input_boundary == INPUT_BOUNDARY
        and summary.responsibility_state == "completed"
        and summary.canonical_stage_state == "incomplete"
        and summary.stop == STOP_AFTER_STRUCTURAL_SUMMARY,
        "Summary responsibility or STOP boundary changed",
    )
    check(
        "inventory_reference",
        summary.input_inventory_ref == _inventory_ref(inventory),
        "Summary does not identify the exact input Inventory",
    )
    check(
        "orientation_object_lineage",
        (
            summary.orientation_object_id,
            summary.orientation_object_version,
        )
        == (
            inventory.orientation_object_id,
            inventory.orientation_object_version,
        ),
        "Orientation Object lineage was not preserved",
    )
    check(
        "representation_lineage",
        (
            summary.representation_id,
            summary.representation_version,
            summary.representation_integrity,
        )
        == (
            inventory.representation_id,
            inventory.representation_version,
            inventory.representation_integrity,
        ),
        "Representation lineage was not preserved",
    )
    check(
        "source_lineage",
        (
            summary.source_id,
            summary.source_revision,
            summary.source_integrity,
            summary.source_boundary,
        )
        == (
            inventory.source_id,
            inventory.source_revision,
            inventory.source_integrity,
            inventory.source_boundary,
        ),
        "source lineage was not preserved",
    )
    check(
        "ordered_structure",
        summary.total_declared_element_count == inventory.ordered_element_count
        and summary.ordered_element_kinds
        == tuple(element.element_kind for element in inventory.elements)
        and summary.first_canonical_ordinal == inventory.elements[0].ordinal
        and summary.final_canonical_ordinal == inventory.elements[-1].ordinal,
        "canonical Inventory order was not preserved",
    )
    check(
        "heading_declarations",
        summary.declared_headings
        == tuple(
            DeclaredHeadingSummary(
                element_id=element.element_id,
                element_kind=element.element_kind,
                ordinal=element.ordinal,
                level=element.level,
            )
            for element in inventory.elements
            if element.element_kind in ("atx_heading", "setext_heading")
            and element.level is not None
        ),
        "declared headings differ from Inventory declarations",
    )
    expected_declared_kinds = tuple(
        dict.fromkeys(element.element_kind for element in inventory.elements)
    )
    check(
        "profile_vocabulary_coverage",
        summary.declared_block_kinds == expected_declared_kinds
        and summary.absent_block_kinds
        == tuple(
            kind
            for kind in PROFILE_V1_VOCABULARY
            if kind not in expected_declared_kinds
        )
        and summary.profile_v1_vocabulary == PROFILE_V1_VOCABULARY,
        "Summary vocabulary coverage differs from Inventory and Profile v1",
    )
    forbidden = {
        "claim",
        "claims",
        "concept",
        "concepts",
        "confidence",
        "content",
        "entities",
        "entity",
        "evidence",
        "intent",
        "meaning",
        "relations",
        "semantic",
        "statistics",
        "summary_text",
        "topic",
        "topics",
    }
    check(
        "no_semantic_or_downstream_fields",
        forbidden.isdisjoint(_nested_keys(asdict(summary))),
        "Summary contains semantic or downstream fields",
    )
    return StructuralSummaryConformance(not errors, tuple(checks), tuple(errors))


def structural_summary_as_dict(
    summary: StructuralSummaryDiagnostic,
) -> dict[str, object]:
    """Return the deterministic internal Summary proof shape."""

    summary.__post_init__()
    return asdict(summary)


def canonical_structural_summary_bytes(
    summary: StructuralSummaryDiagnostic,
) -> bytes:
    """Return stable bytes for deterministic replay verification."""

    return _canonical_bytes(structural_summary_as_dict(summary))


def _nested_keys(value: object) -> set[str]:
    if isinstance(value, Mapping):
        return set(value).union(
            *(_nested_keys(item) for item in value.values()),
        )
    if isinstance(value, (list, tuple)):
        return set().union(*(_nested_keys(item) for item in value))
    return set()


__all__: tuple[str, ...] = ()
