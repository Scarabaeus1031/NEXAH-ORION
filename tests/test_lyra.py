"""Phase 6B tests for deterministic Human → ORION → Human translation."""

from __future__ import annotations

from dataclasses import FrozenInstanceError, replace
import unittest

from orion.lyra import (
    CANONICAL_ORIENTATION_VOCABULARY,
    ClarificationRequired,
    HumanLanguageRequest,
    LyraExplainer,
    LyraTranslator,
    OrientationIntent,
    UnknownRepresentation,
    UnknownTarget,
    UnsupportedIntent,
)
from orion.lyra_execution import LyraOrientationExecutor
from orion.transformation_contracts import (
    DEFAULT_TRANSITION_CONTRACTS,
    GraphEdge,
    RepresentationGraph,
    TransitionContractRegistry,
)
from orion.transformation_engine import (
    OrientationObject,
    RepresentationRef,
    TransformationEngine,
)


def orientation(representation_type: str = "Observation") -> OrientationObject:
    return OrientationObject(
        orientation_object_id="orientation-lyra-1",
        orientation_object_version="orientation-object/1",
        representation=RepresentationRef(
            representation_id="representation-lyra-1",
            representation_type=representation_type,
            representation_version="representation/1",
            coordinate_profile="coordinate-profile/1",
        ),
        source_references=("source:lyra-test",),
        provenance=("source:lyra-test@revision-1",),
        epoch="epoch-lyra-1",
        known_constants=("constant:lyra-1",),
    )


def request(
    utterance: str,
    representation_type: str = "Observation",
) -> HumanLanguageRequest:
    return HumanLanguageRequest(utterance, orientation(representation_type))


class LyraVocabularyAndTranslationTests(unittest.TestCase):
    def test_supported_vocabulary_is_exactly_the_phase_6a_catalog(self) -> None:
        self.assertEqual(
            tuple(entry.intent.value for entry in CANONICAL_ORIENTATION_VOCABULARY),
            (
                "Observe",
                "Represent",
                "Project",
                "Navigate",
                "Compare",
                "Explain",
                "Inspect",
                "Plan",
                "Validate",
                "Why",
                "Show Alternatives",
                "What is missing?",
            ),
        )

    def test_canonical_navigation_maps_only_to_existing_runtime_inputs(self) -> None:
        human_request = request("Navigate Observation → Calendar Projection")
        translation = LyraTranslator().translate(human_request)

        self.assertEqual(translation.intents, (OrientationIntent.NAVIGATE,))
        self.assertEqual(translation.source_representation, "Observation")
        self.assertEqual(translation.target.representation_type, "Calendar Projection")
        self.assertIs(translation.request, human_request)
        self.assertIs(
            translation.request.orientation_object,
            human_request.orientation_object,
        )

    def test_documented_natural_language_example_is_deterministic(self) -> None:
        translation = LyraTranslator().translate(
            request("I want to understand how this observation reaches the calendar.")
        )

        self.assertEqual(
            translation.intents,
            (OrientationIntent.NAVIGATE, OrientationIntent.EXPLAIN),
        )
        self.assertEqual(translation.target.representation_type, "Calendar Projection")

    def test_project_and_plan_are_explicit_planning_intents(self) -> None:
        translator = LyraTranslator()
        projected = translator.translate(
            request("Project Observation -> Calendar Projection")
        )
        planned = translator.translate(
            request("Plan Observation → Calendar Projection")
        )

        self.assertEqual(projected.intents, (OrientationIntent.PROJECT,))
        self.assertEqual(planned.intents, (OrientationIntent.PLAN,))
        self.assertEqual(projected.target, planned.target)

    def test_unknown_language_returns_unsupported_intent(self) -> None:
        with self.assertRaises(UnsupportedIntent):
            LyraTranslator().translate(request("Please discover a magical route"))

    def test_known_but_incomplete_language_requires_clarification(self) -> None:
        with self.assertRaises(ClarificationRequired):
            LyraTranslator().translate(request("Navigate Observation"))
        with self.assertRaises(ClarificationRequired):
            LyraTranslator().translate(request("Explain"))

    def test_multiple_targets_require_clarification(self) -> None:
        with self.assertRaises(ClarificationRequired):
            LyraTranslator().translate(
                request(
                    "Navigate Observation → Calendar Projection → Orientation Layer"
                )
            )

    def test_unknown_source_and_target_are_distinct(self) -> None:
        translator = LyraTranslator()
        with self.assertRaises(UnknownRepresentation):
            translator.translate(request("Navigate Unknown Space → Calendar Projection"))
        with self.assertRaises(UnknownTarget):
            translator.translate(request("Navigate Observation → Unknown Target"))

    def test_known_source_must_match_supplied_orientation_object(self) -> None:
        with self.assertRaises(ClarificationRequired):
            LyraTranslator().translate(
                request(
                    "Navigate Observation → Calendar Projection",
                    "Stellar Projection",
                )
            )

    def test_language_models_are_immutable(self) -> None:
        human_request = request("Navigate Observation → Calendar Projection")
        translation = LyraTranslator().translate(human_request)

        with self.assertRaises(FrozenInstanceError):
            human_request.utterance = "changed"  # type: ignore[misc]
        with self.assertRaises(FrozenInstanceError):
            translation.intents = ()  # type: ignore[misc]


