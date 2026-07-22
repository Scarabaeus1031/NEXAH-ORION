"""End-to-end tests for the in-process NEXAHEDRON to ORION Gateway."""

from __future__ import annotations

from dataclasses import replace
import unittest

from orion.gateway import GatewayResponse, OrientationGateway
from orion.public_contracts import (
    ClarificationResult,
    ContinuationOption,
    ContractSet,
    EvidenceReference,
    OrientationReport,
    OrientationRequest,
    PublicContract,
    RuntimeError,
    TraceabilityTarget,
    validate_contract_set,
    validate_orientation_request,
    validate_public_contract,
)
from orion.public_contracts.fixtures import EVIDENCE, RUNTIME_ERROR


def request_payload() -> dict[str, object]:
    return {
        "request_id": "gateway-understand-01",
        "request_version": "1",
        "mode": "understand",
        "requested_by": {
            "requester_id": "nexahedron-alpha",
            "requester_kind": "authorized_consumer",
            "authority_domain": "nexahedron.local-session",
        },
        "human_authority": {
            "human_ref": "human-alpha",
            "authority_scope": ["intention", "scope", "continuation"],
        },
        "orientation_objects": [
            {
                "object_id": "object-paper-01",
                "object_version": "1",
                "object_kind": "Research Paper",
                "source_owner": "author-team-01",
                "source_ref": "source-paper-01",
                "source_revision": "3",
                "identity_scope": "external",
                "representation_refs": ["representation-paper-01@1"],
                "access_status": "available",
            }
        ],
        "intention": {
            "direction": "Understand the structure and evidence of this paper.",
            "focus": "structure and evidence",
        },
        "scope": {
            "include": ["claims", "structure", "evidence"],
            "exclude": ["implementation advice"],
            "unresolved": [],
            "depth": "focused",
        },
    }


def gateway_evidence() -> EvidenceReference:
    return replace(
        EVIDENCE,
        evidence_id="evidence-gateway-understand-01",
        traceability=(
            TraceabilityTarget(
                "report-gateway-understand-01-1",
                "1",
                "mode_payload.content.claims_and_support[0]",
                "finding-gateway-01",
            ),
        ),
    )


def contract_identity(contract: PublicContract) -> tuple[str, str, str]:
    if isinstance(contract, OrientationReport):
        return (
            contract.identity.report_id,
            contract.identity.report_version,
            contract.schema_version,
        )
    if isinstance(contract, ClarificationResult):
        return contract.result_id, contract.result_version, contract.schema_version
    if isinstance(contract, ContinuationOption):
        return contract.option_id, contract.option_version, contract.schema_version
    if isinstance(contract, RuntimeError):
        return contract.error_id, contract.error_version, contract.schema_version
    raise AssertionError(f"unexpected Gateway contract: {type(contract).__name__}")


class RaisingRuntime:
    def orient(
        self,
        request: OrientationRequest,
        evidence: tuple[EvidenceReference, ...] = (),
    ) -> tuple[PublicContract, ...]:
        raise ValueError("private runtime failure")


class InvalidOutcomeRuntime:
    def orient(
        self,
        request: OrientationRequest,
        evidence: tuple[EvidenceReference, ...] = (),
    ) -> tuple[PublicContract, ...]:
        return (replace(RUNTIME_ERROR, effects="write"),)  # type: ignore[arg-type,return-value]


