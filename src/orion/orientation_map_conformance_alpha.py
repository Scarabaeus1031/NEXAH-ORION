"""External observational Orientation Map Conformance for Slice III WP24.

The validator observes supplied immutable WP22 and WP23 Orientation Map
artifacts and their exact frozen lineage. It creates only a conformance report.
It never constructs, repairs, normalizes, completes, visualizes, or interprets
an Orientation Map.
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
from orion.navigation_certification_alpha import (
    PASSED,
    STOP_AT_NAVIGATION_CERTIFIED,
    NavigationCertificationReport,
    canonical_navigation_certification_report_bytes,
)
from orion.navigation_conformance_alpha import (
    NavigationConformanceReport,
    canonical_navigation_conformance_report_bytes,
)
from orion.navigation_construction_alpha import (
    ADJACENCY_RELATION_KINDS,
    ConstructedNavigationObject,
    NavigationEntry,
    canonical_constructed_navigation_bytes,
)
from orion.navigation_object_alpha import (
    NavigationObject,
    canonical_navigation_object_bytes,
)
from orion.orientation_map_construction_alpha import (
    CONSTRUCTION_STATE,
    ORIENTATION_MAP_CONSTRUCTION_SCHEMA_VERSION,
    SERIALIZATION_VERSION as CONSTRUCTION_SERIALIZATION_VERSION,
    STOP_AFTER_ORIENTATION_MAP_CONSTRUCTION,
    ConstructedOrientationMap,
    OrientationMapEntry,
    canonical_constructed_orientation_map_bytes,
    constructed_orientation_map_from_dict,
)
from orion.orientation_map_object_alpha import (
    CONTRACT_STATE,
    ORIENTATION_MAP_SCHEMA_VERSION,
    SERIALIZATION_VERSION as MAP_SERIALIZATION_VERSION,
    STOP_AFTER_ORIENTATION_MAP_OBJECT,
    OrientationMapObject,
    canonical_orientation_map_object_bytes,
    orientation_map_object_from_dict,
)
from orion.relations_certification_alpha import (
    PASSED as RELATIONS_PASSED,
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


ORIENTATION_MAP_CONFORMANCE_SCHEMA_VERSION = (
    "orion.orientation-map-conformance/0.1-alpha"
)
RESPONSIBILITY = "external_orientation_map_conformance"
ACCEPTED = "accepted"
REJECTED = "rejected"
STOP_AFTER_ORIENTATION_MAP_CONFORMANCE = (
    "after_external_orientation_map_conformance"
)

_REPORT_ID = re.compile(r"^orientation-map-conformance-[0-9a-f]{24}$")
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
    orientation_map_id: str,
    orientation_map_ref: str | None,
    construction_id: str,
    construction_ref: str | None,
    navigation_certification_id: str,
    navigation_certification_ref: str | None,
    relation_set_id: str,
    relation_set_ref: str | None,
    structural_summary_ref: str | None,
    structural_statistics_ref: str | None,
    valid: bool,
    decision: str,
    checks: tuple[str, ...],
    errors: tuple[str, ...],
    accepted_orientation_map_ref: str | None,
    accepted_construction_ref: str | None,
    inputs_unchanged: bool,
) -> dict[str, object]:
    return {
        "schema_version": ORIENTATION_MAP_CONFORMANCE_SCHEMA_VERSION,
        "orientation_map_id": orientation_map_id,
        "orientation_map_ref": orientation_map_ref,
        "construction_id": construction_id,
        "construction_ref": construction_ref,
        "navigation_certification_id": navigation_certification_id,
        "navigation_certification_ref": navigation_certification_ref,
        "relation_set_id": relation_set_id,
        "relation_set_ref": relation_set_ref,
        "structural_summary_ref": structural_summary_ref,
        "structural_statistics_ref": structural_statistics_ref,
        "valid": valid,
        "decision": decision,
        "checks": checks,
        "errors": errors,
        "accepted_orientation_map_ref": accepted_orientation_map_ref,
        "accepted_construction_ref": accepted_construction_ref,
        "inputs_unchanged": inputs_unchanged,
        "responsibility": RESPONSIBILITY,
        "stop": STOP_AFTER_ORIENTATION_MAP_CONFORMANCE,
    }


@dataclass(frozen=True, slots=True)
class OrientationMapConformanceReport:
    """Immutable observation of supplied Orientation Map artifacts."""

    report_id: str
    schema_version: str
    orientation_map_id: str
    orientation_map_ref: str | None
    construction_id: str
    construction_ref: str | None
    navigation_certification_id: str
    navigation_certification_ref: str | None
    relation_set_id: str
    relation_set_ref: str | None
    structural_summary_ref: str | None
    structural_statistics_ref: str | None
    valid: bool
    decision: str
    checks: tuple[str, ...]
    errors: tuple[str, ...]
    accepted_orientation_map_ref: str | None
    accepted_construction_ref: str | None
    inputs_unchanged: bool
    responsibility: str
    stop: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "checks", tuple(self.checks))
        object.__setattr__(self, "errors", tuple(self.errors))
        if _REPORT_ID.fullmatch(self.report_id) is None:
            raise ValueError("report_id is not canonical")
        if self.schema_version != ORIENTATION_MAP_CONFORMANCE_SCHEMA_VERSION:
            raise ValueError("Orientation Map Conformance schema changed")
        for field_name in (
            "orientation_map_id",
            "construction_id",
            "navigation_certification_id",
            "relation_set_id",
        ):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value:
                raise ValueError(f"{field_name} must be observed exact text")
        for field_name in (
            "orientation_map_ref",
            "construction_ref",
            "navigation_certification_ref",
            "relation_set_ref",
            "structural_summary_ref",
            "structural_statistics_ref",
            "accepted_orientation_map_ref",
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
            if self.accepted_orientation_map_ref != self.orientation_map_ref:
                raise ValueError("accepted Map Object differs from input")
            if self.accepted_construction_ref != self.construction_ref:
                raise ValueError("accepted Map Construction differs from input")
        elif (
            self.accepted_orientation_map_ref is not None
            or self.accepted_construction_ref is not None
        ):
            raise ValueError("rejected report cannot accept Map artifacts")
        if type(self.inputs_unchanged) is not bool or not self.inputs_unchanged:
            raise ValueError("Conformance must leave every input unchanged")
        if self.responsibility != RESPONSIBILITY:
            raise ValueError("Orientation Map Conformance responsibility changed")
        if self.stop != STOP_AFTER_ORIENTATION_MAP_CONFORMANCE:
            raise ValueError("Orientation Map Conformance STOP changed")
        basis = _report_basis(
            orientation_map_id=self.orientation_map_id,
            orientation_map_ref=self.orientation_map_ref,
            construction_id=self.construction_id,
            construction_ref=self.construction_ref,
            navigation_certification_id=self.navigation_certification_id,
            navigation_certification_ref=self.navigation_certification_ref,
            relation_set_id=self.relation_set_id,
            relation_set_ref=self.relation_set_ref,
            structural_summary_ref=self.structural_summary_ref,
            structural_statistics_ref=self.structural_statistics_ref,
            valid=self.valid,
            decision=self.decision,
            checks=self.checks,
            errors=self.errors,
            accepted_orientation_map_ref=self.accepted_orientation_map_ref,
            accepted_construction_ref=self.accepted_construction_ref,
            inputs_unchanged=self.inputs_unchanged,
        )
        if self.report_id != (
            f"orientation-map-conformance-{_digest(basis)[:24]}"
        ):
            raise ValueError("report_id differs from its observations")


def validate_orientation_map_conformance(
    orientation_map: object,
    constructed_map: object,
    navigation_certification: object,
    navigation: object,
    constructed_navigation: object,
    navigation_conformance: object,
    relation_set: object,
    relations_certification: object,
    summary: object,
    statistics: object,
) -> OrientationMapConformanceReport:
    """Observe supplied Orientation Map artifacts and return a report only."""

    checks: list[str] = []
    errors: list[str] = []

    def check(name: str, condition: bool, error: str) -> None:
        checks.append(name)
        if not condition:
            errors.append(error)

    expected_types = (
        OrientationMapObject,
        ConstructedOrientationMap,
        NavigationCertificationReport,
        NavigationObject,
        ConstructedNavigationObject,
        NavigationConformanceReport,
        DeclaredReferenceRelationSet,
        RelationsCertificationReport,
        StructuralSummaryDiagnostic,
        StructuralStatisticsDiagnostic,
    )
    supplied_values = (
        orientation_map,
        constructed_map,
        navigation_certification,
        navigation,
        constructed_navigation,
        navigation_conformance,
        relation_set,
        relations_certification,
        summary,
        statistics,
    )
    labels = (
        "orientation_map_object",
        "constructed_orientation_map",
        "navigation_certification",
        "navigation_object",
        "constructed_navigation",
        "navigation_conformance",
        "relation_set",
        "relations_certification",
        "structural_summary",
        "structural_statistics",
    )
    before = tuple(
        _observed_bytes(value, expected)
        for value, expected in zip(
            supplied_values,
            expected_types,
            strict=True,
        )
    )
    refs = tuple(
        _artifact_ref(value) if value is not None else None
        for value in before
    )
    (
        orientation_map_bytes,
        construction_bytes,
        navigation_certification_bytes,
        navigation_bytes,
        navigation_construction_bytes,
        navigation_conformance_bytes,
        relation_set_bytes,
        relations_certification_bytes,
        summary_bytes,
        statistics_bytes,
    ) = before
    (
        orientation_map_ref,
        construction_ref,
        navigation_certification_ref,
        navigation_ref,
        navigation_construction_ref,
        navigation_conformance_ref,
        relation_set_ref,
        relations_certification_ref,
        summary_ref,
        statistics_ref,
    ) = refs

    type_validity: dict[str, bool] = {}
    for label, value, expected in zip(
        labels,
        supplied_values,
        expected_types,
        strict=True,
    ):
        valid_type = isinstance(value, expected)
        type_validity[label] = valid_type
        check(
            f"{label}_type",
            valid_type,
            f"Input is not immutable {label.replace('_', ' ').title()}",
        )

    def shape_is_valid(value: object, label: str) -> bool:
        if not type_validity[label]:
            return False
        try:
            value.__post_init__()
            return True
        except (AttributeError, TypeError, ValueError):
            return False

    shapes = {
        label: shape_is_valid(value, label)
        for label, value in zip(labels, supplied_values, strict=True)
    }
    for label in labels:
        check(
            f"{label}_shape",
            shapes[label],
            f"{label.replace('_', ' ').title()} is malformed",
        )

    navigation_gate_valid = (
        shapes["navigation_certification"]
        and navigation_certification.certified
        and navigation_certification.status == PASSED
        and not navigation_certification.errors
        and navigation_certification.stop == STOP_AT_NAVIGATION_CERTIFIED
    )
    check(
        "navigation_certification_gate",
        navigation_gate_valid,
        "Navigation Certification Gate has not passed",
    )
    relations_gate_valid = (
        shapes["relations_certification"]
        and relations_certification.certified
        and relations_certification.status == RELATIONS_PASSED
        and not relations_certification.errors
        and relations_certification.stop == STOP_AT_RELATIONS_CERTIFIED
    )
    check(
        "relations_certification_gate",
        relations_gate_valid,
        "Relations Certification Gate has not passed",
    )

    map_contract_valid = (
        shapes["orientation_map_object"]
        and orientation_map.orientation_map_schema_version
        == ORIENTATION_MAP_SCHEMA_VERSION
        and orientation_map.serialization_version == MAP_SERIALIZATION_VERSION
        and orientation_map.contract_state == CONTRACT_STATE
        and orientation_map.canonical_order == 0
        and not orientation_map.externally_conformant
        and orientation_map.stop == STOP_AFTER_ORIENTATION_MAP_OBJECT
    )
    check(
        "orientation_map_contract",
        map_contract_valid,
        "Orientation Map Object differs from the frozen WP22 contract",
    )
    construction_state_valid = (
        shapes["constructed_orientation_map"]
        and constructed_map.schema_version
        == ORIENTATION_MAP_CONSTRUCTION_SCHEMA_VERSION
        and constructed_map.serialization_version
        == CONSTRUCTION_SERIALIZATION_VERSION
        and constructed_map.construction_state == CONSTRUCTION_STATE
        and not constructed_map.externally_conformant
        and constructed_map.stop == STOP_AFTER_ORIENTATION_MAP_CONSTRUCTION
    )
    check(
        "orientation_map_construction_state",
        construction_state_valid,
        "Constructed Orientation Map is not the exact WP23 candidate state",
    )

    reference_consistency = (
        all(shapes.values())
        and orientation_map.navigation_certification_id
        == navigation_certification.certification_id
        and orientation_map.navigation_certification_ref
        == navigation_certification_ref
        and orientation_map.navigation_object_id == navigation.navigation_id
        and orientation_map.navigation_object_ref == navigation_ref
        and orientation_map.navigation_construction_id
        == constructed_navigation.construction_id
        and orientation_map.navigation_construction_ref
        == navigation_construction_ref
        and orientation_map.navigation_conformance_id
        == navigation_conformance.report_id
        and orientation_map.navigation_conformance_ref
        == navigation_conformance_ref
        and orientation_map.relation_set_id == relation_set.relation_set_id
        and orientation_map.relation_set_ref == relation_set_ref
        and orientation_map.relations_certification_id
        == relations_certification.certification_id
        and orientation_map.relations_certification_ref
        == relations_certification_ref
        and orientation_map.summary_id == summary.summary_id
        and orientation_map.summary_ref == summary_ref
        and orientation_map.statistics_id == statistics.statistics_id
        and orientation_map.statistics_ref == statistics_ref
        and orientation_map.provenance_ref == navigation_certification_ref
        and constructed_map.orientation_map_id
        == orientation_map.orientation_map_id
        and constructed_map.orientation_map_contract_ref
        == orientation_map_ref
        and constructed_map.navigation_certification_id
        == navigation_certification.certification_id
        and constructed_map.navigation_certification_ref
        == navigation_certification_ref
        and constructed_map.navigation_construction_id
        == constructed_navigation.construction_id
        and constructed_map.navigation_construction_ref
        == navigation_construction_ref
        and constructed_map.provenance_ref == navigation_certification_ref
        and navigation_certification.navigation_id == navigation.navigation_id
        and navigation_certification.navigation_ref == navigation_ref
        and navigation_certification.construction_id
        == constructed_navigation.construction_id
        and navigation_certification.construction_ref
        == navigation_construction_ref
        and navigation_certification.conformance_report_id
        == navigation_conformance.report_id
        and navigation_certification.conformance_report_ref
        == navigation_conformance_ref
        and navigation_certification.relation_set_ref == relation_set_ref
        and navigation_certification.relations_certification_ref
        == relations_certification_ref
        and navigation_certification.structural_summary_ref == summary_ref
        and navigation_certification.structural_statistics_ref
        == statistics_ref
        and relations_certification.relation_set_id
        == relation_set.relation_set_id
        and relations_certification.relation_set_ref == relation_set_ref
        and relations_certification.structural_summary_ref == summary_ref
        and relations_certification.structural_statistics_ref == statistics_ref
    )
    check(
        "certified_reference_consistency",
        reference_consistency,
        "Orientation Map artifacts do not name the exact certified inputs",
    )

    map_entries = (
        constructed_map.entries
        if isinstance(constructed_map, ConstructedOrientationMap)
        and isinstance(constructed_map.entries, tuple)
        else ()
    )
    navigation_entries = (
        constructed_navigation.entries
        if isinstance(constructed_navigation, ConstructedNavigationObject)
        and isinstance(constructed_navigation.entries, tuple)
        else ()
    )
    relation_objects = (
        relation_set.relations
        if isinstance(relation_set, DeclaredReferenceRelationSet)
        and isinstance(relation_set.relations, tuple)
        else ()
    )
    map_entry_types_valid = all(
        isinstance(entry, OrientationMapEntry) for entry in map_entries
    )
    navigation_entry_types_valid = all(
        isinstance(entry, NavigationEntry) for entry in navigation_entries
    )
    check(
        "orientation_map_entry_types",
        map_entry_types_valid,
        "Constructed Orientation Map contains a malformed entry type",
    )
    entry_order_valid = (
        shapes["constructed_orientation_map"]
        and map_entry_types_valid
        and navigation_entry_types_valid
        and len(map_entries) == len(navigation_entries)
        and tuple(entry.canonical_order for entry in map_entries)
        == tuple(range(len(map_entries)))
        and tuple(entry.canonical_order for entry in map_entries)
        == tuple(entry.canonical_order for entry in navigation_entries)
    )
    check(
        "canonical_entry_order",
        entry_order_valid,
        "Orientation Map ordering differs from certified Navigation",
    )
    duplicate_free = (
        map_entry_types_valid
        and len({entry.entry_id for entry in map_entries}) == len(map_entries)
        and len({entry.navigation_entry_id for entry in map_entries})
        == len(map_entries)
        and len({entry.navigation_entry_ref for entry in map_entries})
        == len(map_entries)
        and len({entry.relation_id for entry in map_entries})
        == len(map_entries)
        and len({entry.relation_ref for entry in map_entries})
        == len(map_entries)
    )
    check(
        "duplicate_entry_absence",
        duplicate_free,
        "Constructed Orientation Map contains duplicate entries or references",
    )

    exact_navigation_references = False
    exact_relation_references = False
    exact_adjacency_references = False
    provenance_valid = False
    if (
        map_entry_types_valid
        and navigation_entry_types_valid
        and len(map_entries) == len(navigation_entries)
    ):
        expected_navigation_refs = tuple(
            _artifact_ref(_canonical_bytes(asdict(entry)))
            for entry in navigation_entries
        )
        exact_navigation_references = (
            tuple(entry.navigation_entry_id for entry in map_entries)
            == tuple(entry.entry_id for entry in navigation_entries)
            and tuple(entry.navigation_entry_ref for entry in map_entries)
            == expected_navigation_refs
            and all(
                (
                    map_entry.relation_id == navigation_entry.relation_id
                    and map_entry.relation_ref == navigation_entry.relation_ref
                    and map_entry.relation_kind
                    == navigation_entry.relation_kind
                    and map_entry.source_element_id
                    == navigation_entry.source_element_id
                    and map_entry.target_element_id
                    == navigation_entry.target_element_id
                )
                for map_entry, navigation_entry in zip(
                    map_entries,
                    navigation_entries,
                    strict=True,
                )
            )
        )
        exact_adjacency_references = all(
            map_entry.structural_adjacency_ref
            == navigation_entry.structural_adjacency_ref
            and (
                map_entry.structural_adjacency_ref == map_entry.relation_ref
                if map_entry.relation_kind in ADJACENCY_RELATION_KINDS
                else map_entry.structural_adjacency_ref is None
            )
            for map_entry, navigation_entry in zip(
                map_entries,
                navigation_entries,
                strict=True,
            )
        )
        provenance_valid = (
            constructed_map.provenance_ref == navigation_certification_ref
            and orientation_map.provenance_ref == navigation_certification_ref
            and all(
                map_entry.provenance_ref == navigation_entry.provenance_ref
                for map_entry, navigation_entry in zip(
                    map_entries,
                    navigation_entries,
                    strict=True,
                )
            )
        )
    if (
        map_entry_types_valid
        and len(map_entries) == len(relation_objects)
    ):
        expected_relation_refs = tuple(
            _artifact_ref(canonical_relation_object_bytes(relation))
            for relation in relation_objects
        )
        exact_relation_references = (
            tuple(entry.relation_id for entry in map_entries)
            == tuple(relation.relation_id for relation in relation_objects)
            and tuple(entry.relation_ref for entry in map_entries)
            == expected_relation_refs
            and tuple(entry.relation_kind for entry in map_entries)
            == tuple(relation.relation_kind for relation in relation_objects)
            and tuple(entry.source_element_id for entry in map_entries)
            == tuple(
                relation.source_element_id for relation in relation_objects
            )
            and tuple(entry.target_element_id for entry in map_entries)
            == tuple(
                relation.target_element_id for relation in relation_objects
            )
        )
    check(
        "exact_navigation_entry_references",
        exact_navigation_references,
        "Orientation Map Entries do not exactly reference Navigation Entries",
    )
    check(
        "exact_relation_references",
        exact_relation_references,
        "Orientation Map Entries do not exactly reference certified Relations",
    )
    check(
        "exact_structural_adjacency_references",
        exact_adjacency_references,
        "Orientation Map adjacency differs from certified Navigation",
    )
    check(
        "provenance_preservation",
        provenance_valid,
        "Orientation Map provenance does not preserve certified lineage",
    )

    map_serialization_valid = False
    if shapes["orientation_map_object"] and orientation_map_bytes is not None:
        try:
            parsed_map = orientation_map_object_from_dict(
                asdict(orientation_map)
            )
            map_serialization_valid = (
                canonical_orientation_map_object_bytes(orientation_map)
                == orientation_map_bytes
                and canonical_orientation_map_object_bytes(parsed_map)
                == orientation_map_bytes
            )
        except (AttributeError, TypeError, ValueError):
            pass
    check(
        "orientation_map_canonical_serialization",
        map_serialization_valid,
        "Orientation Map Object canonical serialization does not replay",
    )
    construction_serialization_valid = False
    if shapes["constructed_orientation_map"] and construction_bytes is not None:
        try:
            parsed_construction = constructed_orientation_map_from_dict(
                asdict(constructed_map)
            )
            construction_serialization_valid = (
                canonical_constructed_orientation_map_bytes(constructed_map)
                == construction_bytes
                and canonical_constructed_orientation_map_bytes(
                    parsed_construction
                )
                == construction_bytes
            )
        except (AttributeError, TypeError, ValueError):
            pass
    check(
        "construction_canonical_serialization",
        construction_serialization_valid,
        "Constructed Orientation Map canonical serialization does not replay",
    )

    prohibited_fields = {
        "coordinates",
        "coordinate",
        "geometry",
        "layout",
        "positions",
        "position",
        "rendering_state",
        "visualization_state",
        "camera_state",
        "animation_state",
        "interaction_state",
        "clusters",
        "clustering",
        "ranking",
        "recommendations",
        "semantic_interpretation",
        "semantic_neighborhoods",
        "routes",
        "route",
        "traversal",
        "traversal_execution",
    }
    boundary_valid = (
        orientation_map_bytes is not None
        and construction_bytes is not None
        and not (_nested_keys(asdict(orientation_map)) & prohibited_fields)
        and not (_nested_keys(asdict(constructed_map)) & prohibited_fields)
    )
    check(
        "responsibility_boundary",
        boundary_valid,
        "Orientation Map artifacts contain forbidden downstream state",
    )

    after = tuple(
        _observed_bytes(value, expected)
        for value, expected in zip(
            supplied_values,
            expected_types,
            strict=True,
        )
    )
    inputs_unchanged = before == after
    check(
        "inputs_unchanged",
        inputs_unchanged,
        "Orientation Map Conformance changed a supplied artifact",
    )

    valid = not errors
    decision = ACCEPTED if valid else REJECTED
    accepted_map_ref = orientation_map_ref if valid else None
    accepted_construction_ref = construction_ref if valid else None
    orientation_map_id = _safe_text(
        getattr(orientation_map, "orientation_map_id", None),
        "unavailable",
    )
    construction_id = _safe_text(
        getattr(constructed_map, "construction_id", None),
        "unavailable",
    )
    navigation_certification_id = _safe_text(
        getattr(navigation_certification, "certification_id", None),
        "unavailable",
    )
    relation_set_id = _safe_text(
        getattr(relation_set, "relation_set_id", None),
        "unavailable",
    )
    basis = _report_basis(
        orientation_map_id=orientation_map_id,
        orientation_map_ref=orientation_map_ref,
        construction_id=construction_id,
        construction_ref=construction_ref,
        navigation_certification_id=navigation_certification_id,
        navigation_certification_ref=navigation_certification_ref,
        relation_set_id=relation_set_id,
        relation_set_ref=relation_set_ref,
        structural_summary_ref=summary_ref,
        structural_statistics_ref=statistics_ref,
        valid=valid,
        decision=decision,
        checks=tuple(checks),
        errors=tuple(errors),
        accepted_orientation_map_ref=accepted_map_ref,
        accepted_construction_ref=accepted_construction_ref,
        inputs_unchanged=inputs_unchanged,
    )
    return OrientationMapConformanceReport(
        report_id=f"orientation-map-conformance-{_digest(basis)[:24]}",
        schema_version=ORIENTATION_MAP_CONFORMANCE_SCHEMA_VERSION,
        orientation_map_id=orientation_map_id,
        orientation_map_ref=orientation_map_ref,
        construction_id=construction_id,
        construction_ref=construction_ref,
        navigation_certification_id=navigation_certification_id,
        navigation_certification_ref=navigation_certification_ref,
        relation_set_id=relation_set_id,
        relation_set_ref=relation_set_ref,
        structural_summary_ref=summary_ref,
        structural_statistics_ref=statistics_ref,
        valid=valid,
        decision=decision,
        checks=tuple(checks),
        errors=tuple(errors),
        accepted_orientation_map_ref=accepted_map_ref,
        accepted_construction_ref=accepted_construction_ref,
        inputs_unchanged=inputs_unchanged,
        responsibility=RESPONSIBILITY,
        stop=STOP_AFTER_ORIENTATION_MAP_CONFORMANCE,
    )


def orientation_map_conformance_report_as_dict(
    report: OrientationMapConformanceReport,
) -> dict[str, object]:
    report.__post_init__()
    return asdict(report)


def canonical_orientation_map_conformance_report_bytes(
    report: OrientationMapConformanceReport,
) -> bytes:
    return _canonical_bytes(orientation_map_conformance_report_as_dict(report))


def orientation_map_conformance_report_from_dict(
    value: Mapping[str, object],
) -> OrientationMapConformanceReport:
    if not isinstance(value, Mapping):
        raise TypeError("Orientation Map Conformance Report must be a mapping")
    expected_fields = {
        "report_id",
        "schema_version",
        "orientation_map_id",
        "orientation_map_ref",
        "construction_id",
        "construction_ref",
        "navigation_certification_id",
        "navigation_certification_ref",
        "relation_set_id",
        "relation_set_ref",
        "structural_summary_ref",
        "structural_statistics_ref",
        "valid",
        "decision",
        "checks",
        "errors",
        "accepted_orientation_map_ref",
        "accepted_construction_ref",
        "inputs_unchanged",
        "responsibility",
        "stop",
    }
    if set(value) != expected_fields:
        raise ValueError(
            "Orientation Map Conformance fields do not match WP24"
        )
    return OrientationMapConformanceReport(**dict(value))


__all__: tuple[str, ...] = ()
