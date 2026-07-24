"""Focused tests for observational WP28 Expression Conformance."""

from __future__ import annotations

import ast
from dataclasses import FrozenInstanceError, asdict, fields
from hashlib import sha256
import inspect
from pathlib import Path
import subprocess
import sys
import unittest

from orion.expression_conformance_alpha import (
    ACCEPTED,
    REJECTED,
    RESPONSIBILITY,
    STOP_AFTER_EXPRESSION_CONFORMANCE,
    ExpressionConformanceReport,
    canonical_expression_conformance_report_bytes,
    expression_conformance_report_as_dict,
    expression_conformance_report_from_dict,
    validate_expression_conformance,
)
from orion.expression_construction_alpha import (
    canonical_expression_artifact_bytes,
)
from orion.expression_contract_alpha import (
    canonical_expression_contract_bytes,
)


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from slice_iv_expression_conformance_proof import (  # noqa: E402
    WP26_SHA256,
    WP26_SOURCE,
    WP27_SHA256,
    WP27_SOURCE,
    build_wp28_artifacts,
    build_wp28_proof,
)


PROOF = ROOT / "scripts" / "slice_iv_expression_conformance_proof.py"


def unsafe_replace(value: object, **changes: object) -> object:
    clone = object.__new__(type(value))
    for field in fields(value):
        object.__setattr__(
            clone,
            field.name,
            changes.get(field.name, getattr(value, field.name)),
        )
    return clone


