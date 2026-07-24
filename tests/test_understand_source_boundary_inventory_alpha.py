"""Tests for metadata-only UNDERSTAND declared source-boundary inventory."""

from __future__ import annotations

import ast
from dataclasses import FrozenInstanceError, asdict, replace
from hashlib import sha256
import inspect
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

from orion.public_contracts import IntegrityReference
from orion.public_contracts.fixtures import VALID_REQUEST
from orion.understand_representation_inventory_alpha import (
    DeclaredRepresentationInventoryDiagnostic,
    DeclaredRepresentationInventoryEntry,
)
from orion.understand_source_boundary_inventory_alpha import (
    DeclaredSourceBoundaryInventoryDiagnostic,
    inventory_declared_source_boundaries,
)
from orion.understand_stage1_alpha import UnderstandStage1BindingDiagnostic


ROOT = Path(__file__).resolve().parent.parent
PROOF = ROOT / "scripts" / "understand_source_boundary_inventory_alpha_proof.py"
NEXAHEDRON_ROOT = Path(
    os.environ.get("NEXAHEDRON_ROOT", ROOT.parent / "NEXAHEDRON")
)
HAS_NEXAHEDRON_ALPHA = (
    NEXAHEDRON_ROOT / "scripts" / "representation-referenced-request.mjs"
).is_file()
CONTENT_SHA256 = "a" * 64
REPRESENTATION_SHA256 = "b" * 64
REPRESENTATION_VERSION = f"sha256:{REPRESENTATION_SHA256}"


def boundary_input() -> tuple[
    object,
    UnderstandStage1BindingDiagnostic,
    DeclaredRepresentationInventoryDiagnostic,
]:
    representation_id = "representation-paper-01"
    representation_ref = f"{representation_id}@{REPRESENTATION_VERSION}"
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
    request = replace(VALID_REQUEST, orientation_objects=(orientation_object,))
    stage1 = UnderstandStage1BindingDiagnostic(
        diagnostic_version="0.1-alpha",
        request_id=request.request_id,
        request_version=request.request_version,
        operator_id="orion.orientation-operator/understand",
        operator_version="1.0",
        orientation_object_id=orientation_object.object_id,
        orientation_object_version=orientation_object.object_version,
        representation_id=representation_id,
        representation_version=REPRESENTATION_VERSION,
        source_owner=orientation_object.source_owner,
        source_ref=orientation_object.source_ref,
        source_revision=orientation_object.source_revision,
        integrity_method="sha256",
        integrity_value=CONTENT_SHA256,
        integrity_coverage="whole",
        integrity_verified=True,
        stage_id="understand/1",
        completion_state="completed",
        stop="before_understand/2",
    )
    entry = DeclaredRepresentationInventoryEntry(
        representation_id=representation_id,
        representation_version=REPRESENTATION_VERSION,
        representation_schema="orion.representation/exact-text/0.1-alpha",
        projection_id="orion.projection/exact-text",
        projection_version="0.1-alpha",
        renderer_id="orion.renderer/exact-text",
        renderer_version="0.1-alpha",
        target_domain="orion.representation.text-exact",
        media_type="text/plain;charset=utf-8",
        fragment_ref="whole",
        declared_lossiness=("none",),
    )
    inventory = DeclaredRepresentationInventoryDiagnostic(
        diagnostic_version="0.1-alpha",
        request_id=request.request_id,
        request_version=request.request_version,
        operator_id=stage1.operator_id,
        operator_version=stage1.operator_version,
        orientation_object_id=orientation_object.object_id,
        orientation_object_version=orientation_object.object_version,
        canonical_stage="understand/2",
        responsibility="declared_representation_inventory",
        ordered_representation_count=1,
        representations=(entry,),
        responsibility_state="completed",
        stop="before_source_structure_inventory",
    )
    return request, stage1, inventory


def execute_proof() -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(PROOF)],
        cwd=ROOT,
        env={**os.environ, "PYTHONPATH": str(ROOT / "src")},
        check=False,
        capture_output=True,
        text=True,
    )


