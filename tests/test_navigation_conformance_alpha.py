"""Focused tests for observational WP20 Navigation Conformance."""

from __future__ import annotations

import ast
from dataclasses import FrozenInstanceError, asdict, fields
from hashlib import sha256
from pathlib import Path
import subprocess
import sys
import unittest

from orion.navigation_conformance_alpha import (
    ACCEPTED,
    REJECTED,
    STOP_AFTER_NAVIGATION_CONFORMANCE,
    NavigationConformanceReport,
    canonical_navigation_conformance_report_bytes,
    navigation_conformance_report_as_dict,
    navigation_conformance_report_from_dict,
    validate_navigation_conformance,
)
from orion.navigation_construction_alpha import (
    canonical_constructed_navigation_bytes,
)
from orion.navigation_object_alpha import canonical_navigation_object_bytes
from orion.relations_certification_alpha import FROZEN_RELATIONS_CONTRACTS


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from slice_iii_navigation_conformance_proof import (  # noqa: E402
    WP19_SHA256,
    WP19_SOURCE,
    build_wp20_artifacts,
    build_wp20_proof,
)
from slice_iii_navigation_construction_proof import (  # noqa: E402
    WP17_SHA256,
    WP17_SOURCE,
    WP18_SHA256,
    WP18_SOURCE,
)


PROOF = ROOT / "scripts" / "slice_iii_navigation_conformance_proof.py"


def unsafe_replace(value: object, **changes: object) -> object:
    clone = object.__new__(type(value))
    for field in fields(value):
        object.__setattr__(
            clone,
            field.name,
            changes.get(field.name, getattr(value, field.name)),
        )
    return clone


def validate(artifacts, *, constructed=None):
    return validate_navigation_conformance(
        (
            artifacts["constructed_navigation"]
            if constructed is None
            else constructed
        ),
        artifacts["navigation"],
        artifacts["relation_set"],
        artifacts["certification"],
        artifacts["summary"],
        artifacts["statistics"],
    )


