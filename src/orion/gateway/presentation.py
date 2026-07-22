"""Presentation-only views derived from valid public contract outcomes."""

from __future__ import annotations

from dataclasses import dataclass

from orion.public_contracts import (
    ClarificationResult,
    ContinuationOption,
    OrientationReport,
    PublicContract,
    RuntimeError,
)


@dataclass(frozen=True, slots=True)
class PresentationModel:
    """A NEXAHEDRON-ready view that retains its public source identity."""

    source_contract_type: str
    source_identity: str
    source_version: str
    source_schema_version: str
    title: str
    summary: str
    status: str
    orientation: str | None = None
    evidence: tuple[str, ...] = ()
    continuation_suggestions: tuple[str, ...] = ()
    messages: tuple[str, ...] = ()


def map_presentation(contract: PublicContract) -> PresentationModel:
    """Map one validated runtime outcome without changing the source contract."""

    if isinstance(contract, OrientationReport):
        content = contract.mode_payload.content
        return PresentationModel(
            source_contract_type="OrientationReport",
            source_identity=contract.identity.report_id,
            source_version=contract.identity.report_version,
            source_schema_version=contract.schema_version,
            title="Orientation Report",
            summary=_display_text(
                content.get("orientation_summary"),
                "Orientation Report available.",
            ),
            status=contract.status,
            orientation=contract.orientation.mode,
            evidence=contract.evidence,
            continuation_suggestions=contract.continuations,
            messages=tuple(issue.reason for issue in contract.issues),
        )
    if isinstance(contract, ClarificationResult):
        return PresentationModel(
            source_contract_type="ClarificationResult",
            source_identity=contract.result_id,
            source_version=contract.result_version,
            source_schema_version=contract.schema_version,
            title="Clarification Required",
            summary="More information is required before orientation can begin.",
            status=contract.readiness,
            orientation=contract.mode,
            messages=tuple(issue.reason for issue in contract.issues),
        )
    if isinstance(contract, ContinuationOption):
        return PresentationModel(
            source_contract_type="ContinuationOption",
            source_identity=contract.option_id,
            source_version=contract.option_version,
            source_schema_version=contract.schema_version,
            title="Continue Orientation",
            summary=_humanize(contract.action_type),
            status=contract.availability,
            orientation=contract.target_mode,
            evidence=contract.preserved_context.evidence_refs,
            continuation_suggestions=(
                f"{contract.option_id}@{contract.option_version}",
            ),
            messages=tuple(blocker.required_resolution for blocker in contract.blockers),
        )
    if isinstance(contract, RuntimeError):
        return PresentationModel(
            source_contract_type="RuntimeError",
            source_identity=contract.error_id,
            source_version=contract.error_version,
            source_schema_version=contract.schema_version,
            title=_humanize(contract.kind),
            summary=_humanize(contract.reason_code),
            status=contract.kind,
            continuation_suggestions=contract.continuation.option_refs,
            messages=contract.issues,
        )
    raise TypeError("public contract has no Gateway presentation mapping")


def _display_text(value: object, fallback: str) -> str:
    return value if isinstance(value, str) and value else fallback


def _humanize(value: str) -> str:
    return value.replace("_", " ").strip().capitalize()


__all__ = ["PresentationModel", "map_presentation"]
