"""Phase 5A tests for the declarative Operator Registry."""

from __future__ import annotations

from dataclasses import FrozenInstanceError, fields
import unittest

from orion.operator_registry import (
    DEFAULT_OPERATOR_REGISTRY,
    OperatorRegistry,
    OperatorSpecification,
    OperatorStatus,
)
from orion.transformation_contracts import DEFAULT_TRANSITION_CONTRACTS
from orion.transformation_engine import (
    OrientationObject,
    RepresentationRef,
    RepresentationTarget,
    TransformationEngine,
)


def orientation() -> OrientationObject:
    return OrientationObject(
        orientation_object_id="orientation-object-operator-test",
        orientation_object_version="orientation-object/1",
        representation=RepresentationRef(
            representation_id="stellar-source-1",
            representation_type="Stellar Projection",
            representation_version="representation/1",
            coordinate_profile="test-coordinate-profile/1",
        ),
        source_references=("source:operator-registry-test",),
        provenance=("source:operator-registry-test@revision-1",),
        epoch="epoch-test-1",
    )


class OperatorRegistryTests(unittest.TestCase):
    def test_registry_and_specifications_are_immutable(self) -> None:
        specification = DEFAULT_OPERATOR_REGISTRY.operators[0]

        with self.assertRaises(FrozenInstanceError):
            specification.executable = True  # type: ignore[misc]
        with self.assertRaises(FrozenInstanceError):
            DEFAULT_OPERATOR_REGISTRY.operators = ()  # type: ignore[misc]

    def test_lookup_is_exact_and_deterministic(self) -> None:
        operator_id = "orion.operator.placeholder/T13"

        first = DEFAULT_OPERATOR_REGISTRY.get(operator_id)
        second = DEFAULT_OPERATOR_REGISTRY.get(operator_id)

        self.assertIs(first, second)
        self.assertIsNotNone(first)
        self.assertIsNone(DEFAULT_OPERATOR_REGISTRY.get("missing"))
        self.assertEqual(
            DEFAULT_OPERATOR_REGISTRY.for_transition("T13"),
            (first,),
        )

    def test_catalog_covers_every_registered_transition_once(self) -> None:
        expected = tuple(
            contract.transition_id
            for contract in DEFAULT_TRANSITION_CONTRACTS.contracts
        )
        actual = tuple(
            specification.implemented_transition_ids[0]
            for specification in DEFAULT_OPERATOR_REGISTRY.operators
        )

        self.assertEqual(actual, expected)
        self.assertEqual(len(DEFAULT_OPERATOR_REGISTRY.operators), 15)
        self.assertTrue(
            all(
                len(DEFAULT_OPERATOR_REGISTRY.for_transition(transition_id)) == 1
                for transition_id in expected
            )
        )

    def test_status_lifecycle_contains_only_declared_values(self) -> None:
        self.assertEqual(
            tuple(status.value for status in OperatorStatus),
            (
                "unknown",
                "candidate",
                "documented",
                "verified",
                "experimental",
                "retired",
            ),
        )

    def test_unknown_and_candidate_statuses_match_phase_3c(self) -> None:
        by_status = {
            status: tuple(
                spec.implemented_transition_ids[0]
                for spec in DEFAULT_OPERATOR_REGISTRY.operators
                if spec.status is status
            )
            for status in OperatorStatus
        }

        self.assertEqual(
            by_status[OperatorStatus.UNKNOWN],
            ("T01", "T02", "T04", "T05", "T08", "T11", "T14"),
        )
        self.assertEqual(
            by_status[OperatorStatus.CANDIDATE],
            ("T03", "T06", "T07", "T09", "T10", "T12", "T13", "T15"),
        )
        self.assertTrue(
            all(
                not transition_ids
                for status, transition_ids in by_status.items()
                if status not in (OperatorStatus.UNKNOWN, OperatorStatus.CANDIDATE)
            )
        )

    def test_contract_version_compatibility_is_explicit(self) -> None:
        specification = DEFAULT_OPERATOR_REGISTRY.for_transition("T13")[0]

        self.assertTrue(specification.supports_contract("T13", "0.1-draft"))
        self.assertFalse(specification.supports_contract("T13", "0.2"))
        self.assertFalse(specification.supports_contract("T12", "0.1-draft"))
        self.assertFalse(specification.supports_representation("representation/1"))

    def test_phase_5a_rejects_executable_operator_metadata(self) -> None:
        template = DEFAULT_OPERATOR_REGISTRY.operators[0]
        values = {
            field.name: getattr(template, field.name)
            for field in fields(OperatorSpecification)
        }
        values["status"] = OperatorStatus.VERIFIED
        values["executable"] = True

        with self.assertRaisesRegex(ValueError, "never executable"):
            OperatorSpecification(**values)

    def test_engine_copies_registry_metadata_without_changing_route(self) -> None:
        report = TransformationEngine().execute(
            orientation(),
            RepresentationTarget("Calendar Projection"),
        )

        self.assertEqual(report.plan.transition_ids, ("T13",))
        step = report.plan.path[0]
        self.assertEqual(step.operator_id, "orion.operator.placeholder/T13")
        self.assertEqual(step.operator_version, "0.1-draft")
        self.assertEqual(step.operator_status, "candidate")
        self.assertIn("implementation owner unassigned", step.operator_owner or "")
        issue = next(item for item in report.issues if item.kind == "MissingOperator")
        self.assertIn(step.operator_id or "", issue.reason)
        self.assertIn("executable=false", issue.reason)
        self.assertIsNone(report.produced_representation)

    def test_engine_reports_absent_registry_entry_without_inference(self) -> None:
        report = TransformationEngine(operators=OperatorRegistry(())).execute(
            orientation(),
            RepresentationTarget("Calendar Projection"),
        )

        self.assertEqual(report.plan.transition_ids, ("T13",))
        issue = next(item for item in report.issues if item.kind == "MissingOperator")
        self.assertIn("no Operator Registry entry", issue.reason)
        self.assertIsNone(report.plan.path[0].operator_id)

    def test_registry_contains_metadata_only_and_no_execution_capability(self) -> None:
        for specification in DEFAULT_OPERATOR_REGISTRY.operators:
            self.assertFalse(specification.executable)
            self.assertEqual(specification.provider_dependencies, ())
            self.assertEqual(specification.renderer_dependencies, ())
            for field in fields(specification):
                self.assertFalse(callable(getattr(specification, field.name)))


if __name__ == "__main__":
    unittest.main()
