"""Focused tests for WP15 deterministic declared-reference Relations."""

from __future__ import annotations

import ast
from dataclasses import FrozenInstanceError, asdict, replace
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
import unittest

from orion.declared_cross_references_alpha import (
    COMPLETE_RELATION_KIND_ORDER,
    STOP_AFTER_DECLARED_CROSS_REFERENCES,
    AcceptedDeclaredCrossReference,
    DeclaredReferenceRelationSet,
    accepted_declared_cross_reference_from_dict,
    canonical_declared_cross_reference_bytes,
    canonical_declared_reference_relation_set_bytes,
    declared_cross_reference_from_explicit_values,
    declared_reference_relation_set_as_dict,
    declared_reference_relation_set_from_dict,
    generate_declared_reference_relations,
    validate_declared_reference_relation_set,
)
from orion.markdown_structural_renderer_alpha import (
    MarkdownStructuralRendererAlpha,
)
from orion.structural_equality_relations_alpha import (
    generate_structural_equality_relations,
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

from slice_iii_declared_cross_references_proof import (  # noqa: E402
    build_wp15_proof,
)
from slice_iii_structural_equality_proof import _confirmed_source  # noqa: E402


PROOF = ROOT / "scripts" / "slice_iii_declared_cross_references_proof.py"


def artifacts():
    representation = MarkdownStructuralRendererAlpha().render(
        _confirmed_source()
    )
    inventory = inventory_declared_source_elements(representation)
    summary = summarize_declared_structure(inventory)
    statistics = measure_declared_structure(inventory)
    return summary, statistics


def declaration_for(summary, statistics):
    return declared_cross_reference_from_explicit_values(
        declaration_version="1",
        source_element_id=statistics.element_spans[1].element_id,
        target_element_id=statistics.element_spans[3].element_id,
        provenance_ref=summary.input_inventory_ref,
    )


class DeclaredCrossReferencesAlphaTests(unittest.TestCase):
    def test_every_element_receives_one_exact_source_reference(self) -> None:
        summary, statistics = artifacts()
        relation_set = generate_declared_reference_relations(
            summary,
            statistics,
        )
        source_relations = tuple(
            relation
            for relation in relation_set.relations
            if relation.relation_kind == "source_reference"
        )

        self.assertEqual(
            tuple(relation.source_element_id for relation in source_relations),
            tuple(span.element_id for span in statistics.element_spans),
        )
        self.assertEqual(len(source_relations), statistics.total_ordered_elements)
        self.assertTrue(
            all(
                relation.target_element_id
                == relation.provenance.source_boundary_id
                for relation in source_relations
            )
        )

    def test_profile_v1_absence_produces_no_cross_reference(self) -> None:
        summary, statistics = artifacts()
        relation_set = generate_declared_reference_relations(
            summary,
            statistics,
        )

        self.assertEqual(relation_set.accepted_declaration_refs, ())
        self.assertEqual(relation_set.declared_cross_reference_count, 0)
        self.assertFalse(
            any(
                relation.relation_kind == "declared_cross_reference"
                for relation in relation_set.relations
            )
        )

    def test_one_explicit_declaration_produces_exactly_one_relation(self) -> None:
        summary, statistics = artifacts()
        declaration = declaration_for(summary, statistics)
        relation_set = generate_declared_reference_relations(
            summary,
            statistics,
            (declaration,),
        )
        cross_relations = tuple(
            relation
            for relation in relation_set.relations
            if relation.relation_kind == "declared_cross_reference"
        )

        self.assertEqual(len(cross_relations), 1)
        self.assertEqual(
            (
                cross_relations[0].source_element_id,
                cross_relations[0].target_element_id,
            ),
            (
                declaration.source_element_id,
                declaration.target_element_id,
            ),
        )
        self.assertEqual(
            relation_set.accepted_declaration_refs,
            (
                "sha256:"
                + sha256(
                    canonical_declared_cross_reference_bytes(declaration)
                ).hexdigest(),
            ),
        )

    def test_raw_or_inferred_pair_is_rejected(self) -> None:
        summary, statistics = artifacts()

        with self.assertRaises(TypeError):
            generate_declared_reference_relations(
                summary,
                statistics,
                (
                    {
                        "source_element_id": (
                            statistics.element_spans[0].element_id
                        ),
                        "target_element_id": (
                            statistics.element_spans[1].element_id
                        ),
                    },
                ),
            )

    def test_unresolved_declaration_endpoint_is_rejected(self) -> None:
        summary, statistics = artifacts()
        declaration = declared_cross_reference_from_explicit_values(
            declaration_version="1",
            source_element_id=statistics.element_spans[1].element_id,
            target_element_id="element-000000000000000000000000",
            provenance_ref=summary.input_inventory_ref,
        )

        with self.assertRaisesRegex(ValueError, "unresolved"):
            generate_declared_reference_relations(
                summary,
                statistics,
                (declaration,),
            )

    def test_tampered_declaration_integrity_is_rejected(self) -> None:
        summary, statistics = artifacts()
        declaration = declaration_for(summary, statistics)

        with self.assertRaisesRegex(ValueError, "integrity"):
            generate_declared_reference_relations(
                summary,
                statistics,
                (replace(declaration, declaration_integrity="0" * 64),),
            )

    def test_declaration_with_different_inventory_provenance_is_rejected(
        self,
    ) -> None:
        summary, statistics = artifacts()
        declaration = declared_cross_reference_from_explicit_values(
            declaration_version="1",
            source_element_id=statistics.element_spans[1].element_id,
            target_element_id=statistics.element_spans[3].element_id,
            provenance_ref="sha256:" + "0" * 64,
        )

        with self.assertRaisesRegex(ValueError, "accepted Inventory"):
            generate_declared_reference_relations(
                summary,
                statistics,
                (declaration,),
            )

    def test_duplicate_declaration_is_rejected(self) -> None:
        summary, statistics = artifacts()
        declaration = declaration_for(summary, statistics)

        with self.assertRaisesRegex(ValueError, "duplicate"):
            generate_declared_reference_relations(
                summary,
                statistics,
                (declaration, declaration),
            )

    def test_wp14_relation_facts_are_preserved_without_rediscovery(self) -> None:
        summary, statistics = artifacts()
        wp14 = generate_structural_equality_relations(summary, statistics)
        complete = generate_declared_reference_relations(summary, statistics)
        prior_kinds = {
            "immediately_precedes",
            "immediately_follows",
            "same_element_kind",
            "same_heading_level",
        }

        self.assertEqual(
            {
                (
                    relation.relation_kind,
                    relation.source_element_id,
                    relation.target_element_id,
                )
                for relation in wp14.relations
            },
            {
                (
                    relation.relation_kind,
                    relation.source_element_id,
                    relation.target_element_id,
                )
                for relation in complete.relations
                if relation.relation_kind in prior_kinds
            },
        )

    def test_complete_candidate_has_canonical_type_and_ordinal_order(self) -> None:
        summary, statistics = artifacts()
        declaration = declaration_for(summary, statistics)
        relation_set = generate_declared_reference_relations(
            summary,
            statistics,
            (declaration,),
        )
        rank = {
            kind: index for index, kind in enumerate(COMPLETE_RELATION_KIND_ORDER)
        }

        self.assertEqual(
            tuple(
                relation.canonical_order for relation in relation_set.relations
            ),
            tuple(range(relation_set.relation_count)),
        )
        self.assertEqual(
            tuple(
                rank[relation.relation_kind]
                for relation in relation_set.relations
            ),
            tuple(
                sorted(
                    rank[relation.relation_kind]
                    for relation in relation_set.relations
                )
            ),
        )

    def test_declaration_input_order_does_not_change_candidate(self) -> None:
        summary, statistics = artifacts()
        first = declaration_for(summary, statistics)
        second = declared_cross_reference_from_explicit_values(
            declaration_version="1",
            source_element_id=statistics.element_spans[2].element_id,
            target_element_id=statistics.element_spans[5].element_id,
            provenance_ref=summary.input_inventory_ref,
        )

        forward = generate_declared_reference_relations(
            summary,
            statistics,
            (first, second),
        )
        reverse = generate_declared_reference_relations(
            summary,
            statistics,
            (second, first),
        )

        self.assertEqual(forward, reverse)
        self.assertEqual(
            canonical_declared_reference_relation_set_bytes(forward),
            canonical_declared_reference_relation_set_bytes(reverse),
        )

    def test_only_reference_kinds_are_new_in_wp15(self) -> None:
        summary, statistics = artifacts()
        declaration = declaration_for(summary, statistics)
        wp14 = generate_structural_equality_relations(summary, statistics)
        complete = generate_declared_reference_relations(
            summary,
            statistics,
            (declaration,),
        )
        old_triples = {
            (
                relation.relation_kind,
                relation.source_element_id,
                relation.target_element_id,
            )
            for relation in wp14.relations
        }
        new_kinds = {
            relation.relation_kind
            for relation in complete.relations
            if (
                relation.relation_kind,
                relation.source_element_id,
                relation.target_element_id,
            )
            not in old_triples
        }

        self.assertEqual(
            new_kinds,
            {"source_reference", "declared_cross_reference"},
        )

    def test_candidate_and_declaration_are_immutable(self) -> None:
        summary, statistics = artifacts()
        declaration = declaration_for(summary, statistics)
        relation_set = generate_declared_reference_relations(
            summary,
            statistics,
            (declaration,),
        )

        with self.assertRaises(FrozenInstanceError):
            declaration.direction = "inferred"
        with self.assertRaises(FrozenInstanceError):
            relation_set.relation_count = 0
        self.assertIsInstance(declaration, AcceptedDeclaredCrossReference)
        self.assertIsInstance(relation_set, DeclaredReferenceRelationSet)
        self.assertIsInstance(relation_set.relations, tuple)

    def test_every_relation_preserves_wp12_provenance(self) -> None:
        summary, statistics = artifacts()
        declaration = declaration_for(summary, statistics)
        relation_set = generate_declared_reference_relations(
            summary,
            statistics,
            (declaration,),
        )

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
        self.assertEqual(declaration.provenance_ref, summary.input_inventory_ref)

    def test_replay_and_serialization_are_byte_identical(self) -> None:
        summary, statistics = artifacts()
        declaration = declaration_for(summary, statistics)
        first = generate_declared_reference_relations(
            summary,
            statistics,
            (declaration,),
        )
        second = generate_declared_reference_relations(
            summary,
            statistics,
            (declaration,),
        )

        self.assertEqual(first, second)
        self.assertEqual(
            canonical_declared_reference_relation_set_bytes(first),
            canonical_declared_reference_relation_set_bytes(second),
        )
        self.assertEqual(
            canonical_declared_reference_relation_set_bytes(first),
            json.dumps(
                asdict(first),
                ensure_ascii=False,
                separators=(",", ":"),
                sort_keys=True,
            ).encode("utf-8"),
        )

    def test_strict_schema_round_trips_and_rejects_unknown_fields(self) -> None:
        summary, statistics = artifacts()
        declaration = declaration_for(summary, statistics)
        relation_set = generate_declared_reference_relations(
            summary,
            statistics,
            (declaration,),
        )
        declaration_payload = asdict(declaration)
        set_payload = declared_reference_relation_set_as_dict(relation_set)

        self.assertEqual(
            accepted_declared_cross_reference_from_dict(declaration_payload),
            declaration,
        )
        self.assertEqual(
            declared_reference_relation_set_from_dict(set_payload),
            relation_set,
        )
        with self.assertRaises(ValueError):
            accepted_declared_cross_reference_from_dict(
                {**declaration_payload, "inferred": True}
            )
        with self.assertRaises(ValueError):
            declared_reference_relation_set_from_dict(
                {**set_payload, "graph": ()}
            )

    def test_construction_rejects_tampered_candidate_identity(self) -> None:
        summary, statistics = artifacts()
        declaration = declaration_for(summary, statistics)
        relation_set = generate_declared_reference_relations(
            summary,
            statistics,
            (declaration,),
        )

        with self.assertRaisesRegex(ValueError, "exact basis"):
            replace(
                relation_set,
                relation_set_id="relation-set-000000000000000000000000",
            )

    def test_canonical_proof_reaches_wp15_and_stops(self) -> None:
        proof, successful = build_wp15_proof()

        self.assertTrue(successful)
        self.assertTrue(proof["source_reference_coverage_verified"])
        self.assertTrue(proof["declaration_preserved"])
        self.assertTrue(proof["undeclared_reference_rejected"])
        self.assertTrue(proof["tampered_declaration_rejected"])
        self.assertTrue(proof["replay_byte_identical"])
        self.assertFalse(any(proof["downstream_execution"].values()))
        self.assertEqual(proof["stop"], STOP_AFTER_DECLARED_CROSS_REFERENCES)

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

    def test_module_imports_no_source_or_downstream_capability(self) -> None:
        path = ROOT / "src" / "orion" / "declared_cross_references_alpha.py"
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
