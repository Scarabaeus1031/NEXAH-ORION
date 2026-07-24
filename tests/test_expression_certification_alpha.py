"""Focused tests for observational WP29 Expression Certification."""

from __future__ import annotations

import ast
from dataclasses import FrozenInstanceError, asdict, fields
from hashlib import sha256
import inspect
from pathlib import Path
import subprocess
import sys
import unittest

from orion.expression_certification_alpha import (
    CERTIFIED,
    EXPRESSION_CERTIFICATION_SCHEMA_VERSION,
    EXPRESSION_CERTIFICATION_VERSION,
    RESPONSIBILITY,
    STOP_AT_EXPRESSION_CERTIFIED,
    ExpressionCertificationReport,
    canonical_expression_certification_report_bytes,
    certify_expression,
    expression_certification_report_as_dict,
    expression_certification_report_from_dict,
)
from orion.expression_conformance_alpha import (
    canonical_expression_conformance_report_bytes,
)


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from slice_iv_expression_certification_proof import (  # noqa: E402
    WP28_SHA256,
    WP28_SOURCE,
    build_wp29_artifacts,
    build_wp29_proof,
)


PROOF = ROOT / "scripts" / "slice_iv_expression_certification_proof.py"


def unsafe_replace(value: object, **changes: object) -> object:
    clone = object.__new__(type(value))
    for field in fields(value):
        object.__setattr__(
            clone,
            field.name,
            changes.get(field.name, getattr(value, field.name)),
        )
    return clone


