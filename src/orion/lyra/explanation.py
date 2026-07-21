"""Faithful deterministic explanations of existing Transformation Reports."""

from __future__ import annotations

from dataclasses import dataclass

from ..transformation_engine import TransformationReport
from .models import LyraExplanation


_ISSUE_LABELS = {
    "UnsupportedPath": "Unsupported",
    "MissingOperator": "Missing Operator",
    "MissingContract": "Missing Contract",
    "MissingRenderer": "Missing Renderer",
    "InvariantViolation": "Invariant Violation",
    "ContractIncompatible": "Contract Incompatible",
}


@dataclass(frozen=True, slots=True)
class LyraExplainer:
    """Project report fields into language without changing their meaning."""

    def explain(self, report: TransformationReport) -> LyraExplanation:
        if not isinstance(report, TransformationReport):
            raise TypeError("report must be a TransformationReport")

        sentences: list[str] = []
        if report.status == "planned":
            sentences.append(
                "Status: planned. Success: a deterministic planning result is available."
            )
        else:
            sentences.append("Status: blocked. The deterministic plan is blocked.")

        if report.plan.transition_ids:
            sentences.append(
                "Registered route: " + " → ".join(report.plan.transition_ids) + "."
            )
        else:
            sentences.append("Registered route: none.")

        if report.plan.alternative_paths:
            alternatives = "; ".join(
                " → ".join(path) for path in report.plan.alternative_paths
            )
            sentences.append(f"Alternative paths: {alternatives}.")
        else:
            sentences.append("Alternative paths: none.")

        for issue in report.issues:
            label = _ISSUE_LABELS.get(issue.kind, issue.kind)
            location = issue.transition_id or "request"
            sentences.append(
                f"{label} at {location}: {issue.reason} "
                f"Evidence: {issue.evidence_level}."
            )

        validation_state = "valid" if report.validation.valid else "invalid"
        sentences.append(f"Validation summary: {validation_state}.")
        sentences.append(
            "Validation checks: "
            + ("; ".join(report.validation.checks) if report.validation.checks else "none")
            + "."
        )
        sentences.append(
            "Validation errors: "
            + ("; ".join(report.validation.errors) if report.validation.errors else "none")
            + "."
        )
        sentences.append(
            "Evidence summary: "
            + (" → ".join(report.plan.evidence_chain) if report.plan.evidence_chain else "none")
            + "."
        )
        sentences.append(
            "Source references: "
            + ("; ".join(report.plan.source_references) if report.plan.source_references else "none")
            + "."
        )
        sentences.append(
            "Source provenance: "
            + ("; ".join(report.plan.source_provenance) if report.plan.source_provenance else "none")
            + "."
        )
        provenance_steps = tuple(
            f"{step.transition_id}@{step.contract_version or 'unknown'}:{step.evidence_level}"
            for step in report.plan.provenance_chain
        )
        sentences.append(
            "Transformation provenance: "
            + ("; ".join(provenance_steps) if provenance_steps else "none")
            + "."
        )
        sentences.append(
            "Required invariants: "
            + ("; ".join(report.plan.required_invariants) or "none")
            + "."
        )
        sentences.append(
            "Preserved invariants: "
            + ("; ".join(report.plan.preserved_invariants) or "none")
            + "."
        )
        if report.produced_representation is None:
            sentences.append("No target representation was produced.")

        return LyraExplanation(source_report=report, sentences=tuple(sentences))
