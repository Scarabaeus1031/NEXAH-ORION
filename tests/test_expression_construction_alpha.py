"""Focused tests for deterministic WP27 Expression Construction."""

from __future__ import annotations

import ast
from dataclasses import FrozenInstanceError, asdict, fields
from hashlib import sha256
import inspect
from pathlib import Path
import subprocess
import sys
import unittest

from orion.expression_construction_alpha import (
    CONSTRUCTION_STATE,
    EXPRESSION_ARTIFACT_SCHEMA_VERSION,
    RESPONSIBILITY,
    SERIALIZATION_VERSION,
    STOP_AFTER_EXPRESSION_CONSTRUCTION,
    ExpressionArtifact,
    canonical_expression_artifact_bytes,
    construct_expression,
    expression_artifact_as_dict,
    expression_artifact_from_dict,
)
from orion.expression_contract_alpha import (
    canonical_expression_contract_bytes,
)


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from slice_iv_expression_construction_proof import (  # noqa: E402
    WP26_SHA256,
    WP26_SOURCE,
    build_wp27_artifacts,
    build_wp27_proof,
)


PROOF = ROOT / "scripts" / "slice_iv_expression_construction_proof.py"


def unsafe_replace(value: object, **changes: object) -> object:
    clone = object.__new__(type(value))
    for field in fields(value):
        object.__setattr__(
            clone,
            field.name,
            changes.get(field.name, getattr(value, field.name)),
        )
    return clone


class ExpressionConstructionAlphaTests(unittest.TestCase):
    def test_construction_accepts_only_one_expression_contract(self) -> None:
        parameters = tuple(inspect.signature(construct_expression).parameters)

        self.assertEqual(parameters, ("contract",))
        with self.assertRaises(TypeError):
            construct_expression({})

    def test_artifact_preserves_exact_contract_authority(self) -> None:
        artifacts = build_wp27_artifacts()
        contract = artifacts["expression_contract"]
        artifact = artifacts["expression_artifact"]

        self.assertIsInstance(artifact, ExpressionArtifact)
        self.assertEqual(
            artifact.schema_version,
            EXPRESSION_ARTIFACT_SCHEMA_VERSION,
        )
        self.assertEqual(artifact.expression_contract_id, contract.contract_id)
        self.assertEqual(
            artifact.expression_contract_integrity,
            contract.contract_integrity,
        )
        self.assertEqual(
            artifact.expression_contract_schema_version,
            contract.schema_version,
        )
        self.assertEqual(
            artifact.expression_contract_version,
            contract.contract_version,
        )
        self.assertEqual(
            artifact.expression_contract_status,
            contract.status,
        )
        self.assertEqual(
            artifact.communicative_scope,
            contract.communicative_scope,
        )
        self.assertEqual(
            artifact.declared_lossiness,
            contract.declared_lossiness,
        )
        self.assertEqual(
            artifact.declared_exclusions,
            contract.declared_exclusions,
        )
        self.assertEqual(artifact.provenance_ref, contract.provenance_ref)
        self.assertEqual(artifact.canonical_order, 0)
        self.assertEqual(artifact.serialization_version, SERIALIZATION_VERSION)
        self.assertEqual(artifact.construction_state, CONSTRUCTION_STATE)
        self.assertEqual(artifact.responsibility, RESPONSIBILITY)
        self.assertFalse(artifact.externally_conformant)
        self.assertEqual(
            artifact.stop,
            STOP_AFTER_EXPRESSION_CONSTRUCTION,
        )

    def test_artifact_is_immutable_and_schema_strict(self) -> None:
        artifact = build_wp27_artifacts()["expression_artifact"]
        payload = expression_artifact_as_dict(artifact)

        with self.assertRaises(FrozenInstanceError):
            artifact.construction_state = "accepted"
        self.assertEqual(expression_artifact_from_dict(payload), artifact)
        with self.assertRaises(ValueError):
            expression_artifact_from_dict({**payload, "rendered_text": ""})

    def test_identity_and_serialization_replay_are_byte_identical(self) -> None:
        first = build_wp27_artifacts()["expression_artifact"]
        second = build_wp27_artifacts()["expression_artifact"]

        self.assertEqual(first, second)
        self.assertEqual(
            canonical_expression_artifact_bytes(first),
            canonical_expression_artifact_bytes(second),
        )

    def test_identity_integrity_or_state_tampering_is_rejected(self) -> None:
        artifact = build_wp27_artifacts()["expression_artifact"]
        payload = expression_artifact_as_dict(artifact)

        with self.assertRaises(ValueError):
            expression_artifact_from_dict(
                {**payload, "expression_id": "expression-" + "0" * 24}
            )
        with self.assertRaises(ValueError):
            expression_artifact_from_dict(
                {**payload, "expression_integrity": "0" * 64}
            )
        with self.assertRaises(ValueError):
            expression_artifact_from_dict(
                {**payload, "externally_conformant": True}
            )

    def test_invalid_or_mutated_contract_is_rejected(self) -> None:
        artifacts = build_wp27_artifacts()
        invalid = unsafe_replace(
            artifacts["expression_contract"],
            stop="after_expression_construction",
        )

        with self.assertRaises(ValueError):
            construct_expression(invalid)

    def test_construction_does_not_modify_contract(self) -> None:
        artifacts = build_wp27_artifacts()
        contract = artifacts["expression_contract"]
        before = canonical_expression_contract_bytes(contract)

        construct_expression(contract)
        after = canonical_expression_contract_bytes(contract)

        self.assertEqual(before, after)

    def test_artifact_contains_no_language_presentation_or_semantics(self) -> None:
        keys = set(asdict(build_wp27_artifacts()["expression_artifact"]))

        self.assertFalse(
            keys
            & {
                "text",
                "rendered_text",
                "generated_language",
                "prompt",
                "provider",
                "model",
                "template",
                "html",
                "markdown",
                "ui",
                "visualization",
                "graphics",
                "report",
                "interpretation",
                "meaning",
                "reasoning",
                "recommendation",
                "action",
                "runtime",
                "gateway",
                "presentation",
                "relations",
                "orientation",
            }
        )

    def test_module_reopens_no_upstream_or_downstream_artifact(self) -> None:
        path = ROOT / "src" / "orion" / "expression_construction_alpha.py"
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
            "construct_orientation_map",
            "validate_orientation_map_conformance",
            "certify_slice_iii",
            "validate_expression_conformance",
            "certify_expression",
            "generate_language",
            "invoke_lyra",
            "invoke_sirius",
            "execute_runtime",
        }

        self.assertEqual(
            orion_modules,
            {"orion.expression_contract_alpha"},
        )
        self.assertFalse(prohibited_calls & called_names)

    def test_frozen_wp26_contract_source_is_unchanged(self) -> None:
        self.assertEqual(
            sha256(WP26_SOURCE.read_bytes()).hexdigest(),
            WP26_SHA256,
        )

    def test_canonical_proof_constructs_and_stops(self) -> None:
        proof, successful = build_wp27_proof()

        self.assertTrue(successful)
        self.assertTrue(proof["frozen_wp26"]["verified"])
        self.assertTrue(
            all(proof["construction_validation"].values())
        )
        self.assertTrue(proof["contract_unchanged"])
        self.assertTrue(proof["artifact_replay_byte_identical"])
        self.assertTrue(proof["provenance_preserved"])
        self.assertFalse(any(proof["downstream_execution"].values()))
        self.assertEqual(
            proof["stop"],
            STOP_AFTER_EXPRESSION_CONSTRUCTION,
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
