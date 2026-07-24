"""Executable proof tests for Slice II Structural Expansion II."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parent.parent
PROOF = ROOT / "scripts" / "slice_ii_structural_expansion_ii_proofs.py"


def execute_proof() -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(PROOF)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )


class SliceIIStructuralExpansionIIProofTests(unittest.TestCase):
    def test_each_work_package_has_a_valid_bounded_proof(self) -> None:
        result = execute_proof()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        value = json.loads(result.stdout)
        self.assertTrue(value["all_proofs_valid"])
        self.assertEqual(
            tuple(proof["work_package"] for proof in value["proofs"]),
            ("WP5", "WP6", "WP7"),
        )
        for proof in value["proofs"]:
            with self.subTest(work_package=proof["work_package"]):
                self.assertTrue(proof["external_conformance"]["valid"])
                self.assertTrue(proof["required_kinds_present"])
                self.assertTrue(
                    proof["determinism"][
                        "representation_byte_identical_replay"
                    ]
                )
                self.assertTrue(
                    proof["determinism"]["inventory_byte_identical_replay"]
                )
                self.assertEqual(
                    proof["stop"],
                    "after_declared_source_element_inventory",
                )
                self.assertFalse(proof["summary_executed"])
                self.assertFalse(proof["statistics_executed"])
                self.assertFalse(proof["relations_created"])
                self.assertFalse(proof["navigation_executed"])
                self.assertEqual(proof["semantic_processing"], "none")
                self.assertFalse(proof["runtime_executed"])
                self.assertFalse(proof["gateway_executed"])

    def test_complete_proof_output_is_byte_identical(self) -> None:
        first = execute_proof()
        second = execute_proof()

        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(first.stdout, second.stdout)


if __name__ == "__main__":
    unittest.main()
