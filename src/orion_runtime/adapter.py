"""Mechanical invocation adapter for the frozen Slice II-IV Core chain."""

from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any, Callable

from .canonical import canonical_bytes, digest_ref
from .constants import (
    COMMUNICATIVE_SCOPE,
    DECLARED_EXCLUSIONS,
    DECLARED_LOSSINESS,
    EXPECTED_ARTIFACT_KINDS,
    MANIFEST_SCHEMA,
    MAX_ELEMENTS,
    MAX_MANIFEST_BYTES,
    MAX_RELATIONS,
    TERMINAL_STOP,
)
from .errors import RuntimeBoundaryError


@dataclass(frozen=True, slots=True)
class AdapterResult:
    artifact_manifest: dict[str, Any]
    terminal_certification_ref: str
    terminal_stop: str
    element_count: int
    relation_count: int


def invoke_frozen_core(envelope: dict[str, Any]) -> AdapterResult:
    """Invoke only the 31 entry points frozen by the execution contract."""
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

    input_before = canonical_bytes(envelope)
    material = envelope["confirmed_material"]
    source = material["source"]
    confirmation = material["confirmation"]

    confirmed_source = ConfirmedMarkdownSource.create(
        orientation_object_id=material["orientation_object_id"],
        orientation_object_version=material["orientation_object_version"],
        source_id=source["entry_id"],
        source_owner=source["source_owner"],
        source_ref=source["source_ref"],
        content=source["content"],
        confirmed_by=confirmation["confirmed_by"],
        confirmed_revision=confirmation["confirmed_revision"],
    )
    if (
        confirmed_source.source_revision != source["source_version"]
        or confirmed_source.content_sha256 != source["integrity_sha256"]
        or confirmed_source.confirmation_id != confirmation["confirmation_id"]
    ):
        _adapter_failure("confirmed_material_mapping")

    renderer = MarkdownStructuralRendererAlpha()
    projection = renderer.project(confirmed_source)
    representation = renderer.render(confirmed_source)
    if len(representation.elements) > MAX_ELEMENTS:
        _profile_failure("element_count")
    representation_check = validate_markdown_structural_representation(
        confirmed_source,
        representation,
        renderer=renderer,
    )
    if not representation_check.valid:
        _adapter_failure("representation_conformance")
    inventory = inventory_declared_source_elements(representation)
    summary = summarize_declared_structure(inventory)
    if not validate_structural_summary(inventory, summary).valid:
        _adapter_failure("structural_summary")
    statistics = measure_declared_structure(inventory)
    if not validate_structural_statistics(inventory, statistics).valid:
        _adapter_failure("structural_statistics")

    sequential = generate_sequential_relations(summary, statistics)
    if not validate_sequential_relation_set(summary, statistics, sequential).valid:
        _adapter_failure("sequential_relations")
    equality = generate_structural_equality_relations(summary, statistics)
    if not validate_structural_equality_relation_set(
        summary, statistics, equality
    ).valid:
        _adapter_failure("structural_equality")
    relation_set = generate_declared_reference_relations(
        summary,
        statistics,
        declarations=(),
    )
    if relation_set.relation_count > MAX_RELATIONS:
        _profile_failure("relation_count")
    if not validate_declared_reference_relation_set(
        summary,
        statistics,
        (),
        relation_set,
    ).valid:
        _adapter_failure("declared_references")
    relation_conformance = validate_relation_conformance(
        relation_set,
        summary,
        statistics,
    )
    if not relation_conformance.valid:
        _adapter_failure("relation_conformance")
    relations_certification = certify_relations(
        relation_set,
        relation_conformance,
        summary,
        statistics,
    )

    navigation = create_navigation_object(
        relation_set,
        relations_certification,
        summary,
        statistics,
    )
    constructed_navigation = construct_navigation(
        navigation,
        relation_set,
        relations_certification,
        summary,
        statistics,
    )
    navigation_conformance = validate_navigation_conformance(
        constructed_navigation,
        navigation,
        relation_set,
        relations_certification,
        summary,
        statistics,
    )
    if not navigation_conformance.valid:
        _adapter_failure("navigation_conformance")
    navigation_certification = certify_navigation(
        navigation,
        constructed_navigation,
        navigation_conformance,
        relation_set,
        relations_certification,
        summary,
        statistics,
    )

    orientation_map = create_orientation_map_object(
        navigation_certification,
        navigation,
        constructed_navigation,
        navigation_conformance,
        relation_set,
        relations_certification,
        summary,
        statistics,
    )
    constructed_map = construct_orientation_map(
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
    map_conformance = validate_orientation_map_conformance(
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
        _adapter_failure("orientation_map_conformance")
    slice_iii_certification = certify_slice_iii(
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

    expression_contract = create_expression_contract(
        slice_iii_certification,
        map_conformance,
        orientation_map,
        constructed_map,
        communicative_scope=COMMUNICATIVE_SCOPE,
        declared_lossiness=DECLARED_LOSSINESS,
        declared_exclusions=DECLARED_EXCLUSIONS,
    )
    if not validate_expression_contract(
        slice_iii_certification,
        map_conformance,
        orientation_map,
        constructed_map,
        expression_contract,
    ).valid:
        _adapter_failure("expression_contract")
    expression_artifact = construct_expression(expression_contract)
    expression_conformance = validate_expression_conformance(
        expression_contract,
        expression_artifact,
    )
    if not expression_conformance.valid:
        _adapter_failure("expression_conformance")
    expression_certification = certify_expression(expression_conformance)
    slice_iv_certification = certify_slice_iv(expression_certification)
    if slice_iv_certification.stop != TERMINAL_STOP:
        _adapter_failure("terminal_stop")

    artifact_specs: tuple[tuple[str, object, Callable[[Any], bytes]], ...] = (
        ("structural_representation", representation, canonical_representation_bytes),
        ("source_element_inventory", inventory, canonical_inventory_bytes),
        ("structural_summary", summary, canonical_structural_summary_bytes),
        ("structural_statistics", statistics, canonical_structural_statistics_bytes),
        ("sequential_relation_set", sequential, canonical_sequential_relation_set_bytes),
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
        ("navigation_object", navigation, canonical_navigation_object_bytes),
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
        ("orientation_map_object", orientation_map, canonical_orientation_map_object_bytes),
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
        ("expression_contract", expression_contract, canonical_expression_contract_bytes),
        ("expression_artifact", expression_artifact, canonical_expression_artifact_bytes),
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
        version = next(
            (
                getattr(artifact, name)
                for name in (
                    "schema_version",
                    "diagnostic_version",
                    "navigation_schema_version",
                    "orientation_map_schema_version",
                )
                if hasattr(artifact, name)
            ),
            "",
        )
        if not version:
            _adapter_failure(f"artifact_version:{kind}")
        entries.append(
            {
                "ordinal": ordinal,
                "artifact_kind": kind,
                "artifact_version": version,
                "artifact_ref": digest_ref(serialized),
                "canonical_byte_length": len(serialized),
                "body": json.loads(serialized.decode("utf-8")),
            }
        )
    if tuple(item["artifact_kind"] for item in entries) != EXPECTED_ARTIFACT_KINDS:
        _adapter_failure("artifact_order")
    manifest = {
        "schema_version": MANIFEST_SCHEMA,
        "artifact_count": len(entries),
        "artifacts": entries,
        "terminal_artifact_ref": entries[-1]["artifact_ref"],
    }
    if len(canonical_bytes(manifest)) > MAX_MANIFEST_BYTES:
        _profile_failure("manifest_size")
    if canonical_bytes(envelope) != input_before:
        _adapter_failure("input_mutation")
    # Projection is intentionally executed even though it is not manifested.
    if projection is None:
        _adapter_failure("projection_missing")
    return AdapterResult(
        artifact_manifest=manifest,
        terminal_certification_ref=entries[-1]["artifact_ref"],
        terminal_stop=TERMINAL_STOP,
        element_count=len(representation.elements),
        relation_count=relation_set.relation_count,
    )


def _adapter_failure(rule: str) -> None:
    raise RuntimeBoundaryError(
        status=500,
        category="core_invocation",
        code="core_invocation_failed",
        retry="manual_review",
        detail_refs=(rule,),
    )


def _profile_failure(rule: str) -> None:
    raise RuntimeBoundaryError(
        status=422,
        category="output_validation",
        code="operational_profile_exceeded",
        detail_refs=(rule,),
    )
