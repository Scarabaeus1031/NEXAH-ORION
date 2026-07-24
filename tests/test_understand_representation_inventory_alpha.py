"""Tests for metadata-only UNDERSTAND declared Representation inventory."""

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
from orion.understand_representation_inventory_alpha import (
    DeclaredRepresentationInventoryDiagnostic,
    inventory_declared_representation,
)
from orion.understand_stage1_alpha import bind_understand_stage1


ROOT = Path(__file__).resolve().parent.parent
PROOF = ROOT / "scripts" / "understand_representation_inventory_alpha_proof.py"
NEXAHEDRON_ROOT = Path(
    os.environ.get("NEXAHEDRON_ROOT", ROOT.parent / "NEXAHEDRON")
)
HAS_NEXAHEDRON_ALPHA = (
    NEXAHEDRON_ROOT / "scripts" / "representation-referenced-request.mjs"
).is_file()
CONTENT_SHA256 = "a" * 64
REPRESENTATION_SHA256 = "b" * 64


class _PayloadAccessGuard(dict[str, object]):
    def get(self, key: str, default: object = None) -> object:
        if key == "payload":
            raise AssertionError("inventory attempted to access payload")
        return super().get(key, default)


def inventory_input() -> tuple[object, object, _PayloadAccessGuard]:
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
    representation = _PayloadAccessGuard(
        {
            "schema_version": "orion.representation/exact-text/0.1-alpha",
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
            "fragment_ref": "whole",
            "projection": {
                "projection_id": "orion.projection/exact-text",
                "projection_version": "0.1-alpha",
                "source_media_type": "text/plain;charset=utf-8",
                "target_domain": "orion.representation.text-exact",
                "declared_lossiness": ["none"],
            },
            "renderer_id": "orion.renderer/exact-text",
            "renderer_version": "0.1-alpha",
            "declared_lossiness": ["none"],
            "payload": {"content": "must remain untouched"},
        }
    )
    readiness = prove_runtime_readiness(request)
    stage1 = bind_understand_stage1(
        request,
        readiness,
        {
            **representation,
            "payload": {"content_sha256": CONTENT_SHA256},
        },
    )
    return request, stage1, representation


def execute_proof() -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(PROOF)],
        cwd=ROOT,
        env={**os.environ, "PYTHONPATH": str(ROOT / "src")},
        check=False,
        capture_output=True,
        text=True,
    )


