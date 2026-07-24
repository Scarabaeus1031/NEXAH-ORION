"""Tests for the UNDERSTAND Source Element Inventory Alpha."""

from __future__ import annotations

import ast
from dataclasses import FrozenInstanceError, asdict
import inspect
import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

from orion.markdown_structural_renderer_alpha import (
    ConfirmedMarkdownSource,
    MarkdownStructuralRendererAlpha,
)
from orion.understand_source_element_inventory_alpha import (
    DeclaredSourceElementInventoryDiagnostic,
    DeclaredSourceElementInventoryEntry,
    canonical_inventory_bytes,
    inventory_declared_source_elements,
)


ROOT = Path(__file__).resolve().parent.parent
PROOF = ROOT / "scripts" / "understand_source_element_inventory_alpha_proof.py"
REPRESENTATION_FIXTURE = (
    ROOT
    / "examples"
    / "markdown_structural_renderer_alpha"
    / "immutable_representation.json"
)
SOURCE_CONTENT = (
    "# Orientation\n"
    "\n"
    "Information already exists.\n"
    "Orientation is what is missing.\n"
    "\n"
    "### Continue\n"
    "\n"
    "Bring one exact question.\n"
)


def immutable_representation():
    source = ConfirmedMarkdownSource.create(
        orientation_object_id="orientation-object-alpha",
        orientation_object_version="1",
        source_id="markdown-source-alpha",
        source_owner="human-alpha-reviewer",
        source_ref="local:orientation.md",
        content=SOURCE_CONTENT,
        confirmed_by="human-alpha-reviewer",
        confirmed_revision=1,
    )
    return MarkdownStructuralRendererAlpha().render(source)


def sprint_01_representation():
    source = ConfirmedMarkdownSource.create(
        orientation_object_id="orientation-object-slice-ii",
        orientation_object_version="1",
        source_id="markdown-source-slice-ii",
        source_owner="human-alpha-reviewer",
        source_ref="local:slice-ii.md",
        content=(
            "> quote\n"
            "\n"
            "1. ordered\n"
            "2. second\n"
            "   - nested\n"
            "\n"
            "+ unordered\n"
            "\n"
            "***\n"
        ),
        confirmed_by="human-alpha-reviewer",
        confirmed_revision=1,
    )
    return MarkdownStructuralRendererAlpha().render(source)


def sprint_02_representation():
    source = ConfirmedMarkdownSource.create(
        orientation_object_id="orientation-object-slice-ii-sprint-02",
        orientation_object_version="1",
        source_id="markdown-source-slice-ii-sprint-02",
        source_owner="human-alpha-reviewer",
        source_ref="local:slice-ii-sprint-02.md",
        content=(
            "```text\n"
            "fenced\n"
            "```\n"
            "\n"
            "    indented\n"
            "\n"
            "Primary\n"
            "=======\n"
            "\n"
            "Secondary\n"
            "---\n"
        ),
        confirmed_by="human-alpha-reviewer",
        confirmed_revision=1,
    )
    return MarkdownStructuralRendererAlpha().render(source)


def execute_proof() -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(PROOF)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )


def nested_keys(value: object) -> set[str]:
    if isinstance(value, dict):
        return set(value).union(*(nested_keys(item) for item in value.values()))
    if isinstance(value, (tuple, list)):
        return set().union(*(nested_keys(item) for item in value))
    return set()


