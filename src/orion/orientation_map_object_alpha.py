"""Immutable reference-only Orientation Map Object for Slice III WP22.

WP22 binds the exact certified Navigation and Relations lineage into one
deterministic object contract. It defines no nodes, edges, geometry, layout,
coordinates, routes, visualization, interpretation, or map behavior.
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
    canonical_constructed_navigation_bytes,
)
from orion.navigation_object_alpha import (
    NavigationObject,
    canonical_navigation_object_bytes,
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


ORIENTATION_MAP_SCHEMA_VERSION = "orion.orientation-map/0.1-alpha"
SERIALIZATION_VERSION = "canonical-json/1"
RESPONSIBILITY = "orientation_map_object_contract"
CONTRACT_STATE = "object_contract"
STOP_AFTER_ORIENTATION_MAP_OBJECT = "after_orientation_map_object"

_ORIENTATION_MAP_ID = re.compile(r"^orientation-map-[0-9a-f]{24}$")
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


def _identity_basis(
    *,
    navigation_certification_id: str,
    navigation_certification_ref: str,
    navigation_object_id: str,
    navigation_object_ref: str,
    navigation_construction_id: str,
    navigation_construction_ref: str,
    navigation_conformance_id: str,
    navigation_conformance_ref: str,
    relation_set_id: str,
    relation_set_ref: str,
    relations_certification_id: str,
    relations_certification_ref: str,
    summary_id: str,
    summary_ref: str,
    statistics_id: str,
    statistics_ref: str,
    provenance_ref: str,
    canonical_order: int,
) -> dict[str, object]:
    return {
        "orientation_map_schema_version": ORIENTATION_MAP_SCHEMA_VERSION,
        "navigation_certification_id": navigation_certification_id,
        "navigation_certification_ref": navigation_certification_ref,
        "navigation_object_id": navigation_object_id,
        "navigation_object_ref": navigation_object_ref,
        "navigation_construction_id": navigation_construction_id,
        "navigation_construction_ref": navigation_construction_ref,
        "navigation_conformance_id": navigation_conformance_id,
        "navigation_conformance_ref": navigation_conformance_ref,
        "relation_set_id": relation_set_id,
        "relation_set_ref": relation_set_ref,
        "relations_certification_id": relations_certification_id,
        "relations_certification_ref": relations_certification_ref,
        "summary_id": summary_id,
        "summary_ref": summary_ref,
        "statistics_id": statistics_id,
        "statistics_ref": statistics_ref,
        "provenance_ref": provenance_ref,
        "canonical_order": canonical_order,
        "serialization_version": SERIALIZATION_VERSION,
        "responsibility": RESPONSIBILITY,
        "contract_state": CONTRACT_STATE,
        "externally_conformant": False,
        "stop": STOP_AFTER_ORIENTATION_MAP_OBJECT,
    }


@dataclass(frozen=True, slots=True)
class OrientationMapObject:
    """One immutable Orientation Map contract with no map content."""

    orientation_map_id: str
    orientation_map_integrity: str
    orientation_map_schema_version: str
    navigation_certification_id: str
    navigation_certification_ref: str
    navigation_object_id: str
    navigation_object_ref: str
    navigation_construction_id: str
    navigation_construction_ref: str
    navigation_conformance_id: str
    navigation_conformance_ref: str
    relation_set_id: str
    relation_set_ref: str
    relations_certification_id: str
    relations_certification_ref: str
    summary_id: str
    summary_ref: str
    statistics_id: str
    statistics_ref: str
    provenance_ref: str
    canonical_order: int
    serialization_version: str
    responsibility: str
    contract_state: str
    externally_conformant: bool
    stop: str

    def __post_init__(self) -> None:
        if _ORIENTATION_MAP_ID.fullmatch(self.orientation_map_id) is None:
            raise ValueError("orientation_map_id is not canonical")
        if _SHA256_HEX.fullmatch(self.orientation_map_integrity) is None:
            raise ValueError("orientation_map_integrity must be SHA-256")
        if self.orientation_map_schema_version != ORIENTATION_MAP_SCHEMA_VERSION:
            raise ValueError("Orientation Map schema version changed")
        for field_name in (
            "navigation_certification_id",
            "navigation_object_id",
            "navigation_construction_id",
            "navigation_conformance_id",
            "relation_set_id",
            "relations_certification_id",
            "summary_id",
            "statistics_id",
        ):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value:
                raise ValueError(f"{field_name} must be exact non-empty text")
        for field_name in (
            "navigation_certification_ref",
            "navigation_object_ref",
            "navigation_construction_ref",
            "navigation_conformance_ref",
            "relation_set_ref",
            "relations_certification_ref",
            "summary_ref",
            "statistics_ref",
            "provenance_ref",
        ):
            value = getattr(self, field_name)
            if _SHA256_REF.fullmatch(value) is None:
                raise ValueError(f"{field_name} must be a SHA-256 reference")
        if self.provenance_ref != self.navigation_certification_ref:
            raise ValueError(
                "Orientation Map provenance must name Navigation Certification"
            )
        if type(self.canonical_order) is not int or self.canonical_order != 0:
            raise ValueError("atomic Orientation Map canonical order is zero")
        if self.serialization_version != SERIALIZATION_VERSION:
            raise ValueError("Orientation Map serialization version changed")
        if self.responsibility != RESPONSIBILITY:
            raise ValueError("Orientation Map Object responsibility changed")
        if self.contract_state != CONTRACT_STATE:
            raise ValueError("Orientation Map must remain an object contract")
        if (
            type(self.externally_conformant) is not bool
            or self.externally_conformant
        ):
            raise ValueError("WP22 cannot claim Map Conformance")
        if self.stop != STOP_AFTER_ORIENTATION_MAP_OBJECT:
            raise ValueError("WP22 STOP boundary changed")
        basis = _identity_basis(
            navigation_certification_id=self.navigation_certification_id,
            navigation_certification_ref=self.navigation_certification_ref,
            navigation_object_id=self.navigation_object_id,
            navigation_object_ref=self.navigation_object_ref,
            navigation_construction_id=self.navigation_construction_id,
            navigation_construction_ref=self.navigation_construction_ref,
            navigation_conformance_id=self.navigation_conformance_id,
            navigation_conformance_ref=self.navigation_conformance_ref,
            relation_set_id=self.relation_set_id,
            relation_set_ref=self.relation_set_ref,
            relations_certification_id=self.relations_certification_id,
            relations_certification_ref=self.relations_certification_ref,
            summary_id=self.summary_id,
            summary_ref=self.summary_ref,
            statistics_id=self.statistics_id,
            statistics_ref=self.statistics_ref,
            provenance_ref=self.provenance_ref,
            canonical_order=self.canonical_order,
        )
        digest = _digest(basis)
        if self.orientation_map_id != f"orientation-map-{digest[:24]}":
            raise ValueError("orientation_map_id differs from identity basis")
        if self.orientation_map_integrity != digest:
            raise ValueError(
                "orientation_map_integrity differs from identity basis"
            )


def create_orientation_map_object(
    navigation_certification: NavigationCertificationReport,
    navigation: NavigationObject,
    constructed_navigation: ConstructedNavigationObject,
    navigation_conformance: NavigationConformanceReport,
    relation_set: DeclaredReferenceRelationSet,
    relations_certification: RelationsCertificationReport,
    summary: StructuralSummaryDiagnostic,
    statistics: StructuralStatisticsDiagnostic,
) -> OrientationMapObject:
    """Bind exact certified references without constructing a map."""

    inputs = (
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
            raise TypeError(f"WP22 requires immutable {name}")
        value.__post_init__()

    navigation_certification_ref = _artifact_ref(
        canonical_navigation_certification_report_bytes(
            navigation_certification
        )
    )
    navigation_ref = _artifact_ref(
        canonical_navigation_object_bytes(navigation)
    )
    construction_ref = _artifact_ref(
        canonical_constructed_navigation_bytes(constructed_navigation)
    )
    conformance_ref = _artifact_ref(
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
    if (
        navigation_certification.navigation_id != navigation.navigation_id
        or navigation_certification.navigation_ref != navigation_ref
        or navigation_certification.construction_id
        != constructed_navigation.construction_id
        or navigation_certification.construction_ref != construction_ref
        or navigation_certification.conformance_report_id
        != navigation_conformance.report_id
        or navigation_certification.conformance_report_ref != conformance_ref
        or navigation_certification.relation_set_ref != relation_set_ref
        or navigation_certification.relations_certification_ref
        != relations_certification_ref
        or navigation_certification.structural_summary_ref != summary_ref
        or navigation_certification.structural_statistics_ref != statistics_ref
        or constructed_navigation.navigation_id != navigation.navigation_id
        or constructed_navigation.navigation_contract_ref != navigation_ref
        or navigation_conformance.accepted_construction_ref != construction_ref
        or relation_set.structural_summary_ref != summary_ref
        or relation_set.structural_statistics_ref != statistics_ref
    ):
        raise ValueError("WP22 inputs do not share certified lineage")

    basis = _identity_basis(
        navigation_certification_id=(
            navigation_certification.certification_id
        ),
        navigation_certification_ref=navigation_certification_ref,
        navigation_object_id=navigation.navigation_id,
        navigation_object_ref=navigation_ref,
        navigation_construction_id=constructed_navigation.construction_id,
        navigation_construction_ref=construction_ref,
        navigation_conformance_id=navigation_conformance.report_id,
        navigation_conformance_ref=conformance_ref,
        relation_set_id=relation_set.relation_set_id,
        relation_set_ref=relation_set_ref,
        relations_certification_id=relations_certification.certification_id,
        relations_certification_ref=relations_certification_ref,
        summary_id=summary.summary_id,
        summary_ref=summary_ref,
        statistics_id=statistics.statistics_id,
        statistics_ref=statistics_ref,
        provenance_ref=navigation_certification_ref,
        canonical_order=0,
    )
    digest = _digest(basis)
    return OrientationMapObject(
        orientation_map_id=f"orientation-map-{digest[:24]}",
        orientation_map_integrity=digest,
        orientation_map_schema_version=ORIENTATION_MAP_SCHEMA_VERSION,
        navigation_certification_id=(
            navigation_certification.certification_id
        ),
        navigation_certification_ref=navigation_certification_ref,
        navigation_object_id=navigation.navigation_id,
        navigation_object_ref=navigation_ref,
        navigation_construction_id=constructed_navigation.construction_id,
        navigation_construction_ref=construction_ref,
        navigation_conformance_id=navigation_conformance.report_id,
        navigation_conformance_ref=conformance_ref,
        relation_set_id=relation_set.relation_set_id,
        relation_set_ref=relation_set_ref,
        relations_certification_id=relations_certification.certification_id,
        relations_certification_ref=relations_certification_ref,
        summary_id=summary.summary_id,
        summary_ref=summary_ref,
        statistics_id=statistics.statistics_id,
        statistics_ref=statistics_ref,
        provenance_ref=navigation_certification_ref,
        canonical_order=0,
        serialization_version=SERIALIZATION_VERSION,
        responsibility=RESPONSIBILITY,
        contract_state=CONTRACT_STATE,
        externally_conformant=False,
        stop=STOP_AFTER_ORIENTATION_MAP_OBJECT,
    )


def orientation_map_object_as_dict(
    orientation_map: OrientationMapObject,
) -> dict[str, object]:
    orientation_map.__post_init__()
    return asdict(orientation_map)


def canonical_orientation_map_object_bytes(
    orientation_map: OrientationMapObject,
) -> bytes:
    return _canonical_bytes(orientation_map_object_as_dict(orientation_map))


def orientation_map_object_from_dict(
    value: Mapping[str, object],
) -> OrientationMapObject:
    if not isinstance(value, Mapping):
        raise TypeError("Orientation Map Object must be a mapping")
    expected_fields = {
        "orientation_map_id",
        "orientation_map_integrity",
        "orientation_map_schema_version",
        "navigation_certification_id",
        "navigation_certification_ref",
        "navigation_object_id",
        "navigation_object_ref",
        "navigation_construction_id",
        "navigation_construction_ref",
        "navigation_conformance_id",
        "navigation_conformance_ref",
        "relation_set_id",
        "relation_set_ref",
        "relations_certification_id",
        "relations_certification_ref",
        "summary_id",
        "summary_ref",
        "statistics_id",
        "statistics_ref",
        "provenance_ref",
        "canonical_order",
        "serialization_version",
        "responsibility",
        "contract_state",
        "externally_conformant",
        "stop",
    }
    if set(value) != expected_fields:
        raise ValueError("Orientation Map Object fields do not match WP22")
    return OrientationMapObject(**dict(value))


__all__: tuple[str, ...] = ()
