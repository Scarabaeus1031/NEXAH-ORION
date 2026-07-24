"""Focused tests for observational WP30 Vertical Slice IV Certification."""

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
    canonical_expression_certification_report_bytes,
)
from orion.slice_iv_certification_alpha import (
    CERTIFIED,
    RESPONSIBILITY,
    SLICE_IV_CERTIFICATION_SCHEMA_VERSION,
    SLICE_IV_CERTIFICATION_VERSION,
    STOP_AT_SLICE_IV_CERTIFIED,
    SliceIVCertificationReport,
    canonical_slice_iv_certification_report_bytes,
    certify_slice_iv,
    slice_iv_certification_report_as_dict,
    slice_iv_certification_report_from_dict,
)


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from slice_iv_certification_proof import (  # noqa: E402
    FROZEN_SLICE_IV_SOURCES,
    build_wp30_artifacts,
    build_wp30_proof,
)


PROOF = ROOT / "scripts" / "slice_iv_certification_proof.py"


def unsafe_replace(value: object, **changes: object) -> object:
    clone = object.__new__(type(value))
    for field in fields(value):
        object.__setattr__(
            clone,
            field.name,
            changes.get(field.name, getattr(value, field.name)),
        )
    return clone


class SliceIVCertificationAlphaTests(unittest.TestCase):
    def test_certifier_accepts_exactly_one_wp29_report(self) -> None:
        parameters = tuple(inspect.signature(certify_slice_iv).parameters)

        self.assertEqual(parameters, ("report",))
        with self.assertRaises(TypeError):
            certify_slice_iv({})

    def test_certified_wp29_report_closes_slice_iv(self) -> None:
        artifacts = build_wp30_artifacts()
        expression_certification = artifacts["expression_certification"]
        slice_certification = artifacts["slice_iv_certification"]
        expression_bytes = canonical_expression_certification_report_bytes(
            expression_certification
        )

        self.assertIsInstance(
            slice_certification,
            SliceIVCertificationReport,
        )
        self.assertEqual(
            slice_certification.schema_version,
            SLICE_IV_CERTIFICATION_SCHEMA_VERSION,
        )
        self.assertEqual(
            slice_certification.certification_version,
            SLICE_IV_CERTIFICATION_VERSION,
        )
        self.assertEqual(
            slice_certification.expression_certification_id,
            expression_certification.certification_id,
        )
        self.assertEqual(
            slice_certification.expression_certification_integrity,
            expression_certification.certification_integrity,
        )
        self.assertEqual(
            slice_certification.provenance_ref,
            f"sha256:{sha256(expression_bytes).hexdigest()}",
        )
        self.assertEqual(slice_certification.decision, CERTIFIED)
        self.assertEqual(slice_certification.responsibility, RESPONSIBILITY)
        self.assertEqual(
            slice_certification.stop,
            STOP_AT_SLICE_IV_CERTIFIED,
        )

    def test_report_is_immutable_strict_and_replayable(self) -> None:
        first = build_wp30_artifacts()["slice_iv_certification"]
        second = build_wp30_artifacts()["slice_iv_certification"]
        payload = slice_iv_certification_report_as_dict(first)

        with self.assertRaises(FrozenInstanceError):
            first.decision = "failed"
        self.assertEqual(
            slice_iv_certification_report_from_dict(payload),
            first,
        )
        with self.assertRaises(ValueError):
            slice_iv_certification_report_from_dict(
                {**payload, "expression_payload": {}}
            )
        self.assertEqual(
            canonical_slice_iv_certification_report_bytes(first),
            canonical_slice_iv_certification_report_bytes(second),
        )

    def test_uncertified_wp29_report_produces_no_slice_certification(
        self,
    ) -> None:
        report = build_wp30_artifacts()["expression_certification"]
        uncertified = unsafe_replace(report, decision="accepted")

        with self.assertRaises(ValueError):
            certify_slice_iv(uncertified)

    def test_malformed_wp29_identity_or_stop_is_rejected(self) -> None:
        report = build_wp30_artifacts()["expression_certification"]
        malformed_id = unsafe_replace(
            report,
            certification_id="expression-certification-" + "0" * 24,
        )
        malformed_stop = unsafe_replace(
            report,
            stop="at_slice_iv_certified",
        )

        with self.assertRaises(ValueError):
            certify_slice_iv(malformed_id)
        with self.assertRaises(ValueError):
            certify_slice_iv(malformed_stop)

    def test_slice_certification_tampering_is_rejected(self) -> None:
        report = build_wp30_artifacts()["slice_iv_certification"]
        payload = slice_iv_certification_report_as_dict(report)

        with self.assertRaises(ValueError):
            slice_iv_certification_report_from_dict(
                {
                    **payload,
                    "certification_id": (
                        "slice-iv-certification-" + "0" * 24
                    ),
                }
            )
        with self.assertRaises(ValueError):
            slice_iv_certification_report_from_dict(
                {**payload, "certification_integrity": "0" * 64}
            )

    def test_certification_does_not_modify_wp29_report(self) -> None:
        report = build_wp30_artifacts()["expression_certification"]
        before = canonical_expression_certification_report_bytes(report)

        certify_slice_iv(report)
        after = canonical_expression_certification_report_bytes(report)

        self.assertEqual(before, after)

    def test_report_contains_no_payload_language_or_downstream_state(
        self,
    ) -> None:
        report = build_wp30_artifacts()["slice_iv_certification"]

        self.assertFalse(
            set(asdict(report))
            & {
                "expression_contract",
                "expression_artifact",
                "expression_conformance",
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
            }
        )

    def test_module_reads_only_wp29_and_calls_no_other_stage(self) -> None:
        path = ROOT / "src" / "orion" / "slice_iv_certification_alpha.py"
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
            "certify_expression",
            "invoke_lyra",
            "invoke_sirius",
            "execute_runtime",
        }

        self.assertEqual(
            orion_modules,
            {"orion.expression_certification_alpha"},
        )
        self.assertFalse(prohibited_calls & called_names)

    def test_frozen_wp26_through_wp29_sources_are_unchanged(self) -> None:
        self.assertEqual(
            tuple(item[0] for item in FROZEN_SLICE_IV_SOURCES),
            ("WP26", "WP27", "WP28", "WP29"),
        )
        for work_package, source_path, expected_sha256 in (
            FROZEN_SLICE_IV_SOURCES
        ):
            with self.subTest(work_package=work_package):
                self.assertEqual(
                    sha256((ROOT / source_path).read_bytes()).hexdigest(),
                    expected_sha256,
                )

    def test_canonical_proof_certifies_slice_and_stops(self) -> None:
        proof, successful = build_wp30_proof()

        self.assertTrue(successful)
        self.assertTrue(proof["frozen_sources_verified"])
        self.assertEqual(
            proof["slice_iv_certification"]["decision"],
            CERTIFIED,
        )
        self.assertTrue(proof["input_unchanged"])
        self.assertTrue(proof["certification_replay_byte_identical"])
        self.assertTrue(proof["wp29_references_verified"])
        self.assertTrue(proof["provenance_preserved"])
        self.assertFalse(any(proof["downstream_execution"].values()))
        self.assertEqual(proof["stop"], STOP_AT_SLICE_IV_CERTIFIED)

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
