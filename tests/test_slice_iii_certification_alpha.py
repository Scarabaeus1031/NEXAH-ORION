"""Focused tests for observational WP25 Vertical Slice III Certification."""

from __future__ import annotations

import ast
from dataclasses import FrozenInstanceError, asdict, fields
from hashlib import sha256
from pathlib import Path
import subprocess
import sys
import unittest

from orion.slice_iii_certification_alpha import (
    FROZEN_SLICE_III_CONTRACTS,
    PASSED,
    STOP_AT_SLICE_III_CERTIFIED,
    SliceIIICertificationReport,
    canonical_slice_iii_certification_report_bytes,
    certify_slice_iii,
    slice_iii_certification_report_as_dict,
    slice_iii_certification_report_from_dict,
)


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from slice_iii_certification_proof import (  # noqa: E402
    build_wp25_artifacts,
    build_wp25_proof,
)


PROOF = ROOT / "scripts" / "slice_iii_certification_proof.py"


def unsafe_replace(value: object, **changes: object) -> object:
    clone = object.__new__(type(value))
    for field in fields(value):
        object.__setattr__(
            clone,
            field.name,
            changes.get(field.name, getattr(value, field.name)),
        )
    return clone


def certify(artifacts, *, map_conformance=None):
    return certify_slice_iii(
        artifacts["relation_set"],
        artifacts["certification"],
        artifacts["navigation"],
        artifacts["constructed_navigation"],
        artifacts["navigation_conformance"],
        artifacts["navigation_certification"],
        artifacts["orientation_map_object"],
        artifacts["constructed_orientation_map"],
        (
            artifacts["orientation_map_conformance"]
            if map_conformance is None
            else map_conformance
        ),
        artifacts["summary"],
        artifacts["statistics"],
    )


class SliceIIICertificationAlphaTests(unittest.TestCase):
    def test_canonical_slice_iii_is_certified(self) -> None:
        report = build_wp25_artifacts()["slice_iii_certification"]

        self.assertIsInstance(report, SliceIIICertificationReport)
        self.assertTrue(report.certified)
        self.assertEqual(report.status, PASSED)
        self.assertEqual(report.errors, ())
        self.assertTrue(report.relations_replay_byte_identical)
        self.assertTrue(report.navigation_replay_byte_identical)
        self.assertTrue(report.orientation_map_replay_byte_identical)
        self.assertTrue(report.provenance_preserved)
        self.assertEqual(report.stop, STOP_AT_SLICE_III_CERTIFIED)

    def test_uncertified_map_layer_fails_without_revalidation(self) -> None:
        artifacts = build_wp25_artifacts()
        rejected = unsafe_replace(
            artifacts["orientation_map_conformance"],
            valid=False,
            decision="rejected",
            errors=("observed rejection",),
            accepted_orientation_map_ref=None,
            accepted_construction_ref=None,
        )

        report = certify(artifacts, map_conformance=rejected)

        self.assertFalse(report.certified)
        self.assertIn(
            "WP24 did not accept the exact Orientation Map artifacts",
            report.errors,
        )

    def test_inconsistent_map_reference_fails(self) -> None:
        artifacts = build_wp25_artifacts()
        inconsistent = unsafe_replace(
            artifacts["orientation_map_conformance"],
            orientation_map_ref="sha256:" + "0" * 64,
        )

        report = certify(artifacts, map_conformance=inconsistent)

        self.assertFalse(report.certified)
        self.assertIn(
            "Slice III artifacts do not share exact immutable references",
            report.errors,
        )

    def test_report_is_immutable_strict_and_observational(self) -> None:
        report = build_wp25_artifacts()["slice_iii_certification"]
        payload = slice_iii_certification_report_as_dict(report)

        with self.assertRaises(FrozenInstanceError):
            report.certified = False
        self.assertEqual(
            slice_iii_certification_report_from_dict(payload),
            report,
        )
        with self.assertRaises(ValueError):
            slice_iii_certification_report_from_dict(
                {**payload, "orientation_map": {}}
            )
        self.assertFalse(
            set(asdict(report))
            & {
                "entries",
                "relations",
                "routes",
                "traversal",
                "geometry",
                "visualization",
                "repairs",
                "normalization",
                "slice_iv",
            }
        )

    def test_certification_report_replays_byte_identically(self) -> None:
        first = build_wp25_artifacts()["slice_iii_certification"]
        second = build_wp25_artifacts()["slice_iii_certification"]

        self.assertEqual(
            canonical_slice_iii_certification_report_bytes(first),
            canonical_slice_iii_certification_report_bytes(second),
        )

    def test_frozen_wp12_through_wp24_sources_are_unchanged(self) -> None:
        self.assertEqual(
            tuple(
                contract.work_package
                for contract in FROZEN_SLICE_III_CONTRACTS
            ),
            tuple(f"WP{number}" for number in range(12, 25)),
        )
        for contract in FROZEN_SLICE_III_CONTRACTS:
            with self.subTest(work_package=contract.work_package):
                self.assertEqual(
                    sha256((ROOT / contract.source_path).read_bytes()).hexdigest(),
                    contract.sha256,
                )

    def test_certifier_calls_no_execution_validation_or_slice_iv(self) -> None:
        path = ROOT / "src" / "orion" / "slice_iii_certification_alpha.py"
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
            "generate_relations",
            "construct_navigation",
            "validate_navigation_conformance",
            "construct_orientation_map",
            "validate_orientation_map_conformance",
            "traverse",
            "render_map",
            "begin_slice_iv",
            "invoke_lyra",
            "invoke_sirius",
        }

        self.assertFalse(prohibited & imported_names)
        self.assertFalse(prohibited & called_names)

    def test_canonical_proof_certifies_all_stages_and_stops(self) -> None:
        proof, successful = build_wp25_proof()

        self.assertTrue(successful)
        self.assertTrue(proof["certification"]["certified"])
        self.assertEqual(proof["certification"]["status"], PASSED)
        self.assertTrue(proof["frozen_contracts_verified"])
        self.assertTrue(proof["certification_stages_verified"])
        self.assertTrue(proof["inputs_unchanged"])
        self.assertTrue(proof["certification_replay_byte_identical"])
        self.assertTrue(proof["relations_replay_byte_identical"])
        self.assertTrue(proof["navigation_replay_byte_identical"])
        self.assertTrue(proof["orientation_map_replay_byte_identical"])
        self.assertTrue(proof["provenance_preserved"])
        self.assertFalse(any(proof["downstream_execution"].values()))
        self.assertEqual(proof["stop"], STOP_AT_SLICE_III_CERTIFIED)

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
