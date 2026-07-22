"""Conformance tests for the frozen ORION Public Contract Suite 1.0."""

from __future__ import annotations

from dataclasses import replace
import unittest

from orion.public_contracts.fixtures import (
    BLOCKED_BEFORE_PROCESSING,
    BLOCKED_BEFORE_REQUEST,
    BLOCKED_REPORT,
    BLOCKED_REPORT_REQUEST,
    CANONICAL_CONTRACT_SET,
    CLARIFICATION_REQUEST,
    CLARIFICATION_REQUIRED,
    CLARIFICATION_REQUIRED_ERROR,
    COMPLETE_REPORT,
    COMPLETE_REQUEST,
    CONTINUATION,
    ERROR_REQUEST,
    EVIDENCE,
    PARTIAL_REPORT,
    PARTIAL_REQUEST,
    RUNTIME_ERROR,
    UNSUPPORTED,
    UNSUPPORTED_REQUEST,
    VALID_REQUEST,
)
from orion.public_contracts.models import Scope
from orion.public_contracts.validation import (
    ContractSet,
    validate_clarification_result,
    validate_continuation_option,
    validate_contract_set,
    validate_evidence_reference,
    validate_orientation_report,
    validate_orientation_request,
    validate_public_contract,
    validate_runtime_error,
)


def canonical_set(**changes: object) -> ContractSet:
    values = {
        "requests": (
            VALID_REQUEST,
            COMPLETE_REQUEST,
            PARTIAL_REQUEST,
            BLOCKED_REPORT_REQUEST,
            BLOCKED_BEFORE_REQUEST,
            UNSUPPORTED_REQUEST,
            ERROR_REQUEST,
            CLARIFICATION_REQUEST,
        ),
        "clarifications": (CLARIFICATION_REQUIRED,),
        "reports": (COMPLETE_REPORT, PARTIAL_REPORT, BLOCKED_REPORT),
        "continuations": (CONTINUATION,),
        "evidence": (EVIDENCE,),
        "runtime_errors": (
            UNSUPPORTED,
            BLOCKED_BEFORE_PROCESSING,
            RUNTIME_ERROR,
            CLARIFICATION_REQUIRED_ERROR,
        ),
    }
    values.update(changes)
    return ContractSet(**values)  # type: ignore[arg-type]


class CanonicalFixtureTests(unittest.TestCase):
    def test_every_canonical_fixture_is_contract_valid(self) -> None:
        for fixture in CANONICAL_CONTRACT_SET:
            with self.subTest(contract=type(fixture).__name__):
                self.assertTrue(validate_public_contract(fixture).valid)

    def test_required_fixture_outcomes_are_present(self) -> None:
        self.assertEqual({COMPLETE_REPORT.status, PARTIAL_REPORT.status, BLOCKED_REPORT.status}, {"complete", "partial", "blocked"})
        self.assertEqual(UNSUPPORTED.kind, "unsupported")
        self.assertEqual(BLOCKED_BEFORE_PROCESSING.kind, "blocked")
        self.assertEqual(CLARIFICATION_REQUIRED.readiness, "clarification_required")

    def test_canonical_fixture_graph_is_lineage_valid(self) -> None:
        self.assertTrue(validate_contract_set(canonical_set()).valid)


class OrientationRequestValidationTests(unittest.TestCase):
    def test_rejects_wrong_schema_and_effects(self) -> None:
        invalid = replace(VALID_REQUEST, schema_version="orion.orientation-request/2.0", effects="write")
        codes = {x.code for x in validate_orientation_request(invalid).errors}
        self.assertEqual(codes, {"schema_version", "effects"})

    def test_rejects_duplicate_object_identity_and_version(self) -> None:
        invalid = replace(VALID_REQUEST, orientation_objects=(VALID_REQUEST.orientation_objects[0], VALID_REQUEST.orientation_objects[0]))
        self.assertIn("duplicate", {x.code for x in validate_orientation_request(invalid).errors})

    def test_request_identity_version_is_required(self) -> None:
        invalid = replace(VALID_REQUEST, request_version="")
        self.assertFalse(validate_orientation_request(invalid).valid)


class ClarificationValidationTests(unittest.TestCase):
    def test_rejects_non_blocking_issue(self) -> None:
        issue = replace(CLARIFICATION_REQUIRED.issues[0], blocking=False)
        invalid = replace(CLARIFICATION_REQUIRED, issues=(issue, *CLARIFICATION_REQUIRED.issues[1:]))
        self.assertIn("blocking", {x.code for x in validate_clarification_result(invalid).errors})

    def test_rejects_non_canonical_issue_order(self) -> None:
        invalid = replace(CLARIFICATION_REQUIRED, issues=tuple(reversed(CLARIFICATION_REQUIRED.issues)), required_user_actions=tuple(reversed(CLARIFICATION_REQUIRED.required_user_actions)))
        self.assertIn("issue_order", {x.code for x in validate_clarification_result(invalid).errors})


