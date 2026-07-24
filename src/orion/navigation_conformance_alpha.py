"""External observational Navigation Conformance for Slice III WP20.

The validator consumes supplied immutable WP18 and WP19 Navigation artifacts
with their exact frozen dependencies. It creates only a conformance report. It
never constructs, repairs, normalizes, completes, or traverses Navigation.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
import re
from typing import Mapping

from orion.declared_cross_references_alpha import (
    DeclaredReferenceRelationSet,
    canonical_declared_reference_relation_set_bytes,
)
from orion.navigation_construction_alpha import (
    ADJACENCY_RELATION_KINDS,
    CONSTRUCTION_STATE,
    NAVIGATION_CONSTRUCTION_SCHEMA_VERSION,
    STOP_AFTER_NAVIGATION_CONSTRUCTION,
    ConstructedNavigationObject,
    NavigationEntry,
    canonical_constructed_navigation_bytes,
    constructed_navigation_from_dict,
)
from orion.navigation_object_alpha import (
    CONTRACT_STATE,
    NAVIGATION_SCHEMA_VERSION,
    STOP_AFTER_NAVIGATION_OBJECT,
    NavigationObject,
    canonical_navigation_object_bytes,
    navigation_object_from_dict,
)
from orion.relations_certification_alpha import (
    PASSED,
    STOP_AT_RELATIONS_CERTIFIED,
    RelationsCertificationReport,
    canonical_relations_certification_report_bytes,
)
from orion.structural_relation_alpha import canonical_relation_object_bytes
from orion.understand_structural_statistics_alpha import (
    StructuralStatisticsDiagnostic,
    canonical_structural_statistics_bytes,
)
from orion.understand_structural_summary_alpha import (
    StructuralSummaryDiagnostic,
    canonical_structural_summary_bytes,
)


NAVIGATION_CONFORMANCE_SCHEMA_VERSION = (
    "orion.navigation-conformance/0.1-alpha"
)
RESPONSIBILITY = "external_navigation_conformance"
ACCEPTED = "accepted"
REJECTED = "rejected"
STOP_AFTER_NAVIGATION_CONFORMANCE = "after_external_navigation_conformance"

_REPORT_ID = re.compile(r"^navigation-conformance-[0-9a-f]{24}$")
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


def _observed_bytes(value: object, expected_type: type) -> bytes | None:
    if not isinstance(value, expected_type):
        return None
    try:
        return _canonical_bytes(asdict(value))
    except (AttributeError, TypeError, ValueError):
        return None


def _safe_text(value: object, fallback: str) -> str:
    return value if isinstance(value, str) and value else fallback


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


def _report_basis(
    *,
    construction_id: str,
    construction_ref: str | None,
    navigation_id: str,
    navigation_ref: str | None,
    relation_set_id: str,
    relation_set_ref: str | None,
    relations_certification_id: str,
    relations_certification_ref: str | None,
    structural_summary_ref: str | None,
    structural_statistics_ref: str | None,
    valid: bool,
    decision: str,
    checks: tuple[str, ...],
    errors: tuple[str, ...],
    accepted_construction_ref: str | None,
    inputs_unchanged: bool,
) -> dict[str, object]:
    return {
        "schema_version": NAVIGATION_CONFORMANCE_SCHEMA_VERSION,
        "construction_id": construction_id,
        "construction_ref": construction_ref,
        "navigation_id": navigation_id,
        "navigation_ref": navigation_ref,
        "relation_set_id": relation_set_id,
        "relation_set_ref": relation_set_ref,
        "relations_certification_id": relations_certification_id,
        "relations_certification_ref": relations_certification_ref,
        "structural_summary_ref": structural_summary_ref,
        "structural_statistics_ref": structural_statistics_ref,
        "valid": valid,
        "decision": decision,
        "checks": checks,
        "errors": errors,
        "accepted_construction_ref": accepted_construction_ref,
        "inputs_unchanged": inputs_unchanged,
        "responsibility": RESPONSIBILITY,
        "stop": STOP_AFTER_NAVIGATION_CONFORMANCE,
    }


@dataclass(frozen=True, slots=True)
class NavigationConformanceReport:
    """Immutable observation of supplied Navigation artifacts."""

    report_id: str
    schema_version: str
    construction_id: str
    construction_ref: str | None
    navigation_id: str
    navigation_ref: str | None
    relation_set_id: str
    relation_set_ref: str | None
    relations_certification_id: str
    relations_certification_ref: str | None
    structural_summary_ref: str | None
    structural_statistics_ref: str | None
    valid: bool
    decision: str
    checks: tuple[str, ...]
    errors: tuple[str, ...]
    accepted_construction_ref: str | None
    inputs_unchanged: bool
    responsibility: str
    stop: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "checks", tuple(self.checks))
        object.__setattr__(self, "errors", tuple(self.errors))
        if _REPORT_ID.fullmatch(self.report_id) is None:
            raise ValueError("report_id is not canonical")
        if self.schema_version != NAVIGATION_CONFORMANCE_SCHEMA_VERSION:
            raise ValueError("Navigation Conformance schema changed")
        for field_name in (
            "construction_id",
            "navigation_id",
            "relation_set_id",
            "relations_certification_id",
        ):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value:
                raise ValueError(f"{field_name} must be observed exact text")
        for field_name in (
            "construction_ref",
            "navigation_ref",
            "relation_set_ref",
            "relations_certification_ref",
            "structural_summary_ref",
            "structural_statistics_ref",
            "accepted_construction_ref",
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
        if any(not isinstance(item, str) or not item for item in self.checks):
            raise ValueError("checks must be deterministic non-empty labels")
        if any(not isinstance(item, str) or not item for item in self.errors):
            raise ValueError("errors must be deterministic non-empty text")
        if self.valid:
            if self.accepted_construction_ref != self.construction_ref:
                raise ValueError("accepted construction differs from input")
        elif self.accepted_construction_ref is not None:
            raise ValueError("rejected report cannot accept Navigation")
        if type(self.inputs_unchanged) is not bool or not self.inputs_unchanged:
            raise ValueError("Conformance must leave every input unchanged")
        if self.responsibility != RESPONSIBILITY:
            raise ValueError("Navigation Conformance responsibility changed")
        if self.stop != STOP_AFTER_NAVIGATION_CONFORMANCE:
            raise ValueError("Navigation Conformance STOP changed")
        basis = _report_basis(
            construction_id=self.construction_id,
            construction_ref=self.construction_ref,
            navigation_id=self.navigation_id,
            navigation_ref=self.navigation_ref,
            relation_set_id=self.relation_set_id,
            relation_set_ref=self.relation_set_ref,
            relations_certification_id=self.relations_certification_id,
            relations_certification_ref=self.relations_certification_ref,
            structural_summary_ref=self.structural_summary_ref,
            structural_statistics_ref=self.structural_statistics_ref,
            valid=self.valid,
            decision=self.decision,
            checks=self.checks,
            errors=self.errors,
            accepted_construction_ref=self.accepted_construction_ref,
            inputs_unchanged=self.inputs_unchanged,
        )
        if self.report_id != (
            f"navigation-conformance-{_digest(basis)[:24]}"
        ):
            raise ValueError("report_id differs from its observations")


def validate_navigation_conformance(
    constructed: object,
    navigation: object,
    relation_set: object,
    relations_certification: object,
    summary: object,
    statistics: object,
) -> NavigationConformanceReport:
    """Observe supplied Navigation artifacts and return a report only."""

    checks: list[str] = []
    errors: list[str] = []

    def check(name: str, condition: bool, error: str) -> None:
        checks.append(name)
        if not condition:
            errors.append(error)

    before = (
        _observed_bytes(constructed, ConstructedNavigationObject),
        _observed_bytes(navigation, NavigationObject),
        _observed_bytes(relation_set, DeclaredReferenceRelationSet),
        _observed_bytes(
            relations_certification,
            RelationsCertificationReport,
        ),
        _observed_bytes(summary, StructuralSummaryDiagnostic),
        _observed_bytes(statistics, StructuralStatisticsDiagnostic),
    )
    (
        construction_bytes,
        navigation_bytes,
        relation_set_bytes,
        certification_bytes,
        summary_bytes,
        statistics_bytes,
    ) = before
    construction_ref = (
        _artifact_ref(construction_bytes)
        if construction_bytes is not None
        else None
    )
    navigation_ref = (
        _artifact_ref(navigation_bytes) if navigation_bytes is not None else None
    )
    relation_set_ref = (
        _artifact_ref(relation_set_bytes)
        if relation_set_bytes is not None
        else None
    )
    certification_ref = (
        _artifact_ref(certification_bytes)
        if certification_bytes is not None
        else None
    )
    summary_ref = (
        _artifact_ref(summary_bytes) if summary_bytes is not None else None
    )
    statistics_ref = (
        _artifact_ref(statistics_bytes)
        if statistics_bytes is not None
        else None
    )

    supplied = (
        (
            "constructed_navigation_type",
            constructed,
            ConstructedNavigationObject,
            "Input is not immutable WP19 Navigation Construction",
        ),
        (
            "navigation_object_type",
            navigation,
            NavigationObject,
            "Input is not immutable WP18 Navigation Object",
        ),
        (
            "relation_set_type",
            relation_set,
            DeclaredReferenceRelationSet,
            "Input is not immutable WP15 Relation Set",
        ),
        (
            "relations_certification_type",
            relations_certification,
            RelationsCertificationReport,
            "Input is not immutable Relations Certification",
        ),
        (
            "structural_summary_type",
            summary,
            StructuralSummaryDiagnostic,
            "Input is not immutable Structural Summary",
        ),
        (
            "structural_statistics_type",
            statistics,
            StructuralStatisticsDiagnostic,
            "Input is not immutable Structural Statistics",
        ),
    )
    type_validity: dict[str, bool] = {}
    for name, value, expected, error in supplied:
        valid_type = isinstance(value, expected)
        type_validity[name] = valid_type
        check(name, valid_type, error)

    def shape_is_valid(value: object, type_check: str) -> bool:
        if not type_validity[type_check]:
            return False
        try:
            value.__post_init__()
            return True
        except (AttributeError, TypeError, ValueError):
            return False

    constructed_shape = shape_is_valid(
        constructed,
        "constructed_navigation_type",
    )
    navigation_shape = shape_is_valid(navigation, "navigation_object_type")
    relation_set_shape = shape_is_valid(relation_set, "relation_set_type")
    certification_shape = shape_is_valid(
        relations_certification,
        "relations_certification_type",
    )
    summary_shape = shape_is_valid(summary, "structural_summary_type")
    statistics_shape = shape_is_valid(
        statistics,
        "structural_statistics_type",
    )
    for name, condition, error in (
        (
            "constructed_navigation_shape",
            constructed_shape,
            "Constructed Navigation schema, identity, or STOP is malformed",
        ),
        (
            "navigation_object_shape",
            navigation_shape,
            "Navigation Object schema, identity, or STOP is malformed",
        ),
        (
            "relation_set_shape",
            relation_set_shape,
            "Relation Set is malformed",
        ),
        (
            "relations_certification_shape",
            certification_shape,
            "Relations Certification is malformed",
        ),
        (
            "structural_summary_shape",
            summary_shape,
            "Structural Summary is malformed",
        ),
        (
            "structural_statistics_shape",
            statistics_shape,
            "Structural Statistics is malformed",
        ),
    ):
        check(name, condition, error)

    gate_r_valid = (
        certification_shape
        and relations_certification.certified
        and relations_certification.status == PASSED
        and not relations_certification.errors
        and relations_certification.stop == STOP_AT_RELATIONS_CERTIFIED
    )
    check(
        "relations_certification_gate",
        gate_r_valid,
        "Relations Certification Gate has not passed",
    )

    navigation_contract_valid = (
        navigation_shape
        and navigation.navigation_schema_version == NAVIGATION_SCHEMA_VERSION
        and navigation.contract_state == CONTRACT_STATE
        and navigation.stop == STOP_AFTER_NAVIGATION_OBJECT
        and not navigation.externally_conformant
    )
    check(
        "navigation_object_contract",
        navigation_contract_valid,
        "Navigation Object differs from the frozen WP18 contract",
    )

    construction_state_valid = (
        constructed_shape
        and constructed.schema_version
        == NAVIGATION_CONSTRUCTION_SCHEMA_VERSION
        and constructed.construction_state == CONSTRUCTION_STATE
        and constructed.stop == STOP_AFTER_NAVIGATION_CONSTRUCTION
        and not constructed.externally_conformant
    )
    check(
        "navigation_construction_state",
        construction_state_valid,
        "Constructed Navigation is not the exact WP19 candidate state",
    )

    reference_consistency = (
        constructed_shape
        and navigation_shape
        and relation_set_shape
        and certification_shape
        and summary_shape
        and statistics_shape
        and constructed.navigation_id == navigation.navigation_id
        and constructed.navigation_contract_ref == navigation_ref
        and constructed.relation_set_id == relation_set.relation_set_id
        and constructed.relation_set_ref == relation_set_ref
        and constructed.relations_certification_id
        == relations_certification.certification_id
        and constructed.relations_certification_ref == certification_ref
        and constructed.summary_ref == summary_ref
        and constructed.statistics_ref == statistics_ref
        and constructed.provenance_ref == certification_ref
        and navigation.relation_set_id == relation_set.relation_set_id
        and navigation.relation_set_ref == relation_set_ref
        and navigation.relations_certification_id
        == relations_certification.certification_id
        and navigation.relations_certification_ref == certification_ref
        and navigation.summary_id == summary.summary_id
        and navigation.summary_ref == summary_ref
        and navigation.statistics_id == statistics.statistics_id
        and navigation.statistics_ref == statistics_ref
        and relations_certification.relation_set_id
        == relation_set.relation_set_id
        and relations_certification.relation_set_ref == relation_set_ref
        and relations_certification.structural_summary_ref == summary_ref
        and relations_certification.structural_statistics_ref == statistics_ref
    )
    check(
        "certified_reference_consistency",
        reference_consistency,
        "Navigation artifacts do not name the exact certified inputs",
    )

    entries = (
        constructed.entries
        if isinstance(constructed, ConstructedNavigationObject)
        and isinstance(constructed.entries, tuple)
        else ()
    )
    entry_types_valid = all(
        isinstance(entry, NavigationEntry) for entry in entries
    )
    check(
        "navigation_entry_types",
        entry_types_valid,
        "Constructed Navigation contains a malformed entry type",
    )
    entry_order_valid = (
        constructed_shape
        and relation_set_shape
        and tuple(entry.canonical_order for entry in entries)
        == tuple(range(len(entries)))
        and tuple(entry.canonical_order for entry in entries)
        == tuple(
            relation.canonical_order for relation in relation_set.relations
        )
    )
    check(
        "canonical_entry_order",
        entry_order_valid,
        "Navigation Entry ordering differs from certified Relations",
    )
    duplicate_free = (
        entry_types_valid
        and len({entry.entry_id for entry in entries}) == len(entries)
        and len({entry.relation_id for entry in entries}) == len(entries)
        and len({entry.relation_ref for entry in entries}) == len(entries)
    )
    check(
        "duplicate_entry_absence",
        duplicate_free,
        "Constructed Navigation contains duplicate entries or references",
    )

    exact_relation_references = False
    adjacency_references_valid = False
    provenance_valid = False
    if relation_set_shape and entry_types_valid:
        expected_refs = tuple(
            _artifact_ref(canonical_relation_object_bytes(relation))
            for relation in relation_set.relations
        )
        exact_relation_references = (
            len(entries) == len(relation_set.relations)
            and tuple(entry.relation_id for entry in entries)
            == tuple(
                relation.relation_id for relation in relation_set.relations
            )
            and tuple(entry.relation_ref for entry in entries) == expected_refs
            and tuple(entry.relation_kind for entry in entries)
            == tuple(
                relation.relation_kind for relation in relation_set.relations
            )
            and tuple(entry.source_element_id for entry in entries)
            == tuple(
                relation.source_element_id
                for relation in relation_set.relations
            )
            and tuple(entry.target_element_id for entry in entries)
            == tuple(
                relation.target_element_id
                for relation in relation_set.relations
            )
        )
        adjacency_references_valid = (
            len(entries) == len(relation_set.relations)
            and all(
                (
                    entry.structural_adjacency_ref == entry.relation_ref
                    if relation.relation_kind in ADJACENCY_RELATION_KINDS
                    else entry.structural_adjacency_ref is None
                )
                for entry, relation in zip(
                    entries,
                    relation_set.relations,
                )
            )
        )
        provenance_valid = (
            constructed.provenance_ref == certification_ref
            and navigation.provenance_ref == certification_ref
            and len(entries) == len(relation_set.relations)
            and all(
                entry.provenance_ref
                == relation.provenance.input_inventory_ref
                for entry, relation in zip(
                    entries,
                    relation_set.relations,
                )
            )
        )
    check(
        "immutable_relation_references",
        exact_relation_references,
        "Navigation Entries do not exactly reference certified Relations",
    )
    check(
        "structural_adjacency_references",
        adjacency_references_valid,
        "Navigation adjacency references differ from certified Relations",
    )
    check(
        "provenance_preservation",
        provenance_valid,
        "Navigation provenance does not preserve certified lineage",
    )

    navigation_serialization_valid = False
    if navigation_shape and navigation_bytes is not None:
        try:
            parsed_navigation = navigation_object_from_dict(asdict(navigation))
            navigation_serialization_valid = (
                canonical_navigation_object_bytes(navigation)
                == navigation_bytes
                and canonical_navigation_object_bytes(parsed_navigation)
                == navigation_bytes
            )
        except (AttributeError, TypeError, ValueError):
            pass
    check(
        "navigation_canonical_serialization",
        navigation_serialization_valid,
        "Navigation Object canonical serialization does not replay",
    )

    construction_serialization_valid = False
    if constructed_shape and construction_bytes is not None:
        try:
            parsed_construction = constructed_navigation_from_dict(
                asdict(constructed)
            )
            construction_serialization_valid = (
                canonical_constructed_navigation_bytes(constructed)
                == construction_bytes
                and canonical_constructed_navigation_bytes(
                    parsed_construction
                )
                == construction_bytes
            )
        except (AttributeError, TypeError, ValueError):
            pass
    check(
        "construction_canonical_serialization",
        construction_serialization_valid,
        "Constructed Navigation canonical serialization does not replay",
    )

    prohibited_fields = {
        "routes",
        "route",
        "paths",
        "path",
        "traversal",
        "movements",
        "movement",
        "search",
        "search_state",
        "cursor",
        "history",
        "graph",
        "ranking",
        "rank",
        "heuristics",
        "recommendations",
        "orientation_map",
    }
    boundary_valid = (
        construction_bytes is not None
        and navigation_bytes is not None
        and not (
            _nested_keys(asdict(constructed))
            & prohibited_fields
        )
        and not (_nested_keys(asdict(navigation)) & prohibited_fields)
    )
    check(
        "responsibility_boundary",
        boundary_valid,
        "Navigation artifacts contain traversal or downstream state",
    )

    after = (
        _observed_bytes(constructed, ConstructedNavigationObject),
        _observed_bytes(navigation, NavigationObject),
        _observed_bytes(relation_set, DeclaredReferenceRelationSet),
        _observed_bytes(
            relations_certification,
            RelationsCertificationReport,
        ),
        _observed_bytes(summary, StructuralSummaryDiagnostic),
        _observed_bytes(statistics, StructuralStatisticsDiagnostic),
    )
    inputs_unchanged = before == after
    check(
        "inputs_unchanged",
        inputs_unchanged,
        "Navigation Conformance changed a supplied artifact",
    )

    valid = not errors
    decision = ACCEPTED if valid else REJECTED
    accepted_ref = construction_ref if valid else None
    construction_id = _safe_text(
        getattr(constructed, "construction_id", None),
        "unavailable",
    )
    navigation_id = _safe_text(
        getattr(navigation, "navigation_id", None),
        "unavailable",
    )
    relation_set_id = _safe_text(
        getattr(relation_set, "relation_set_id", None),
        "unavailable",
    )
    certification_id = _safe_text(
        getattr(relations_certification, "certification_id", None),
        "unavailable",
    )
    basis = _report_basis(
        construction_id=construction_id,
        construction_ref=construction_ref,
        navigation_id=navigation_id,
        navigation_ref=navigation_ref,
        relation_set_id=relation_set_id,
        relation_set_ref=relation_set_ref,
        relations_certification_id=certification_id,
        relations_certification_ref=certification_ref,
        structural_summary_ref=summary_ref,
        structural_statistics_ref=statistics_ref,
        valid=valid,
        decision=decision,
        checks=tuple(checks),
        errors=tuple(errors),
        accepted_construction_ref=accepted_ref,
        inputs_unchanged=inputs_unchanged,
    )
    return NavigationConformanceReport(
        report_id=f"navigation-conformance-{_digest(basis)[:24]}",
        schema_version=NAVIGATION_CONFORMANCE_SCHEMA_VERSION,
        construction_id=construction_id,
        construction_ref=construction_ref,
        navigation_id=navigation_id,
        navigation_ref=navigation_ref,
        relation_set_id=relation_set_id,
        relation_set_ref=relation_set_ref,
        relations_certification_id=certification_id,
        relations_certification_ref=certification_ref,
        structural_summary_ref=summary_ref,
        structural_statistics_ref=statistics_ref,
        valid=valid,
        decision=decision,
        checks=tuple(checks),
        errors=tuple(errors),
        accepted_construction_ref=accepted_ref,
        inputs_unchanged=inputs_unchanged,
        responsibility=RESPONSIBILITY,
        stop=STOP_AFTER_NAVIGATION_CONFORMANCE,
    )


def navigation_conformance_report_as_dict(
    report: NavigationConformanceReport,
) -> dict[str, object]:
    report.__post_init__()
    return asdict(report)


def canonical_navigation_conformance_report_bytes(
    report: NavigationConformanceReport,
) -> bytes:
    return _canonical_bytes(navigation_conformance_report_as_dict(report))


def navigation_conformance_report_from_dict(
    value: Mapping[str, object],
) -> NavigationConformanceReport:
    if not isinstance(value, Mapping):
        raise TypeError("Navigation Conformance Report must be a mapping")
    expected_fields = {
        "report_id",
        "schema_version",
        "construction_id",
        "construction_ref",
        "navigation_id",
        "navigation_ref",
        "relation_set_id",
        "relation_set_ref",
        "relations_certification_id",
        "relations_certification_ref",
        "structural_summary_ref",
        "structural_statistics_ref",
        "valid",
        "decision",
        "checks",
        "errors",
        "accepted_construction_ref",
        "inputs_unchanged",
        "responsibility",
        "stop",
    }
    if set(value) != expected_fields:
        raise ValueError("Navigation Conformance fields do not match WP20")
    checks = value["checks"]
    errors = value["errors"]
    if not isinstance(checks, (tuple, list)):
        raise TypeError("checks must be ordered")
    if not isinstance(errors, (tuple, list)):
        raise TypeError("errors must be ordered")
    return NavigationConformanceReport(
        **{
            key: item
            for key, item in value.items()
            if key not in {"checks", "errors"}
        },
        checks=tuple(checks),
        errors=tuple(errors),
    )


__all__: tuple[str, ...] = ()
