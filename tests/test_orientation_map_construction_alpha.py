"""Focused tests for structural WP23 Orientation Map Construction."""

from __future__ import annotations

import ast
from dataclasses import FrozenInstanceError, asdict, fields
from hashlib import sha256
from pathlib import Path
import subprocess
import sys
import unittest

from orion.navigation_certification_alpha import (
    FROZEN_NAVIGATION_CONTRACTS,
    canonical_navigation_certification_report_bytes,
)
from orion.navigation_conformance_alpha import (
    canonical_navigation_conformance_report_bytes,
)
from orion.navigation_construction_alpha import (
    canonical_constructed_navigation_bytes,
)
from orion.navigation_object_alpha import canonical_navigation_object_bytes
from orion.declared_cross_references_alpha import (
    canonical_declared_reference_relation_set_bytes,
)
from orion.orientation_map_construction_alpha import (
    CONSTRUCTION_STATE,
    ORIENTATION_MAP_CONSTRUCTION_SCHEMA_VERSION,
    RESPONSIBILITY,
    STOP_AFTER_ORIENTATION_MAP_CONSTRUCTION,
    ConstructedOrientationMap,
    canonical_constructed_orientation_map_bytes,
    construct_orientation_map,
    constructed_orientation_map_as_dict,
    constructed_orientation_map_from_dict,
)
from orion.orientation_map_object_alpha import (
    canonical_orientation_map_object_bytes,
)
from orion.relations_certification_alpha import (
    canonical_relations_certification_report_bytes,
)
from orion.understand_structural_statistics_alpha import (
    canonical_structural_statistics_bytes,
)
from orion.understand_structural_summary_alpha import (
    canonical_structural_summary_bytes,
)


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from slice_iii_orientation_map_construction_proof import (  # noqa: E402
    WP22_SHA256,
    WP22_SOURCE,
    build_wp23_artifacts,
    build_wp23_proof,
)
from slice_iii_orientation_map_object_proof import (  # noqa: E402
    WP21_SHA256,
    WP21_SOURCE,
)


PROOF = ROOT / "scripts" / "slice_iii_orientation_map_construction_proof.py"


def unsafe_replace(value: object, **changes: object) -> object:
    clone = object.__new__(type(value))
    for field in fields(value):
        object.__setattr__(
            clone,
            field.name,
            changes.get(field.name, getattr(value, field.name)),
        )
    return clone


def construct(artifacts, *, orientation_map=None):
    return construct_orientation_map(
        (
            artifacts["orientation_map_object"]
            if orientation_map is None
            else orientation_map
        ),
        artifacts["navigation_certification"],
        artifacts["navigation"],
        artifacts["constructed_navigation"],
        artifacts["navigation_conformance"],
        artifacts["relation_set"],
        artifacts["certification"],
        artifacts["summary"],
        artifacts["statistics"],
    )


