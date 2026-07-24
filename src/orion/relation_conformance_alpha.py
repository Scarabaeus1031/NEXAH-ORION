"""External observational Relation Conformance for Slice III WP16.

The validator consumes an already-complete immutable WP15 candidate and its
certified Slice II Summary and Statistics. It creates only a conformance
report. It never constructs, repairs, normalizes, or reorders a relation.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
import re
from typing import Mapping

from orion.declared_cross_references_alpha import (
    COMPLETE_RELATION_KIND_ORDER,
    DECLARED_REFERENCE_SET_SCHEMA_VERSION,
    RELATION_SET_STATE,
    STOP_AFTER_DECLARED_CROSS_REFERENCES,
    DeclaredReferenceRelationSet,
    canonical_declared_reference_relation_set_bytes,
    declared_reference_relation_set_from_dict,
)
from orion.structural_relation_alpha import (
    PERMITTED_RELATION_KINDS,
    RelationObject,
    validate_relation_object,
)
from orion.understand_structural_statistics_alpha import (
    StructuralStatisticsDiagnostic,
    canonical_structural_statistics_bytes,
)
from orion.understand_structural_summary_alpha import (
    StructuralSummaryDiagnostic,
    canonical_structural_summary_bytes,
)


RELATION_CONFORMANCE_SCHEMA_VERSION = "orion.relation-conformance/0.1-alpha"
RESPONSIBILITY = "external_relation_conformance"
ACCEPTED = "accepted"
REJECTED = "rejected"
STOP_AFTER_RELATION_CONFORMANCE = "after_external_relation_conformance"

_REPORT_ID = re.compile(r"^relation-conformance-[0-9a-f]{24}$")
_SHA256_REF = re.compile(r"^sha256:[0-9a-f]{64}$")


def _canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _digest(value: object) -> str:
    return sha256(_canonical_bytes(value)).hexdigest()


def _artifact_ref(value: bytes) -> str:
    return f"sha256:{sha256(value).hexdigest()}"


def _observed_relation_set_bytes(value: object) -> bytes | None:
    if not isinstance(value, DeclaredReferenceRelationSet):
        return None
    try:
        return _canonical_bytes(asdict(value))
    except (AttributeError, TypeError, ValueError):
        return None


def _safe_text(value: object, fallback: str) -> str:
    return value if isinstance(value, str) and value else fallback


def _report_identity_basis(
    *,
    relation_set_id: str,
    relation_set_ref: str | None,
    structural_summary_ref: str | None,
    structural_statistics_ref: str | None,
    valid: bool,
    decision: str,
    checks: tuple[str, ...],
    errors: tuple[str, ...],
    accepted_relation_set_ref: str | None,
    input_unchanged: bool,
) -> dict[str, object]:
    return {
        "schema_version": RELATION_CONFORMANCE_SCHEMA_VERSION,
        "relation_set_id": relation_set_id,
        "relation_set_ref": relation_set_ref,
        "structural_summary_ref": structural_summary_ref,
        "structural_statistics_ref": structural_statistics_ref,
        "valid": valid,
        "decision": decision,
        "checks": checks,
        "errors": errors,
        "accepted_relation_set_ref": accepted_relation_set_ref,
        "input_unchanged": input_unchanged,
        "responsibility": RESPONSIBILITY,
        "stop": STOP_AFTER_RELATION_CONFORMANCE,
    }


@dataclass(frozen=True, slots=True)
class RelationConformanceReport:
    """Immutable deterministic observation of one supplied Relation Set."""

    report_id: str
    schema_version: str
    relation_set_id: str
    relation_set_ref: str | None
    structural_summary_ref: str | None
    structural_statistics_ref: str | None
    valid: bool
    decision: str
    checks: tuple[str, ...]
    errors: tuple[str, ...]
    accepted_relation_set_ref: str | None
    input_unchanged: bool
    responsibility: str
    stop: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "checks", tuple(self.checks))
        object.__setattr__(self, "errors", tuple(self.errors))
        if _REPORT_ID.fullmatch(self.report_id) is None:
            raise ValueError("report_id is not canonical")
        if self.schema_version != RELATION_CONFORMANCE_SCHEMA_VERSION:
            raise ValueError("Relation Conformance schema changed")
        if not isinstance(self.relation_set_id, str) or not self.relation_set_id:
            raise ValueError("relation_set_id must be observed exact text")
        for field_name in (
            "relation_set_ref",
            "structural_summary_ref",
            "structural_statistics_ref",
            "accepted_relation_set_ref",
        ):
            value = getattr(self, field_name)
            if value is not None and _SHA256_REF.fullmatch(value) is None:
                raise ValueError(f"{field_name} must be a SHA-256 reference")
        if type(self.valid) is not bool:
            raise TypeError("valid must be boolean")
        if self.decision not in (ACCEPTED, REJECTED):
            raise ValueError("decision is outside the conformance vocabulary")
        if self.valid != (self.decision == ACCEPTED):
            raise ValueError("valid and decision differ")
        if self.valid != (not self.errors):
            raise ValueError("valid and errors differ")
        if any(
            not isinstance(check, str) or not check for check in self.checks
        ):
            raise ValueError("checks must be non-empty deterministic labels")
        if any(
            not isinstance(error, str) or not error for error in self.errors
        ):
            raise ValueError("errors must be non-empty deterministic text")
        if self.valid:
            if self.accepted_relation_set_ref != self.relation_set_ref:
                raise ValueError("accepted set reference differs from input")
        elif self.accepted_relation_set_ref is not None:
            raise ValueError("rejected report cannot accept a Relation Set")
        if type(self.input_unchanged) is not bool or not self.input_unchanged:
            raise ValueError("Conformance must leave its input unchanged")
        if self.responsibility != RESPONSIBILITY:
            raise ValueError("Relation Conformance responsibility changed")
        if self.stop != STOP_AFTER_RELATION_CONFORMANCE:
            raise ValueError("Relation Conformance STOP changed")
        basis = _report_identity_basis(
            relation_set_id=self.relation_set_id,
            relation_set_ref=self.relation_set_ref,
            structural_summary_ref=self.structural_summary_ref,
            structural_statistics_ref=self.structural_statistics_ref,
            valid=self.valid,
            decision=self.decision,
            checks=self.checks,
            errors=self.errors,
            accepted_relation_set_ref=self.accepted_relation_set_ref,
            input_unchanged=self.input_unchanged,
        )
        if self.report_id != f"relation-conformance-{_digest(basis)[:24]}":
            raise ValueError("report_id differs from its observations")


def _supplied_relation_basis_valid(
    relation: RelationObject,
    summary: StructuralSummaryDiagnostic,
    statistics: StructuralStatisticsDiagnostic,
) -> bool:
    """Validate only the declared basis of one supplied relation."""

    ordinal_by_id = {
        span.element_id: span.ordinal for span in statistics.element_spans
    }
    kind_by_id = {
        span.element_id: summary.ordered_element_kinds[span.ordinal]
        for span in statistics.element_spans
    }
    heading_level_by_id = {
        heading.element_id: heading.level
        for heading in summary.declared_headings
    }
    source_ordinal = ordinal_by_id.get(relation.source_element_id)
    target_ordinal = ordinal_by_id.get(relation.target_element_id)
    if relation.relation_kind == "immediately_precedes":
        return (
            source_ordinal is not None
            and target_ordinal is not None
            and target_ordinal == source_ordinal + 1
        )
    if relation.relation_kind == "immediately_follows":
        return (
            source_ordinal is not None
            and target_ordinal is not None
            and source_ordinal == target_ordinal + 1
        )
    if relation.relation_kind == "source_reference":
        return (
            source_ordinal is not None
            and relation.target_element_id
            == relation.provenance.source_boundary_id
        )
    if relation.relation_kind == "same_element_kind":
        return (
            source_ordinal is not None
            and target_ordinal is not None
            and source_ordinal < target_ordinal
            and kind_by_id[relation.source_element_id]
            == kind_by_id[relation.target_element_id]
        )
    if relation.relation_kind == "same_heading_level":
        return (
            source_ordinal is not None
            and target_ordinal is not None
            and source_ordinal < target_ordinal
            and relation.source_element_id in heading_level_by_id
            and relation.target_element_id in heading_level_by_id
            and heading_level_by_id[relation.source_element_id]
            == heading_level_by_id[relation.target_element_id]
        )
    if relation.relation_kind == "declared_cross_reference":
        return source_ordinal is not None and target_ordinal is not None
    return False


def _nested_keys(value: object) -> set[str]:
    if isinstance(value, Mapping):
        keys = set(value)
        for nested in value.values():
            keys.update(_nested_keys(nested))
        return keys
    if isinstance(value, (list, tuple)):
        keys: set[str] = set()
        for nested in value:
            keys.update(_nested_keys(nested))
        return keys
    return set()


def validate_relation_conformance(
    relation_set: object,
    summary: object,
    statistics: object,
) -> RelationConformanceReport:
    """Observe one complete candidate atomically and return a report only."""

    checks: list[str] = []
    errors: list[str] = []

    def check(name: str, condition: bool, error: str) -> None:
        checks.append(name)
        if not condition:
            errors.append(error)

    before = _observed_relation_set_bytes(relation_set)
    relation_set_ref = _artifact_ref(before) if before is not None else None
    summary_ref = None
    statistics_ref = None

    set_type_valid = isinstance(relation_set, DeclaredReferenceRelationSet)
    check(
        "relation_set_type",
        set_type_valid,
        "Input is not an immutable WP15 Relation Set",
    )
    summary_type_valid = isinstance(summary, StructuralSummaryDiagnostic)
    check(
        "structural_summary_type",
        summary_type_valid,
        "Input is not an immutable Structural Summary",
    )
    statistics_type_valid = isinstance(
        statistics,
        StructuralStatisticsDiagnostic,
    )
    check(
        "structural_statistics_type",
        statistics_type_valid,
        "Input is not immutable Structural Statistics",
    )

    summary_shape_valid = False
    if summary_type_valid:
        try:
            summary.__post_init__()
            summary_ref = _artifact_ref(
                canonical_structural_summary_bytes(summary)
            )
            summary_shape_valid = True
        except (AttributeError, TypeError, ValueError):
            pass
    check(
        "structural_summary_shape",
        summary_shape_valid,
        "Structural Summary is malformed",
    )

    statistics_shape_valid = False
    if statistics_type_valid:
        try:
            statistics.__post_init__()
            statistics_ref = _artifact_ref(
                canonical_structural_statistics_bytes(statistics)
            )
            statistics_shape_valid = True
        except (AttributeError, TypeError, ValueError):
            pass
    check(
        "structural_statistics_shape",
        statistics_shape_valid,
        "Structural Statistics is malformed",
    )

    set_shape_valid = False
    if set_type_valid:
        try:
            relation_set.__post_init__()
            set_shape_valid = True
        except (AttributeError, TypeError, ValueError):
            pass
    check(
        "relation_set_shape",
        set_shape_valid,
        "Relation Set schema, identity, counts, or STOP is malformed",
    )

    lineage_valid = (
        summary_shape_valid
        and statistics_shape_valid
        and summary.input_inventory_ref == statistics.input_inventory_ref
        and summary.orientation_object_id == statistics.orientation_object_id
        and summary.orientation_object_version
        == statistics.orientation_object_version
        and summary.representation_id == statistics.representation_id
        and summary.representation_version
        == statistics.representation_version
        and summary.representation_integrity
        == statistics.representation_integrity
        and summary.source_id == statistics.source_id
        and summary.source_revision == statistics.source_revision
        and summary.source_integrity == statistics.source_integrity
        and summary.source_boundary == statistics.source_boundary
    )
    check(
        "slice_ii_lineage",
        lineage_valid,
        "Structural Summary and Statistics lineage differs",
    )

    set_input_refs_valid = (
        set_shape_valid
        and lineage_valid
        and relation_set.structural_summary_ref == summary_ref
        and relation_set.structural_statistics_ref == statistics_ref
        and relation_set.input_inventory_ref == summary.input_inventory_ref
    )
    check(
        "relation_set_input_references",
        set_input_refs_valid,
        "Relation Set does not name the exact Slice II inputs",
    )

    relations: tuple[RelationObject, ...] = (
        relation_set.relations if set_type_valid else ()
    )
    relation_objects_valid = (
        set_shape_valid
        and summary_shape_valid
        and statistics_shape_valid
        and all(
            isinstance(relation, RelationObject)
            and validate_relation_object(summary, statistics, relation).valid
            for relation in relations
        )
    )
    check(
        "relation_objects",
        relation_objects_valid,
        "One or more Relation Objects are malformed or have invalid provenance",
    )

    permitted_kinds_valid = (
        set_shape_valid
        and all(
            relation.relation_kind in PERMITTED_RELATION_KINDS
            for relation in relations
        )
        and tuple(PERMITTED_RELATION_KINDS)
        == COMPLETE_RELATION_KIND_ORDER
    )
    check(
        "permitted_relation_kinds",
        permitted_kinds_valid,
        "Relation Set contains a kind outside the frozen vocabulary",
    )

    relation_keys = tuple(
        (
            relation.relation_kind,
            relation.source_element_id,
            relation.target_element_id,
        )
        for relation in relations
        if isinstance(relation, RelationObject)
    )
    duplicate_free = (
        set_shape_valid
        and len(set(relation_keys)) == len(relation_keys)
        and len(
            {
                relation.relation_id
                for relation in relations
                if isinstance(relation, RelationObject)
            }
        )
        == len(relations)
    )
    check(
        "duplicate_absence",
        duplicate_free,
        "Relation Set contains duplicate identities or relation facts",
    )

    rank = {
        kind: index for index, kind in enumerate(COMPLETE_RELATION_KIND_ORDER)
    }
    canonical_order_valid = (
        set_shape_valid
        and tuple(
            relation.canonical_order for relation in relations
        )
        == tuple(range(len(relations)))
        and all(relation.relation_kind in rank for relation in relations)
        and tuple(rank[relation.relation_kind] for relation in relations)
        == tuple(
            sorted(rank[relation.relation_kind] for relation in relations)
        )
    )
    check(
        "canonical_order",
        canonical_order_valid,
        "Relation Set ordering is not canonical and contiguous",
    )

    declared_element_ids = (
        {span.element_id for span in statistics.element_spans}
        if statistics_shape_valid
        else set()
    )
    endpoint_validity = (
        relation_objects_valid
        and all(
            relation.source_element_id in declared_element_ids
            and (
                relation.target_element_id
                == relation.provenance.source_boundary_id
                if relation.relation_kind == "source_reference"
                else relation.target_element_id in declared_element_ids
            )
            for relation in relations
        )
    )
    check(
        "endpoint_validity",
        endpoint_validity,
        "Relation Set contains an unresolved source or target endpoint",
    )

    supplied_relation_bases_valid = (
        relation_objects_valid
        and all(
            _supplied_relation_basis_valid(relation, summary, statistics)
            for relation in relations
        )
    )
    check(
        "supplied_relation_bases",
        supplied_relation_bases_valid,
        "One or more supplied relations lacks an exact declared basis",
    )

    cross_reference_count = sum(
        relation.relation_kind == "declared_cross_reference"
        for relation in relations
    )
    declaration_bindings_valid = (
        set_shape_valid
        and cross_reference_count
        == relation_set.declared_cross_reference_count
        == len(relation_set.accepted_declaration_refs)
        and len(set(relation_set.accepted_declaration_refs))
        == len(relation_set.accepted_declaration_refs)
        and all(
            _SHA256_REF.fullmatch(reference) is not None
            for reference in relation_set.accepted_declaration_refs
        )
    )
    check(
        "declared_reference_bindings",
        declaration_bindings_valid,
        "Declared relations lack exact immutable declaration references",
    )

    canonical_serialization_valid = False
    if set_shape_valid and before is not None:
        try:
            parsed = declared_reference_relation_set_from_dict(
                asdict(relation_set)
            )
            canonical = canonical_declared_reference_relation_set_bytes(
                relation_set
            )
            canonical_serialization_valid = (
                canonical == before
                and canonical_declared_reference_relation_set_bytes(parsed)
                == before
            )
        except (AttributeError, TypeError, ValueError):
            pass
    check(
        "canonical_serialization",
        canonical_serialization_valid,
        "Relation Set canonical serialization does not replay exactly",
    )

    prohibited_fields = {
        "content",
        "text",
        "topic",
        "concept",
        "entity",
        "claim",
        "evidence",
        "meaning",
        "similarity",
        "parent",
        "child",
        "hierarchy",
        "ranking",
        "recommendation",
        "inference",
        "graph",
        "navigation",
        "orientation_map",
    }
    boundary_valid = (
        before is not None
        and not (
            _nested_keys(asdict(relation_set))
            & prohibited_fields
        )
    )
    check(
        "responsibility_boundary",
        boundary_valid,
        "Relation Set contains inferred, semantic, hierarchy, or downstream fields",
    )

    candidate_state_valid = (
        set_shape_valid
        and relation_set.schema_version
        == DECLARED_REFERENCE_SET_SCHEMA_VERSION
        and relation_set.relation_set_state == RELATION_SET_STATE
        and relation_set.stop == STOP_AFTER_DECLARED_CROSS_REFERENCES
    )
    check(
        "candidate_state",
        candidate_state_valid,
        "Relation Set is not the exact WP15 candidate state",
    )

    after = _observed_relation_set_bytes(relation_set)
    input_unchanged = before == after
    check(
        "input_unchanged",
        input_unchanged,
        "Conformance observation changed the Relation Set",
    )

    valid = not errors
    decision = ACCEPTED if valid else REJECTED
    accepted_ref = relation_set_ref if valid else None
    relation_set_id = _safe_text(
        getattr(relation_set, "relation_set_id", None),
        "unavailable",
    )
    basis = _report_identity_basis(
        relation_set_id=relation_set_id,
        relation_set_ref=relation_set_ref,
        structural_summary_ref=summary_ref,
        structural_statistics_ref=statistics_ref,
        valid=valid,
        decision=decision,
        checks=tuple(checks),
        errors=tuple(errors),
        accepted_relation_set_ref=accepted_ref,
        input_unchanged=input_unchanged,
    )
    return RelationConformanceReport(
        report_id=f"relation-conformance-{_digest(basis)[:24]}",
        schema_version=RELATION_CONFORMANCE_SCHEMA_VERSION,
        relation_set_id=relation_set_id,
        relation_set_ref=relation_set_ref,
        structural_summary_ref=summary_ref,
        structural_statistics_ref=statistics_ref,
        valid=valid,
        decision=decision,
        checks=tuple(checks),
        errors=tuple(errors),
        accepted_relation_set_ref=accepted_ref,
        input_unchanged=input_unchanged,
        responsibility=RESPONSIBILITY,
        stop=STOP_AFTER_RELATION_CONFORMANCE,
    )


def relation_conformance_report_as_dict(
    report: RelationConformanceReport,
) -> dict[str, object]:
    report.__post_init__()
    return asdict(report)


def canonical_relation_conformance_report_bytes(
    report: RelationConformanceReport,
) -> bytes:
    return _canonical_bytes(relation_conformance_report_as_dict(report))


def relation_conformance_report_from_dict(
    value: Mapping[str, object],
) -> RelationConformanceReport:
    if not isinstance(value, Mapping):
        raise TypeError("Relation Conformance Report must be a mapping")
    expected_fields = {
        "report_id",
        "schema_version",
        "relation_set_id",
        "relation_set_ref",
        "structural_summary_ref",
        "structural_statistics_ref",
        "valid",
        "decision",
        "checks",
        "errors",
        "accepted_relation_set_ref",
        "input_unchanged",
        "responsibility",
        "stop",
    }
    if set(value) != expected_fields:
        raise ValueError("Relation Conformance Report fields are not exact")
    checks = value["checks"]
    errors = value["errors"]
    if not isinstance(checks, (list, tuple)):
        raise TypeError("checks must be ordered")
    if not isinstance(errors, (list, tuple)):
        raise TypeError("errors must be ordered")
    return RelationConformanceReport(
        report_id=value["report_id"],
        schema_version=value["schema_version"],
        relation_set_id=value["relation_set_id"],
        relation_set_ref=value["relation_set_ref"],
        structural_summary_ref=value["structural_summary_ref"],
        structural_statistics_ref=value["structural_statistics_ref"],
        valid=value["valid"],
        decision=value["decision"],
        checks=tuple(checks),
        errors=tuple(errors),
        accepted_relation_set_ref=value["accepted_relation_set_ref"],
        input_unchanged=value["input_unchanged"],
        responsibility=value["responsibility"],
        stop=value["stop"],
    )


__all__: tuple[str, ...] = ()
