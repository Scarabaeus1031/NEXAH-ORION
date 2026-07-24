"""Tests for the UNDERSTAND source-element declaration check Alpha."""

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
    DeclaredSourceBoundaryEntry,
    DeclaredSourceBoundaryInventoryDiagnostic,
)
from orion.understand_source_element_declaration_check_alpha import (
    DeclaredSourceElementDeclarationDiagnostic,
    check_declared_source_element_declaration,
)
from orion.understand_stage1_alpha import UnderstandStage1BindingDiagnostic


ROOT = Path(__file__).resolve().parent.parent
PROOF = (
    ROOT
    / "scripts"
    / "understand_source_element_declaration_check_alpha_proof.py"
)
NEXAHEDRON_ROOT = Path(
    os.environ.get("NEXAHEDRON_ROOT", ROOT.parent / "NEXAHEDRON")
)
HAS_NEXAHEDRON_ALPHA = (
    NEXAHEDRON_ROOT / "scripts" / "representation-referenced-request.mjs"
).is_file()
CONTENT_SHA256 = "a" * 64
REPRESENTATION_SHA256 = "b" * 64
REPRESENTATION_VERSION = f"sha256:{REPRESENTATION_SHA256}"


def declaration_input() -> tuple[
    object,
    UnderstandStage1BindingDiagnostic,
    DeclaredRepresentationInventoryDiagnostic,
    DeclaredSourceBoundaryInventoryDiagnostic,
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
    representation = DeclaredRepresentationInventoryEntry(
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
    representation_inventory = DeclaredRepresentationInventoryDiagnostic(
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
        representations=(representation,),
        responsibility_state="completed",
        stop="before_source_structure_inventory",
    )
    boundary = DeclaredSourceBoundaryEntry(
        representation_id=representation_id,
        representation_version=REPRESENTATION_VERSION,
        source_owner=stage1.source_owner,
        source_ref=stage1.source_ref,
        source_revision=stage1.source_revision,
        fragment_ref="whole",
        integrity_method=stage1.integrity_method,
        integrity_value=stage1.integrity_value,
        integrity_coverage=stage1.integrity_coverage,
        integrity_verified=stage1.integrity_verified,
    )
    boundary_inventory = DeclaredSourceBoundaryInventoryDiagnostic(
        diagnostic_version="0.1-alpha",
        request_id=request.request_id,
        request_version=request.request_version,
        operator_id=stage1.operator_id,
        operator_version=stage1.operator_version,
        orientation_object_id=orientation_object.object_id,
        orientation_object_version=orientation_object.object_version,
        predecessor_responsibility="declared_representation_inventory",
        predecessor_stop="before_source_structure_inventory",
        canonical_stage="understand/2",
        responsibility="declared_source_boundary_inventory",
        ordered_boundary_count=1,
        boundaries=(boundary,),
        responsibility_state="completed",
        canonical_stage_state="incomplete",
        stop="before_declared_source_element_inventory",
    )
    return request, stage1, representation_inventory, boundary_inventory


def execute_proof() -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(PROOF)],
        cwd=ROOT,
        env={**os.environ, "PYTHONPATH": str(ROOT / "src")},
        check=False,
        capture_output=True,
        text=True,
    )


