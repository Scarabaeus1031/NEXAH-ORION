"""Tests for the bounded UNDERSTAND Structural Statistics Alpha."""

from __future__ import annotations

import ast
from collections import Counter
from dataclasses import FrozenInstanceError, asdict, replace
from pathlib import Path
import subprocess
import sys
import unittest

from orion.markdown_structural_renderer_alpha import (
    MarkdownStructuralRendererAlpha,
    SourceLocator,
)
from orion.understand_source_element_inventory_alpha import (
    inventory_declared_source_elements,
)
from orion.understand_structural_statistics_alpha import (
    CONTAINER_KINDS,
    HEADING_LEVEL_KEYS,
    PROFILE_V1_VOCABULARY,
    STOP_AFTER_STRUCTURAL_STATISTICS,
    DeclaredCoverage,
    DocumentByteBoundary,
    ElementKindCount,
    ElementStructuralSpan,
    HeadingLevelCount,
    StructuralStatisticsDiagnostic,
    canonical_structural_statistics_bytes,
    measure_declared_structure,
    validate_structural_statistics,
)


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from slice_ii_structural_statistics_proof import (  # noqa: E402
    _empty_source,
    _full_source,
)


PROOF = ROOT / "scripts" / "slice_ii_structural_statistics_proof.py"


def inventory_for(source):
    representation = MarkdownStructuralRendererAlpha().render(source)
    return representation, inventory_declared_source_elements(representation)


def full_inventory():
    return inventory_for(_full_source())


def nested_keys(value: object) -> set[str]:
    if isinstance(value, dict):
        return set(value).union(*(nested_keys(item) for item in value.values()))
    if isinstance(value, (tuple, list)):
        return set().union(*(nested_keys(item) for item in value))
    return set()


