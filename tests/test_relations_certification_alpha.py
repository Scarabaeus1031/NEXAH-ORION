"""Focused tests for WP17 observational Relations Certification."""

from __future__ import annotations

import ast
from dataclasses import FrozenInstanceError, asdict, fields
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
import unittest

from orion.declared_cross_references_alpha import (
    canonical_declared_reference_relation_set_bytes,
    declared_cross_reference_from_explicit_values,
    generate_declared_reference_relations,
)
from orion.markdown_structural_renderer_alpha import (
    MarkdownStructuralRendererAlpha,
)
from orion.relation_conformance_alpha import (
    canonical_relation_conformance_report_bytes,
    validate_relation_conformance,
)
from orion.relations_certification_alpha import (
    FAILED,
    FROZEN_RELATIONS_CONTRACTS,
    PASSED,
    STOP_AT_RELATIONS_CERTIFIED,
    RelationsCertificationReport,
    canonical_relations_certification_report_bytes,
    certify_relations,
    relations_certification_report_as_dict,
    relations_certification_report_from_dict,
)
from orion.understand_source_element_inventory_alpha import (
    inventory_declared_source_elements,
)
from orion.understand_structural_statistics_alpha import (
    canonical_structural_statistics_bytes,
    measure_declared_structure,
)
from orion.understand_structural_summary_alpha import (
    canonical_structural_summary_bytes,
    summarize_declared_structure,
)


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from slice_iii_relations_certification_proof import (  # noqa: E402
    build_wp17_proof,
)
from slice_iii_structural_equality_proof import _confirmed_source  # noqa: E402


PROOF = ROOT / "scripts" / "slice_iii_relations_certification_proof.py"


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
    conformance = validate_relation_conformance(
        relation_set,
        summary,
        statistics,
    )
    return summary, statistics, relation_set, conformance


