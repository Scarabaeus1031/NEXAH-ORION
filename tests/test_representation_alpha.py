"""Conformance tests for the first executable ORION Representation profile."""

from __future__ import annotations

import ast
from dataclasses import FrozenInstanceError, asdict, replace
from hashlib import sha256
import json
from pathlib import Path
import unittest

from orion.contracts import ContextEntry
from orion.representation_alpha import (
    NO_LOSS,
    ConfirmedLocalSource,
    ExactTextRenderer,
    confirmed_source_from_mapping,
    validate_representation,
)


ROOT = Path(__file__).resolve().parent.parent
FIXTURE = ROOT / "examples" / "representation_alpha" / "confirmed_local_source.json"


def fixture_source() -> ConfirmedLocalSource:
    return confirmed_source_from_mapping(
        json.loads(FIXTURE.read_text(encoding="utf-8"))
    )


class RepresentationAlphaTests(unittest.TestCase):
    def setUp(self) -> None:
        self.source = fixture_source()
        self.renderer = ExactTextRenderer()

    def test_fixture_is_exact_human_confirmed_local_text(self) -> None:
        self.assertEqual(self.source.entry.owner, "human-alpha-reviewer")
        self.assertEqual(self.source.fragment_ref, "whole")
        self.assertEqual(
            self.source.entry.revision,
            f"sha256:{self.source.entry.content_sha256}",
        )
        self.assertEqual(
            self.source.entry.content,
            "Information already exists. Orientation is what is missing.\n",
        )

    def test_fixture_loader_rejects_coerced_source_values(self) -> None:
        value = json.loads(FIXTURE.read_text(encoding="utf-8"))
        value["source"]["source_version"] = None

        with self.assertRaisesRegex(ValueError, "source_version"):
            confirmed_source_from_mapping(value)

    def test_identical_confirmed_input_produces_identical_representation(self) -> None:
        first = self.renderer.render(self.source)
        second = self.renderer.render(fixture_source())

        self.assertEqual(first, second)
        self.assertEqual(asdict(first), asdict(second))
        self.assertEqual(
            first.representation_id,
            "representation-5996f6dbc2d089ac",
        )
        self.assertEqual(
            first.representation_version,
            "sha256:ceca69e14960db4a92593c367e0a2604fddb8807933446e992357a663cde66bd",
        )

    def test_representation_is_immutable_and_preserves_source_traceback(self) -> None:
        representation = self.renderer.render(self.source)

        with self.assertRaises(FrozenInstanceError):
            representation.renderer_version = "changed"  # type: ignore[misc]
        self.assertEqual(representation.source, self.source.entry.provenance())
        self.assertEqual(
            representation.orientation_object_id,
            self.source.orientation_object_id,
        )
        self.assertEqual(representation.declared_lossiness, NO_LOSS)

    def test_content_change_creates_new_source_and_representation_version(self) -> None:
        content = f"{self.source.entry.content}One additional line.\n"
        content_sha256 = sha256(content.encode("utf-8")).hexdigest()
        source_version = f"sha256:{content_sha256}"
        confirmation_value = {
            "confirmed_by": self.source.confirmed_by,
            "confirmed_revision": 2,
            "entry_id": self.source.entry.entry_id,
            "fragment_ref": self.source.fragment_ref,
            "revision": source_version,
        }
        confirmation_sha256 = sha256(
            json.dumps(
                confirmation_value,
                ensure_ascii=False,
                separators=(",", ":"),
                sort_keys=True,
            ).encode("utf-8")
        ).hexdigest()
        changed = ConfirmedLocalSource(
            orientation_object_id=self.source.orientation_object_id,
            orientation_object_version="2",
            entry=ContextEntry(
                entry_id=self.source.entry.entry_id,
                owner=self.source.entry.owner,
                source_ref=self.source.entry.source_ref,
                revision=source_version,
                content=content,
                content_sha256=content_sha256,
            ),
            confirmed_by=self.source.confirmed_by,
            confirmed_revision=2,
            confirmation_id=f"confirmation-{confirmation_sha256[:16]}",
        )

        original = self.renderer.render(self.source)
        updated = self.renderer.render(changed)
        self.assertNotEqual(changed.entry.revision, self.source.entry.revision)
        self.assertNotEqual(updated.representation_version, original.representation_version)

    def test_renderer_version_change_creates_new_representation_identity_and_version(self) -> None:
        changed_renderer = replace(self.renderer, renderer_version="0.1-alpha.2")

        original = self.renderer.render(self.source)
        changed = changed_renderer.render(self.source)
        self.assertEqual(changed.representation_id, original.representation_id)
        self.assertNotEqual(changed.representation_version, original.representation_version)

    def test_external_conformance_validates_replay_integrity_and_boundaries(self) -> None:
        representation = self.renderer.render(self.source)
        conformance = validate_representation(
            self.source,
            representation,
            renderer=self.renderer,
        )

        self.assertTrue(conformance.valid)
        self.assertEqual(conformance.errors, ())
        self.assertIn("deterministic_replay", conformance.checks)
        self.assertIn("source_traceback", conformance.checks)
        self.assertIn("no_orientation_or_evidence_semantics", conformance.checks)

    def test_tampered_payload_fails_external_conformance(self) -> None:
        representation = self.renderer.render(self.source)
        object.__setattr__(representation.payload, "content", "Changed after rendering")

        conformance = validate_representation(self.source, representation)

        self.assertFalse(conformance.valid)
        self.assertIn("Representation differs from deterministic replay", conformance.errors)
        self.assertTrue(
            any("digest mismatch" in error for error in conformance.errors),
        )

    def test_invalid_source_returns_failed_conformance_instead_of_raising(self) -> None:
        representation = self.renderer.render(self.source)
        object.__setattr__(self.source.entry, "content", "Changed source")

        conformance = validate_representation(self.source, representation)

        self.assertFalse(conformance.valid)
        self.assertTrue(
            any("content digest mismatch" in error for error in conformance.errors),
        )

    def test_representation_contains_no_evidence_or_report_binding_semantics(self) -> None:
        value = asdict(self.renderer.render(self.source))
        serialized_keys = set(value)

        self.assertTrue(
            {
                "evidence_class",
                "relationship",
                "report_id",
                "target_path",
                "traceability",
            }.isdisjoint(serialized_keys)
        )

    def test_alpha_profile_stays_outside_frozen_public_and_runtime_boundaries(self) -> None:
        import orion

        self.assertNotIn("ExactTextRenderer", orion.__all__)
        path = ROOT / "src" / "orion" / "representation_alpha.py"
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        imported_modules = set()
        forbidden_calls = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_modules.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                imported_modules.add(node.module or "")
            elif (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and node.func.attr in {"read_text", "read_bytes", "write_text", "write_bytes"}
            ):
                forbidden_calls.add(node.func.attr)
            elif (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id == "open"
            ):
                forbidden_calls.add(node.func.id)

        self.assertTrue(
            {
                "orion.gateway",
                "orion.orientation_runtime",
                "orion.public_contracts",
                "openai",
                "anthropic",
                "ollama",
                "requests",
                "urllib",
            }.isdisjoint(imported_modules)
        )
        self.assertEqual(forbidden_calls, set())


if __name__ == "__main__":
    unittest.main()
