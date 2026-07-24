"""Observational Navigation Certification for Slice III WP21.

Certification consumes supplied immutable WP18-WP20 Navigation artifacts and
their exact frozen dependencies. It replays canonical bytes and checks
references only. It never constructs, validates, traverses, or repairs
Navigation.
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
from orion.navigation_conformance_alpha import (
    ACCEPTED,
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
from orion.relations_certification_alpha import (
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


NAVIGATION_CERTIFICATION_SCHEMA_VERSION = (
    "orion.navigation-certification/0.1-alpha"
)
GATE_ID = "slice-iii-navigation"
GATE_VERSION = "0.1-alpha"
PASSED = "passed"
FAILED = "failed"
RESPONSIBILITY = "navigation_certification"
STOP_AT_NAVIGATION_CERTIFIED = "at_navigation_certified"

_CERTIFICATION_ID = re.compile(r"^navigation-certification-[0-9a-f]{24}$")
_SHA256_REF = re.compile(r"^sha256:[0-9a-f]{64}$")
_SHA256_HEX = re.compile(r"^[0-9a-f]{64}$")


@dataclass(frozen=True, slots=True)
class FrozenNavigationContract:
    """One immutable Navigation implementation fingerprint."""

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


FROZEN_NAVIGATION_CONTRACTS = (
    FrozenNavigationContract(
        work_package="WP18",
        component="Navigation Object",
        source_path="src/orion/navigation_object_alpha.py",
        sha256=(
            "d9c99cc09f041fc166739d3954818c109"
            "6d6028926d99125e5d17f9eb18b2036"
        ),
    ),
    FrozenNavigationContract(
        work_package="WP19",
        component="Navigation Construction",
        source_path="src/orion/navigation_construction_alpha.py",
        sha256=(
            "32f48449fe48f00b6b72d76142dee892"
            "a079962bcb47e1ed910d7950509b0336"
        ),
    ),
    FrozenNavigationContract(
        work_package="WP20",
        component="External Navigation Conformance",
        source_path="src/orion/navigation_conformance_alpha.py",
        sha256=(
            "30636b5776fd9eb259e4d1bce8d8afb1"
            "1d93ff47ce0dd72af8ebae962e82ab83"
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


def _certification_basis(
    *,
    navigation_id: str,
    navigation_ref: str | None,
    construction_id: str,
    construction_ref: str | None,
    conformance_report_id: str,
    conformance_report_ref: str | None,
    relation_set_ref: str | None,
    relations_certification_ref: str | None,
    structural_summary_ref: str | None,
    structural_statistics_ref: str | None,
    status: str,
    checks: tuple[str, ...],
    errors: tuple[str, ...],
    navigation_replay_byte_identical: bool,
    construction_replay_byte_identical: bool,
    conformance_report_replay_byte_identical: bool,
    stable_identifiers: bool,
    stable_hashes: bool,
    stable_serialization: bool,
    stable_canonical_ordering: bool,
    provenance_preserved: bool,
    inputs_unchanged: bool,
) -> dict[str, object]:
    return {
        "schema_version": NAVIGATION_CERTIFICATION_SCHEMA_VERSION,
        "gate_id": GATE_ID,
        "gate_version": GATE_VERSION,
        "navigation_id": navigation_id,
        "navigation_ref": navigation_ref,
        "construction_id": construction_id,
        "construction_ref": construction_ref,
        "conformance_report_id": conformance_report_id,
        "conformance_report_ref": conformance_report_ref,
        "relation_set_ref": relation_set_ref,
        "relations_certification_ref": relations_certification_ref,
        "structural_summary_ref": structural_summary_ref,
        "structural_statistics_ref": structural_statistics_ref,
        "frozen_contracts": tuple(
            asdict(contract) for contract in FROZEN_NAVIGATION_CONTRACTS
        ),
        "status": status,
        "checks": checks,
        "errors": errors,
        "navigation_replay_byte_identical": (
            navigation_replay_byte_identical
        ),
        "construction_replay_byte_identical": (
            construction_replay_byte_identical
        ),
        "conformance_report_replay_byte_identical": (
            conformance_report_replay_byte_identical
        ),
        "stable_identifiers": stable_identifiers,
        "stable_hashes": stable_hashes,
        "stable_serialization": stable_serialization,
        "stable_canonical_ordering": stable_canonical_ordering,
        "provenance_preserved": provenance_preserved,
        "inputs_unchanged": inputs_unchanged,
        "responsibility": RESPONSIBILITY,
        "stop": STOP_AT_NAVIGATION_CERTIFIED,
    }


@dataclass(frozen=True, slots=True)
class NavigationCertificationReport:
    """Immutable pass-or-fail record for the Navigation Certification Gate."""

    certification_id: str
    certification_integrity: str
    schema_version: str
    gate_id: str
    gate_version: str
    navigation_id: str
    navigation_ref: str | None
    construction_id: str
    construction_ref: str | None
    conformance_report_id: str
    conformance_report_ref: str | None
    relation_set_ref: str | None
    relations_certification_ref: str | None
    structural_summary_ref: str | None
    structural_statistics_ref: str | None
    frozen_contracts: tuple[FrozenNavigationContract, ...]
    status: str
    certified: bool
    checks: tuple[str, ...]
    errors: tuple[str, ...]
    navigation_replay_byte_identical: bool
    construction_replay_byte_identical: bool
    conformance_report_replay_byte_identical: bool
    stable_identifiers: bool
    stable_hashes: bool
    stable_serialization: bool
    stable_canonical_ordering: bool
    provenance_preserved: bool
    inputs_unchanged: bool
    responsibility: str
    stop: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "frozen_contracts",
            tuple(self.frozen_contracts),
        )
        object.__setattr__(self, "checks", tuple(self.checks))
        object.__setattr__(self, "errors", tuple(self.errors))
        if _CERTIFICATION_ID.fullmatch(self.certification_id) is None:
            raise ValueError("certification_id is not canonical")
        if _SHA256_HEX.fullmatch(self.certification_integrity) is None:
            raise ValueError("certification_integrity must be SHA-256")
        if self.schema_version != NAVIGATION_CERTIFICATION_SCHEMA_VERSION:
            raise ValueError("Navigation Certification schema changed")
        if self.gate_id != GATE_ID or self.gate_version != GATE_VERSION:
            raise ValueError("Navigation Certification Gate changed")
        for field_name in (
            "navigation_id",
            "construction_id",
            "conformance_report_id",
        ):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value:
                raise ValueError(f"{field_name} must be observed exact text")
        for field_name in (
            "navigation_ref",
            "construction_ref",
            "conformance_report_ref",
            "relation_set_ref",
            "relations_certification_ref",
            "structural_summary_ref",
            "structural_statistics_ref",
        ):
            value = getattr(self, field_name)
            if value is not None and _SHA256_REF.fullmatch(value) is None:
                raise ValueError(f"{field_name} must be a SHA-256 reference")
        if self.frozen_contracts != FROZEN_NAVIGATION_CONTRACTS:
            raise ValueError("frozen Navigation contract baseline changed")
        for contract in self.frozen_contracts:
            contract.__post_init__()
        if self.status not in (PASSED, FAILED):
            raise ValueError("status is outside certification vocabulary")
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
            "navigation_replay_byte_identical",
            "construction_replay_byte_identical",
            "conformance_report_replay_byte_identical",
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
            raise ValueError("passed certification has a failed observation")
        if not self.inputs_unchanged:
            raise ValueError("Certification must never mutate inputs")
        if self.responsibility != RESPONSIBILITY:
            raise ValueError("Navigation Certification responsibility changed")
        if self.stop != STOP_AT_NAVIGATION_CERTIFIED:
            raise ValueError("Navigation Certification STOP changed")
        basis = _certification_basis(
            navigation_id=self.navigation_id,
            navigation_ref=self.navigation_ref,
            construction_id=self.construction_id,
            construction_ref=self.construction_ref,
            conformance_report_id=self.conformance_report_id,
            conformance_report_ref=self.conformance_report_ref,
            relation_set_ref=self.relation_set_ref,
            relations_certification_ref=self.relations_certification_ref,
            structural_summary_ref=self.structural_summary_ref,
            structural_statistics_ref=self.structural_statistics_ref,
            status=self.status,
            checks=self.checks,
            errors=self.errors,
            navigation_replay_byte_identical=(
                self.navigation_replay_byte_identical
            ),
            construction_replay_byte_identical=(
                self.construction_replay_byte_identical
            ),
            conformance_report_replay_byte_identical=(
                self.conformance_report_replay_byte_identical
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
            f"navigation-certification-{digest[:24]}"
        ):
            raise ValueError("certification_id differs from observations")
        if self.certification_integrity != digest:
            raise ValueError("certification_integrity differs from observations")


def certify_navigation(
    navigation: object,
    constructed: object,
    conformance_report: object,
    relation_set: object,
    relations_certification: object,
    summary: object,
    statistics: object,
) -> NavigationCertificationReport:
    """Certify supplied immutable artifacts without reconstructing them."""

    checks: list[str] = []
    errors: list[str] = []

    def check(name: str, condition: bool, error: str) -> None:
        checks.append(name)
        if not condition:
            errors.append(error)

    supplied = (
        (navigation, NavigationObject),
        (constructed, ConstructedNavigationObject),
        (conformance_report, NavigationConformanceReport),
        (relation_set, DeclaredReferenceRelationSet),
        (relations_certification, RelationsCertificationReport),
        (summary, StructuralSummaryDiagnostic),
        (statistics, StructuralStatisticsDiagnostic),
    )
    before = tuple(_observed_bytes(value, kind) for value, kind in supplied)
    (
        navigation_bytes,
        construction_bytes,
        conformance_bytes,
        relation_set_bytes,
        relations_certification_bytes,
        summary_bytes,
        statistics_bytes,
    ) = before

    shapes: list[bool] = []
    shape_checks = (
        ("navigation_object", "Navigation Object"),
        ("navigation_construction", "Navigation Construction"),
        ("navigation_conformance", "Navigation Conformance Report"),
        ("relation_set", "Relation Set"),
        ("relations_certification", "Relations Certification"),
        ("structural_summary", "Structural Summary"),
        ("structural_statistics", "Structural Statistics"),
    )
    for (value, kind), (label, human_name) in zip(
        supplied,
        shape_checks,
        strict=True,
    ):
        valid_shape = isinstance(value, kind)
        if valid_shape:
            try:
                value.__post_init__()
            except (AttributeError, TypeError, ValueError):
                valid_shape = False
        shapes.append(valid_shape)
        check(
            f"{label}_immutable_shape",
            valid_shape,
            f"{human_name} is malformed or not immutable",
        )
    (
        navigation_shape,
        construction_shape,
        conformance_shape,
        relation_set_shape,
        relations_certification_shape,
        summary_shape,
        statistics_shape,
    ) = shapes

    navigation_ref = (
        _artifact_ref(navigation_bytes) if navigation_bytes is not None else None
    )
    construction_ref = (
        _artifact_ref(construction_bytes)
        if construction_bytes is not None
        else None
    )
    conformance_ref = (
        _artifact_ref(conformance_bytes)
        if conformance_bytes is not None
        else None
    )
    relation_set_ref = (
        _artifact_ref(relation_set_bytes)
        if relation_set_bytes is not None
        else None
    )
    relations_certification_ref = (
        _artifact_ref(relations_certification_bytes)
        if relations_certification_bytes is not None
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

    conformance_accepted = (
        conformance_shape
        and conformance_report.valid
        and conformance_report.decision == ACCEPTED
        and not conformance_report.errors
        and conformance_report.accepted_construction_ref == construction_ref
        and conformance_report.stop == STOP_AFTER_NAVIGATION_CONFORMANCE
    )
    check(
        "wp20_conformance_accepted",
        conformance_accepted,
        "WP20 did not accept the exact supplied Navigation Construction",
    )

    exact_references = (
        all(shapes)
        and conformance_report.navigation_id == navigation.navigation_id
        and conformance_report.navigation_ref == navigation_ref
        and conformance_report.construction_id
        == constructed.construction_id
        and conformance_report.construction_ref == construction_ref
        and conformance_report.relation_set_id == relation_set.relation_set_id
        and conformance_report.relation_set_ref == relation_set_ref
        and conformance_report.relations_certification_id
        == relations_certification.certification_id
        and conformance_report.relations_certification_ref
        == relations_certification_ref
        and conformance_report.structural_summary_ref == summary_ref
        and conformance_report.structural_statistics_ref == statistics_ref
        and constructed.navigation_id == navigation.navigation_id
        and constructed.navigation_contract_ref == navigation_ref
        and constructed.relation_set_id == relation_set.relation_set_id
        and constructed.relation_set_ref == relation_set_ref
        and constructed.relations_certification_id
        == relations_certification.certification_id
        and constructed.relations_certification_ref
        == relations_certification_ref
        and constructed.summary_ref == summary_ref
        and constructed.statistics_ref == statistics_ref
        and relations_certification.relation_set_id
        == relation_set.relation_set_id
        and relations_certification.relation_set_ref == relation_set_ref
        and relations_certification.structural_summary_ref == summary_ref
        and relations_certification.structural_statistics_ref == statistics_ref
        and relations_certification.stop == STOP_AT_RELATIONS_CERTIFIED
    )
    check(
        "exact_artifact_references",
        exact_references,
        "Navigation Certification inputs do not share exact references",
    )

    navigation_replay = False
    if navigation_shape:
        try:
            navigation_replay = (
                canonical_navigation_object_bytes(navigation)
                == canonical_navigation_object_bytes(navigation)
                == navigation_bytes
            )
        except (AttributeError, TypeError, ValueError):
            pass
    check(
        "navigation_object_byte_replay",
        navigation_replay,
        "Navigation Object bytes do not replay identically",
    )

    construction_replay = False
    if construction_shape:
        try:
            construction_replay = (
                canonical_constructed_navigation_bytes(constructed)
                == canonical_constructed_navigation_bytes(constructed)
                == construction_bytes
            )
        except (AttributeError, TypeError, ValueError):
            pass
    check(
        "navigation_construction_byte_replay",
        construction_replay,
        "Navigation Construction bytes do not replay identically",
    )

    conformance_replay = False
    if conformance_shape:
        try:
            conformance_replay = (
                canonical_navigation_conformance_report_bytes(
                    conformance_report
                )
                == canonical_navigation_conformance_report_bytes(
                    conformance_report
                )
                == conformance_bytes
            )
        except (AttributeError, TypeError, ValueError):
            pass
    check(
        "navigation_conformance_byte_replay",
        conformance_replay,
        "Navigation Conformance Report bytes do not replay identically",
    )

    stable_identifiers = (
        exact_references
        and isinstance(navigation.navigation_id, str)
        and isinstance(constructed.construction_id, str)
        and isinstance(conformance_report.report_id, str)
    )
    check(
        "stable_identifiers",
        stable_identifiers,
        "Navigation identifiers are absent or inconsistent",
    )

    stable_hashes = (
        exact_references
        and all(
            reference is not None
            for reference in (
                navigation_ref,
                construction_ref,
                conformance_ref,
                relation_set_ref,
                relations_certification_ref,
                summary_ref,
                statistics_ref,
            )
        )
    )
    check(
        "stable_hashes",
        stable_hashes,
        "Navigation artifact hashes are absent or inconsistent",
    )

    stable_serialization = (
        navigation_replay and construction_replay and conformance_replay
    )
    check(
        "stable_serialization",
        stable_serialization,
        "Navigation serialization is not stable",
    )

    required_order_checks = {
        "canonical_entry_order",
        "duplicate_entry_absence",
        "immutable_relation_references",
        "structural_adjacency_references",
    }
    stable_canonical_ordering = (
        conformance_accepted
        and required_order_checks.issubset(conformance_report.checks)
    )
    check(
        "stable_canonical_ordering",
        stable_canonical_ordering,
        "Accepted WP20 report lacks canonical ordering observations",
    )

    provenance_preserved = (
        conformance_accepted
        and exact_references
        and "provenance_preservation" in conformance_report.checks
        and constructed.provenance_ref == relations_certification_ref
        and navigation.provenance_ref == relations_certification_ref
    )
    check(
        "provenance_preserved",
        provenance_preserved,
        "Accepted Navigation provenance is incomplete or inconsistent",
    )

    frozen_contracts_present = (
        tuple(
            contract.work_package
            for contract in FROZEN_NAVIGATION_CONTRACTS
        )
        == ("WP18", "WP19", "WP20")
        and len(
            {contract.sha256 for contract in FROZEN_NAVIGATION_CONTRACTS}
        )
        == len(FROZEN_NAVIGATION_CONTRACTS)
    )
    check(
        "frozen_navigation_contract_fingerprints",
        frozen_contracts_present,
        "Frozen WP18-WP20 contract fingerprints are incomplete",
    )

    after = tuple(_observed_bytes(value, kind) for value, kind in supplied)
    inputs_unchanged = before == after
    check(
        "inputs_unchanged",
        inputs_unchanged,
        "Navigation Certification changed a supplied artifact",
    )

    status = PASSED if not errors else FAILED
    navigation_id = (
        navigation.navigation_id if navigation_shape else "unavailable"
    )
    construction_id = (
        constructed.construction_id if construction_shape else "unavailable"
    )
    conformance_report_id = (
        conformance_report.report_id if conformance_shape else "unavailable"
    )
    basis = _certification_basis(
        navigation_id=navigation_id,
        navigation_ref=navigation_ref,
        construction_id=construction_id,
        construction_ref=construction_ref,
        conformance_report_id=conformance_report_id,
        conformance_report_ref=conformance_ref,
        relation_set_ref=relation_set_ref,
        relations_certification_ref=relations_certification_ref,
        structural_summary_ref=summary_ref,
        structural_statistics_ref=statistics_ref,
        status=status,
        checks=tuple(checks),
        errors=tuple(errors),
        navigation_replay_byte_identical=navigation_replay,
        construction_replay_byte_identical=construction_replay,
        conformance_report_replay_byte_identical=conformance_replay,
        stable_identifiers=stable_identifiers,
        stable_hashes=stable_hashes,
        stable_serialization=stable_serialization,
        stable_canonical_ordering=stable_canonical_ordering,
        provenance_preserved=provenance_preserved,
        inputs_unchanged=inputs_unchanged,
    )
    digest = _digest(basis)
    return NavigationCertificationReport(
        certification_id=f"navigation-certification-{digest[:24]}",
        certification_integrity=digest,
        schema_version=NAVIGATION_CERTIFICATION_SCHEMA_VERSION,
        gate_id=GATE_ID,
        gate_version=GATE_VERSION,
        navigation_id=navigation_id,
        navigation_ref=navigation_ref,
        construction_id=construction_id,
        construction_ref=construction_ref,
        conformance_report_id=conformance_report_id,
        conformance_report_ref=conformance_ref,
        relation_set_ref=relation_set_ref,
        relations_certification_ref=relations_certification_ref,
        structural_summary_ref=summary_ref,
        structural_statistics_ref=statistics_ref,
        frozen_contracts=FROZEN_NAVIGATION_CONTRACTS,
        status=status,
        certified=not errors,
        checks=tuple(checks),
        errors=tuple(errors),
        navigation_replay_byte_identical=navigation_replay,
        construction_replay_byte_identical=construction_replay,
        conformance_report_replay_byte_identical=conformance_replay,
        stable_identifiers=stable_identifiers,
        stable_hashes=stable_hashes,
        stable_serialization=stable_serialization,
        stable_canonical_ordering=stable_canonical_ordering,
        provenance_preserved=provenance_preserved,
        inputs_unchanged=inputs_unchanged,
        responsibility=RESPONSIBILITY,
        stop=STOP_AT_NAVIGATION_CERTIFIED,
    )


def navigation_certification_report_as_dict(
    report: NavigationCertificationReport,
) -> dict[str, object]:
    report.__post_init__()
    return asdict(report)


def canonical_navigation_certification_report_bytes(
    report: NavigationCertificationReport,
) -> bytes:
    return _canonical_bytes(navigation_certification_report_as_dict(report))


def navigation_certification_report_from_dict(
    value: Mapping[str, object],
) -> NavigationCertificationReport:
    if not isinstance(value, Mapping):
        raise TypeError("Navigation Certification Report must be a mapping")
    expected_fields = {
        "certification_id",
        "certification_integrity",
        "schema_version",
        "gate_id",
        "gate_version",
        "navigation_id",
        "navigation_ref",
        "construction_id",
        "construction_ref",
        "conformance_report_id",
        "conformance_report_ref",
        "relation_set_ref",
        "relations_certification_ref",
        "structural_summary_ref",
        "structural_statistics_ref",
        "frozen_contracts",
        "status",
        "certified",
        "checks",
        "errors",
        "navigation_replay_byte_identical",
        "construction_replay_byte_identical",
        "conformance_report_replay_byte_identical",
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
        raise ValueError("Navigation Certification fields do not match WP21")
    frozen = value["frozen_contracts"]
    checks = value["checks"]
    errors = value["errors"]
    if not isinstance(frozen, (tuple, list)):
        raise TypeError("frozen_contracts must be ordered")
    if not isinstance(checks, (tuple, list)):
        raise TypeError("checks must be ordered")
    if not isinstance(errors, (tuple, list)):
        raise TypeError("errors must be ordered")
    contracts = tuple(
        item
        if isinstance(item, FrozenNavigationContract)
        else FrozenNavigationContract(**item)
        for item in frozen
    )
    return NavigationCertificationReport(
        **{
            key: item
            for key, item in value.items()
            if key not in {"frozen_contracts", "checks", "errors"}
        },
        frozen_contracts=contracts,
        checks=tuple(checks),
        errors=tuple(errors),
    )


__all__: tuple[str, ...] = ()