class ExpressionConformanceAlphaTests(unittest.TestCase):
    def test_validator_accepts_exactly_contract_and_artifact(self) -> None:
        parameters = tuple(
            inspect.signature(validate_expression_conformance).parameters
        )

        self.assertEqual(parameters, ("contract", "artifact"))

    def test_exact_expression_is_accepted(self) -> None:
        artifacts = build_wp28_artifacts()
        report = artifacts["expression_conformance"]
        contract = artifacts["expression_contract"]
        artifact = artifacts["expression_artifact"]

        self.assertIsInstance(report, ExpressionConformanceReport)
        self.assertTrue(report.valid)
        self.assertEqual(report.decision, ACCEPTED)
        self.assertEqual(report.errors, ())
        self.assertEqual(report.expression_contract_id, contract.contract_id)
        self.assertEqual(
            report.expression_contract_integrity,
            contract.contract_integrity,
        )
        self.assertEqual(report.expression_id, artifact.expression_id)
        self.assertEqual(
            report.expression_integrity,
            artifact.expression_integrity,
        )
        self.assertEqual(
            report.accepted_expression_ref,
            report.expression_ref,
        )
        self.assertTrue(report.inputs_unchanged)
        self.assertEqual(report.responsibility, RESPONSIBILITY)
        self.assertEqual(
            report.stop,
            STOP_AFTER_EXPRESSION_CONFORMANCE,
        )

    def test_report_is_immutable_strict_and_replayable(self) -> None:
        first = build_wp28_artifacts()["expression_conformance"]
        second = build_wp28_artifacts()["expression_conformance"]
        payload = expression_conformance_report_as_dict(first)

        with self.assertRaises(FrozenInstanceError):
            first.valid = False
        self.assertEqual(
            expression_conformance_report_from_dict(payload),
            first,
        )
        with self.assertRaises(ValueError):
            expression_conformance_report_from_dict(
                {**payload, "certified": True}
            )
        self.assertEqual(
            canonical_expression_conformance_report_bytes(first),
            canonical_expression_conformance_report_bytes(second),
        )

    def test_modified_contract_reference_is_rejected(self) -> None:
        artifacts = build_wp28_artifacts()
        modified = unsafe_replace(
            artifacts["expression_artifact"],
            expression_contract_ref="sha256:" + "0" * 64,
        )

        report = validate_expression_conformance(
            artifacts["expression_contract"],
            modified,
        )

        self.assertFalse(report.valid)
        self.assertEqual(report.decision, REJECTED)
        self.assertIsNone(report.accepted_expression_ref)
        self.assertIn(
            "Expression Artifact does not name the exact WP26 Contract",
            report.errors,
        )

    def test_changed_lineage_or_provenance_is_rejected(self) -> None:
        artifacts = build_wp28_artifacts()
        changed_lineage = unsafe_replace(
            artifacts["expression_artifact"],
            orientation_map_ref="sha256:" + "0" * 64,
        )
        changed_provenance = unsafe_replace(
            artifacts["expression_artifact"],
            provenance_ref="sha256:" + "0" * 64,
        )

        lineage_report = validate_expression_conformance(
            artifacts["expression_contract"],
            changed_lineage,
        )
        provenance_report = validate_expression_conformance(
            artifacts["expression_contract"],
            changed_provenance,
        )

        self.assertFalse(lineage_report.valid)
        self.assertIn(
            "Expression Artifact changed certified Slice III references",
            lineage_report.errors,
        )
        self.assertFalse(provenance_report.valid)
        self.assertIn(
            "Expression Artifact changed certified provenance",
            provenance_report.errors,
        )

    def test_changed_scope_lossiness_or_exclusions_are_rejected(self) -> None:
        artifacts = build_wp28_artifacts()
        artifact = artifacts["expression_artifact"]
        variants = (
            unsafe_replace(
                artifact,
                communicative_scope=("canonical_order",),
            ),
            unsafe_replace(
                artifact,
                declared_lossiness=("semantic_meaning",),
            ),
            unsafe_replace(
                artifact,
                declared_exclusions=("actions",),
            ),
        )

        for variant in variants:
            with self.subTest(field=variant):
                report = validate_expression_conformance(
                    artifacts["expression_contract"],
                    variant,
                )
                self.assertFalse(report.valid)
                self.assertIn(
                    "Expression scope, lossiness, or exclusions changed",
                    report.errors,
                )

    def test_duplicate_declarations_or_changed_state_are_rejected(self) -> None:
        artifacts = build_wp28_artifacts()
        artifact = artifacts["expression_artifact"]
        duplicate = unsafe_replace(
            artifact,
            declared_exclusions=("actions", "actions"),
        )
        changed_state = unsafe_replace(
            artifact,
            externally_conformant=True,
        )

        duplicate_report = validate_expression_conformance(
            artifacts["expression_contract"],
            duplicate,
        )
        state_report = validate_expression_conformance(
            artifacts["expression_contract"],
            changed_state,
        )

        self.assertFalse(duplicate_report.valid)
        self.assertIn(
            "Expression Artifact ordering or declarations are not canonical",
            duplicate_report.errors,
        )
        self.assertFalse(state_report.valid)
        self.assertIn(
            "Expression Artifact differs from frozen WP27 candidate state",
            state_report.errors,
        )

    def test_wrong_types_and_unexpected_payload_are_rejected(self) -> None:
        artifacts = build_wp28_artifacts()
        payload = {
            **asdict(artifacts["expression_artifact"]),
            "generated_language": "not permitted",
        }

        wrong_contract = validate_expression_conformance(
            {},
            artifacts["expression_artifact"],
        )
        payload_report = validate_expression_conformance(
            artifacts["expression_contract"],
            payload,
        )

        self.assertFalse(wrong_contract.valid)
        self.assertEqual(wrong_contract.decision, REJECTED)
        self.assertFalse(payload_report.valid)
        self.assertEqual(payload_report.decision, REJECTED)

    def test_observation_does_not_modify_inputs(self) -> None:
        artifacts = build_wp28_artifacts()
        contract = artifacts["expression_contract"]
        artifact = artifacts["expression_artifact"]
        before = (
            canonical_expression_contract_bytes(contract),
            canonical_expression_artifact_bytes(artifact),
        )

        validate_expression_conformance(contract, artifact)
        after = (
            canonical_expression_contract_bytes(contract),
            canonical_expression_artifact_bytes(artifact),
        )

        self.assertEqual(before, after)

    def test_report_contains_no_expression_content_or_certification(self) -> None:
        report = build_wp28_artifacts()["expression_conformance"]

        self.assertFalse(
            set(asdict(report))
            & {
                "text",
                "generated_language",
                "prompt",
                "provider",
                "html",
                "markdown",
                "visualization",
                "interpretation",
                "reasoning",
                "recommendation",
                "action",
                "runtime",
                "gateway",
                "presentation",
                "certified",
                "certification",
            }
        )

    def test_validator_calls_no_constructor_or_downstream_capability(self) -> None:
        path = ROOT / "src" / "orion" / "expression_conformance_alpha.py"
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
            "repair_expression",
            "normalize_expression",
            "certify_expression",
            "generate_language",
            "invoke_lyra",
            "invoke_sirius",
            "execute_runtime",
        }

        self.assertEqual(
            orion_modules,
            {
                "orion.expression_contract_alpha",
                "orion.expression_construction_alpha",
            },
        )
        self.assertFalse(prohibited_calls & called_names)

    def test_frozen_wp26_and_wp27_sources_are_unchanged(self) -> None:
        self.assertEqual(
            sha256(WP26_SOURCE.read_bytes()).hexdigest(),
            WP26_SHA256,
        )
        self.assertEqual(
            sha256(WP27_SOURCE.read_bytes()).hexdigest(),
            WP27_SHA256,
        )

    def test_canonical_proof_observes_and_stops(self) -> None:
        proof, successful = build_wp28_proof()

        self.assertTrue(successful)
        self.assertTrue(proof["frozen_sources_verified"])
        self.assertTrue(proof["conformance_report"]["valid"])
        self.assertEqual(
            proof["conformance_report"]["decision"],
            ACCEPTED,
        )
        self.assertTrue(proof["inputs_unchanged"])
        self.assertTrue(proof["report_replay_byte_identical"])
        self.assertTrue(proof["authority_references_verified"])
        self.assertTrue(proof["provenance_verified"])
        self.assertFalse(any(proof["downstream_execution"].values()))
        self.assertEqual(
            proof["stop"],
            STOP_AFTER_EXPRESSION_CONFORMANCE,
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
