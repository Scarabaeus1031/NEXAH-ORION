"""Focused tests for the immutable WP26 Expression Contract."""

from __future__ import annotations

import ast
from dataclasses import FrozenInstanceError, asdict, fields
from hashlib import sha256
from pathlib import Path
import subprocess
import sys
import unittest

from orion.expression_contract_alpha import (
    EXPRESSION_CONTRACT_SCHEMA_VERSION,
    EXPRESSION_CONTRACT_VERSION,
    PERMITTED_COMMUNICATIVE_SCOPE,
    RESPONSIBILITY,
    SERIALIZATION_VERSION,
    STATUS,
    STOP_AT_EXPRESSION_CONTRACT,
    ExpressionContract,
    canonical_expression_contract_bytes,
    create_expression_contract,
    expression_contract_as_dict,
    expression_contract_from_dict,
    validate_expression_contract,
)
from orion.orientation_map_conformance_alpha import (
    canonical_orientation_map_conformance_report_bytes,
)
from orion.orientation_map_construction_alpha import (
    canonical_constructed_orientation_map_bytes,
)
from orion.orientation_map_object_alpha import (
    canonical_orientation_map_object_bytes,
)
from orion.slice_iii_certification_alpha import (
    FROZEN_SLICE_III_CONTRACTS,
    canonical_slice_iii_certification_report_bytes,
)


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from slice_iv_expression_contract_proof import (  # noqa: E402
    DECLARED_EXCLUSIONS,
    DECLARED_LOSSINESS,
    WP25_SHA256,
    WP25_SOURCE,
    build_wp26_artifacts,
    build_wp26_proof,
)


PROOF = ROOT / "scripts" / "slice_iv_expression_contract_proof.py"


def unsafe_replace(value: object, **changes: object) -> object:
    clone = object.__new__(type(value))
    for field in fields(value):
        object.__setattr__(
            clone,
            field.name,
            changes.get(field.name, getattr(value, field.name)),
        )
    return clone


def create(
    artifacts: dict[str, object],
    *,
    certification=None,
    conformance=None,
    scope=None,
) -> ExpressionContract:
    return create_expression_contract(
        (
            artifacts["slice_iii_certification"]
            if certification is None
            else certification
        ),
        (
            artifacts["orientation_map_conformance"]
            if conformance is None
            else conformance
        ),
        artifacts["orientation_map_object"],
        artifacts["constructed_orientation_map"],
        communicative_scope=(
            artifacts["expression_contract"].communicative_scope
            if scope is None
            else scope
        ),
        declared_lossiness=DECLARED_LOSSINESS,
        declared_exclusions=DECLARED_EXCLUSIONS,
    )


