"""Focused tests for observational WP24 Orientation Map Conformance."""

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
)
from orion.orientation_map_conformance_alpha import (
    ACCEPTED,
    REJECTED,
    STOP_AFTER_ORIENTATION_MAP_CONFORMANCE,
    OrientationMapConformanceReport,
    canonical_orientation_map_conformance_report_bytes,
    orientation_map_conformance_report_as_dict,
    orientation_map_conformance_report_from_dict,
    validate_orientation_map_conformance,
)
from orion.orientation_map_construction_alpha import (
    canonical_constructed_orientation_map_bytes,
)
from orion.orientation_map_object_alpha import (
    canonical_orientation_map_object_bytes,
)


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from slice_iii_orientation_map_conformance_proof import (  # noqa: E402
    WP23_SHA256,
    WP23_SOURCE,
    build_wp24_artifacts,
    build_wp24_proof,
)
from slice_iii_orientation_map_construction_proof import (  # noqa: E402
    WP21_SHA256,
    WP21_SOURCE,
    WP22_SHA256,
    WP22_SOURCE,
)


PROOF = ROOT / "scripts" / "slice_iii_orientation_map_conformance_proof.py"


def unsafe_replace(value: object, **changes: object) -> object:
    clone = object.__new__(type(value))
    for field in fields(value):
        object.__setattr__(
            clone,
            field.name,
            changes.get(field.name, getattr(value, field.name)),
        )
    return clone


