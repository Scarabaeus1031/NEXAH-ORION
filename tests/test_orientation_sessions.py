"""Documentation-backed Phase 6C Orientation Session conformance tests."""

from __future__ import annotations

from pathlib import Path
import unittest

from orion.lyra import (
    CANONICAL_ORIENTATION_VOCABULARY,
    ClarificationRequired,
    HumanLanguageRequest,
    LyraExplainer,
    LyraTranslator,
    OrientationIntent,
    UnknownRepresentation,
    UnsupportedIntent,
)
from orion.lyra_execution import LyraOrientationExecutor
from orion.transformation_engine import OrientationObject, RepresentationRef


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SESSIONS_ROOT = REPOSITORY_ROOT / "docs" / "orientation_sessions"
REQUIRED_SECTIONS = (
    "## Human Request",
    "## LYRA Translation",
    "## ORION Input",
    "## ORION Result",
    "## LYRA Explanation",
    "## Boundary Check",
)
SESSION_CASES = {
    "alternatives/registered_alternatives.md": "alternatives",
    "blockers/blocked_route.md": "blocked",
    "blockers/missing_operator.md": "missing_operator",
    "blockers/missing_renderer.md": "missing_renderer",
    "blockers/unknown_representation.md": "unknown_representation",
    "canonical/clarification_required.md": "clarification",
    "canonical/full_round_trip.md": "full_round_trip",
    "canonical/unsupported_vocabulary.md": "unsupported",
    "comparison/report_comparison.md": "comparison",
    "explanation/planned_identity.md": "planned_identity",
    "inspection/report_metadata.md": "inspection",
    "navigation/existing_route.md": "navigation",
    "validation/validation_outcome.md": "validation",
}


def orientation(representation_type: str) -> OrientationObject:
    return OrientationObject(
        orientation_object_id="session-object-1",
        orientation_object_version="orientation-object/1",
        representation=RepresentationRef(
            representation_id="session-representation-1",
            representation_type=representation_type,
            representation_version="representation/1",
            coordinate_profile="coordinate-profile/1",
        ),
        source_references=("source:session",),
        provenance=("source:session@revision-1",),
        epoch="epoch-session",
        known_constants=("constant:session",),
    )


def human_request(utterance: str, source: str) -> HumanLanguageRequest:
    return HumanLanguageRequest(utterance, orientation(source))


class OrientationSessionDocumentationTests(unittest.TestCase):
    def test_index_and_conformance_cases_cover_every_session(self) -> None:
        documented = {
            path.relative_to(SESSIONS_ROOT).as_posix()
            for path in SESSIONS_ROOT.rglob("*.md")
            if path.name != "README.md"
        }
        self.assertEqual(documented, set(SESSION_CASES))

        index = (SESSIONS_ROOT / "README.md").read_text(encoding="utf-8")
        for relative_path in sorted(documented):
            self.assertIn(f"]({relative_path})", index)

    def test_every_session_uses_the_canonical_document_shape(self) -> None:
        session_ids: set[str] = set()
        for relative_path in sorted(SESSION_CASES):
            text = (SESSIONS_ROOT / relative_path).read_text(encoding="utf-8")
            self.assertTrue(text.startswith("# "), relative_path)
            positions = [text.index(section) for section in REQUIRED_SECTIONS]
            self.assertEqual(positions, sorted(positions), relative_path)
            self.assertIn("- Format: `orientation-session/1`", text)
            session_line = next(
                line for line in text.splitlines() if line.startswith("- Session ID: ")
            )
            self.assertNotIn(session_line, session_ids)
            session_ids.add(session_line)


class OrientationSessionExecutionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.executor = LyraOrientationExecutor()

    def execute(self, utterance: str, source: str):
        return self.executor.execute(human_request(utterance, source))

    def stellar_calendar(self):
        return self.execute(
            "Navigate Stellar Projection → Calendar Projection",
            "Stellar Projection",
        )

    def test_every_documented_session_executes_its_expected_scenario(self) -> None:
        for relative_path, scenario in sorted(SESSION_CASES.items()):
            with self.subTest(session=relative_path):
                getattr(self, f"assert_{scenario}")()

    def assert_full_round_trip(self) -> None:
        interaction = self.execute(
            "I want to understand how this observation reaches the calendar.",
            "Observation",
        )
        self.assertEqual(interaction.report.status, "blocked")
        self.assertEqual(
            interaction.report.plan.transition_ids,
            ("T02", "T04", "T06", "T08", "T11", "T13"),
        )
        self.assert_round_trip_fields(interaction)

    def assert_navigation(self) -> None:
        interaction = self.stellar_calendar()
        self.assertEqual(interaction.report.plan.transition_ids, ("T13",))
        self.assertEqual(
            interaction.report.plan.alternative_paths,
            (("T12", "T14"),),
        )
        self.assert_round_trip_fields(interaction)

    def assert_planned_identity(self) -> None:
        interaction = self.execute(
            "Navigate Observation → Observation",
            "Observation",
        )
        self.assertEqual(interaction.report.status, "planned")
        self.assertTrue(interaction.report.validation.valid)
        self.assertEqual(interaction.report.plan.transition_ids, ())
        self.assertEqual(interaction.report.issues, ())
        self.assert_round_trip_fields(interaction)

    def assert_blocked(self) -> None:
        interaction = self.execute(
            "Navigate Observation → Calendar Projection",
            "Observation",
        )
        self.assertEqual(interaction.report.status, "blocked")
        self.assertEqual(len(interaction.report.issues), 12)
        self.assertEqual(len(interaction.report.plan.alternative_paths), 7)
        self.assert_round_trip_fields(interaction)

    def assert_missing_operator(self) -> None:
        interaction = self.stellar_calendar()
        self.assertIn("MissingOperator", {issue.kind for issue in interaction.report.issues})
        self.assertIn("Missing Operator at T13", interaction.explanation.text)
        self.assert_round_trip_fields(interaction)

    def assert_missing_renderer(self) -> None:
        interaction = self.stellar_calendar()
        self.assertIn("MissingRenderer", {issue.kind for issue in interaction.report.issues})
        self.assertIn("Missing Renderer at T13", interaction.explanation.text)
        self.assert_round_trip_fields(interaction)

    def assert_unknown_representation(self) -> None:
        with self.assertRaises(UnknownRepresentation):
            LyraTranslator().translate(
                human_request(
                    "Navigate Unknown Space → Calendar Projection",
                    "Observation",
                )
            )

    def assert_clarification(self) -> None:
        with self.assertRaises(ClarificationRequired):
            LyraTranslator().translate(
                human_request("Navigate Observation", "Observation")
            )

    def assert_unsupported(self) -> None:
        with self.assertRaises(UnsupportedIntent):
            LyraTranslator().translate(
                human_request("Discover a magical route", "Observation")
            )

    def assert_comparison(self) -> None:
        self.assert_report_view_intent(OrientationIntent.COMPARE)
        planned = self.execute(
            "Navigate Observation → Observation",
            "Observation",
        )
        blocked = self.stellar_calendar()
        comparison = (
            planned.report.status,
            planned.report.validation.valid,
            blocked.report.status,
            blocked.report.validation.valid,
            blocked.report.plan.transition_ids,
        )
        self.assertEqual(comparison, ("planned", True, "blocked", False, ("T13",)))
        self.assert_round_trip_fields(planned)
        self.assert_round_trip_fields(blocked)

    def assert_inspection(self) -> None:
        self.assert_report_view_intent(OrientationIntent.INSPECT)
        interaction = self.stellar_calendar()
        report = interaction.report
        self.assertEqual(
            report.plan.graph_version,
            "orientation-representation-graph/0.1-draft",
        )
        self.assertEqual(report.plan.source_references, ("source:session",))
        self.assertEqual(
            report.plan.source_provenance,
            ("source:session@revision-1",),
        )
        self.assertEqual(report.plan.evidence_chain, ("E0–E1",))
        self.assert_round_trip_fields(interaction)

    def assert_validation(self) -> None:
        self.assert_report_view_intent(OrientationIntent.VALIDATE)
        interaction = self.stellar_calendar()
        self.assertFalse(interaction.report.validation.valid)
        self.assertTrue(interaction.report.validation.checks)
        self.assertTrue(interaction.report.validation.errors)
        self.assertIn("Validation summary: invalid", interaction.explanation.text)
        self.assert_round_trip_fields(interaction)

    def assert_alternatives(self) -> None:
        self.assert_report_view_intent(OrientationIntent.SHOW_ALTERNATIVES)
        interaction = self.stellar_calendar()
        self.assertEqual(
            interaction.explanation.alternatives,
            (("T12", "T14"),),
        )
        self.assertIn("Alternative paths: T12 → T14.", interaction.explanation.text)
        self.assert_round_trip_fields(interaction)

    def assert_round_trip_fields(self, interaction) -> None:
        report = interaction.report
        explanation = interaction.explanation
        self.assertIs(explanation.source_report, report)
        self.assertEqual(explanation.status, report.status)
        self.assertEqual(explanation.evidence, report.plan.evidence_chain)
        self.assertEqual(explanation.provenance, report.plan.provenance_chain)
        self.assertEqual(explanation.blockers, report.issues)
        self.assertEqual(explanation.alternatives, report.plan.alternative_paths)
        self.assertEqual(explanation.source_report.validation, report.validation)

    def assert_report_view_intent(self, intent: OrientationIntent) -> None:
        entry = next(
            entry
            for entry in CANONICAL_ORIENTATION_VOCABULARY
            if entry.intent is intent
        )
        self.assertTrue(entry.report_view)
        self.assertFalse(entry.planning_input)


if __name__ == "__main__":
    unittest.main()