class ExpressionContractAlphaTests(unittest.TestCase):
    def test_contract_binds_exact_certified_map_lineage(self) -> None:
        artifacts = build_wp26_artifacts()
        contract = artifacts["expression_contract"]
        certification = artifacts["slice_iii_certification"]
        conformance = artifacts["orientation_map_conformance"]
        orientation_map = artifacts["orientation_map_object"]
        constructed = artifacts["constructed_orientation_map"]

        self.assertIsInstance(contract, ExpressionContract)
        self.assertEqual(
            contract.schema_version,
            EXPRESSION_CONTRACT_SCHEMA_VERSION,
        )
        self.assertEqual(
            contract.contract_version,
            EXPRESSION_CONTRACT_VERSION,
        )
        self.assertEqual(
            contract.slice_iii_certification_id,
            certification.certification_id,
        )
        self.assertEqual(
            contract.orientation_map_conformance_id,
            conformance.report_id,
        )
        self.assertEqual(
            contract.orientation_map_id,
            orientation_map.orientation_map_id,
        )
        self.assertEqual(
            contract.orientation_map_construction_id,
            constructed.construction_id,
        )
        self.assertEqual(
            contract.provenance_ref,
            contract.slice_iii_certification_ref,
        )
        self.assertEqual(contract.serialization_version, SERIALIZATION_VERSION)
        self.assertEqual(contract.status, STATUS)
        self.assertEqual(contract.responsibility, RESPONSIBILITY)
        self.assertEqual(contract.stop, STOP_AT_EXPRESSION_CONTRACT)

    def test_contract_is_immutable_and_schema_strict(self) -> None:
        contract = build_wp26_artifacts()["expression_contract"]
        payload = expression_contract_as_dict(contract)

        with self.assertRaises(FrozenInstanceError):
            contract.status = "constructed"
        self.assertEqual(expression_contract_from_dict(payload), contract)
        with self.assertRaises(ValueError):
            expression_contract_from_dict({**payload, "rendered_text": ""})

    def test_identity_and_serialization_replay_are_byte_identical(self) -> None:
        first = build_wp26_artifacts()["expression_contract"]
        second = build_wp26_artifacts()["expression_contract"]

        self.assertEqual(first, second)
        self.assertEqual(
            canonical_expression_contract_bytes(first),
            canonical_expression_contract_bytes(second),
        )

    def test_scope_and_declarations_must_be_canonical(self) -> None:
        artifacts = build_wp26_artifacts()

        with self.assertRaises(ValueError):
            create(artifacts, scope=("provenance", "canonical_order"))
        with self.assertRaises(ValueError):
            create(artifacts, scope=("canonical_order", "canonical_order"))
        with self.assertRaises(ValueError):
            create(artifacts, scope=("semantic_meaning",))
        self.assertTrue(
            set(artifacts["expression_contract"].communicative_scope)
            <= set(PERMITTED_COMMUNICATIVE_SCOPE)
        )

    def test_identity_or_integrity_tampering_is_rejected(self) -> None:
        contract = build_wp26_artifacts()["expression_contract"]
        payload = expression_contract_as_dict(contract)

        with self.assertRaises(ValueError):
            expression_contract_from_dict(
                {
                    **payload,
                    "contract_id": "expression-contract-" + "0" * 24,
                }
            )
        with self.assertRaises(ValueError):
            expression_contract_from_dict(
                {**payload, "contract_integrity": "0" * 64}
            )

    def test_uncertified_slice_iii_is_rejected(self) -> None:
        artifacts = build_wp26_artifacts()
        rejected = unsafe_replace(
            artifacts["slice_iii_certification"],
            certified=False,
            status="failed",
            errors=("not certified",),
        )

        with self.assertRaises(ValueError):
            create(artifacts, certification=rejected)

    def test_unaccepted_or_inconsistent_map_lineage_is_rejected(self) -> None:
        artifacts = build_wp26_artifacts()
        rejected = unsafe_replace(
            artifacts["orientation_map_conformance"],
            valid=False,
            decision="rejected",
            errors=("not accepted",),
            accepted_orientation_map_ref=None,
            accepted_construction_ref=None,
        )
        inconsistent = unsafe_replace(
            artifacts["orientation_map_conformance"],
            orientation_map_ref="sha256:" + "0" * 64,
        )

        with self.assertRaises(ValueError):
            create(artifacts, conformance=rejected)
        with self.assertRaises(ValueError):
            create(artifacts, conformance=inconsistent)

    def test_validation_is_observational_and_exact(self) -> None:
        artifacts = build_wp26_artifacts()
        contract = artifacts["expression_contract"]
        validation = validate_expression_contract(
            artifacts["slice_iii_certification"],
            artifacts["orientation_map_conformance"],
            artifacts["orientation_map_object"],
            artifacts["constructed_orientation_map"],
            contract,
        )

        self.assertTrue(validation.valid)
        self.assertEqual(validation.errors, ())
        self.assertEqual(validation.stop, STOP_AT_EXPRESSION_CONTRACT)

    def test_creation_does_not_modify_inputs(self) -> None:
        artifacts = build_wp26_artifacts()
        before = (
            canonical_slice_iii_certification_report_bytes(
                artifacts["slice_iii_certification"]
            ),
            canonical_orientation_map_conformance_report_bytes(
                artifacts["orientation_map_conformance"]
            ),
            canonical_orientation_map_object_bytes(
                artifacts["orientation_map_object"]
            ),
            canonical_constructed_orientation_map_bytes(
                artifacts["constructed_orientation_map"]
            ),
        )

        create(artifacts)
        after = (
            canonical_slice_iii_certification_report_bytes(
                artifacts["slice_iii_certification"]
            ),
            canonical_orientation_map_conformance_report_bytes(
                artifacts["orientation_map_conformance"]
            ),
            canonical_orientation_map_object_bytes(
                artifacts["orientation_map_object"]
            ),
            canonical_constructed_orientation_map_bytes(
                artifacts["constructed_orientation_map"]
            ),
        )

        self.assertEqual(before, after)

    def test_contract_contains_no_expression_or_execution_content(self) -> None:
        keys = set(asdict(build_wp26_artifacts()["expression_contract"]))

        self.assertFalse(
            keys
            & {
                "rendered_text",
                "generated_language",
                "prompt",
                "provider",
                "model",
                "template",
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
                "expression",
                "conformance",
                "certification",
            }
        )

    def test_module_imports_or_calls_no_downstream_capability(self) -> None:
        path = ROOT / "src" / "orion" / "expression_contract_alpha.py"
        tree = ast.parse(path.read_text(encoding="utf-8"))
        imported_modules = {
            node.module
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and node.module
        }
        called_names = {
            node.func.id
            for node in ast.walk(tree)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
        }
        prohibited_modules = (
            "lyra",
            "sirius",
            "gateway",
            "orientation_runtime",
        )
        prohibited_calls = {
            "construct_expression",
            "render_expression",
            "format_expression",
            "validate_expression_conformance",
            "certify_expression",
            "invoke_lyra",
            "invoke_sirius",
            "execute_runtime",
        }

        self.assertFalse(
            any(
                fragment in module
                for module in imported_modules
                for fragment in prohibited_modules
            )
        )
        self.assertFalse(prohibited_calls & called_names)

    def test_frozen_slice_iii_sources_are_unchanged(self) -> None:
        records = tuple(
            (
                contract.work_package,
                ROOT / contract.source_path,
                contract.sha256,
            )
            for contract in FROZEN_SLICE_III_CONTRACTS
        ) + (("WP25", WP25_SOURCE, WP25_SHA256),)
        for work_package, path, expected in records:
            with self.subTest(work_package=work_package):
                self.assertEqual(sha256(path.read_bytes()).hexdigest(), expected)

    def test_canonical_proof_validates_contract_and_stops(self) -> None:
        proof, successful = build_wp26_proof()

        self.assertTrue(successful)
        self.assertTrue(proof["frozen_slice_iii_verified"])
        self.assertTrue(proof["validation"]["valid"])
        self.assertTrue(proof["inputs_unchanged"])
        self.assertTrue(proof["contract_replay_byte_identical"])
        self.assertTrue(proof["provenance_preserved"])
        self.assertFalse(any(proof["downstream_execution"].values()))
        self.assertEqual(proof["stop"], STOP_AT_EXPRESSION_CONTRACT)

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
