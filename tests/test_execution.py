"""Executable acceptance tests for the Phase 1A architecture slice."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
import unittest

from orion.backend import ReasoningBackend
from orion.contracts import (
    ContextEntry,
    OrientationRequest,
    ReasoningClaim,
    ReasoningResult,
)
from orion.executor import OrientationExecutor
from orion.fake_backend import FakeBackend


def request() -> OrientationRequest:
    return OrientationRequest(
        request_id="req-phase-1a",
        objective="Prove one complete ORION execution.",
        requested_by="phase-1a-test",
        scope=("architecture",),
    )


def context() -> tuple[ContextEntry, ...]:
    return (
        ContextEntry.create(
            entry_id="core-baseline",
            owner="NEXAH Core",
            source_ref="git:NEXAH",
            revision="9f79bb06210402c40c9ef7d9937ca00d86c092b1",
            content="The Core remains frozen and owns canonical decisions.",
        ),
        ContextEntry.create(
            entry_id="orion-principle",
            owner="ORION",
            source_ref="docs/architecture/ORION_ARCHITECTURE.md",
            revision="phase-1a",
            content="The model proposes. The Orchestrator validates. The Kernel decides.",
        ),
    )


class TamperingBackend:
    """Test double proving that backend claims do not bypass validation."""

    @property
    def backend_id(self) -> str:
        return "tampering-backend/0.1"

    def reason(self, request, context) -> ReasoningResult:
        return ReasoningResult(
            result_id="result-tampered",
            request_id=request.request_id,
            manifest_id=context.manifest_id,
            backend_id=self.backend_id,
            output="Unsupported candidate.",
            claims=(
                ReasoningClaim(
                    claim_id="claim-tampered",
                    text="This claim cites context that was never supplied.",
                    evidence_refs=("missing-context",),
                ),
            ),
        )


class ExecutionTests(unittest.TestCase):
    def test_complete_execution_preserves_provenance(self) -> None:
        response = OrientationExecutor(FakeBackend()).execute(request(), context())

        self.assertTrue(response.validated)
        self.assertIsNotNone(response.candidate_output)
        self.assertEqual(response.backend_id, "fake-backend/0.1")
        self.assertEqual(
            tuple(ref.entry_id for ref in response.provenance),
            ("core-baseline", "orion-principle"),
        )
        self.assertEqual(response.claims[0].evidence_refs, response.provenance_ids)
        self.assertEqual(response.canonical_effects, ())

    def test_fake_backend_is_deterministic_and_replaceable(self) -> None:
        backend = FakeBackend()
        executor = OrientationExecutor(backend)

        first = executor.execute(request(), context())
        second = executor.execute(request(), context())

        self.assertIsInstance(backend, ReasoningBackend)
        self.assertEqual(first, second)

    def test_invalid_backend_output_is_not_exposed_as_candidate(self) -> None:
        response = OrientationExecutor(TamperingBackend()).execute(request(), context())

        self.assertFalse(response.validated)
        self.assertIsNone(response.candidate_output)
        self.assertEqual(response.claims, ())
        self.assertEqual(response.canonical_effects, ())
        self.assertEqual(
            tuple(ref.entry_id for ref in response.provenance),
            ("core-baseline", "orion-principle"),
        )
        self.assertIn("claim_evidence_unknown", response.validation.errors[0])

    def test_context_content_cannot_be_changed_without_detection(self) -> None:
        entry = context()[0]

        with self.assertRaises(ValueError):
            ContextEntry(
                entry_id=entry.entry_id,
                owner=entry.owner,
                source_ref=entry.source_ref,
                revision=entry.revision,
                content="changed",
                content_sha256=entry.content_sha256,
            )

        with self.assertRaises(FrozenInstanceError):
            entry.content = "changed"  # type: ignore[misc]


if __name__ == "__main__":
    unittest.main()