class ExpressionCertificationAlphaTests(unittest.TestCase):
    def test_certifier_accepts_exactly_one_wp28_report(self) -> None:
        parameters = tuple(inspect.signature(certify_expression).parameters)

        self.assertEqual(parameters, ("report",))
        with self.assertRaises(TypeError):
            certify_expression({})

    def test_accepted_wp28_report_is_certified(self) -> None:
        artifacts = build_wp29_artifacts()
        conformance = artifacts["expression_conformance"]
        certification = artifacts["expression_certification"]
        conformance_bytes = canonical_expression_conformance_report_bytes(
            conformance
        )

        self.assertIsInstance(
            certification,
            ExpressionCertificationReport,
        )
        self.assertEqual(
            certification.schema_version,
            EXPRESSION_CERTIFICATION_SCHEMA_VERSION,
        )
        self.assertEqual(
            certification.certification_version,
            EXPRESSION_CERTIFICATION_VERSION,
        )
        self.assertEqual(
            certification.expression_conformance_report_id,
            conformance.report_id,
        )
        self.assertEqual(
            certification.expression_conformance_report_integrity,
            sha256(conformance_bytes).hexdigest(),
        )
        self.assertEqual(
            certification.expression_ref,
            conformance.accepted_expression_ref,
        )
        self.assertEqual(certification.decision, CERTIFIED)
        self.assertEqual(
            certification.provenance_ref,
            certification.expression_conformance_report_ref,
        )
        self.assertEqual(certification.responsibility, RESPONSIBILITY)
        self.assertEqual(
            certification.stop,
            STOP_AT_EXPRESSION_CERTIFIED,
        )

    def test_certification_is_immutable_strict_and_replayable(self) -> None:
        first = build_wp29_artifacts()["expression_certification"]
        second = build_wp29_artifacts()["expression_certification"]
        payload = expression_certification_report_as_dict(first)

        with self.assertRaises(FrozenInstanceError):
            first.decision = "failed"
        self.assertEqual(
            expression_certification_report_from_dict(payload),
            first,
        )
        with self.assertRaises(ValueError):
            expression_certification_report_from_dict(
                {**payload, "expression_payload": {}}
            )
        self.assertEqual(
            canonical_expression_certification_report_bytes(first),
            canonical_expression_certification_report_bytes(second),
        )

    def test_rejected_wp28_report_produces_no_certification(self) -> None:
        artifacts = build_wp29_artifacts()
        rejected = unsafe_replace(
            artifacts["expression_conformance"],
            valid=False,
            decision="rejected",
            errors=("not accepted",),
            accepted_expression_ref=None,
        )

        with self.assertRaises(ValueError):
            certify_expression(rejected)

    def test_malformed_wp28_identity_or_stop_is_rejected(self) -> None:
        artifacts = build_wp29_artifacts()
        malformed_id = unsafe_replace(
            artifacts["expression_conformance"],
            report_id="expression-conformance-" + "0" * 24,
        )
        malformed_stop = unsafe_replace(
            artifacts["expression_conformance"],
            stop="at_expression_certified",
        )

        with self.assertRaises(ValueError):
            certify_expression(malformed_id)
        with self.assertRaises(ValueError):
            certify_expression(malformed_stop)

    def test_certification_identity_or_integrity_tampering_is_rejected(
        self,
    ) -> None:
        certification = build_wp29_artifacts()["expression_certification"]
        payload = expression_certification_report_as_dict(certification)

        with self.assertRaises(ValueError):
            expression_certification_report_from_dict(
                {
                    **payload,
                    "certification_id": (
                        "expression-certification-" + "0" * 24
                    ),
                }
            )
        with self.assertRaises(ValueError):
            expression_certification_report_from_dict(
                {**payload, "certification_integrity": "0" * 64}
            )

    def test_certification_does_not_modify_wp28_report(self) -> None:
        artifacts = build_wp29_artifacts()
        conformance = artifacts["expression_conformance"]
        before = canonical_expression_conformance_report_bytes(conformance)

        certify_expression(conformance)
        after = canonical_expression_conformance_report_bytes(conformance)

        self.assertEqual(before, after)

    def test_report_contains_no_payload_language_or_slice_closeout(self) -> None:
        certification = build_wp29_artifacts()["expression_certification"]

        self.assertFalse(
            set(asdict(certification))
            & {
                "expression_artifact",
                "expression_contract",
                "orientation_map",
                "payload",
                "text",
                "generated_language",
                "prompt",
                "provider",
                "html",
                "markdown",
                "graphics",
                "interpretation",
                "reasoning",
                "runtime",
                "gateway",
                "presentation",
                "slice_iv_certified",
            }
        )

    def test_module_reopens_no_previous_or_downstream_artifact(self) -> None:
        path = ROOT / "src" / "orion" / "expression_certification_alpha.py"
        tree = ast.parse(path.read_text(encoding="utf-8"))
        imported_modules = {
            node.module
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and node.module
        }
        orion_modules = {
            module
            for module in imported_modules
            if module.startswith("orion.")
        }
        called_names = {
            node.func.id
            for node in ast.walk(tree)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
        }
        prohibited_calls = {
            "create_expression_contract",
            "construct_expression",
            "validate_expression_conformance",
            "certify_slice_iv",
            "generate_language",
            "invoke_lyra",
            "invoke_sirius",
            "execute_runtime",
        }

        self.assertEqual(
            orion_modules,
            {"orion.expression_conformance_alpha"},
        )
        self.assertFalse(prohibited_calls & called_names)

    def test_frozen_wp28_source_is_unchanged(self) -> None:
        self.assertEqual(
            sha256(WP28_SOURCE.read_bytes()).hexdigest(),
            WP28_SHA256,
        )

    def test_canonical_proof_certifies_and_stops(self) -> None:
        proof, successful = build_wp29_proof()

        self.assertTrue(successful)
        self.assertTrue(proof["frozen_wp28"]["verified"])
        self.assertEqual(
            proof["expression_certification"]["decision"],
            CERTIFIED,
        )
        self.assertTrue(proof["input_unchanged"])
        self.assertTrue(proof["certification_replay_byte_identical"])
        self.assertTrue(proof["wp28_references_verified"])
        self.assertTrue(proof["provenance_preserved"])
        self.assertFalse(any(proof["downstream_execution"].values()))
        self.assertEqual(proof["stop"], STOP_AT_EXPRESSION_CERTIFIED)

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
