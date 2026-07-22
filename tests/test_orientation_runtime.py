"""End-to-end conformance tests for the minimal Understand runtime."""

from __future__ import annotations

from dataclasses import replace
import unittest

from orion.orientation_runtime import OrientationRuntime
from orion.public_contracts import (
    ClarificationResult,
    ContinuationOption,
    ContractSet,
    EvidenceReference,
    OrientationReport,
    OrientationRequest,
    RuntimeError,
    TraceabilityTarget,
    validate_contract_set,
    validate_public_contract,
)
from orion.public_contracts.fixtures import EVIDENCE, VALID_REQUEST


PUBLIC_OUTCOME_TYPES = (
    OrientationRequest,
    ClarificationResult,
    EvidenceReference,
    OrientationReport,
    ContinuationOption,
    RuntimeError,
)


def runtime_evidence(request: OrientationRequest = VALID_REQUEST) -> EvidenceReference:
    report_id = f"report-{request.request_id}-{request.request_version}"
    return replace(
        EVIDENCE,
        evidence_id=f"evidence-{request.request_id}",
        traceability=(
            TraceabilityTarget(
                report_id,
                "1",
                "mode_payload.content.claims_and_support[0]",
                "finding-understand-01",
            ),
        ),
    )


class OrientationRuntimeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.runtime = OrientationRuntime()

    def assert_public_and_valid(self, outcomes: tuple[object, ...]) -> None:
        self.assertTrue(outcomes)
        for outcome in outcomes:
            with self.subTest(outcome=type(outcome).__name__):
                self.assertIs(type(outcome) in PUBLIC_OUTCOME_TYPES, True)
                self.assertTrue(validate_public_contract(outcome).valid)  # type: ignore[arg-type]

    def test_valid_understand_request_completes_end_to_end(self) -> None:
        evidence = runtime_evidence()

        outcomes = self.runtime.orient(VALID_REQUEST, (evidence,))

        self.assert_public_and_valid(outcomes)
        self.assertEqual(tuple(type(item) for item in outcomes), (OrientationReport, ContinuationOption))
        report, continuation = outcomes
        self.assertEqual(report.status, "complete")
        self.assertEqual(report.orientation.mode, "understand")
        self.assertEqual(continuation.source_report_id, report.identity.report_id)
        graph = ContractSet(
            requests=(VALID_REQUEST,),
            reports=(report,),
            continuations=(continuation,),
            evidence=(evidence,),
        )
        self.assertTrue(validate_contract_set(graph).valid)

    def test_missing_required_scope_returns_clarification(self) -> None:
        request = replace(
            VALID_REQUEST,
            scope=replace(VALID_REQUEST.scope, unresolved=("focus",)),
        )

        outcomes = self.runtime.orient(request)

        self.assert_public_and_valid(outcomes)
        error, clarification = outcomes
        self.assertIsInstance(error, RuntimeError)
        self.assertIsInstance(clarification, ClarificationResult)
        self.assertEqual(error.kind, "clarification_required")
        self.assertEqual(clarification.readiness, "clarification_required")
        self.assertEqual(error.result_ref, f"{clarification.result_id}@{clarification.result_version}")
        self.assertTrue(
            validate_contract_set(
                ContractSet(
                    requests=(request,),
                    clarifications=(clarification,),
                    runtime_errors=(error,),
                )
            ).valid
        )

    def test_clarification_issues_follow_canonical_priority_order(self) -> None:
        unresolved_object = replace(
            VALID_REQUEST.orientation_objects[0],
            object_version="unknown",
            source_revision="unknown",
            access_status=None,
        )
        request = replace(
            VALID_REQUEST,
            orientation_objects=(unresolved_object,),
            scope=replace(VALID_REQUEST.scope, include=(), depth=None),
        )

        error, clarification = self.runtime.orient(request)

        self.assertIsInstance(error, RuntimeError)
        self.assertIsInstance(clarification, ClarificationResult)
        self.assertEqual(
            tuple(issue.priority_tier for issue in clarification.issues),
            ("authority", "identity", "scope", "required_parameter"),
        )
        self.assertTrue(validate_public_contract(clarification).valid)

    def test_unsupported_mode_returns_public_runtime_error(self) -> None:
        request = replace(VALID_REQUEST, mode="compare")  # type: ignore[arg-type]

        outcomes = self.runtime.orient(request)

        self.assert_public_and_valid(outcomes)
        self.assertEqual(len(outcomes), 1)
        error = outcomes[0]
        self.assertIsInstance(error, RuntimeError)
        self.assertEqual(error.kind, "unsupported")
        self.assertEqual(error.stage, "readiness_validation")

    def test_restricted_object_blocks_before_processing(self) -> None:
        restricted = replace(VALID_REQUEST.orientation_objects[0], access_status="restricted")
        request = replace(VALID_REQUEST, orientation_objects=(restricted,))

        outcomes = self.runtime.orient(request)

        self.assert_public_and_valid(outcomes)
        self.assertEqual(len(outcomes), 1)
        error = outcomes[0]
        self.assertIsInstance(error, RuntimeError)
        self.assertEqual(error.kind, "blocked")
        self.assertEqual(error.stage, "readiness_validation")

    def test_missing_evidence_produces_contract_valid_blocked_report(self) -> None:
        outcomes = self.runtime.orient(VALID_REQUEST)

        self.assert_public_and_valid(outcomes)
        self.assertEqual(len(outcomes), 1)
        report = outcomes[0]
        self.assertIsInstance(report, OrientationReport)
        self.assertEqual(report.status, "blocked")
        self.assertEqual(report.process[5].state, "blocked")
        self.assertTrue(report.issues[0].blocking)
        self.assertTrue(
            validate_contract_set(
                ContractSet(requests=(VALID_REQUEST,), reports=(report,))
            ).valid
        )

    def test_successful_report_has_all_understand_stages_and_bound_evidence(self) -> None:
        evidence = runtime_evidence()

        report = self.runtime.orient(VALID_REQUEST, (evidence,))[0]

        self.assertIsInstance(report, OrientationReport)
        self.assertEqual(report.status, "complete")
        self.assertEqual(len(report.process), 11)
        self.assertTrue(all(stage.state == "completed" for stage in report.process))
        self.assertEqual(report.process[5].evidence_refs, report.evidence)
        self.assertEqual(
            tuple(
                item["evidence_ref"]
                for item in report.mode_payload.content["claims_and_support"]
            ),
            report.evidence,
        )
        self.assertEqual(
            report.mode_payload.content["suggested_continuations"],
            report.continuations,
        )

    def test_continuation_preserves_complete_report_lineage(self) -> None:
        evidence = runtime_evidence()
        report, continuation = self.runtime.orient(VALID_REQUEST, (evidence,))

        self.assertIsInstance(report, OrientationReport)
        self.assertIsInstance(continuation, ContinuationOption)
        context = continuation.preserved_context
        self.assertEqual(
            context.report_refs,
            (f"{report.identity.report_id}@{report.identity.report_version}",),
        )
        self.assertEqual(context.orientation_object_refs, report.orientation.orientation_object_refs)
        self.assertEqual(context.evidence_refs, report.evidence)
        self.assertEqual(context.scope_ref, f"{VALID_REQUEST.request_id}@1.scope")
        self.assertEqual(context.intention_ref, f"{VALID_REQUEST.request_id}@1.intention")
        self.assertEqual(context.human_authority_ref, report.orientation.human_authority_ref)

    def test_invalid_request_returns_valid_invalid_outcome(self) -> None:
        request = replace(VALID_REQUEST, effects="write")  # type: ignore[arg-type]

        outcomes = self.runtime.orient(request)

        self.assert_public_and_valid(outcomes)
        self.assertEqual(len(outcomes), 1)
        self.assertIsInstance(outcomes[0], RuntimeError)
        self.assertEqual(outcomes[0].kind, "invalid")
        self.assertEqual(outcomes[0].stage, "contract_validation")

    def test_unbound_evidence_cannot_complete_the_report(self) -> None:
        evidence = replace(
            runtime_evidence(),
            source=replace(EVIDENCE.source, source_ref="different-source"),
        )

        outcomes = self.runtime.orient(VALID_REQUEST, (evidence,))

        self.assert_public_and_valid(outcomes)
        self.assertIsInstance(outcomes[0], OrientationReport)
        self.assertEqual(outcomes[0].status, "blocked")

    def test_unexpected_boundary_failure_is_a_public_runtime_error(self) -> None:
        outcomes = self.runtime.orient(None)  # type: ignore[arg-type]

        self.assert_public_and_valid(outcomes)
        self.assertEqual(len(outcomes), 1)
        self.assertIsInstance(outcomes[0], RuntimeError)
        self.assertEqual(outcomes[0].kind, "internal_failure")
        self.assertEqual(outcomes[0].result_presence, "none")


if __name__ == "__main__":
    unittest.main()