class UnderstandSourceElementInventoryAlphaTests(unittest.TestCase):
    def test_inventory_preserves_declared_order_identity_and_locators(self) -> None:
        representation = immutable_representation()

        inventory = inventory_declared_source_elements(representation)

        self.assertEqual(inventory.canonical_stage, "understand/2")
        self.assertEqual(
            inventory.responsibility,
            "declared_source_element_inventory",
        )
        self.assertEqual(
            inventory.input_boundary,
            "immutable_structural_representation",
        )
        self.assertEqual(inventory.ordered_element_count, 5)
        self.assertEqual(
            tuple(element.element_kind for element in inventory.elements),
            (
                "document",
                "atx_heading",
                "paragraph",
                "atx_heading",
                "paragraph",
            ),
        )
        self.assertEqual(
            tuple(element.ordinal for element in inventory.elements),
            (0, 1, 2, 3, 4),
        )
        self.assertEqual(
            tuple(element.element_id for element in inventory.elements),
            tuple(element.element_id for element in representation.elements),
        )
        self.assertEqual(
            tuple(element.locator for element in inventory.elements),
            tuple(element.locator for element in representation.elements),
        )
        self.assertTrue(
            all(
                inventory_element.locator is representation_element.locator
                for inventory_element, representation_element in zip(
                    inventory.elements,
                    representation.elements,
                    strict=True,
                )
            )
        )
        self.assertEqual(
            tuple(element.level for element in inventory.elements),
            (None, 1, None, 3, None),
        )
        self.assertEqual(inventory.responsibility_state, "completed")
        self.assertEqual(inventory.canonical_stage_state, "incomplete")
        self.assertEqual(
            inventory.stop,
            "after_declared_source_element_inventory",
        )

    def test_inventory_preserves_representation_and_source_lineage(self) -> None:
        representation = immutable_representation()

        inventory = inventory_declared_source_elements(representation)

        self.assertEqual(
            (
                inventory.orientation_object_id,
                inventory.orientation_object_version,
            ),
            (
                representation.orientation_object_id,
                representation.orientation_object_version,
            ),
        )
        self.assertEqual(
            (
                inventory.representation_id,
                inventory.representation_version,
                inventory.representation_integrity,
            ),
            (
                representation.representation_id,
                representation.representation_version,
                representation.representation_sha256,
            ),
        )
        self.assertEqual(inventory.source_id, representation.source.entry_id)
        self.assertEqual(
            inventory.source_revision,
            representation.source.revision,
        )
        self.assertEqual(
            inventory.source_integrity,
            representation.source.content_sha256,
        )
        self.assertEqual(inventory.source_boundary, representation.boundary_ref)

    def test_inventory_preserves_sprint_01_vocabulary_without_discovery(self) -> None:
        representation = sprint_01_representation()

        inventory = inventory_declared_source_elements(representation)

        self.assertEqual(
            tuple(element.element_kind for element in inventory.elements),
            tuple(element.element_kind for element in representation.elements),
        )
        self.assertTrue(
            {
                "block_quote",
                "ordered_list",
                "unordered_list",
                "list_item",
                "thematic_break",
            }.issubset({element.element_kind for element in inventory.elements})
        )
        self.assertEqual(
            tuple(element.element_id for element in inventory.elements),
            tuple(element.element_id for element in representation.elements),
        )
        self.assertEqual(
            tuple(element.locator for element in inventory.elements),
            tuple(element.locator for element in representation.elements),
        )
        self.assertEqual(
            canonical_inventory_bytes(inventory),
            canonical_inventory_bytes(
                inventory_declared_source_elements(representation)
            ),
        )

    def test_inventory_preserves_sprint_02_vocabulary_and_heading_levels(
        self,
    ) -> None:
        representation = sprint_02_representation()

        inventory = inventory_declared_source_elements(representation)

        self.assertEqual(
            tuple(element.element_kind for element in inventory.elements),
            (
                "document",
                "fenced_code_block",
                "indented_code_block",
                "setext_heading",
                "setext_heading",
            ),
        )
        self.assertEqual(
            tuple(element.level for element in inventory.elements),
            (None, None, None, 1, 2),
        )
        self.assertEqual(
            tuple(element.element_id for element in inventory.elements),
            tuple(element.element_id for element in representation.elements),
        )
        self.assertEqual(
            tuple(element.locator for element in inventory.elements),
            tuple(element.locator for element in representation.elements),
        )
        self.assertEqual(
            canonical_inventory_bytes(inventory),
            canonical_inventory_bytes(
                inventory_declared_source_elements(representation)
            ),
        )

    def test_inventory_is_immutable_and_internal(self) -> None:
        import orion
        import orion.understand_source_element_inventory_alpha as module

        inventory = inventory_declared_source_elements(immutable_representation())

        self.assertIsInstance(
            inventory,
            DeclaredSourceElementInventoryDiagnostic,
        )
        self.assertTrue(
            all(
                isinstance(element, DeclaredSourceElementInventoryEntry)
                for element in inventory.elements
            )
        )
        self.assertEqual(module.__all__, ())
        self.assertNotIn(
            "DeclaredSourceElementInventoryDiagnostic",
            orion.__all__,
        )
        with self.assertRaises(FrozenInstanceError):
            inventory.responsibility_state = "changed"  # type: ignore[misc]
        with self.assertRaises(FrozenInstanceError):
            inventory.elements[0].ordinal = 9  # type: ignore[misc]

    def test_repeated_inventory_is_byte_identical(self) -> None:
        representation = immutable_representation()

        first = inventory_declared_source_elements(representation)
        second = inventory_declared_source_elements(representation)

        self.assertEqual(first, second)
        self.assertEqual(
            canonical_inventory_bytes(first),
            canonical_inventory_bytes(second),
        )

    def test_inventory_requires_only_immutable_representation(self) -> None:
        self.assertEqual(
            tuple(inspect.signature(inventory_declared_source_elements).parameters),
            ("representation",),
        )
        with self.assertRaisesRegex(
            TypeError,
            "immutable Structural Representation",
        ):
            inventory_declared_source_elements({})  # type: ignore[arg-type]

    def test_inventory_never_executes_projection_renderer_or_io(self) -> None:
        representation = immutable_representation()

        with (
            patch(
                "builtins.open",
                side_effect=AssertionError("filesystem access is forbidden"),
            ),
            patch.object(
                MarkdownStructuralRendererAlpha,
                "project",
                side_effect=AssertionError("Projection execution is forbidden"),
            ),
            patch.object(
                MarkdownStructuralRendererAlpha,
                "render",
                side_effect=AssertionError("Renderer execution is forbidden"),
            ),
        ):
            inventory = inventory_declared_source_elements(representation)

        self.assertEqual(inventory.ordered_element_count, 5)

    def test_inventory_contains_no_raw_material_or_downstream_semantics(self) -> None:
        value = asdict(
            inventory_declared_source_elements(immutable_representation())
        )
        keys = nested_keys(value)

        self.assertTrue(
            {
                "content",
                "payload",
                "markdown",
                "concepts",
                "evidence",
                "findings",
                "summary",
                "report",
                "continuations",
                "confidence",
            }.isdisjoint(keys)
        )

    def test_changed_declared_order_is_rejected_not_repaired(self) -> None:
        representation = immutable_representation()
        object.__setattr__(representation.elements[1], "ordinal", 9)

        with self.assertRaisesRegex(ValueError, "ordinals must be contiguous"):
            inventory_declared_source_elements(representation)

    def test_source_has_no_parser_io_projection_or_renderer_execution(self) -> None:
        module_path = (
            ROOT
            / "src"
            / "orion"
            / "understand_source_element_inventory_alpha.py"
        )
        source = module_path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(module_path))
        imports: set[str] = set()
        calls: set[str] = set()
        attributes: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                imports.add(node.module or "")
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    calls.add(node.func.id)
                elif isinstance(node.func, ast.Attribute):
                    calls.add(node.func.attr)
            elif isinstance(node, ast.Attribute):
                attributes.add(node.attr)

        self.assertTrue(
            {
                "pathlib",
                "os",
                "re",
                "html",
                "markdown",
                "markdown_it",
                "commonmark",
                "orion.gateway",
                "orion.orientation_runtime",
                "orion.public_contracts",
            }.isdisjoint(imports)
        )
        self.assertTrue(
            {
                "open",
                "read",
                "read_text",
                "read_bytes",
                "match",
                "search",
                "findall",
                "loads",
                "project",
                "render",
                "orient",
            }.isdisjoint(calls)
        )
        self.assertTrue({"content", "payload"}.isdisjoint(attributes))

    def test_fixture_contains_representation_but_no_raw_markdown(self) -> None:
        value = json.loads(REPRESENTATION_FIXTURE.read_text(encoding="utf-8"))

        self.assertEqual(
            value["representation_id"],
            "representation-7bdb85d76e6b9a8d",
        )
        self.assertNotIn("content", nested_keys(value))
        self.assertEqual(len(value["elements"]), 5)

    def test_executable_proof_consumes_only_frozen_representation(self) -> None:
        result = execute_proof()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        proof = json.loads(result.stdout)
        inventory = proof["inventory"]
        self.assertEqual(
            proof["diagnostic_kind"],
            "internal_declared_source_element_inventory",
        )
        self.assertEqual(inventory["ordered_element_count"], 5)
        self.assertEqual(
            [element["element_id"] for element in inventory["elements"]],
            [
                "element-7fc58ef6c4d0dce49638a642",
                "element-430556706e37ea26ea746f40",
                "element-8fad73d957fd0d4e5423ecd2",
                "element-657bfb8e7607a211dce059de",
                "element-feb3190cea005113506aa2f3",
            ],
        )
        self.assertTrue(proof["determinism"]["byte_identical_replay"])
        self.assertFalse(proof["raw_markdown_available"])
        self.assertFalse(proof["raw_markdown_accessed"])
        self.assertFalse(proof["projection_executed"])
        self.assertFalse(proof["renderer_executed"])
        self.assertFalse(proof["structure_created"])
        self.assertFalse(proof["runtime_executed"])
        self.assertFalse(proof["gateway_executed"])
        self.assertEqual(proof["semantic_processing"], "none")
        self.assertEqual(
            proof["stop"],
            "after_declared_source_element_inventory",
        )

    def test_executable_proof_is_byte_identical(self) -> None:
        first = execute_proof()
        second = execute_proof()

        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(first.stdout, second.stdout)


if __name__ == "__main__":
    unittest.main()