class OrientationMapConstructionAlphaTests(unittest.TestCase):
    def test_construction_maps_navigation_entries_one_to_one(self) -> None:
        artifacts = build_wp23_artifacts()
        navigation = artifacts["constructed_navigation"]
        orientation_map = artifacts["constructed_orientation_map"]

        self.assertIsInstance(orientation_map, ConstructedOrientationMap)
        self.assertEqual(
            orientation_map.schema_version,
            ORIENTATION_MAP_CONSTRUCTION_SCHEMA_VERSION,
        )
        self.assertEqual(orientation_map.entry_count, navigation.entry_count)
        self.assertEqual(
            tuple(
                entry.navigation_entry_id for entry in orientation_map.entries
            ),
            tuple(entry.entry_id for entry in navigation.entries),
        )
        self.assertEqual(
            tuple(entry.relation_ref for entry in orientation_map.entries),
            tuple(entry.relation_ref for entry in navigation.entries),
        )

    def test_canonical_navigation_order_is_preserved_exactly(self) -> None:
        artifacts = build_wp23_artifacts()
        navigation = artifacts["constructed_navigation"]
        orientation_map = artifacts["constructed_orientation_map"]

        self.assertEqual(
            tuple(entry.canonical_order for entry in orientation_map.entries),
            tuple(entry.canonical_order for entry in navigation.entries),
        )
        self.assertEqual(
            tuple(entry.relation_kind for entry in orientation_map.entries),
            tuple(entry.relation_kind for entry in navigation.entries),
        )

    def test_structural_adjacency_references_are_preserved(self) -> None:
        artifacts = build_wp23_artifacts()
        navigation = artifacts["constructed_navigation"]
        orientation_map = artifacts["constructed_orientation_map"]

        self.assertEqual(
            tuple(
                entry.structural_adjacency_ref
                for entry in orientation_map.entries
            ),
            tuple(
                entry.structural_adjacency_ref for entry in navigation.entries
            ),
        )

    def test_provenance_is_preserved(self) -> None:
        artifacts = build_wp23_artifacts()
        navigation = artifacts["constructed_navigation"]
        orientation_map = artifacts["constructed_orientation_map"]

        self.assertEqual(
            orientation_map.provenance_ref,
            artifacts["orientation_map_object"].navigation_certification_ref,
        )
        self.assertEqual(
            tuple(entry.provenance_ref for entry in orientation_map.entries),
            tuple(entry.provenance_ref for entry in navigation.entries),
        )

    def test_output_is_immutable_strict_and_unvalidated(self) -> None:
        orientation_map = build_wp23_artifacts()[
            "constructed_orientation_map"
        ]
        payload = constructed_orientation_map_as_dict(orientation_map)

        with self.assertRaises(FrozenInstanceError):
            orientation_map.entry_count = 0
        with self.assertRaises(FrozenInstanceError):
            orientation_map.entries[0].canonical_order = 99
        self.assertEqual(
            constructed_orientation_map_from_dict(payload),
            orientation_map,
        )
        with self.assertRaises(ValueError):
            constructed_orientation_map_from_dict(
                {**payload, "coordinates": ()}
            )
        self.assertEqual(orientation_map.responsibility, RESPONSIBILITY)
        self.assertEqual(
            orientation_map.construction_state,
            CONSTRUCTION_STATE,
        )
        self.assertFalse(orientation_map.externally_conformant)
        self.assertEqual(
            orientation_map.stop,
            STOP_AFTER_ORIENTATION_MAP_CONSTRUCTION,
        )

    def test_construction_replay_is_byte_identical(self) -> None:
        first = build_wp23_artifacts()["constructed_orientation_map"]
        second = build_wp23_artifacts()["constructed_orientation_map"]

        self.assertEqual(first, second)
        self.assertEqual(
            canonical_constructed_orientation_map_bytes(first),
            canonical_constructed_orientation_map_bytes(second),
        )

    def test_uncertified_or_inconsistent_input_is_rejected(self) -> None:
        artifacts = build_wp23_artifacts()
        uncertified = unsafe_replace(
            artifacts["navigation_certification"],
            certified=False,
            status="failed",
            errors=("not certified",),
        )
        artifacts["navigation_certification"] = uncertified
        with self.assertRaises(ValueError):
            construct(artifacts)

        artifacts = build_wp23_artifacts()
        inconsistent = unsafe_replace(
            artifacts["orientation_map_object"],
            navigation_construction_id="navigation-construction-" + "0" * 24,
        )
        with self.assertRaises(ValueError):
            construct(artifacts, orientation_map=inconsistent)

    def test_construction_does_not_modify_inputs(self) -> None:
        artifacts = build_wp23_artifacts()
        before = (
            canonical_orientation_map_object_bytes(
                artifacts["orientation_map_object"]
            ),
            canonical_navigation_certification_report_bytes(
                artifacts["navigation_certification"]
            ),
            canonical_navigation_object_bytes(artifacts["navigation"]),
            canonical_constructed_navigation_bytes(
                artifacts["constructed_navigation"]
            ),
            canonical_navigation_conformance_report_bytes(
                artifacts["navigation_conformance"]
            ),
            canonical_declared_reference_relation_set_bytes(
                artifacts["relation_set"]
            ),
            canonical_relations_certification_report_bytes(
                artifacts["certification"]
            ),
            canonical_structural_summary_bytes(artifacts["summary"]),
            canonical_structural_statistics_bytes(artifacts["statistics"]),
        )

        construct(artifacts)
        after = (
            canonical_orientation_map_object_bytes(
                artifacts["orientation_map_object"]
            ),
            canonical_navigation_certification_report_bytes(
                artifacts["navigation_certification"]
            ),
            canonical_navigation_object_bytes(artifacts["navigation"]),
            canonical_constructed_navigation_bytes(
                artifacts["constructed_navigation"]
            ),
            canonical_navigation_conformance_report_bytes(
                artifacts["navigation_conformance"]
            ),
            canonical_declared_reference_relation_set_bytes(
                artifacts["relation_set"]
            ),
            canonical_relations_certification_report_bytes(
                artifacts["certification"]
            ),
            canonical_structural_summary_bytes(artifacts["summary"]),
            canonical_structural_statistics_bytes(artifacts["statistics"]),
        )

        self.assertEqual(before, after)

    def test_output_contains_no_geometry_or_visualization(self) -> None:
        keys = set(
            asdict(
                build_wp23_artifacts()["constructed_orientation_map"]
            )
        )

        self.assertFalse(
            keys
            & {
                "coordinates",
                "geometry",
                "layout",
                "positions",
                "clusters",
                "rendering",
                "drawing",
                "visualization",
                "camera",
                "interaction",
                "animation",
                "shortest_paths",
                "recommendations",
                "ranking",
                "semantic_neighborhoods",
            }
        )

    def test_module_calls_no_validator_renderer_or_algorithm(self) -> None:
        path = ROOT / "src" / "orion" / "orientation_map_construction_alpha.py"
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
            "validate_orientation_map",
            "certify_orientation_map",
            "generate_layout",
            "render_map",
            "cluster",
            "find_shortest_path",
            "rank",
            "recommend",
        }

        self.assertFalse(prohibited & imported_names)
        self.assertFalse(prohibited & called_names)

    def test_frozen_wp18_through_wp22_sources_are_unchanged(self) -> None:
        records = tuple(
            (
                contract.work_package,
                ROOT / contract.source_path,
                contract.sha256,
            )
            for contract in FROZEN_NAVIGATION_CONTRACTS
        ) + (
            ("WP21", WP21_SOURCE, WP21_SHA256),
            ("WP22", WP22_SOURCE, WP22_SHA256),
        )
        for work_package, path, expected in records:
            with self.subTest(work_package=work_package):
                self.assertEqual(
                    sha256(path.read_bytes()).hexdigest(),
                    expected,
                )

    def test_canonical_proof_constructs_and_stops(self) -> None:
        proof, successful = build_wp23_proof()

        self.assertTrue(successful)
        self.assertTrue(proof["frozen_dependencies_verified"])
        self.assertTrue(proof["canonical_navigation_order_preserved"])
        self.assertTrue(proof["navigation_entry_references_exact"])
        self.assertTrue(proof["structural_references_preserved"])
        self.assertTrue(proof["provenance_preserved"])
        self.assertTrue(proof["inputs_unchanged"])
        self.assertTrue(proof["construction_replay_byte_identical"])
        self.assertFalse(any(proof["downstream_execution"].values()))
        self.assertEqual(
            proof["stop"],
            STOP_AFTER_ORIENTATION_MAP_CONSTRUCTION,
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
