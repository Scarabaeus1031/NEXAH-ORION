"""Internal Runtime Readiness Alpha probe.

This module executes the existing Runtime-owned pre-processing checks and
stops at the first processing operation.  It does not add a public readiness
outcome, alter Runtime behavior, or invoke an Orientation result path.
"""

from __future__ import annotations

from dataclasses import dataclass

from orion.orientation_runtime.runtime import OrientationRuntime
from orion.public_contracts import OrientationRequest, validate_orientation_request


READINESS_DIAGNOSTIC_VERSION = "0.1-alpha"
READY_CHECKS = (
    "contract_validation:valid",
    "mode_support:supported",
    "clarification:none",
    "source_access:available",
)


class _ProcessingBoundaryReached(RuntimeError):
    """Sentinel proving that all existing readiness branches were passed."""


class _ReadinessProbe(OrientationRuntime):
    """Existing Runtime execution with a hard stop before processing."""

    def _report_id(self, request: OrientationRequest) -> str:
        raise _ProcessingBoundaryReached


@dataclass(frozen=True, slots=True)
class RuntimeReadinessDiagnostic:
    """Internal proof artifact; never a public Runtime result."""

    diagnostic_version: str
    request_id: str
    request_version: str
    request_schema_version: str
    mode: str
    decision: str
    checks: tuple[str, ...]
    stop: str


def prove_runtime_readiness(
    request: OrientationRequest,
) -> RuntimeReadinessDiagnostic:
    """Prove one validated request reaches, but does not enter, processing."""

    validation = validate_orientation_request(request)
    if not validation.valid:
        raise ValueError("Runtime Readiness Alpha requires a valid request")

    probe = _ReadinessProbe()
    try:
        outcomes = probe._orient(request, ())
    except _ProcessingBoundaryReached:
        return RuntimeReadinessDiagnostic(
            diagnostic_version=READINESS_DIAGNOSTIC_VERSION,
            request_id=request.request_id,
            request_version=request.request_version,
            request_schema_version=request.schema_version,
            mode=request.mode,
            decision="ready",
            checks=READY_CHECKS,
            stop="before_processing",
        )

    outcome_names = ", ".join(type(outcome).__name__ for outcome in outcomes)
    raise ValueError(
        "request did not reach the processing boundary"
        + (f": {outcome_names}" if outcome_names else "")
    )


__all__: tuple[str, ...] = ()
