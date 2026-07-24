"""Focused tests for WP13 — deterministic Sequential Relations."""

from __future__ import annotations

import ast
from dataclasses import FrozenInstanceError, asdict, replace
import json
from pathlib import Path
import subprocess
import sys
import unittest

from orion.markdown_structural_renderer_alpha import MarkdownStructuralRendererAlpha
from orion.sequential_relations_alpha import (
    SEQUENTIAL_RELATION_KINDS,
    SEQUENTIAL_RELATION_SET_SCHEMA_VERSION,
    STOP_AFTER_SEQUENTIAL_RELATIONS,
    SequentialRelationSet,
    canonical_sequential_relation_set_bytes,
    generate_sequential_relations,
    sequential_relation_set_as_dict,
    sequential_relation_set_from_dict,
    validate_sequential_relation_set,
)
from orion.structural_relation_alpha import (
    RELATION_SCHEMA_VERSION,
    RelationObject,
    validate_relation_object,
)
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

from slice_ii_structural_statistics_proof import (  # noqa: E402
    _empty_source,
    _full_source,
)
from slice_iii_sequential_relations_proof import (  # noqa: E402
    build_wp13_proof,
)


PROOF = ROOT / "scripts" / "slice_iii_sequential_relations_proof.py"


def artifacts(source=None):
    source = _full_source() if source is None else source
    representation = MarkdownStructuralRendererAlpha().render(source)
    inventory = inventory_declared_source_elements(representation)
    summary = summarize_declared_structure(inventory)
    statistics = measure_declared_structure(inventory)
    return summary, statistics


