"""Focused tests for the atomic WP22 Orientation Map Object contract."""

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
from orion.orientation_map_object_alpha import (
    CONTRACT_STATE,
    ORIENTATION_MAP_SCHEMA_VERSION,
    RESPONSIBILITY,
    SERIALIZATION_VERSION,
    STOP_AFTER_ORIENTATION_MAP_OBJECT,
    OrientationMapObject,
    canonical_orientation_map_object_bytes,
    create_orientation_map_object,
    orientation_map_object_as_dict,
    orientation_map_object_from_dict,
)


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from slice_iii_orientation_map_object_proof import (  # noqa: E402
    WP21_SHA256,
    WP21_SOURCE,
    build_wp22_artifacts,
    build_wp22_proof,
)


PROOF = ROOT / "scripts" / "slice_iii_orientation_map_object_proof.py"


def unsafe_replace(value: object, **changes: object) -> object:
    clone = object.__new__(type(value))
    for field in fields(value):
        object.__setattr__(
            clone,
            field.name,
            changes.get(field.name, getattr(value, field.name)),
        )
    return clone


def create(artifacts, *, navigation_certification=None, navigation=None):
    return create_orientation_map_object(
        (
            artifacts["navigation_certification"]
            if navigation_certification is None
            else navigation_certification
        ),
        artifacts["navigation"] if navigation is None else navigation,
        artifacts["constructed_navigation"],
        artifacts["navigation_conformance"],
        artifacts["relation_set"],
        artifacts["certification"],
        artifacts["summary"],
        artifacts["statistics"],
    )


