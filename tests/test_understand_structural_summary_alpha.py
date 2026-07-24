"""Tests for the bounded UNDERSTAND Structural Summary Alpha."""

from __future__ import annotations

import ast
from dataclasses import FrozenInstanceError, asdict, replace
from hashlib import sha256
import inspect
import json
from pathlib import Path
import subprocess
import sys
import unittest

from orion.markdown_structural_renderer_alpha import (
    ALPHA_ELEMENT_KINDS,
    ConfirmedMarkdownSource,
    MarkdownStructuralRendererAlpha,
)
from orion.understand_source_element_inventory_alpha import (
    canonical_inventory_bytes,
    inventory_declared_source_elements,
)
from orion.understand_structural_summary_alpha import (
    STOP_AFTER_STRUCTURAL_SUMMARY,
    DeclaredHeadingSummary,
    StructuralSummaryDiagnostic,
    canonical_structural_summary_bytes,
    summarize_declared_structure,
    validate_structural_summary,
)


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from slice_ii_structural_summary_proof import (  # noqa: E402
    _confirmed_source,
)


PROOF = ROOT / "scripts" / "slice_ii_structural_summary_proof.py"


def complete_inventory():
    representation = MarkdownStructuralRendererAlpha().render(
        _confirmed_source()
    )
    return representation, inventory_declared_source_elements(representation)


def nested_keys(value: object) -> set[str]:
    if isinstance(value, dict):
        return set(value).union(*(nested_keys(item) for item in value.values()))
    if isinstance(value, (tuple, list)):
        return set().union(*(nested_keys(item) for item in value))
    return set()


