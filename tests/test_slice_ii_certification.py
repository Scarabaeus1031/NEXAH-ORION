"""Certification tests for the complete bounded Vertical Slice II."""

from __future__ import annotations

import ast
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from slice_ii_certification_proof import (  # noqa: E402
    CAPABILITY_PROOFS,
    CERTIFICATION_STATE,
    FIXTURE,
    FIXTURE_SHA256,
    STOP_AT_SLICE_II_COMPLETE,
    build_slice_ii_certification,
    canonical_certification_bytes,
)


PROOF = ROOT / "scripts" / "slice_ii_certification_proof.py"


class SliceIICertificationTests(unittest.TestCase):
    def test_complete_chain_reaches_slice_ii_complete_and_stops(self) -> None:
        proof, certified = build_slice_ii_certification()

        self.assertTrue(certified)
        self.assertTrue(proof["certified"])
        self.assertEqual(proof["certification_state"], CERTIFICATION_STATE)
        self.assertEqual(proof["stop"], STOP_AT_SLICE_II_COMPLETE)
        self.assertEqual(
            proof["chain"],
            (
                "confirmed_markdown",
                "projection",
                "renderer",
                "immutable_structural_representation",
                "external_conformance",
                "understand_inventory",
                "structural_summary",
                "structural_statistics",
                "slice_ii_complete",
                "stop",
            ),
        )

    def test_every_definition_of_done_condition_is_true(self) -> None:
        proof, certified = build_slice_ii_certification()

        self.assertTrue(certified)
        self.assertGreaterEqual(len(proof["definition_of_done"]), 25)
        self.assertTrue(all(proof["definition_of_done"].values()))

    def test_every_artifact_is_immutable_and_byte_identical(self) -> None:
        proof, certified = build_slice_ii_certification()

        self.assertTrue(certified)
        self.assertTrue(all(proof["artifact_replay"].values()))
        self.assertTrue(all(proof["immutability"].values()))
        self.assertTrue(proof["provenance_verified"])
        for artifact in proof["artifacts"].values():
            self.assertEqual(len(artifact["sha256"]), 64)
            self.assertGreater(artifact["byte_length"], 0)

    def test_every_capability_proof_replays_byte_identically(self) -> None:
        proof, certified = build_slice_ii_certification()

        self.assertTrue(certified)
        replays = proof["capability_proof_replays"]
        self.assertEqual(
            tuple(replay["proof"] for replay in replays),
            CAPABILITY_PROOFS,
        )
        self.assertTrue(all(replay["byte_identical"] for replay in replays))
        self.assertTrue(all(len(replay["sha256"]) == 64 for replay in replays))
        self.assertTrue(all(replay["byte_length"] > 0 for replay in replays))

    def test_responsibility_and_negative_boundaries_are_certified(self) -> None:
        proof, certified = build_slice_ii_certification()

        self.assertTrue(certified)
        self.assertTrue(all(proof["responsibility_boundaries"].values()))
        self.assertTrue(all(proof["negative_boundary_checks"].values()))
        self.assertTrue(proof["utf8_verified"])
        self.assertTrue(proof["interval_union_verified"])

    def test_fixture_integrity_is_exact(self) -> None:
        proof, certified = build_slice_ii_certification()

        self.assertTrue(certified)
        self.assertEqual(sha256(FIXTURE.read_bytes()).hexdigest(), FIXTURE_SHA256)
        self.assertTrue(proof["fixture"]["integrity_verified"])
        self.assertEqual(proof["fixture"]["sha256"], FIXTURE_SHA256)

    def test_no_downstream_capability_executes(self) -> None:
        proof, certified = build_slice_ii_certification()

        self.assertTrue(certified)
        self.assertFalse(any(proof["downstream_execution"].values()))

    def test_certification_is_byte_identical_in_process(self) -> None:
        first, first_certified = build_slice_ii_certification()
        second, second_certified = build_slice_ii_certification()

        self.assertTrue(first_certified and second_certified)
        self.assertEqual(
            canonical_certification_bytes(first),
            canonical_certification_bytes(second),
        )

    def test_executable_certification_replays_byte_identically(self) -> None:
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
        self.assertEqual(second.stderr, b"")
        self.assertEqual(first.stdout, second.stdout)
        proof = json.loads(first.stdout)
        self.assertTrue(proof["certified"])
        self.assertEqual(proof["stop"], STOP_AT_SLICE_II_COMPLETE)

    def test_certification_imports_no_runtime_gateway_or_downstream_module(
        self,
    ) -> None:
        tree = ast.parse(PROOF.read_text(encoding="utf-8"))
        imported_modules = {
            node.module
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and node.module is not None
        }
        prohibited_fragments = (
            "orientation_runtime",
            "gateway",
            "relation",
            "navigation",
            "lyra",
            "sirius",
        )

        self.assertFalse(
            any(
                fragment in module
                for module in imported_modules
                for fragment in prohibited_fragments
            )
        )


if __name__ == "__main__":
    unittest.main()
