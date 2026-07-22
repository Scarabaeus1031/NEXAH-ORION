"""The thin, in-process NEXAHEDRON to ORION Gateway boundary."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Protocol

from orion.orientation_runtime import OrientationRuntime
from orion.public_contracts import (
    NO_EFFECTS,
    ORIENTATION_REQUEST_SCHEMA,
    RUNTIME_ERROR_SCHEMA,
    ClarificationResult,
    ContinuationOption,
    ContinuationPolicy,
    ContractSet,
    EvidenceReference,
    OrientationReport,
    OrientationRequest,
    PublicContract,
    RetryPolicy,
    RuntimeError,
    validate_contract_set,
    validate_evidence_reference,
    validate_orientation_request,
    validate_public_contract,
)

from .presentation import PresentationModel, map_presentation
from .translation import GatewayInputError, construct_orientation_request


class RuntimeBoundary(Protocol):
    """The public-only execution surface consumed by the Gateway."""

    def orient(
        self,
        request: OrientationRequest,
        evidence: tuple[EvidenceReference, ...] = (),
    ) -> tuple[PublicContract, ...]: ...


@dataclass(frozen=True, slots=True)
class GatewayResponse:
    """Validated public outcomes and presentation views derived from them."""

    request: OrientationRequest | None
    contracts: tuple[PublicContract, ...]
    presentation: tuple[PresentationModel, ...]


class OrientationGateway:
    """Translate, validate, invoke, validate, and map—nothing more."""

    def __init__(self, runtime: RuntimeBoundary | None = None) -> None:
        self._runtime = runtime or OrientationRuntime()

    def handle(
        self,
        payload: Mapping[str, object],
        evidence: tuple[EvidenceReference, ...] = (),
    ) -> GatewayResponse:
        """Execute one in-process request without leaking invalid objects."""

        try:
            request = construct_orientation_request(payload)
        except (GatewayInputError, TypeError, ValueError):
            return self._response(
                None,
                (self._error(None, "invalid", "contract_validation", "external_request_invalid", (), "after_user_action"),),
            )

        request_validation = validate_orientation_request(request)
        if not request_validation.valid:
            issues = tuple(issue.code for issue in request_validation.errors)
            return self._response(
                None,
                (self._error(None, "invalid", "contract_validation", "orientation_request_invalid", issues, "after_user_action"),),
            )

        try:
            evidence_errors = self._evidence_errors(evidence)
        except Exception:
            evidence_errors = ("evidence_input_invalid",)
        if evidence_errors:
            return self._response(
                request,
                (self._error(request, "invalid", "contract_validation", "evidence_reference_invalid", evidence_errors, "after_user_action"),),
            )

        try:
            outcomes = self._runtime.orient(request, evidence)
        except Exception:
            outcomes = (
                self._error(request, "internal_failure", "processing", "runtime_boundary_failure", (), "manual_review"),
            )

        if not self._valid_outcomes(request, evidence, outcomes):
            outcomes = (
                self._error(
                    request,
                    "validation_failed",
                    "report_contract_validation",
                    "runtime_outcome_invalid",
                    (),
                    "manual_review",
                ),
            )
        return self._response(request, outcomes, evidence)

    @staticmethod
    def _evidence_errors(evidence: tuple[EvidenceReference, ...]) -> tuple[str, ...]:
        errors: list[str] = []
        for item in evidence:
            if type(item) is not EvidenceReference:
                errors.append("contract_type")
                continue
            errors.extend(issue.code for issue in validate_evidence_reference(item).errors)
        return tuple(errors)

    def _valid_outcomes(
        self,
        request: OrientationRequest,
        evidence: tuple[EvidenceReference, ...],
        outcomes: tuple[PublicContract, ...],
    ) -> bool:
        if not outcomes or not all(validate_public_contract(item).valid for item in outcomes):
            return False
        supported = (ClarificationResult, OrientationReport, ContinuationOption, RuntimeError)
        if not all(type(item) in supported for item in outcomes):
            return False
        graph = ContractSet(
            requests=(request,),
            clarifications=tuple(item for item in outcomes if isinstance(item, ClarificationResult)),
            reports=tuple(item for item in outcomes if isinstance(item, OrientationReport)),
            continuations=tuple(item for item in outcomes if isinstance(item, ContinuationOption)),
            evidence=evidence,
            runtime_errors=tuple(item for item in outcomes if isinstance(item, RuntimeError)),
        )
        return validate_contract_set(graph).valid

    def _response(
        self,
        request: OrientationRequest | None,
        contracts: tuple[PublicContract, ...],
        evidence: tuple[EvidenceReference, ...] = (),
    ) -> GatewayResponse:
        valid = tuple(item for item in contracts if validate_public_contract(item).valid)
        if len(valid) != len(contracts):
            fallback = self._error(
                request,
                "internal_failure",
                "processing",
                "gateway_publication_failure",
                (),
                "manual_review",
            )
            valid = (fallback,)
        return GatewayResponse(
            request=request,
            contracts=valid,
            presentation=tuple(map_presentation(item, evidence) for item in valid),
        )

    @staticmethod
    def _error(
        request: OrientationRequest | None,
        kind: str,
        stage: str,
        reason: str,
        issues: tuple[str, ...],
        retry: str,
    ) -> RuntimeError:
        has_identity = request is not None
        error = RuntimeError(
            schema_version=RUNTIME_ERROR_SCHEMA,
            error_id=f"gateway-{kind}-{request.request_id if request else 'unidentified'}",
            error_version="1",
            kind=kind,  # type: ignore[arg-type]
            request_id=request.request_id if request else None,
            request_version=request.request_version if request else None,
            request_schema_version=ORIENTATION_REQUEST_SCHEMA if request else None,
            stage=stage,  # type: ignore[arg-type]
            reason_code=reason,
            issues=issues,
            result_presence="none",
            retry=RetryPolicy(retry, retry == "safe", issues),  # type: ignore[arg-type]
            continuation=ContinuationPolicy(False, (), has_identity, retry == "after_user_action"),
            consumer_behavior={
                "present_kind": True,
                "preserve_request": has_identity,
                "present_as_completed": False,
            },
            effects=NO_EFFECTS,
        )
        assert validate_public_contract(error).valid
        return error


__all__ = ["GatewayResponse", "OrientationGateway", "RuntimeBoundary"]