class UnderstandStructuralSummaryAlphaTests(unittest.TestCase):
    def test_summary_recomputes_every_field_from_inventory(self) -> None:
        representation, inventory = complete_inventory()

        summary = summarize_declared_structure(inventory)

        expected_inventory_ref = (
            "sha256:"
            + sha256(canonical_inventory_bytes(inventory)).hexdigest()
        )
        self.assertEqual(summary.diagnostic_version, "0.1-alpha")
        self.assertEqual(summary.canonical_stage, "understand/2")
        self.assertEqual(summary.operator_id, "orion.orientation-operator/understand")
        self.assertEqual(summary.operator_version, "1.0")
        self.assertEqual(summary.responsibility, "structural_summary")
        self.assertEqual(
            summary.input_boundary,
            "declared_source_element_inventory",
        )
        self.assertEqual(summary.input_inventory_ref, expected_inventory_ref)
        self.assertEqual(
            (
                summary.orientation_object_id,
                summary.orientation_object_version,
            ),
            (
                inventory.orientation_object_id,
                inventory.orientation_object_version,
            ),
        )
        self.assertEqual(
            (
                summary.representation_id,
                summary.representation_version,
                summary.representation_integrity,
            ),
            (
                representation.representation_id,
                representation.representation_version,
                representation.representation_sha256,
            ),
        )
        self.assertEqual(
            (
                summary.source_id,
                summary.source_revision,
                summary.source_integrity,
                summary.source_boundary,
            ),
            (
                inventory.source_id,
                inventory.source_revision,
                inventory.source_integrity,
                inventory.source_boundary,
            ),
        )
        self.assertEqual(
            summary.total_declared_element_count,
            inventory.ordered_element_count,
        )
        self.assertEqual(
            summary.ordered_element_kinds,
            tuple(element.element_kind for element in inventory.elements),
        )
        self.assertEqual(summary.first_canonical_ordinal, 0)
        self.assertEqual(
            summary.final_canonical_ordinal,
            inventory.ordered_element_count - 1,
        )
        self.assertEqual(summary.profile_v1_vocabulary, ALPHA_ELEMENT_KINDS)
        self.assertEqual(summary.absent_block_kinds, ())
        self.assertEqual(summary.responsibility_state, "completed")
        self.assertEqual(summary.canonical_stage_state, "incomplete")
        self.assertEqual(summary.stop, STOP_AFTER_STRUCTURAL_SUMMARY)

    def test_summary_preserves_heading_declarations_without_text(self) -> None:
        _, inventory = complete_inventory()

        summary = summarize_declared_structure(inventory)

        self.assertEqual(
            tuple(
                (
                    heading.element_kind,
                    heading.ordinal,
                    heading.level,
                )
                for heading in summary.declared_headings
            ),
            (
                ("atx_heading", 1, 1),
                ("setext_heading", 22, 2),
            ),
        )
        self.assertEqual(
            tuple(heading.element_id for heading in summary.declared_headings),
            tuple(
                element.element_id
                for element in inventory.elements
                if element.element_kind in ("atx_heading", "setext_heading")
            ),
        )

    def test_summary_coverage_preserves_first_declared_order(self) -> None:
        _, inventory = complete_inventory()

        summary = summarize_declared_structure(inventory)

        self.assertEqual(
            summary.declared_block_kinds,
            tuple(
                dict.fromkeys(
                    element.element_kind for element in inventory.elements
                )
            ),
        )
        self.assertEqual(
            set(summary.declared_block_kinds),
            set(ALPHA_ELEMENT_KINDS),
        )

    def test_empty_document_summary_preserves_root_only_boundary(self) -> None:
        source = ConfirmedMarkdownSource.create(
            orientation_object_id="orientation-object-empty",
            orientation_object_version="1",
            source_id="markdown-source-empty",
            source_owner="human-alpha-reviewer",
            source_ref="local:empty.md",
            content="",
            confirmed_by="human-alpha-reviewer",
            confirmed_revision=1,
        )
        representation = MarkdownStructuralRendererAlpha().render(source)
        inventory = inventory_declared_source_elements(representation)

        summary = summarize_declared_structure(inventory)

        self.assertEqual(summary.total_declared_element_count, 1)
        self.assertEqual(summary.ordered_element_kinds, ("document",))
        self.assertEqual(summary.declared_headings, ())
        self.assertEqual(summary.first_canonical_ordinal, 0)
        self.assertEqual(summary.final_canonical_ordinal, 0)
        self.assertEqual(summary.declared_block_kinds, ("document",))
        self.assertEqual(
            summary.absent_block_kinds,
            tuple(kind for kind in ALPHA_ELEMENT_KINDS if kind != "document"),
        )
        self.assertTrue(validate_structural_summary(inventory, summary).valid)

    def test_summary_is_immutable_and_internal(self) -> None:
        import orion
        import orion.understand_structural_summary_alpha as module

        _, inventory = complete_inventory()
        summary = summarize_declared_structure(inventory)

        self.assertIsInstance(summary, StructuralSummaryDiagnostic)
        self.assertTrue(
            all(
                isinstance(heading, DeclaredHeadingSummary)
                for heading in summary.declared_headings
            )
        )
        self.assertEqual(module.__all__, ())
        self.assertNotIn("StructuralSummaryDiagnostic", orion.__all__)
        with self.assertRaises(FrozenInstanceError):
            summary.responsibility_state = "changed"  # type: ignore[misc]
        with self.assertRaises(FrozenInstanceError):
            summary.declared_headings[0].level = 4  # type: ignore[misc]

    def test_summary_replay_is_byte_identical(self) -> None:
        _, inventory = complete_inventory()

        first = summarize_declared_structure(inventory)
        second = summarize_declared_structure(inventory)

        self.assertEqual(first, second)
        self.assertEqual(
            canonical_structural_summary_bytes(first),
            canonical_structural_summary_bytes(second),
        )

    def test_external_conformance_verifies_every_summary_field(self) -> None:
        _, inventory = complete_inventory()
        summary = summarize_declared_structure(inventory)

        conformance = validate_structural_summary(inventory, summary)

        self.assertTrue(conformance.valid)
        self.assertEqual(conformance.errors, ())
        self.assertEqual(
            conformance.checks,
            (
                "input_inventory_valid",
                "summary_shape_valid",
                "deterministic_derivation",
                "diagnostic_identity_and_version",
                "responsibility_and_stop",
                "inventory_reference",
                "orientation_object_lineage",
                "representation_lineage",
                "source_lineage",
                "ordered_structure",
                "heading_declarations",
                "profile_vocabulary_coverage",
                "no_semantic_or_downstream_fields",
            ),
        )

    def test_external_conformance_rejects_tampered_lineage(self) -> None:
        _, inventory = complete_inventory()
        summary = summarize_declared_structure(inventory)
        tampered = replace(summary, source_id="different-source")

        conformance = validate_structural_summary(inventory, tampered)

        self.assertFalse(conformance.valid)
        self.assertIn(
            "Summary differs from deterministic Inventory derivation",
            conformance.errors,
        )
        self.assertIn(
            "source lineage was not preserved",
            conformance.errors,
        )

    def test_summary_rejects_non_inventory_and_invalid_inventory(self) -> None:
        with self.assertRaisesRegex(TypeError, "immutable Source Element Inventory"):
            summarize_declared_structure(object())  # type: ignore[arg-type]

        _, inventory = complete_inventory()
        object.__setattr__(inventory, "ordered_element_count", 999)
        with self.assertRaisesRegex(ValueError, "does not match inventory"):
            summarize_declared_structure(inventory)

    def test_summary_interface_has_no_source_or_renderer_input(self) -> None:
        self.assertEqual(
            tuple(inspect.signature(summarize_declared_structure).parameters),
            ("inventory",),
        )
        module_path = (
            ROOT / "src" / "orion" / "understand_structural_summary_alpha.py"
        )
        tree = ast.parse(module_path.read_text(encoding="utf-8"))
        imported_names = {
            alias.name
            for node in ast.walk(tree)
            if isinstance(node, (ast.Import, ast.ImportFrom))
            for alias in node.names
        }
        self.assertNotIn("ConfirmedMarkdownSource", imported_names)
        self.assertNotIn("MarkdownStructuralRendererAlpha", imported_names)
        self.assertNotIn("Path", imported_names)

    def test_summary_contains_no_semantic_or_downstream_fields(self) -> None:
        _, inventory = complete_inventory()
        summary = summarize_declared_structure(inventory)
        forbidden = {
            "claim",
            "claims",
            "concept",
            "concepts",
            "confidence",
            "content",
            "entities",
            "entity",
            "evidence",
            "intent",
            "meaning",
            "relations",
            "semantic",
            "statistics",
            "summary_text",
            "topic",
            "topics",
        }

        self.assertTrue(forbidden.isdisjoint(nested_keys(asdict(summary))))
        summary_bytes = canonical_structural_summary_bytes(summary)
        self.assertNotIn(b"Orientation", summary_bytes)
        self.assertNotIn(b"A plain paragraph.", summary_bytes)

    def test_canonical_proof_stops_after_summary_and_replays(self) -> None:
        command = [sys.executable, str(PROOF)]
        first = subprocess.run(
            command,
            cwd=ROOT,
            check=False,
            capture_output=True,
        )
        second = subprocess.run(
            command,
            cwd=ROOT,
            check=False,
            capture_output=True,
        )

        self.assertEqual(first.returncode, 0, first.stderr.decode())
        self.assertEqual(second.returncode, 0, second.stderr.decode())
        self.assertEqual(first.stderr, b"")
        self.assertEqual(second.stderr, b"")
        self.assertEqual(first.stdout, second.stdout)
        proof = json.loads(first.stdout)
        self.assertTrue(proof["proof_valid"])
        self.assertEqual(proof["stop"], STOP_AFTER_STRUCTURAL_SUMMARY)
        self.assertTrue(all(proof["verification"].values()))
        self.assertFalse(
            any(
                value
                for key, value in proof["summary_boundary"].items()
                if key != "input"
            )
        )
        self.assertFalse(any(proof["downstream_execution"].values()))


if __name__ == "__main__":
    unittest.main()
