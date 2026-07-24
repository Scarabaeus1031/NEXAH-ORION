"""Focused tests for WP12 — immutable atomic Relation Object."""

from __future__ import annotations

import ast
from dataclasses import FrozenInstanceError, asdict, fields, replace
import json
from pathlib import Path
import subprocess
import sys
import unittest

from orion.markdown_structural_renderer_alpha import MarkdownStructuralRendererAlpha
from orion.structural_relation_alpha import (
    PERMITTED_RELATION_KINDS,
    RELATION_SCHEMA_VERSION,
    STOP_AFTER_RELATION_OBJECT,
    RelationObject,
    RelationProvenance,
    canonical_relation_object_bytes,
    create_relation_object,
    relation_object_as_dict,
    relation_object_from_dict,
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

from slice_ii_structural_statistics_proof import _full_source  # noqa: E402
from slice_iii_relation_object_proof import build_wp12_proof  # noqa: E402


PROOF = ROOT / "scripts" / "slice_iii_relation_object_proof.py"


def slice_ii_artifacts():
    representation = MarkdownStructuralRendererAlpha().render(_full_source())
    inventory = inventory_declared_source_elements(representation)
    summary = summarize_declared_structure(inventory)
    statistics = measure_declared_structure(inventory)
    return summary, statistics


def relation_for(
    relation_kind: str = "immediately_precedes",
) -> tuple[object, object, RelationObject]:
    summary, statistics = slice_ii_artifacts()
    source_id = statistics.element_spans[0].element_id
    target_id = statistics.element_spans[1].element_id
    if relation_kind == "source_reference":
        seed = create_relation_object(
            summary,
            statistics,
            relation_kind="immediately_precedes",
            source_element_id=source_id,
            target_element_id=target_id,
            canonical_order=0,
        )
        target_id = seed.provenance.source_boundary_id
    relation = create_relation_object(
        summary,
        statistics,
        relation_kind=relation_kind,
        source_element_id=source_id,
        target_element_id=target_id,
        canonical_order=0,
    )
    return summary, statistics, relation


def nested_keys(value: object) -> set[str]:
    if isinstance(value, dict):
        return set(value).union(
            *(nested_keys(item) for item in value.values())
        )
    if isinstance(value, (tuple, list)):
        return set().union(*(nested_keys(item) for item in value))
    return set()


class StructuralRelationAlphaTests(unittest.TestCase):
    def test_relation_object_has_exact_required_atomic_fields(self) -> None:
        self.assertEqual(
            tuple(field.name for field in fields(RelationObject)),
            (
                "relation_id",
                "relation_kind",
                "source_element_id",
                "target_element_id",
                "provenance",
                "canonical_order",
                "schema_version",
            ),
        )

    def test_all_and_only_frozen_relation_kinds_are_accepted(self) -> None:
        self.assertEqual(
            PERMITTED_RELATION_KINDS,
            (
                "immediately_precedes",
                "immediately_follows",
                "source_reference",
                "same_element_kind",
                "same_heading_level",
                "declared_cross_reference",
            ),
        )
        for kind in PERMITTED_RELATION_KINDS:
            summary, statistics, relation = relation_for(kind)
            self.assertEqual(relation.relation_kind, kind)
            self.assertTrue(
                validate_relation_object(summary, statistics, relation).valid
            )

    def test_relation_and_provenance_are_immutable(self) -> None:
        _, _, relation = relation_for()

        with self.assertRaises(FrozenInstanceError):
            relation.relation_kind = "same_element_kind"
        with self.assertRaises(FrozenInstanceError):
            relation.provenance.source_id = "changed"

    def test_canonical_serialization_is_stable_utf8_json(self) -> None:
        _, _, first = relation_for()
        _, _, second = relation_for()

        first_bytes = canonical_relation_object_bytes(first)
        self.assertEqual(first_bytes, canonical_relation_object_bytes(second))
        self.assertEqual(
            first_bytes,
            json.dumps(
                asdict(first),
                ensure_ascii=False,
                separators=(",", ":"),
                sort_keys=True,
            ).encode("utf-8"),
        )

    def test_identity_changes_for_every_identity_bearing_field(self) -> None:
        summary, statistics, relation = relation_for()
        changed_order = create_relation_object(
            summary,
            statistics,
            relation_kind=relation.relation_kind,
            source_element_id=relation.source_element_id,
            target_element_id=relation.target_element_id,
            canonical_order=1,
        )
        changed_kind = create_relation_object(
            summary,
            statistics,
            relation_kind="immediately_follows",
            source_element_id=relation.source_element_id,
            target_element_id=relation.target_element_id,
            canonical_order=0,
        )

        self.assertNotEqual(relation.relation_id, changed_order.relation_id)
        self.assertNotEqual(relation.relation_id, changed_kind.relation_id)

    def test_schema_round_trip_rejects_unknown_and_missing_fields(self) -> None:
        _, _, relation = relation_for()
        payload = relation_object_as_dict(relation)

        self.assertEqual(relation_object_from_dict(payload), relation)
        with self.assertRaises(ValueError):
            relation_object_from_dict({**payload, "semantic_label": "topic"})
        missing = dict(payload)
        missing.pop("canonical_order")
        with self.assertRaises(ValueError):
            relation_object_from_dict(missing)
        wrong_identity = {
            **payload,
            "relation_id": "relation-000000000000000000000000",
        }
        with self.assertRaises(ValueError):
            relation_object_from_dict(wrong_identity)
        broken_provenance = dict(payload)
        broken_provenance["provenance"] = {
            **payload["provenance"],
            "confidence": 1,
        }
        with self.assertRaises(ValueError):
            relation_object_from_dict(broken_provenance)

    def test_unknown_kind_and_invalid_identifiers_are_rejected(self) -> None:
        summary, statistics, relation = relation_for()
        with self.assertRaises(ValueError):
            create_relation_object(
                summary,
                statistics,
                relation_kind="semantic_similarity",
                source_element_id=relation.source_element_id,
                target_element_id=relation.target_element_id,
                canonical_order=0,
            )
        with self.assertRaises(ValueError):
            create_relation_object(
                summary,
                statistics,
                relation_kind="immediately_precedes",
                source_element_id="not-an-element",
                target_element_id=relation.target_element_id,
                canonical_order=0,
            )
        with self.assertRaises(ValueError):
            create_relation_object(
                summary,
                statistics,
                relation_kind="immediately_precedes",
                source_element_id=relation.source_element_id,
                target_element_id="not-an-element",
                canonical_order=0,
            )

    def test_canonical_order_rejects_negative_and_boolean_values(self) -> None:
        summary, statistics, relation = relation_for()
        for value in (-1, True):
            with self.assertRaises(ValueError):
                create_relation_object(
                    summary,
                    statistics,
                    relation_kind=relation.relation_kind,
                    source_element_id=relation.source_element_id,
                    target_element_id=relation.target_element_id,
                    canonical_order=value,
                )

    def test_validation_rejects_tampered_identity_and_provenance(self) -> None:
        summary, statistics, relation = relation_for()
        tampered_id = replace(
            relation,
            relation_id="relation-000000000000000000000000",
        )
        tampered_provenance = replace(
            relation,
            provenance=replace(
                relation.provenance,
                structural_summary_id="structural-summary-tampered",
            ),
        )

        self.assertFalse(
            validate_relation_object(summary, statistics, tampered_id).valid
        )
        validation = validate_relation_object(
            summary,
            statistics,
            tampered_provenance,
        )
        self.assertFalse(validation.valid)
        self.assertIn(
            "Relation provenance differs from certified Slice II artifacts",
            validation.errors,
        )

    def test_validation_rejects_undeclared_but_well_formed_endpoint(self) -> None:
        summary, statistics, relation = relation_for()
        undeclared = create_relation_object(
            summary,
            statistics,
            relation_kind=relation.relation_kind,
            source_element_id=relation.source_element_id,
            target_element_id="element-ffffffffffffffffffffffff",
            canonical_order=0,
        )

        validation = validate_relation_object(summary, statistics, undeclared)
        self.assertFalse(validation.valid)
        self.assertIn(
            "Relation target endpoint is not declared by Structural Statistics",
            validation.errors,
        )

    def test_source_reference_requires_exact_source_boundary(self) -> None:
        summary, statistics, relation = relation_for("source_reference")
        self.assertEqual(
            relation.target_element_id,
            relation.provenance.source_boundary_id,
        )
        self.assertTrue(
            validate_relation_object(summary, statistics, relation).valid
        )
        with self.assertRaises(ValueError):
            create_relation_object(
                summary,
                statistics,
                relation_kind="source_reference",
                source_element_id=relation.source_element_id,
                target_element_id=statistics.element_spans[1].element_id,
                canonical_order=0,
            )

    def test_no_semantic_graph_navigation_or_source_content_fields_exist(
        self,
    ) -> None:
        _, _, relation = relation_for()
        keys = nested_keys(asdict(relation))
        prohibited = {
            "content",
            "text",
            "topic",
            "concept",
            "entity",
            "claim",
            "evidence",
            "meaning",
            "confidence",
            "ranking",
            "recommendation",
            "relations",
            "graph",
            "navigation",
            "orientation_map",
        }

        self.assertFalse(keys & prohibited)

    def test_proof_reaches_relation_object_and_stops(self) -> None:
        proof, successful = build_wp12_proof()

        self.assertTrue(successful)
        self.assertTrue(proof["successful"])
        self.assertEqual(proof["schema_version"], RELATION_SCHEMA_VERSION)
        self.assertEqual(proof["stop"], STOP_AFTER_RELATION_OBJECT)
        self.assertTrue(proof["validation"]["valid"])
        self.assertTrue(proof["provenance_verified"])
        self.assertTrue(proof["relation_replay_byte_identical"])
        self.assertFalse(any(proof["downstream_execution"].values()))

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

    def test_wp12_module_and_proof_import_no_downstream_capability(self) -> None:
        paths = (
            ROOT / "src" / "orion" / "structural_relation_alpha.py",
            PROOF,
        )
        prohibited = (
            "navigation",
            "orientation_map",
            "gateway",
            "orientation_runtime",
            "lyra",
            "sirius",
        )
        for path in paths:
            tree = ast.parse(path.read_text(encoding="utf-8"))
            modules = {
                node.module
                for node in ast.walk(tree)
                if isinstance(node, ast.ImportFrom) and node.module
            }
            self.assertFalse(
                any(
                    fragment in module
                    for module in modules
                    for fragment in prohibited
                )
            )


if __name__ == "__main__":
    unittest.main()
