"""Focused tests for behavior-free WP19 Navigation Construction."""

from __future__ import annotations

import ast
from dataclasses import FrozenInstanceError, asdict, fields
from hashlib import sha256
from pathlib import Path
import subprocess
import sys
import unittest

from orion.declared_cross_references_alpha import (
    canonical_declared_reference_relation_set_bytes,
)
from orion.navigation_construction_alpha import (
    ADJACENCY_RELATION_KINDS,
    CONSTRUCTION_STATE,
    NAVIGATION_CONSTRUCTION_SCHEMA_VERSION,
    RESPONSIBILITY,
    STOP_AFTER_NAVIGATION_CONSTRUCTION,
    ConstructedNavigationObject,
    canonical_constructed_navigation_bytes,
    construct_navigation,
    constructed_navigation_as_dict,
    constructed_navigation_from_dict,
)
from orion.navigation_object_alpha import canonical_navigation_object_bytes
from orion.relations_certification_alpha import (
    FROZEN_RELATIONS_CONTRACTS,
    canonical_relations_certification_report_bytes,
)
from orion.structural_relation_alpha import canonical_relation_object_bytes


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from slice_iii_navigation_construction_proof import (  # noqa: E402
    WP18_SHA256,
    WP18_SOURCE,
    build_wp19_artifacts,
    build_wp19_proof,
)
from slice_iii_navigation_object_proof import (  # noqa: E402
    WP17_SHA256,
    WP17_SOURCE,
)


PROOF = ROOT / "scripts" / "slice_iii_navigation_construction_proof.py"


def unsafe_replace(value: object, **changes: object) -> object:
    clone = object.__new__(type(value))
    for field in fields(value):
        object.__setattr__(
            clone,
            field.name,
            changes.get(field.name, getattr(value, field.name)),
        )
    return clone