class LyraExplanationAndInteractionTests(unittest.TestCase):
    def test_complete_default_interaction_preserves_blocked_status(self) -> None:
        interaction = LyraOrientationExecutor().execute(
            request("Navigate Observation → Calendar Projection")
        )

        self.assertEqual(interaction.report.status, "blocked")
        self.assertEqual(interaction.explanation.status, "blocked")
        self.assertIn("Status: blocked", interaction.explanation.text)
        self.assertIs(interaction.explanation.source_report, interaction.report)
        self.assertIsNone(interaction.report.produced_representation)

    def test_missing_capabilities_are_explained_without_semantic_change(self) -> None:
        interaction = LyraOrientationExecutor().execute(
            request(
                "Navigate Stellar Projection → Calendar Projection",
                "Stellar Projection",
            )
        )

        kinds = tuple(issue.kind for issue in interaction.report.issues)
        self.assertIn("MissingOperator", kinds)
        self.assertIn("MissingRenderer", kinds)
        self.assertIn("Missing Operator", interaction.explanation.text)
        self.assertIn("Missing Renderer", interaction.explanation.text)
        self.assertEqual(interaction.explanation.blockers, interaction.report.issues)

    def test_missing_contract_and_invariant_violation_are_supported(self) -> None:
        graph = RepresentationGraph(
            edges=(GraphEdge("T13", "Stellar Projection", "Calendar Projection"),)
        )
        no_contract_engine = TransformationEngine(
            graph=graph,
            contracts=TransitionContractRegistry(()),
        )
        no_contract_executor = LyraOrientationExecutor(
            engine=no_contract_engine,
            translator=LyraTranslator(graph),
        )
        missing = no_contract_executor.execute(
            request(
                "Navigate Stellar Projection → Calendar Projection",
                "Stellar Projection",
            )
        )
        self.assertIn("Missing Contract", missing.explanation.text)

        original = DEFAULT_TRANSITION_CONTRACTS.get("T13")
        assert original is not None
        unsafe = replace(
            original,
            preserved_invariants=(
                "identity",
                "orientation_object_id",
                "source_references",
                "epoch",
                "known_constants",
            ),
        )
        unsafe_engine = TransformationEngine(
            graph=graph,
            contracts=TransitionContractRegistry((unsafe,)),
        )
        unsafe_interaction = LyraOrientationExecutor(
            engine=unsafe_engine,
            translator=LyraTranslator(graph),
        ).execute(
            request(
                "Navigate Stellar Projection → Calendar Projection",
                "Stellar Projection",
            )
        )
        self.assertIn("Invariant Violation", unsafe_interaction.explanation.text)
        self.assertIn("provenance", unsafe_interaction.explanation.text)

    def test_unsupported_path_is_explained_as_unsupported(self) -> None:
        interaction = LyraOrientationExecutor().execute(
            request(
                "Navigate Calendar Projection → Observation",
                "Calendar Projection",
            )
        )

        self.assertEqual(
            tuple(issue.kind for issue in interaction.report.issues),
            ("UnsupportedPath",),
        )
        self.assertIn("Unsupported at request", interaction.explanation.text)

    def test_alternatives_validation_evidence_and_provenance_survive_round_trip(self) -> None:
        interaction = LyraOrientationExecutor().execute(
            request(
                "Navigate Stellar Projection → Calendar Projection",
                "Stellar Projection",
            )
        )
        report = interaction.report
        explanation = interaction.explanation

        self.assertEqual(explanation.status, report.status)
        self.assertEqual(explanation.evidence, report.plan.evidence_chain)
        self.assertEqual(explanation.provenance, report.plan.provenance_chain)
        self.assertEqual(explanation.blockers, report.issues)
        self.assertEqual(explanation.alternatives, report.plan.alternative_paths)
        self.assertIn("T12 → T14", explanation.text)
        self.assertIn("Evidence summary: E0–E1", explanation.text)
        self.assertIn("Source provenance: source:lyra-test@revision-1", explanation.text)
        self.assertIn(
            f"Validation summary: {'valid' if report.validation.valid else 'invalid'}",
            explanation.text,
        )

    def test_successful_no_transition_plan_is_not_described_as_execution(self) -> None:
        interaction = LyraOrientationExecutor().execute(
            request("Navigate Observation → Observation")
        )

        self.assertEqual(interaction.report.status, "planned")
        self.assertTrue(interaction.report.validation.valid)
        self.assertIn("Status: planned", interaction.explanation.text)
        self.assertIn("Success: a deterministic planning result", interaction.explanation.text)
        self.assertIn("Registered route: none", interaction.explanation.text)
        self.assertIn("No target representation was produced", interaction.explanation.text)

    def test_no_report_information_disappears_from_language_projection(self) -> None:
        report = TransformationEngine().execute(
            orientation("Stellar Projection"),
            LyraTranslator().translate(
                request(
                    "Navigate Stellar Projection → Calendar Projection",
                    "Stellar Projection",
                )
            ).target,
        )
        explanation = LyraExplainer().explain(report)

        self.assertIs(explanation.source_report, report)
        self.assertEqual(explanation.source_report.plan, report.plan)
        self.assertEqual(explanation.source_report.validation, report.validation)
        self.assertEqual(explanation.source_report.issues, report.issues)


if __name__ == "__main__":
    unittest.main()