def full_relation_set():
    summary, statistics = artifacts()
    return summary, statistics, generate_sequential_relations(
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


class SequentialRelationsAlphaTests(unittest.TestCase):
    def test_every_adjacent_pair_produces_exact_inverse_relations(self) -> None:
        _, statistics, relation_set = full_relation_set()
        spans = statistics.element_spans
        pairs = tuple(zip(spans, spans[1:]))
        pair_count = len(pairs)

        self.assertEqual(relation_set.relation_count, pair_count * 2)
        self.assertEqual(
            tuple(
                (
                    relation.source_element_id,
                    relation.target_element_id,
                )
                for relation in relation_set.relations[:pair_count]
            ),
            tuple(
                (source.element_id, target.element_id)
                for source, target in pairs
            ),
        )
        self.assertEqual(
            tuple(
                (
                    relation.source_element_id,
                    relation.target_element_id,
                )
                for relation in relation_set.relations[pair_count:]
            ),
            tuple(
                (target.element_id, source.element_id)
                for source, target in pairs
            ),
        )

    def test_only_two_sequential_kinds_are_generated(self) -> None:
        _, _, relation_set = full_relation_set()
        kinds = tuple(
            relation.relation_kind for relation in relation_set.relations
        )
        pair_count = relation_set.relation_count // 2

        self.assertEqual(
            kinds,
            ("immediately_precedes",) * pair_count
            + ("immediately_follows",) * pair_count,
        )
        self.assertEqual(set(kinds), set(SEQUENTIAL_RELATION_KINDS))
        self.assertFalse(
            set(kinds)
            & {
                "same_element_kind",
                "same_heading_level",
                "source_reference",
                "declared_cross_reference",
            }
        )

    def test_canonical_order_is_contiguous_and_type_first(self) -> None:
        _, _, relation_set = full_relation_set()

        self.assertEqual(
            tuple(
                relation.canonical_order
                for relation in relation_set.relations
            ),
            tuple(range(relation_set.relation_count)),
        )
        self.assertEqual(
            relation_set.schema_version,
            SEQUENTIAL_RELATION_SET_SCHEMA_VERSION,
        )

    def test_first_and_last_boundaries_have_no_invented_neighbour(self) -> None:
        _, statistics, relation_set = full_relation_set()
        first = statistics.element_spans[0].element_id
        last = statistics.element_spans[-1].element_id

        self.assertFalse(
            any(
                relation.relation_kind == "immediately_follows"
                and relation.source_element_id == first
                for relation in relation_set.relations
            )
        )
        self.assertFalse(
            any(
                relation.relation_kind == "immediately_precedes"
                and relation.source_element_id == last
                for relation in relation_set.relations
            )
        )

    def test_no_gap_or_transitive_relation_is_generated(self) -> None:
        _, statistics, relation_set = full_relation_set()
        ordinal_by_id = {
            span.element_id: span.ordinal
            for span in statistics.element_spans
        }

        for relation in relation_set.relations:
            source = ordinal_by_id[relation.source_element_id]
            target = ordinal_by_id[relation.target_element_id]
            expected_delta = (
                1
                if relation.relation_kind == "immediately_precedes"
                else -1
            )
            self.assertEqual(target - source, expected_delta)

    def test_duplicate_relations_are_rejected(self) -> None:
        _, _, relation_set = full_relation_set()
        first = relation_set.relations[0]
        duplicate_at_next_order = replace(first, canonical_order=1)

        with self.assertRaises(ValueError):
            replace(
                relation_set,
                relations=(first, duplicate_at_next_order),
                relation_count=2,
            )

    def test_relation_set_and_relation_objects_are_immutable(self) -> None:
        _, _, relation_set = full_relation_set()

        with self.assertRaises(FrozenInstanceError):
            relation_set.relation_count = 0
        with self.assertRaises(FrozenInstanceError):
            relation_set.relations[0].relation_kind = "same_element_kind"
        self.assertIsInstance(relation_set.relations, tuple)
        self.assertTrue(
            all(
                isinstance(relation, RelationObject)
                for relation in relation_set.relations
            )
        )

    def test_every_relation_preserves_wp12_contract_and_provenance(self) -> None:
        summary, statistics, relation_set = full_relation_set()

        self.assertTrue(
            all(
                relation.schema_version == RELATION_SCHEMA_VERSION
                and validate_relation_object(
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
        self.assertEqual(
            {
                relation.provenance.structural_statistics_ref
                for relation in relation_set.relations
            },
            {relation_set.structural_statistics_ref},
        )

    def test_generation_and_serialization_replay_byte_identically(self) -> None:
        summary, statistics = artifacts()
        first = generate_sequential_relations(summary, statistics)
        second = generate_sequential_relations(summary, statistics)

        self.assertEqual(first, second)
        self.assertEqual(
            canonical_sequential_relation_set_bytes(first),
            canonical_sequential_relation_set_bytes(second),
        )
        self.assertEqual(
            canonical_sequential_relation_set_bytes(first),
            json.dumps(
                asdict(first),
                ensure_ascii=False,
                separators=(",", ":"),
                sort_keys=True,
            ).encode("utf-8"),
        )

    def test_empty_document_produces_an_empty_candidate_set(self) -> None:
        summary, statistics = artifacts(_empty_source())

        relation_set = generate_sequential_relations(summary, statistics)

        self.assertEqual(relation_set.relation_count, 0)
        self.assertEqual(relation_set.relations, ())
        self.assertTrue(
            validate_sequential_relation_set(
                summary,
                statistics,
                relation_set,
            ).valid
        )

    def test_set_validation_rejects_tampered_identity(self) -> None:
        summary, statistics, relation_set = full_relation_set()
        tampered = replace(
            relation_set,
            relation_set_id="relation-set-000000000000000000000000",
        )

        validation = validate_sequential_relation_set(
            summary,
            statistics,
            tampered,
        )
        self.assertFalse(validation.valid)
        self.assertIn(
            "Relation Set differs from deterministic adjacency generation",
            validation.errors,
        )

    def test_strict_schema_round_trip_rejects_unknown_fields(self) -> None:
        _, _, relation_set = full_relation_set()
        payload = sequential_relation_set_as_dict(relation_set)

        self.assertEqual(
            sequential_relation_set_from_dict(payload),
            relation_set,
        )
        with self.assertRaises(ValueError):
            sequential_relation_set_from_dict(
                {**payload, "graph": {"nodes": []}}
            )
        wrong_id = {
            **payload,
            "relation_set_id": "relation-set-000000000000000000000000",
        }
        with self.assertRaises(ValueError):
            sequential_relation_set_from_dict(wrong_id)

    def test_no_source_semantic_graph_or_navigation_fields_exist(self) -> None:
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
            "hierarchy",
            "ranking",
            "recommendation",
            "graph",
            "navigation",
            "orientation_map",
        }

        self.assertFalse(keys & prohibited)

    def test_canonical_proof_reaches_sequential_relations_and_stops(
        self,
    ) -> None:
        proof, successful = build_wp13_proof()

        self.assertTrue(successful)
        self.assertTrue(proof["successful"])
        self.assertTrue(proof["adjacency_verified"])
        self.assertTrue(proof["duplicates_absent"])
        self.assertTrue(proof["boundary_verified"])
        self.assertTrue(proof["canonical_order_verified"])
        self.assertTrue(proof["provenance_verified"])
        self.assertTrue(proof["relation_set_replay_byte_identical"])
        self.assertTrue(proof["forbidden_kinds_absent"])
        self.assertFalse(any(proof["downstream_execution"].values()))
        self.assertEqual(proof["stop"], STOP_AFTER_SEQUENTIAL_RELATIONS)

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

    def test_wp13_module_imports_no_source_or_downstream_capability(self) -> None:
        path = ROOT / "src" / "orion" / "sequential_relations_alpha.py"
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
