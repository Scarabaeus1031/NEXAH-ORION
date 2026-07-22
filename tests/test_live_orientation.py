"""Acceptance test for the first complete live Orientation Journey."""

from __future__ import annotations

import unittest

from orion.public_contracts import (
    ContinuationOption,
    OrientationReport,
    validate_public_contract,
)
from scripts.phase_vi_live_orientation import HUMAN_REQUEST, run_session, trace


class FirstLiveOrientationTests(unittest.TestCase):
    def test_complete_human_journey_is_valid_and_inspectable(self) -> None:
        session = run_session()

        self.assertIsNotNone(session.response.request)
        request = session.response.request
        self.assertEqual(request.intention.direction, HUMAN_REQUEST)  # type: ignore[union-attr]
        self.assertEqual(request.mode, "understand")  # type: ignore[union-attr]
        self.assertTrue(
            all(validate_public_contract(item).valid for item in session.response.contracts)
        )

        report = next(
            item
            for item in session.response.contracts
            if isinstance(item, OrientationReport)
        )
        continuation = next(
            item
            for item in session.response.contracts
            if isinstance(item, ContinuationOption)
        )
        self.assertEqual(report.status, "complete")
        self.assertEqual(report.validation.contract_validation, "valid")
        self.assertEqual(report.validation.orientation_validation.status, "valid")
        self.assertEqual(report.evidence, continuation.preserved_context.evidence_refs)
        self.assertEqual(continuation.action_type, "inspect_evidence")
        self.assertEqual(continuation.availability, "available")

        report_view = session.response.presentation[0]
        self.assertIn(request.intention.focus, report_view.summary)  # type: ignore[union-attr]
        self.assertEqual(
            tuple(item.evidence_ref for item in report_view.evidence_details),
            report.evidence,
        )
        self.assertTrue(
            all(item.fragment_ref for item in report_view.evidence_details)
        )

        recorded = trace(session)
        self.assertEqual(
            tuple(recorded),
            (
                "session_id",
                "request",
                "validated_request",
                "runtime_outcome",
                "evidence",
                "orientation_report",
                "continuation",
                "presentation",
            ),
        )


if __name__ == "__main__":
    unittest.main()