class NavigationConformanceAlphaTests(unittest.TestCase):
    def test_canonical_navigation_is_accepted(self) -> None:
        artifacts = build_wp20_artifacts()
        report = artifacts["navigation_conformance"]

        self.assertIsInstance(report, NavigationConformanceReport)
        self.assertTrue(report.valid)
        self.assertEqual(report.decision, ACCEPTED)
        self.assertEqual(report.errors, ())
        self.assertEqual(
            report.accepted_construction_ref,
            report.construction_ref,
        )
        self.assertEqual(report.stop, STOP_AFTER_NAVIGATION_CONFORMANCE)

    def test_malformed_construction_is_rejected_without_repair(self) -> None:
        artifacts = build_wp20_artifacts()
        malformed = unsafe_replace(
            artifacts["constructed_navigation"],
            construction_integrity="0" * 64,
        )

        report = validate(artifacts, constructed=malformed)

        self.assertFalse(report.valid)
        self.assertEqual(report.decision, REJECTED)
        self.assertIn(
            "Constructed Navigation schema, identity, or STOP is malformed",
            report.errors,
        )
        self.assertIsNone(report.accepted_construction_ref)

    def test_duplicate_entries_are_rejected(self) -> None:
        artifacts = build_wp20_artifacts()
        constructed = artifacts["constructed_navigation"]
        duplicate_entries = constructed.entries[:-1] + (
            constructed.entries[0],
        )
        malformed = unsafe_replace(constructed, entries=duplicate_entries)

        report = validate(artifacts, constructed=malformed)

        self.assertFalse(report.valid)
        self.assertIn(
            "Constructed Navigation contains duplicate entries or references",
            report.errors,
        )

    def test_invalid_relation_reference_is_rejected(self) -> None:
        artifacts = build_wp20_artifacts()
        constructed = artifacts["constructed_navigation"]
        entry = constructed.entries[-1]
        invalid_entry = unsafe_replace(
            entry,
            relation_ref="sha256:" + "0" * 64,
        )
        malformed = unsafe_replace(
            constructed,
            entries=constructed.entries[:-1] + (invalid_entry,),
        )

        report = validate(artifacts, constructed=malformed)

        self.assertFalse(report.valid)
        self.assertIn(
            "Navigation Entries do not exactly reference certified Relations",
            report.errors,
        )

    def test_invalid_provenance_is_rejected(self) -> None:
        artifacts = build_wp20_artifacts()
        constructed = artifacts["constructed_navigation"]
        entry = constructed.entries[-1]
        invalid_entry = unsafe_replace(
            entry,
            provenance_ref="sha256:" + "0" * 64,
        )
        malformed = unsafe_replace(
            constructed,
            entries=constructed.entries[:-1] + (invalid_entry,),
        )

        report = validate(artifacts, constructed=malformed)

        self.assertFalse(report.valid)
        self.assertIn(
            "Navigation provenance does not preserve certified lineage",
            report.errors,
        )

    def test_reordered_entries_are_rejected(self) -> None:
        artifacts = build_wp20_artifacts()
        constructed = artifacts["constructed_navigation"]
        malformed = unsafe_replace(
            constructed,
            entries=tuple(reversed(constructed.entries)),
        )

        report = validate(artifacts, constructed=malformed)

        self.assertFalse(report.valid)
        self.assertIn(
            "Navigation Entry ordering differs from certified Relations",
            report.errors,
        )

    def test_report_is_immutable_and_strict(self) -> None:
        report = build_wp20_artifacts()["navigation_conformance"]
        payload = navigation_conformance_report_as_dict(report)

        with self.assertRaises(FrozenInstanceError):
            report.valid = False
        self.assertEqual(
            navigation_conformance_report_from_dict(payload),
            report,
        )
        with self.assertRaises(ValueError):
            navigation_conformance_report_from_dict(
                {**payload, "repaired_navigation": True}
            )

    def test_report_replay_is_byte_identical(self) -> None:
        first_artifacts = build_wp20_artifacts()
        second_artifacts = build_wp20_artifacts()

        self.assertEqual(
            canonical_navigation_conformance_report_bytes(
                first_artifacts["navigation_conformance"]
            ),
            canonical_navigation_conformance_report_bytes(
                second_artifacts["navigation_conformance"]
            ),
        )

    def test_validation_leaves_navigation_inputs_unchanged(self) -> None:
        artifacts = build_wp20_artifacts()
        before = (
            canonical_constructed_navigation_bytes(
                artifacts["constructed_navigation"]
            ),
            canonical_navigation_object_bytes(artifacts["navigation"]),
        )

        report = validate(artifacts)
        after = (
            canonical_constructed_navigation_bytes(
                artifacts["constructed_navigation"]
            ),
            canonical_navigation_object_bytes(artifacts["navigation"]),
        )

        self.assertTrue(report.inputs_unchanged)
        self.assertEqual(before, after)

    def test_report_contains_results_only(self) -> None:
        report = build_wp20_artifacts()["navigation_conformance"]
        keys = set(asdict(report))

        self.assertFalse(
            keys
            & {
                "entries",
                "relations",
                "routes",
                "traversal",
                "repairs",
                "normalized_navigation",
                "navigation_certification",
                "orientation_map",
            }
        )

    def test_validator_calls_no_constructor_or_downstream_behavior(self) -> None:
        path = ROOT / "src" / "orion" / "navigation_conformance_alpha.py"
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
            "traverse",
            "find_path",
            "search_graph",
            "certify_navigation",
            "construct_orientation_map",
        }

        self.assertFalse(prohibited & imported_names)
        self.assertFalse(prohibited & called_names)

    def test_frozen_wp12_through_wp19_sources_are_unchanged(self) -> None:
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
            ("WP19", WP19_SOURCE, WP19_SHA256),
        )
        for work_package, path, expected in records:
            with self.subTest(work_package=work_package):
                self.assertEqual(
                    sha256(path.read_bytes()).hexdigest(),
                    expected,
                )

    def test_canonical_proof_validates_and_stops(self) -> None:
        proof, successful = build_wp20_proof()

        self.assertTrue(successful)
        self.assertTrue(proof["conformance"]["valid"])
        self.assertEqual(proof["conformance"]["decision"], ACCEPTED)
        self.assertTrue(proof["frozen_dependencies_verified"])
        self.assertTrue(proof["inputs_unchanged"])
        self.assertTrue(proof["report_replay_byte_identical"])
        self.assertTrue(proof["provenance_verified"])
        self.assertFalse(any(proof["downstream_execution"].values()))
        self.assertEqual(
            proof["stop"],
            STOP_AFTER_NAVIGATION_CONFORMANCE,
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
