#!/usr/bin/env python3
"""Non-production Gate 0 harness for the frozen ORION Slice II-IV chain.

This script is verification only. It is not the Runtime or Gateway.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
from typing import Any, Callable


ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
CORE_COMMIT = "d34fbb2f99334534f4db89465a29f8bdb16d14d3"
CORE_FINGERPRINT = (
    "6201362c094530a0a31fa3d80b46c9131011bb8c8d400183271b0da0eb423f8d"
)
API_VERSION = "1.0"
RUNTIME_VERSION = "1.1.0"
MATERIAL_SCHEMA = "orion.confirmed-material/1.0"
LINEAGE_SCHEMA = "orion.clarification-lineage/1.0"
MANIFEST_SCHEMA = "orion.runtime-artifact-manifest/1.0"
TERMINAL_STOP = "at_slice_iv_certified"

COMMUNICATIVE_SCOPE = (
    "canonical_order",
    "orientation_map_entries",
    "orientation_map_identity",
    "provenance",
    "structural_adjacency",
)
DECLARED_LOSSINESS = (
    "human_interpretation",
    "semantic_meaning",
    "visual_layout",
)
DECLARED_EXCLUSIONS = (
    "actions",
    "generated_language",
    "recommendations",
    "semantic_reasoning",
)

EXPECTED_CALL_ORDER = (
    "ConfirmedMarkdownSource.create",
    "MarkdownStructuralRendererAlpha.project",
    "MarkdownStructuralRendererAlpha.render",
    "validate_markdown_structural_representation",
    "inventory_declared_source_elements",
    "summarize_declared_structure",
    "validate_structural_summary",
    "measure_declared_structure",
    "validate_structural_statistics",
    "generate_sequential_relations",
    "validate_sequential_relation_set",
    "generate_structural_equality_relations",
    "validate_structural_equality_relation_set",
    "generate_declared_reference_relations",
    "validate_declared_reference_relation_set",
    "validate_relation_conformance",
    "certify_relations",
    "create_navigation_object",
    "construct_navigation",
    "validate_navigation_conformance",
    "certify_navigation",
    "create_orientation_map_object",
    "construct_orientation_map",
    "validate_orientation_map_conformance",
    "certify_slice_iii",
    "create_expression_contract",
    "validate_expression_contract",
    "construct_expression",
    "validate_expression_conformance",
    "certify_expression",
    "certify_slice_iv",
)

EXPECTED_ARTIFACT_KINDS = (
    "structural_representation",
    "source_element_inventory",
    "structural_summary",
    "structural_statistics",
    "sequential_relation_set",
    "structural_equality_relation_set",
    "declared_reference_relation_set",
    "relation_conformance",
    "relations_certification",
    "navigation_object",
    "constructed_navigation",
    "navigation_conformance",
    "navigation_certification",
    "orientation_map_object",
    "constructed_orientation_map",
    "orientation_map_conformance",
    "slice_iii_certification",
    "expression_contract",
    "expression_artifact",
    "expression_conformance",
    "expression_certification",
    "slice_iv_certification",
)


def canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def digest_ref(value: bytes) -> str:
    return f"sha256:{sha256(value).hexdigest()}"


def core_source_hashes() -> dict[str, str]:
    return {
        str(path.relative_to(ROOT)): sha256(path.read_bytes()).hexdigest()
        for path in sorted(SRC.joinpath("orion").rglob("*.py"))
    }


def build_confirmed_material() -> dict[str, object]:
    content = (
        "# Gate 0\n"
        "\n"
        "The frozen ORION Core is invoked through its certified boundaries.\n"
        "\n"
        "## Verification\n"
        "\n"
        "Every produced artifact remains deterministic and inspectable.\n"
    )
    content_digest = sha256(content.encode("utf-8")).hexdigest()
    source_version = f"sha256:{content_digest}"
    confirmation_basis = {
        "orientation_object_id": "gate0-orientation-object",
        "orientation_object_version": "1",
        "source_id": "gate0-confirmed-source",
        "source_revision": source_version,
        "confirmed_by": "gate0-human-authority",
        "confirmed_revision": 1,
        "boundary_ref": "whole",
    }
    confirmation_digest = sha256(
        canonical_bytes(confirmation_basis)
    ).hexdigest()
    return {
        "schema_version": MATERIAL_SCHEMA,
        "orientation_object_id": "gate0-orientation-object",
        "orientation_object_version": "1",
        "source": {
            "entry_id": "gate0-confirmed-source",
            "source_owner": "gate0-human-authority",
            "source_ref": "gate0://confirmed-source/markdown",
            "source_version": source_version,
            "fragment_ref": "whole",
            "media_type": "text/markdown;charset=utf-8",
            "grammar": "CommonMark",
            "grammar_version": "0.31.2",
            "content": content,
            "integrity_sha256": content_digest,
        },
        "confirmation": {
            "confirmed_by": "gate0-human-authority",
            "confirmed_revision": 1,
            "confirmation_id": (
                f"confirmation-{confirmation_digest[:16]}"
            ),
        },
    }


def execute_once() -> dict[str, object]:
    sys.path.insert(0, str(SRC))

    from orion.declared_cross_references_alpha import (
        canonical_declared_reference_relation_set_bytes,
        generate_declared_reference_relations,
        validate_declared_reference_relation_set,
    )
    from orion.expression_certification_alpha import (
        canonical_expression_certification_report_bytes,
        certify_expression,
    )
    from orion.expression_conformance_alpha import (
        canonical_expression_conformance_report_bytes,
        validate_expression_conformance,
    )
    from orion.expression_construction_alpha import (
        canonical_expression_artifact_bytes,
        construct_expression,
    )
    from orion.expression_contract_alpha import (
        canonical_expression_contract_bytes,
        create_expression_contract,
        validate_expression_contract,
    )
    from orion.markdown_structural_renderer_alpha import (
        ConfirmedMarkdownSource,
        MarkdownStructuralRendererAlpha,
        canonical_representation_bytes,
        validate_markdown_structural_representation,
    )
    from orion.navigation_certification_alpha import (
        canonical_navigation_certification_report_bytes,
        certify_navigation,
    )
    from orion.navigation_conformance_alpha import (
        canonical_navigation_conformance_report_bytes,
        validate_navigation_conformance,
    )
    from orion.navigation_construction_alpha import (
        canonical_constructed_navigation_bytes,
        construct_navigation,
    )
    from orion.navigation_object_alpha import (
        canonical_navigation_object_bytes,
        create_navigation_object,
    )
    from orion.orientation_map_conformance_alpha import (
        canonical_orientation_map_conformance_report_bytes,
        validate_orientation_map_conformance,
    )
    from orion.orientation_map_construction_alpha import (
        canonical_constructed_orientation_map_bytes,
        construct_orientation_map,
    )
    from orion.orientation_map_object_alpha import (
        canonical_orientation_map_object_bytes,
        create_orientation_map_object,
    )
    from orion.public_contracts import (
        ContractSet,
        HumanAuthorityReference,
        IntegrityReference,
        Intention,
        NO_EFFECTS,
        ORIENTATION_REQUEST_SCHEMA,
        OrientationObjectReference,
        OrientationRequest,
        RequesterReference,
        Scope,
        validate_contract_set,
    )
    from orion.relation_conformance_alpha import (
        canonical_relation_conformance_report_bytes,
        validate_relation_conformance,
    )
    from orion.relations_certification_alpha import (
        canonical_relations_certification_report_bytes,
        certify_relations,
    )
    from orion.sequential_relations_alpha import (
        canonical_sequential_relation_set_bytes,
        generate_sequential_relations,
        validate_sequential_relation_set,
    )
    from orion.slice_iii_certification_alpha import (
        canonical_slice_iii_certification_report_bytes,
        certify_slice_iii,
    )
    from orion.slice_iv_certification_alpha import (
        canonical_slice_iv_certification_report_bytes,
        certify_slice_iv,
    )
    from orion.structural_equality_relations_alpha import (
        canonical_structural_equality_relation_set_bytes,
        generate_structural_equality_relations,
        validate_structural_equality_relation_set,
    )
    from orion.understand_source_element_inventory_alpha import (
        canonical_inventory_bytes,
        inventory_declared_source_elements,
    )
    from orion.understand_structural_statistics_alpha import (
        canonical_structural_statistics_bytes,
        measure_declared_structure,
        validate_structural_statistics,
    )
    from orion.understand_structural_summary_alpha import (
        canonical_structural_summary_bytes,
        summarize_declared_structure,
        validate_structural_summary,
    )

    frozen_before = core_source_hashes()
    material = build_confirmed_material()
    source = material["source"]
    confirmation = material["confirmation"]

    request = OrientationRequest(
        schema_version=ORIENTATION_REQUEST_SCHEMA,
        request_id="gate0-request",
        request_version="1",
        mode="understand",
        requested_by=RequesterReference(
            "nexahedron-gate0",
            "authorized_consumer",
            "nexahedron.gate0",
        ),
        human_authority=HumanAuthorityReference(
            "gate0-human-authority",
            ("intention", "scope", "continuation"),
        ),
        orientation_objects=(
            OrientationObjectReference(
                object_id=str(material["orientation_object_id"]),
                object_version=str(material["orientation_object_version"]),
                object_kind="Document",
                source_owner=str(source["source_owner"]),
                source_ref=str(source["source_ref"]),
                source_revision=str(source["source_version"]),
                identity_scope="session_local",
                integrity_ref=IntegrityReference(
                    "sha256",
                    str(source["integrity_sha256"]),
                    "whole",
                    True,
                ),
                access_status="available",
            ),
        ),
        intention=Intention(
            "Inspect the deterministic structural orientation of this material."
        ),
        scope=Scope(("declared structure",), (), ()),
        effects=NO_EFFECTS,
    )
    lineage = {
        "schema_version": LINEAGE_SCHEMA,
        "requests": [],
        "clarifications": [],
    }
    contract_validation = validate_contract_set(
        ContractSet(requests=(request,))
    )
    if not contract_validation.valid:
        raise AssertionError(
            f"Orientation Request invalid: {contract_validation.errors}"
        )

    request_basis = {
        "api_version": API_VERSION,
        "request": asdict(request),
        "confirmed_material": material,
        "lineage": lineage,
        "evidence": [],
    }
    request_digest = digest_ref(canonical_bytes(request_basis))

    calls: list[str] = []

    def call(name: str, function: Callable[..., Any], *args: Any, **kwargs: Any):
        calls.append(name)
        return function(*args, **kwargs)

    confirmed_source = call(
        "ConfirmedMarkdownSource.create",
        ConfirmedMarkdownSource.create,
        orientation_object_id=str(material["orientation_object_id"]),
        orientation_object_version=str(
            material["orientation_object_version"]
        ),
        source_id=str(source["entry_id"]),
        source_owner=str(source["source_owner"]),
        source_ref=str(source["source_ref"]),
        content=str(source["content"]),
        confirmed_by=str(confirmation["confirmed_by"]),
        confirmed_revision=int(confirmation["confirmed_revision"]),
    )
    if (
        confirmed_source.source_revision != source["source_version"]
        or confirmed_source.content_sha256 != source["integrity_sha256"]
        or confirmed_source.confirmation_id
        != confirmation["confirmation_id"]
    ):
        raise AssertionError("Confirmed Material mapping differs from Core")

    renderer = MarkdownStructuralRendererAlpha()
    projection = call(
        "MarkdownStructuralRendererAlpha.project",
        renderer.project,
        confirmed_source,
    )
    representation = call(
        "MarkdownStructuralRendererAlpha.render",
        renderer.render,
        confirmed_source,
    )
    representation_conformance = call(
        "validate_markdown_structural_representation",
        validate_markdown_structural_representation,
        confirmed_source,
        representation,
        renderer=renderer,
    )
    if not representation_conformance.valid:
        raise AssertionError("Representation Conformance rejected output")

    inventory = call(
        "inventory_declared_source_elements",
        inventory_declared_source_elements,
        representation,
    )
    summary = call(
        "summarize_declared_structure",
        summarize_declared_structure,
        inventory,
    )
    summary_validation = call(
        "validate_structural_summary",
        validate_structural_summary,
        inventory,
        summary,
    )
    if not summary_validation.valid:
        raise AssertionError("Structural Summary validation failed")

    statistics = call(
        "measure_declared_structure",
        measure_declared_structure,
        inventory,
    )
    statistics_validation = call(
        "validate_structural_statistics",
        validate_structural_statistics,
        inventory,
        statistics,
    )
    if not statistics_validation.valid:
        raise AssertionError("Structural Statistics validation failed")

    sequential = call(
        "generate_sequential_relations",
        generate_sequential_relations,
        summary,
        statistics,
    )
    sequential_validation = call(
        "validate_sequential_relation_set",
        validate_sequential_relation_set,
        summary,
        statistics,
        sequential,
    )
    if not sequential_validation.valid:
        raise AssertionError("Sequential Relation validation failed")

    equality = call(
        "generate_structural_equality_relations",
        generate_structural_equality_relations,
        summary,
        statistics,
    )
    equality_validation = call(
        "validate_structural_equality_relation_set",
        validate_structural_equality_relation_set,
        summary,
        statistics,
        equality,
    )
    if not equality_validation.valid:
        raise AssertionError("Structural Equality validation failed")

    relation_set = call(
        "generate_declared_reference_relations",
        generate_declared_reference_relations,
        summary,
        statistics,
        declarations=(),
    )
    declared_validation = call(
        "validate_declared_reference_relation_set",
        validate_declared_reference_relation_set,
        summary,
        statistics,
        (),
        relation_set,
    )
    if not declared_validation.valid:
        raise AssertionError("Declared Reference validation failed")

    relation_conformance = call(
        "validate_relation_conformance",
        validate_relation_conformance,
        relation_set,
        summary,
        statistics,
    )
    if not relation_conformance.valid:
        raise AssertionError("Relation Conformance rejected output")
    relations_certification = call(
        "certify_relations",
        certify_relations,
        relation_set,
        relation_conformance,
        summary,
        statistics,
    )

    navigation = call(
        "create_navigation_object",
        create_navigation_object,
        relation_set,
        relations_certification,
        summary,
        statistics,
    )
    constructed_navigation = call(
        "construct_navigation",
        construct_navigation,
        navigation,
        relation_set,
        relations_certification,
        summary,
        statistics,
    )
    navigation_conformance = call(
        "validate_navigation_conformance",
        validate_navigation_conformance,
        constructed_navigation,
        navigation,
        relation_set,
        relations_certification,
        summary,
        statistics,
    )
    if not navigation_conformance.valid:
        raise AssertionError("Navigation Conformance rejected output")
    navigation_certification = call(
        "certify_navigation",
        certify_navigation,
        navigation,
        constructed_navigation,
        navigation_conformance,
        relation_set,
        relations_certification,
        summary,
        statistics,
    )

    orientation_map = call(
        "create_orientation_map_object",
        create_orientation_map_object,
        navigation_certification,
        navigation,
        constructed_navigation,
        navigation_conformance,
        relation_set,
        relations_certification,
        summary,
        statistics,
    )
    constructed_map = call(
        "construct_orientation_map",
        construct_orientation_map,
        orientation_map,
        navigation_certification,
        navigation,
        constructed_navigation,
        navigation_conformance,
        relation_set,
        relations_certification,
        summary,
        statistics,
    )
    map_conformance = call(
        "validate_orientation_map_conformance",
        validate_orientation_map_conformance,
        orientation_map,
        constructed_map,
        navigation_certification,
        navigation,
        constructed_navigation,
        navigation_conformance,
        relation_set,
        relations_certification,
        summary,
        statistics,
    )
    if not map_conformance.valid:
        raise AssertionError("Orientation Map Conformance rejected output")
    slice_iii_certification = call(
        "certify_slice_iii",
        certify_slice_iii,
        relation_set,
        relations_certification,
        navigation,
        constructed_navigation,
        navigation_conformance,
        navigation_certification,
        orientation_map,
        constructed_map,
        map_conformance,
        summary,
        statistics,
    )

    expression_contract = call(
        "create_expression_contract",
        create_expression_contract,
        slice_iii_certification,
        map_conformance,
        orientation_map,
        constructed_map,
        communicative_scope=COMMUNICATIVE_SCOPE,
        declared_lossiness=DECLARED_LOSSINESS,
        declared_exclusions=DECLARED_EXCLUSIONS,
    )
    expression_contract_validation = call(
        "validate_expression_contract",
        validate_expression_contract,
        slice_iii_certification,
        map_conformance,
        orientation_map,
        constructed_map,
        expression_contract,
    )
    if not expression_contract_validation.valid:
        raise AssertionError("Expression Contract validation failed")
    expression_artifact = call(
        "construct_expression",
        construct_expression,
        expression_contract,
    )
    expression_conformance = call(
        "validate_expression_conformance",
        validate_expression_conformance,
        expression_contract,
        expression_artifact,
    )
    if not expression_conformance.valid:
        raise AssertionError("Expression Conformance rejected output")
    expression_certification = call(
        "certify_expression",
        certify_expression,
        expression_conformance,
    )
    slice_iv_certification = call(
        "certify_slice_iv",
        certify_slice_iv,
        expression_certification,
    )

    if tuple(calls) != EXPECTED_CALL_ORDER:
        raise AssertionError("Execution order differs from frozen contract")
    if slice_iv_certification.stop != TERMINAL_STOP:
        raise AssertionError("Terminal Slice IV STOP not reached")

    artifact_specs: tuple[
        tuple[str, object, Callable[[Any], bytes]], ...
    ] = (
        (
            "structural_representation",
            representation,
            canonical_representation_bytes,
        ),
        ("source_element_inventory", inventory, canonical_inventory_bytes),
        ("structural_summary", summary, canonical_structural_summary_bytes),
        (
            "structural_statistics",
            statistics,
            canonical_structural_statistics_bytes,
        ),
        (
            "sequential_relation_set",
            sequential,
            canonical_sequential_relation_set_bytes,
        ),
        (
            "structural_equality_relation_set",
            equality,
            canonical_structural_equality_relation_set_bytes,
        ),
        (
            "declared_reference_relation_set",
            relation_set,
            canonical_declared_reference_relation_set_bytes,
        ),
        (
            "relation_conformance",
            relation_conformance,
            canonical_relation_conformance_report_bytes,
        ),
        (
            "relations_certification",
            relations_certification,
            canonical_relations_certification_report_bytes,
        ),
        (
            "navigation_object",
            navigation,
            canonical_navigation_object_bytes,
        ),
        (
            "constructed_navigation",
            constructed_navigation,
            canonical_constructed_navigation_bytes,
        ),
        (
            "navigation_conformance",
            navigation_conformance,
            canonical_navigation_conformance_report_bytes,
        ),
        (
            "navigation_certification",
            navigation_certification,
            canonical_navigation_certification_report_bytes,
        ),
        (
            "orientation_map_object",
            orientation_map,
            canonical_orientation_map_object_bytes,
        ),
        (
            "constructed_orientation_map",
            constructed_map,
            canonical_constructed_orientation_map_bytes,
        ),
        (
            "orientation_map_conformance",
            map_conformance,
            canonical_orientation_map_conformance_report_bytes,
        ),
        (
            "slice_iii_certification",
            slice_iii_certification,
            canonical_slice_iii_certification_report_bytes,
        ),
        (
            "expression_contract",
            expression_contract,
            canonical_expression_contract_bytes,
        ),
        (
            "expression_artifact",
            expression_artifact,
            canonical_expression_artifact_bytes,
        ),
        (
            "expression_conformance",
            expression_conformance,
            canonical_expression_conformance_report_bytes,
        ),
        (
            "expression_certification",
            expression_certification,
            canonical_expression_certification_report_bytes,
        ),
        (
            "slice_iv_certification",
            slice_iv_certification,
            canonical_slice_iv_certification_report_bytes,
        ),
    )

    entries = []
    for ordinal, (kind, artifact, serializer) in enumerate(artifact_specs):
        serialized = serializer(artifact)
        body = json.loads(serialized.decode("utf-8"))
        version = next(
            (
                getattr(artifact, field_name)
                for field_name in (
                    "schema_version",
                    "diagnostic_version",
                    "navigation_schema_version",
                    "orientation_map_schema_version",
                )
                if hasattr(artifact, field_name)
            ),
            "",
        )
        if not version:
            raise AssertionError(f"{kind} has no frozen version")
        entries.append(
            {
                "ordinal": ordinal,
                "artifact_kind": kind,
                "artifact_version": version,
                "artifact_ref": digest_ref(serialized),
                "canonical_byte_length": len(serialized),
                "body": body,
            }
        )

    if tuple(entry["artifact_kind"] for entry in entries) != (
        EXPECTED_ARTIFACT_KINDS
    ):
        raise AssertionError("Manifest order differs from frozen contract")

    terminal_ref = entries[-1]["artifact_ref"]
    manifest = {
        "schema_version": MANIFEST_SCHEMA,
        "artifact_count": len(entries),
        "artifacts": entries,
        "terminal_artifact_ref": terminal_ref,
    }
    manifest_bytes = canonical_bytes(manifest)
    if len(entries) != 22 or len(manifest_bytes) > 16_000_000:
        raise AssertionError("Manifest violates frozen count or size")

    result_basis = {
        "api_version": API_VERSION,
        "request_digest": request_digest,
        "core_release": {
            "version": "1.0.0",
            "commit": CORE_COMMIT,
            "fingerprint": CORE_FINGERPRINT,
        },
        "status": "complete",
        "terminal_stop": TERMINAL_STOP,
        "artifact_manifest": manifest,
        "terminal_certification_ref": terminal_ref,
    }
    result_digest = digest_ref(canonical_bytes(result_basis))

    response_bytes = canonical_bytes(result_basis)
    resource_checks = {
        "request_bytes_within_limit": (
            len(canonical_bytes(request_basis)) <= 2_000_000
        ),
        "source_bytes_within_limit": (
            len(str(source["content"]).encode("utf-8")) <= 262_144
        ),
        "source_lines_within_limit": (
            len(str(source["content"]).splitlines()) <= 8_192
        ),
        "elements_within_limit": len(representation.elements) <= 128,
        "relations_within_limit": relation_set.relation_count <= 16_384,
        "manifest_bytes_within_limit": len(manifest_bytes) <= 16_000_000,
        "response_bytes_within_limit": len(response_bytes) <= 16_777_216,
    }
    if not all(resource_checks.values()):
        raise AssertionError("Gate 0 input exceeds an operational bound")

    frozen_after = core_source_hashes()
    if frozen_before != frozen_after:
        raise AssertionError("Frozen Core files changed during invocation")

    forbidden_modules = (
        "orion.gateway",
        "orion.gateway.gateway",
        "orion.orientation_runtime",
        "orion.orientation_runtime.runtime",
    )
    historical_modules_loaded = tuple(
        module for module in forbidden_modules if module in sys.modules
    )
    if historical_modules_loaded:
        raise AssertionError(
            f"Historical Runtime dependency loaded: {historical_modules_loaded}"
        )

    return {
        "proof_schema": "orion.gate0-execution-proof/1.0",
        "api_version": API_VERSION,
        "runtime_version_declared_only": RUNTIME_VERSION,
        "core_release": {
            "commit": CORE_COMMIT,
            "fingerprint": CORE_FINGERPRINT,
        },
        "request_id": request.request_id,
        "request_digest": request_digest,
        "result_digest": result_digest,
        "call_order": calls,
        "call_count": len(calls),
        "artifact_manifest": manifest,
        "manifest_ref": digest_ref(manifest_bytes),
        "manifest_byte_length": len(manifest_bytes),
        "terminal_certification_ref": terminal_ref,
        "terminal_certification_id": (
            slice_iv_certification.certification_id
        ),
        "terminal_certification_integrity": (
            slice_iv_certification.certification_integrity
        ),
        "terminal_stop": slice_iv_certification.stop,
        "expression_artifact_ref": entries[18]["artifact_ref"],
        "expression_certification_ref": entries[20]["artifact_ref"],
        "projection_block_count": len(projection.blocks),
        "element_count": len(representation.elements),
        "relation_count": relation_set.relation_count,
        "resource_checks": resource_checks,
        "confirmed_material_mapping_verified": True,
        "request_contract_verified": True,
        "clarification_contract_verified": (
            not request.clarification_of
            and not lineage["requests"]
            and not lineage["clarifications"]
        ),
        "core_sources_unchanged": True,
        "historical_runtime_modules_loaded": list(
            historical_modules_loaded
        ),
    }


def replay_summary(first: dict[str, object], second: dict[str, object]):
    first_manifest = first["artifact_manifest"]
    second_manifest = second["artifact_manifest"]
    first_entries = first_manifest["artifacts"]
    second_entries = second_manifest["artifacts"]
    comparisons = {
        "artifact_count_equal": (
            first_manifest["artifact_count"]
            == second_manifest["artifact_count"]
            == 22
        ),
        "artifact_order_equal": (
            [entry["artifact_kind"] for entry in first_entries]
            == [entry["artifact_kind"] for entry in second_entries]
        ),
        "artifact_refs_equal": (
            [entry["artifact_ref"] for entry in first_entries]
            == [entry["artifact_ref"] for entry in second_entries]
        ),
        "artifact_bodies_equal": (
            [entry["body"] for entry in first_entries]
            == [entry["body"] for entry in second_entries]
        ),
        "manifest_equal": first_manifest == second_manifest,
        "request_digest_equal": (
            first["request_digest"] == second["request_digest"]
        ),
        "result_digest_equal": (
            first["result_digest"] == second["result_digest"]
        ),
        "terminal_certification_equal": (
            first["terminal_certification_ref"]
            == second["terminal_certification_ref"]
            and first["terminal_certification_integrity"]
            == second["terminal_certification_integrity"]
        ),
        "expression_artifacts_equal": (
            first["expression_artifact_ref"]
            == second["expression_artifact_ref"]
            and first["expression_certification_ref"]
            == second["expression_certification_ref"]
        ),
        "call_order_equal": first["call_order"] == second["call_order"],
    }
    return {
        "proof_schema": "orion.gate0-replay-proof/1.0",
        "comparisons": comparisons,
        "byte_identical": all(comparisons.values()),
        "first_manifest_ref": first["manifest_ref"],
        "second_manifest_ref": second["manifest_ref"],
        "terminal_stop": first["terminal_stop"],
    }


def run_worker() -> int:
    print(canonical_bytes(execute_once()).decode("utf-8"))
    return 0


def run_supervisor() -> int:
    command = [sys.executable, str(Path(__file__).resolve()), "--worker"]
    outputs = []
    for _ in range(2):
        completed = subprocess.run(
            command,
            cwd=ROOT,
            check=False,
            capture_output=True,
            timeout=30,
        )
        if completed.returncode != 0:
            sys.stderr.write(completed.stderr.decode("utf-8", "replace"))
            return completed.returncode or 1
        outputs.append(json.loads(completed.stdout.decode("utf-8")))

    replay = replay_summary(outputs[0], outputs[1])
    proof = {
        "proof_schema": "orion.gate0-supervised-proof/1.0",
        "independent_worker_processes": 2,
        "initial": {
            key: outputs[0][key]
            for key in (
                "request_digest",
                "result_digest",
                "manifest_ref",
                "manifest_byte_length",
                "terminal_certification_ref",
                "terminal_certification_id",
                "terminal_stop",
                "call_count",
                "element_count",
                "relation_count",
                "resource_checks",
                "core_sources_unchanged",
                "historical_runtime_modules_loaded",
            )
        },
        "replay": replay,
        "passed": (
            replay["byte_identical"]
            and outputs[0]["call_order"] == list(EXPECTED_CALL_ORDER)
            and outputs[0]["terminal_stop"] == TERMINAL_STOP
            and outputs[0]["core_sources_unchanged"]
            and not outputs[0]["historical_runtime_modules_loaded"]
        ),
    }
    print(canonical_bytes(proof).decode("utf-8"))
    return 0 if proof["passed"] else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker", action="store_true")
    args = parser.parse_args()
    return run_worker() if args.worker else run_supervisor()


if __name__ == "__main__":
    raise SystemExit(main())
