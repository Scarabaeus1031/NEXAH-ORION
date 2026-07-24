"""Focused tests for observational WP21 Navigation Certification."""

from __future__ import annotations

import ast
from dataclasses import FrozenInstanceError, asdict, fields
from hashlib import sha256
from pathlib import Path
import subprocess
import sys
import unittest

from orion.navigation_certification_alpha import (
    FAILED,
    FROZEN_NAVIGATION_CONTRACTS,
    PASSED,
    STOP_AT_NAVIGATION_CERTIFIED,
    NavigationCertificationReport,
    canonical_navigation_certification_report_bytes,
    certify_navigation,
    navigation_certification_report_as_dict,
    navigation_certification_report_from_dict,
)
from orion.navigation_conformance_alpha import (
    canonical_navigation_conformance_report_bytes,
)
from orion.navigation_construction_alpha import (
    canonical_constructed_navigation_bytes,
)
from orion.navigation_object_alpha import canonical_navigation_object_bytes


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from slice_iii_navigation_certification_proof import (  # noqa: E402
    build_wp21_artifacts,
    build_wp21_proof,
)


PROOF = ROOT / "scripts" / "slice_iii_navigation_certification_proof.py"


def unsafe_replace(value: object, **changes: object) -> object:
    clone = object.__new__(type(value))
    for field in fields(value):
        object.__setattr__(
            clone,
            field.name,
            changes.get(field.name, getattr(value, field.name)),
        )
    return clone


def certify(artifacts, *, conformance=None, constructed=None):
    return certify_navigation(
        artifacts["navigation"],
        (
            artifacts["constructed_navigation"]
            if constructed is None
            else constructed
        ),
        (
            artifacts["navigation_conformance"]
            if conformance is None
            else conformance
        ),
        artifacts["relation_set"],
        artifacts["certification"],
        artifacts["summary"],
        artifacts["statistics"],
    )