class OrientationGatewayTests(unittest.TestCase):
    def assert_valid_response(self, response: GatewayResponse) -> None:
        self.assertTrue(response.contracts)
        self.assertEqual(len(response.contracts), len(response.presentation))
        if response.request is not None:
            self.assertTrue(validate_orientation_request(response.request).valid)
        for contract, presentation in zip(response.contracts, response.presentation):
            with self.subTest(contract=type(contract).__name__):
                self.assertTrue(validate_public_contract(contract).valid)
                identity, version, schema = contract_identity(contract)
                self.assertEqual(presentation.source_identity, identity)
                self.assertEqual(presentation.source_version, version)
                self.assertEqual(presentation.source_schema_version, schema)

    def test_valid_understand_request_is_constructed_and_executed(self) -> None:
        response = OrientationGateway().handle(request_payload(), (gateway_evidence(),))

        self.assert_valid_response(response)
        self.assertIsInstance(response.request, OrientationRequest)
        self.assertEqual(response.request.mode, "understand")
        self.assertEqual(
            tuple(type(contract) for contract in response.contracts),
            (OrientationReport, ContinuationOption),
        )

    def test_clarification_flow_remains_public_and_traceable(self) -> None:
        payload = request_payload()
        payload["scope"] = {
            "include": ["claims"],
            "exclude": [],
            "unresolved": ["focus"],
            "depth": "focused",
        }

        response = OrientationGateway().handle(payload)

        self.assert_valid_response(response)
        error, clarification = response.contracts
        self.assertIsInstance(error, RuntimeError)
        self.assertIsInstance(clarification, ClarificationResult)
        self.assertEqual(error.kind, "clarification_required")
        self.assertEqual(response.presentation[1].title, "Clarification Required")
        self.assertTrue(
            validate_contract_set(
                ContractSet(
                    requests=(response.request,),  # type: ignore[arg-type]
                    clarifications=(clarification,),
                    runtime_errors=(error,),
                )
            ).valid
        )

    def test_restricted_source_is_blocked_before_processing(self) -> None:
        payload = request_payload()
        orientation_object = dict(payload["orientation_objects"][0])  # type: ignore[index]
        orientation_object["access_status"] = "restricted"
        payload["orientation_objects"] = [orientation_object]

        response = OrientationGateway().handle(payload)

        self.assert_valid_response(response)
        self.assertIsInstance(response.contracts[0], RuntimeError)
        self.assertEqual(response.contracts[0].kind, "blocked")
        self.assertEqual(response.contracts[0].stage, "readiness_validation")

    def test_missing_evidence_returns_a_blocked_report(self) -> None:
        response = OrientationGateway().handle(request_payload())

        self.assert_valid_response(response)
        self.assertIsInstance(response.contracts[0], OrientationReport)
        self.assertEqual(response.contracts[0].status, "blocked")
        self.assertEqual(response.presentation[0].status, "blocked")
        self.assertTrue(response.presentation[0].messages)

    def test_unsupported_mode_is_returned_without_gateway_substitution(self) -> None:
        payload = request_payload()
        payload["mode"] = "compare"

        response = OrientationGateway().handle(payload)

        self.assert_valid_response(response)
        self.assertIsInstance(response.contracts[0], RuntimeError)
        self.assertEqual(response.contracts[0].kind, "unsupported")

    def test_runtime_exception_becomes_public_internal_failure(self) -> None:
        response = OrientationGateway(RaisingRuntime()).handle(request_payload())

        self.assert_valid_response(response)
        self.assertIsInstance(response.contracts[0], RuntimeError)
        self.assertEqual(response.contracts[0].kind, "internal_failure")
        self.assertNotIn("private runtime failure", response.presentation[0].summary)

    def test_successful_report_presentation_is_derived_from_contract(self) -> None:
        response = OrientationGateway().handle(request_payload(), (gateway_evidence(),))
        report = response.contracts[0]
        presentation = response.presentation[0]

        self.assertIsInstance(report, OrientationReport)
        self.assertEqual(
            presentation.summary,
            report.mode_payload.content["orientation_summary"],
        )
        self.assertEqual(presentation.orientation, report.orientation.mode)
        self.assertEqual(presentation.evidence, report.evidence)
        self.assertEqual(presentation.continuation_suggestions, report.continuations)

    def test_invalid_external_request_never_reaches_runtime(self) -> None:
        response = OrientationGateway(RaisingRuntime()).handle({"mode": "understand"})

        self.assert_valid_response(response)
        self.assertIsNone(response.request)
        self.assertIsInstance(response.contracts[0], RuntimeError)
        self.assertEqual(response.contracts[0].kind, "invalid")
        self.assertEqual(response.contracts[0].stage, "contract_validation")

    def test_invalid_evidence_is_rejected_before_runtime(self) -> None:
        invalid = replace(gateway_evidence(), schema_version="orion.evidence-reference/2.0")

        response = OrientationGateway(RaisingRuntime()).handle(request_payload(), (invalid,))

        self.assert_valid_response(response)
        self.assertIsInstance(response.contracts[0], RuntimeError)
        self.assertEqual(response.contracts[0].kind, "invalid")
        self.assertEqual(response.contracts[0].reason_code, "evidence_reference_invalid")

    def test_invalid_runtime_output_is_replaced_not_exposed(self) -> None:
        response = OrientationGateway(InvalidOutcomeRuntime()).handle(request_payload())

        self.assert_valid_response(response)
        self.assertEqual(len(response.contracts), 1)
        error = response.contracts[0]
        self.assertIsInstance(error, RuntimeError)
        self.assertEqual(error.kind, "validation_failed")
        self.assertEqual(error.reason_code, "runtime_outcome_invalid")
        self.assertEqual(error.effects, "none")


if __name__ == "__main__":
    unittest.main()
