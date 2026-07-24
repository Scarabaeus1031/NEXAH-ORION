"""Phase VII real-world corpus and multi-session acceptance tests."""

from __future__ import annotations

import unittest

from orion.public_contracts import (
    ContinuationOption,
    OrientationReport,
    validate_public_contract,
)
from scripts.phase_vii_real_world_evaluation import (
    full_trace,
    load_corpus,
    metrics,
    run_corpus,
    verify_document,
)


REVIEW_CLASSES = {
    "Runtime",
    "Presentation",
    "Evidence",
    "UX",
    "Missing Representation",
    "Missing Capability",
}


class RealWorldOrientationCorpusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.corpus, cls.sessions = run_corpus()

    def test_corpus_is_versioned_diverse_and_reproducible(self) -> None:
        documents = self.corpus["documents"]
        self.assertEqual(self.corpus["corpus_version"], "1.0.1")
        self.assertGreaterEqual(len(documents), 10)
        self.assertLessEqual(len(documents), 20)
        self.assertGreaterEqual(len({item["document_type"] for item in documents}), 10)
        for document in documents:
            with self.subTest(document=document["document_id"]):
                self.assertEqual(verify_document(document), document["sha256"])
                self.assertGreaterEqual(len(document["evidence_fragments"]), 2)

    def test_every_document_completes_one_independent_understand_session(self) -> None:
        self.assertEqual(len(self.sessions), len(self.corpus["documents"]))
        request_ids = set()
        report_ids = set()
        for session in self.sessions:
            with self.subTest(document=session.document["document_id"]):
                request = session.response.request
                self.assertIsNotNone(request)
                self.assertEqual(request.mode, "understand")  # type: ignore[union-attr]
                self.assertEqual(
                    request.intention.direction,  # type: ignore[union-attr]
                    session.document["human_intention"],
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
                self.assertTrue(validate_public_contract(report).valid)
                self.assertTrue(validate_public_contract(continuation).valid)
                self.assertEqual(report.orientation.scope, request.scope)  # type: ignore[union-attr]
                self.assertIn(
                    request.intention.focus,  # type: ignore[union-attr]
                    report.mode_payload.content["orientation_summary"],
                )
                self.assertEqual(
                    report.mode_payload.content["key_concepts"],
                    request.scope.include,  # type: ignore[union-attr]
                )
                self.assertEqual(report.evidence, continuation.preserved_context.evidence_refs)
                self.assertEqual(continuation.action_type, "inspect_evidence")
                self.assertEqual(continuation.availability, "available")
                request_ids.add(request.request_id)  # type: ignore[union-attr]
                report_ids.add(report.identity.report_id)
        self.assertEqual(len(request_ids), len(self.sessions))
        self.assertEqual(len(report_ids), len(self.sessions))

    def test_evidence_and_presentation_make_source_support_inspectable(self) -> None:
        for session in self.sessions:
            with self.subTest(document=session.document["document_id"]):
                report = next(
                    item
                    for item in session.response.contracts
                    if isinstance(item, OrientationReport)
                )
                view = session.response.presentation[0]
                self.assertEqual(view.evidence, report.evidence)
                self.assertEqual(len(view.evidence_details), len(session.evidence))
                self.assertEqual(
                    tuple(detail.source_version for detail in view.evidence_details),
                    tuple(session.document["sha256"] for _ in session.evidence),
                )
                self.assertEqual(
                    tuple(detail.fragment_ref for detail in view.evidence_details),
                    tuple(
                        f"text_quote:{quote}"
                        for quote in session.document["evidence_fragments"]
                    ),
                )
                self.assertEqual(
                    report.mode_payload.content["suggested_continuations"],
                    report.continuations,
                )

    def test_every_session_has_the_required_review_classification(self) -> None:
        for session in self.sessions:
            with self.subTest(document=session.document["document_id"]):
                self.assertEqual(set(session.review), REVIEW_CLASSES)
                self.assertTrue(all(session.review.values()))

    def test_cross_session_metrics_meet_phase_vii_threshold(self) -> None:
        result = metrics(self.sessions)
        self.assertEqual(result["session_count"], 12)
        self.assertEqual(result["completion"], {"count": 12, "rate": 1.0})
        self.assertEqual(result["clarification"], {"count": 0, "rate": 0.0})
        self.assertEqual(result["blocked"], {"count": 0, "rate": 0.0})
        self.assertEqual(result["unsupported"], {"count": 0, "rate": 0.0})
        self.assertEqual(result["evidence_coverage_complete"]["rate"], 1.0)
        self.assertEqual(result["continuation_useful"]["rate"], 1.0)
        self.assertEqual(result["user_understanding_proxy"]["rate"], 1.0)

    def test_full_trace_records_every_required_observation_stage(self) -> None:
        recorded = full_trace(self.sessions[0])
        self.assertEqual(
            tuple(recorded),
            (
                "document",
                "request",
                "validated_request",
                "runtime_outcome",
                "evidence",
                "orientation_report",
                "continuation",
                "presentation",
                "review",
            ),
        )

    def test_loader_enforces_current_corpus_envelope(self) -> None:
        # Calling the loader itself is part of conformance: it enforces version,
        # cardinality, and unique document identities before any Runtime call.
        self.assertEqual(load_corpus()["corpus_id"], self.corpus["corpus_id"])


if __name__ == "__main__":
    unittest.main()