class NavigationCertificationAlphaTests(unittest.TestCase):
    def test_accepted_navigation_layer_is_certified(self) -> None:
        certification = build_wp21_artifacts()["navigation_certification"]

        self.assertIsInstance(certification, NavigationCertificationReport)
        self.assertTrue(certification.certified)
        self.assertEqual(certification.status, PASSED)
        self.assertEqual(certification.errors, ())
        self.assertEqual(
            certification.stop,
            STOP_AT_NAVIGATION_CERTIFIED,
        )
        self.assertTrue(certification.navigation_replay_byte_identical)
        self.assertTrue(certification.construction_replay_byte_identical)
        self.assertTrue(
            certification.conformance_report_replay_byte_identical
        )

    def test_rejected_wp20_report_blocks_certification(self) -> None:
        artifacts = build_wp21_artifacts()
        rejected = unsafe_replace(
            artifacts["navigation_conformance"],
            valid=False,
            decision="rejected",
            errors=("declared rejection",),
            accepted_construction_ref=None,
        )

        certification = certify(artifacts, conformance=rejected)

        self.assertFalse(certification.certified)
        self.assertEqual(certification.status, FAILED)
        self.assertIn(
            "Navigation Conformance Report is malformed or not immutable",
            certification.errors,
        )

    def test_inconsistent_construction_blocks_certification(self) -> None:
        artifacts = build_wp21_artifacts()
        inconsistent = unsafe_replace(
            artifacts["constructed_navigation"],
            navigation_id="navigation-" + "0" * 24,
        )

        certification = certify(artifacts, constructed=inconsistent)

        self.assertFalse(certification.certified)
        self.assertEqual(certification.status, FAILED)
        self.assertIn(
            "Navigation Construction is malformed or not immutable",
            certification.errors,
        )

    def test_certification_does_not_modify_inputs(self) -> None:
        artifacts = build_wp21_artifacts()
        before = (
            canonical_navigation_object_bytes(artifacts["navigation"]),
            canonical_constructed_navigation_bytes(
                artifacts["constructed_navigation"]
            ),
            canonical_navigation_conformance_report_bytes(
                artifacts["navigation_conformance"]
            ),
        )

        certification = certify(artifacts)
        after = (
            canonical_navigation_object_bytes(artifacts["navigation"]),
            canonical_constructed_navigation_bytes(
                artifacts["constructed_navigation"]
            ),
            canonical_navigation_conformance_report_bytes(
                artifacts["navigation_conformance"]
            ),
        )

        self.assertTrue(certification.inputs_unchanged)
        self.assertEqual(before, after)

    def test_certification_report_is_immutable_and_strict(self) -> None:
        certification = build_wp21_artifacts()["navigation_certification"]
        payload = navigation_certification_report_as_dict(certification)

        with self.assertRaises(FrozenInstanceError):
            certification.certified = False
        self.assertEqual(
            navigation_certification_report_from_dict(payload),
            certification,
        )
        with self.assertRaises(ValueError):
            navigation_certification_report_from_dict(
                {**payload, "orientation_map_ready": True}
            )

    def test_certification_replay_is_byte_identical(self) -> None:
        first = build_wp21_artifacts()["navigation_certification"]
        second = build_wp21_artifacts()["navigation_certification"]

        self.assertEqual(first, second)
        self.assertEqual(
            canonical_navigation_certification_report_bytes(first),
            canonical_navigation_certification_report_bytes(second),
        )

    def test_frozen_wp18_through_wp20_hashes_match_repository(self) -> None:
        for contract in FROZEN_NAVIGATION_CONTRACTS:
            with self.subTest(work_package=contract.work_package):
                self.assertEqual(
                    sha256((ROOT / contract.source_path).read_bytes()).hexdigest(),
                    contract.sha256,
                )

    def test_certification_preserves_exact_artifact_references(self) -> None:
        artifacts = build_wp21_artifacts()
        certification = artifacts["navigation_certification"]

        self.assertEqual(
            certification.navigation_ref,
            artifacts["navigation_conformance"].navigation_ref,
        )
        self.assertEqual(
            certification.construction_ref,
            artifacts["navigation_conformance"].construction_ref,
        )
        self.assertEqual(
            certification.conformance_report_ref,
            "sha256:"
            + sha256(
                canonical_navigation_conformance_report_bytes(
                    artifacts["navigation_conformance"]
                )
            ).hexdigest(),
        )
        self.assertTrue(certification.provenance_preserved)

    def test_canonical_order_is_observed_from_accepted_wp20(self) -> None:
        certification = build_wp21_artifacts()["navigation_certification"]

        self.assertTrue(certification.stable_canonical_ordering)
        self.assertIn(
            "stable_canonical_ordering",
            certification.checks,
        )

    def test_report_contains_no_navigation_behavior_or_map(self) -> None:
        certification = build_wp21_artifacts()["navigation_certification"]
        keys = set(asdict(certification))

        self.assertFalse(
            keys
            & {
                "entries",
                "relations",
                "routes",
                "traversal",
                "movements",
                "repairs",
                "orientation_map",
            }
        )

    def test_certifier_calls_no_constructor_validator_or_downstream(self) -> None:
        path = ROOT / "src" / "orion" / "navigation_certification_alpha.py"
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
            "construct_navigation",
            "validate_navigation_conformance",
            "traverse",
            "find_path",
            "search_graph",
            "construct_orientation_map",
        }

        self.assertFalse(prohibited & imported_names)
        self.assertFalse(prohibited & called_names)

    def test_canonical_proof_certifies_and_stops(self) -> None:
        proof, successful = build_wp21_proof()

        self.assertTrue(successful)
        self.assertTrue(proof["certification"]["certified"])
        self.assertEqual(proof["certification"]["status"], PASSED)
        self.assertTrue(proof["inputs_unchanged"])
        self.assertTrue(proof["certification_replay_byte_identical"])
        self.assertTrue(proof["frozen_navigation_contracts_verified"])
        self.assertTrue(proof["package_proof_replays_verified"])
        self.assertTrue(proof["provenance_preserved"])
        self.assertFalse(any(proof["downstream_execution"].values()))
        self.assertEqual(proof["stop"], STOP_AT_NAVIGATION_CERTIFIED)

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
