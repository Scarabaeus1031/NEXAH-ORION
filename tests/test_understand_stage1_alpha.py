"""Conformance tests for semantically free UNDERSTAND Stage 1 binding."""

from __future__ import annotations

import ast
from copy import deepcopy
from dataclasses import FrozenInstanceError, asdict, replace
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

from orion.public_contracts import IntegrityReference
from orion.public_contracts.fixtures import VALID_REQUEST
from orion.readiness_alpha import prove_runtime_readiness
from orion.understand_stage1_alpha import (
    UnderstandStage1BindingDiagnostic,
    bind_understand_stage1,
)


ROOT = Path(__file__).resolve().parent.parent
PROOF = ROOT / "scripts" / "understand_stage1_alpha_proof.py"
NEXAHEDRON_ROOT = Path(
    os.environ.get("NEXAHEDRON_ROOT", ROOT.parent / "NEXAHEDRON")
)
HAS_NEXAHEDRON_ALPHA = (
    NEXAHEDRON_ROOT / "scripts" / "representation-referenced-request.mjs"
).is_file()
CONTENT_SHA256 = "a" * 64
REPRESENTATION_SHA256 = "b" * 64


class _ContentGuard(dict[str, object]):
    def get(self, key: str, default: object = None) -> object:
        if key == "content":
            raise AssertionError("Stage 1 attempted to read Representation content")
        return super().get(key, default)


def stage1_input() -> tuple[object, object, dict[str, object]]:
    representation_ref = (
        "representation-paper-01"
        f"@sha256:{REPRESENTATION_SHA256}"
    )
    orientation_object = replace(
        VALID_REQUEST.orientation_objects[0],
        representation_refs=(representation_ref,),
        integrity_ref=IntegrityReference(
            "sha256",
            CONTENT_SHA256,
            "whole",
            True,
        ),
    )
    request = replace(
        VALID_REQUEST,
        orientation_objects=(orientation_object,),
    )
    readiness = prove_runtime_readiness(request)
    representation = {
        "representation_id": "representation-paper-01",
        "representation_version": f"sha256:{REPRESENTATION_SHA256}",
        "representation_sha256": REPRESENTATION_SHA256,
        "orientation_object_id": orientation_object.object_id,
        "orientation_object_version": orientation_object.object_version,
        "source": {
            "owner": orientation_object.source_owner,
            "source_ref": orientation_object.source_ref,
            "revision": orientation_object.source_revision,
        },
        "payload": _ContentGuard(
            {
                "content": "must remain unread",
                "content_sha256": CONTENT_SHA256,
            }
        ),
    }
    return request, readiness, representation


def execute_proof() -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(PROOF)],
        cwd=ROOT,
        env={**os.environ, "PYTHONPATH": str(ROOT / "src")},
        check=False,
        capture_output=True,
        text=True,
    )


