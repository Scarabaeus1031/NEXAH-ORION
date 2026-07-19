"""Tests for deterministic Phase 2A repository context construction."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from orion import (
    ContextBuilder,
    ContextDocumentNotFoundError,
    ContextualOrientationExecutor,
    FakeBackend,
    InvalidContextDocumentPathError,
    OrientationRequest,
    RepositoryContextProvider,
)


def request() -> OrientationRequest:
    return OrientationRequest(
        request_id="req-phase-2a",
        objective="Review the selected repository documents.",
        requested_by="phase-2a-test",
        scope=("architecture",),
    )


class ContextBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        (self.root / "docs" / "architecture").mkdir(parents=True)
        (self.root / "README.md").write_text("Repository overview.\n", encoding="utf-8")
        (self.root / "docs" / "architecture" / "ORION.md").write_text(
            "The orchestrator validates.\n",
            encoding="utf-8",
        )
        self.provider = RepositoryContextProvider(
            repository_root=self.root,
            source_id="orion",
            owner="NEXAH ORION",
            revision="test-revision",
        )

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_manifest_generation_is_deterministic_and_auditable(self) -> None:
        builder = ContextBuilder(
            self.provider,
            ("README.md", "docs/architecture/ORION.md"),
        )

        first = builder.build(request())
        second = builder.build(request())

        self.assertEqual(first, second)
        self.assertEqual(first.manifest_sha256, second.manifest_sha256)
        self.assertEqual(
            tuple(entry.source_ref for entry in first.entries),
            ("orion:README.md", "orion:docs/architecture/ORION.md"),
        )
        self.assertEqual(
            first.entries[0].content_sha256,
            sha256(b"Repository overview.\n").hexdigest(),
        )
        self.assertTrue(
            all(entry.revision == "test-revision" for entry in first.entries)
        )
        self.assertEqual(first.provenance[0].owner, "NEXAH ORION")
        self.assertEqual(
            first.provenance[0].content_sha256,
            first.entries[0].content_sha256,
        )

    def test_order_is_reproducible_and_duplicate_paths_are_prevented(self) -> None:
        first = ContextBuilder(
            self.provider,
            (
                "docs/architecture/ORION.md",
                "README.md",
                "README.md",
            ),
        ).build(request())
        second = ContextBuilder(
            self.provider,
            ("README.md", "docs/architecture/ORION.md"),
        ).build(request())

        self.assertEqual(first, second)
        self.assertEqual(len(first.entries), 2)
        self.assertEqual(
            tuple(entry.entry_id for entry in first.entries),
            ("orion:README.md", "orion:docs/architecture/ORION.md"),
        )

    def test_missing_document_fails_explicitly(self) -> None:
        builder = ContextBuilder(self.provider, ("docs/missing.md",))

        with self.assertRaisesRegex(
            ContextDocumentNotFoundError,
            "docs/missing.md",
        ):
            builder.build(request())

    def test_repository_escape_is_rejected(self) -> None:
        builder = ContextBuilder(self.provider, ("../outside.md",))

        with self.assertRaises(InvalidContextDocumentPathError):
            builder.build(request())

    def test_manifest_and_builder_configuration_are_immutable(self) -> None:
        builder = ContextBuilder(self.provider, ("README.md",))
        manifest = builder.build(request())

        with self.assertRaises(FrozenInstanceError):
            manifest.entries = ()  # type: ignore[misc]
        with self.assertRaises(FrozenInstanceError):
            manifest.entries[0].content = "changed"  # type: ignore[misc]
        with self.assertRaises(FrozenInstanceError):
            builder.document_paths = ()  # type: ignore[misc]

    def test_context_is_built_before_the_backend_is_invoked(self) -> None:
        builder = ContextBuilder(self.provider, ("README.md",))

        response = ContextualOrientationExecutor(
            backend=FakeBackend(),
            context_builder=builder,
        ).execute(request())

        self.assertTrue(response.validated)
        self.assertEqual(response.provenance_ids, ("orion:README.md",))
        self.assertEqual(
            response.claims[0].evidence_refs,
            response.provenance_ids,
        )


if __name__ == "__main__":
    unittest.main()
