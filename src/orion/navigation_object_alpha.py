"""Immutable reference-only Navigation Object contract for Slice III WP18.

WP18 binds certified Relations and exact Slice II references into one
deterministic navigation context. It defines no catalog, address, transition,
traversal, route, graph, recommendation, or map behavior.
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
from orion.relations_certification_alpha import (
    PASSED,
    STOP_AT_RELATIONS_CERTIFIED,
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


NAVIGATION_SCHEMA_VERSION = "orion.navigation/0.1-alpha"
SERIALIZATION_VERSION = "canonical-json/1"
RESPONSIBILITY = "navigation_object_contract"
CONTRACT_STATE = "object_contract"
STOP_AFTER_NAVIGATION_OBJECT = "after_navigation_object"

_NAVIGATION_ID = re.compile(r"^navigation-[0-9a-f]{24}$")
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
        "navigation_schema_version": NAVIGATION_SCHEMA_VERSION,
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
        "stop": STOP_AFTER_NAVIGATION_OBJECT,
    }


@dataclass(frozen=True, slots=True)
class NavigationObject:
    """One immutable Navigation context with no navigation behavior."""

    navigation_id: str
    navigation_integrity: str
    navigation_schema_version: str
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
        if _NAVIGATION_ID.fullmatch(self.navigation_id) is None:
            raise ValueError("navigation_id is not canonical")
        if _SHA256_HEX.fullmatch(self.navigation_integrity) is None:
            raise ValueError("navigation_integrity must be SHA-256 hexadecimal")
        if self.navigation_schema_version != NAVIGATION_SCHEMA_VERSION:
            raise ValueError("Navigation schema version changed")
        for field_name in (
            "relation_set_id",
            "relations_certification_id",
            "summary_id",
            "statistics_id",
        ):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value:
                raise ValueError(f"{field_name} must be exact non-empty text")
        for field_name in (
            "relation_set_ref",
            "relations_certification_ref",
            "summary_ref",
            "statistics_ref",
            "provenance_ref",
        ):
            value = getattr(self, field_name)
            if _SHA256_REF.fullmatch(value) is None:
                raise ValueError(f"{field_name} must be a SHA-256 reference")
        if self.provenance_ref != self.relations_certification_ref:
            raise ValueError(
                "Navigation provenance must be the exact Gate R reference"
            )
        if type(self.canonical_order) is not int or self.canonical_order != 0:
            raise ValueError("the atomic Navigation Object canonical order is zero")
        if self.serialization_version != SERIALIZATION_VERSION:
            raise ValueError("Navigation serialization version changed")
        if self.responsibility != RESPONSIBILITY:
            raise ValueError("Navigation Object responsibility changed")
        if self.contract_state != CONTRACT_STATE:
            raise ValueError("Navigation Object must remain an object contract")
        if (
            type(self.externally_conformant) is not bool
            or self.externally_conformant
        ):
            raise ValueError("WP18 cannot claim External Navigation Conformance")
        if self.stop != STOP_AFTER_NAVIGATION_OBJECT:
            raise ValueError("WP18 STOP boundary changed")
        basis = _identity_basis(
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
        if self.navigation_id != f"navigation-{digest[:24]}":
            raise ValueError("navigation_id differs from canonical identity basis")
        if self.navigation_integrity != digest:
            raise ValueError(
                "navigation_integrity differs from canonical identity basis"
            )


def create_navigation_object(
    relation_set: DeclaredReferenceRelationSet,
    relations_certification: RelationsCertificationReport,
    summary: StructuralSummaryDiagnostic,
    statistics: StructuralStatisticsDiagnostic,
) -> NavigationObject:
    """Bind exact certified references without constructing Navigation."""

    if not isinstance(relation_set, DeclaredReferenceRelationSet):
        raise TypeError("Navigation Object requires an immutable Relation Set")
    if not isinstance(relations_certification, RelationsCertificationReport):
        raise TypeError(
            "Navigation Object requires Relations Certification Report"
        )
    if not isinstance(summary, StructuralSummaryDiagnostic):
        raise TypeError("Navigation Object requires Structural Summary")
    if not isinstance(statistics, StructuralStatisticsDiagnostic):
        raise TypeError("Navigation Object requires Structural Statistics")
    relation_set.__post_init__()
    relations_certification.__post_init__()
    summary.__post_init__()
    statistics.__post_init__()

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
        not relations_certification.certified
        or relations_certification.status != PASSED
        or relations_certification.errors
        or relations_certification.stop != STOP_AT_RELATIONS_CERTIFIED
    ):
        raise ValueError("Relations Certification Gate has not passed")
    if (
        relations_certification.relation_set_id != relation_set.relation_set_id
        or relations_certification.relation_set_ref != relation_set_ref
        or relations_certification.structural_summary_ref != summary_ref
        or relations_certification.structural_statistics_ref != statistics_ref
        or relation_set.structural_summary_ref != summary_ref
        or relation_set.structural_statistics_ref != statistics_ref
        or relation_set.input_inventory_ref
        != summary.input_inventory_ref
        or summary.input_inventory_ref != statistics.input_inventory_ref
    ):
        raise ValueError("Navigation inputs do not share certified lineage")

    basis = _identity_basis(
        relation_set_id=relation_set.relation_set_id,
        relation_set_ref=relation_set_ref,
        relations_certification_id=(
            relations_certification.certification_id
        ),
        relations_certification_ref=relations_certification_ref,
        summary_id=summary.summary_id,
        summary_ref=summary_ref,
        statistics_id=statistics.statistics_id,
        statistics_ref=statistics_ref,
        provenance_ref=relations_certification_ref,
        canonical_order=0,
    )
    digest = _digest(basis)
    return NavigationObject(
        navigation_id=f"navigation-{digest[:24]}",
        navigation_integrity=digest,
        navigation_schema_version=NAVIGATION_SCHEMA_VERSION,
        relation_set_id=relation_set.relation_set_id,
        relation_set_ref=relation_set_ref,
        relations_certification_id=(
            relations_certification.certification_id
        ),
        relations_certification_ref=relations_certification_ref,
        summary_id=summary.summary_id,
        summary_ref=summary_ref,
        statistics_id=statistics.statistics_id,
        statistics_ref=statistics_ref,
        provenance_ref=relations_certification_ref,
        canonical_order=0,
        serialization_version=SERIALIZATION_VERSION,
        responsibility=RESPONSIBILITY,
        contract_state=CONTRACT_STATE,
        externally_conformant=False,
        stop=STOP_AFTER_NAVIGATION_OBJECT,
    )


def navigation_object_as_dict(
    navigation: NavigationObject,
) -> dict[str, object]:
    navigation.__post_init__()
    return asdict(navigation)


def canonical_navigation_object_bytes(navigation: NavigationObject) -> bytes:
    return _canonical_bytes(navigation_object_as_dict(navigation))


def navigation_object_from_dict(value: Mapping[str, object]) -> NavigationObject:
    if not isinstance(value, Mapping):
        raise TypeError("Navigation Object must be a mapping")
    expected_fields = {
        "navigation_id",
        "navigation_integrity",
        "navigation_schema_version",
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
        raise ValueError("Navigation Object fields do not match WP18")
    return NavigationObject(**dict(value))


__all__: tuple[str, ...] = ()