class NavigationConstructionAlphaTests(unittest.TestCase):
    def test_construction_materializes_exact_relation_references(self) -> None:
        artifacts = build_wp19_artifacts()
        relation_set = artifacts["relation_set"]
        constructed = artifacts["constructed_navigation"]

        self.assertIsInstance(constructed, ConstructedNavigationObject)
        self.assertEqual(
            constructed.schema_version,
            NAVIGATION_CONSTRUCTION_SCHEMA_VERSION,
        )
        self.assertEqual(constructed.entry_count, relation_set.relation_count)
        self.assertEqual(
            tuple(entry.relation_id for entry in constructed.entries),
            tuple(relation.relation_id for relation in relation_set.relations),
        )
        self.assertEqual(
            tuple(entry.relation_ref for entry in constructed.entries),
            tuple(
                "sha256:"
                + sha256(canonical_relation_object_bytes(relation)).hexdigest()
                for relation in relation_set.relations
            ),
        )

    def test_canonical_relation_order_is_preserved_exactly(self) -> None:
        artifacts = build_wp19_artifacts()
        relation_set = artifacts["relation_set"]
        constructed = artifacts["constructed_navigation"]

        self.assertEqual(
            tuple(entry.canonical_order for entry in constructed.entries),
            tuple(relation.canonical_order for relation in relation_set.relations),
        )
        self.assertEqual(
            tuple(entry.relation_kind for entry in constructed.entries),
            tuple(relation.relation_kind for relation in relation_set.relations),
        )

    def test_only_sequential_relations_receive_adjacency_references(self) -> None:
        constructed = build_wp19_artifacts()["constructed_navigation"]

        for entry in constructed.entries:
            with self.subTest(relation_kind=entry.relation_kind):
                if entry.relation_kind in ADJACENCY_RELATION_KINDS:
                    self.assertEqual(
                        entry.structural_adjacency_ref,
                        entry.relation_ref,
                    )
                else:
                    self.assertIsNone(entry.structural_adjacency_ref)

    def test_provenance_links_are_exact(self) -> None:
        artifacts = build_wp19_artifacts()
        constructed = artifacts["constructed_navigation"]
        relation_set = artifacts["relation_set"]
        navigation = artifacts["navigation"]

        self.assertEqual(
            constructed.provenance_ref,
            navigation.relations_certification_ref,
        )
        self.assertEqual(
            tuple(entry.provenance_ref for entry in constructed.entries),
            tuple(
                relation.provenance.input_inventory_ref
                for relation in relation_set.relations
            ),
        )

    def test_output_is_immutable_strict_and_unvalidated(self) -> None:
        constructed = build_wp19_artifacts()["constructed_navigation"]
        payload = constructed_navigation_as_dict(constructed)

        with self.assertRaises(FrozenInstanceError):
            constructed.entry_count = 0
        with self.assertRaises(FrozenInstanceError):
            constructed.entries[0].canonical_order = 99
        self.assertEqual(
            constructed_navigation_from_dict(payload),
            constructed,
        )
        with self.assertRaises(ValueError):
            constructed_navigation_from_dict({**payload, "routes": ()})
        self.assertEqual(constructed.responsibility, RESPONSIBILITY)
        self.assertEqual(constructed.construction_state, CONSTRUCTION_STATE)
        self.assertFalse(constructed.externally_conformant)
        self.assertEqual(
            constructed.stop,
            STOP_AFTER_NAVIGATION_CONSTRUCTION,
        )

    def test_construction_replay_is_byte_identical(self) -> None:
        first = build_wp19_artifacts()["constructed_navigation"]
        second = build_wp19_artifacts()["constructed_navigation"]

        self.assertEqual(first, second)
        self.assertEqual(
            canonical_constructed_navigation_bytes(first),
            canonical_constructed_navigation_bytes(second),
        )

    def test_uncertified_or_inconsistent_inputs_are_rejected(self) -> None:
        artifacts = build_wp19_artifacts()
        uncertified = unsafe_replace(
            artifacts["certification"],
            certified=False,
            status="failed",
            errors=("not certified",),
        )
        with self.assertRaises(ValueError):
            construct_navigation(
                artifacts["navigation"],
                artifacts["relation_set"],
                uncertified,
                artifacts["summary"],
                artifacts["statistics"],
            )

        inconsistent = unsafe_replace(
            artifacts["navigation"],
            relation_set_id="relation-set-" + "0" * 24,
        )
        with self.assertRaises(ValueError):
            construct_navigation(
                inconsistent,
                artifacts["relation_set"],
                artifacts["certification"],
                artifacts["summary"],
                artifacts["statistics"],
            )

    def test_construction_does_not_modify_inputs(self) -> None:
        artifacts = build_wp19_artifacts()
        before = (
            canonical_navigation_object_bytes(artifacts["navigation"]),
            canonical_declared_reference_relation_set_bytes(
                artifacts["relation_set"]
            ),
            canonical_relations_certification_report_bytes(
                artifacts["certification"]
            ),
            tuple(
                canonical_relation_object_bytes(relation)
                for relation in artifacts["relation_set"].relations
            ),
        )
        construct_navigation(
            artifacts["navigation"],
            artifacts["relation_set"],
            artifacts["certification"],
            artifacts["summary"],
            artifacts["statistics"],
        )
        after = (
            canonical_navigation_object_bytes(artifacts["navigation"]),
            canonical_declared_reference_relation_set_bytes(
                artifacts["relation_set"]
            ),
            canonical_relations_certification_report_bytes(
                artifacts["certification"]
            ),
            tuple(
                canonical_relation_object_bytes(relation)
                for relation in artifacts["relation_set"].relations
            ),
        )

        self.assertEqual(before, after)

    def test_output_contains_no_traversal_or_map_state(self) -> None:
        keys = set(
            asdict(build_wp19_artifacts()["constructed_navigation"])
        )

        self.assertFalse(
            keys
            & {
                "routes",
                "paths",
                "traversal",
                "movements",
                "cursor",
                "history",
                "graph",
                "ranking",
                "recommendations",
                "orientation_map",
                "validation",
                "certification",
            }
        )

    def test_module_calls_no_navigation_algorithm_or_validator(self) -> None:
        path = ROOT / "src" / "orion" / "navigation_construction_alpha.py"
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
        prohibited = {
            "traverse",
            "find_path",
            "search_graph",
            "rank",
            "recommend",
            "validate_navigation",
            "certify_navigation",
            "construct_orientation_map",
        }

        self.assertFalse(prohibited & imported_names)
        self.assertFalse(prohibited & called_names)

    def test_frozen_wp12_through_wp18_sources_are_unchanged(self) -> None:
        records = tuple(
            (
                contract.work_package,
                ROOT / contract.source_path,
                contract.sha256,
            )
            for contract in FROZEN_RELATIONS_CONTRACTS
        ) + (
            ("WP17", WP17_SOURCE, WP17_SHA256),
            ("WP18", WP18_SOURCE, WP18_SHA256),
        )
        for work_package, path, expected in records:
            with self.subTest(work_package=work_package):
                self.assertEqual(
                    sha256(path.read_bytes()).hexdigest(),
                    expected,
                )

    def test_canonical_proof_constructs_and_stops(self) -> None:
        proof, successful = build_wp19_proof()

        self.assertTrue(successful)
        self.assertTrue(proof["frozen_dependencies_verified"])
        self.assertTrue(proof["canonical_relation_order_preserved"])
        self.assertTrue(proof["relation_references_exact"])
        self.assertTrue(proof["adjacency_references_exact"])
        self.assertTrue(proof["provenance_preserved"])
        self.assertTrue(proof["inputs_unchanged"])
        self.assertTrue(proof["construction_replay_byte_identical"])
        self.assertFalse(any(proof["downstream_execution"].values()))
        self.assertEqual(
            proof["stop"],
            STOP_AFTER_NAVIGATION_CONSTRUCTION,
        )

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


if __name__ == "__main__":
    unittest.main()