class UnderstandSourceBoundaryInventoryAlphaTests(unittest.TestCase):
    def test_preserves_exact_declared_boundary_and_lineage(self) -> None:
        request, stage1, inventory = boundary_input()

        diagnostic = inventory_declared_source_boundaries(
            request,  # type: ignore[arg-type]
            stage1,
            inventory,
        )

        self.assertEqual(
            diagnostic.predecessor_responsibility,
            "declared_representation_inventory",
        )
        self.assertEqual(
            diagnostic.predecessor_stop,
            "before_source_structure_inventory",
        )
        self.assertEqual(diagnostic.canonical_stage, "understand/2")
        self.assertEqual(
            diagnostic.responsibility,
            "declared_source_boundary_inventory",
        )
        self.assertEqual(diagnostic.ordered_boundary_count, 1)
        self.assertEqual(len(diagnostic.boundaries), 1)
        boundary = diagnostic.boundaries[0]
        self.assertEqual(boundary.representation_id, stage1.representation_id)
        self.assertEqual(
            boundary.representation_version,
            stage1.representation_version,
        )
        self.assertEqual(boundary.source_ref, stage1.source_ref)
        self.assertEqual(boundary.source_revision, stage1.source_revision)
        self.assertEqual(boundary.fragment_ref, "whole")
        self.assertEqual(boundary.integrity_value, stage1.integrity_value)
        self.assertTrue(boundary.integrity_verified)
        self.assertEqual(diagnostic.responsibility_state, "completed")
        self.assertEqual(diagnostic.canonical_stage_state, "incomplete")
        self.assertEqual(
            diagnostic.stop,
            "before_declared_source_element_inventory",
        )

    def test_diagnostic_is_immutable_internal_and_not_a_runtime_outcome(self) -> None:
        import orion
        import orion.understand_source_boundary_inventory_alpha as module

        request, stage1, inventory = boundary_input()
        diagnostic = inventory_declared_source_boundaries(
            request,  # type: ignore[arg-type]
            stage1,
            inventory,
        )
        value = asdict(diagnostic)

        self.assertIsInstance(
            diagnostic,
            DeclaredSourceBoundaryInventoryDiagnostic,
        )
        self.assertEqual(module.__all__, ())
        self.assertNotIn(
            "DeclaredSourceBoundaryInventoryDiagnostic",
            orion.__all__,
        )
        self.assertNotIn("schema_version", value)
        self.assertNotIn("status", value)
        self.assertNotIn("result", value)
        self.assertNotIn("report", value)
        with self.assertRaises(FrozenInstanceError):
            diagnostic.canonical_stage_state = "completed"  # type: ignore[misc]

    def test_rejects_any_predecessor_or_lineage_mismatch(self) -> None:
        request, stage1, inventory = boundary_input()
        orientation_object = request.orientation_objects[0]  # type: ignore[union-attr]
        cases = (
            (
                "predecessor responsibility",
                request,
                stage1,
                replace(inventory, responsibility="source_structure_inventory"),
            ),
            (
                "predecessor stop",
                request,
                stage1,
                replace(inventory, stop="after_source_structure_inventory"),
            ),
            (
                "request identity",
                replace(request, request_id="request-other"),
                stage1,
                inventory,
            ),
            (
                "object identity",
                replace(
                    request,
                    orientation_objects=(
                        replace(orientation_object, object_id="object-other"),
                    ),
                ),
                stage1,
                inventory,
            ),
            (
                "source revision",
                replace(
                    request,
                    orientation_objects=(
                        replace(
                            orientation_object,
                            source_revision="sha256:other",
                        ),
                    ),
                ),
                stage1,
                inventory,
            ),
            (
                "Representation identity",
                request,
                stage1,
                replace(
                    inventory,
                    representations=(
                        replace(
                            inventory.representations[0],
                            representation_id="representation-other",
                        ),
                    ),
                ),
            ),
            (
                "fragment boundary",
                request,
                stage1,
                replace(
                    inventory,
                    representations=(
                        replace(inventory.representations[0], fragment_ref="part"),
                    ),
                ),
            ),
            (
                "integrity coverage",
                replace(
                    request,
                    orientation_objects=(
                        replace(
                            orientation_object,
                            integrity_ref=replace(
                                orientation_object.integrity_ref,
                                coverage="part",
                            ),
                        ),
                    ),
                ),
                stage1,
                inventory,
            ),
        )

        for name, changed_request, changed_stage1, changed_inventory in cases:
            with self.subTest(name=name):
                with self.assertRaises(ValueError):
                    inventory_declared_source_boundaries(
                        changed_request,  # type: ignore[arg-type]
                        changed_stage1,
                        changed_inventory,
                    )

    def test_refuses_multiple_boundaries_without_selection_or_repair(self) -> None:
        request, stage1, inventory = boundary_input()
        changed = replace(
            inventory,
            ordered_representation_count=2,
            representations=(
                *inventory.representations,
                replace(
                    inventory.representations[0],
                    representation_id="representation-other",
                ),
            ),
        )

        with self.assertRaisesRegex(ValueError, "one Representation"):
            inventory_declared_source_boundaries(
                request,  # type: ignore[arg-type]
                stage1,
                changed,
            )

    def test_signature_excludes_representation_payload_and_source_content(self) -> None:
        self.assertEqual(
            tuple(inspect.signature(inventory_declared_source_boundaries).parameters),
            ("request", "stage1", "representation_inventory"),
        )

    def test_file_access_sentinel_remains_untriggered(self) -> None:
        request, stage1, inventory = boundary_input()

        with patch(
            "builtins.open",
            side_effect=AssertionError("source-content access is forbidden"),
        ):
            diagnostic = inventory_declared_source_boundaries(
                request,  # type: ignore[arg-type]
                stage1,
                inventory,
            )

        self.assertEqual(diagnostic.ordered_boundary_count, 1)

    def test_source_has_no_io_semantic_or_downstream_dependency(self) -> None:
        module_path = (
            ROOT
            / "src"
            / "orion"
            / "understand_source_boundary_inventory_alpha.py"
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

        self.assertTrue(
            {
                "pathlib",
                "os",
                "orion.backend",
                "orion.context_builder",
                "orion.context_brief",
                "orion.contracts",
                "orion.gateway",
                "orion.lyra",
                "orion.representation_alpha",
                "orion.transformation_engine",
            }.isdisjoint(imports)
        )
        self.assertTrue(
            {
                "open",
                "read",
                "read_text",
                "read_bytes",
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
            "ContextManifest",
            "ContextBrief",
            "EvidenceReference",
            "OrientationReport",
            "ContinuationOption",
            "ReasoningBackend",
            "tokenizer",
            "embedding",
            "classifier",
        ):
            self.assertNotIn(forbidden_term, source)

    @unittest.skipUnless(
        HAS_NEXAHEDRON_ALPHA,
        "accepted NEXAHEDRON Alpha checkout is not connected",
    )
    def test_cross_repository_proof_stops_before_source_elements(self) -> None:
        result = execute_proof()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        proof = json.loads(result.stdout)
        diagnostic = proof["boundary_inventory"]
        self.assertEqual(
            proof["diagnostic_kind"],
            "internal_declared_source_boundary_inventory",
        )
        self.assertEqual(
            diagnostic["predecessor_responsibility"],
            "declared_representation_inventory",
        )
        self.assertEqual(diagnostic["ordered_boundary_count"], 1)
        self.assertEqual(diagnostic["boundaries"][0]["fragment_ref"], "whole")
        self.assertEqual(proof["payload_accessed"], False)
        self.assertEqual(proof["source_content_accessed"], False)
        self.assertEqual(proof["source_elements_inventoried"], False)
        self.assertEqual(proof["semantic_processing"], "none")
        self.assertEqual(proof["canonical_stage_completed"], False)
        self.assertEqual(
            proof["stop"],
            "before_declared_source_element_inventory",
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
            "9b639edffc15bec1d5d6acd83658f845c8e01c31227fdae20a277c2d39f3dbe1",
        )


if __name__ == "__main__":
    unittest.main()
