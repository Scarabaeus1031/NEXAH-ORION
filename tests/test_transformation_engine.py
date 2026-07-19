"""Phase 4A tests for deterministic Transformation Graph orchestration."""

from __future__ import annotations

from dataclasses import FrozenInstanceError, replace
import unittest

from orion.transformation_contracts import (
    DEFAULT_REPRESENTATION_GRAPH,
    DEFAULT_TRANSITION_CONTRACTS,
    GraphEdge,
    RepresentationGraph,
    TransitionContractRegistry,
)
from orion.transformation_engine import (
    OrientationObject,
    RepresentationRef,
    RepresentationTarget,
    TransformationEngine,
)


def orientation(
    representation_type: str = "Stellar Projection",
) -> OrientationObject:
    return OrientationObject(
        orientation_object_id="orientation-object-1",
        orientation_object_version="orientation-object/1",
        representation=RepresentationRef(
            representation_id="representation-source-1",
            representation_type=representation_type,
            representation_version="representation/1",
            coordinate_profile="test-coordinate-profile/1",
        ),
        source_references=("source:observation-1",),
        provenance=("source:observation-1@revision-1",),
        epoch="epoch-test-1",
        known_constants=("constant:test-1",),
    )


class TransformationEngineTests(unittest.TestCase):
    def test_default_graph_and_contract_catalog_match_without_runtime_capabilities(self) -> None:
        graph_ids = tuple(
            edge.transition_id for edge in DEFAULT_REPRESENTATION_GRAPH.edges
        )
        contract_ids = tuple(
            contract.transition_id
            for contract in DEFAULT_TRANSITION_CONTRACTS.contracts
        )

        self.assertEqual(graph_ids, contract_ids)
        for edge, contract in zip(
            DEFAULT_REPRESENTATION_GRAPH.edges,
            DEFAULT_TRANSITION_CONTRACTS.contracts,
        ):
            self.assertEqual(contract.source_representation, edge.source_representation)
            self.assertEqual(contract.target_representation, edge.target_representation)
            self.assertIn(contract.operator_status, ("unknown", "candidate"))
            self.assertFalse(contract.has_executable_operator)
            self.assertFalse(contract.has_renderer)

    def test_shortest_registered_path_is_selected_deterministically(self) -> None:
        engine = TransformationEngine()

        first = engine.execute(
            orientation(),
            RepresentationTarget("Calendar Projection"),
        )
        second = engine.execute(
            orientation(),
            RepresentationTarget("Calendar Projection"),
        )

        self.assertEqual(first.plan.transition_ids, ("T13",))
        self.assertEqual(first.plan, second.plan)
        self.assertEqual(first.plan.plan_id, second.plan.plan_id)
        self.assertEqual(first.report_id, second.report_id)

    def test_multiple_registered_routes_are_reported_without_inference(self) -> None:
        report = TransformationEngine().execute(
            orientation(),
            RepresentationTarget("Calendar Projection"),
        )

        self.assertEqual(report.plan.transition_ids, ("T13",))
        self.assertIn(("T12", "T14"), report.plan.alternative_paths)

    def test_active_invariants_are_preserved_across_the_selected_path(self) -> None:
        report = TransformationEngine().execute(
            orientation("Observation"),
            RepresentationTarget("Stellar Projection"),
        )

        self.assertEqual(
            report.plan.required_invariants,
            (
                "identity",
                "provenance",
                "orientation_object_id",
                "source_references",
                "epoch",
                "known_constants",
            ),
        )
        self.assertEqual(
            report.plan.preserved_invariants,
            report.plan.required_invariants,
        )
        self.assertFalse(
            any(issue.kind == "InvariantViolation" for issue in report.issues)
        )

    def test_provenance_chain_preserves_object_and_source_references(self) -> None:
        source = orientation()
        report = TransformationEngine().execute(
            source,
            RepresentationTarget("Orientation Layer"),
        )

        self.assertEqual(report.plan.orientation_object_id, source.orientation_object_id)
        self.assertEqual(report.plan.source_references, source.source_references)
        self.assertEqual(report.plan.source_provenance, source.provenance)
        self.assertEqual(
            tuple(step.transition_id for step in report.plan.provenance_chain),
            report.plan.transition_ids,
        )
        self.assertEqual(
            tuple(step.sequence for step in report.plan.provenance_chain),
            tuple(range(1, len(report.plan.path) + 1)),
        )

    def test_contract_endpoint_incompatibility_is_reported(self) -> None:
        graph = RepresentationGraph(
            edges=(GraphEdge("T13", "Stellar Projection", "Calendar Projection"),)
        )
        original = DEFAULT_TRANSITION_CONTRACTS.get("T13")
        assert original is not None
        incompatible = replace(original, source_representation="Observation")
        engine = TransformationEngine(
            graph=graph,
            contracts=TransitionContractRegistry((incompatible,)),
        )

        report = engine.execute(
            orientation(),
            RepresentationTarget("Calendar Projection"),
        )

        self.assertTrue(
            any(issue.kind == "ContractIncompatible" for issue in report.issues)
        )

    def test_unsupported_direction_returns_no_fabricated_path(self) -> None:
        report = TransformationEngine().execute(
            orientation(),
            RepresentationTarget("Reality"),
        )

        self.assertEqual(report.plan.transition_ids, ())
        self.assertEqual(report.plan.alternative_paths, ())
        self.assertEqual(report.status, "blocked")
        self.assertEqual(tuple(issue.kind for issue in report.issues), ("UnsupportedPath",))

    def test_missing_contract_stops_the_registered_edge(self) -> None:
        engine = TransformationEngine(
            graph=RepresentationGraph(
                edges=(GraphEdge("T13", "Stellar Projection", "Calendar Projection"),)
            ),
            contracts=TransitionContractRegistry(()),
        )

        report = engine.execute(
            orientation(),
            RepresentationTarget("Calendar Projection"),
        )

        self.assertEqual(report.plan.transition_ids, ("T13",))
        self.assertEqual(tuple(issue.kind for issue in report.issues), ("MissingContract",))
        self.assertEqual(report.plan.evidence_chain, ("unknown",))

    def test_missing_operator_and_renderer_include_evidence_and_reason(self) -> None:
        report = TransformationEngine().execute(
            orientation(),
            RepresentationTarget("Calendar Projection"),
        )

        self.assertEqual(report.status, "blocked")
        issues = {issue.kind: issue for issue in report.issues}
        self.assertEqual(issues["MissingOperator"].transition_id, "T13")
        self.assertEqual(issues["MissingOperator"].evidence_level, "E0–E1")
        self.assertIn("candidate", issues["MissingOperator"].reason)
        self.assertEqual(issues["MissingRenderer"].evidence_level, "E0–E1")
        self.assertIn("Calendar/Temporal Renderer", issues["MissingRenderer"].reason)

    def test_evidence_is_propagated_in_path_order(self) -> None:
        report = TransformationEngine().execute(
            orientation(),
            RepresentationTarget("Orientation Layer"),
        )

        self.assertEqual(report.plan.transition_ids, ("T13", "T15"))
        self.assertEqual(report.plan.evidence_chain, ("E0–E1", "E1"))
        self.assertEqual(
            tuple(step.evidence_level for step in report.plan.provenance_chain),
            report.plan.evidence_chain,
        )

    def test_contract_version_compatibility_is_checked(self) -> None:
        graph = RepresentationGraph(
            edges=(GraphEdge("T13", "Stellar Projection", "Calendar Projection"),)
        )
        original = DEFAULT_TRANSITION_CONTRACTS.get("T13")
        assert original is not None
        versioned = replace(
            original,
            supported_source_versions=("stellar/2",),
            target_representation_version="calendar/2",
        )
        engine = TransformationEngine(
            graph=graph,
            contracts=TransitionContractRegistry((versioned,)),
        )

        report = engine.execute(
            orientation(),
            RepresentationTarget("Calendar Projection", "calendar/1"),
        )

        incompatible_reasons = tuple(
            issue.reason
            for issue in report.issues
            if issue.kind == "ContractIncompatible"
        )
        self.assertEqual(len(incompatible_reasons), 2)
        self.assertTrue(any("source version" in reason for reason in incompatible_reasons))
        self.assertTrue(any("requested version" in reason for reason in incompatible_reasons))

    def test_invariant_violation_is_explicit(self) -> None:
        graph = RepresentationGraph(
            edges=(GraphEdge("T13", "Stellar Projection", "Calendar Projection"),)
        )
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
        engine = TransformationEngine(
            graph=graph,
            contracts=TransitionContractRegistry((unsafe,)),
        )

        report = engine.execute(
            orientation(),
            RepresentationTarget("Calendar Projection"),
        )

        invariant_issue = next(
            issue for issue in report.issues if issue.kind == "InvariantViolation"
        )
        self.assertIn("provenance", invariant_issue.reason)
        self.assertNotIn("provenance", report.plan.preserved_invariants)

    def test_plan_and_report_are_immutable_and_produce_no_representation(self) -> None:
        report = TransformationEngine().execute(
            orientation(),
            RepresentationTarget("Calendar Projection"),
        )

        with self.assertRaises(FrozenInstanceError):
            report.status = "planned"  # type: ignore[misc]
        with self.assertRaises(FrozenInstanceError):
            report.plan.path = ()  # type: ignore[misc]
        self.assertIsNone(report.produced_representation)


if __name__ == "__main__":
    unittest.main()
