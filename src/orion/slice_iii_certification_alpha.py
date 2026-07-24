"""Observational Vertical Slice III Certification for WP25.

Certification consumes supplied immutable Relations, Navigation, Orientation
Map, Summary, and Statistics artifacts. It replays canonical bytes and checks
their accepted lineage only. It never constructs, validates, traverses,
visualizes, repairs, completes, or interprets an artifact.
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
    FROZEN_NAVIGATION_CONTRACTS,
    PASSED as NAVIGATION_PASSED,
    STOP_AT_NAVIGATION_CERTIFIED,
    NavigationCertificationReport,
    canonical_navigation_certification_report_bytes,
)
from orion.navigation_conformance_alpha import (
    ACCEPTED as NAVIGATION_ACCEPTED,
    STOP_AFTER_NAVIGATION_CONFORMANCE,
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
from orion.orientation_map_conformance_alpha import (
    ACCEPTED as MAP_ACCEPTED,
    STOP_AFTER_ORIENTATION_MAP_CONFORMANCE,
    OrientationMapConformanceReport,
    canonical_orientation_map_conformance_report_bytes,
)
from orion.orientation_map_construction_alpha import (
    ConstructedOrientationMap,
    canonical_constructed_orientation_map_bytes,
)
from orion.orientation_map_object_alpha import (
    OrientationMapObject,
    canonical_orientation_map_object_bytes,
)
from orion.relations_certification_alpha import (
    FROZEN_RELATIONS_CONTRACTS,
    PASSED as RELATIONS_PASSED,
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


SLICE_III_CERTIFICATION_SCHEMA_VERSION = (
    "orion.slice-iii-certification/0.1-alpha"
)
GATE_ID = "vertical-slice-iii"
GATE_VERSION = "0.1-alpha"
PASSED = "passed"
FAILED = "failed"
RESPONSIBILITY = "vertical_slice_iii_certification"
STOP_AT_SLICE_III_CERTIFIED = "at_slice_iii_certified"

_CERTIFICATION_ID = re.compile(r"^slice-iii-certification-[0-9a-f]{24}$")
_SHA256_REF = re.compile(r"^sha256:[0-9a-f]{64}$")
_SHA256_HEX = re.compile(r"^[0-9a-f]{64}$")


@dataclass(frozen=True, slots=True)
class FrozenSliceIIIContract:
    """One immutable implementation fingerprint certified by WP25."""

    work_package: str
    component: str
    source_path: str
    sha256: str

    def __post_init__(self) -> None:
        for field_name in ("work_package", "component", "source_path"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value:
                raise ValueError(f"{field_name} must be exact non-empty text")
        if _SHA256_HEX.fullmatch(self.sha256) is None:
            raise ValueError("frozen contract hash must be SHA-256 hexadecimal")


FROZEN_SLICE_III_CONTRACTS = (
    *(
        FrozenSliceIIIContract(
            work_package=contract.work_package,
            component=contract.component,
            source_path=contract.source_path,
            sha256=contract.sha256,
        )
        for contract in FROZEN_RELATIONS_CONTRACTS
    ),
    FrozenSliceIIIContract(
        work_package="WP17",
        component="Relations Certification",
        source_path="src/orion/relations_certification_alpha.py",
        sha256=(
            "8329de7c8c60fd58aae42045ede2239e"
            "ee98df0ebba70edaceb7feffe7a97a18"
        ),
    ),
    *(
        FrozenSliceIIIContract(
            work_package=contract.work_package,
            component=contract.component,
            source_path=contract.source_path,
            sha256=contract.sha256,
        )
        for contract in FROZEN_NAVIGATION_CONTRACTS
    ),
    FrozenSliceIIIContract(
        work_package="WP21",
        component="Navigation Certification",
        source_path="src/orion/navigation_certification_alpha.py",
        sha256=(
            "444aa58f06c4e6d8c11384a06b8dae0b"
            "1e9fbb666719f90c535b9780bff02e33"
        ),
    ),
    FrozenSliceIIIContract(
        work_package="WP22",
        component="Orientation Map Object",
        source_path="src/orion/orientation_map_object_alpha.py",
        sha256=(
            "6d743c773c813d3d56719f30fea66e78"
            "aa354f7665f2d4befdcc341aaa844fcb"
        ),
    ),
    FrozenSliceIIIContract(
        work_package="WP23",
        component="Orientation Map Construction",
        source_path="src/orion/orientation_map_construction_alpha.py",
        sha256=(
            "0c6ea6001183d4feb8eee84779b1d0777"
            "1a0d85d15c00d77e1b5f580de43d1eb"
        ),
    ),
    FrozenSliceIIIContract(
        work_package="WP24",
        component="External Orientation Map Conformance",
        source_path="src/orion/orientation_map_conformance_alpha.py",
        sha256=(
            "82609be6e9d32a67e1cc13de94d7fd85"
            "1737a56d270a123269632d0de98700d6"
        ),
    ),
)


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


def _certification_basis(
    *,
    relation_set_id: str,
    relation_set_ref: str | None,
    relations_certification_id: str,
    relations_certification_ref: str | None,
    navigation_id: str,
    navigation_ref: str | None,
    navigation_certification_id: str,
    navigation_certification_ref: str | None,
    orientation_map_id: str,
    orientation_map_ref: str | None,
    orientation_map_construction_id: str,
    orientation_map_construction_ref: str | None,
    orientation_map_conformance_id: str,
    orientation_map_conformance_ref: str | None,
    structural_summary_ref: str | None,
    structural_statistics_ref: str | None,
    status: str,
    checks: tuple[str, ...],
    errors: tuple[str, ...],
    relations_replay_byte_identical: bool,
    navigation_replay_byte_identical: bool,
    orientation_map_replay_byte_identical: bool,
    stable_identifiers: bool,
    stable_hashes: bool,
    stable_serialization: bool,
    stable_canonical_ordering: bool,
    provenance_preserved: bool,
    inputs_unchanged: bool,
) -> dict[str, object]:
    return {
        "schema_version": SLICE_III_CERTIFICATION_SCHEMA_VERSION,
        "gate_id": GATE_ID,
        "gate_version": GATE_VERSION,
        "relation_set_id": relation_set_id,
        "relation_set_ref": relation_set_ref,
        "relations_certification_id": relations_certification_id,
        "relations_certification_ref": relations_certification_ref,
        "navigation_id": navigation_id,
        "navigation_ref": navigation_ref,
        "navigation_certification_id": navigation_certification_id,
        "navigation_certification_ref": navigation_certification_ref,
        "orientation_map_id": orientation_map_id,
        "orientation_map_ref": orientation_map_ref,
        "orientation_map_construction_id": orientation_map_construction_id,
        "orientation_map_construction_ref": orientation_map_construction_ref,
        "orientation_map_conformance_id": orientation_map_conformance_id,
        "orientation_map_conformance_ref": orientation_map_conformance_ref,
        "structural_summary_ref": structural_summary_ref,
        "structural_statistics_ref": structural_statistics_ref,
        "frozen_contracts": tuple(
            asdict(contract) for contract in FROZEN_SLICE_III_CONTRACTS
        ),
        "status": status,
        "checks": checks,
        "errors": errors,
        "relations_replay_byte_identical": relations_replay_byte_identical,
        "navigation_replay_byte_identical": navigation_replay_byte_identical,
        "orientation_map_replay_byte_identical": (
            orientation_map_replay_byte_identical
        ),
        "stable_identifiers": stable_identifiers,
        "stable_hashes": stable_hashes,
        "stable_serialization": stable_serialization,
        "stable_canonical_ordering": stable_canonical_ordering,
        "provenance_preserved": provenance_preserved,
        "inputs_unchanged": inputs_unchanged,
        "responsibility": RESPONSIBILITY,
        "stop": STOP_AT_SLICE_III_CERTIFIED,
    }


@dataclass(frozen=True, slots=True)
class SliceIIICertificationReport:
    """Immutable pass-or-fail record for the Slice III Certification Gate."""

    certification_id: str
    certification_integrity: str
    schema_version: str
    gate_id: str
    gate_version: str
    relation_set_id: str
    relation_set_ref: str | None
    relations_certification_id: str
    relations_certification_ref: str | None
    navigation_id: str
    navigation_ref: str | None
    navigation_certification_id: str
    navigation_certification_ref: str | None
    orientation_map_id: str
    orientation_map_ref: str | None
    orientation_map_construction_id: str
    orientation_map_construction_ref: str | None
    orientation_map_conformance_id: str
    orientation_map_conformance_ref: str | None
    structural_summary_ref: str | None
    structural_statistics_ref: str | None
    frozen_contracts: tuple[FrozenSliceIIIContract, ...]
    status: str
    certified: bool
    checks: tuple[str, ...]
    errors: tuple[str, ...]
    relations_replay_byte_identical: bool
    navigation_replay_byte_identical: bool
    orientation_map_replay_byte_identical: bool
    stable_identifiers: bool
    stable_hashes: bool
    stable_serialization: bool
    stable_canonical_ordering: bool
    provenance_preserved: bool
    inputs_unchanged: bool
    responsibility: str
    stop: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "frozen_contracts", tuple(self.frozen_contracts))
        object.__setattr__(self, "checks", tuple(self.checks))
        object.__setattr__(self, "errors", tuple(self.errors))
        if _CERTIFICATION_ID.fullmatch(self.certification_id) is None:
            raise ValueError("certification_id is not canonical")
        if _SHA256_HEX.fullmatch(self.certification_integrity) is None:
            raise ValueError("certification_integrity must be SHA-256")
        if self.schema_version != SLICE_III_CERTIFICATION_SCHEMA_VERSION:
            raise ValueError("Slice III Certification schema changed")
        if self.gate_id != GATE_ID or self.gate_version != GATE_VERSION:
            raise ValueError("Slice III Certification gate identity changed")
        for field_name in (
            "relation_set_id",
            "relations_certification_id",
            "navigation_id",
            "navigation_certification_id",
            "orientation_map_id",
            "orientation_map_construction_id",
            "orientation_map_conformance_id",
        ):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value:
                raise ValueError(f"{field_name} must be observed exact text")
        for field_name in (
            "relation_set_ref",
            "relations_certification_ref",
            "navigation_ref",
            "navigation_certification_ref",
            "orientation_map_ref",
            "orientation_map_construction_ref",
            "orientation_map_conformance_ref",
            "structural_summary_ref",
            "structural_statistics_ref",
        ):
            value = getattr(self, field_name)
            if value is not None and _SHA256_REF.fullmatch(value) is None:
                raise ValueError(f"{field_name} must be a SHA-256 reference")
        if self.frozen_contracts != FROZEN_SLICE_III_CONTRACTS:
            raise ValueError("frozen Slice III contract fingerprints changed")
        if self.status not in (PASSED, FAILED):
            raise ValueError("status is outside the certification vocabulary")
        if type(self.certified) is not bool:
            raise TypeError("certified must be boolean")
        if self.certified != (self.status == PASSED):
            raise ValueError("certified and status differ")
        if self.certified != (not self.errors):
            raise ValueError("certified and errors differ")
        if any(not isinstance(item, str) or not item for item in self.checks):
            raise ValueError("checks must be deterministic non-empty labels")
        if any(not isinstance(item, str) or not item for item in self.errors):
            raise ValueError("errors must be deterministic non-empty text")
        boolean_fields = (
            "relations_replay_byte_identical",
            "navigation_replay_byte_identical",
            "orientation_map_replay_byte_identical",
            "stable_identifiers",
            "stable_hashes",
            "stable_serialization",
            "stable_canonical_ordering",
            "provenance_preserved",
            "inputs_unchanged",
        )
        if any(type(getattr(self, name)) is not bool for name in boolean_fields):
            raise TypeError("certification observations must be boolean")
        if self.certified and not all(
            getattr(self, name) for name in boolean_fields
        ):
            raise ValueError("passed certification contains a failed observation")
        if not self.inputs_unchanged:
            raise ValueError("Certification must never mutate supplied artifacts")
        if self.responsibility != RESPONSIBILITY:
            raise ValueError("Slice III Certification responsibility changed")
        if self.stop != STOP_AT_SLICE_III_CERTIFIED:
            raise ValueError("Slice III Certification STOP changed")
        basis = _certification_basis(
            relation_set_id=self.relation_set_id,
            relation_set_ref=self.relation_set_ref,
            relations_certification_id=self.relations_certification_id,
            relations_certification_ref=self.relations_certification_ref,
            navigation_id=self.navigation_id,
            navigation_ref=self.navigation_ref,
            navigation_certification_id=self.navigation_certification_id,
            navigation_certification_ref=self.navigation_certification_ref,
            orientation_map_id=self.orientation_map_id,
            orientation_map_ref=self.orientation_map_ref,
            orientation_map_construction_id=self.orientation_map_construction_id,
            orientation_map_construction_ref=(
                self.orientation_map_construction_ref
            ),
            orientation_map_conformance_id=self.orientation_map_conformance_id,
            orientation_map_conformance_ref=(
                self.orientation_map_conformance_ref
            ),
            structural_summary_ref=self.structural_summary_ref,
            structural_statistics_ref=self.structural_statistics_ref,
            status=self.status,
            checks=self.checks,
            errors=self.errors,
            relations_replay_byte_identical=(
                self.relations_replay_byte_identical
            ),
            navigation_replay_byte_identical=(
                self.navigation_replay_byte_identical
            ),
            orientation_map_replay_byte_identical=(
                self.orientation_map_replay_byte_identical
            ),
            stable_identifiers=self.stable_identifiers,
            stable_hashes=self.stable_hashes,
            stable_serialization=self.stable_serialization,
            stable_canonical_ordering=self.stable_canonical_ordering,
            provenance_preserved=self.provenance_preserved,
            inputs_unchanged=self.inputs_unchanged,
        )
        digest = _digest(basis)
        if self.certification_id != (
            f"slice-iii-certification-{digest[:24]}"
        ):
            raise ValueError("certification_id differs from observations")
        if self.certification_integrity != digest:
            raise ValueError("certification_integrity differs from observations")


def certify_slice_iii(
    relation_set: object,
    relations_certification: object,
    navigation: object,
    constructed_navigation: object,
    navigation_conformance: object,
    navigation_certification: object,
    orientation_map: object,
    constructed_map: object,
    orientation_map_conformance: object,
    summary: object,
    statistics: object,
) -> SliceIIICertificationReport:
    """Certify supplied immutable artifacts without executing their layers."""

    checks: list[str] = []
    errors: list[str] = []

    def check(name: str, condition: bool, error: str) -> None:
        checks.append(name)
        if not condition:
            errors.append(error)

    values = (
        relation_set,
        relations_certification,
        navigation,
        constructed_navigation,
        navigation_conformance,
        navigation_certification,
        orientation_map,
        constructed_map,
        orientation_map_conformance,
        summary,
        statistics,
    )
    types = (
        DeclaredReferenceRelationSet,
        RelationsCertificationReport,
        NavigationObject,
        ConstructedNavigationObject,
        NavigationConformanceReport,
        NavigationCertificationReport,
        OrientationMapObject,
        ConstructedOrientationMap,
        OrientationMapConformanceReport,
        StructuralSummaryDiagnostic,
        StructuralStatisticsDiagnostic,
    )
    labels = (
        "relation_set",
        "relations_certification",
        "navigation_object",
        "navigation_construction",
        "navigation_conformance",
        "navigation_certification",
        "orientation_map_object",
        "orientation_map_construction",
        "orientation_map_conformance",
        "structural_summary",
        "structural_statistics",
    )
    before = tuple(
        _observed_bytes(value, expected)
        for value, expected in zip(values, types, strict=True)
    )
    refs = tuple(
        _artifact_ref(value) if value is not None else None
        for value in before
    )
    (
        relation_set_bytes,
        relations_certification_bytes,
        navigation_bytes,
        navigation_construction_bytes,
        navigation_conformance_bytes,
        navigation_certification_bytes,
        orientation_map_bytes,
        orientation_map_construction_bytes,
        orientation_map_conformance_bytes,
        summary_bytes,
        statistics_bytes,
    ) = before
    (
        relation_set_ref,
        relations_certification_ref,
        navigation_ref,
        navigation_construction_ref,
        navigation_conformance_ref,
        navigation_certification_ref,
        orientation_map_ref,
        orientation_map_construction_ref,
        orientation_map_conformance_ref,
        summary_ref,
        statistics_ref,
    ) = refs

    shapes: dict[str, bool] = {}
    for label, value, expected in zip(labels, values, types, strict=True):
        valid_shape = False
        if isinstance(value, expected):
            try:
                value.__post_init__()
                valid_shape = True
            except (AttributeError, TypeError, ValueError):
                pass
        shapes[label] = valid_shape
        check(
            f"{label}_immutable_shape",
            valid_shape,
            f"{label.replace('_', ' ').title()} is malformed or not immutable",
        )

    relations_accepted = (
        shapes["relations_certification"]
        and relations_certification.certified
        and relations_certification.status == RELATIONS_PASSED
        and not relations_certification.errors
        and relations_certification.stop == STOP_AT_RELATIONS_CERTIFIED
        and relations_certification.relation_set_ref == relation_set_ref
    )
    check(
        "relations_layer_certified",
        relations_accepted,
        "Relations layer is not exactly certified",
    )
    navigation_accepted = (
        shapes["navigation_certification"]
        and shapes["navigation_conformance"]
        and navigation_certification.certified
        and navigation_certification.status == NAVIGATION_PASSED
        and not navigation_certification.errors
        and navigation_certification.stop == STOP_AT_NAVIGATION_CERTIFIED
        and navigation_conformance.valid
        and navigation_conformance.decision == NAVIGATION_ACCEPTED
        and not navigation_conformance.errors
        and navigation_conformance.stop
        == STOP_AFTER_NAVIGATION_CONFORMANCE
    )
    check(
        "navigation_layer_certified",
        navigation_accepted,
        "Navigation layer is not exactly certified",
    )
    map_accepted = (
        shapes["orientation_map_conformance"]
        and orientation_map_conformance.valid
        and orientation_map_conformance.decision == MAP_ACCEPTED
        and not orientation_map_conformance.errors
        and orientation_map_conformance.stop
        == STOP_AFTER_ORIENTATION_MAP_CONFORMANCE
        and orientation_map_conformance.accepted_orientation_map_ref
        == orientation_map_ref
        and orientation_map_conformance.accepted_construction_ref
        == orientation_map_construction_ref
    )
    check(
        "orientation_map_layer_conformant",
        map_accepted,
        "WP24 did not accept the exact Orientation Map artifacts",
    )

    reference_consistency = (
        all(shapes.values())
        and relations_certification.relation_set_id
        == relation_set.relation_set_id
        and relations_certification.relation_set_ref == relation_set_ref
        and navigation.relation_set_ref == relation_set_ref
        and navigation.relations_certification_ref
        == relations_certification_ref
        and constructed_navigation.navigation_id == navigation.navigation_id
        and constructed_navigation.navigation_contract_ref == navigation_ref
        and navigation_conformance.navigation_ref == navigation_ref
        and navigation_conformance.construction_ref
        == navigation_construction_ref
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
        and orientation_map.navigation_certification_id
        == navigation_certification.certification_id
        and orientation_map.navigation_certification_ref
        == navigation_certification_ref
        and orientation_map.navigation_object_ref == navigation_ref
        and orientation_map.navigation_construction_ref
        == navigation_construction_ref
        and orientation_map.navigation_conformance_ref
        == navigation_conformance_ref
        and orientation_map.relation_set_ref == relation_set_ref
        and orientation_map.relations_certification_ref
        == relations_certification_ref
        and constructed_map.orientation_map_id
        == orientation_map.orientation_map_id
        and constructed_map.orientation_map_contract_ref == orientation_map_ref
        and constructed_map.navigation_certification_ref
        == navigation_certification_ref
        and constructed_map.navigation_construction_ref
        == navigation_construction_ref
        and orientation_map_conformance.orientation_map_id
        == orientation_map.orientation_map_id
        and orientation_map_conformance.orientation_map_ref
        == orientation_map_ref
        and orientation_map_conformance.construction_id
        == constructed_map.construction_id
        and orientation_map_conformance.construction_ref
        == orientation_map_construction_ref
        and orientation_map_conformance.navigation_certification_ref
        == navigation_certification_ref
        and orientation_map_conformance.relation_set_ref == relation_set_ref
        and relations_certification.structural_summary_ref == summary_ref
        and relations_certification.structural_statistics_ref == statistics_ref
        and navigation_certification.structural_summary_ref == summary_ref
        and navigation_certification.structural_statistics_ref == statistics_ref
        and orientation_map.summary_ref == summary_ref
        and orientation_map.statistics_ref == statistics_ref
        and orientation_map_conformance.structural_summary_ref == summary_ref
        and orientation_map_conformance.structural_statistics_ref
        == statistics_ref
    )
    check(
        "complete_dependency_chain",
        reference_consistency,
        "Slice III artifacts do not share exact immutable references",
    )

    relations_replay = (
        shapes["relation_set"]
        and shapes["relations_certification"]
        and canonical_declared_reference_relation_set_bytes(relation_set)
        == relation_set_bytes
        and canonical_relations_certification_report_bytes(
            relations_certification
        )
        == relations_certification_bytes
    )
    check(
        "relations_layer_byte_replay",
        relations_replay,
        "Relations artifacts do not replay byte-identically",
    )
    navigation_replay = (
        shapes["navigation_object"]
        and shapes["navigation_construction"]
        and shapes["navigation_conformance"]
        and shapes["navigation_certification"]
        and canonical_navigation_object_bytes(navigation) == navigation_bytes
        and canonical_constructed_navigation_bytes(constructed_navigation)
        == navigation_construction_bytes
        and canonical_navigation_conformance_report_bytes(
            navigation_conformance
        )
        == navigation_conformance_bytes
        and canonical_navigation_certification_report_bytes(
            navigation_certification
        )
        == navigation_certification_bytes
    )
    check(
        "navigation_layer_byte_replay",
        navigation_replay,
        "Navigation artifacts do not replay byte-identically",
    )
    orientation_map_replay = (
        shapes["orientation_map_object"]
        and shapes["orientation_map_construction"]
        and shapes["orientation_map_conformance"]
        and canonical_orientation_map_object_bytes(orientation_map)
        == orientation_map_bytes
        and canonical_constructed_orientation_map_bytes(constructed_map)
        == orientation_map_construction_bytes
        and canonical_orientation_map_conformance_report_bytes(
            orientation_map_conformance
        )
        == orientation_map_conformance_bytes
    )
    check(
        "orientation_map_layer_byte_replay",
        orientation_map_replay,
        "Orientation Map artifacts do not replay byte-identically",
    )

    stable_identifiers = (
        reference_consistency
        and isinstance(relation_set.relation_set_id, str)
        and isinstance(relations_certification.certification_id, str)
        and isinstance(navigation.navigation_id, str)
        and isinstance(navigation_certification.certification_id, str)
        and isinstance(orientation_map.orientation_map_id, str)
        and isinstance(constructed_map.construction_id, str)
        and isinstance(orientation_map_conformance.report_id, str)
    )
    check(
        "stable_identifiers",
        stable_identifiers,
        "Slice III identifiers are absent or inconsistent",
    )
    stable_hashes = all(reference is not None for reference in refs)
    check(
        "stable_hashes",
        stable_hashes,
        "Slice III artifact hashes are absent",
    )
    stable_serialization = (
        relations_replay and navigation_replay and orientation_map_replay
    )
    check(
        "stable_serialization",
        stable_serialization,
        "Slice III canonical serialization is not stable",
    )
    stable_canonical_ordering = (
        all(shapes.values())
        and tuple(
            relation.canonical_order for relation in relation_set.relations
        )
        == tuple(range(len(relation_set.relations)))
        and tuple(
            entry.canonical_order
            for entry in constructed_navigation.entries
        )
        == tuple(range(len(constructed_navigation.entries)))
        and tuple(entry.canonical_order for entry in constructed_map.entries)
        == tuple(range(len(constructed_map.entries)))
        and tuple(
            entry.relation_id for entry in constructed_navigation.entries
        )
        == tuple(relation.relation_id for relation in relation_set.relations)
        and tuple(
            entry.navigation_entry_id for entry in constructed_map.entries
        )
        == tuple(entry.entry_id for entry in constructed_navigation.entries)
    )
    check(
        "stable_canonical_ordering",
        stable_canonical_ordering,
        "Slice III canonical ordering is inconsistent",
    )
    provenance_preserved = (
        reference_consistency
        and relations_certification.provenance_preserved
        and navigation_certification.provenance_preserved
        and "provenance_preservation" in orientation_map_conformance.checks
        and orientation_map.provenance_ref == navigation_certification_ref
        and constructed_map.provenance_ref == navigation_certification_ref
    )
    check(
        "provenance_preserved",
        provenance_preserved,
        "Slice III provenance is incomplete or inconsistent",
    )
    frozen_contracts_present = (
        tuple(
            contract.work_package
            for contract in FROZEN_SLICE_III_CONTRACTS
        )
        == tuple(f"WP{number}" for number in range(12, 25))
        and len(
            {contract.sha256 for contract in FROZEN_SLICE_III_CONTRACTS}
        )
        == len(FROZEN_SLICE_III_CONTRACTS)
    )
    check(
        "frozen_contract_fingerprints",
        frozen_contracts_present,
        "Frozen WP12-WP24 contract fingerprints are incomplete",
    )

    after = tuple(
        _observed_bytes(value, expected)
        for value, expected in zip(values, types, strict=True)
    )
    inputs_unchanged = before == after
    check(
        "inputs_unchanged",
        inputs_unchanged,
        "Slice III Certification changed a supplied artifact",
    )

    status = PASSED if not errors else FAILED
    relation_set_id = _safe_text(
        getattr(relation_set, "relation_set_id", None),
        "unavailable",
    )
    relations_certification_id = _safe_text(
        getattr(relations_certification, "certification_id", None),
        "unavailable",
    )
    navigation_id = _safe_text(
        getattr(navigation, "navigation_id", None),
        "unavailable",
    )
    navigation_certification_id = _safe_text(
        getattr(navigation_certification, "certification_id", None),
        "unavailable",
    )
    orientation_map_id = _safe_text(
        getattr(orientation_map, "orientation_map_id", None),
        "unavailable",
    )
    map_construction_id = _safe_text(
        getattr(constructed_map, "construction_id", None),
        "unavailable",
    )
    map_conformance_id = _safe_text(
        getattr(orientation_map_conformance, "report_id", None),
        "unavailable",
    )
    basis = _certification_basis(
        relation_set_id=relation_set_id,
        relation_set_ref=relation_set_ref,
        relations_certification_id=relations_certification_id,
        relations_certification_ref=relations_certification_ref,
        navigation_id=navigation_id,
        navigation_ref=navigation_ref,
        navigation_certification_id=navigation_certification_id,
        navigation_certification_ref=navigation_certification_ref,
        orientation_map_id=orientation_map_id,
        orientation_map_ref=orientation_map_ref,
        orientation_map_construction_id=map_construction_id,
        orientation_map_construction_ref=orientation_map_construction_ref,
        orientation_map_conformance_id=map_conformance_id,
        orientation_map_conformance_ref=orientation_map_conformance_ref,
        structural_summary_ref=summary_ref,
        structural_statistics_ref=statistics_ref,
        status=status,
        checks=tuple(checks),
        errors=tuple(errors),
        relations_replay_byte_identical=relations_replay,
        navigation_replay_byte_identical=navigation_replay,
        orientation_map_replay_byte_identical=orientation_map_replay,
        stable_identifiers=stable_identifiers,
        stable_hashes=stable_hashes,
        stable_serialization=stable_serialization,
        stable_canonical_ordering=stable_canonical_ordering,
        provenance_preserved=provenance_preserved,
        inputs_unchanged=inputs_unchanged,
    )
    digest = _digest(basis)
    return SliceIIICertificationReport(
        certification_id=f"slice-iii-certification-{digest[:24]}",
        certification_integrity=digest,
        schema_version=SLICE_III_CERTIFICATION_SCHEMA_VERSION,
        gate_id=GATE_ID,
        gate_version=GATE_VERSION,
        relation_set_id=relation_set_id,
        relation_set_ref=relation_set_ref,
        relations_certification_id=relations_certification_id,
        relations_certification_ref=relations_certification_ref,
        navigation_id=navigation_id,
        navigation_ref=navigation_ref,
        navigation_certification_id=navigation_certification_id,
        navigation_certification_ref=navigation_certification_ref,
        orientation_map_id=orientation_map_id,
        orientation_map_ref=orientation_map_ref,
        orientation_map_construction_id=map_construction_id,
        orientation_map_construction_ref=orientation_map_construction_ref,
        orientation_map_conformance_id=map_conformance_id,
        orientation_map_conformance_ref=orientation_map_conformance_ref,
        structural_summary_ref=summary_ref,
        structural_statistics_ref=statistics_ref,
        frozen_contracts=FROZEN_SLICE_III_CONTRACTS,
        status=status,
        certified=status == PASSED,
        checks=tuple(checks),
        errors=tuple(errors),
        relations_replay_byte_identical=relations_replay,
        navigation_replay_byte_identical=navigation_replay,
        orientation_map_replay_byte_identical=orientation_map_replay,
        stable_identifiers=stable_identifiers,
        stable_hashes=stable_hashes,
        stable_serialization=stable_serialization,
        stable_canonical_ordering=stable_canonical_ordering,
        provenance_preserved=provenance_preserved,
        inputs_unchanged=inputs_unchanged,
        responsibility=RESPONSIBILITY,
        stop=STOP_AT_SLICE_III_CERTIFIED,
    )


def slice_iii_certification_report_as_dict(
    report: SliceIIICertificationReport,
) -> dict[str, object]:
    report.__post_init__()
    return asdict(report)


def canonical_slice_iii_certification_report_bytes(
    report: SliceIIICertificationReport,
) -> bytes:
    return _canonical_bytes(slice_iii_certification_report_as_dict(report))


def _frozen_contract_from_dict(
    value: Mapping[str, object],
) -> FrozenSliceIIIContract:
    if not isinstance(value, Mapping):
        raise TypeError("frozen contract must be a mapping")
    expected = {"work_package", "component", "source_path", "sha256"}
    if set(value) != expected:
        raise ValueError("frozen contract fields do not match WP25")
    return FrozenSliceIIIContract(**dict(value))


def slice_iii_certification_report_from_dict(
    value: Mapping[str, object],
) -> SliceIIICertificationReport:
    if not isinstance(value, Mapping):
        raise TypeError("Slice III Certification Report must be a mapping")
    expected_fields = {
        "certification_id",
        "certification_integrity",
        "schema_version",
        "gate_id",
        "gate_version",
        "relation_set_id",
        "relation_set_ref",
        "relations_certification_id",
        "relations_certification_ref",
        "navigation_id",
        "navigation_ref",
        "navigation_certification_id",
        "navigation_certification_ref",
        "orientation_map_id",
        "orientation_map_ref",
        "orientation_map_construction_id",
        "orientation_map_construction_ref",
        "orientation_map_conformance_id",
        "orientation_map_conformance_ref",
        "structural_summary_ref",
        "structural_statistics_ref",
        "frozen_contracts",
        "status",
        "certified",
        "checks",
        "errors",
        "relations_replay_byte_identical",
        "navigation_replay_byte_identical",
        "orientation_map_replay_byte_identical",
        "stable_identifiers",
        "stable_hashes",
        "stable_serialization",
        "stable_canonical_ordering",
        "provenance_preserved",
        "inputs_unchanged",
        "responsibility",
        "stop",
    }
    if set(value) != expected_fields:
        raise ValueError("Slice III Certification fields do not match WP25")
    frozen_value = value["frozen_contracts"]
    if not isinstance(frozen_value, (tuple, list)):
        raise TypeError("frozen_contracts must be ordered")
    frozen_contracts = tuple(
        _frozen_contract_from_dict(item) for item in frozen_value
    )
    return SliceIIICertificationReport(
        **{
            key: item
            for key, item in value.items()
            if key != "frozen_contracts"
        },
        frozen_contracts=frozen_contracts,
    )


__all__: tuple[str, ...] = ()