class RelationsCertificationAlphaTests(unittest.TestCase):
    def test_accepted_relations_layer_is_certified(self) -> None:
        summary, statistics, relation_set, conformance = artifacts()

        certification = certify_relations(
            relation_set,
            conformance,
            summary,
            statistics,
        )

        self.assertTrue(certification.certified)
        self.assertEqual(certification.status, PASSED)
        self.assertEqual(certification.errors, ())
        self.assertEqual(certification.stop, STOP_AT_RELATIONS_CERTIFIED)
        self.assertTrue(certification.relation_set_replay_byte_identical)
        self.assertTrue(
            certification.conformance_report_replay_byte_identical
        )

    def test_unaccepted_conformance_report_blocks_certification(self) -> None:
        summary, statistics, relation_set, conformance = artifacts()
        rejected = unsafe_replace(
            conformance,
            valid=False,
            decision="rejected",
            errors=("declared rejection",),
            accepted_relation_set_ref=None,
        )

        certification = certify_relations(
            relation_set,
            rejected,
            summary,
            statistics,
        )

        self.assertFalse(certification.certified)
        self.assertEqual(certification.status, FAILED)
        self.assertIn(
            "Relation Conformance Report is malformed or not immutable",
            certification.errors,
        )

    def test_inconsistent_relation_set_reference_blocks_certification(
        self,
    ) -> None:
        summary, statistics, relation_set, conformance = artifacts()
        inconsistent = unsafe_replace(
            conformance,
            relation_set_ref="sha256:" + "0" * 64,
            accepted_relation_set_ref="sha256:" + "0" * 64,
        )

        certification = certify_relations(
            relation_set,
            inconsistent,
            summary,
            statistics,
        )

        self.assertFalse(certification.certified)
        self.assertIn(
            "Relation Conformance Report is malformed or not immutable",
            certification.errors,
        )

    def test_malformed_relation_set_blocks_certification_without_repair(
        self,
    ) -> None:
        summary, statistics, relation_set, conformance = artifacts()
        malformed = unsafe_replace(
            relation_set,
            relation_set_id="relation-set-000000000000000000000000",
        )

        certification = certify_relations(
            malformed,
            conformance,
            summary,
            statistics,
        )

        self.assertFalse(certification.certified)
        self.assertEqual(certification.status, FAILED)
        self.assertIn(
            "Relation Set is malformed or not immutable",
            certification.errors,
        )

    def test_certification_does_not_modify_any_input(self) -> None:
        summary, statistics, relation_set, conformance = artifacts()
        before = (
            canonical_declared_reference_relation_set_bytes(relation_set),
            canonical_relation_conformance_report_bytes(conformance),
            canonical_structural_summary_bytes(summary),
            canonical_structural_statistics_bytes(statistics),
        )

        certification = certify_relations(
            relation_set,
            conformance,
            summary,
            statistics,
        )
        after = (
            canonical_declared_reference_relation_set_bytes(relation_set),
            canonical_relation_conformance_report_bytes(conformance),
            canonical_structural_summary_bytes(summary),
            canonical_structural_statistics_bytes(statistics),
        )

        self.assertTrue(certification.inputs_unchanged)
        self.assertEqual(before, after)

    def test_certification_report_is_immutable_and_strict(self) -> None:
        summary, statistics, relation_set, conformance = artifacts()
        certification = certify_relations(
            relation_set,
            conformance,
            summary,
            statistics,
        )
        payload = relations_certification_report_as_dict(certification)

        self.assertIsInstance(certification, RelationsCertificationReport)
        with self.assertRaises(FrozenInstanceError):
            certification.certified = False
        self.assertEqual(
            relations_certification_report_from_dict(payload),
            certification,
        )
        with self.assertRaises(ValueError):
            relations_certification_report_from_dict(
                {**payload, "navigation_ready": True}
            )

    def test_certification_replay_is_byte_identical(self) -> None:
        summary, statistics, relation_set, conformance = artifacts()
        first = certify_relations(
            relation_set,
            conformance,
            summary,
            statistics,
        )
        second = certify_relations(
            relation_set,
            conformance,
            summary,
            statistics,
        )

        self.assertEqual(first, second)
        self.assertEqual(
            canonical_relations_certification_report_bytes(first),
            canonical_relations_certification_report_bytes(second),
        )

    def test_frozen_wp12_through_wp16_hashes_match_repository(self) -> None:
        for contract in FROZEN_RELATIONS_CONTRACTS:
            with self.subTest(work_package=contract.work_package):
                self.assertEqual(
                    sha256((ROOT / contract.source_path).read_bytes()).hexdigest(),
                    contract.sha256,
                )

    def test_report_preserves_exact_artifact_references(self) -> None:
        summary, statistics, relation_set, conformance = artifacts()
        certification = certify_relations(
            relation_set,
            conformance,
            summary,
            statistics,
        )

        self.assertEqual(
            certification.relation_set_ref,
            conformance.accepted_relation_set_ref,
        )
        self.assertEqual(
            certification.structural_summary_ref,
            conformance.structural_summary_ref,
        )
        self.assertEqual(
            certification.structural_statistics_ref,
            conformance.structural_statistics_ref,
        )
        self.assertTrue(certification.provenance_preserved)

    def test_canonical_order_is_observed_from_accepted_wp16_report(self) -> None:
        summary, statistics, relation_set, conformance = artifacts()
        certification = certify_relations(
            relation_set,
            conformance,
            summary,
            statistics,
        )

        self.assertIn("canonical_order", conformance.checks)
        self.assertTrue(certification.stable_canonical_ordering)

    def test_canonical_proof_certifies_and_stops(self) -> None:
        proof, successful = build_wp17_proof()

        self.assertTrue(successful)
        self.assertTrue(proof["certification"]["certified"])
        self.assertEqual(proof["certification"]["status"], PASSED)
        self.assertTrue(proof["inputs_unchanged"])
        self.assertTrue(proof["certification_replay_byte_identical"])
        self.assertTrue(proof["frozen_contracts_verified"])
        self.assertTrue(proof["package_proofs_verified"])
        self.assertFalse(any(proof["downstream_execution"].values()))
        self.assertEqual(proof["stop"], STOP_AT_RELATIONS_CERTIFIED)

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

    def test_certifier_imports_or_calls_no_generator_or_validator(self) -> None:
        path = ROOT / "src" / "orion" / "relations_certification_alpha.py"
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
        self.assertNotIn("validate_relation_conformance", imported_names)
        self.assertFalse(
            any(name.startswith("generate_") for name in called_names)
        )
        self.assertNotIn("validate_relation_conformance", called_names)

    def test_certifier_imports_no_source_or_downstream_capability(self) -> None:
        path = ROOT / "src" / "orion" / "relations_certification_alpha.py"
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

    def test_report_contains_no_navigation_or_map_payload(self) -> None:
        summary, statistics, relation_set, conformance = artifacts()
        certification = certify_relations(
            relation_set,
            conformance,
            summary,
            statistics,
        )
        keys = set(asdict(certification))

        self.assertFalse(
            keys
            & {
                "relations",
                "navigation",
                "orientation_map",
                "semantic_validation",
                "generated_relations",
            }
        )


if __name__ == "__main__":
    unittest.main()
