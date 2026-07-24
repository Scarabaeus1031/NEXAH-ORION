"""Focused tests for WP16 External Relation Conformance."""

from __future__ import annotations

import ast
from dataclasses import FrozenInstanceError, asdict, fields
import json
from pathlib import Path
import subprocess
import sys
import unittest

import orion.declared_cross_references_alpha as declared_reference_module
from orion.declared_cross_references_alpha import (
    declared_cross_reference_from_explicit_values,
    generate_declared_reference_relations,
)
from orion.markdown_structural_renderer_alpha import (
    MarkdownStructuralRendererAlpha,
)
from orion.relation_conformance_alpha import (
    ACCEPTED,
    REJECTED,
    STOP_AFTER_RELATION_CONFORMANCE,
    RelationConformanceReport,
    canonical_relation_conformance_report_bytes,
    relation_conformance_report_as_dict,
    relation_conformance_report_from_dict,
    validate_relation_conformance,
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

from slice_iii_relation_conformance_proof import (  # noqa: E402
    build_wp16_proof,
)
from slice_iii_structural_equality_proof import _confirmed_source  # noqa: E402


PROOF = ROOT / "scripts" / "slice_iii_relation_conformance_proof.py"


def unsafe_replace(value: object, **changes: object) -> object:
    clone = object.__new__(type(value))
    for field in fields(value):
        object.__setattr__(
            clone,
            field.name,
            changes.get(field.name, getattr(value, field.name)),
        )
    return clone


def artifacts():
    representation = MarkdownStructuralRendererAlpha().render(
        _confirmed_source()
    )
    inventory = inventory_declared_source_elements(representation)
    summary = summarize_declared_structure(inventory)
    statistics = measure_declared_structure(inventory)
    declaration = declared_cross_reference_from_explicit_values(
        declaration_version="1",
        source_element_id=statistics.element_spans[1].element_id,
        target_element_id=statistics.element_spans[3].element_id,
        provenance_ref=summary.input_inventory_ref,
    )
    relation_set = generate_declared_reference_relations(
        summary,
        statistics,
        (declaration,),
    )
    return summary, statistics, relation_set


class RelationConformanceAlphaTests(unittest.TestCase):
    def test_valid_complete_candidate_is_accepted(self) -> None:
        summary, statistics, relation_set = artifacts()

        report = validate_relation_conformance(
            relation_set,
            summary,
            statistics,
        )

        self.assertTrue(report.valid)
        self.assertEqual(report.decision, ACCEPTED)
        self.assertEqual(
            report.accepted_relation_set_ref,
            report.relation_set_ref,
        )
        self.assertEqual(report.errors, ())
        self.assertEqual(report.stop, STOP_AFTER_RELATION_CONFORMANCE)

    def test_validation_does_not_modify_candidate(self) -> None:
        summary, statistics, relation_set = artifacts()
        before = json.dumps(
            asdict(relation_set),
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")

        report = validate_relation_conformance(
            relation_set,
            summary,
            statistics,
        )
        after = json.dumps(
            asdict(relation_set),
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")

        self.assertTrue(report.input_unchanged)
        self.assertEqual(before, after)

    def test_malformed_relation_set_is_rejected_not_repaired(self) -> None:
        summary, statistics, _ = artifacts()

        report = validate_relation_conformance(
            {"relations": ()},
            summary,
            statistics,
        )

        self.assertFalse(report.valid)
        self.assertEqual(report.decision, REJECTED)
        self.assertIsNone(report.accepted_relation_set_ref)
        self.assertIn(
            "Input is not an immutable WP15 Relation Set",
            report.errors,
        )

    def test_duplicate_relation_is_detected(self) -> None:
        summary, statistics, relation_set = artifacts()
        duplicate = unsafe_replace(
            relation_set,
            relations=relation_set.relations + (relation_set.relations[0],),
            relation_count=relation_set.relation_count + 1,
        )

        report = validate_relation_conformance(
            duplicate,
            summary,
            statistics,
        )

        self.assertFalse(report.valid)
        self.assertIn(
            "Relation Set contains duplicate identities or relation facts",
            report.errors,
        )

    def test_invalid_endpoint_is_rejected(self) -> None:
        summary, statistics, relation_set = artifacts()
        bad_relation = unsafe_replace(
            relation_set.relations[0],
            target_element_id="element-000000000000000000000000",
        )
        tampered = unsafe_replace(
            relation_set,
            relations=(bad_relation,) + relation_set.relations[1:],
        )

        report = validate_relation_conformance(
            tampered,
            summary,
            statistics,
        )

        self.assertFalse(report.valid)
        self.assertIn(
            "Relation Set contains an unresolved source or target endpoint",
            report.errors,
        )

    def test_supplied_relation_without_exact_structural_basis_is_rejected(
        self,
    ) -> None:
        summary, statistics, relation_set = artifacts()
        bad_relation = unsafe_replace(
            relation_set.relations[0],
            target_element_id=statistics.element_spans[2].element_id,
        )
        tampered = unsafe_replace(
            relation_set,
            relations=(bad_relation,) + relation_set.relations[1:],
        )

        report = validate_relation_conformance(
            tampered,
            summary,
            statistics,
        )

        self.assertFalse(report.valid)
        self.assertIn(
            "One or more supplied relations lacks an exact declared basis",
            report.errors,
        )

    def test_invalid_provenance_is_rejected(self) -> None:
        summary, statistics, relation_set = artifacts()
        bad_provenance = unsafe_replace(
            relation_set.relations[0].provenance,
            source_integrity="0" * 64,
        )
        bad_relation = unsafe_replace(
            relation_set.relations[0],
            provenance=bad_provenance,
        )
        tampered = unsafe_replace(
            relation_set,
            relations=(bad_relation,) + relation_set.relations[1:],
        )

        report = validate_relation_conformance(
            tampered,
            summary,
            statistics,
        )

        self.assertFalse(report.valid)
        self.assertIn(
            "One or more Relation Objects are malformed or have invalid provenance",
            report.errors,
        )

    def test_invalid_relation_kind_is_rejected(self) -> None:
        summary, statistics, relation_set = artifacts()
        bad_relation = unsafe_replace(
            relation_set.relations[0],
            relation_kind="semantic_similarity",
        )
        tampered = unsafe_replace(
            relation_set,
            relations=(bad_relation,) + relation_set.relations[1:],
        )

        report = validate_relation_conformance(
            tampered,
            summary,
            statistics,
        )

        self.assertFalse(report.valid)
        self.assertIn(
            "Relation Set contains a kind outside the frozen vocabulary",
            report.errors,
        )

    def test_noncanonical_order_is_rejected_without_reordering(self) -> None:
        summary, statistics, relation_set = artifacts()
        reordered_relations = (
            relation_set.relations[1],
            relation_set.relations[0],
        ) + relation_set.relations[2:]
        tampered = unsafe_replace(
            relation_set,
            relations=reordered_relations,
        )
        before = tuple(
            relation.relation_id for relation in tampered.relations
        )

        report = validate_relation_conformance(
            tampered,
            summary,
            statistics,
        )

        self.assertFalse(report.valid)
        self.assertIn(
            "Relation Set ordering is not canonical and contiguous",
            report.errors,
        )
        self.assertEqual(
            before,
            tuple(relation.relation_id for relation in tampered.relations),
        )

    def test_conformance_does_not_require_or_complete_additional_relations(
        self,
    ) -> None:
        summary, statistics, _ = artifacts()
        complete_without_declarations = generate_declared_reference_relations(
            summary,
            statistics,
        )
        supplied_relations = complete_without_declarations.relations[:-1]
        basis = declared_reference_module._set_identity_basis(
            structural_equality_relation_set_ref=(
                complete_without_declarations.structural_equality_relation_set_ref
            ),
            structural_summary_ref=(
                complete_without_declarations.structural_summary_ref
            ),
            structural_statistics_ref=(
                complete_without_declarations.structural_statistics_ref
            ),
            input_inventory_ref=complete_without_declarations.input_inventory_ref,
            accepted_declaration_refs=(),
            source_reference_count=(
                complete_without_declarations.source_reference_count
            ),
            declared_cross_reference_count=0,
            relations=supplied_relations,
        )
        supplied_subset = unsafe_replace(
            complete_without_declarations,
            relation_set_id=(
                "relation-set-"
                + declared_reference_module._digest(basis)[:24]
            ),
            relation_count=len(supplied_relations),
            relations=supplied_relations,
        )
        supplied_subset.__post_init__()
        before = tuple(
            relation.relation_id for relation in supplied_subset.relations
        )

        report = validate_relation_conformance(
            supplied_subset,
            summary,
            statistics,
        )

        self.assertTrue(report.valid)
        self.assertEqual(report.decision, ACCEPTED)
        self.assertEqual(
            before,
            tuple(
                relation.relation_id
                for relation in supplied_subset.relations
            ),
        )

    def test_changed_slice_ii_reference_is_rejected(self) -> None:
        summary, statistics, relation_set = artifacts()
        tampered = unsafe_replace(
            relation_set,
            structural_summary_ref="sha256:" + "0" * 64,
        )

        report = validate_relation_conformance(
            tampered,
            summary,
            statistics,
        )

        self.assertFalse(report.valid)
        self.assertIn(
            "Relation Set does not name the exact Slice II inputs",
            report.errors,
        )

    def test_report_is_immutable_and_strictly_serializable(self) -> None:
        summary, statistics, relation_set = artifacts()
        report = validate_relation_conformance(
            relation_set,
            summary,
            statistics,
        )
        payload = relation_conformance_report_as_dict(report)

        self.assertIsInstance(report, RelationConformanceReport)
        with self.assertRaises(FrozenInstanceError):
            report.valid = False
        self.assertEqual(
            relation_conformance_report_from_dict(payload),
            report,
        )
        with self.assertRaises(ValueError):
            relation_conformance_report_from_dict(
                {**payload, "normalized_relations": ()}
            )

    def test_report_replay_is_byte_identical(self) -> None:
        summary, statistics, relation_set = artifacts()
        first = validate_relation_conformance(
            relation_set,
            summary,
            statistics,
        )
        second = validate_relation_conformance(
            relation_set,
            summary,
            statistics,
        )

        self.assertEqual(first, second)
        self.assertEqual(
            canonical_relation_conformance_report_bytes(first),
            canonical_relation_conformance_report_bytes(second),
        )

    def test_rejection_replay_is_byte_identical(self) -> None:
        summary, statistics, relation_set = artifacts()
        bad_relation = unsafe_replace(
            relation_set.relations[0],
            relation_kind="semantic_similarity",
        )
        tampered = unsafe_replace(
            relation_set,
            relations=(bad_relation,) + relation_set.relations[1:],
        )
        first = validate_relation_conformance(
            tampered,
            summary,
            statistics,
        )
        second = validate_relation_conformance(
            tampered,
            summary,
            statistics,
        )

        self.assertFalse(first.valid)
        self.assertEqual(
            canonical_relation_conformance_report_bytes(first),
            canonical_relation_conformance_report_bytes(second),
        )

    def test_prohibited_downstream_fields_are_absent(self) -> None:
        summary, statistics, relation_set = artifacts()
        report = validate_relation_conformance(
            relation_set,
            summary,
            statistics,
        )
        keys = set(asdict(report))

        self.assertFalse(
            keys
            & {
                "relations",
                "normalized_relations",
                "graph",
                "navigation",
                "orientation_map",
                "semantic_validation",
            }
        )

    def test_canonical_proof_accepts_and_stops(self) -> None:
        proof, successful = build_wp16_proof()

        self.assertTrue(successful)
        self.assertTrue(proof["conformance_report"]["valid"])
        self.assertEqual(
            proof["conformance_report"]["decision"],
            ACCEPTED,
        )
        self.assertTrue(proof["candidate_unchanged"])
        self.assertTrue(proof["completion_not_evaluated"])
        self.assertTrue(proof["report_replay_byte_identical"])
        self.assertTrue(proof["tamper_matrix_rejected"])
        self.assertFalse(any(proof["downstream_execution"].values()))
        self.assertEqual(proof["stop"], STOP_AFTER_RELATION_CONFORMANCE)

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

    def test_validator_imports_or_calls_no_relation_generator(self) -> None:
        path = ROOT / "src" / "orion" / "relation_conformance_alpha.py"
        tree = ast.parse(path.read_text(encoding="utf-8"))
        imported_names = {
            alias.name
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom)
            for alias in node.names
        }
        called_names = {
            node.func.id
            for node in ast.walk(tree)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
        }

        self.assertFalse(
            any(name.startswith("generate_") for name in imported_names)
        )
        self.assertFalse(
            any(name.startswith("generate_") for name in called_names)
        )

    def test_validator_imports_no_source_or_downstream_capability(self) -> None:
        path = ROOT / "src" / "orion" / "relation_conformance_alpha.py"
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
