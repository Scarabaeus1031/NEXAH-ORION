"""Deterministic structural Orientation Map Construction for Slice III WP23.

WP23 materializes one Orientation Map Entry per certified Navigation Entry. It
does not validate, certify, lay out, position, render, visualize, traverse, or
interpret an Orientation Map.
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
    ConstructedNavigationObject,
    NavigationEntry,
    canonical_constructed_navigation_bytes,
)
from orion.navigation_object_alpha import (
    NavigationObject,
    canonical_navigation_object_bytes,
)
from orion.orientation_map_object_alpha import (
    STOP_AFTER_ORIENTATION_MAP_OBJECT,
    OrientationMapObject,
    canonical_orientation_map_object_bytes,
)
from orion.relations_certification_alpha import (
    RelationsCertificationReport,
    canonical_relations_certification_report_bytes,
)
from orion.understand_structural_statistics_alpha import (
    StructuralStatisticsDiagnostic,
    canonical_structural_statistics_bytes,
)
from orion.understand_structural_summary_alpha import (
    StructuralSummaryDiagnostic,
    canonical_structural_summary_bytes,
)


ORIENTATION_MAP_ENTRY_SCHEMA_VERSION = (
    "orion.orientation-map-entry/0.1-alpha"
)
ORIENTATION_MAP_CONSTRUCTION_SCHEMA_VERSION = (
    "orion.orientation-map-construction/0.1-alpha"
)
SERIALIZATION_VERSION = "canonical-json/1"
RESPONSIBILITY = "orientation_map_construction"
CONSTRUCTION_STATE = "constructed_unvalidated"
STOP_AFTER_ORIENTATION_MAP_CONSTRUCTION = (
    "after_orientation_map_construction"
)

_ENTRY_ID = re.compile(r"^orientation-map-entry-[0-9a-f]{24}$")
_CONSTRUCTION_ID = re.compile(
    r"^orientation-map-construction-[0-9a-f]{24}$"
)
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


def _require_sha256_ref(value: str, field_name: str) -> None:
    if not isinstance(value, str) or _SHA256_REF.fullmatch(value) is None:
        raise ValueError(f"{field_name} must be a SHA-256 reference")


def _navigation_entry_bytes(entry: NavigationEntry) -> bytes:
    entry.__post_init__()
    return _canonical_bytes(asdict(entry))


def _entry_basis(
    *,
    canonical_order: int,
    navigation_entry_id: str,
    navigation_entry_ref: str,
    relation_id: str,
    relation_ref: str,
    relation_kind: str,
    source_element_id: str,
    target_element_id: str,
    structural_adjacency_ref: str | None,
    provenance_ref: str,
) -> dict[str, object]:
    return {
        "entry_schema_version": ORIENTATION_MAP_ENTRY_SCHEMA_VERSION,
        "canonical_order": canonical_order,
        "navigation_entry_id": navigation_entry_id,
        "navigation_entry_ref": navigation_entry_ref,
        "relation_id": relation_id,
        "relation_ref": relation_ref,
        "relation_kind": relation_kind,
        "source_element_id": source_element_id,
        "target_element_id": target_element_id,
        "structural_adjacency_ref": structural_adjacency_ref,
        "provenance_ref": provenance_ref,
    }


@dataclass(frozen=True, slots=True)
class OrientationMapEntry:
    """One immutable reference to one certified Navigation Entry."""

    entry_id: str
    entry_schema_version: str
    canonical_order: int
    navigation_entry_id: str
    navigation_entry_ref: str
    relation_id: str
    relation_ref: str
    relation_kind: str
    source_element_id: str
    target_element_id: str
    structural_adjacency_ref: str | None
    provenance_ref: str

    def __post_init__(self) -> None:
        if _ENTRY_ID.fullmatch(self.entry_id) is None:
            raise ValueError("Orientation Map entry_id is not canonical")
        if self.entry_schema_version != ORIENTATION_MAP_ENTRY_SCHEMA_VERSION:
            raise ValueError("Orientation Map Entry schema changed")
        if type(self.canonical_order) is not int or self.canonical_order < 0:
            raise ValueError("canonical_order must be non-negative")
        for field_name in (
            "navigation_entry_id",
            "relation_id",
            "relation_kind",
            "source_element_id",
            "target_element_id",
        ):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value:
                raise ValueError(f"{field_name} must be exact non-empty text")
        for field_name in (
            "navigation_entry_ref",
            "relation_ref",
            "provenance_ref",
        ):
            _require_sha256_ref(getattr(self, field_name), field_name)
        if self.structural_adjacency_ref is not None:
            _require_sha256_ref(
                self.structural_adjacency_ref,
                "structural_adjacency_ref",
            )
            if self.structural_adjacency_ref != self.relation_ref:
                raise ValueError(
                    "Map adjacency must preserve the exact Relation reference"
                )
        basis = _entry_basis(
            canonical_order=self.canonical_order,
            navigation_entry_id=self.navigation_entry_id,
            navigation_entry_ref=self.navigation_entry_ref,
            relation_id=self.relation_id,
            relation_ref=self.relation_ref,
            relation_kind=self.relation_kind,
            source_element_id=self.source_element_id,
            target_element_id=self.target_element_id,
            structural_adjacency_ref=self.structural_adjacency_ref,
            provenance_ref=self.provenance_ref,
        )
        if self.entry_id != (
            f"orientation-map-entry-{_digest(basis)[:24]}"
        ):
            raise ValueError("Orientation Map entry_id differs from basis")


def _entry_from_navigation(entry: NavigationEntry) -> OrientationMapEntry:
    entry.__post_init__()
    basis = _entry_basis(
        canonical_order=entry.canonical_order,
        navigation_entry_id=entry.entry_id,
        navigation_entry_ref=_artifact_ref(_navigation_entry_bytes(entry)),
        relation_id=entry.relation_id,
        relation_ref=entry.relation_ref,
        relation_kind=entry.relation_kind,
        source_element_id=entry.source_element_id,
        target_element_id=entry.target_element_id,
        structural_adjacency_ref=entry.structural_adjacency_ref,
        provenance_ref=entry.provenance_ref,
    )
    return OrientationMapEntry(
        entry_id=f"orientation-map-entry-{_digest(basis)[:24]}",
        **basis,
    )


def _construction_basis(
    *,
    orientation_map_id: str,
    orientation_map_contract_ref: str,
    navigation_certification_id: str,
    navigation_certification_ref: str,
    navigation_construction_id: str,
    navigation_construction_ref: str,
    entries: tuple[OrientationMapEntry, ...],
    provenance_ref: str,
) -> dict[str, object]:
    return {
        "schema_version": ORIENTATION_MAP_CONSTRUCTION_SCHEMA_VERSION,
        "orientation_map_id": orientation_map_id,
        "orientation_map_contract_ref": orientation_map_contract_ref,
        "navigation_certification_id": navigation_certification_id,
        "navigation_certification_ref": navigation_certification_ref,
        "navigation_construction_id": navigation_construction_id,
        "navigation_construction_ref": navigation_construction_ref,
        "entry_count": len(entries),
        "entries": tuple(asdict(entry) for entry in entries),
        "provenance_ref": provenance_ref,
        "serialization_version": SERIALIZATION_VERSION,
        "responsibility": RESPONSIBILITY,
        "construction_state": CONSTRUCTION_STATE,
        "externally_conformant": False,
        "stop": STOP_AFTER_ORIENTATION_MAP_CONSTRUCTION,
    }


@dataclass(frozen=True, slots=True)
class ConstructedOrientationMap:
    """Immutable structural Orientation Map with no graphical content."""

    construction_id: str
    construction_integrity: str
    schema_version: str
    orientation_map_id: str
    orientation_map_contract_ref: str
    navigation_certification_id: str
    navigation_certification_ref: str
    navigation_construction_id: str
    navigation_construction_ref: str
    entry_count: int
    entries: tuple[OrientationMapEntry, ...]
    provenance_ref: str
    serialization_version: str
    responsibility: str
    construction_state: str
    externally_conformant: bool
    stop: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "entries", tuple(self.entries))
        if _CONSTRUCTION_ID.fullmatch(self.construction_id) is None:
            raise ValueError("Map construction_id is not canonical")
        if _SHA256_HEX.fullmatch(self.construction_integrity) is None:
            raise ValueError("Map construction_integrity must be SHA-256")
        if self.schema_version != ORIENTATION_MAP_CONSTRUCTION_SCHEMA_VERSION:
            raise ValueError("Orientation Map Construction schema changed")
        for field_name in (
            "orientation_map_id",
            "navigation_certification_id",
            "navigation_construction_id",
        ):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value:
                raise ValueError(f"{field_name} must be exact non-empty text")
        for field_name in (
            "orientation_map_contract_ref",
            "navigation_certification_ref",
            "navigation_construction_ref",
            "provenance_ref",
        ):
            _require_sha256_ref(getattr(self, field_name), field_name)
        if self.provenance_ref != self.navigation_certification_ref:
            raise ValueError("Map provenance must name Navigation Certification")
        if type(self.entry_count) is not int or self.entry_count < 0:
            raise ValueError("entry_count must be non-negative")
        if self.entry_count != len(self.entries):
            raise ValueError("entry_count differs from entries")
        if any(
            not isinstance(entry, OrientationMapEntry)
            for entry in self.entries
        ):
            raise TypeError("entries must be immutable Orientation Map Entries")
        for entry in self.entries:
            entry.__post_init__()
        if tuple(entry.canonical_order for entry in self.entries) != tuple(
            range(self.entry_count)
        ):
            raise ValueError("Orientation Map Entries are not canonical")
        map_ids = tuple(entry.entry_id for entry in self.entries)
        navigation_ids = tuple(
            entry.navigation_entry_id for entry in self.entries
        )
        navigation_refs = tuple(
            entry.navigation_entry_ref for entry in self.entries
        )
        if len(set(map_ids)) != len(map_ids):
            raise ValueError("Orientation Map Entries contain duplicate IDs")
        if len(set(navigation_ids)) != len(navigation_ids):
            raise ValueError("Navigation Entry identities are duplicated")
        if len(set(navigation_refs)) != len(navigation_refs):
            raise ValueError("Navigation Entry references are duplicated")
        if self.serialization_version != SERIALIZATION_VERSION:
            raise ValueError("Map Construction serialization changed")
        if self.responsibility != RESPONSIBILITY:
            raise ValueError("Map Construction responsibility changed")
        if self.construction_state != CONSTRUCTION_STATE:
            raise ValueError("WP23 output must remain unvalidated")
        if (
            type(self.externally_conformant) is not bool
            or self.externally_conformant
        ):
            raise ValueError("WP23 cannot claim Map Conformance")
        if self.stop != STOP_AFTER_ORIENTATION_MAP_CONSTRUCTION:
            raise ValueError("WP23 STOP boundary changed")
        basis = _construction_basis(
            orientation_map_id=self.orientation_map_id,
            orientation_map_contract_ref=self.orientation_map_contract_ref,
            navigation_certification_id=self.navigation_certification_id,
            navigation_certification_ref=self.navigation_certification_ref,
            navigation_construction_id=self.navigation_construction_id,
            navigation_construction_ref=self.navigation_construction_ref,
            entries=self.entries,
            provenance_ref=self.provenance_ref,
        )
        digest = _digest(basis)
        if self.construction_id != (
            f"orientation-map-construction-{digest[:24]}"
        ):
            raise ValueError("Map construction_id differs from basis")
        if self.construction_integrity != digest:
            raise ValueError("Map construction_integrity differs from basis")


def construct_orientation_map(
    orientation_map: OrientationMapObject,
    navigation_certification: NavigationCertificationReport,
    navigation: NavigationObject,
    constructed_navigation: ConstructedNavigationObject,
    navigation_conformance: NavigationConformanceReport,
    relation_set: DeclaredReferenceRelationSet,
    relations_certification: RelationsCertificationReport,
    summary: StructuralSummaryDiagnostic,
    statistics: StructuralStatisticsDiagnostic,
) -> ConstructedOrientationMap:
    """Materialize exact Navigation Entry references and stop."""

    inputs = (
        (orientation_map, OrientationMapObject, "Orientation Map Object"),
        (
            navigation_certification,
            NavigationCertificationReport,
            "Navigation Certification",
        ),
        (navigation, NavigationObject, "Navigation Object"),
        (
            constructed_navigation,
            ConstructedNavigationObject,
            "Navigation Construction",
        ),
        (
            navigation_conformance,
            NavigationConformanceReport,
            "Navigation Conformance",
        ),
        (relation_set, DeclaredReferenceRelationSet, "Relation Set"),
        (
            relations_certification,
            RelationsCertificationReport,
            "Relations Certification",
        ),
        (summary, StructuralSummaryDiagnostic, "Structural Summary"),
        (statistics, StructuralStatisticsDiagnostic, "Structural Statistics"),
    )
    for value, expected, name in inputs:
        if not isinstance(value, expected):
            raise TypeError(f"WP23 requires immutable {name}")
        value.__post_init__()

    orientation_map_ref = _artifact_ref(
        canonical_orientation_map_object_bytes(orientation_map)
    )
    navigation_certification_ref = _artifact_ref(
        canonical_navigation_certification_report_bytes(
            navigation_certification
        )
    )
    navigation_ref = _artifact_ref(
        canonical_navigation_object_bytes(navigation)
    )
    navigation_construction_ref = _artifact_ref(
        canonical_constructed_navigation_bytes(constructed_navigation)
    )
    navigation_conformance_ref = _artifact_ref(
        canonical_navigation_conformance_report_bytes(
            navigation_conformance
        )
    )
    relation_set_ref = _artifact_ref(
        canonical_declared_reference_relation_set_bytes(relation_set)
    )
    relations_certification_ref = _artifact_ref(
        canonical_relations_certification_report_bytes(
            relations_certification
        )
    )
    summary_ref = _artifact_ref(canonical_structural_summary_bytes(summary))
    statistics_ref = _artifact_ref(
        canonical_structural_statistics_bytes(statistics)
    )
    if (
        not navigation_certification.certified
        or navigation_certification.status != PASSED
        or navigation_certification.errors
        or navigation_certification.stop != STOP_AT_NAVIGATION_CERTIFIED
    ):
        raise ValueError("Navigation Certification Gate has not passed")
    if orientation_map.stop != STOP_AFTER_ORIENTATION_MAP_OBJECT:
        raise ValueError("WP22 contract did not stop at its frozen boundary")
    if (
        orientation_map.navigation_certification_id
        != navigation_certification.certification_id
        or orientation_map.navigation_certification_ref
        != navigation_certification_ref
        or orientation_map.navigation_object_id != navigation.navigation_id
        or orientation_map.navigation_object_ref != navigation_ref
        or orientation_map.navigation_construction_id
        != constructed_navigation.construction_id
        or orientation_map.navigation_construction_ref
        != navigation_construction_ref
        or orientation_map.navigation_conformance_id
        != navigation_conformance.report_id
        or orientation_map.navigation_conformance_ref
        != navigation_conformance_ref
        or orientation_map.relation_set_id != relation_set.relation_set_id
        or orientation_map.relation_set_ref != relation_set_ref
        or orientation_map.relations_certification_id
        != relations_certification.certification_id
        or orientation_map.relations_certification_ref
        != relations_certification_ref
        or orientation_map.summary_id != summary.summary_id
        or orientation_map.summary_ref != summary_ref
        or orientation_map.statistics_id != statistics.statistics_id
        or orientation_map.statistics_ref != statistics_ref
        or orientation_map.provenance_ref != navigation_certification_ref
        or navigation_certification.navigation_id != navigation.navigation_id
        or navigation_certification.navigation_ref != navigation_ref
        or navigation_certification.construction_id
        != constructed_navigation.construction_id
        or navigation_certification.construction_ref
        != navigation_construction_ref
        or navigation_certification.conformance_report_id
        != navigation_conformance.report_id
        or navigation_certification.conformance_report_ref
        != navigation_conformance_ref
    ):
        raise ValueError("WP23 inputs do not share certified lineage")

    entries = tuple(
        _entry_from_navigation(entry)
        for entry in constructed_navigation.entries
    )
    basis = _construction_basis(
        orientation_map_id=orientation_map.orientation_map_id,
        orientation_map_contract_ref=orientation_map_ref,
        navigation_certification_id=(
            navigation_certification.certification_id
        ),
        navigation_certification_ref=navigation_certification_ref,
        navigation_construction_id=constructed_navigation.construction_id,
        navigation_construction_ref=navigation_construction_ref,
        entries=entries,
        provenance_ref=navigation_certification_ref,
    )
    digest = _digest(basis)
    return ConstructedOrientationMap(
        construction_id=f"orientation-map-construction-{digest[:24]}",
        construction_integrity=digest,
        schema_version=ORIENTATION_MAP_CONSTRUCTION_SCHEMA_VERSION,
        orientation_map_id=orientation_map.orientation_map_id,
        orientation_map_contract_ref=orientation_map_ref,
        navigation_certification_id=(
            navigation_certification.certification_id
        ),
        navigation_certification_ref=navigation_certification_ref,
        navigation_construction_id=constructed_navigation.construction_id,
        navigation_construction_ref=navigation_construction_ref,
        entry_count=len(entries),
        entries=entries,
        provenance_ref=navigation_certification_ref,
        serialization_version=SERIALIZATION_VERSION,
        responsibility=RESPONSIBILITY,
        construction_state=CONSTRUCTION_STATE,
        externally_conformant=False,
        stop=STOP_AFTER_ORIENTATION_MAP_CONSTRUCTION,
    )


def orientation_map_entry_from_dict(
    value: Mapping[str, object],
) -> OrientationMapEntry:
    if not isinstance(value, Mapping):
        raise TypeError("Orientation Map Entry must be a mapping")
    expected_fields = {
        "entry_id",
        "entry_schema_version",
        "canonical_order",
        "navigation_entry_id",
        "navigation_entry_ref",
        "relation_id",
        "relation_ref",
        "relation_kind",
        "source_element_id",
        "target_element_id",
        "structural_adjacency_ref",
        "provenance_ref",
    }
    if set(value) != expected_fields:
        raise ValueError("Orientation Map Entry fields do not match WP23")
    return OrientationMapEntry(**dict(value))


def constructed_orientation_map_as_dict(
    orientation_map: ConstructedOrientationMap,
) -> dict[str, object]:
    orientation_map.__post_init__()
    return asdict(orientation_map)


def canonical_constructed_orientation_map_bytes(
    orientation_map: ConstructedOrientationMap,
) -> bytes:
    return _canonical_bytes(
        constructed_orientation_map_as_dict(orientation_map)
    )


def constructed_orientation_map_from_dict(
    value: Mapping[str, object],
) -> ConstructedOrientationMap:
    if not isinstance(value, Mapping):
        raise TypeError("Constructed Orientation Map must be a mapping")
    expected_fields = {
        "construction_id",
        "construction_integrity",
        "schema_version",
        "orientation_map_id",
        "orientation_map_contract_ref",
        "navigation_certification_id",
        "navigation_certification_ref",
        "navigation_construction_id",
        "navigation_construction_ref",
        "entry_count",
        "entries",
        "provenance_ref",
        "serialization_version",
        "responsibility",
        "construction_state",
        "externally_conformant",
        "stop",
    }
    if set(value) != expected_fields:
        raise ValueError("Constructed Orientation Map fields do not match WP23")
    entries_value = value["entries"]
    if not isinstance(entries_value, (tuple, list)):
        raise TypeError("entries must be an ordered collection")
    entries = tuple(
        orientation_map_entry_from_dict(entry) for entry in entries_value
    )
    return ConstructedOrientationMap(
        **{key: item for key, item in value.items() if key != "entries"},
        entries=entries,
    )


__all__: tuple[str, ...] = ()
