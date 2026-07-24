"""Deterministic sequential Structural Relations for Vertical Slice III WP13.

This module consumes immutable Structural Summary and Structural Statistics
artifacts and creates only immediate predecessor/successor Relation Objects.
It never reads source text, infers hierarchy, constructs a graph, or performs
navigation.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
import re
from typing import Mapping

from orion.structural_relation_alpha import (
    RelationObject,
    canonical_relation_object_bytes,
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


SEQUENTIAL_RELATION_SET_SCHEMA_VERSION = (
    "orion.relation-set/sequential/0.1-alpha"
)
SEQUENTIAL_RELATION_KINDS = (
    "immediately_precedes",
    "immediately_follows",
)
RESPONSIBILITY = "sequential_relations"
RELATION_SET_STATE = "candidate"
STOP_AFTER_SEQUENTIAL_RELATIONS = "after_sequential_relations"

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
        raise TypeError("Sequential Relations requires Structural Summary")
    if not isinstance(statistics, StructuralStatisticsDiagnostic):
        raise TypeError("Sequential Relations requires Structural Statistics")
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
        summary.total_declared_element_count,
        summary.first_canonical_ordinal,
        summary.final_canonical_ordinal,
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
        statistics.total_ordered_elements,
        statistics.first_canonical_ordinal,
        statistics.final_canonical_ordinal,
    )
    if summary_lineage != statistics_lineage:
        raise ValueError("Structural Summary and Statistics lineage differs")
    if tuple(span.ordinal for span in statistics.element_spans) != tuple(
        range(statistics.total_ordered_elements)
    ):
        raise ValueError("Structural Statistics order is not canonical")


def _relation_set_identity_basis(
    *,
    structural_summary_ref: str,
    structural_statistics_ref: str,
    input_inventory_ref: str,
    relations: tuple[RelationObject, ...],
) -> dict[str, object]:
    return {
        "schema_version": SEQUENTIAL_RELATION_SET_SCHEMA_VERSION,
        "structural_summary_ref": structural_summary_ref,
        "structural_statistics_ref": structural_statistics_ref,
        "input_inventory_ref": input_inventory_ref,
        "relation_count": len(relations),
        "relation_ids": tuple(relation.relation_id for relation in relations),
        "responsibility": RESPONSIBILITY,
        "relation_set_state": RELATION_SET_STATE,
        "stop": STOP_AFTER_SEQUENTIAL_RELATIONS,
    }


def _expected_relation_set_id(
    *,
    structural_summary_ref: str,
    structural_statistics_ref: str,
    input_inventory_ref: str,
    relations: tuple[RelationObject, ...],
) -> str:
    basis = _relation_set_identity_basis(
        structural_summary_ref=structural_summary_ref,
        structural_statistics_ref=structural_statistics_ref,
        input_inventory_ref=input_inventory_ref,
        relations=relations,
    )
    return f"relation-set-{_digest(basis)[:24]}"


@dataclass(frozen=True, slots=True)
class SequentialRelationSet:
    """Immutable candidate set containing sequential Relation Objects only."""

    relation_set_id: str
    schema_version: str
    structural_summary_ref: str
    structural_statistics_ref: str
    input_inventory_ref: str
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
        if self.schema_version != SEQUENTIAL_RELATION_SET_SCHEMA_VERSION:
            raise ValueError("schema_version is not the WP13 schema")
        for field_name in (
            "structural_summary_ref",
            "structural_statistics_ref",
            "input_inventory_ref",
        ):
            _require_sha256_ref(getattr(self, field_name), field_name)
        if type(self.relation_count) is not int or self.relation_count < 0:
            raise ValueError("relation_count must be a non-negative integer")
        if self.relation_count != len(self.relations):
            raise ValueError("relation_count differs from Relation Objects")
        if any(
            not isinstance(relation, RelationObject)
            for relation in self.relations
        ):
            raise TypeError("relations must contain immutable Relation Objects")
        for relation in self.relations:
            relation.__post_init__()
        if any(
            relation.relation_kind not in SEQUENTIAL_RELATION_KINDS
            for relation in self.relations
        ):
            raise ValueError("WP13 Relation Set contains a forbidden kind")
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
        kinds = tuple(relation.relation_kind for relation in self.relations)
        follows_index = next(
            (
                index
                for index, kind in enumerate(kinds)
                if kind == "immediately_follows"
            ),
            len(kinds),
        )
        if any(
            kind != "immediately_precedes"
            for kind in kinds[:follows_index]
        ) or any(
            kind != "immediately_follows"
            for kind in kinds[follows_index:]
        ):
            raise ValueError("Relation kinds do not follow canonical type order")
        if self.responsibility != RESPONSIBILITY:
            raise ValueError("Relation Set responsibility changed")
        if self.relation_set_state != RELATION_SET_STATE:
            raise ValueError("WP13 Relation Set must remain a candidate")
        if self.stop != STOP_AFTER_SEQUENTIAL_RELATIONS:
            raise ValueError("WP13 STOP boundary changed")


@dataclass(frozen=True, slots=True)
class SequentialRelationSetValidation:
    """Deterministic validation of one WP13 candidate Relation Set."""

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


def generate_sequential_relations(
    summary: StructuralSummaryDiagnostic,
    statistics: StructuralStatisticsDiagnostic,
) -> SequentialRelationSet:
    """Generate immediate adjacency only from canonical Slice II order."""

    _validate_inputs(summary, statistics)
    spans = statistics.element_spans
    adjacent_pairs = tuple(zip(spans, spans[1:]))
    relation_count_per_kind = len(adjacent_pairs)

    precedes = tuple(
        create_relation_object(
            summary,
            statistics,
            relation_kind="immediately_precedes",
            source_element_id=source.element_id,
            target_element_id=target.element_id,
            canonical_order=index,
        )
        for index, (source, target) in enumerate(adjacent_pairs)
    )
    follows = tuple(
        create_relation_object(
            summary,
            statistics,
            relation_kind="immediately_follows",
            source_element_id=target.element_id,
            target_element_id=source.element_id,
            canonical_order=relation_count_per_kind + index,
        )
        for index, (source, target) in enumerate(adjacent_pairs)
    )
    relations = precedes + follows
    for relation in relations:
        validation = validate_relation_object(summary, statistics, relation)
        if not validation.valid:
            raise ValueError(
                "Generated Relation Object failed WP12 validation: "
                + "; ".join(validation.errors)
            )

    structural_summary_ref = _artifact_ref(
        canonical_structural_summary_bytes(summary)
    )
    structural_statistics_ref = _artifact_ref(
        canonical_structural_statistics_bytes(statistics)
    )
    relation_set = SequentialRelationSet(
        relation_set_id=_expected_relation_set_id(
            structural_summary_ref=structural_summary_ref,
            structural_statistics_ref=structural_statistics_ref,
            input_inventory_ref=summary.input_inventory_ref,
            relations=relations,
        ),
        schema_version=SEQUENTIAL_RELATION_SET_SCHEMA_VERSION,
        structural_summary_ref=structural_summary_ref,
        structural_statistics_ref=structural_statistics_ref,
        input_inventory_ref=summary.input_inventory_ref,
        relation_count=len(relations),
        relations=relations,
        responsibility=RESPONSIBILITY,
        relation_set_state=RELATION_SET_STATE,
        stop=STOP_AFTER_SEQUENTIAL_RELATIONS,
    )
    relation_set.__post_init__()
    return relation_set


def validate_sequential_relation_set(
    summary: StructuralSummaryDiagnostic,
    statistics: StructuralStatisticsDiagnostic,
    relation_set: SequentialRelationSet,
) -> SequentialRelationSetValidation:
    """Independently recompute and validate the complete WP13 output."""

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
        expected = generate_sequential_relations(summary, statistics)
    except (AttributeError, TypeError, ValueError) as exc:
        errors.append(f"deterministic generation unavailable: {exc}")

    check(
        "deterministic_generation",
        expected is not None and relation_set == expected,
        "Relation Set differs from deterministic adjacency generation",
    )
    check(
        "relation_set_identity",
        relation_set.relation_set_id
        == _expected_relation_set_id(
            structural_summary_ref=relation_set.structural_summary_ref,
            structural_statistics_ref=relation_set.structural_statistics_ref,
            input_inventory_ref=relation_set.input_inventory_ref,
            relations=relation_set.relations,
        ),
        "Relation Set identity differs from canonical basis",
    )
    relation_validations = tuple(
        validate_relation_object(summary, statistics, relation)
        for relation in relation_set.relations
    )
    check(
        "relation_objects_valid",
        all(validation.valid for validation in relation_validations),
        "Relation Set contains an invalid WP12 Relation Object",
    )
    check(
        "only_sequential_kinds",
        set(
            relation.relation_kind for relation in relation_set.relations
        ).issubset(SEQUENTIAL_RELATION_KINDS),
        "Relation Set contains a non-sequential relation kind",
    )
    expected_pair_count = max(statistics.total_ordered_elements - 1, 0)
    check(
        "complete_adjacency_count",
        relation_set.relation_count == expected_pair_count * 2,
        "Relation Set count does not cover every adjacent pair twice",
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
        "Relation Set does not preserve exact Slice II references",
    )
    check(
        "responsibility_and_stop",
        relation_set.schema_version
        == SEQUENTIAL_RELATION_SET_SCHEMA_VERSION
        and relation_set.responsibility == RESPONSIBILITY
        and relation_set.relation_set_state == RELATION_SET_STATE
        and relation_set.stop == STOP_AFTER_SEQUENTIAL_RELATIONS,
        "WP13 responsibility or STOP changed",
    )

    return SequentialRelationSetValidation(
        valid=not errors,
        checks=tuple(checks),
        errors=tuple(errors),
    )


def sequential_relation_set_as_dict(
    relation_set: SequentialRelationSet,
) -> dict[str, object]:
    """Return the exact deterministic candidate Relation Set shape."""

    relation_set.__post_init__()
    return asdict(relation_set)


def canonical_sequential_relation_set_bytes(
    relation_set: SequentialRelationSet,
) -> bytes:
    """Serialize one WP13 Relation Set as canonical UTF-8 JSON."""

    return _canonical_bytes(sequential_relation_set_as_dict(relation_set))


def sequential_relation_set_from_dict(
    value: Mapping[str, object],
) -> SequentialRelationSet:
    """Parse the exact WP13 schema and reject unknown or missing fields."""

    if not isinstance(value, Mapping):
        raise TypeError("Sequential Relation Set input must be a mapping")
    expected_fields = {
        "relation_set_id",
        "schema_version",
        "structural_summary_ref",
        "structural_statistics_ref",
        "input_inventory_ref",
        "relation_count",
        "relations",
        "responsibility",
        "relation_set_state",
        "stop",
    }
    if set(value) != expected_fields:
        raise ValueError(
            "Sequential Relation Set fields do not match the WP13 schema"
        )
    relation_values = value["relations"]
    if not isinstance(relation_values, (list, tuple)):
        raise TypeError("relations must be an ordered sequence")
    relations = tuple(
        relation_object_from_dict(relation)
        for relation in relation_values
    )
    relation_set = SequentialRelationSet(
        relation_set_id=value["relation_set_id"],
        schema_version=value["schema_version"],
        structural_summary_ref=value["structural_summary_ref"],
        structural_statistics_ref=value["structural_statistics_ref"],
        input_inventory_ref=value["input_inventory_ref"],
        relation_count=value["relation_count"],
        relations=relations,
        responsibility=value["responsibility"],
        relation_set_state=value["relation_set_state"],
        stop=value["stop"],
    )
    expected_id = _expected_relation_set_id(
        structural_summary_ref=relation_set.structural_summary_ref,
        structural_statistics_ref=relation_set.structural_statistics_ref,
        input_inventory_ref=relation_set.input_inventory_ref,
        relations=relation_set.relations,
    )
    if relation_set.relation_set_id != expected_id:
        raise ValueError(
            "relation_set_id differs from the canonical identity basis"
        )
    return relation_set


__all__: tuple[str, ...] = ()
