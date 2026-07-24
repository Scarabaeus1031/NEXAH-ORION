"""Tests for deterministic Phase 2C context briefs."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from orion.brief_backend import ContextBriefReasoningBackend
from orion.brief_execution import ContextBriefOrientationExecutor
from orion.context_brief import (
    ContextBrief,
    ContextBriefBuilder,
)
from orion.context_builder import RepositoryContextProvider
from orion.contracts import (
    ContextEntry,
    ContextManifest,
    OrientationRequest,
    ReasoningClaim,
    ReasoningResult,
)
from orion.document_selector import (
    DocumentSelectionRule,
    DocumentSelector,
)
from orion.contracts import result_id_for


def request(*, scope: tuple[str, ...] = ("brief",)) -> OrientationRequest:
    return OrientationRequest(
        request_id="req-phase-2c",
        objective="Present deterministic context metadata.",
        requested_by="phase-2c-test",
        scope=scope,
    )


def manifest() -> ContextManifest:
    return ContextManifest.create(
        request(),
        (
            ContextEntry.create(
                entry_id="orion:docs/b.md",
                owner="NEXAH ORION",
                source_ref="orion:docs/b.md",
                revision="revision-1",
                content="Second in source order.\n",
            ),
            ContextEntry.create(
                entry_id="orion:docs/a.md",
                owner="NEXAH ORION",
                source_ref="orion:docs/a.md",
                revision="revision-1",
                content="First alphabetically, second in manifest. ä\n",
            ),
        ),
    )


class RecordingBriefBackend:
    def __init__(self) -> None:
        self.received_brief: ContextBrief | None = None

    @property
    def backend_id(self) -> str:
        return "recording-brief-backend/0.1"

    def reason(self, request, context: ContextBrief) -> ReasoningResult:
        self.received_brief = context
        evidence_refs = tuple(
            entry.provenance.entry_id for entry in context.entries
        )
        return ReasoningResult(
            result_id=result_id_for(
                request_id=request.request_id,
                manifest_id=context.manifest_id,
                backend_id=self.backend_id,
            ),
            request_id=request.request_id,
            manifest_id=context.manifest_id,
            backend_id=self.backend_id,
            output="The backend received deterministic context metadata.",
            claims=(
                ReasoningClaim(
                    claim_id="claim-context-brief",
                    text="The brief preserves source provenance.",
                    evidence_refs=evidence_refs,
                ),
            ),
        )


class ContextBriefBuilderTests(unittest.TestCase):
    def test_ordering_is_preserved_and_explicit(self) -> None:
        brief = ContextBriefBuilder().build(manifest())

        self.assertEqual(
            tuple(entry.source_ref for entry in brief.entries),
            ("orion:docs/b.md", "orion:docs/a.md"),
        )
        self.assertEqual(
            tuple(entry.repository_path for entry in brief.entries),
            ("docs/b.md", "docs/a.md"),
        )
        self.assertEqual(
            tuple(entry.document_order for entry in brief.entries),
            (0, 1),
        )

    def test_brief_is_immutable_and_contains_no_document_text(self) -> None:
        brief = ContextBriefBuilder().build(manifest())

        with self.assertRaises(FrozenInstanceError):
            brief.entries = ()  # type: ignore[misc]
        with self.assertRaises(FrozenInstanceError):
            brief.entries[0].document_order = 3  # type: ignore[misc]
        self.assertFalse(hasattr(brief.entries[0], "content"))
        self.assertFalse(hasattr(brief, "prompt"))

    def test_provenance_hash_revision_and_length_are_preserved(self) -> None:
        source_manifest = manifest()
        brief = ContextBriefBuilder().build(source_manifest)

        for source, presented in zip(source_manifest.entries, brief.entries):
            self.assertEqual(presented.provenance, source.provenance())
            self.assertEqual(presented.revision, source.revision)
            self.assertEqual(presented.content_sha256, source.content_sha256)
            self.assertEqual(
                presented.document_length,
                len(source.content.encode("utf-8")),
            )

    def test_manifest_integrity_is_revalidated(self) -> None:
        tampered = manifest()
        object.__setattr__(tampered, "manifest_sha256", "0" * 64)

        with self.assertRaisesRegex(ValueError, "manifest digest mismatch"):
            ContextBriefBuilder().build(tampered)

    def test_repeated_generation_is_equal(self) -> None:
        source_manifest = manifest()
        builder = ContextBriefBuilder()

        first = builder.build(source_manifest)
        second = builder.build(source_manifest)

        self.assertEqual(first, second)
        self.assertEqual(first.brief_sha256, second.brief_sha256)

    def test_every_valid_source_reference_has_a_deterministic_path(self) -> None:
        legacy_manifest = ContextManifest.create(
            request(),
            (
                ContextEntry.create(
                    entry_id="legacy-entry",
                    owner="NEXAH ORION",
                    source_ref="legacy-source-without-separator",
                    revision="revision-1",
                    content="Legacy but valid manifest content.",
                ),
            ),
        )

        brief = ContextBriefBuilder().build(legacy_manifest)

        self.assertEqual(
            brief.entries[0].repository_path,
            "legacy-source-without-separator",
        )

    def test_brief_reaches_a_brief_capable_backend(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / "README.md").write_text(
                "Brief pipeline context.\n",
                encoding="utf-8",
            )
            backend = RecordingBriefBackend()
            executor = ContextBriefOrientationExecutor(
                backend=backend,
                selector=DocumentSelector(
                    rules=(
                        DocumentSelectionRule(
                            rule_id="scope-brief/1",
                            scope="brief",
                            document_paths=("README.md",),
                        ),
                    )
                ),
                context_provider=RepositoryContextProvider(
                    repository_root=root,
                    source_id="test-repository",
                    owner="NEXAH ORION",
                    revision="test-revision",
                ),
            )

            response = executor.execute(request())

        self.assertIsInstance(backend, ContextBriefReasoningBackend)
        self.assertIsInstance(backend.received_brief, ContextBrief)
        self.assertTrue(response.validated)
        self.assertEqual(
            response.provenance_ids,
            ("test-repository:README.md",),
        )


if __name__ == "__main__":
    unittest.main()
