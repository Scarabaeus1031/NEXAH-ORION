"""Validation between untrusted reasoning output and ORION response."""

from __future__ import annotations

from .contracts import (
    ContextManifest,
    OrientationRequest,
    ReasoningResult,
    ValidationReport,
)


def validate_execution(
    request: OrientationRequest,
    context: ContextManifest,
    result: ReasoningResult,
    *,
    expected_backend_id: str,
) -> ValidationReport:
    checks: list[str] = []
    errors: list[str] = []

    _check(
        context.request_id == request.request_id,
        "context_request_matches",
        "context_request_mismatch",
        checks,
        errors,
    )
    _check(
        result.request_id == request.request_id,
        "result_request_matches",
        "result_request_mismatch",
        checks,
        errors,
    )
    _check(
        result.manifest_id == context.manifest_id,
        "result_manifest_matches",
        "result_manifest_mismatch",
        checks,
        errors,
    )
    _check(
        result.backend_id == expected_backend_id,
        "result_backend_matches",
        "result_backend_mismatch",
        checks,
        errors,
    )

    known_entries = {entry.entry_id for entry in context.entries}
    for claim in result.claims:
        _check(
            bool(claim.evidence_refs),
            f"claim_has_evidence:{claim.claim_id}",
            f"claim_has_no_evidence:{claim.claim_id}",
            checks,
            errors,
        )
        unknown = sorted(set(claim.evidence_refs) - known_entries)
        _check(
            not unknown,
            f"claim_evidence_known:{claim.claim_id}",
            f"claim_evidence_unknown:{claim.claim_id}:{','.join(unknown)}",
            checks,
            errors,
        )

    return ValidationReport(
        valid=not errors,
        checks=tuple(checks),
        errors=tuple(errors),
    )


def _check(
    condition: bool,
    success: str,
    error: str,
    checks: list[str],
    errors: list[str],
) -> None:
    if condition:
        checks.append(success)
    else:
        errors.append(error)