class OrientationMapObjectAlphaTests(unittest.TestCase):
    def test_object_references_exact_certified_artifacts(self) -> None:
        artifacts = build_wp22_artifacts()
        orientation_map = artifacts["orientation_map_object"]

        self.assertIsInstance(orientation_map, OrientationMapObject)
        self.assertEqual(
            orientation_map.orientation_map_schema_version,
            ORIENTATION_MAP_SCHEMA_VERSION,
        )
        self.assertEqual(
            orientation_map.navigation_certification_id,
            artifacts["navigation_certification"].certification_id,
        )
        self.assertEqual(
            orientation_map.navigation_object_id,
            artifacts["navigation"].navigation_id,
        )
        self.assertEqual(
            orientation_map.navigation_construction_id,
            artifacts["constructed_navigation"].construction_id,
        )
        self.assertEqual(
            orientation_map.navigation_conformance_id,
            artifacts["navigation_conformance"].report_id,
        )
        self.assertEqual(
            orientation_map.relation_set_id,
            artifacts["relation_set"].relation_set_id,
        )
        self.assertEqual(orientation_map.canonical_order, 0)
        self.assertEqual(
            orientation_map.serialization_version,
            SERIALIZATION_VERSION,
        )
        self.assertEqual(orientation_map.responsibility, RESPONSIBILITY)
        self.assertEqual(orientation_map.contract_state, CONTRACT_STATE)
        self.assertFalse(orientation_map.externally_conformant)
        self.assertEqual(
            orientation_map.stop,
            STOP_AFTER_ORIENTATION_MAP_OBJECT,
        )

    def test_object_is_immutable_and_schema_strict(self) -> None:
        orientation_map = build_wp22_artifacts()["orientation_map_object"]
        payload = orientation_map_object_as_dict(orientation_map)

        with self.assertRaises(FrozenInstanceError):
            orientation_map.canonical_order = 1
        self.assertEqual(
            orientation_map_object_from_dict(payload),
            orientation_map,
        )
        with self.assertRaises(ValueError):
            orientation_map_object_from_dict({**payload, "nodes": ()})

    def test_identity_and_serialization_replay_are_byte_identical(self) -> None:
        first = build_wp22_artifacts()["orientation_map_object"]
        second = build_wp22_artifacts()["orientation_map_object"]

        self.assertEqual(first, second)
        self.assertEqual(
            canonical_orientation_map_object_bytes(first),
            canonical_orientation_map_object_bytes(second),
        )

    def test_identity_or_integrity_tampering_is_rejected(self) -> None:
        orientation_map = build_wp22_artifacts()["orientation_map_object"]
        payload = orientation_map_object_as_dict(orientation_map)

        with self.assertRaises(ValueError):
            orientation_map_object_from_dict(
                {
                    **payload,
                    "orientation_map_id": "orientation-map-" + "0" * 24,
                }
            )
        with self.assertRaises(ValueError):
            orientation_map_object_from_dict(
                {**payload, "orientation_map_integrity": "0" * 64}
            )

    def test_uncertified_navigation_is_rejected(self) -> None:
        artifacts = build_wp22_artifacts()
        uncertified = unsafe_replace(
            artifacts["navigation_certification"],
            certified=False,
            status="failed",
            errors=("not certified",),
        )

        with self.assertRaises(ValueError):
            create(artifacts, navigation_certification=uncertified)

    def test_inconsistent_navigation_lineage_is_rejected(self) -> None:
        artifacts = build_wp22_artifacts()
        inconsistent = unsafe_replace(
            artifacts["navigation"],
            navigation_id="navigation-" + "0" * 24,
        )

        with self.assertRaises(ValueError):
            create(artifacts, navigation=inconsistent)

    def test_non_artifact_input_is_rejected(self) -> None:
        artifacts = build_wp22_artifacts()

        with self.assertRaises(TypeError):
            create_orientation_map_object(
                {},
                artifacts["navigation"],
                artifacts["constructed_navigation"],
                artifacts["navigation_conformance"],
                artifacts["relation_set"],
                artifacts["certification"],
                artifacts["summary"],
                artifacts["statistics"],
            )

    def test_creation_does_not_modify_inputs(self) -> None:
        artifacts = build_wp22_artifacts()
        before = (
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
        )

        create(artifacts)
        after = (
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
        )

        self.assertEqual(before, after)

    def test_contract_contains_no_constructed_or_visual_map_content(self) -> None:
        keys = set(
            asdict(build_wp22_artifacts()["orientation_map_object"])
        )

        self.assertFalse(
            keys
            & {
                "nodes",
                "edges",
                "transitions",
                "geometry",
                "layout",
                "coordinates",
                "positions",
                "regions",
                "clusters",
                "routes",
                "rendering",
                "visualization",
                "navigation_behavior",
            }
        )

    def test_module_imports_or_calls_no_map_constructor_or_behavior(self) -> None:
        path = ROOT / "src" / "orion" / "orientation_map_object_alpha.py"
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
            "construct_orientation_map",
            "validate_orientation_map",
            "certify_orientation_map",
            "generate_nodes",
            "generate_edges",
            "generate_layout",
            "render_map",
            "traverse",
        }

        self.assertFalse(prohibited & imported_names)
        self.assertFalse(prohibited & called_names)

    def test_frozen_wp18_through_wp21_sources_are_unchanged(self) -> None:
        records = tuple(
            (
                contract.work_package,
                ROOT / contract.source_path,
                contract.sha256,
            )
            for contract in FROZEN_NAVIGATION_CONTRACTS
        ) + (("WP21", WP21_SOURCE, WP21_SHA256),)
        for work_package, path, expected in records:
            with self.subTest(work_package=work_package):
                self.assertEqual(
                    sha256(path.read_bytes()).hexdigest(),
                    expected,
                )

    def test_canonical_proof_creates_contract_and_stops(self) -> None:
        proof, successful = build_wp22_proof()

        self.assertTrue(successful)
        self.assertTrue(proof["frozen_navigation_verified"])
        self.assertTrue(proof["inputs_unchanged"])
        self.assertTrue(proof["orientation_map_replay_byte_identical"])
        self.assertTrue(proof["provenance_preserved"])
        self.assertFalse(any(proof["downstream_execution"].values()))
        self.assertEqual(
            proof["stop"],
            STOP_AFTER_ORIENTATION_MAP_OBJECT,
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