class UnderstandSourceElementDeclarationCheckAlphaTests(unittest.TestCase):
    def test_exact_profile_deterministically_reports_not_declared(self) -> None:
        request, stage1, representation_inventory, boundary_inventory = (
            declaration_input()
        )

        diagnostic = check_declared_source_element_declaration(
            request,  # type: ignore[arg-type]
            stage1,
            representation_inventory,
            boundary_inventory,
        )

        self.assertEqual(
            diagnostic.predecessor_responsibility,
            "declared_source_boundary_inventory",
        )
        self.assertEqual(
            diagnostic.predecessor_stop,
            "before_declared_source_element_inventory",
        )
        self.assertEqual(diagnostic.canonical_stage, "understand/2")
        self.assertEqual(
            diagnostic.responsibility,
            "declared_source_element_declaration_check",
        )
        self.assertEqual(
            diagnostic.declaration_basis,
            "orion.representation/exact-text/0.1-alpha",
        )
        self.assertEqual(diagnostic.declaration_state, "not_declared")
        self.assertEqual(diagnostic.responsibility_state, "completed")
        self.assertEqual(diagnostic.canonical_stage_state, "incomplete")
        self.assertEqual(
            diagnostic.stop,
            "before_declared_source_element_inventory",
        )

    def test_diagnostic_is_immutable_internal_and_contains_no_inventory(self) -> None:
        import orion
        import orion.understand_source_element_declaration_check_alpha as module

        request, stage1, representation_inventory, boundary_inventory = (
            declaration_input()
        )
        diagnostic = check_declared_source_element_declaration(
            request,  # type: ignore[arg-type]
            stage1,
            representation_inventory,
            boundary_inventory,
        )
        value = asdict(diagnostic)

        self.assertIsInstance(
            diagnostic,
            DeclaredSourceElementDeclarationDiagnostic,
        )
        self.assertEqual(module.__all__, ())
        self.assertNotIn(
            "DeclaredSourceElementDeclarationDiagnostic",
            orion.__all__,
        )
        for forbidden_field in (
            "elements",
            "element_count",
            "payload",
            "content_length",
            "findings",
            "evidence",
            "report",
            "continuations",
        ):
            self.assertNotIn(forbidden_field, value)
        with self.assertRaises(FrozenInstanceError):
            diagnostic.declaration_state = "declared"  # type: ignore[misc]

    def test_unknown_or_changed_profile_fails_without_guessing(self) -> None:
        request, stage1, inventory, boundary = declaration_input()
        mutations = (
            ("schema", "representation_schema", "other/schema"),
            ("projection", "projection_id", "other/projection"),
            ("projection version", "projection_version", "2"),
            ("renderer", "renderer_id", "other/renderer"),
            ("renderer version", "renderer_version", "2"),
            ("target domain", "target_domain", "other/domain"),
            ("media type", "media_type", "text/markdown"),
            ("lossiness", "declared_lossiness", ("unknown",)),
        )

        for name, field_name, value in mutations:
            with self.subTest(name=name):
                changed_entry = replace(
                    inventory.representations[0],
                    **{field_name: value},
                )
                changed = replace(inventory, representations=(changed_entry,))
                with self.assertRaisesRegex(ValueError, "unknown Representation"):
                    check_declared_source_element_declaration(
                        request,  # type: ignore[arg-type]
                        stage1,
                        changed,
                        boundary,
                    )

    def test_predecessor_and_identity_mismatches_fail(self) -> None:
        request, stage1, inventory, boundary = declaration_input()
        orientation_object = request.orientation_objects[0]  # type: ignore[union-attr]
        cases = (
            (
                "predecessor responsibility",
                request,
                stage1,
                inventory,
                replace(boundary, responsibility="other"),
            ),
            (
                "predecessor stop",
                request,
                stage1,
                inventory,
                replace(boundary, stop="after_inventory"),
            ),
            (
                "request",
                replace(request, request_id="request-other"),
                stage1,
                inventory,
                boundary,
            ),
            (
                "object",
                replace(
                    request,
                    orientation_objects=(
                        replace(orientation_object, object_id="object-other"),
                    ),
                ),
                stage1,
                inventory,
                boundary,
            ),
            (
                "Representation",
                request,
                stage1,
                inventory,
                replace(
                    boundary,
                    boundaries=(
                        replace(
                            boundary.boundaries[0],
                            representation_id="representation-other",
                        ),
                    ),
                ),
            ),
            (
                "source",
                request,
                stage1,
                inventory,
                replace(
                    boundary,
                    boundaries=(
                        replace(boundary.boundaries[0], source_ref="source-other"),
                    ),
                ),
            ),
        )

        for name, changed_request, changed_stage1, changed_inventory, changed_boundary in cases:
            with self.subTest(name=name):
                with self.assertRaises(ValueError):
                    check_declared_source_element_declaration(
                        changed_request,  # type: ignore[arg-type]
                        changed_stage1,
                        changed_inventory,
                        changed_boundary,
                    )

    def test_signature_and_io_sentinel_exclude_content_inputs(self) -> None:
        self.assertEqual(
            tuple(
                inspect.signature(
                    check_declared_source_element_declaration
                ).parameters
            ),
            (
                "request",
                "stage1",
                "representation_inventory",
                "boundary_inventory",
            ),
        )
        request, stage1, inventory, boundary = declaration_input()
        with patch(
            "builtins.open",
            side_effect=AssertionError("filesystem access is forbidden"),
        ):
            diagnostic = check_declared_source_element_declaration(
                request,  # type: ignore[arg-type]
                stage1,
                inventory,
                boundary,
            )
        self.assertEqual(diagnostic.declaration_state, "not_declared")

    def test_source_has_no_io_parser_semantic_or_downstream_dependency(self) -> None:
        module_path = (
            ROOT
            / "src"
            / "orion"
            / "understand_source_element_declaration_check_alpha.py"
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
                "re",
                "json",
                "xml",
                "html",
                "markdown",
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
                "compile",
                "match",
                "search",
                "findall",
                "loads",
                "orient",
                "render",
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
    def test_cross_repository_proof_stops_before_element_inventory(self) -> None:
        result = execute_proof()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        proof = json.loads(result.stdout)
        diagnostic = proof["declaration"]
        self.assertEqual(
            proof["diagnostic_kind"],
            "internal_declared_source_element_declaration_check",
        )
        self.assertEqual(
            diagnostic["predecessor_responsibility"],
            "declared_source_boundary_inventory",
        )
        self.assertEqual(diagnostic["declaration_state"], "not_declared")
        self.assertFalse(proof["element_inventory_created"])
        self.assertFalse(proof["payload_accessed"])
        self.assertFalse(proof["parser_invoked"])
        self.assertFalse(proof["filesystem_accessed"])
        self.assertEqual(proof["structural_discovery"], "none")
        self.assertEqual(proof["semantic_processing"], "none")
        self.assertFalse(proof["canonical_stage_completed"])
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
            "740808f29d4b40b3f55c12472be52db4f93c4d615621b255da810055feebb4d7",
        )


if __name__ == "__main__":
    unittest.main()
