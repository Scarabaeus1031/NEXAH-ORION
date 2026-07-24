"""Deterministic source and declared-reference Relations for Slice III WP15.

WP15 consumes certified Slice II lineage, the immutable WP14 candidate, and
zero or more explicit immutable cross-reference declarations. It never reads
source text or discovers a reference.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
import re
from typing import Mapping

from orion.structural_equality_relations_alpha import (
    canonical_structural_equality_relation_set_bytes,
    generate_structural_equality_relations,
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


DECLARATION_SCHEMA_VERSION = "orion.declared-cross-reference/0.1-alpha"
DECLARED_REFERENCE_SET_SCHEMA_VERSION = (
    "orion.relation-set/declared-references/0.1-alpha"
)
COMPLETE_RELATION_KIND_ORDER = (
    "immediately_precedes",
    "immediately_follows",
    "source_reference",
    "same_element_kind",
    "same_heading_level",
    "declared_cross_reference",
)
RESPONSIBILITY = "source_and_declared_cross_references"
RELATION_SET_STATE = "candidate"
STOP_AFTER_DECLARED_CROSS_REFERENCES = "after_declared_cross_references"

_ELEMENT_ID = re.compile(r"^element-[0-9a-f]{24}$")
_DECLARATION_ID = re.compile(r"^declared-reference-[0-9a-f]{24}$")
_RELATION_SET_ID = re.compile(r"^relation-set-[0-9a-f]{24}$")
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


def _artifact_ref(value: bytes) -> str:
    return f"sha256:{sha256(value).hexdigest()}"


def _require_text(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{field_name} must be exact non-empty text")


def _require_sha256_ref(value: str, field_name: str) -> None:
    if not isinstance(value, str) or _SHA256_REF.fullmatch(value) is None:
        raise ValueError(f"{field_name} must be a SHA-256 reference")


def _declaration_basis(
    *,
    declaration_version: str,
    source_element_id: str,
    target_element_id: str,
    direction: str,
    provenance_ref: str,
    schema_version: str,
) -> dict[str, object]:
    return {
        "declaration_version": declaration_version,
        "source_element_id": source_element_id,
        "target_element_id": target_element_id,
        "direction": direction,
        "provenance_ref": provenance_ref,
        "schema_version": schema_version,
    }


@dataclass(frozen=True, slots=True)
class AcceptedDeclaredCrossReference:
    """One explicit immutable declaration accepted before Relations begins."""

    declaration_id: str
    declaration_version: str
    source_element_id: str
    target_element_id: str
    direction: str
    provenance_ref: str
    declaration_integrity: str
    schema_version: str

    def __post_init__(self) -> None:
        if _DECLARATION_ID.fullmatch(self.declaration_id) is None:
            raise ValueError("declaration_id is not canonical")
        _require_text(self.declaration_version, "declaration_version")
        if _ELEMENT_ID.fullmatch(self.source_element_id) is None:
            raise ValueError("declaration source is not an element identifier")
        if _ELEMENT_ID.fullmatch(self.target_element_id) is None:
            raise ValueError("declaration target is not an element identifier")
        if self.source_element_id == self.target_element_id:
            raise ValueError("declared reference endpoints must be distinct")
        if self.direction != "directed":
            raise ValueError("declared reference direction must be explicit")
        _require_sha256_ref(self.provenance_ref, "provenance_ref")
        if _SHA256_HEX.fullmatch(self.declaration_integrity) is None:
            raise ValueError("declaration_integrity must be SHA-256 hexadecimal")
        if self.schema_version != DECLARATION_SCHEMA_VERSION:
            raise ValueError("declaration schema version changed")
        basis = _declaration_basis(
            declaration_version=self.declaration_version,
            source_element_id=self.source_element_id,
            target_element_id=self.target_element_id,
            direction=self.direction,
            provenance_ref=self.provenance_ref,
            schema_version=self.schema_version,
        )
        digest = _digest(basis)
        if self.declaration_id != f"declared-reference-{digest[:24]}":
            raise ValueError("declaration_id differs from its exact basis")
        if self.declaration_integrity != digest:
            raise ValueError("declaration_integrity differs from its exact basis")


def declared_cross_reference_from_explicit_values(
    *,
    declaration_version: str,
    source_element_id: str,
    target_element_id: str,
    provenance_ref: str,
) -> AcceptedDeclaredCrossReference:
    """Bind explicit values; this grants no authority and discovers no link."""

    basis = _declaration_basis(
        declaration_version=declaration_version,
        source_element_id=source_element_id,
        target_element_id=target_element_id,
        direction="directed",
        provenance_ref=provenance_ref,
        schema_version=DECLARATION_SCHEMA_VERSION,
    )
    digest = _digest(basis)
    return AcceptedDeclaredCrossReference(
        declaration_id=f"declared-reference-{digest[:24]}",
        declaration_version=declaration_version,
        source_element_id=source_element_id,
        target_element_id=target_element_id,
        direction="directed",
        provenance_ref=provenance_ref,
        declaration_integrity=digest,
        schema_version=DECLARATION_SCHEMA_VERSION,
    )


def canonical_declared_cross_reference_bytes(
    declaration: AcceptedDeclaredCrossReference,
) -> bytes:
    declaration.__post_init__()
    return _canonical_bytes(asdict(declaration))


def accepted_declared_cross_reference_from_dict(
    value: Mapping[str, object],
) -> AcceptedDeclaredCrossReference:
    if not isinstance(value, Mapping):
        raise TypeError("declared cross-reference must be a mapping")
    expected_fields = {
        "declaration_id",
        "declaration_version",
        "source_element_id",
        "target_element_id",
        "direction",
        "provenance_ref",
        "declaration_integrity",
        "schema_version",
    }
    if set(value) != expected_fields:
        raise ValueError("declared cross-reference fields are not exact")
    return AcceptedDeclaredCrossReference(**dict(value))


def _source_boundary_id(
    summary: StructuralSummaryDiagnostic,
) -> str:
    basis = {
        "source_id": summary.source_id,
        "source_revision": summary.source_revision,
        "source_integrity": summary.source_integrity,
        "source_boundary": summary.source_boundary,
    }
    return f"source-boundary-{_digest(basis)[:24]}"


def _validate_inputs(
    summary: StructuralSummaryDiagnostic,
    statistics: StructuralStatisticsDiagnostic,
    declarations: tuple[AcceptedDeclaredCrossReference, ...],
) -> None:
    if not isinstance(summary, StructuralSummaryDiagnostic):
        raise TypeError("WP15 requires immutable Structural Summary")
    if not isinstance(statistics, StructuralStatisticsDiagnostic):
        raise TypeError("WP15 requires immutable Structural Statistics")
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
    ):
        raise ValueError("Structural Summary and Statistics lineage differs")
    if not isinstance(declarations, tuple):
        raise TypeError("accepted declarations must be an immutable tuple")
    declared_ids = {span.element_id for span in statistics.element_spans}
    declaration_ids: set[str] = set()
    endpoint_pairs: set[tuple[str, str]] = set()
    for declaration in declarations:
        if not isinstance(declaration, AcceptedDeclaredCrossReference):
            raise TypeError("cross-reference input is not an accepted declaration")
        declaration.__post_init__()
        if (
            declaration.source_element_id not in declared_ids
            or declaration.target_element_id not in declared_ids
        ):
            raise ValueError("declared cross-reference endpoint is unresolved")
        if declaration.provenance_ref != summary.input_inventory_ref:
            raise ValueError(
                "declared cross-reference provenance does not name the "
                "accepted Inventory"
            )
        if declaration.declaration_id in declaration_ids:
            raise ValueError("duplicate declared cross-reference identity")
        pair = (
            declaration.source_element_id,
            declaration.target_element_id,
        )
        if pair in endpoint_pairs:
            raise ValueError("duplicate declared cross-reference endpoints")
        declaration_ids.add(declaration.declaration_id)
        endpoint_pairs.add(pair)


def _set_identity_basis(
    *,
    structural_equality_relation_set_ref: str,
    structural_summary_ref: str,
    structural_statistics_ref: str,
    input_inventory_ref: str,
    accepted_declaration_refs: tuple[str, ...],
    source_reference_count: int,
    declared_cross_reference_count: int,
    relations: tuple[RelationObject, ...],
) -> dict[str, object]:
    return {
        "schema_version": DECLARED_REFERENCE_SET_SCHEMA_VERSION,
        "structural_equality_relation_set_ref": (
            structural_equality_relation_set_ref
        ),
        "structural_summary_ref": structural_summary_ref,
        "structural_statistics_ref": structural_statistics_ref,
        "input_inventory_ref": input_inventory_ref,
        "accepted_declaration_refs": accepted_declaration_refs,
        "source_reference_count": source_reference_count,
        "declared_cross_reference_count": declared_cross_reference_count,
        "relation_count": len(relations),
        "relation_ids": tuple(relation.relation_id for relation in relations),
        "responsibility": RESPONSIBILITY,
        "relation_set_state": RELATION_SET_STATE,
        "stop": STOP_AFTER_DECLARED_CROSS_REFERENCES,
    }


@dataclass(frozen=True, slots=True)
class DeclaredReferenceRelationSet:
    """Complete immutable WP15 candidate Structural Relation Set."""

    relation_set_id: str
    schema_version: str
    structural_equality_relation_set_ref: str
    structural_summary_ref: str
    structural_statistics_ref: str
    input_inventory_ref: str
    accepted_declaration_refs: tuple[str, ...]
    source_reference_count: int
    declared_cross_reference_count: int
    relation_count: int
    relations: tuple[RelationObject, ...]
    responsibility: str
    relation_set_state: str
    stop: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "accepted_declaration_refs",
            tuple(self.accepted_declaration_refs),
        )
        object.__setattr__(self, "relations", tuple(self.relations))
        if _RELATION_SET_ID.fullmatch(self.relation_set_id) is None:
            raise ValueError("relation_set_id is not canonical")
        if self.schema_version != DECLARED_REFERENCE_SET_SCHEMA_VERSION:
            raise ValueError("schema_version is not the WP15 schema")
        for field_name in (
            "structural_equality_relation_set_ref",
            "structural_summary_ref",
            "structural_statistics_ref",
            "input_inventory_ref",
        ):
            _require_sha256_ref(getattr(self, field_name), field_name)
        if any(
            _SHA256_REF.fullmatch(reference) is None
            for reference in self.accepted_declaration_refs
        ):
            raise ValueError("accepted declaration reference is malformed")
        if len(set(self.accepted_declaration_refs)) != len(
            self.accepted_declaration_refs
        ):
            raise ValueError("accepted declaration references contain duplicates")
        for field_name in (
            "source_reference_count",
            "declared_cross_reference_count",
            "relation_count",
        ):
            value = getattr(self, field_name)
            if type(value) is not int or value < 0:
                raise ValueError(f"{field_name} must be non-negative")
        if self.relation_count != len(self.relations):
            raise ValueError("relation_count does not match relations")
        if self.declared_cross_reference_count != len(
            self.accepted_declaration_refs
        ):
            raise ValueError("declaration count does not match accepted inputs")
        for relation in self.relations:
            if not isinstance(relation, RelationObject):
                raise TypeError("relations must be WP12 Relation Objects")
            relation.__post_init__()
        if tuple(
            relation.canonical_order for relation in self.relations
        ) != tuple(range(self.relation_count)):
            raise ValueError("relations are not in contiguous canonical order")
        keys = tuple(
            (
                relation.relation_kind,
                relation.source_element_id,
                relation.target_element_id,
            )
            for relation in self.relations
        )
        if len(set(keys)) != len(keys):
            raise ValueError("complete candidate contains duplicate relations")
        rank = {
            kind: index for index, kind in enumerate(COMPLETE_RELATION_KIND_ORDER)
        }
        kinds = tuple(relation.relation_kind for relation in self.relations)
        if any(kind not in rank for kind in kinds):
            raise ValueError("complete candidate contains a forbidden kind")
        if tuple(rank[kind] for kind in kinds) != tuple(
            sorted(rank[kind] for kind in kinds)
        ):
            raise ValueError("relations do not follow canonical type order")
        if (
            sum(kind == "source_reference" for kind in kinds)
            != self.source_reference_count
        ):
            raise ValueError("source_reference_count does not match relations")
        if (
            sum(kind == "declared_cross_reference" for kind in kinds)
            != self.declared_cross_reference_count
        ):
            raise ValueError(
                "declared_cross_reference_count does not match relations"
            )
        if self.responsibility != RESPONSIBILITY:
            raise ValueError("WP15 responsibility changed")
        if self.relation_set_state != RELATION_SET_STATE:
            raise ValueError("WP15 set must remain a candidate")
        if self.stop != STOP_AFTER_DECLARED_CROSS_REFERENCES:
            raise ValueError("WP15 STOP boundary changed")
        expected_id = "relation-set-" + _digest(
            _set_identity_basis(
                structural_equality_relation_set_ref=(
                    self.structural_equality_relation_set_ref
                ),
                structural_summary_ref=self.structural_summary_ref,
                structural_statistics_ref=self.structural_statistics_ref,
                input_inventory_ref=self.input_inventory_ref,
                accepted_declaration_refs=self.accepted_declaration_refs,
                source_reference_count=self.source_reference_count,
                declared_cross_reference_count=(
                    self.declared_cross_reference_count
                ),
                relations=self.relations,
            )
        )[:24]
        if self.relation_set_id != expected_id:
            raise ValueError("relation_set_id differs from its exact basis")


@dataclass(frozen=True, slots=True)
class DeclaredReferenceSetValidation:
    valid: bool
    checks: tuple[str, ...]
    errors: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "checks", tuple(self.checks))
        object.__setattr__(self, "errors", tuple(self.errors))
        if type(self.valid) is not bool:
            raise TypeError("valid must be boolean")
        if self.valid != (not self.errors):
            raise ValueError("validation state must match errors")


def _rebind_prior_relations(
    summary: StructuralSummaryDiagnostic,
    statistics: StructuralStatisticsDiagnostic,
    relation_kind: str,
    source_target_pairs: tuple[tuple[str, str], ...],
    start_order: int,
) -> tuple[RelationObject, ...]:
    return tuple(
        create_relation_object(
            summary,
            statistics,
            relation_kind=relation_kind,
            source_element_id=source_id,
            target_element_id=target_id,
            canonical_order=start_order + index,
        )
        for index, (source_id, target_id) in enumerate(source_target_pairs)
    )


def generate_declared_reference_relations(
    summary: StructuralSummaryDiagnostic,
    statistics: StructuralStatisticsDiagnostic,
    declarations: tuple[AcceptedDeclaredCrossReference, ...] = (),
) -> DeclaredReferenceRelationSet:
    """Complete the candidate set using only exact authoritative references."""

    _validate_inputs(summary, statistics, declarations)
    wp14 = generate_structural_equality_relations(summary, statistics)
    prior_by_kind = {
        kind: tuple(
            (
                relation.source_element_id,
                relation.target_element_id,
            )
            for relation in wp14.relations
            if relation.relation_kind == kind
        )
        for kind in (
            "immediately_precedes",
            "immediately_follows",
            "same_element_kind",
            "same_heading_level",
        )
    }
    boundary_id = _source_boundary_id(summary)
    source_pairs = tuple(
        (span.element_id, boundary_id)
        for span in statistics.element_spans
    )
    ordered_declarations = tuple(
        sorted(
            declarations,
            key=lambda declaration: (
                next(
                    span.ordinal
                    for span in statistics.element_spans
                    if span.element_id == declaration.source_element_id
                ),
                next(
                    span.ordinal
                    for span in statistics.element_spans
                    if span.element_id == declaration.target_element_id
                ),
                declaration.declaration_id,
            ),
        )
    )
    declared_pairs = tuple(
        (
            declaration.source_element_id,
            declaration.target_element_id,
        )
        for declaration in ordered_declarations
    )

    relations: tuple[RelationObject, ...] = ()
    groups = (
        ("immediately_precedes", prior_by_kind["immediately_precedes"]),
        ("immediately_follows", prior_by_kind["immediately_follows"]),
        ("source_reference", source_pairs),
        ("same_element_kind", prior_by_kind["same_element_kind"]),
        ("same_heading_level", prior_by_kind["same_heading_level"]),
        ("declared_cross_reference", declared_pairs),
    )
    for relation_kind, pairs in groups:
        relations += _rebind_prior_relations(
            summary,
            statistics,
            relation_kind,
            pairs,
            len(relations),
        )
    for relation in relations:
        validation = validate_relation_object(summary, statistics, relation)
        if not validation.valid:
            raise ValueError(
                "Generated reference Relation failed WP12 validation: "
                + "; ".join(validation.errors)
            )

    declaration_refs = tuple(
        _artifact_ref(canonical_declared_cross_reference_bytes(declaration))
        for declaration in ordered_declarations
    )
    wp14_ref = _artifact_ref(
        canonical_structural_equality_relation_set_bytes(wp14)
    )
    summary_ref = _artifact_ref(canonical_structural_summary_bytes(summary))
    statistics_ref = _artifact_ref(
        canonical_structural_statistics_bytes(statistics)
    )
    basis = _set_identity_basis(
        structural_equality_relation_set_ref=wp14_ref,
        structural_summary_ref=summary_ref,
        structural_statistics_ref=statistics_ref,
        input_inventory_ref=summary.input_inventory_ref,
        accepted_declaration_refs=declaration_refs,
        source_reference_count=len(source_pairs),
        declared_cross_reference_count=len(declared_pairs),
        relations=relations,
    )
    return DeclaredReferenceRelationSet(
        relation_set_id=f"relation-set-{_digest(basis)[:24]}",
        schema_version=DECLARED_REFERENCE_SET_SCHEMA_VERSION,
        structural_equality_relation_set_ref=wp14_ref,
        structural_summary_ref=summary_ref,
        structural_statistics_ref=statistics_ref,
        input_inventory_ref=summary.input_inventory_ref,
        accepted_declaration_refs=declaration_refs,
        source_reference_count=len(source_pairs),
        declared_cross_reference_count=len(declared_pairs),
        relation_count=len(relations),
        relations=relations,
        responsibility=RESPONSIBILITY,
        relation_set_state=RELATION_SET_STATE,
        stop=STOP_AFTER_DECLARED_CROSS_REFERENCES,
    )


def validate_declared_reference_relation_set(
    summary: StructuralSummaryDiagnostic,
    statistics: StructuralStatisticsDiagnostic,
    declarations: tuple[AcceptedDeclaredCrossReference, ...],
    relation_set: DeclaredReferenceRelationSet,
) -> DeclaredReferenceSetValidation:
    checks: list[str] = []
    errors: list[str] = []
    try:
        _validate_inputs(summary, statistics, declarations)
        checks.append("inputs_valid")
    except (AttributeError, TypeError, ValueError) as exc:
        checks.append("inputs_valid")
        errors.append(str(exc))
    try:
        relation_set.__post_init__()
        checks.append("relation_set_shape_valid")
    except (AttributeError, TypeError, ValueError) as exc:
        checks.append("relation_set_shape_valid")
        errors.append(str(exc))
    expected = None
    try:
        expected = generate_declared_reference_relations(
            summary,
            statistics,
            declarations,
        )
    except (AttributeError, TypeError, ValueError) as exc:
        errors.append(f"deterministic generation unavailable: {exc}")
    checks.append("deterministic_generation")
    if expected is None or expected != relation_set:
        errors.append("Relation Set differs from deterministic generation")
    checks.append("wp12_relation_objects_valid")
    if not all(
        validate_relation_object(summary, statistics, relation).valid
        for relation in relation_set.relations
    ):
        errors.append("Relation Set contains an invalid WP12 Relation Object")
    return DeclaredReferenceSetValidation(
        valid=not errors,
        checks=tuple(checks),
        errors=tuple(errors),
    )


def declared_reference_relation_set_as_dict(
    relation_set: DeclaredReferenceRelationSet,
) -> dict[str, object]:
    relation_set.__post_init__()
    return asdict(relation_set)


def canonical_declared_reference_relation_set_bytes(
    relation_set: DeclaredReferenceRelationSet,
) -> bytes:
    return _canonical_bytes(declared_reference_relation_set_as_dict(relation_set))


def declared_reference_relation_set_from_dict(
    value: Mapping[str, object],
) -> DeclaredReferenceRelationSet:
    if not isinstance(value, Mapping):
        raise TypeError("Declared Reference Relation Set must be a mapping")
    expected_fields = {
        "relation_set_id",
        "schema_version",
        "structural_equality_relation_set_ref",
        "structural_summary_ref",
        "structural_statistics_ref",
        "input_inventory_ref",
        "accepted_declaration_refs",
        "source_reference_count",
        "declared_cross_reference_count",
        "relation_count",
        "relations",
        "responsibility",
        "relation_set_state",
        "stop",
    }
    if set(value) != expected_fields:
        raise ValueError("Declared Reference Relation Set fields are not exact")
    relation_values = value["relations"]
    if not isinstance(relation_values, (list, tuple)):
        raise TypeError("relations must be an ordered sequence")
    declaration_refs = value["accepted_declaration_refs"]
    if not isinstance(declaration_refs, (list, tuple)):
        raise TypeError("accepted_declaration_refs must be ordered")
    return DeclaredReferenceRelationSet(
        relation_set_id=value["relation_set_id"],
        schema_version=value["schema_version"],
        structural_equality_relation_set_ref=(
            value["structural_equality_relation_set_ref"]
        ),
        structural_summary_ref=value["structural_summary_ref"],
        structural_statistics_ref=value["structural_statistics_ref"],
        input_inventory_ref=value["input_inventory_ref"],
        accepted_declaration_refs=tuple(declaration_refs),
        source_reference_count=value["source_reference_count"],
        declared_cross_reference_count=value[
            "declared_cross_reference_count"
        ],
        relation_count=value["relation_count"],
        relations=tuple(
            relation_object_from_dict(relation)
            for relation in relation_values
        ),
        responsibility=value["responsibility"],
        relation_set_state=value["relation_set_state"],
        stop=value["stop"],
    )


__all__: tuple[str, ...] = ()
