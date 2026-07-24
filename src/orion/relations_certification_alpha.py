"""Observational Relations Certification for Slice III WP17.

Certification consumes supplied immutable WP15 and WP16 artifacts plus their
exact Slice II Summary and Statistics. It replays canonical bytes and checks
references only. It never generates or validates a relation.
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
from orion.relation_conformance_alpha import (
    ACCEPTED,
    STOP_AFTER_RELATION_CONFORMANCE,
    RelationConformanceReport,
    canonical_relation_conformance_report_bytes,
)
from orion.understand_structural_statistics_alpha import (
    StructuralStatisticsDiagnostic,
    canonical_structural_statistics_bytes,
)
from orion.understand_structural_summary_alpha import (
    StructuralSummaryDiagnostic,
    canonical_structural_summary_bytes,
)


RELATIONS_CERTIFICATION_SCHEMA_VERSION = (
    "orion.relations-certification/0.1-alpha"
)
GATE_ID = "slice-iii-relations"
GATE_VERSION = "0.1-alpha"
PASSED = "passed"
FAILED = "failed"
RESPONSIBILITY = "relations_certification"
STOP_AT_RELATIONS_CERTIFIED = "at_relations_certified"

_CERTIFICATION_ID = re.compile(r"^relations-certification-[0-9a-f]{24}$")
_SHA256_REF = re.compile(r"^sha256:[0-9a-f]{64}$")
_SHA256_HEX = re.compile(r"^[0-9a-f]{64}$")


@dataclass(frozen=True, slots=True)
class FrozenRelationsContract:
    """One immutable implementation fingerprint certified by Gate R."""

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


FROZEN_RELATIONS_CONTRACTS = (
    FrozenRelationsContract(
        work_package="WP12",
        component="Relation Object",
        source_path="src/orion/structural_relation_alpha.py",
        sha256=(
            "32e23f75e4f4868f810ba1c9adeb5955"
            "4980c2992700b0d57b16e91da855a8c1"
        ),
    ),
    FrozenRelationsContract(
        work_package="WP13",
        component="Sequential Relations",
        source_path="src/orion/sequential_relations_alpha.py",
        sha256=(
            "47763598a0f9c06abf34f6018c47f264"
            "84d0cf13d0fb292bb9607726ee25aa18"
        ),
    ),
    FrozenRelationsContract(
        work_package="WP14",
        component="Structural Equality Relations",
        source_path="src/orion/structural_equality_relations_alpha.py",
        sha256=(
            "c53e4ba2c683b5913f9616636f9be8c6"
            "568f75aad964001a91876bc4186b83e4"
        ),
    ),
    FrozenRelationsContract(
        work_package="WP15",
        component="Declared Cross References",
        source_path="src/orion/declared_cross_references_alpha.py",
        sha256=(
            "48573342d6d907802f8867415efe1e1dc"
            "103f052a4265a9ce1c0bf2ce7300445"
        ),
    ),
    FrozenRelationsContract(
        work_package="WP16",
        component="External Relation Conformance",
        source_path="src/orion/relation_conformance_alpha.py",
        sha256=(
            "c1108687b020d33f08cc59209315db1f"
            "1b6f67fd3b268d1b7f51a88b154d0a50"
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
    relation_set_id: str,
    relation_set_ref: str | None,
    conformance_report_id: str,
    conformance_report_ref: str | None,
    structural_summary_ref: str | None,
    structural_statistics_ref: str | None,
    status: str,
    checks: tuple[str, ...],
    errors: tuple[str, ...],
    relation_set_replay_byte_identical: bool,
    conformance_report_replay_byte_identical: bool,
    stable_identifiers: bool,
    stable_hashes: bool,
    stable_serialization: bool,
    stable_canonical_ordering: bool,
    provenance_preserved: bool,
    inputs_unchanged: bool,
) -> dict[str, object]:
    return {
        "schema_version": RELATIONS_CERTIFICATION_SCHEMA_VERSION,
        "gate_id": GATE_ID,
        "gate_version": GATE_VERSION,
        "relation_set_id": relation_set_id,
        "relation_set_ref": relation_set_ref,
        "conformance_report_id": conformance_report_id,
        "conformance_report_ref": conformance_report_ref,
        "structural_summary_ref": structural_summary_ref,
        "structural_statistics_ref": structural_statistics_ref,
        "frozen_contracts": tuple(
            asdict(contract) for contract in FROZEN_RELATIONS_CONTRACTS
        ),
        "status": status,
        "checks": checks,
        "errors": errors,
        "relation_set_replay_byte_identical": (
            relation_set_replay_byte_identical
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
        "stop": STOP_AT_RELATIONS_CERTIFIED,
    }


@dataclass(frozen=True, slots=True)
class RelationsCertificationReport:
    """Immutable pass-or-fail record for the Relations Certification Gate."""

    certification_id: str
    certification_integrity: str
    schema_version: str
    gate_id: str
    gate_version: str
    relation_set_id: str
    relation_set_ref: str | None
    conformance_report_id: str
    conformance_report_ref: str | None
    structural_summary_ref: str | None
    structural_statistics_ref: str | None
    frozen_contracts: tuple[FrozenRelationsContract, ...]
    status: str
    certified: bool
    checks: tuple[str, ...]
    errors: tuple[str, ...]
    relation_set_replay_byte_identical: bool
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
            raise ValueError("certification_integrity is not SHA-256")
        if self.schema_version != RELATIONS_CERTIFICATION_SCHEMA_VERSION:
            raise ValueError("Relations Certification schema changed")
        if self.gate_id != GATE_ID or self.gate_version != GATE_VERSION:
            raise ValueError("Relations Certification gate identity changed")
        for field_name in ("relation_set_id", "conformance_report_id"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value:
                raise ValueError(f"{field_name} must be observed exact text")
        for field_name in (
            "relation_set_ref",
            "conformance_report_ref",
            "structural_summary_ref",
            "structural_statistics_ref",
        ):
            value = getattr(self, field_name)
            if value is not None and _SHA256_REF.fullmatch(value) is None:
                raise ValueError(f"{field_name} must be a SHA-256 reference")
        if self.frozen_contracts != FROZEN_RELATIONS_CONTRACTS:
            raise ValueError("frozen Relations contract fingerprints changed")
        if self.status not in (PASSED, FAILED):
            raise ValueError("status is outside the certification vocabulary")
        if type(self.certified) is not bool:
            raise TypeError("certified must be boolean")
        if self.certified != (self.status == PASSED):
            raise ValueError("certified and status differ")
        if self.certified != (not self.errors):
            raise ValueError("certified and errors differ")
        if any(
            not isinstance(check, str) or not check for check in self.checks
        ):
            raise ValueError("checks must be non-empty deterministic labels")
        if any(
            not isinstance(error, str) or not error for error in self.errors
        ):
            raise ValueError("errors must be non-empty deterministic text")
        boolean_fields = (
            "relation_set_replay_byte_identical",
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
            raise ValueError("passed certification contains a failed observation")
        if not self.inputs_unchanged:
            raise ValueError("Certification must never mutate supplied artifacts")
        if self.responsibility != RESPONSIBILITY:
            raise ValueError("Relations Certification responsibility changed")
        if self.stop != STOP_AT_RELATIONS_CERTIFIED:
            raise ValueError("Relations Certification STOP changed")
        basis = _certification_basis(
            relation_set_id=self.relation_set_id,
            relation_set_ref=self.relation_set_ref,
            conformance_report_id=self.conformance_report_id,
            conformance_report_ref=self.conformance_report_ref,
            structural_summary_ref=self.structural_summary_ref,
            structural_statistics_ref=self.structural_statistics_ref,
            status=self.status,
            checks=self.checks,
            errors=self.errors,
            relation_set_replay_byte_identical=(
                self.relation_set_replay_byte_identical
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
        if self.certification_id != f"relations-certification-{digest[:24]}":
            raise ValueError("certification_id differs from observations")
        if self.certification_integrity != digest:
            raise ValueError("certification_integrity differs from observations")


def certify_relations(
    relation_set: object,
    conformance_report: object,
    summary: object,
    statistics: object,
) -> RelationsCertificationReport:
    """Certify supplied immutable artifacts without reconstructing them."""

    checks: list[str] = []
    errors: list[str] = []

    def check(name: str, condition: bool, error: str) -> None:
        checks.append(name)
        if not condition:
            errors.append(error)

    relation_before = _observed_bytes(
        relation_set,
        DeclaredReferenceRelationSet,
    )
    conformance_before = _observed_bytes(
        conformance_report,
        RelationConformanceReport,
    )
    summary_before = _observed_bytes(summary, StructuralSummaryDiagnostic)
    statistics_before = _observed_bytes(
        statistics,
        StructuralStatisticsDiagnostic,
    )

    relation_shape = False
    if isinstance(relation_set, DeclaredReferenceRelationSet):
        try:
            relation_set.__post_init__()
            relation_shape = True
        except (AttributeError, TypeError, ValueError):
            pass
    check(
        "relation_set_immutable_shape",
        relation_shape,
        "Relation Set is malformed or not immutable",
    )

    conformance_shape = False
    if isinstance(conformance_report, RelationConformanceReport):
        try:
            conformance_report.__post_init__()
            conformance_shape = True
        except (AttributeError, TypeError, ValueError):
            pass
    check(
        "conformance_report_immutable_shape",
        conformance_shape,
        "Relation Conformance Report is malformed or not immutable",
    )

    summary_shape = False
    if isinstance(summary, StructuralSummaryDiagnostic):
        try:
            summary.__post_init__()
            summary_shape = True
        except (AttributeError, TypeError, ValueError):
            pass
    check(
        "structural_summary_immutable_shape",
        summary_shape,
        "Structural Summary is malformed or not immutable",
    )

    statistics_shape = False
    if isinstance(statistics, StructuralStatisticsDiagnostic):
        try:
            statistics.__post_init__()
            statistics_shape = True
        except (AttributeError, TypeError, ValueError):
            pass
    check(
        "structural_statistics_immutable_shape",
        statistics_shape,
        "Structural Statistics is malformed or not immutable",
    )

    relation_ref = (
        _artifact_ref(relation_before)
        if relation_before is not None
        else None
    )
    conformance_ref = (
        _artifact_ref(conformance_before)
        if conformance_before is not None
        else None
    )
    summary_ref = (
        _artifact_ref(summary_before) if summary_before is not None else None
    )
    statistics_ref = (
        _artifact_ref(statistics_before)
        if statistics_before is not None
        else None
    )

    conformance_accepted = (
        conformance_shape
        and conformance_report.valid
        and conformance_report.decision == ACCEPTED
        and conformance_report.errors == ()
        and conformance_report.accepted_relation_set_ref == relation_ref
        and conformance_report.stop == STOP_AFTER_RELATION_CONFORMANCE
    )
    check(
        "wp16_conformance_accepted",
        conformance_accepted,
        "WP16 did not accept the exact supplied Relation Set",
    )

    input_references_consistent = (
        relation_shape
        and conformance_shape
        and summary_shape
        and statistics_shape
        and conformance_report.relation_set_id == relation_set.relation_set_id
        and conformance_report.relation_set_ref == relation_ref
        and conformance_report.structural_summary_ref == summary_ref
        and conformance_report.structural_statistics_ref == statistics_ref
        and relation_set.structural_summary_ref == summary_ref
        and relation_set.structural_statistics_ref == statistics_ref
        and relation_set.input_inventory_ref
        == summary.input_inventory_ref
        == statistics.input_inventory_ref
    )
    check(
        "input_reference_consistency",
        input_references_consistent,
        "Certification inputs do not share exact immutable references",
    )

    relation_replay = False
    if relation_shape:
        try:
            relation_replay = (
                canonical_declared_reference_relation_set_bytes(relation_set)
                == canonical_declared_reference_relation_set_bytes(relation_set)
                == relation_before
            )
        except (AttributeError, TypeError, ValueError):
            pass
    check(
        "relation_set_byte_replay",
        relation_replay,
        "Relation Set canonical bytes do not replay identically",
    )

    conformance_replay = False
    if conformance_shape:
        try:
            conformance_replay = (
                canonical_relation_conformance_report_bytes(conformance_report)
                == canonical_relation_conformance_report_bytes(
                    conformance_report
                )
                == conformance_before
            )
        except (AttributeError, TypeError, ValueError):
            pass
    check(
        "conformance_report_byte_replay",
        conformance_replay,
        "Relation Conformance Report bytes do not replay identically",
    )

    stable_identifiers = (
        relation_shape
        and conformance_shape
        and conformance_report.relation_set_id == relation_set.relation_set_id
        and isinstance(relation_set.relation_set_id, str)
        and isinstance(conformance_report.report_id, str)
    )
    check(
        "stable_identifiers",
        stable_identifiers,
        "Relations identifiers are absent or inconsistent",
    )

    stable_hashes = (
        relation_ref is not None
        and conformance_ref is not None
        and summary_ref is not None
        and statistics_ref is not None
        and conformance_report.relation_set_ref == relation_ref
        if conformance_shape
        else False
    )
    check(
        "stable_hashes",
        stable_hashes,
        "Relations artifact hashes are absent or inconsistent",
    )

    stable_serialization = relation_replay and conformance_replay
    check(
        "stable_serialization",
        stable_serialization,
        "Relations serialization is not stable",
    )

    required_wp16_checks = {
        "canonical_order",
        "duplicate_absence",
        "relation_objects",
        "relation_set_input_references",
        "supplied_relation_bases",
    }
    stable_canonical_ordering = (
        conformance_accepted
        and required_wp16_checks.issubset(conformance_report.checks)
    )
    check(
        "stable_canonical_ordering",
        stable_canonical_ordering,
        "Accepted WP16 report lacks canonical ordering observations",
    )

    provenance_preserved = (
        conformance_accepted
        and {
            "slice_ii_lineage",
            "relation_set_input_references",
            "relation_objects",
            "declared_reference_bindings",
        }.issubset(conformance_report.checks)
        and input_references_consistent
    )
    check(
        "provenance_preserved",
        provenance_preserved,
        "Accepted Relations provenance is incomplete or inconsistent",
    )

    frozen_contracts_present = (
        tuple(contract.work_package for contract in FROZEN_RELATIONS_CONTRACTS)
        == ("WP12", "WP13", "WP14", "WP15", "WP16")
        and len(
            {contract.sha256 for contract in FROZEN_RELATIONS_CONTRACTS}
        )
        == len(FROZEN_RELATIONS_CONTRACTS)
    )
    check(
        "frozen_contract_fingerprints",
        frozen_contracts_present,
        "Frozen WP12-WP16 contract fingerprints are incomplete",
    )

    relation_after = _observed_bytes(
        relation_set,
        DeclaredReferenceRelationSet,
    )
    conformance_after = _observed_bytes(
        conformance_report,
        RelationConformanceReport,
    )
    summary_after = _observed_bytes(summary, StructuralSummaryDiagnostic)
    statistics_after = _observed_bytes(
        statistics,
        StructuralStatisticsDiagnostic,
    )
    inputs_unchanged = (
        relation_before == relation_after
        and conformance_before == conformance_after
        and summary_before == summary_after
        and statistics_before == statistics_after
    )
    check(
        "inputs_unchanged",
        inputs_unchanged,
        "Relations Certification changed a supplied artifact",
    )

    status = PASSED if not errors else FAILED
    relation_set_id = (
        relation_set.relation_set_id if relation_shape else "unavailable"
    )
    conformance_report_id = (
        conformance_report.report_id
        if conformance_shape
        else "unavailable"
    )
    basis = _certification_basis(
        relation_set_id=relation_set_id,
        relation_set_ref=relation_ref,
        conformance_report_id=conformance_report_id,
        conformance_report_ref=conformance_ref,
        structural_summary_ref=summary_ref,
        structural_statistics_ref=statistics_ref,
        status=status,
        checks=tuple(checks),
        errors=tuple(errors),
        relation_set_replay_byte_identical=relation_replay,
        conformance_report_replay_byte_identical=conformance_replay,
        stable_identifiers=stable_identifiers,
        stable_hashes=stable_hashes,
        stable_serialization=stable_serialization,
        stable_canonical_ordering=stable_canonical_ordering,
        provenance_preserved=provenance_preserved,
        inputs_unchanged=inputs_unchanged,
    )
    digest = _digest(basis)
    return RelationsCertificationReport(
        certification_id=f"relations-certification-{digest[:24]}",
        certification_integrity=digest,
        schema_version=RELATIONS_CERTIFICATION_SCHEMA_VERSION,
        gate_id=GATE_ID,
        gate_version=GATE_VERSION,
        relation_set_id=relation_set_id,
        relation_set_ref=relation_ref,
        conformance_report_id=conformance_report_id,
        conformance_report_ref=conformance_ref,
        structural_summary_ref=summary_ref,
        structural_statistics_ref=statistics_ref,
        frozen_contracts=FROZEN_RELATIONS_CONTRACTS,
        status=status,
        certified=not errors,
        checks=tuple(checks),
        errors=tuple(errors),
        relation_set_replay_byte_identical=relation_replay,
        conformance_report_replay_byte_identical=conformance_replay,
        stable_identifiers=stable_identifiers,
        stable_hashes=stable_hashes,
        stable_serialization=stable_serialization,
        stable_canonical_ordering=stable_canonical_ordering,
        provenance_preserved=provenance_preserved,
        inputs_unchanged=inputs_unchanged,
        responsibility=RESPONSIBILITY,
        stop=STOP_AT_RELATIONS_CERTIFIED,
    )


def relations_certification_report_as_dict(
    report: RelationsCertificationReport,
) -> dict[str, object]:
    report.__post_init__()
    return asdict(report)


def canonical_relations_certification_report_bytes(
    report: RelationsCertificationReport,
) -> bytes:
    return _canonical_bytes(relations_certification_report_as_dict(report))


def relations_certification_report_from_dict(
    value: Mapping[str, object],
) -> RelationsCertificationReport:
    if not isinstance(value, Mapping):
        raise TypeError("Relations Certification Report must be a mapping")
    expected_fields = {
        "certification_id",
        "certification_integrity",
        "schema_version",
        "gate_id",
        "gate_version",
        "relation_set_id",
        "relation_set_ref",
        "conformance_report_id",
        "conformance_report_ref",
        "structural_summary_ref",
        "structural_statistics_ref",
        "frozen_contracts",
        "status",
        "certified",
        "checks",
        "errors",
        "relation_set_replay_byte_identical",
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
        raise ValueError("Relations Certification Report fields are not exact")
    frozen_values = value["frozen_contracts"]
    checks = value["checks"]
    errors = value["errors"]
    if not isinstance(frozen_values, (list, tuple)):
        raise TypeError("frozen_contracts must be ordered")
    if not isinstance(checks, (list, tuple)):
        raise TypeError("checks must be ordered")
    if not isinstance(errors, (list, tuple)):
        raise TypeError("errors must be ordered")
    return RelationsCertificationReport(
        certification_id=value["certification_id"],
        certification_integrity=value["certification_integrity"],
        schema_version=value["schema_version"],
        gate_id=value["gate_id"],
        gate_version=value["gate_version"],
        relation_set_id=value["relation_set_id"],
        relation_set_ref=value["relation_set_ref"],
        conformance_report_id=value["conformance_report_id"],
        conformance_report_ref=value["conformance_report_ref"],
        structural_summary_ref=value["structural_summary_ref"],
        structural_statistics_ref=value["structural_statistics_ref"],
        frozen_contracts=tuple(
            FrozenRelationsContract(**dict(contract))
            for contract in frozen_values
        ),
        status=value["status"],
        certified=value["certified"],
        checks=tuple(checks),
        errors=tuple(errors),
        relation_set_replay_byte_identical=value[
            "relation_set_replay_byte_identical"
        ],
        conformance_report_replay_byte_identical=value[
            "conformance_report_replay_byte_identical"
        ],
        stable_identifiers=value["stable_identifiers"],
        stable_hashes=value["stable_hashes"],
        stable_serialization=value["stable_serialization"],
        stable_canonical_ordering=value["stable_canonical_ordering"],
        provenance_preserved=value["provenance_preserved"],
        inputs_unchanged=value["inputs_unchanged"],
        responsibility=value["responsibility"],
        stop=value["stop"],
    )


__all__: tuple[str, ...] = ()