class ReportValidationTests(unittest.TestCase):
    def test_report_mode_and_payload_must_match(self) -> None:
        invalid = replace(COMPLETE_REPORT, mode_payload=replace(COMPLETE_REPORT.mode_payload, mode="compare"))
        self.assertIn("mode", {x.code for x in validate_orientation_report(invalid).errors})

    def test_complete_report_cannot_contain_blocked_stage(self) -> None:
        stages = (replace(COMPLETE_REPORT.process[0], state="blocked", reason="blocked"), *COMPLETE_REPORT.process[1:])
        invalid = replace(COMPLETE_REPORT, process=stages)
        self.assertIn("complete_process", {x.code for x in validate_orientation_report(invalid).errors})

    def test_blocked_report_requires_absent_output(self) -> None:
        validation = replace(BLOCKED_REPORT.validation, orientation_validation=replace(BLOCKED_REPORT.validation.orientation_validation, absent_outputs=()))
        invalid = replace(BLOCKED_REPORT, validation=validation)
        self.assertIn("absent_output", {x.code for x in validate_orientation_report(invalid).errors})


class EvidenceValidationTests(unittest.TestCase):
    def test_derived_evidence_requires_versioned_derivation(self) -> None:
        invalid = replace(EVIDENCE, evidence_class="derived")
        self.assertIn("derived_provenance", {x.code for x in validate_evidence_reference(invalid).errors})

    def test_evidence_and_source_identity_remain_distinct(self) -> None:
        invalid = replace(EVIDENCE, evidence_id=EVIDENCE.source.source_id)
        self.assertIn("identity", {x.code for x in validate_evidence_reference(invalid).errors})


class RuntimeErrorValidationTests(unittest.TestCase):
    def test_blocked_runtime_error_cannot_claim_processing_began(self) -> None:
        invalid = replace(BLOCKED_BEFORE_PROCESSING, stage="processing")
        self.assertIn("blocked_stage", {x.code for x in validate_runtime_error(invalid).errors})

    def test_clarification_required_must_reference_result(self) -> None:
        invalid = replace(CLARIFICATION_REQUIRED_ERROR, result_presence="none", result_ref=None)
        self.assertIn("clarification_result", {x.code for x in validate_runtime_error(invalid).errors})


class LineageValidationTests(unittest.TestCase):
    def test_report_scope_must_equal_request_scope(self) -> None:
        altered = replace(COMPLETE_REPORT, orientation=replace(COMPLETE_REPORT.orientation, scope=Scope(("different",), (), ())))
        result = validate_contract_set(canonical_set(reports=(altered, PARTIAL_REPORT, BLOCKED_REPORT)))
        self.assertIn("scope_lineage", {x.code for x in result.errors})

    def test_continuation_cannot_drop_evidence(self) -> None:
        context = replace(CONTINUATION.preserved_context, evidence_refs=())
        altered = replace(CONTINUATION, preserved_context=context)
        result = validate_contract_set(canonical_set(continuations=(altered,)))
        self.assertIn("preserved_evidence", {x.code for x in result.errors})

    def test_continuation_cannot_change_source_report(self) -> None:
        altered = replace(CONTINUATION, source_report_version="2")
        result = validate_contract_set(canonical_set(continuations=(altered,)))
        self.assertIn("source_report", {x.code for x in result.errors})

    def test_evidence_must_trace_to_referencing_report(self) -> None:
        target = replace(EVIDENCE.traceability[0], report_id="other-report")
        altered = replace(EVIDENCE, traceability=(target,))
        result = validate_contract_set(canonical_set(evidence=(altered,)))
        self.assertIn("evidence_trace", {x.code for x in result.errors})

    def test_clarification_request_lineage_must_resolve(self) -> None:
        altered = replace(CLARIFICATION_REQUIRED, request_version="2")
        result = validate_contract_set(canonical_set(clarifications=(altered,)))
        self.assertIn("request_ref", {x.code for x in result.errors})

    def test_duplicate_public_identity_and_version_is_rejected(self) -> None:
        result = validate_contract_set(canonical_set(requests=(VALID_REQUEST, VALID_REQUEST)))
        self.assertIn("duplicate_identity", {x.code for x in result.errors})


if __name__ == "__main__":
    unittest.main()
