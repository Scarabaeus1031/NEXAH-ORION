"""External observational Expression Conformance for Slice IV WP28.

WP28 observes one supplied WP26 Expression Contract and one supplied WP27
Expression Artifact. It constructs, repairs, normalizes, completes, certifies,
interprets, presents, or executes nothing.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
import re
from typing import Mapping

from orion.expression_construction_alpha import (
    CONSTRUCTION_STATE,
    EXPRESSION_ARTIFACT_SCHEMA_VERSION,
    RESPONSIBILITY as CONSTRUCTION_RESPONSIBILITY,
    STOP_AFTER_EXPRESSION_CONSTRUCTION,
    ExpressionArtifact,
    canonical_expression_artifact_bytes,
    expression_artifact_from_dict,
)
from orion.expression_contract_alpha import (
    EXPRESSION_CONTRACT_SCHEMA_VERSION,
    EXPRESSION_CONTRACT_VERSION,
    RESPONSIBILITY as CONTRACT_RESPONSIBILITY,
    STATUS as CONTRACT_STATUS,
    STOP_AT_EXPRESSION_CONTRACT,
    ExpressionContract,
    canonical_expression_contract_bytes,
    expression_contract_from_dict,
)


EXPRESSION_CONFORMANCE_SCHEMA_VERSION = (
    "orion.expression-conformance/0.1-alpha"
)
RESPONSIBILITY = "external_expression_conformance"
ACCEPTED = "accepted"
REJECTED = "rejected"
STOP_AFTER_EXPRESSION_CONFORMANCE = "after_expression_conformance"

_REPORT_ID = re.compile(r"^expression-conformance-[0-9a-f]{24}$")
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


def _observed_bytes(value: object, expected_type: type) -> bytes | None:
    if not isinstance(value, expected_type):
        return None
    try:
        return _canonical_bytes(asdict(value))
    except (AttributeError, TypeError, ValueError):
        return None


def _safe_text(value: object, fallback: str) -> str:
    return value if isinstance(value, str) and value else fallback


def _report_basis(
    *,
    expression_contract_id: str,
    expression_contract_integrity: str,
    expression_contract_ref: str | None,
    expression_id: str,
    expression_integrity: str,
    expression_ref: str | None,
    valid: bool,
    decision: str,
    checks: tuple[str, ...],
    errors: tuple[str, ...],
    accepted_expression_ref: str | None,
    inputs_unchanged: bool,
) -> dict[str, object]:
    return {
        "schema_version": EXPRESSION_CONFORMANCE_SCHEMA_VERSION,
        "expression_contract_id": expression_contract_id,
        "expression_contract_integrity": expression_contract_integrity,
        "expression_contract_ref": expression_contract_ref,
        "expression_id": expression_id,
        "expression_integrity": expression_integrity,
        "expression_ref": expression_ref,
        "valid": valid,
        "decision": decision,
        "checks": checks,
        "errors": errors,
        "accepted_expression_ref": accepted_expression_ref,
        "inputs_unchanged": inputs_unchanged,
        "responsibility": RESPONSIBILITY,
        "stop": STOP_AFTER_EXPRESSION_CONFORMANCE,
    }


@dataclass(frozen=True, slots=True)
class ExpressionConformanceReport:
    """Immutable external observation of one Expression Artifact."""

    report_id: str
    schema_version: str
    expression_contract_id: str
    expression_contract_integrity: str
    expression_contract_ref: str | None
    expression_id: str
    expression_integrity: str
    expression_ref: str | None
    valid: bool
    decision: str
    checks: tuple[str, ...]
    errors: tuple[str, ...]
    accepted_expression_ref: str | None
    inputs_unchanged: bool
    responsibility: str
    stop: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "checks", tuple(self.checks))
        object.__setattr__(self, "errors", tuple(self.errors))
        if _REPORT_ID.fullmatch(self.report_id) is None:
            raise ValueError("report_id is not canonical")
        if self.schema_version != EXPRESSION_CONFORMANCE_SCHEMA_VERSION:
            raise ValueError("Expression Conformance schema changed")
        for field_name in ("expression_contract_id", "expression_id"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value:
                raise ValueError(f"{field_name} must be observed exact text")
        for field_name in (
            "expression_contract_integrity",
            "expression_integrity",
        ):
            value = getattr(self, field_name)
            if _SHA256_HEX.fullmatch(value) is None:
                raise ValueError(f"{field_name} must be observed SHA-256")
        for field_name in (
            "expression_contract_ref",
            "expression_ref",
            "accepted_expression_ref",
        ):
            value = getattr(self, field_name)
            if value is not None and _SHA256_REF.fullmatch(value) is None:
                raise ValueError(f"{field_name} must be a SHA-256 reference")
        if type(self.valid) is not bool:
            raise TypeError("valid must be boolean")
        if self.decision not in (ACCEPTED, REJECTED):
            raise ValueError("decision is outside conformance vocabulary")
        if self.valid != (self.decision == ACCEPTED):
            raise ValueError("valid and decision differ")
        if self.valid != (not self.errors):
            raise ValueError("valid and errors differ")
        if any(not isinstance(item, str) or not item for item in self.checks):
            raise ValueError("checks must be deterministic non-empty labels")
        if any(not isinstance(item, str) or not item for item in self.errors):
            raise ValueError("errors must be deterministic non-empty text")
        if self.valid:
            if self.accepted_expression_ref != self.expression_ref:
                raise ValueError("accepted Expression differs from input")
        elif self.accepted_expression_ref is not None:
            raise ValueError("rejected report cannot accept Expression")
        if type(self.inputs_unchanged) is not bool or not self.inputs_unchanged:
            raise ValueError("Conformance must leave every input unchanged")
        if self.responsibility != RESPONSIBILITY:
            raise ValueError("Expression Conformance responsibility changed")
        if self.stop != STOP_AFTER_EXPRESSION_CONFORMANCE:
            raise ValueError("WP28 STOP boundary changed")
        basis = _report_basis(
            expression_contract_id=self.expression_contract_id,
            expression_contract_integrity=(
                self.expression_contract_integrity
            ),
            expression_contract_ref=self.expression_contract_ref,
            expression_id=self.expression_id,
            expression_integrity=self.expression_integrity,
            expression_ref=self.expression_ref,
            valid=self.valid,
            decision=self.decision,
            checks=self.checks,
            errors=self.errors,
            accepted_expression_ref=self.accepted_expression_ref,
            inputs_unchanged=self.inputs_unchanged,
        )
        if self.report_id != (
            f"expression-conformance-{_digest(basis)[:24]}"
        ):
            raise ValueError("report_id differs from its observations")


def validate_expression_conformance(
    contract: object,
    artifact: object,
) -> ExpressionConformanceReport:
    """Observe exact WP26 and WP27 artifacts and return a report only."""

    checks: list[str] = []
    errors: list[str] = []

    def check(name: str, condition: bool, error: str) -> None:
        checks.append(name)
        if not condition:
            errors.append(error)

    before = (
        _observed_bytes(contract, ExpressionContract),
        _observed_bytes(artifact, ExpressionArtifact),
    )
    contract_bytes, artifact_bytes = before
    contract_ref = (
        _artifact_ref(contract_bytes) if contract_bytes is not None else None
    )
    artifact_ref = (
        _artifact_ref(artifact_bytes) if artifact_bytes is not None else None
    )

    contract_type = isinstance(contract, ExpressionContract)
    artifact_type = isinstance(artifact, ExpressionArtifact)
    check(
        "expression_contract_type",
        contract_type,
        "Input is not immutable WP26 Expression Contract",
    )
    check(
        "expression_artifact_type",
        artifact_type,
        "Input is not immutable WP27 Expression Artifact",
    )

    def shape_is_valid(value: object, valid_type: bool) -> bool:
        if not valid_type:
            return False
        try:
            value.__post_init__()
            return True
        except (AttributeError, TypeError, ValueError):
            return False

    contract_shape = shape_is_valid(contract, contract_type)
    artifact_shape = shape_is_valid(artifact, artifact_type)
    check(
        "expression_contract_shape",
        contract_shape,
        "Expression Contract schema, identity, integrity, or STOP is malformed",
    )
    check(
        "expression_artifact_shape",
        artifact_shape,
        "Expression Artifact schema, identity, integrity, or STOP is malformed",
    )

    contract_authority = (
        contract_shape
        and contract.schema_version == EXPRESSION_CONTRACT_SCHEMA_VERSION
        and contract.contract_version == EXPRESSION_CONTRACT_VERSION
        and contract.status == CONTRACT_STATUS
        and contract.responsibility == CONTRACT_RESPONSIBILITY
        and contract.stop == STOP_AT_EXPRESSION_CONTRACT
    )
    check(
        "expression_contract_authority",
        contract_authority,
        "Expression Contract differs from frozen WP26 authority",
    )
    construction_state = (
        artifact_shape
        and artifact.schema_version == EXPRESSION_ARTIFACT_SCHEMA_VERSION
        and artifact.construction_state == CONSTRUCTION_STATE
        and artifact.responsibility == CONSTRUCTION_RESPONSIBILITY
        and artifact.stop == STOP_AFTER_EXPRESSION_CONSTRUCTION
        and not artifact.externally_conformant
    )
    check(
        "expression_construction_state",
        construction_state,
        "Expression Artifact differs from frozen WP27 candidate state",
    )

    exact_contract_reference = (
        contract_shape
        and artifact_shape
        and artifact.expression_contract_id == contract.contract_id
        and artifact.expression_contract_integrity
        == contract.contract_integrity
        and artifact.expression_contract_ref == contract_ref
        and artifact.expression_contract_schema_version
        == contract.schema_version
        and artifact.expression_contract_version
        == contract.contract_version
        and artifact.expression_contract_status == contract.status
    )
    check(
        "exact_contract_reference",
        exact_contract_reference,
        "Expression Artifact does not name the exact WP26 Contract",
    )
    exact_slice_iii_lineage = (
        contract_shape
        and artifact_shape
        and artifact.slice_iii_certification_ref
        == contract.slice_iii_certification_ref
        and artifact.orientation_map_conformance_ref
        == contract.orientation_map_conformance_ref
        and artifact.orientation_map_id == contract.orientation_map_id
        and artifact.orientation_map_ref == contract.orientation_map_ref
        and artifact.orientation_map_construction_id
        == contract.orientation_map_construction_id
        and artifact.orientation_map_construction_ref
        == contract.orientation_map_construction_ref
    )
    check(
        "exact_slice_iii_lineage",
        exact_slice_iii_lineage,
        "Expression Artifact changed certified Slice III references",
    )
    provenance_preserved = (
        contract_shape
        and artifact_shape
        and artifact.provenance_ref == contract.provenance_ref
        and artifact.provenance_ref
        == artifact.slice_iii_certification_ref
    )
    check(
        "provenance_preserved",
        provenance_preserved,
        "Expression Artifact changed certified provenance",
    )
    declarations_preserved = (
        contract_shape
        and artifact_shape
        and artifact.communicative_scope == contract.communicative_scope
        and artifact.declared_lossiness == contract.declared_lossiness
        and artifact.declared_exclusions == contract.declared_exclusions
    )
    check(
        "declarations_preserved",
        declarations_preserved,
        "Expression scope, lossiness, or exclusions changed",
    )
    canonical_order_preserved = (
        artifact_shape
        and artifact.canonical_order == 0
        and artifact.communicative_scope
        == tuple(sorted(set(artifact.communicative_scope)))
        and artifact.declared_lossiness
        == tuple(sorted(set(artifact.declared_lossiness)))
        and artifact.declared_exclusions
        == tuple(sorted(set(artifact.declared_exclusions)))
    )
    check(
        "canonical_order_preserved",
        canonical_order_preserved,
        "Expression Artifact ordering or declarations are not canonical",
    )

    contract_serialization = False
    if contract_shape and contract_bytes is not None:
        try:
            contract_round_trip = expression_contract_from_dict(
                asdict(contract)
            )
            contract_serialization = (
                canonical_expression_contract_bytes(contract)
                == contract_bytes
                and canonical_expression_contract_bytes(contract_round_trip)
                == contract_bytes
            )
        except (AttributeError, TypeError, ValueError):
            contract_serialization = False
    check(
        "contract_serialization_canonical",
        contract_serialization,
        "Expression Contract serialization is not canonical",
    )
    artifact_serialization = False
    if artifact_shape and artifact_bytes is not None:
        try:
            artifact_round_trip = expression_artifact_from_dict(
                asdict(artifact)
            )
            artifact_serialization = (
                canonical_expression_artifact_bytes(artifact)
                == artifact_bytes
                and canonical_expression_artifact_bytes(artifact_round_trip)
                == artifact_bytes
            )
        except (AttributeError, TypeError, ValueError):
            artifact_serialization = False
    check(
        "artifact_serialization_canonical",
        artifact_serialization,
        "Expression Artifact serialization is not canonical",
    )

    forbidden_fields = {
        "text",
        "rendered_text",
        "generated_language",
        "prompt",
        "provider",
        "model",
        "template",
        "html",
        "markdown",
        "ui",
        "visualization",
        "graphics",
        "report",
        "interpretation",
        "meaning",
        "reasoning",
        "recommendation",
        "action",
        "runtime",
        "gateway",
        "presentation",
        "certification",
    }
    contract_fields = set(asdict(contract)) if contract_type else set()
    artifact_fields = set(asdict(artifact)) if artifact_type else set()
    no_unexpected_authority = not (
        forbidden_fields & (contract_fields | artifact_fields)
    )
    check(
        "unexpected_authority_absent",
        no_unexpected_authority,
        "Expression inputs contain unexpected payload or authority",
    )

    after = (
        _observed_bytes(contract, ExpressionContract),
        _observed_bytes(artifact, ExpressionArtifact),
    )
    inputs_unchanged = before == after
    check(
        "inputs_unchanged",
        inputs_unchanged,
        "External Expression Conformance modified a supplied artifact",
    )

    valid = not errors
    decision = ACCEPTED if valid else REJECTED
    accepted_expression_ref = artifact_ref if valid else None
    contract_id = _safe_text(
        getattr(contract, "contract_id", None),
        "unavailable-expression-contract",
    )
    contract_integrity = _safe_text(
        getattr(contract, "contract_integrity", None),
        "0" * 64,
    )
    if _SHA256_HEX.fullmatch(contract_integrity) is None:
        contract_integrity = "0" * 64
    expression_id = _safe_text(
        getattr(artifact, "expression_id", None),
        "unavailable-expression",
    )
    expression_integrity = _safe_text(
        getattr(artifact, "expression_integrity", None),
        "0" * 64,
    )
    if _SHA256_HEX.fullmatch(expression_integrity) is None:
        expression_integrity = "0" * 64
    basis = _report_basis(
        expression_contract_id=contract_id,
        expression_contract_integrity=contract_integrity,
        expression_contract_ref=contract_ref,
        expression_id=expression_id,
        expression_integrity=expression_integrity,
        expression_ref=artifact_ref,
        valid=valid,
        decision=decision,
        checks=tuple(checks),
        errors=tuple(errors),
        accepted_expression_ref=accepted_expression_ref,
        inputs_unchanged=inputs_unchanged,
    )
    return ExpressionConformanceReport(
        report_id=f"expression-conformance-{_digest(basis)[:24]}",
        schema_version=EXPRESSION_CONFORMANCE_SCHEMA_VERSION,
        expression_contract_id=contract_id,
        expression_contract_integrity=contract_integrity,
        expression_contract_ref=contract_ref,
        expression_id=expression_id,
        expression_integrity=expression_integrity,
        expression_ref=artifact_ref,
        valid=valid,
        decision=decision,
        checks=tuple(checks),
        errors=tuple(errors),
        accepted_expression_ref=accepted_expression_ref,
        inputs_unchanged=inputs_unchanged,
        responsibility=RESPONSIBILITY,
        stop=STOP_AFTER_EXPRESSION_CONFORMANCE,
    )


def expression_conformance_report_as_dict(
    report: ExpressionConformanceReport,
) -> dict[str, object]:
    report.__post_init__()
    return asdict(report)


def canonical_expression_conformance_report_bytes(
    report: ExpressionConformanceReport,
) -> bytes:
    return _canonical_bytes(expression_conformance_report_as_dict(report))


def expression_conformance_report_from_dict(
    value: Mapping[str, object],
) -> ExpressionConformanceReport:
    if not isinstance(value, Mapping):
        raise TypeError("Expression Conformance Report must be a mapping")
    expected_fields = {
        "report_id",
        "schema_version",
        "expression_contract_id",
        "expression_contract_integrity",
        "expression_contract_ref",
        "expression_id",
        "expression_integrity",
        "expression_ref",
        "valid",
        "decision",
        "checks",
        "errors",
        "accepted_expression_ref",
        "inputs_unchanged",
        "responsibility",
        "stop",
    }
    if set(value) != expected_fields:
        raise ValueError("Expression Conformance fields do not match WP28")
    converted = dict(value)
    for field_name in ("checks", "errors"):
        field_value = converted[field_name]
        if not isinstance(field_value, (tuple, list)):
            raise TypeError(f"{field_name} must be ordered")
        converted[field_name] = tuple(field_value)
    return ExpressionConformanceReport(**converted)


__all__: tuple[str, ...] = ()
