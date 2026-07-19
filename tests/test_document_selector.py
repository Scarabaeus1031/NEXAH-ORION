"""Tests for deterministic Phase 2B document-path selection."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from orion import (
    DocumentSelectionRule,
    DocumentSelector,
    EmptyDocumentSelectionError,
    FakeBackend,
    OrientationRequest,
    RepositoryContextProvider,
    SelectingOrientationExecutor,
    UnknownDocumentScopeError,
)


def request(
    *,
    scope: tuple[str, ...] = ("architecture",),
    objective: str = "Review the repository architecture.",
) -> OrientationRequest:
    return OrientationRequest(
        request_id="req-phase-2b",
        objective=objective,
        requested_by="phase-2b-test",
        request_type="review",
        scope=scope,
    )


class DocumentSelectorTests(unittest.TestCase):
    def test_selection_is_deterministic(self) -> None:
        selector = DocumentSelector()

        first = selector.select(request())
        second = selector.select(request())

        self.assertEqual(first, second)
        self.assertEqual(first.rule_id, "explicit-scope-selection/1")
        self.assertNotIn("content_sha256", first.__dataclass_fields__)
        with self.assertRaises(FrozenInstanceError):
            first.selected_paths = ()  # type: ignore[misc]

    def test_unknown_scope_fails_explicitly(self) -> None:
        with self.assertRaisesRegex(
            UnknownDocumentScopeError,
            "unknown",
        ):
            DocumentSelector().select(request(scope=("unknown",)))

    def test_empty_selection_fails_explicitly(self) -> None:
        selector = DocumentSelector(
            rules=(
                DocumentSelectionRule(
                    rule_id="scope-empty/1",
                    scope="empty",
                    document_paths=(),
                ),
            )
        )

        with self.assertRaises(EmptyDocumentSelectionError):
            selector.select(request(scope=("empty",)))

    def test_paths_are_ordered_and_duplicates_are_eliminated(self) -> None:
        selector = DocumentSelector(
            rules=(
                DocumentSelectionRule(
                    rule_id="scope-alpha/1",
                    scope="alpha",
                    document_paths=("z.md", "shared.md", "a.md"),
                ),
                DocumentSelectionRule(
                    rule_id="scope-beta/1",
                    scope="beta",
                    document_paths=("shared.md", "b.md", "b.md"),
                ),
            )
        )

        result = selector.select(request(scope=("beta", "alpha")))

        self.assertEqual(
            result.selected_paths,
            ("a.md", "b.md", "shared.md", "z.md"),
        )

    def test_rule_provenance_records_request_inputs_and_matched_rules(self) -> None:
        objective = "Inspect validation ownership."

        result = DocumentSelector().select(
            request(scope=("validation",), objective=objective)
        )

        self.assertEqual(result.selection_provenance[0], "request_id:req-phase-2b")
        self.assertEqual(result.selection_provenance[1], "request_type:review")
        self.assertEqual(result.selection_provenance[2], "requested_by:phase-2b-test")
        self.assertEqual(
            result.selection_provenance[3],
            "request_schema:orion.orientation-request/0.1",
        )
        self.assertEqual(result.selection_provenance[4], f"objective:{objective}")
        self.assertEqual(
            result.selection_provenance[5],
            "scope:validation;rule:scope-validation/1",
        )

    def test_selector_does_not_read_selected_documents(self) -> None:
        selector = DocumentSelector(
            rules=(
                DocumentSelectionRule(
                    rule_id="scope-missing/1",
                    scope="missing",
                    document_paths=("does-not-exist.md",),
                ),
            )
        )

        result = selector.select(request(scope=("missing",)))

        self.assertEqual(result.selected_paths, ("does-not-exist.md",))

    def test_selected_paths_feed_the_unchanged_context_builder(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / "README.md").write_text(
                "Selected repository context.\n",
                encoding="utf-8",
            )
            selector = DocumentSelector(
                rules=(
                    DocumentSelectionRule(
                        rule_id="scope-test/1",
                        scope="test",
                        document_paths=("README.md",),
                    ),
                )
            )
            provider = RepositoryContextProvider(
                repository_root=root,
                source_id="test-repository",
                owner="NEXAH ORION",
                revision="test-revision",
            )

            response = SelectingOrientationExecutor(
                backend=FakeBackend(),
                selector=selector,
                context_provider=provider,
            ).execute(request(scope=("test",)))

        self.assertTrue(response.validated)
        self.assertEqual(
            response.provenance_ids,
            ("test-repository:README.md",),
        )


if __name__ == "__main__":
    unittest.main()
