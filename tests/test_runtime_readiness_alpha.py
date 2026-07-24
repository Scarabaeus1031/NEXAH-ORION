"""Tests for the bounded Runtime Readiness Validation Alpha proof."""

from __future__ import annotations

import ast
from dataclasses import FrozenInstanceError
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

from orion.public_contracts.fixtures import VALID_REQUEST
from orion.readiness_alpha import (
    RuntimeReadinessDiagnostic,
    _ReadinessProbe,
    prove_runtime_readiness,
)


ROOT = Path(__file__).resolve().parent.parent
PROOF = ROOT / "scripts" / "runtime_readiness_alpha_proof.py"
NEXAHEDRON_ROOT = Path(
    os.environ.get("NEXAHEDRON_ROOT", ROOT.parent / "NEXAHEDRON")
)
HAS_NEXAHEDRON_ALPHA = (
    NEXAHEDRON_ROOT / "scripts" / "representation-referenced-request.mjs"
).is_file()


def execute_proof() -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(PROOF)],
        cwd=ROOT,
        env={
            **os.environ,
            "PYTHONPATH": str(ROOT / "src"),
        },
        check=False,
        capture_output=True,
        text=True,
    )


class RuntimeReadinessAlphaTests(unittest.TestCase):
    def test_existing_runtime_rules_classify_one_valid_request_as_ready(self) -> None:
        diagnostic = prove_runtime_readiness(VALID_REQUEST)

        self.assertEqual(diagnostic.decision, "ready")
        self.assertEqual(diagnostic.stop, "before_processing")
        self.assertEqual(diagnostic.request_id, VALID_REQUEST.request_id)
        self.assertEqual(
            diagnostic.checks,
            (
                "contract_validation:valid",
                "mode_support:supported",
                "clarification:none",
                "source_access:available",
            ),
        )
        with self.assertRaises(FrozenInstanceError):
            diagnostic.decision = "changed"  # type: ignore[misc]

    def test_probe_cannot_enter_any_downstream_result_path(self) -> None:
        forbidden = AssertionError("downstream Runtime path executed")
        with (
            patch.object(
                _ReadinessProbe,
                "_blocked_report",
                side_effect=forbidden,
            ),
            patch.object(
                _ReadinessProbe,
                "_complete_report",
                side_effect=forbidden,
            ),
            patch.object(
                _ReadinessProbe,
                "_continuation",
                side_effect=forbidden,
            ),
            patch.object(
                _ReadinessProbe,
                "_publish",
                side_effect=forbidden,
            ),
        ):
            diagnostic = prove_runtime_readiness(VALID_REQUEST)

        self.assertEqual(diagnostic.stop, "before_processing")

    def test_diagnostic_is_internal_and_not_a_public_contract(self) -> None:
        import orion
        import orion.readiness_alpha as readiness_alpha

        diagnostic = prove_runtime_readiness(VALID_REQUEST)

        self.assertEqual(readiness_alpha.__all__, ())
        self.assertNotIn("RuntimeReadinessDiagnostic", orion.__all__)
        self.assertIsInstance(diagnostic, RuntimeReadinessDiagnostic)
        self.assertFalse(hasattr(diagnostic, "schema_version"))

    @unittest.skipUnless(
        HAS_NEXAHEDRON_ALPHA,
        "accepted NEXAHEDRON Alpha checkout is not connected",
    )
    def test_cross_repository_proof_preserves_exact_lineage(self) -> None:
        result = execute_proof()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        proof = json.loads(result.stdout)
        self.assertEqual(proof["diagnostic_kind"], "internal_runtime_readiness_proof")
        self.assertEqual(proof["readiness"]["decision"], "ready")
        self.assertEqual(proof["readiness"]["stop"], "before_processing")
        self.assertEqual(proof["stop"], "before_processing")
        self.assertTrue(proof["public_contract_validation"]["valid"])
        self.assertEqual(proof["public_contract_validation"]["errors"], [])
        self.assertTrue(all(proof["lineage"]["checks"].values()))
        self.assertEqual(
            proof["lineage"]["representation_ref"],
            "representation-ec8b75a6dec2ab21@sha256:9c71a8186680b9cb2c23cd11a374e876c0b78d5ff2ecf5f1eb23f007dd7366fd",
        )

    @unittest.skipUnless(
        HAS_NEXAHEDRON_ALPHA,
        "accepted NEXAHEDRON Alpha checkout is not connected",
    )
    def test_cross_repository_proof_is_byte_identical(self) -> None:
        first = execute_proof()
        second = execute_proof()

        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual(
            sha256(first.stdout.encode("utf-8")).hexdigest(),
            "dd8547f2e4b110e992ebb99079dd7d39a73f8da98e814b0dd9a1d347fc07eaf1",
        )

    def test_alpha_modules_contain_no_forbidden_downstream_dependencies(self) -> None:
        imported_modules: set[str] = set()
        forbidden_calls: set[str] = set()
        for path in (
            ROOT / "src" / "orion" / "readiness_alpha.py",
            PROOF,
        ):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imported_modules.update(alias.name for alias in node.names)
                elif isinstance(node, ast.ImportFrom):
                    imported_modules.add(node.module or "")
                elif isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name):
                        forbidden_calls.add(node.func.id)
                    elif isinstance(node.func, ast.Attribute):
                        forbidden_calls.add(node.func.attr)

        self.assertTrue(
            {
                "orion.gateway.gateway",
                "orion.gateway.presentation",
                "orion.operator_registry",
                "orion.public_contracts.fixtures",
                "orion.lyra",
                "requests",
                "urllib",
            }.isdisjoint(imported_modules)
        )
        self.assertTrue(
            {
                "orient",
                "_blocked_report",
                "_complete_report",
                "_continuation",
                "_publish",
                "fetch",
            }.isdisjoint(forbidden_calls)
        )


if __name__ == "__main__":
    unittest.main()
