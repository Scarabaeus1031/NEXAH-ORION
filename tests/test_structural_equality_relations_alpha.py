"""Focused tests for WP14 — deterministic Structural Equality Relations."""

from __future__ import annotations

import ast
from collections import Counter
from dataclasses import FrozenInstanceError, asdict, replace
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
import unittest

from orion.markdown_structural_renderer_alpha import MarkdownStructuralRendererAlpha
from orion.sequential_relations_alpha import (
    canonical_sequential_relation_set_bytes,
    generate_sequential_relations,
)
from orion.structural_equality_relations_alpha import (
    COMPLETE_WP14_KIND_ORDER,
    STOP_AFTER_STRUCTURAL_EQUALITY,
    STRUCTURAL_EQUALITY_KINDS,
    StructuralEqualityRelationSet,
    canonical_structural_equality_relation_set_bytes,
    generate_structural_equality_relations,
    structural_equality_relation_set_as_dict,
    structural_equality_relation_set_from_dict,
    validate_structural_equality_relation_set,
)
from orion.structural_relation_alpha import validate_relation_object
from orion.understand_source_element_inventory_alpha import (
    inventory_declared_source_elements,
)
from orion.understand_structural_statistics_alpha import (
    measure_declared_structure,
)
from orion.understand_structural_summary_alpha import (
    summarize_declared_structure,
)


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from slice_iii_structural_equality_proof import (  # noqa: E402
    _confirmed_source,
    build_wp14_proof,
)


PROOF = ROOT / "scripts" / "slice_iii_structural_equality_proof.py"


def artifacts():
    representation = MarkdownStructuralRendererAlpha().render(
        _confirmed_source()
    )
    inventory = inventory_declared_source_elements(representation)
    summary = summarize_declared_structure(inventory)
    statistics = measure_declared_structure(inventory)
    return summary, statistics


def full_relation_set():
    summary, statistics = artifacts()
    return summary, statistics, generate_structural_equality_relations(
        summary,
        statistics,
    )


def nested_keys(value: object) -> set[str]:
    if isinstance(value, dict):
        return set(value).union(
            *(nested_keys(item) for item in value.values())
        )
    if isinstance(value, (tuple, list)):
        return set().union(*(nested_keys(item) for item in value))
    return set()