class UnderstandStructuralStatisticsAlphaTests(unittest.TestCase):
    def test_statistics_exactly_measure_complete_inventory(self) -> None:
        _, inventory = full_inventory()

        statistics = measure_declared_structure(inventory)

        expected_counts = Counter(
            element.element_kind for element in inventory.elements
        )
        self.assertEqual(statistics.total_ordered_elements, 23)
        self.assertEqual(
            tuple(
                (entry.element_kind, entry.count)
                for entry in statistics.count_by_element_kind
            ),
            tuple(
                (kind, expected_counts[kind])
                for kind in PROFILE_V1_VOCABULARY
            ),
        )
        self.assertEqual(
            tuple(
                (entry.element_kind, entry.level, entry.count)
                for entry in statistics.heading_level_distribution
            ),
            (
                ("atx_heading", 1, 1),
                ("atx_heading", 2, 0),
                ("atx_heading", 3, 0),
                ("atx_heading", 4, 0),
                ("atx_heading", 5, 0),
                ("atx_heading", 6, 0),
                ("setext_heading", 1, 0),
                ("setext_heading", 2, 1),
            ),
        )
        expected_containers = sum(
            expected_counts[kind] for kind in CONTAINER_KINDS
        )
        self.assertEqual(statistics.declared_container_kind_count, 11)
        self.assertEqual(
            statistics.declared_container_kind_count,
            expected_containers,
        )
        self.assertEqual(statistics.declared_leaf_kind_count, 12)
        self.assertEqual(
            statistics.declared_container_kind_count
            + statistics.declared_leaf_kind_count,
            statistics.total_ordered_elements,
        )
        self.assertEqual(statistics.first_canonical_ordinal, 0)
        self.assertEqual(statistics.final_canonical_ordinal, 22)
        self.assertEqual(statistics.present_block_kind_count, 11)
        self.assertEqual(statistics.absent_block_kind_count, 0)
        self.assertEqual(statistics.nesting_depth, "unavailable")
        self.assertEqual(
            statistics.stop,
            STOP_AFTER_STRUCTURAL_STATISTICS,
        )

    def test_spans_derive_from_exact_locators(self) -> None:
        _, inventory = full_inventory()

        statistics = measure_declared_structure(inventory)

        expected = tuple(
            (
                element.element_id,
                element.ordinal,
                element.locator.end_byte - element.locator.start_byte,
                (
                    0
                    if element.locator.end_byte == element.locator.start_byte
                    else (
                        element.locator.end_line
                        - element.locator.start_line
                        + 1
                    )
                ),
            )
            for element in inventory.elements
        )
        self.assertEqual(
            tuple(
                (
                    span.element_id,
                    span.ordinal,
                    span.byte_span,
                    span.physical_line_span,
                )
                for span in statistics.element_spans
            ),
            expected,
        )

    def test_interval_union_does_not_double_count_overlapping_locators(
        self,
    ) -> None:
        _, inventory = full_inventory()

        statistics = measure_declared_structure(inventory)

        covered_byte_positions = set()
        covered_lines = set()
        for element in inventory.elements[1:]:
            covered_byte_positions.update(
                range(
                    element.locator.start_byte,
                    element.locator.end_byte,
                )
            )
            if element.locator.end_byte > element.locator.start_byte:
                covered_lines.update(
                    range(
                        element.locator.start_line,
                        element.locator.end_line + 1,
                    )
                )
        document = inventory.elements[0].locator
        self.assertEqual(
            statistics.non_document_byte_coverage.covered,
            len(covered_byte_positions),
        )
        self.assertEqual(
            statistics.non_document_byte_coverage.available,
            document.end_byte - document.start_byte,
        )
        self.assertEqual(
            statistics.non_document_line_coverage.covered,
            len(covered_lines),
        )
        self.assertGreater(
            sum(span.byte_span for span in statistics.element_spans[1:]),
            statistics.non_document_byte_coverage.covered,
        )

    def test_blank_lines_remain_explicitly_uncovered(self) -> None:
        _, inventory = full_inventory()

        statistics = measure_declared_structure(inventory)

        self.assertEqual(
            statistics.non_document_byte_coverage,
            DeclaredCoverage(covered=250, available=256, uncovered=6),
        )
        self.assertEqual(
            statistics.non_document_line_coverage,
            DeclaredCoverage(covered=18, available=24, uncovered=6),
        )

    def test_utf8_is_measured_only_through_byte_locators(self) -> None:
        source = _full_source()
        representation, inventory = inventory_for(source)

        statistics = measure_declared_structure(inventory)

        utf8_width = len(source.content.encode("utf-8"))
        self.assertGreater(utf8_width, len(source.content))
        self.assertEqual(
            statistics.document_byte_boundary,
            DocumentByteBoundary(
                start_byte=0,
                end_byte=utf8_width,
                byte_width=utf8_width,
            ),
        )
        self.assertEqual(
            statistics.source_integrity,
            representation.source.content_sha256,
        )
        self.assertNotIn("content", asdict(statistics))

    def test_empty_document_has_zero_coverage_and_unavailable_depth(self) -> None:
        _, inventory = inventory_for(_empty_source())

        statistics = measure_declared_structure(inventory)

        self.assertEqual(statistics.total_ordered_elements, 1)
        self.assertEqual(
            tuple(entry.count for entry in statistics.count_by_element_kind),
            (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        )
        self.assertEqual(
            statistics.document_byte_boundary,
            DocumentByteBoundary(start_byte=0, end_byte=0, byte_width=0),
        )
        self.assertEqual(
            statistics.non_document_byte_coverage,
            DeclaredCoverage(covered=0, available=0, uncovered=0),
        )
        self.assertEqual(
            statistics.non_document_line_coverage,
            DeclaredCoverage(covered=0, available=0, uncovered=0),
        )
        self.assertEqual(statistics.element_spans[0].byte_span, 0)
        self.assertEqual(statistics.element_spans[0].physical_line_span, 0)
        self.assertEqual(statistics.nesting_depth, "unavailable")

    def test_statistics_preserves_complete_lineage(self) -> None:
        representation, inventory = full_inventory()

        statistics = measure_declared_structure(inventory)

        self.assertEqual(
            (
                statistics.orientation_object_id,
                statistics.orientation_object_version,
            ),
            (
                inventory.orientation_object_id,
                inventory.orientation_object_version,
            ),
        )
        self.assertEqual(
            (
                statistics.representation_id,
                statistics.representation_version,
                statistics.representation_integrity,
            ),
            (
                representation.representation_id,
                representation.representation_version,
                representation.representation_sha256,
            ),
        )
        self.assertEqual(
            (
                statistics.source_id,
                statistics.source_revision,
                statistics.source_integrity,
                statistics.source_boundary,
            ),
            (
                inventory.source_id,
                inventory.source_revision,
                inventory.source_integrity,
                inventory.source_boundary,
            ),
        )

    def test_statistics_is_immutable_internal_and_canonically_ordered(
        self,
    ) -> None:
        import orion
        import orion.understand_structural_statistics_alpha as module

        _, inventory = full_inventory()
        statistics = measure_declared_structure(inventory)

        self.assertIsInstance(statistics, StructuralStatisticsDiagnostic)
        self.assertTrue(
            all(
                isinstance(entry, ElementKindCount)
                for entry in statistics.count_by_element_kind
            )
        )
        self.assertTrue(
            all(
                isinstance(entry, HeadingLevelCount)
                for entry in statistics.heading_level_distribution
            )
        )
        self.assertTrue(
            all(
                isinstance(entry, ElementStructuralSpan)
                for entry in statistics.element_spans
            )
        )
        self.assertEqual(
            tuple(
                entry.element_kind
                for entry in statistics.count_by_element_kind
            ),
            PROFILE_V1_VOCABULARY,
        )
        self.assertEqual(
            tuple(
                (entry.element_kind, entry.level)
                for entry in statistics.heading_level_distribution
            ),
            HEADING_LEVEL_KEYS,
        )
        self.assertEqual(module.__all__, ())
        self.assertNotIn("StructuralStatisticsDiagnostic", orion.__all__)
        with self.assertRaises(FrozenInstanceError):
            statistics.nesting_depth = "changed"  # type: ignore[misc]
        with self.assertRaises(FrozenInstanceError):
            statistics.element_spans[0].byte_span = 1  # type: ignore[misc]

    def test_statistics_replay_is_byte_identical(self) -> None:
        _, inventory = full_inventory()

        first = measure_declared_structure(inventory)
        second = measure_declared_structure(inventory)

        self.assertEqual(first, second)
        self.assertEqual(
            canonical_structural_statistics_bytes(first),
            canonical_structural_statistics_bytes(second),
        )

    def test_external_conformance_verifies_all_measurement_groups(self) -> None:
        _, inventory = full_inventory()
        statistics = measure_declared_structure(inventory)

        conformance = validate_structural_statistics(inventory, statistics)

        self.assertTrue(conformance.valid)
        self.assertEqual(conformance.errors, ())
        self.assertEqual(
            conformance.checks,
            (
                "input_inventory_valid",
                "statistics_shape_valid",
                "deterministic_measurement",
                "diagnostic_identity_and_version",
                "responsibility_and_stop",
                "inventory_reference",
                "orientation_object_lineage",
                "representation_lineage",
                "source_lineage",
                "element_measurements",
                "coverage_measurements",
                "nesting_depth_unavailable",
                "no_semantic_relation_or_navigation_fields",
            ),
        )

    def test_external_conformance_rejects_tampered_statistics(self) -> None:
        _, inventory = full_inventory()
        statistics = measure_declared_structure(inventory)
        tampered = replace(statistics, source_id="different-source")

        conformance = validate_structural_statistics(inventory, tampered)

        self.assertFalse(conformance.valid)
        self.assertIn(
            "Statistics differs from deterministic Inventory measurement",
            conformance.errors,
        )
        self.assertIn("source lineage was not preserved", conformance.errors)

    def test_statistics_rejects_invalid_input_and_broken_ordinals(self) -> None:
        with self.assertRaisesRegex(
            TypeError,
            "immutable Source Element Inventory",
        ):
            measure_declared_structure(object())  # type: ignore[arg-type]

        _, inventory = full_inventory()
        object.__setattr__(inventory.elements[1], "ordinal", 99)
        with self.assertRaisesRegex(ValueError, "ordinals must remain canonical"):
            measure_declared_structure(inventory)

    def test_statistics_rejects_unknown_kind_and_invalid_heading_level(
        self,
    ) -> None:
        _, unknown_inventory = full_inventory()
        object.__setattr__(
            unknown_inventory.elements[1],
            "element_kind",
            "unknown",
        )
        with self.assertRaisesRegex(ValueError, "outside the accepted Renderer"):
            measure_declared_structure(unknown_inventory)

        _, invalid_heading_inventory = full_inventory()
        object.__setattr__(invalid_heading_inventory.elements[1], "level", 7)
        with self.assertRaisesRegex(ValueError, "level must be 1 through 6"):
            measure_declared_structure(invalid_heading_inventory)

    def test_statistics_rejects_locator_outside_document_boundary(self) -> None:
        _, inventory = full_inventory()
        document = inventory.elements[0].locator
        outside = replace(
            inventory.elements[1],
            locator=SourceLocator(
                start_byte=inventory.elements[1].locator.start_byte,
                end_byte=document.end_byte + 1,
                start_line=inventory.elements[1].locator.start_line,
                end_line=document.end_line,
            ),
        )
        tampered = replace(
            inventory,
            elements=(inventory.elements[0], outside, *inventory.elements[2:]),
        )

        with self.assertRaisesRegex(ValueError, "outside document byte boundary"):
            measure_declared_structure(tampered)

    def test_statistics_interface_has_no_source_or_representation_input(
        self,
    ) -> None:
        import inspect

        self.assertEqual(
            tuple(inspect.signature(measure_declared_structure).parameters),
            ("inventory",),
        )
        module_path = (
            ROOT / "src" / "orion" / "understand_structural_statistics_alpha.py"
        )
        tree = ast.parse(module_path.read_text(encoding="utf-8"))
        imported_names = {
            alias.name
            for node in ast.walk(tree)
            if isinstance(node, (ast.Import, ast.ImportFrom))
            for alias in node.names
        }
        self.assertNotIn("ConfirmedMarkdownSource", imported_names)
        self.assertNotIn("ImmutableMarkdownStructuralRepresentation", imported_names)
        self.assertNotIn("MarkdownStructuralRendererAlpha", imported_names)
        self.assertNotIn("Path", imported_names)

    def test_statistics_contains_no_source_semantics_or_relations(self) -> None:
        source = _full_source()
        _, inventory = inventory_for(source)
        statistics = measure_declared_structure(inventory)
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
            "navigation",
            "relations",
            "semantic",
            "summary_text",
            "topic",
            "topics",
        }

        self.assertTrue(forbidden.isdisjoint(nested_keys(asdict(statistics))))
        statistics_bytes = canonical_structural_statistics_bytes(statistics)
        self.assertNotIn("orientation — café".encode(), statistics_bytes)
        self.assertNotIn(b"Quoted paragraph.", statistics_bytes)

    def test_canonical_proof_replays_and_stops_after_statistics(self) -> None:
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
        proof = __import__("json").loads(first.stdout)
        self.assertTrue(proof["proof_valid"])
        self.assertEqual(proof["stop"], STOP_AFTER_STRUCTURAL_STATISTICS)
        self.assertEqual(
            tuple(case["case"] for case in proof["cases"]),
            ("complete_vocabulary_utf8", "empty_document"),
        )
        self.assertTrue(
            all(
                all(case["verification"].values()) and case["valid"]
                for case in proof["cases"]
            )
        )
        self.assertFalse(
            any(
                value
                for key, value in proof["statistics_boundary"].items()
                if key != "input"
            )
        )
        self.assertFalse(any(proof["downstream_execution"].values()))


if __name__ == "__main__":
    unittest.main()
