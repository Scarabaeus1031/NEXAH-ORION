"""Deterministic structural-equality Relations for Slice III WP14.

The implementation consumes immutable Structural Summary and Structural
Statistics artifacts. It compares declared kind and heading-level fields only.
It never reads content, infers hierarchy, or assigns semantic similarity.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
import re
from typing import Mapping

from orion.sequential_relations_alpha import (
    SequentialRelationSet,
    canonical_sequential_relation_set_bytes,
    generate_sequential_relations,
)
from orion.structural_relation_alpha import (
    RelationObject,
    create_relation_object,
    relation_object_from_dict,
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


STRUCTURAL_EQUALITY_SET_SCHEMA_VERSION = (
    "orion.relation-set/structural-equality/0.1-alpha"
)
STRUCTURAL_EQUALITY_KINDS = (
    "same_element_kind",
    "same_heading_level",
)
COMPLETE_WP14_KIND_ORDER = (
    "immediately_precedes",
    "immediately_follows",
    "same_element_kind",
    "same_heading_level",
)
RESPONSIBILITY = "structural_equality_relations"
RELATION_SET_STATE = "candidate"
STOP_AFTER_STRUCTURAL_EQUALITY = "after_structural_equality_relations"

_RELATION_SET_ID = re.compile(r"^relation-set-[0-9a-f]{24}$")
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


def _require_sha256_ref(value: str, field_name: str) -> None:
    if not isinstance(value, str) or _SHA256_REF.fullmatch(value) is None:
        raise ValueError(f"{field_name} must be a SHA-256 reference")


def _validate_inputs(
    summary: StructuralSummaryDiagnostic,
    statistics: StructuralStatisticsDiagnostic,
) -> None:
    if not isinstance(summary, StructuralSummaryDiagnostic):
        raise TypeError("Structural Equality requires Structural Summary")
    if not isinstance(statistics, StructuralStatisticsDiagnostic):
        raise TypeError("Structural Equality requires Structural Statistics")
    summary.__post_init__()
    statistics.__post_init__()
    if (
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
        summary.total_declared_element_count,
        summary.first_canonical_ordinal,
        summary.final_canonical_ordinal,
    ) != (
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
        statistics.total_ordered_elements,
        statistics.first_canonical_ordinal,
        statistics.final_canonical_ordinal,
    ):
        raise ValueError("Structural Summary and Statistics lineage differs")
    if len(summary.ordered_element_kinds) != len(statistics.element_spans):
        raise ValueError("Declared kinds and element spans differ")
    heading_ids = {
        span.element_id: span.ordinal for span in statistics.element_spans
    }
    for heading in summary.declared_headings:
        if heading.element_id not in heading_ids:
            raise ValueError("Declared heading is absent from Statistics")
        if heading_ids[heading.element_id] != heading.ordinal:
            raise ValueError("Declared heading ordinal differs from Statistics")


def _identity_basis(
    *,
    sequential_relation_set_ref: str,
    structural_summary_ref: str,
    structural_statistics_ref: str,
    input_inventory_ref: str,
    sequential_relation_count: int,
    equality_relation_count: int,
    relations: tuple[RelationObject, ...],
) -> dict[str, object]:
    return {
        "schema_version": STRUCTURAL_EQUALITY_SET_SCHEMA_VERSION,
        "sequential_relation_set_ref": sequential_relation_set_ref,
        "structural_summary_ref": structural_summary_ref,
        "structural_statistics_ref": structural_statistics_ref,
        "input_inventory_ref": input_inventory_ref,
        "sequential_relation_count": sequential_relation_count,
        "equality_relation_count": equality_relation_count,
        "relation_count": len(relations),
        "relation_ids": tuple(relation.relation_id for relation in relations),
        "responsibility": RESPONSIBILITY,
        "relation_set_state": RELATION_SET_STATE,
        "stop": STOP_AFTER_STRUCTURAL_EQUALITY,
    }


def _expected_set_id(
    *,
    sequential_relation_set_ref: str,
    structural_summary_ref: str,
    structural_statistics_ref: str,
    input_inventory_ref: str,
    sequential_relation_count: int,
    equality_relation_count: int,
    relations: tuple[RelationObject, ...],
) -> str:
    return "relation-set-" + _digest(
        _identity_basis(
            sequential_relation_set_ref=sequential_relation_set_ref,
            structural_summary_ref=structural_summary_ref,
            structural_statistics_ref=structural_statistics_ref,
            input_inventory_ref=input_inventory_ref,
            sequential_relation_count=sequential_relation_count,
            equality_relation_count=equality_relation_count,
            relations=relations,
        )
    )[:24]


@dataclass(frozen=True, slots=True)
class StructuralEqualityRelationSet:
    """Immutable candidate set containing sequential and equality relations."""

    relation_set_id: str
    schema_version: str
    sequential_relation_set_ref: str
    structural_summary_ref: str
    structural_statistics_ref: str
    input_inventory_ref: str
    sequential_relation_count: int
    equality_relation_count: int
    relation_count: int
    relations: tuple[RelationObject, ...]
    responsibility: str
    relation_set_state: str
    stop: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "relations", tuple(self.relations))
        if _RELATION_SET_ID.fullmatch(self.relation_set_id) is None:
            raise ValueError(
                "relation_set_id must be a canonical relation-set identifier"
            )
        if self.schema_version != STRUCTURAL_EQUALITY_SET_SCHEMA_VERSION:
            raise ValueError("schema_version is not the WP14 schema")
        for field_name in (
            "sequential_relation_set_ref",
            "structural_summary_ref",
            "structural_statistics_ref",
            "input_inventory_ref",
        ):
            _require_sha256_ref(getattr(self, field_name), field_name)
        for field_name in (
            "sequential_relation_count",
            "equality_relation_count",
            "relation_count",
        ):
            value = getattr(self, field_name)
            if type(value) is not int or value < 0:
                raise ValueError(f"{field_name} must be a non-negative integer")
        if (
            self.sequential_relation_count + self.equality_relation_count
            != self.relation_count
            or self.relation_count != len(self.relations)
        ):
            raise ValueError("Relation Set counts do not reconcile")
        if any(
            not isinstance(relation, RelationObject)
            for relation in self.relations
        ):
            raise TypeError("relations must contain WP12 Relation Objects")
        for relation in self.relations:
            relation.__post_init__()
        if tuple(
            relation.canonical_order for relation in self.relations
        ) != tuple(range(self.relation_count)):
            raise ValueError("Relation Objects are not in canonical order")
        relation_ids = tuple(
            relation.relation_id for relation in self.relations
        )
        if len(set(relation_ids)) != len(relation_ids):
            raise ValueError("Relation Set contains duplicate relation IDs")
        relation_keys = tuple(
            (
                relation.relation_kind,
                relation.source_element_id,
                relation.target_element_id,
            )
            for relation in self.relations
        )
        if len(set(relation_keys)) != len(relation_keys):
            raise ValueError("Relation Set contains duplicate relations")
        kind_rank = {
            kind: index for index, kind in enumerate(COMPLETE_WP14_KIND_ORDER)
        }
        kinds = tuple(relation.relation_kind for relation in self.relations)
        if any(kind not in kind_rank for kind in kinds):
            raise ValueError("WP14 Relation Set contains a forbidden kind")
        if tuple(kind_rank[kind] for kind in kinds) != tuple(
            sorted(kind_rank[kind] for kind in kinds)
        ):
            raise ValueError("Relation kinds do not follow canonical type order")
        if any(
            relation.relation_kind not in STRUCTURAL_EQUALITY_KINDS
            for relation in self.relations[self.sequential_relation_count :]
        ):
            raise ValueError("Equality suffix contains a non-equality relation")
        if self.responsibility != RESPONSIBILITY:
            raise ValueError("Relation Set responsibility changed")
        if self.relation_set_state != RELATION_SET_STATE:
            raise ValueError("WP14 Relation Set must remain a candidate")
        if self.stop != STOP_AFTER_STRUCTURAL_EQUALITY:
            raise ValueError("WP14 STOP boundary changed")


@dataclass(frozen=True, slots=True)
class StructuralEqualitySetValidation:
    """Deterministic validation of one WP14 candidate Relation Set."""

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


def _unordered_equal_kind_pairs(
    summary: StructuralSummaryDiagnostic,
    statistics: StructuralStatisticsDiagnostic,
) -> tuple[tuple[str, str], ...]:
    elements = tuple(
        (
            span.ordinal,
            span.element_id,
            summary.ordered_element_kinds[span.ordinal],
        )
        for span in statistics.element_spans
    )
    return tuple(
        (source_id, target_id)
        for source_index, (_, source_id, source_kind) in enumerate(elements)
        for _, target_id, target_kind in elements[source_index + 1 :]
        if source_kind == target_kind
    )


def _unordered_equal_heading_level_pairs(
    summary: StructuralSummaryDiagnostic,
) -> tuple[tuple[str, str], ...]:
    headings = tuple(
        sorted(summary.declared_headings, key=lambda item: item.ordinal)
    )
    return tuple(
        (source.element_id, target.element_id)
        for source_index, source in enumerate(headings)
        for target in headings[source_index + 1 :]
        if source.level == target.level
    )


def generate_structural_equality_relations(
    summary: StructuralSummaryDiagnostic,
    statistics: StructuralStatisticsDiagnostic,
) -> StructuralEqualityRelationSet:
    """Extend deterministic sequential relations with structural equality."""

    _validate_inputs(summary, statistics)
    sequential_set = generate_sequential_relations(summary, statistics)
    sequential_count = sequential_set.relation_count
    equal_kind_pairs = _unordered_equal_kind_pairs(summary, statistics)
    equal_heading_pairs = _unordered_equal_heading_level_pairs(summary)

    same_kind = tuple(
        create_relation_object(
            summary,
            statistics,
            relation_kind="same_element_kind",
            source_element_id=source_id,
            target_element_id=target_id,
            canonical_order=sequential_count + index,
        )
        for index, (source_id, target_id) in enumerate(equal_kind_pairs)
    )
    same_heading_level = tuple(
        create_relation_object(
            summary,
            statistics,
            relation_kind="same_heading_level",
            source_element_id=source_id,
            target_element_id=target_id,
            canonical_order=sequential_count
            + len(same_kind)
            + index,
        )
        for index, (source_id, target_id) in enumerate(equal_heading_pairs)
    )
    equality_relations = same_kind + same_heading_level
    for relation in equality_relations:
        validation = validate_relation_object(summary, statistics, relation)
        if not validation.valid:
            raise ValueError(
                "Generated equality Relation failed WP12 validation: "
                + "; ".join(validation.errors)
            )
    relations = sequential_set.relations + equality_relations
    sequential_ref = _artifact_ref(
        canonical_sequential_relation_set_bytes(sequential_set)
    )
    summary_ref = _artifact_ref(canonical_structural_summary_bytes(summary))
    statistics_ref = _artifact_ref(
        canonical_structural_statistics_bytes(statistics)
    )
    equality_count = len(equality_relations)
    relation_set = StructuralEqualityRelationSet(
        relation_set_id=_expected_set_id(
            sequential_relation_set_ref=sequential_ref,
            structural_summary_ref=summary_ref,
            structural_statistics_ref=statistics_ref,
            input_inventory_ref=summary.input_inventory_ref,
            sequential_relation_count=sequential_count,
            equality_relation_count=equality_count,
            relations=relations,
        ),
        schema_version=STRUCTURAL_EQUALITY_SET_SCHEMA_VERSION,
        sequential_relation_set_ref=sequential_ref,
        structural_summary_ref=summary_ref,
        structural_statistics_ref=statistics_ref,
        input_inventory_ref=summary.input_inventory_ref,
        sequential_relation_count=sequential_count,
        equality_relation_count=equality_count,
        relation_count=len(relations),
        relations=relations,
        responsibility=RESPONSIBILITY,
        relation_set_state=RELATION_SET_STATE,
        stop=STOP_AFTER_STRUCTURAL_EQUALITY,
    )
    relation_set.__post_init__()
    return relation_set


def validate_structural_equality_relation_set(
    summary: StructuralSummaryDiagnostic,
    statistics: StructuralStatisticsDiagnostic,
    relation_set: StructuralEqualityRelationSet,
) -> StructuralEqualitySetValidation:
    """Independently recompute and validate the complete WP14 candidate."""

    checks: list[str] = []
    errors: list[str] = []

    def check(name: str, condition: bool, error: str) -> None:
        checks.append(name)
        if not condition:
            errors.append(error)

    try:
        _validate_inputs(summary, statistics)
        checks.append("slice_ii_inputs_valid")
    except (AttributeError, TypeError, ValueError) as exc:
        checks.append("slice_ii_inputs_valid")
        errors.append(str(exc))
    try:
        relation_set.__post_init__()
        checks.append("relation_set_shape_valid")
    except (AttributeError, TypeError, ValueError) as exc:
        checks.append("relation_set_shape_valid")
        errors.append(str(exc))

    expected = None
    try:
        expected = generate_structural_equality_relations(summary, statistics)
    except (AttributeError, TypeError, ValueError) as exc:
        errors.append(f"deterministic generation unavailable: {exc}")

    check(
        "deterministic_generation",
        expected is not None and relation_set == expected,
        "Relation Set differs from deterministic equality generation",
    )
    expected_id = _expected_set_id(
        sequential_relation_set_ref=relation_set.sequential_relation_set_ref,
        structural_summary_ref=relation_set.structural_summary_ref,
        structural_statistics_ref=relation_set.structural_statistics_ref,
        input_inventory_ref=relation_set.input_inventory_ref,
        sequential_relation_count=relation_set.sequential_relation_count,
        equality_relation_count=relation_set.equality_relation_count,
        relations=relation_set.relations,
    )
    check(
        "relation_set_identity",
        relation_set.relation_set_id == expected_id,
        "Relation Set identity differs from canonical basis",
    )
    sequential_set: SequentialRelationSet | None = None
    try:
        sequential_set = generate_sequential_relations(summary, statistics)
    except (AttributeError, TypeError, ValueError):
        pass
    check(
        "wp13_prefix_preserved",
        sequential_set is not None
        and relation_set.relations[: relation_set.sequential_relation_count]
        == sequential_set.relations
        and relation_set.sequential_relation_set_ref
        == _artifact_ref(canonical_sequential_relation_set_bytes(sequential_set)),
        "WP13 Sequential Relation Set was not preserved exactly",
    )
    check(
        "relation_objects_valid",
        all(
            validate_relation_object(summary, statistics, relation).valid
            for relation in relation_set.relations
        ),
        "Relation Set contains an invalid WP12 Relation Object",
    )
    equality_suffix = relation_set.relations[
        relation_set.sequential_relation_count :
    ]
    check(
        "only_equality_kinds_added",
        all(
            relation.relation_kind in STRUCTURAL_EQUALITY_KINDS
            for relation in equality_suffix
        ),
        "WP14 added a non-equality relation kind",
    )
    check(
        "provenance_references",
        relation_set.structural_summary_ref
        == _artifact_ref(canonical_structural_summary_bytes(summary))
        and relation_set.structural_statistics_ref
        == _artifact_ref(canonical_structural_statistics_bytes(statistics))
        and relation_set.input_inventory_ref
        == summary.input_inventory_ref
        == statistics.input_inventory_ref,
        "WP14 does not preserve exact Slice II references",
    )
    check(
        "responsibility_and_stop",
        relation_set.schema_version == STRUCTURAL_EQUALITY_SET_SCHEMA_VERSION
        and relation_set.responsibility == RESPONSIBILITY
        and relation_set.relation_set_state == RELATION_SET_STATE
        and relation_set.stop == STOP_AFTER_STRUCTURAL_EQUALITY,
        "WP14 responsibility or STOP changed",
    )

    return StructuralEqualitySetValidation(
        valid=not errors,
        checks=tuple(checks),
        errors=tuple(errors),
    )


def structural_equality_relation_set_as_dict(
    relation_set: StructuralEqualityRelationSet,
) -> dict[str, object]:
    relation_set.__post_init__()
    return asdict(relation_set)


def canonical_structural_equality_relation_set_bytes(
    relation_set: StructuralEqualityRelationSet,
) -> bytes:
    return _canonical_bytes(structural_equality_relation_set_as_dict(relation_set))


def structural_equality_relation_set_from_dict(
    value: Mapping[str, object],
) -> StructuralEqualityRelationSet:
    if not isinstance(value, Mapping):
        raise TypeError("Structural Equality Relation Set must be a mapping")
    expected_fields = {
        "relation_set_id",
        "schema_version",
        "sequential_relation_set_ref",
        "structural_summary_ref",
        "structural_statistics_ref",
        "input_inventory_ref",
        "sequential_relation_count",
        "equality_relation_count",
        "relation_count",
        "relations",
        "responsibility",
        "relation_set_state",
        "stop",
    }
    if set(value) != expected_fields:
        raise ValueError(
            "Structural Equality Relation Set fields do not match WP14"
        )
    relation_values = value["relations"]
    if not isinstance(relation_values, (list, tuple)):
        raise TypeError("relations must be an ordered sequence")
    relations = tuple(
        relation_object_from_dict(relation)
        for relation in relation_values
    )
    relation_set = StructuralEqualityRelationSet(
        relation_set_id=value["relation_set_id"],
        schema_version=value["schema_version"],
        sequential_relation_set_ref=value["sequential_relation_set_ref"],
        structural_summary_ref=value["structural_summary_ref"],
        structural_statistics_ref=value["structural_statistics_ref"],
        input_inventory_ref=value["input_inventory_ref"],
        sequential_relation_count=value["sequential_relation_count"],
        equality_relation_count=value["equality_relation_count"],
        relation_count=value["relation_count"],
        relations=relations,
        responsibility=value["responsibility"],
        relation_set_state=value["relation_set_state"],
        stop=value["stop"],
    )
    expected_id = _expected_set_id(
        sequential_relation_set_ref=relation_set.sequential_relation_set_ref,
        structural_summary_ref=relation_set.structural_summary_ref,
        structural_statistics_ref=relation_set.structural_statistics_ref,
        input_inventory_ref=relation_set.input_inventory_ref,
        sequential_relation_count=relation_set.sequential_relation_count,
        equality_relation_count=relation_set.equality_relation_count,
        relations=relation_set.relations,
    )
    if relation_set.relation_set_id != expected_id:
        raise ValueError(
            "relation_set_id differs from the canonical identity basis"
        )
    return relation_set


__all__: tuple[str, ...] = ()