class UnderstandRepresentationInventoryAlphaTests(unittest.TestCase):
    def test_inventory_preserves_exact_declared_metadata_and_order(self) -> None:
        request, stage1, representation = inventory_input()

        diagnostic = inventory_declared_representation(  # type: ignore[arg-type]
            request,
            stage1,
            representation,
        )

        self.assertEqual(diagnostic.canonical_stage, "understand/2")
        self.assertEqual(
            diagnostic.responsibility,
            "declared_representation_inventory",
        )
        self.assertEqual(diagnostic.ordered_representation_count, 1)
        self.assertEqual(len(diagnostic.representations), 1)
        entry = diagnostic.representations[0]
        self.assertEqual(entry.representation_id, "representation-paper-01")
        self.assertEqual(
            entry.representation_version,
            f"sha256:{REPRESENTATION_SHA256}",
        )
        self.assertEqual(entry.projection_id, "orion.projection/exact-text")
        self.assertEqual(entry.renderer_id, "orion.renderer/exact-text")
        self.assertEqual(entry.declared_lossiness, ("none",))
        self.assertEqual(diagnostic.responsibility_state, "completed")
        self.assertEqual(diagnostic.stop, "before_source_structure_inventory")

    def test_payload_access_guard_remains_untriggered(self) -> None:
        request, stage1, representation = inventory_input()

        diagnostic = inventory_declared_representation(  # type: ignore[arg-type]
            request,
            stage1,
            representation,
        )

        self.assertEqual(diagnostic.ordered_representation_count, 1)

    def test_inventory_diagnostic_is_internal_and_does_not_complete_stage2(self) -> None:
        import orion
        import orion.understand_representation_inventory_alpha as inventory_alpha

        request, stage1, representation = inventory_input()
        diagnostic = inventory_declared_representation(  # type: ignore[arg-type]
            request,
            stage1,
            representation,
        )
        value = asdict(diagnostic)

        self.assertIsInstance(
            diagnostic,
            DeclaredRepresentationInventoryDiagnostic,
        )
        self.assertEqual(inventory_alpha.__all__, ())
        self.assertNotIn(
            "DeclaredRepresentationInventoryDiagnostic",
            orion.__all__,
        )
        self.assertFalse(hasattr(diagnostic, "schema_version"))
        self.assertNotIn("stage_state", value)
        self.assertNotEqual(value["responsibility_state"], "stage_completed")
        with self.assertRaises(FrozenInstanceError):
            diagnostic.canonical_stage = "understand/3"  # type: ignore[misc]

    def test_mismatched_declared_metadata_fails_without_selection_or_repair(self) -> None:
        request, stage1, representation = inventory_input()
        mutations = {
            "representation identity": lambda value: value.update(
                representation_id="similar-representation"
            ),
            "representation version": lambda value: value.update(
                representation_version=f"sha256:{'c' * 64}"
            ),
            "projection identity": lambda value: value["projection"].update(  # type: ignore[union-attr]
                projection_id=""
            ),
            "renderer version": lambda value: value.update(
                renderer_version=""
            ),
            "target domain": lambda value: value["projection"].update(  # type: ignore[union-attr]
                target_domain=""
            ),
            "lossiness": lambda value: value.update(
                declared_lossiness=["unknown"]
            ),
        }

        for name, mutate in mutations.items():
            with self.subTest(name=name):
                changed = deepcopy(representation)
                mutate(changed)
                with self.assertRaises(ValueError):
                    inventory_declared_representation(  # type: ignore[arg-type]
                        request,
                        stage1,
                        changed,
                    )

    def test_inventory_refuses_more_than_the_exact_alpha_representation(self) -> None:
        request, stage1, representation = inventory_input()
        orientation_object = request.orientation_objects[0]  # type: ignore[union-attr]
        changed_request = replace(
            request,
            orientation_objects=(
                replace(
                    orientation_object,
                    representation_refs=(
                        *orientation_object.representation_refs,
                        "representation-other@1",
                    ),
                ),
            ),
        )

        with self.assertRaisesRegex(ValueError, "exactly one"):
            inventory_declared_representation(
                changed_request,
                stage1,  # type: ignore[arg-type]
                representation,
            )

    @unittest.skipUnless(
        HAS_NEXAHEDRON_ALPHA,
        "accepted NEXAHEDRON Alpha checkout is not connected",
    )
    def test_cross_repository_proof_stops_before_source_structure(self) -> None:
        result = execute_proof()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        proof = json.loads(result.stdout)
        self.assertEqual(
            proof["diagnostic_kind"],
            "internal_declared_representation_inventory",
        )
        self.assertEqual(
            proof["inventory"]["responsibility"],
            "declared_representation_inventory",
        )
        self.assertEqual(proof["inventory"]["ordered_representation_count"], 1)
        self.assertEqual(proof["payload_accessed"], False)
        self.assertEqual(proof["source_structure_inspected"], False)
        self.assertEqual(proof["semantic_processing"], "none")
        self.assertEqual(proof["stage_completed"], False)
        self.assertEqual(proof["stop"], "before_source_structure_inventory")

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
            "54469b52ac2fb4b3fc1d72b8da9b2d4b731b3023158151a1b75281e11fba3b2b",
        )

    def test_inventory_source_has_no_semantic_or_downstream_dependency(self) -> None:
        module_path = (
            ROOT
            / "src"
            / "orion"
            / "understand_representation_inventory_alpha.py"
        )
        source = module_path.read_text(encoding="utf-8")
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

        self.assertNotIn('get("payload")', source)
        self.assertNotIn('["payload"]', source)
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
                "sorted",
                "min",
                "max",
                "_report_id",
                "_blocked_report",
                "_complete_report",
                "_continuation",
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
            "heading",
            "paragraph",
            "graph",
        ):
            self.assertNotIn(forbidden_term, source)


if __name__ == "__main__":
    unittest.main()