def validate(artifacts, *, orientation_map=None, constructed_map=None):
    return validate_orientation_map_conformance(
        (
            artifacts["orientation_map_object"]
            if orientation_map is None
            else orientation_map
        ),
        (
            artifacts["constructed_orientation_map"]
            if constructed_map is None
            else constructed_map
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


class OrientationMapConformanceAlphaTests(unittest.TestCase):
    def test_canonical_orientation_map_is_accepted(self) -> None:
        report = build_wp24_artifacts()["orientation_map_conformance"]

        self.assertIsInstance(report, OrientationMapConformanceReport)
        self.assertTrue(report.valid)
        self.assertEqual(report.decision, ACCEPTED)
        self.assertEqual(report.errors, ())
        self.assertEqual(
            report.accepted_orientation_map_ref,
            report.orientation_map_ref,
        )
        self.assertEqual(
            report.accepted_construction_ref,
            report.construction_ref,
        )
        self.assertEqual(
            report.stop,
            STOP_AFTER_ORIENTATION_MAP_CONFORMANCE,
        )

    def test_malformed_orientation_map_object_is_rejected(self) -> None:
        artifacts = build_wp24_artifacts()
        malformed = unsafe_replace(
            artifacts["orientation_map_object"],
            orientation_map_integrity="0" * 64,
        )

        report = validate(artifacts, orientation_map=malformed)

        self.assertEqual(report.decision, REJECTED)
        self.assertIn("Orientation Map Object is malformed", report.errors)

    def test_malformed_constructed_map_is_rejected(self) -> None:
        artifacts = build_wp24_artifacts()
        malformed = unsafe_replace(
            artifacts["constructed_orientation_map"],
            construction_integrity="0" * 64,
        )

        report = validate(artifacts, constructed_map=malformed)

        self.assertEqual(report.decision, REJECTED)
        self.assertIn(
            "Constructed Orientation Map is malformed",
            report.errors,
        )

    def test_duplicate_entry_is_rejected(self) -> None:
        artifacts = build_wp24_artifacts()
        constructed = artifacts["constructed_orientation_map"]
        malformed = unsafe_replace(
            constructed,
            entries=constructed.entries[:-1] + (constructed.entries[0],),
        )

        report = validate(artifacts, constructed_map=malformed)

        self.assertEqual(report.decision, REJECTED)
        self.assertIn(
            "Constructed Orientation Map contains duplicate entries or references",
            report.errors,
        )

    def test_invalid_navigation_reference_is_rejected(self) -> None:
        artifacts = build_wp24_artifacts()
        constructed = artifacts["constructed_orientation_map"]
        invalid = unsafe_replace(
            constructed.entries[-1],
            navigation_entry_ref="sha256:" + "0" * 64,
        )
        malformed = unsafe_replace(
            constructed,
            entries=constructed.entries[:-1] + (invalid,),
        )

        report = validate(artifacts, constructed_map=malformed)

        self.assertIn(
            "Orientation Map Entries do not exactly reference Navigation Entries",
            report.errors,
        )

    def test_invalid_relation_reference_is_rejected(self) -> None:
        artifacts = build_wp24_artifacts()
        constructed = artifacts["constructed_orientation_map"]
        invalid = unsafe_replace(
            constructed.entries[-1],
            relation_ref="sha256:" + "0" * 64,
        )
        malformed = unsafe_replace(
            constructed,
            entries=constructed.entries[:-1] + (invalid,),
        )

        report = validate(artifacts, constructed_map=malformed)

        self.assertIn(
            "Orientation Map Entries do not exactly reference certified Relations",
            report.errors,
        )

    def test_invalid_adjacency_reference_is_rejected(self) -> None:
        artifacts = build_wp24_artifacts()
        constructed = artifacts["constructed_orientation_map"]
        index = next(
            index
            for index, entry in enumerate(constructed.entries)
            if entry.structural_adjacency_ref is not None
        )
        invalid = unsafe_replace(
            constructed.entries[index],
            structural_adjacency_ref="sha256:" + "0" * 64,
        )
        entries = list(constructed.entries)
        entries[index] = invalid
        malformed = unsafe_replace(constructed, entries=tuple(entries))

        report = validate(artifacts, constructed_map=malformed)

        self.assertIn(
            "Orientation Map adjacency differs from certified Navigation",
            report.errors,
        )

    def test_invalid_provenance_is_rejected(self) -> None:
        artifacts = build_wp24_artifacts()
        constructed = artifacts["constructed_orientation_map"]
        invalid = unsafe_replace(
            constructed.entries[-1],
            provenance_ref="sha256:" + "0" * 64,
        )
        malformed = unsafe_replace(
            constructed,
            entries=constructed.entries[:-1] + (invalid,),
        )

        report = validate(artifacts, constructed_map=malformed)

        self.assertIn(
            "Orientation Map provenance does not preserve certified lineage",
            report.errors,
        )

    def test_ordering_violation_is_rejected(self) -> None:
        artifacts = build_wp24_artifacts()
        constructed = artifacts["constructed_orientation_map"]
        malformed = unsafe_replace(
            constructed,
            entries=tuple(reversed(constructed.entries)),
        )

        report = validate(artifacts, constructed_map=malformed)

        self.assertIn(
            "Orientation Map ordering differs from certified Navigation",
            report.errors,
        )

    def test_identity_or_integrity_tamper_is_rejected(self) -> None:
        artifacts = build_wp24_artifacts()
        malformed = unsafe_replace(
            artifacts["constructed_orientation_map"],
            construction_id="orientation-map-construction-" + "0" * 24,
        )

        report = validate(artifacts, constructed_map=malformed)

        self.assertEqual(report.decision, REJECTED)
        self.assertIn(
            "Constructed Orientation Map is malformed",
            report.errors,
        )

    def test_forbidden_candidate_state_is_rejected(self) -> None:
        artifacts = build_wp24_artifacts()
        malformed = unsafe_replace(
            artifacts["constructed_orientation_map"],
            construction_state="rendered",
        )

        report = validate(artifacts, constructed_map=malformed)

        self.assertIn(
            "Constructed Orientation Map is not the exact WP23 candidate state",
            report.errors,
        )

    def test_report_is_immutable_strict_and_results_only(self) -> None:
        report = build_wp24_artifacts()["orientation_map_conformance"]
        payload = orientation_map_conformance_report_as_dict(report)

        with self.assertRaises(FrozenInstanceError):
            report.valid = False
        self.assertEqual(
            orientation_map_conformance_report_from_dict(payload),
            report,
        )
        with self.assertRaises(ValueError):
            orientation_map_conformance_report_from_dict(
                {**payload, "repaired_entries": ()}
            )
        self.assertFalse(
            set(asdict(report))
            & {
                "entries",
                "coordinates",
                "geometry",
                "layout",
                "repairs",
                "normalization",
                "orientation_map_certification",
            }
        )

    def test_report_and_rejection_replay_are_byte_identical(self) -> None:
        first = build_wp24_artifacts()["orientation_map_conformance"]
        second = build_wp24_artifacts()["orientation_map_conformance"]
        self.assertEqual(
            canonical_orientation_map_conformance_report_bytes(first),
            canonical_orientation_map_conformance_report_bytes(second),
        )

        artifacts = build_wp24_artifacts()
        malformed = unsafe_replace(
            artifacts["constructed_orientation_map"],
            construction_integrity="0" * 64,
        )
        first_rejection = validate(artifacts, constructed_map=malformed)
        second_rejection = validate(artifacts, constructed_map=malformed)
        self.assertEqual(
            canonical_orientation_map_conformance_report_bytes(
                first_rejection
            ),
            canonical_orientation_map_conformance_report_bytes(
                second_rejection
            ),
        )

    def test_validation_leaves_map_inputs_unchanged(self) -> None:
        artifacts = build_wp24_artifacts()
        before = (
            canonical_orientation_map_object_bytes(
                artifacts["orientation_map_object"]
            ),
            canonical_constructed_orientation_map_bytes(
                artifacts["constructed_orientation_map"]
            ),
        )

        report = validate(artifacts)
        after = (
            canonical_orientation_map_object_bytes(
                artifacts["orientation_map_object"]
            ),
            canonical_constructed_orientation_map_bytes(
                artifacts["constructed_orientation_map"]
            ),
        )

        self.assertTrue(report.inputs_unchanged)
        self.assertEqual(before, after)

    def test_validator_calls_no_constructor_or_certification(self) -> None:
        path = ROOT / "src" / "orion" / "orientation_map_conformance_alpha.py"
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
            "create_orientation_map_object",
            "certify_orientation_map",
            "certify_slice_iii",
            "render_map",
            "compute_geometry",
            "traverse",
        }

        self.assertFalse(prohibited & imported_names)
        self.assertFalse(prohibited & called_names)

    def test_frozen_wp18_through_wp23_sources_are_unchanged(self) -> None:
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
            ("WP23", WP23_SOURCE, WP23_SHA256),
        )
        for work_package, path, expected in records:
            with self.subTest(work_package=work_package):
                self.assertEqual(
                    sha256(path.read_bytes()).hexdigest(),
                    expected,
                )

    def test_canonical_proof_validates_and_stops(self) -> None:
        proof, successful = build_wp24_proof()

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
            STOP_AFTER_ORIENTATION_MAP_CONFORMANCE,
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
