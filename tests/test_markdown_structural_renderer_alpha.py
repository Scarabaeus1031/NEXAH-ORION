"""Tests for the Markdown Structural Renderer reference Alpha."""

from __future__ import annotations

import ast
from dataclasses import FrozenInstanceError, asdict
from pathlib import Path
import subprocess
import sys
import unittest

from orion.markdown_structural_renderer_alpha import (
    ALPHA_ELEMENT_KINDS,
    ConfirmedMarkdownSource,
    MarkdownStructuralRendererAlpha,
    canonical_representation_bytes,
    validate_markdown_structural_representation,
)


ROOT = Path(__file__).resolve().parent.parent
PROOF = ROOT / "scripts" / "markdown_structural_renderer_alpha_proof.py"
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


def confirmed_source(content: str = SOURCE_CONTENT) -> ConfirmedMarkdownSource:
    return ConfirmedMarkdownSource.create(
        orientation_object_id="orientation-object-alpha",
        orientation_object_version="1",
        source_id="markdown-source-alpha",
        source_owner="human-alpha-reviewer",
        source_ref="local:orientation.md",
        content=content,
        confirmed_by="human-alpha-reviewer",
        confirmed_revision=1,
    )


class MarkdownStructuralRendererAlphaTests(unittest.TestCase):
    def setUp(self) -> None:
        self.source = confirmed_source()
        self.renderer = MarkdownStructuralRendererAlpha()

    def test_projection_preserves_slice_i_document_heading_and_paragraph(self) -> None:
        mapping = self.renderer.project(self.source)

        self.assertEqual(
            tuple(block.element_kind for block in mapping.blocks),
            (
                "document",
                "atx_heading",
                "paragraph",
                "atx_heading",
                "paragraph",
            ),
        )
        self.assertEqual(
            tuple(block.ordinal for block in mapping.blocks),
            (0, 1, 2, 3, 4),
        )
        self.assertEqual(
            tuple(block.level for block in mapping.blocks),
            (None, 1, None, 3, None),
        )
        self.assertTrue(
            set(block.element_kind for block in mapping.blocks).issubset(
                ALPHA_ELEMENT_KINDS
            )
        )

    def test_projection_derives_canonical_full_line_locators(self) -> None:
        mapping = self.renderer.project(self.source)

        self.assertEqual(
            tuple(asdict(block.locator) for block in mapping.blocks),
            (
                {
                    "start_byte": 0,
                    "end_byte": 116,
                    "start_line": 1,
                    "end_line": 8,
                },
                {
                    "start_byte": 0,
                    "end_byte": 14,
                    "start_line": 1,
                    "end_line": 1,
                },
                {
                    "start_byte": 15,
                    "end_byte": 75,
                    "start_line": 3,
                    "end_line": 4,
                },
                {
                    "start_byte": 76,
                    "end_byte": 89,
                    "start_line": 6,
                    "end_line": 6,
                },
                {
                    "start_byte": 90,
                    "end_byte": 116,
                    "start_line": 8,
                    "end_line": 8,
                },
            ),
        )

    def test_utf8_locators_use_bytes_not_code_points(self) -> None:
        source = confirmed_source("# Maßstab\n\nÄnderung bleibt sichtbar.\n")
        mapping = self.renderer.project(source)

        heading = mapping.blocks[1]
        paragraph = mapping.blocks[2]
        self.assertEqual(heading.locator.start_byte, 0)
        self.assertEqual(
            heading.locator.end_byte,
            len("# Maßstab\n".encode("utf-8")),
        )
        self.assertEqual(
            paragraph.locator.start_byte,
            len("# Maßstab\n\n".encode("utf-8")),
        )
        self.assertEqual(
            paragraph.locator.end_byte,
            len(source.content.encode("utf-8")),
        )

    def test_empty_source_produces_only_zero_width_document(self) -> None:
        source = confirmed_source("")
        representation = self.renderer.render(source)

        self.assertEqual(len(representation.elements), 1)
        document = representation.elements[0]
        self.assertEqual(document.element_kind, "document")
        self.assertEqual(document.ordinal, 0)
        self.assertEqual(
            asdict(document.locator),
            {
                "start_byte": 0,
                "end_byte": 0,
                "start_line": 1,
                "end_line": 1,
            },
        )

    def test_identical_input_produces_byte_identical_representation(self) -> None:
        first = self.renderer.render(self.source)
        second = self.renderer.render(confirmed_source())

        self.assertEqual(first, second)
        self.assertEqual(
            canonical_representation_bytes(first),
            canonical_representation_bytes(second),
        )
        self.assertEqual(
            first.representation_id,
            "representation-7bdb85d76e6b9a8d",
        )
        self.assertEqual(
            first.representation_version,
            "sha256:0cfe0b88b38415de949efd720bb6cbc48a919230dbed51260ef0015592586723",
        )
        self.assertEqual(
            tuple(element.element_id for element in first.elements),
            (
                "element-7fc58ef6c4d0dce49638a642",
                "element-430556706e37ea26ea746f40",
                "element-8fad73d957fd0d4e5423ecd2",
                "element-657bfb8e7607a211dce059de",
                "element-feb3190cea005113506aa2f3",
            ),
        )

    def test_representation_and_nested_elements_are_immutable(self) -> None:
        representation = self.renderer.render(self.source)

        with self.assertRaises(FrozenInstanceError):
            representation.renderer_version = "changed"  # type: ignore[misc]
        with self.assertRaises(FrozenInstanceError):
            representation.elements[0].ordinal = 9  # type: ignore[misc]

    def test_source_edit_changes_elements_and_representation_version(self) -> None:
        original = self.renderer.render(self.source)
        changed = self.renderer.render(
            confirmed_source(f"{SOURCE_CONTENT}\nOne more paragraph.\n")
        )

        self.assertNotEqual(changed.source.revision, original.source.revision)
        self.assertNotEqual(
            changed.elements[0].element_id,
            original.elements[0].element_id,
        )
        self.assertNotEqual(
            changed.representation_version,
            original.representation_version,
        )

    def test_commonmark_atx_boundary_is_deterministic(self) -> None:
        source = confirmed_source(
            "   ###### Accepted\n"
            "\n"
            "####### This remains a paragraph.\n"
        )
        mapping = self.renderer.project(source)

        self.assertEqual(
            tuple(block.element_kind for block in mapping.blocks),
            ("document", "atx_heading", "paragraph"),
        )
        self.assertEqual(mapping.blocks[1].level, 6)

    def test_block_quote_projection_preserves_lazy_and_nested_containers(self) -> None:
        source = confirmed_source(
            "> quoted\n"
            "lazy continuation\n"
            ">\n"
            "> > nested\n"
        )

        mapping = self.renderer.project(source)

        self.assertEqual(
            tuple(block.element_kind for block in mapping.blocks),
            (
                "document",
                "block_quote",
                "paragraph",
                "block_quote",
                "paragraph",
            ),
        )
        self.assertEqual(
            tuple(asdict(block.locator) for block in mapping.blocks[1:]),
            (
                {
                    "start_byte": 0,
                    "end_byte": len(source.content.encode("utf-8")),
                    "start_line": 1,
                    "end_line": 4,
                },
                {
                    "start_byte": 0,
                    "end_byte": len(
                        "> quoted\nlazy continuation\n".encode("utf-8")
                    ),
                    "start_line": 1,
                    "end_line": 2,
                },
                {
                    "start_byte": len(
                        "> quoted\nlazy continuation\n>\n".encode("utf-8")
                    ),
                    "end_byte": len(source.content.encode("utf-8")),
                    "start_line": 4,
                    "end_line": 4,
                },
                {
                    "start_byte": len(
                        "> quoted\nlazy continuation\n>\n".encode("utf-8")
                    ),
                    "end_byte": len(source.content.encode("utf-8")),
                    "start_line": 4,
                    "end_line": 4,
                },
            ),
        )

    def test_block_quote_lazy_continuation_stops_before_new_block(self) -> None:
        mapping = self.renderer.project(
            confirmed_source(
                "> quoted\n"
                "lazy continuation\n"
                "# outside\n"
            )
        )

        self.assertEqual(
            tuple(block.element_kind for block in mapping.blocks),
            ("document", "block_quote", "paragraph", "atx_heading"),
        )
        self.assertEqual(mapping.blocks[1].locator.end_line, 2)
        self.assertEqual(mapping.blocks[3].locator.start_line, 3)

    def test_atomic_list_family_uses_depth_first_preorder(self) -> None:
        source = confirmed_source(
            "1. first\n"
            "2. second\n"
            "   - nested\n"
            "\n"
            "+ other\n"
        )

        mapping = self.renderer.project(source)

        self.assertEqual(
            tuple(block.element_kind for block in mapping.blocks),
            (
                "document",
                "ordered_list",
                "list_item",
                "paragraph",
                "list_item",
                "paragraph",
                "unordered_list",
                "list_item",
                "paragraph",
                "unordered_list",
                "list_item",
                "paragraph",
            ),
        )
        self.assertEqual(
            tuple(block.ordinal for block in mapping.blocks),
            tuple(range(len(mapping.blocks))),
        )
        self.assertEqual(
            (mapping.blocks[1].locator.start_line, mapping.blocks[1].locator.end_line),
            (1, 4),
        )
        self.assertEqual(
            (mapping.blocks[6].locator.start_line, mapping.blocks[6].locator.end_line),
            (3, 4),
        )
        self.assertEqual(
            (mapping.blocks[9].locator.start_line, mapping.blocks[9].locator.end_line),
            (5, 5),
        )

    def test_list_marker_changes_create_distinct_containers(self) -> None:
        mapping = self.renderer.project(
            confirmed_source("- first\n+ second\n1. ordered\n2) separate\n")
        )

        self.assertEqual(
            tuple(
                block.element_kind
                for block in mapping.blocks
                if block.element_kind in {"ordered_list", "unordered_list"}
            ),
            (
                "unordered_list",
                "unordered_list",
                "ordered_list",
                "ordered_list",
            ),
        )

    def test_ordered_list_paragraph_interruption_requires_start_number_one(
        self,
    ) -> None:
        mapping = self.renderer.project(
            confirmed_source(
                "Paragraph\n"
                "2. remains paragraph text\n"
                "\n"
                "2. begins after a blank line\n"
            )
        )

        self.assertEqual(
            tuple(block.element_kind for block in mapping.blocks),
            (
                "document",
                "paragraph",
                "ordered_list",
                "list_item",
                "paragraph",
            ),
        )
        self.assertEqual(mapping.blocks[1].locator.end_line, 2)
        self.assertEqual(mapping.blocks[2].locator.start_line, 4)

    def test_empty_list_item_exists_but_does_not_interrupt_paragraph(self) -> None:
        mapping = self.renderer.project(
            confirmed_source(
                "Paragraph\n"
                "+\n"
                "\n"
                "+\n"
            )
        )

        self.assertEqual(
            tuple(block.element_kind for block in mapping.blocks),
            ("document", "paragraph", "unordered_list", "list_item"),
        )
        self.assertEqual(mapping.blocks[1].locator.end_line, 2)
        self.assertEqual(mapping.blocks[3].locator.start_line, 4)

    def test_list_marker_with_five_spaces_creates_nested_indented_code(
        self,
    ) -> None:
        mapping = self.renderer.project(
            confirmed_source("-     content after marker\n")
        )

        self.assertEqual(
            tuple(block.element_kind for block in mapping.blocks),
            (
                "document",
                "unordered_list",
                "list_item",
                "indented_code_block",
            ),
        )
        self.assertEqual(mapping.blocks[1].locator, mapping.blocks[3].locator)

    def test_thematic_break_projection_respects_list_precedence(self) -> None:
        mapping = self.renderer.project(
            confirmed_source("***\n\n- item\n\n- - -\n")
        )

        self.assertEqual(
            tuple(block.element_kind for block in mapping.blocks),
            (
                "document",
                "thematic_break",
                "unordered_list",
                "list_item",
                "paragraph",
                "thematic_break",
            ),
        )
        self.assertEqual(mapping.blocks[1].locator.start_line, 1)
        self.assertEqual(mapping.blocks[5].locator.start_line, 5)

    def test_marker_like_text_remains_paragraph_content(self) -> None:
        mapping = self.renderer.project(
            confirmed_source(
                "Escaped \\\\> marker.\n"
                "1234567890. too many digits\n"
                "-- not a break\n"
                "*-* mixed markers\n"
            )
        )

        self.assertEqual(
            tuple(block.element_kind for block in mapping.blocks),
            ("document", "paragraph"),
        )

    def test_fenced_code_blocks_preserve_closed_and_unclosed_extents(self) -> None:
        source = confirmed_source(
            "```text\n"
            "code\n"
            "````\n"
            "\n"
            "~~~\n"
            "unclosed\n"
        )

        mapping = self.renderer.project(source)

        self.assertEqual(
            tuple(block.element_kind for block in mapping.blocks),
            ("document", "fenced_code_block", "fenced_code_block"),
        )
        self.assertEqual(
            (mapping.blocks[1].locator.start_line, mapping.blocks[1].locator.end_line),
            (1, 3),
        )
        self.assertEqual(
            (mapping.blocks[2].locator.start_line, mapping.blocks[2].locator.end_line),
            (5, 6),
        )

    def test_short_fence_does_not_close_longer_opening_fence(self) -> None:
        mapping = self.renderer.project(
            confirmed_source(
                "````\n"
                "content\n"
                "```\n"
                "still content\n"
                "`````\n"
            )
        )

        self.assertEqual(
            tuple(block.element_kind for block in mapping.blocks),
            ("document", "fenced_code_block"),
        )
        self.assertEqual(mapping.blocks[1].locator.end_line, 5)

    def test_fenced_code_blocks_work_inside_existing_containers(self) -> None:
        mapping = self.renderer.project(
            confirmed_source(
                "> ```\n"
                "> quoted code\n"
                "> ```\n"
                "\n"
                "- ~~~\n"
                "  listed code\n"
                "  ~~~\n"
            )
        )

        self.assertEqual(
            tuple(block.element_kind for block in mapping.blocks),
            (
                "document",
                "block_quote",
                "fenced_code_block",
                "unordered_list",
                "list_item",
                "fenced_code_block",
            ),
        )

    def test_backtick_in_backtick_fence_info_prevents_fence_recognition(
        self,
    ) -> None:
        mapping = self.renderer.project(
            confirmed_source("``` info`invalid\nordinary text\n")
        )

        self.assertEqual(
            tuple(block.element_kind for block in mapping.blocks),
            ("document", "paragraph"),
        )

    def test_indented_code_block_preserves_internal_but_not_trailing_blanks(
        self,
    ) -> None:
        mapping = self.renderer.project(
            confirmed_source(
                "    first\n"
                "\n"
                "\tsecond\n"
                "\n"
                "paragraph\n"
            )
        )

        self.assertEqual(
            tuple(block.element_kind for block in mapping.blocks),
            ("document", "indented_code_block", "paragraph"),
        )
        self.assertEqual(
            (mapping.blocks[1].locator.start_line, mapping.blocks[1].locator.end_line),
            (1, 3),
        )
        self.assertEqual(mapping.blocks[2].locator.start_line, 5)

    def test_indentation_cannot_interrupt_a_paragraph(self) -> None:
        mapping = self.renderer.project(
            confirmed_source(
                "Paragraph\n"
                "    remains paragraph continuation\n"
            )
        )

        self.assertEqual(
            tuple(block.element_kind for block in mapping.blocks),
            ("document", "paragraph"),
        )
        self.assertEqual(mapping.blocks[1].locator.end_line, 2)

    def test_setext_heading_levels_and_multiline_extent(self) -> None:
        mapping = self.renderer.project(
            confirmed_source(
                "Primary\n"
                "=======\n"
                "\n"
                "Secondary line one\n"
                "line two\n"
                "---\n"
            )
        )

        self.assertEqual(
            tuple(block.element_kind for block in mapping.blocks),
            ("document", "setext_heading", "setext_heading"),
        )
        self.assertEqual(
            tuple(block.level for block in mapping.blocks),
            (None, 1, 2),
        )
        self.assertEqual(
            (mapping.blocks[2].locator.start_line, mapping.blocks[2].locator.end_line),
            (4, 6),
        )

    def test_setext_heading_works_inside_block_quote(self) -> None:
        mapping = self.renderer.project(
            confirmed_source(
                "> Heading\n"
                "> ---\n"
            )
        )

        self.assertEqual(
            tuple(block.element_kind for block in mapping.blocks),
            ("document", "block_quote", "setext_heading"),
        )
        self.assertEqual(mapping.blocks[2].level, 2)
        self.assertEqual(mapping.blocks[1].locator, mapping.blocks[2].locator)

    def test_thematic_break_without_preceding_paragraph_remains_break(self) -> None:
        mapping = self.renderer.project(confirmed_source("---\n"))

        self.assertEqual(
            tuple(block.element_kind for block in mapping.blocks),
            ("document", "thematic_break"),
        )

    def test_only_excluded_html_blocks_fail_after_structural_expansion(self) -> None:
        with self.assertRaisesRegex(
            ValueError,
            "outside Renderer Alpha scope: html_block",
        ):
            self.renderer.render(
                confirmed_source("<div>\ntext\n</div>\n")
            )

    def test_link_reference_definitions_are_omitted_not_rejected(self) -> None:
        mapping = self.renderer.project(
            confirmed_source(
                "[source]: https://example.com\n"
                "\n"
                "Visible paragraph.\n"
            )
        )

        self.assertEqual(
            tuple(block.element_kind for block in mapping.blocks),
            ("document", "paragraph"),
        )
        self.assertEqual(mapping.blocks[1].locator.start_line, 3)

    def test_new_block_kinds_are_immutable_and_externally_conformant(self) -> None:
        source = confirmed_source(
            "> quote\n"
            "\n"
            "1. ordered\n"
            "\n"
            "- unordered\n"
            "\n"
            "***\n"
            "\n"
            "```text\n"
            "code\n"
            "```\n"
            "\n"
            "    indented\n"
            "\n"
            "Setext\n"
            "---\n"
        )
        representation = self.renderer.render(source)
        replay = self.renderer.render(source)
        conformance = validate_markdown_structural_representation(
            source,
            representation,
        )

        self.assertTrue(conformance.valid)
        self.assertEqual(conformance.errors, ())
        self.assertEqual(
            canonical_representation_bytes(representation),
            canonical_representation_bytes(replay),
        )
        self.assertTrue(
            {
                "block_quote",
                "ordered_list",
                "unordered_list",
                "list_item",
                "thematic_break",
                "fenced_code_block",
                "indented_code_block",
                "setext_heading",
            }.issubset(
                {element.element_kind for element in representation.elements}
            )
        )
        with self.assertRaises(FrozenInstanceError):
            representation.elements[1].ordinal = 99  # type: ignore[misc]

    def test_invalid_profile_source_domain_fails_without_repair(self) -> None:
        invalid_sources = {
            "bom": "\ufeff# Heading\n",
            "carriage_return": "# Heading\r\n",
            "null": "Paragraph\x00\n",
            "surrogate": "Paragraph\ud800\n",
        }

        for label, content in invalid_sources.items():
            with self.subTest(label=label):
                with self.assertRaises(ValueError):
                    confirmed_source(content)

    def test_external_conformance_replays_all_deterministic_outputs(self) -> None:
        representation = self.renderer.render(self.source)
        conformance = validate_markdown_structural_representation(
            self.source,
            representation,
            renderer=self.renderer,
        )

        self.assertTrue(conformance.valid)
        self.assertEqual(conformance.errors, ())
        self.assertIn("deterministic_replay", conformance.checks)
        self.assertIn("canonical_ordinals", conformance.checks)
        self.assertIn("supported_element_vocabulary", conformance.checks)
        self.assertIn("canonical_locator_bounds", conformance.checks)
        self.assertIn("one_to_one_projected_declarations", conformance.checks)
        self.assertIn("deterministic_element_identities", conformance.checks)
        self.assertIn("unique_element_identities", conformance.checks)
        self.assertIn(
            "no_orientation_or_understand_semantics",
            conformance.checks,
        )

    def test_tampered_element_fails_external_conformance(self) -> None:
        representation = self.renderer.render(self.source)
        object.__setattr__(representation.elements[1], "element_id", "element-tampered")

        conformance = validate_markdown_structural_representation(
            self.source,
            representation,
        )

        self.assertFalse(conformance.valid)
        self.assertIn(
            "Representation differs from deterministic replay",
            conformance.errors,
        )
        self.assertIn(
            "Structural element identity mismatch",
            conformance.errors,
        )

    def test_alpha_stays_outside_runtime_gateway_and_understand(self) -> None:
        import orion

        self.assertNotIn("MarkdownStructuralRendererAlpha", orion.__all__)
        path = ROOT / "src" / "orion" / "markdown_structural_renderer_alpha.py"
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        imported_modules = set()
        forbidden_io = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_modules.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                imported_modules.add(node.module or "")
            elif (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and node.func.attr
                in {"read_text", "read_bytes", "write_text", "write_bytes"}
            ):
                forbidden_io.add(node.func.attr)
            elif (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id == "open"
            ):
                forbidden_io.add(node.func.id)

        self.assertTrue(
            {
                "orion.gateway",
                "orion.orientation_runtime",
                "orion.understand_stage1_alpha",
                "orion.understand_representation_inventory_alpha",
                "orion.understand_source_boundary_inventory_alpha",
                "orion.understand_source_element_declaration_check_alpha",
                "openai",
                "anthropic",
                "ollama",
                "requests",
                "urllib",
            }.isdisjoint(imported_modules)
        )
        self.assertEqual(forbidden_io, set())

    def test_executable_proof_is_reproducible(self) -> None:
        first = subprocess.run(
            [sys.executable, str(PROOF)],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        second = subprocess.run(
            [sys.executable, str(PROOF)],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

        self.assertEqual(first.stdout, second.stdout)
        self.assertIn('"valid": true', first.stdout)
        self.assertIn('"stop": "after_immutable_representation"', first.stdout)


if __name__ == "__main__":
    unittest.main()
