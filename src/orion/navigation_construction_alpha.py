"""Deterministic, behavior-free Navigation Construction for Slice III WP19.

WP19 materializes ordered references to certified Relations. It does not
validate Navigation, execute traversal, resolve routes, search a graph, or
construct an Orientation Map.
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
from orion.navigation_object_alpha import (
    STOP_AFTER_NAVIGATION_OBJECT,
    NavigationObject,
    canonical_navigation_object_bytes,
)
from orion.relations_certification_alpha import (
    PASSED,
    STOP_AT_RELATIONS_CERTIFIED,
    RelationsCertificationReport,
    canonical_relations_certification_report_bytes,
)
from orion.structural_relation_alpha import (
    RelationObject,
    canonical_relation_object_bytes,
)
from orion.understand_structural_statistics_alpha import (
    StructuralStatisticsDiagnostic,
    canonical_structural_statistics_bytes,
)
from orion.understand_structural_summary_alpha import (
    StructuralSummaryDiagnostic,
    canonical_structural_summary_bytes,
)


NAVIGATION_ENTRY_SCHEMA_VERSION = "orion.navigation-entry/0.1-alpha"
NAVIGATION_CONSTRUCTION_SCHEMA_VERSION = (
    "orion.navigation-construction/0.1-alpha"
)
SERIALIZATION_VERSION = "canonical-json/1"
RESPONSIBILITY = "navigation_construction"
CONSTRUCTION_STATE = "constructed_unvalidated"
STOP_AFTER_NAVIGATION_CONSTRUCTION = "after_navigation_construction"
ADJACENCY_RELATION_KINDS = (
    "immediately_precedes",
    "immediately_follows",
)

_ENTRY_ID = re.compile(r"^navigation-entry-[0-9a-f]{24}$")
_CONSTRUCTION_ID = re.compile(r"^navigation-construction-[0-9a-f]{24}$")
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


def _entry_basis(
    *,
    canonical_order: int,
    relation_id: str,
    relation_ref: str,
    relation_kind: str,
    source_element_id: str,
    target_element_id: str,
    structural_adjacency_ref: str | None,
    provenance_ref: str,
) -> dict[str, object]:
    return {
        "entry_schema_version": NAVIGATION_ENTRY_SCHEMA_VERSION,
        "canonical_order": canonical_order,
        "relation_id": relation_id,
        "relation_ref": relation_ref,
        "relation_kind": relation_kind,
        "source_element_id": source_element_id,
        "target_element_id": target_element_id,
        "structural_adjacency_ref": structural_adjacency_ref,
        "provenance_ref": provenance_ref,
    }


@dataclass(frozen=True, slots=True)
class NavigationEntry:
    """One ordered reference to one immutable certified Relation."""

    entry_id: str
    entry_schema_version: str
    canonical_order: int
    relation_id: str
    relation_ref: str
    relation_kind: str
    source_element_id: str
    target_element_id: str
    structural_adjacency_ref: str | None
    provenance_ref: str

    def __post_init__(self) -> None:
        if _ENTRY_ID.fullmatch(self.entry_id) is None:
            raise ValueError("entry_id is not canonical")
        if self.entry_schema_version != NAVIGATION_ENTRY_SCHEMA_VERSION:
            raise ValueError("Navigation Entry schema version changed")
        if type(self.canonical_order) is not int or self.canonical_order < 0:
            raise ValueError("canonical_order must be non-negative")
        for field_name in (
            "relation_id",
            "relation_kind",
            "source_element_id",
            "target_element_id",
        ):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value:
                raise ValueError(f"{field_name} must be exact non-empty text")
        _require_sha256_ref(self.relation_ref, "relation_ref")
        _require_sha256_ref(self.provenance_ref, "provenance_ref")
        if self.relation_kind in ADJACENCY_RELATION_KINDS:
            if self.structural_adjacency_ref != self.relation_ref:
                raise ValueError(
                    "adjacency entry must cite its exact Relation reference"
                )
        elif self.structural_adjacency_ref is not None:
            raise ValueError(
                "non-adjacency entry cannot claim structural adjacency"
            )
        basis = _entry_basis(
            canonical_order=self.canonical_order,
            relation_id=self.relation_id,
            relation_ref=self.relation_ref,
            relation_kind=self.relation_kind,
            source_element_id=self.source_element_id,
            target_element_id=self.target_element_id,
            structural_adjacency_ref=self.structural_adjacency_ref,
            provenance_ref=self.provenance_ref,
        )
        if self.entry_id != f"navigation-entry-{_digest(basis)[:24]}":
            raise ValueError("entry_id differs from its canonical basis")


def _entry_from_relation(relation: RelationObject) -> NavigationEntry:
    relation.__post_init__()
    relation_ref = _artifact_ref(canonical_relation_object_bytes(relation))
    adjacency_ref = (
        relation_ref
        if relation.relation_kind in ADJACENCY_RELATION_KINDS
        else None
    )
    basis = _entry_basis(
        canonical_order=relation.canonical_order,
        relation_id=relation.relation_id,
        relation_ref=relation_ref,
        relation_kind=relation.relation_kind,
        source_element_id=relation.source_element_id,
        target_element_id=relation.target_element_id,
        structural_adjacency_ref=adjacency_ref,
        provenance_ref=relation.provenance.input_inventory_ref,
    )
    return NavigationEntry(
        entry_id=f"navigation-entry-{_digest(basis)[:24]}",
        **basis,
    )


def _construction_basis(
    *,
    navigation_id: str,
    navigation_contract_ref: str,
    relation_set_id: str,
    relation_set_ref: str,
    relations_certification_id: str,
    relations_certification_ref: str,
    summary_ref: str,
    statistics_ref: str,
    entries: tuple[NavigationEntry, ...],
    provenance_ref: str,
) -> dict[str, object]:
    return {
        "schema_version": NAVIGATION_CONSTRUCTION_SCHEMA_VERSION,
        "navigation_id": navigation_id,
        "navigation_contract_ref": navigation_contract_ref,
        "relation_set_id": relation_set_id,
        "relation_set_ref": relation_set_ref,
        "relations_certification_id": relations_certification_id,
        "relations_certification_ref": relations_certification_ref,
        "summary_ref": summary_ref,
        "statistics_ref": statistics_ref,
        "entry_count": len(entries),
        "entries": tuple(asdict(entry) for entry in entries),
        "provenance_ref": provenance_ref,
        "serialization_version": SERIALIZATION_VERSION,
        "responsibility": RESPONSIBILITY,
        "construction_state": CONSTRUCTION_STATE,
        "externally_conformant": False,
        "stop": STOP_AFTER_NAVIGATION_CONSTRUCTION,
    }


@dataclass(frozen=True, slots=True)
class ConstructedNavigationObject:
    """Immutable ordered Navigation metadata with no Navigation behavior."""

    construction_id: str
    construction_integrity: str
    schema_version: str
    navigation_id: str
    navigation_contract_ref: str
    relation_set_id: str
    relation_set_ref: str
    relations_certification_id: str
    relations_certification_ref: str
    summary_ref: str
    statistics_ref: str
    entry_count: int
    entries: tuple[NavigationEntry, ...]
    provenance_ref: str
    serialization_version: str
    responsibility: str
    construction_state: str
    externally_conformant: bool
    stop: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "entries", tuple(self.entries))
        if _CONSTRUCTION_ID.fullmatch(self.construction_id) is None:
            raise ValueError("construction_id is not canonical")
        if _SHA256_HEX.fullmatch(self.construction_integrity) is None:
            raise ValueError("construction_integrity must be SHA-256")
        if self.schema_version != NAVIGATION_CONSTRUCTION_SCHEMA_VERSION:
            raise ValueError("Navigation Construction schema changed")
        for field_name in (
            "navigation_id",
            "relation_set_id",
            "relations_certification_id",
        ):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value:
                raise ValueError(f"{field_name} must be exact non-empty text")
        for field_name in (
            "navigation_contract_ref",
            "relation_set_ref",
            "relations_certification_ref",
            "summary_ref",
            "statistics_ref",
            "provenance_ref",
        ):
            _require_sha256_ref(getattr(self, field_name), field_name)
        if self.provenance_ref != self.relations_certification_ref:
            raise ValueError("Construction provenance must name Gate R")
        if type(self.entry_count) is not int or self.entry_count < 0:
            raise ValueError("entry_count must be non-negative")
        if self.entry_count != len(self.entries):
            raise ValueError("entry_count differs from entries")
        if any(not isinstance(entry, NavigationEntry) for entry in self.entries):
            raise TypeError("entries must be immutable Navigation Entries")
        for entry in self.entries:
            entry.__post_init__()
        if tuple(entry.canonical_order for entry in self.entries) != tuple(
            range(self.entry_count)
        ):
            raise ValueError("Navigation Entries are not canonically ordered")
        relation_ids = tuple(entry.relation_id for entry in self.entries)
        relation_refs = tuple(entry.relation_ref for entry in self.entries)
        if len(set(relation_ids)) != len(relation_ids):
            raise ValueError("Navigation Entries duplicate a Relation identity")
        if len(set(relation_refs)) != len(relation_refs):
            raise ValueError("Navigation Entries duplicate a Relation reference")
        if self.serialization_version != SERIALIZATION_VERSION:
            raise ValueError("Navigation Construction serialization changed")
        if self.responsibility != RESPONSIBILITY:
            raise ValueError("Navigation Construction responsibility changed")
        if self.construction_state != CONSTRUCTION_STATE:
            raise ValueError("WP19 output must remain unvalidated")
        if (
            type(self.externally_conformant) is not bool
            or self.externally_conformant
        ):
            raise ValueError("WP19 cannot claim Navigation Conformance")
        if self.stop != STOP_AFTER_NAVIGATION_CONSTRUCTION:
            raise ValueError("WP19 STOP boundary changed")
        basis = _construction_basis(
            navigation_id=self.navigation_id,
            navigation_contract_ref=self.navigation_contract_ref,
            relation_set_id=self.relation_set_id,
            relation_set_ref=self.relation_set_ref,
            relations_certification_id=self.relations_certification_id,
            relations_certification_ref=self.relations_certification_ref,
            summary_ref=self.summary_ref,
            statistics_ref=self.statistics_ref,
            entries=self.entries,
            provenance_ref=self.provenance_ref,
        )
        digest = _digest(basis)
        if self.construction_id != (
            f"navigation-construction-{digest[:24]}"
        ):
            raise ValueError("construction_id differs from canonical basis")
        if self.construction_integrity != digest:
            raise ValueError(
                "construction_integrity differs from canonical basis"
            )


def construct_navigation(
    navigation: NavigationObject,
    relation_set: DeclaredReferenceRelationSet,
    relations_certification: RelationsCertificationReport,
    summary: StructuralSummaryDiagnostic,
    statistics: StructuralStatisticsDiagnostic,
) -> ConstructedNavigationObject:
    """Materialize exact ordered Relation references and stop."""

    if not isinstance(navigation, NavigationObject):
        raise TypeError("WP19 requires the immutable WP18 Navigation Object")
    if not isinstance(relation_set, DeclaredReferenceRelationSet):
        raise TypeError("WP19 requires the immutable certified Relation Set")
    if not isinstance(
        relations_certification,
        RelationsCertificationReport,
    ):
        raise TypeError("WP19 requires immutable Relations Certification")
    if not isinstance(summary, StructuralSummaryDiagnostic):
        raise TypeError("WP19 requires immutable Structural Summary")
    if not isinstance(statistics, StructuralStatisticsDiagnostic):
        raise TypeError("WP19 requires immutable Structural Statistics")
    navigation.__post_init__()
    relation_set.__post_init__()
    relations_certification.__post_init__()
    summary.__post_init__()
    statistics.__post_init__()

    navigation_ref = _artifact_ref(canonical_navigation_object_bytes(navigation))
    relation_set_ref = _artifact_ref(
        canonical_declared_reference_relation_set_bytes(relation_set)
    )
    certification_ref = _artifact_ref(
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
    if navigation.stop != STOP_AFTER_NAVIGATION_OBJECT:
        raise ValueError("WP18 contract did not stop at its frozen boundary")
    if (
        navigation.relation_set_id != relation_set.relation_set_id
        or navigation.relation_set_ref != relation_set_ref
        or navigation.relations_certification_id
        != relations_certification.certification_id
        or navigation.relations_certification_ref != certification_ref
        or navigation.summary_id != summary.summary_id
        or navigation.summary_ref != summary_ref
        or navigation.statistics_id != statistics.statistics_id
        or navigation.statistics_ref != statistics_ref
        or navigation.provenance_ref != certification_ref
        or relations_certification.relation_set_id
        != relation_set.relation_set_id
        or relations_certification.relation_set_ref != relation_set_ref
        or relations_certification.structural_summary_ref != summary_ref
        or relations_certification.structural_statistics_ref != statistics_ref
    ):
        raise ValueError("WP19 inputs do not share certified lineage")

    entries = tuple(_entry_from_relation(item) for item in relation_set.relations)
    basis = _construction_basis(
        navigation_id=navigation.navigation_id,
        navigation_contract_ref=navigation_ref,
        relation_set_id=relation_set.relation_set_id,
        relation_set_ref=relation_set_ref,
        relations_certification_id=relations_certification.certification_id,
        relations_certification_ref=certification_ref,
        summary_ref=summary_ref,
        statistics_ref=statistics_ref,
        entries=entries,
        provenance_ref=certification_ref,
    )
    digest = _digest(basis)
    return ConstructedNavigationObject(
        construction_id=f"navigation-construction-{digest[:24]}",
        construction_integrity=digest,
        schema_version=NAVIGATION_CONSTRUCTION_SCHEMA_VERSION,
        navigation_id=navigation.navigation_id,
        navigation_contract_ref=navigation_ref,
        relation_set_id=relation_set.relation_set_id,
        relation_set_ref=relation_set_ref,
        relations_certification_id=relations_certification.certification_id,
        relations_certification_ref=certification_ref,
        summary_ref=summary_ref,
        statistics_ref=statistics_ref,
        entry_count=len(entries),
        entries=entries,
        provenance_ref=certification_ref,
        serialization_version=SERIALIZATION_VERSION,
        responsibility=RESPONSIBILITY,
        construction_state=CONSTRUCTION_STATE,
        externally_conformant=False,
        stop=STOP_AFTER_NAVIGATION_CONSTRUCTION,
    )


def navigation_entry_from_dict(
    value: Mapping[str, object],
) -> NavigationEntry:
    if not isinstance(value, Mapping):
        raise TypeError("Navigation Entry must be a mapping")
    expected_fields = {
        "entry_id",
        "entry_schema_version",
        "canonical_order",
        "relation_id",
        "relation_ref",
        "relation_kind",
        "source_element_id",
        "target_element_id",
        "structural_adjacency_ref",
        "provenance_ref",
    }
    if set(value) != expected_fields:
        raise ValueError("Navigation Entry fields do not match WP19")
    return NavigationEntry(**dict(value))


def constructed_navigation_as_dict(
    navigation: ConstructedNavigationObject,
) -> dict[str, object]:
    navigation.__post_init__()
    return asdict(navigation)


def canonical_constructed_navigation_bytes(
    navigation: ConstructedNavigationObject,
) -> bytes:
    return _canonical_bytes(constructed_navigation_as_dict(navigation))


def constructed_navigation_from_dict(
    value: Mapping[str, object],
) -> ConstructedNavigationObject:
    if not isinstance(value, Mapping):
        raise TypeError("Constructed Navigation Object must be a mapping")
    expected_fields = {
        "construction_id",
        "construction_integrity",
        "schema_version",
        "navigation_id",
        "navigation_contract_ref",
        "relation_set_id",
        "relation_set_ref",
        "relations_certification_id",
        "relations_certification_ref",
        "summary_ref",
        "statistics_ref",
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
        raise ValueError("Constructed Navigation fields do not match WP19")
    entries_value = value["entries"]
    if not isinstance(entries_value, (tuple, list)):
        raise TypeError("entries must be an ordered collection")
    entries = tuple(
        navigation_entry_from_dict(entry) for entry in entries_value
    )
    return ConstructedNavigationObject(
        **{key: item for key, item in value.items() if key != "entries"},
        entries=entries,
    )


__all__: tuple[str, ...] = ()
