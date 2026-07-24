"""Immutable atomic Structural Relation Object for Vertical Slice III WP12.

WP12 defines, constructs, serializes, and validates exactly one explicitly
supplied relation. It performs no relation discovery, generation, traversal,
graph construction, source access, or semantic interpretation.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
import re
from typing import Mapping

from orion.understand_structural_statistics_alpha import (
    StructuralStatisticsDiagnostic,
    canonical_structural_statistics_bytes,
)
from orion.understand_structural_summary_alpha import (
    StructuralSummaryDiagnostic,
    canonical_structural_summary_bytes,
)


RELATION_SCHEMA_VERSION = "orion.relation/0.1-alpha"
PERMITTED_RELATION_KINDS = (
    "immediately_precedes",
    "immediately_follows",
    "source_reference",
    "same_element_kind",
    "same_heading_level",
    "declared_cross_reference",
)
STOP_AFTER_RELATION_OBJECT = "after_relation_object"

_ELEMENT_ID = re.compile(r"^element-[0-9a-f]{24}$")
_SOURCE_BOUNDARY_ID = re.compile(r"^source-boundary-[0-9a-f]{24}$")
_RELATION_ID = re.compile(r"^relation-[0-9a-f]{24}$")
_SHA256_REF = re.compile(r"^sha256:[0-9a-f]{64}$")
_SHA256_HEX = re.compile(r"^[0-9a-f]{64}$")


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
    if not isinstance(value, str) or _SHA256_REF.fullmatch(value) is None:
        raise ValueError(f"{field_name} must be a SHA-256 reference")


def _require_sha256_hex(value: str, field_name: str) -> None:
    if not isinstance(value, str) or _SHA256_HEX.fullmatch(value) is None:
        raise ValueError(f"{field_name} must be lowercase SHA-256 hexadecimal")


def _artifact_ref(canonical_bytes: bytes) -> str:
    return f"sha256:{sha256(canonical_bytes).hexdigest()}"


@dataclass(frozen=True, slots=True)
class RelationProvenance:
    """Exact certified Slice II lineage accepted by one Relation Object."""

    structural_summary_id: str
    structural_summary_ref: str
    structural_statistics_id: str
    structural_statistics_ref: str
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
    source_boundary_id: str

    def __post_init__(self) -> None:
        for field_name in (
            "structural_summary_id",
            "structural_statistics_id",
            "orientation_object_id",
            "orientation_object_version",
            "representation_id",
            "representation_version",
            "source_id",
            "source_revision",
            "source_boundary",
        ):
            _require_text(getattr(self, field_name), field_name)
        for field_name in (
            "structural_summary_ref",
            "structural_statistics_ref",
            "input_inventory_ref",
        ):
            _require_sha256_ref(getattr(self, field_name), field_name)
        for field_name in ("representation_integrity", "source_integrity"):
            _require_sha256_hex(getattr(self, field_name), field_name)
        if _SOURCE_BOUNDARY_ID.fullmatch(self.source_boundary_id) is None:
            raise ValueError(
                "source_boundary_id must be a canonical source-boundary identifier"
            )


def _relation_identity_basis(
    *,
    relation_kind: str,
    source_element_id: str,
    target_element_id: str,
    provenance: RelationProvenance,
    canonical_order: int,
    schema_version: str,
) -> dict[str, object]:
    return {
        "relation_kind": relation_kind,
        "source_element_id": source_element_id,
        "target_element_id": target_element_id,
        "provenance": asdict(provenance),
        "canonical_order": canonical_order,
        "schema_version": schema_version,
    }


def _expected_relation_id(
    *,
    relation_kind: str,
    source_element_id: str,
    target_element_id: str,
    provenance: RelationProvenance,
    canonical_order: int,
    schema_version: str,
) -> str:
    basis = _relation_identity_basis(
        relation_kind=relation_kind,
        source_element_id=source_element_id,
        target_element_id=target_element_id,
        provenance=provenance,
        canonical_order=canonical_order,
        schema_version=schema_version,
    )
    return f"relation-{_digest(basis)[:24]}"


@dataclass(frozen=True, slots=True)
class RelationObject:
    """One immutable explicitly constructed structural relation."""

    relation_id: str
    relation_kind: str
    source_element_id: str
    target_element_id: str
    provenance: RelationProvenance
    canonical_order: int
    schema_version: str

    def __post_init__(self) -> None:
        if _RELATION_ID.fullmatch(self.relation_id) is None:
            raise ValueError("relation_id must be a canonical relation identifier")
        if self.relation_kind not in PERMITTED_RELATION_KINDS:
            raise ValueError("relation_kind is outside the frozen Slice III vocabulary")
        if _ELEMENT_ID.fullmatch(self.source_element_id) is None:
            raise ValueError(
                "source_element_id must be a canonical element identifier"
            )
        if self.relation_kind == "source_reference":
            if _SOURCE_BOUNDARY_ID.fullmatch(self.target_element_id) is None:
                raise ValueError(
                    "source_reference target must be a source-boundary identifier"
                )
        elif _ELEMENT_ID.fullmatch(self.target_element_id) is None:
            raise ValueError(
                "target_element_id must be a canonical element identifier"
            )
        if self.source_element_id == self.target_element_id:
            raise ValueError("Relation Object endpoints must be distinct")
        if not isinstance(self.provenance, RelationProvenance):
            raise TypeError("provenance must be immutable RelationProvenance")
        self.provenance.__post_init__()
        if type(self.canonical_order) is not int or self.canonical_order < 0:
            raise ValueError("canonical_order must be a non-negative integer")
        if self.schema_version != RELATION_SCHEMA_VERSION:
            raise ValueError("schema_version is not the WP12 Relation schema")


@dataclass(frozen=True, slots=True)
class RelationObjectValidation:
    """Deterministic object-contract validation result."""

    valid: bool
    checks: tuple[str, ...]
    errors: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "checks", tuple(self.checks))
        object.__setattr__(self, "errors", tuple(self.errors))
        if type(self.valid) is not bool:
            raise TypeError("valid must be boolean")
        if any(not isinstance(check, str) or not check for check in self.checks):
            raise ValueError("validation checks must be non-empty text")
        if any(not isinstance(error, str) or not error for error in self.errors):
            raise ValueError("validation errors must be non-empty text")
        if self.valid != (not self.errors):
            raise ValueError("validation state must match errors")


def _validate_slice_ii_lineage(
    summary: StructuralSummaryDiagnostic,
    statistics: StructuralStatisticsDiagnostic,
) -> None:
    if not isinstance(summary, StructuralSummaryDiagnostic):
        raise TypeError("Relation Object requires immutable Structural Summary")
    if not isinstance(statistics, StructuralStatisticsDiagnostic):
        raise TypeError("Relation Object requires immutable Structural Statistics")
    summary.__post_init__()
    statistics.__post_init__()
    summary_lineage = (
        summary.input_inventory_ref,
        summary.orientation_object_id,
        summary.orientation_object_version,
        summary.representation_id,
        summary.representation_version,
        summary.representation_integrity,
        summary.source_id,
        summary.source_revision,
        summary.source_integrity,
        summary.source_boundary,
    )
    statistics_lineage = (
        statistics.input_inventory_ref,
        statistics.orientation_object_id,
        statistics.orientation_object_version,
        statistics.representation_id,
        statistics.representation_version,
        statistics.representation_integrity,
        statistics.source_id,
        statistics.source_revision,
        statistics.source_integrity,
        statistics.source_boundary,
    )
    if summary_lineage != statistics_lineage:
        raise ValueError("Structural Summary and Statistics lineage differs")
    if (
        summary.total_declared_element_count
        != statistics.total_ordered_elements
        or summary.first_canonical_ordinal
        != statistics.first_canonical_ordinal
        or summary.final_canonical_ordinal
        != statistics.final_canonical_ordinal
    ):
        raise ValueError("Structural Summary and Statistics boundaries differ")


def _provenance_from_slice_ii(
    summary: StructuralSummaryDiagnostic,
    statistics: StructuralStatisticsDiagnostic,
) -> RelationProvenance:
    _validate_slice_ii_lineage(summary, statistics)
    source_boundary_basis = {
        "source_id": summary.source_id,
        "source_revision": summary.source_revision,
        "source_integrity": summary.source_integrity,
        "source_boundary": summary.source_boundary,
    }
    return RelationProvenance(
        structural_summary_id=summary.summary_id,
        structural_summary_ref=_artifact_ref(
            canonical_structural_summary_bytes(summary)
        ),
        structural_statistics_id=statistics.statistics_id,
        structural_statistics_ref=_artifact_ref(
            canonical_structural_statistics_bytes(statistics)
        ),
        input_inventory_ref=summary.input_inventory_ref,
        orientation_object_id=summary.orientation_object_id,
        orientation_object_version=summary.orientation_object_version,
        representation_id=summary.representation_id,
        representation_version=summary.representation_version,
        representation_integrity=summary.representation_integrity,
        source_id=summary.source_id,
        source_revision=summary.source_revision,
        source_integrity=summary.source_integrity,
        source_boundary=summary.source_boundary,
        source_boundary_id=(
            f"source-boundary-{_digest(source_boundary_basis)[:24]}"
        ),
    )


def create_relation_object(
    summary: StructuralSummaryDiagnostic,
    statistics: StructuralStatisticsDiagnostic,
    *,
    relation_kind: str,
    source_element_id: str,
    target_element_id: str,
    canonical_order: int,
) -> RelationObject:
    """Construct one explicit Relation Object without discovering a relation."""

    provenance = _provenance_from_slice_ii(summary, statistics)
    relation_id = _expected_relation_id(
        relation_kind=relation_kind,
        source_element_id=source_element_id,
        target_element_id=target_element_id,
        provenance=provenance,
        canonical_order=canonical_order,
        schema_version=RELATION_SCHEMA_VERSION,
    )
    relation = RelationObject(
        relation_id=relation_id,
        relation_kind=relation_kind,
        source_element_id=source_element_id,
        target_element_id=target_element_id,
        provenance=provenance,
        canonical_order=canonical_order,
        schema_version=RELATION_SCHEMA_VERSION,
    )
    relation.__post_init__()
    return relation


def validate_relation_object(
    summary: StructuralSummaryDiagnostic,
    statistics: StructuralStatisticsDiagnostic,
    relation: RelationObject,
) -> RelationObjectValidation:
    """Validate one object against exact certified Slice II lineage."""

    checks: list[str] = []
    errors: list[str] = []

    def check(name: str, condition: bool, error: str) -> None:
        checks.append(name)
        if not condition:
            errors.append(error)

    try:
        _validate_slice_ii_lineage(summary, statistics)
        checks.append("slice_ii_lineage_valid")
    except (AttributeError, TypeError, ValueError) as exc:
        checks.append("slice_ii_lineage_valid")
        errors.append(str(exc))

    try:
        relation.__post_init__()
        checks.append("relation_shape_valid")
    except (AttributeError, TypeError, ValueError) as exc:
        checks.append("relation_shape_valid")
        errors.append(str(exc))

    expected_provenance = None
    try:
        expected_provenance = _provenance_from_slice_ii(summary, statistics)
    except (AttributeError, TypeError, ValueError):
        pass

    check(
        "provenance_exact",
        expected_provenance is not None
        and relation.provenance == expected_provenance,
        "Relation provenance differs from certified Slice II artifacts",
    )
    expected_id = _expected_relation_id(
        relation_kind=relation.relation_kind,
        source_element_id=relation.source_element_id,
        target_element_id=relation.target_element_id,
        provenance=relation.provenance,
        canonical_order=relation.canonical_order,
        schema_version=relation.schema_version,
    )
    check(
        "relation_identity",
        relation.relation_id == expected_id,
        "Relation identity differs from canonical identity basis",
    )

    declared_element_ids = {
        span.element_id for span in statistics.element_spans
    }
    check(
        "source_endpoint_declared",
        relation.source_element_id in declared_element_ids,
        "Relation source endpoint is not declared by Structural Statistics",
    )
    if relation.relation_kind == "source_reference":
        target_valid = (
            expected_provenance is not None
            and relation.target_element_id
            == expected_provenance.source_boundary_id
        )
        target_error = (
            "source_reference target is not the exact source boundary"
        )
    else:
        target_valid = relation.target_element_id in declared_element_ids
        target_error = (
            "Relation target endpoint is not declared by Structural Statistics"
        )
    check("target_endpoint_declared", target_valid, target_error)
    check(
        "canonical_order_shape",
        type(relation.canonical_order) is int and relation.canonical_order >= 0,
        "canonical_order is not a non-negative integer",
    )
    check(
        "schema_and_vocabulary",
        relation.schema_version == RELATION_SCHEMA_VERSION
        and relation.relation_kind in PERMITTED_RELATION_KINDS,
        "Relation schema or kind is not accepted",
    )

    return RelationObjectValidation(
        valid=not errors,
        checks=tuple(checks),
        errors=tuple(errors),
    )


def relation_object_as_dict(relation: RelationObject) -> dict[str, object]:
    """Return the exact deterministic Relation Object shape."""

    relation.__post_init__()
    return asdict(relation)


def canonical_relation_object_bytes(relation: RelationObject) -> bytes:
    """Serialize one Relation Object as canonical UTF-8 JSON."""

    return _canonical_bytes(relation_object_as_dict(relation))


def relation_object_from_dict(value: Mapping[str, object]) -> RelationObject:
    """Parse exactly the WP12 schema and reject unknown or missing fields."""

    if not isinstance(value, Mapping):
        raise TypeError("Relation Object input must be a mapping")
    expected_fields = {
        "relation_id",
        "relation_kind",
        "source_element_id",
        "target_element_id",
        "provenance",
        "canonical_order",
        "schema_version",
    }
    if set(value) != expected_fields:
        raise ValueError("Relation Object fields do not match the WP12 schema")
    provenance_value = value["provenance"]
    if not isinstance(provenance_value, Mapping):
        raise TypeError("provenance must be a mapping")
    provenance_fields = {
        "structural_summary_id",
        "structural_summary_ref",
        "structural_statistics_id",
        "structural_statistics_ref",
        "input_inventory_ref",
        "orientation_object_id",
        "orientation_object_version",
        "representation_id",
        "representation_version",
        "representation_integrity",
        "source_id",
        "source_revision",
        "source_integrity",
        "source_boundary",
        "source_boundary_id",
    }
    if set(provenance_value) != provenance_fields:
        raise ValueError("provenance fields do not match the WP12 schema")
    provenance = RelationProvenance(**dict(provenance_value))
    relation = RelationObject(
        relation_id=value["relation_id"],
        relation_kind=value["relation_kind"],
        source_element_id=value["source_element_id"],
        target_element_id=value["target_element_id"],
        provenance=provenance,
        canonical_order=value["canonical_order"],
        schema_version=value["schema_version"],
    )
    expected_id = _expected_relation_id(
        relation_kind=relation.relation_kind,
        source_element_id=relation.source_element_id,
        target_element_id=relation.target_element_id,
        provenance=relation.provenance,
        canonical_order=relation.canonical_order,
        schema_version=relation.schema_version,
    )
    if relation.relation_id != expected_id:
        raise ValueError("relation_id differs from the canonical identity basis")
    return relation


__all__: tuple[str, ...] = ()