class UnderstandStage1AlphaTests(unittest.TestCase):
    def test_stage1_binds_only_exact_declared_identity(self) -> None:
        request, readiness, representation = stage1_input()

        diagnostic = bind_understand_stage1(  # type: ignore[arg-type]
            request,
            readiness,
            representation,
        )

        self.assertEqual(diagnostic.stage_id, "understand/1")
        self.assertEqual(diagnostic.completion_state, "completed")
        self.assertEqual(diagnostic.stop, "before_understand/2")
        self.assertEqual(
            diagnostic.operator_id,
            "orion.orientation-operator/understand",
        )
        self.assertEqual(diagnostic.operator_version, "1.0")
        self.assertEqual(
            diagnostic.representation_version,
            f"sha256:{REPRESENTATION_SHA256}",
        )
        self.assertEqual(diagnostic.integrity_value, CONTENT_SHA256)

    def test_binding_diagnostic_is_immutable_and_internal(self) -> None:
        import orion
        import orion.understand_stage1_alpha as stage1_alpha

        request, readiness, representation = stage1_input()
        diagnostic = bind_understand_stage1(  # type: ignore[arg-type]
            request,
            readiness,
            representation,
        )

        self.assertIsInstance(diagnostic, UnderstandStage1BindingDiagnostic)
        self.assertEqual(stage1_alpha.__all__, ())
        self.assertNotIn("UnderstandStage1BindingDiagnostic", orion.__all__)
        self.assertFalse(hasattr(diagnostic, "schema_version"))
        self.assertEqual(
            set(asdict(diagnostic)),
            {
                "diagnostic_version",
                "request_id",
                "request_version",
                "operator_id",
                "operator_version",
                "orientation_object_id",
                "orientation_object_version",
                "representation_id",
                "representation_version",
                "source_owner",
                "source_ref",
                "source_revision",
                "integrity_method",
                "integrity_value",
                "integrity_coverage",
                "integrity_verified",
                "stage_id",
                "completion_state",
                "stop",
            },
        )
        with self.assertRaises(FrozenInstanceError):
            diagnostic.stage_id = "understand/2"  # type: ignore[misc]

    def test_content_is_never_read(self) -> None:
        request, readiness, representation = stage1_input()

        diagnostic = bind_understand_stage1(  # type: ignore[arg-type]
            request,
            readiness,
            representation,
        )

        self.assertEqual(diagnostic.stop, "before_understand/2")

    def test_every_identity_mismatch_fails_without_repair(self) -> None:
        request, readiness, representation = stage1_input()
        mutations = {
            "representation reference": lambda value: value.update(
                representation_id="Representation-paper-01"
            ),
            "representation version": lambda value: value.update(
                representation_version=f"sha256:{'c' * 64}"
            ),
            "object identity": lambda value: value.update(
                orientation_object_id="similar-object"
            ),
            "source identity": lambda value: value["source"].update(  # type: ignore[union-attr]
                source_ref="similar-source"
            ),
            "source revision": lambda value: value["source"].update(  # type: ignore[union-attr]
                revision="nearby-revision"
            ),
            "integrity": lambda value: value["payload"].update(  # type: ignore[union-attr]
                content_sha256="d" * 64
            ),
        }

        for name, mutate in mutations.items():
            with self.subTest(name=name):
                changed = deepcopy(representation)
                mutate(changed)
                with self.assertRaises(ValueError):
                    bind_understand_stage1(  # type: ignore[arg-type]
                        request,
                        readiness,
                        changed,
                    )

    def test_non_ready_or_different_request_cannot_enter_stage1(self) -> None:
        request, readiness, representation = stage1_input()

        with self.assertRaisesRegex(ValueError, "readiness identity"):
            bind_understand_stage1(  # type: ignore[arg-type]
                replace(request, request_id="different-request"),
                readiness,
                representation,
            )

    @unittest.skipUnless(
        HAS_NEXAHEDRON_ALPHA,
        "accepted NEXAHEDRON Alpha checkout is not connected",
    )
    def test_cross_repository_proof_stops_after_stage1(self) -> None:
        result = execute_proof()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        proof = json.loads(result.stdout)
        self.assertEqual(
            proof["diagnostic_kind"],
            "internal_understand_stage1_binding",
        )
        self.assertEqual(proof["stages_completed"], ["understand/1"])
        self.assertEqual(proof["semantic_processing"], "none")
        self.assertEqual(proof["stop"], "before_understand/2")
        self.assertEqual(proof["binding"]["stage_id"], "understand/1")
        self.assertEqual(
            proof["binding"]["operator_id"],
            "orion.orientation-operator/understand",
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
            "b3d845ea91ae4bd0af295ff9237a13189f86e27114c769ca7d6ac431ab1b1723",
        )

    def test_stage1_source_has_no_semantic_or_downstream_dependency(self) -> None:
        module_path = ROOT / "src" / "orion" / "understand_stage1_alpha.py"
        proof_path = ROOT / "scripts" / "understand_stage1_alpha_proof.py"
        source = module_path.read_text(encoding="utf-8")
        proof_source = proof_path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(module_path))
        imports: set[str] = set()
        calls: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                imports.add(node.module or "")
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    calls.add(node.func.id)
                elif isinstance(node.func, ast.Attribute):
                    calls.add(node.func.attr)

        self.assertNotIn('get("content")', source)
        self.assertTrue(
            {
                "orion.backend",
                "orion.context_builder",
                "orion.gateway",
                "orion.lyra",
                "orion.operator_registry",
                "orion.representation_alpha",
                "orion.transformation_engine",
            }.isdisjoint(imports)
        )
        self.assertTrue(
            {
                "orient",
                "render",
                "validate_representation",
                "_report_id",
                "_blocked_report",
                "_complete_report",
                "_continuation",
                "_publish",
            }.isdisjoint(calls)
        )
        for forbidden_term in (
            "EvidenceReference",
            "OrientationReport",
            "ContinuationOption",
            "ReasoningBackend",
            "tokenizer",
            "embedding",
            "classifier",
        ):
            self.assertNotIn(forbidden_term, source)
            self.assertNotIn(forbidden_term, proof_source)
        for forbidden_gateway_term in (
            "OrientationGateway",
            "GatewayResponse",
            "RuntimeBoundary",
            "PresentationModel",
        ):
            self.assertNotIn(forbidden_gateway_term, proof_source)


if __name__ == "__main__":
    unittest.main()