class StructuralEqualityRelationsAlphaTests(unittest.TestCase):
    def test_same_element_kind_contains_every_unordered_qualifying_pair(
        self,
    ) -> None:
        summary, statistics, relation_set = full_relation_set()
        records = tuple(
            (
                span.element_id,
                summary.ordered_element_kinds[span.ordinal],
            )
            for span in statistics.element_spans
        )
        expected = tuple(
            (source_id, target_id)
            for source_index, (source_id, source_kind) in enumerate(records)
            for target_id, target_kind in records[source_index + 1 :]
            if source_kind == target_kind
        )
        actual = tuple(
            (relation.source_element_id, relation.target_element_id)
            for relation in relation_set.relations
            if relation.relation_kind == "same_element_kind"
        )

        self.assertEqual(actual, expected)
        self.assertEqual(len(actual), 6)

    def test_same_heading_level_uses_only_identical_declared_levels(self) -> None:
        summary, _, relation_set = full_relation_set()
        headings = {
            heading.element_id: heading
            for heading in summary.declared_headings
        }
        relations = tuple(
            relation
            for relation in relation_set.relations
            if relation.relation_kind == "same_heading_level"
        )

        self.assertEqual(len(relations), 1)
        relation = relations[0]
        self.assertEqual(
            headings[relation.source_element_id].level,
            headings[relation.target_element_id].level,
        )
        self.assertEqual(headings[relation.source_element_id].level, 2)

    def test_different_kinds_and_heading_levels_are_never_related(self) -> None:
        summary, statistics, relation_set = full_relation_set()
        kind_by_id = {
            span.element_id: summary.ordered_element_kinds[span.ordinal]
            for span in statistics.element_spans
        }
        heading_by_id = {
            heading.element_id: heading.level
            for heading in summary.declared_headings
        }

        for relation in relation_set.relations:
            if relation.relation_kind == "same_element_kind":
                self.assertEqual(
                    kind_by_id[relation.source_element_id],
                    kind_by_id[relation.target_element_id],
                )
            if relation.relation_kind == "same_heading_level":
                self.assertEqual(
                    heading_by_id[relation.source_element_id],
                    heading_by_id[relation.target_element_id],
                )

    def test_only_equality_kinds_are_added_to_wp13(self) -> None:
        _, _, relation_set = full_relation_set()
        suffix = relation_set.relations[
            relation_set.sequential_relation_count :
        ]

        self.assertEqual(
            set(relation.relation_kind for relation in suffix),
            set(STRUCTURAL_EQUALITY_KINDS),
        )
        self.assertFalse(
            set(relation.relation_kind for relation in relation_set.relations)
            & {"source_reference", "declared_cross_reference"}
        )

    def test_wp13_prefix_is_preserved_byte_identically(self) -> None:
        summary, statistics, relation_set = full_relation_set()
        sequential_set = generate_sequential_relations(summary, statistics)
        prefix = relation_set.relations[
            : relation_set.sequential_relation_count
        ]

        self.assertEqual(prefix, sequential_set.relations)
        self.assertEqual(
            relation_set.sequential_relation_set_ref,
            "sha256:"
            + sha256(
                canonical_sequential_relation_set_bytes(sequential_set)
            ).hexdigest(),
        )

    def test_symmetric_endpoints_use_lower_ordinal_first(self) -> None:
        _, statistics, relation_set = full_relation_set()
        ordinal = {
            span.element_id: span.ordinal for span in statistics.element_spans
        }
        equality_relations = relation_set.relations[
            relation_set.sequential_relation_count :
        ]

        self.assertTrue(
            all(
                ordinal[relation.source_element_id]
                < ordinal[relation.target_element_id]
                for relation in equality_relations
            )
        )

    def test_canonical_order_is_type_first_and_contiguous(self) -> None:
        _, _, relation_set = full_relation_set()
        rank = {
            kind: index for index, kind in enumerate(COMPLETE_WP14_KIND_ORDER)
        }
        kinds = tuple(
            relation.relation_kind for relation in relation_set.relations
        )

        self.assertEqual(
            tuple(relation.canonical_order for relation in relation_set.relations),
            tuple(range(relation_set.relation_count)),
        )
        self.assertEqual(
            tuple(rank[kind] for kind in kinds),
            tuple(sorted(rank[kind] for kind in kinds)),
        )

    def test_duplicate_relation_is_rejected(self) -> None:
        _, _, relation_set = full_relation_set()
        equality = relation_set.relations[
            relation_set.sequential_relation_count
        ]
        duplicate = replace(
            equality,
            canonical_order=relation_set.relation_count,
        )

        with self.assertRaises(ValueError):
            replace(
                relation_set,
                relations=relation_set.relations + (duplicate,),
                equality_relation_count=relation_set.equality_relation_count + 1,
                relation_count=relation_set.relation_count + 1,
            )

    def test_relation_set_is_immutable(self) -> None:
        _, _, relation_set = full_relation_set()

        with self.assertRaises(FrozenInstanceError):
            relation_set.equality_relation_count = 0
        self.assertIsInstance(relation_set.relations, tuple)
        self.assertIsInstance(relation_set, StructuralEqualityRelationSet)

    def test_every_relation_preserves_provenance_and_wp12_validation(
        self,
    ) -> None:
        summary, statistics, relation_set = full_relation_set()

        self.assertTrue(
            all(
                validate_relation_object(
                    summary,
                    statistics,
                    relation,
                ).valid
                for relation in relation_set.relations
            )
        )
        self.assertEqual(
            {
                relation.provenance.structural_summary_ref
                for relation in relation_set.relations
            },
            {relation_set.structural_summary_ref},
        )

    def test_generation_and_serialization_replay_byte_identically(self) -> None:
        summary, statistics = artifacts()
        first = generate_structural_equality_relations(summary, statistics)
        second = generate_structural_equality_relations(summary, statistics)

        self.assertEqual(first, second)
        self.assertEqual(
            canonical_structural_equality_relation_set_bytes(first),
            canonical_structural_equality_relation_set_bytes(second),
        )
        self.assertEqual(
            canonical_structural_equality_relation_set_bytes(first),
            json.dumps(
                asdict(first),
                ensure_ascii=False,
                separators=(",", ":"),
                sort_keys=True,
            ).encode("utf-8"),
        )

    def test_validation_rejects_tampered_identity(self) -> None:
        summary, statistics, relation_set = full_relation_set()
        tampered = replace(
            relation_set,
            relation_set_id="relation-set-000000000000000000000000",
        )

        validation = validate_structural_equality_relation_set(
            summary,
            statistics,
            tampered,
        )
        self.assertFalse(validation.valid)
        self.assertIn(
            "Relation Set differs from deterministic equality generation",
            validation.errors,
        )

    def test_strict_schema_round_trip_rejects_unknown_fields(self) -> None:
        _, _, relation_set = full_relation_set()
        payload = structural_equality_relation_set_as_dict(relation_set)

        self.assertEqual(
            structural_equality_relation_set_from_dict(payload),
            relation_set,
        )
        with self.assertRaises(ValueError):
            structural_equality_relation_set_from_dict(
                {**payload, "semantic_similarity": ()}
            )

    def test_no_semantic_hierarchy_graph_or_navigation_fields_exist(
        self,
    ) -> None:
        _, _, relation_set = full_relation_set()
        keys = nested_keys(asdict(relation_set))
        prohibited = {
            "content",
            "text",
            "topic",
            "concept",
            "entity",
            "claim",
            "evidence",
            "meaning",
            "similarity",
            "parent",
            "child",
            "hierarchy",
            "ranking",
            "recommendation",
            "graph",
            "navigation",
            "orientation_map",
        }

        self.assertFalse(keys & prohibited)

    def test_canonical_proof_reaches_structural_equality_and_stops(
        self,
    ) -> None:
        proof, successful = build_wp14_proof()

        self.assertTrue(successful)
        self.assertTrue(proof["same_element_kind_verified"])
        self.assertTrue(proof["same_heading_level_verified"])
        self.assertTrue(proof["symmetric_endpoint_order_verified"])
        self.assertTrue(proof["duplicates_absent"])
        self.assertTrue(proof["canonical_order_verified"])
        self.assertTrue(proof["sequential_prefix_preserved"])
        self.assertTrue(proof["provenance_verified"])
        self.assertTrue(proof["relation_set_replay_byte_identical"])
        self.assertTrue(proof["forbidden_kinds_absent"])
        self.assertFalse(any(proof["downstream_execution"].values()))
        self.assertEqual(proof["stop"], STOP_AFTER_STRUCTURAL_EQUALITY)

    def test_executable_proof_replays_byte_identically(self) -> None:
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
        self.assertEqual(first.stdout, second.stdout)

    def test_wp14_module_imports_no_source_or_downstream_capability(self) -> None:
        path = ROOT / "src" / "orion" / "structural_equality_relations_alpha.py"
        tree = ast.parse(path.read_text(encoding="utf-8"))
        modules = {
            node.module
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and node.module
        }
        prohibited = (
            "markdown_structural_renderer",
            "source_element_inventory",
            "navigation",
            "orientation_map",
            "gateway",
            "orientation_runtime",
            "lyra",
            "sirius",
        )

        self.assertFalse(
            any(
                fragment in module
                for module in modules
                for fragment in prohibited
            )
        )


if __name__ == "__main__":
    unittest.main()
