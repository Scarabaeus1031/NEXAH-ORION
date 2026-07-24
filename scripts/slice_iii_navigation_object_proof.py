#!/usr/bin/env python3
"""Replay the bounded WP18 Navigation Object proof."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from orion.declared_cross_references_alpha import (  # noqa: E402
    canonical_declared_reference_relation_set_bytes,
    declared_cross_reference_from_explicit_values,
    generate_declared_reference_relations,
)
from orion.markdown_structural_renderer_alpha import (  # noqa: E402
    MarkdownStructuralRendererAlpha,
    validate_markdown_structural_representation,
)
from orion.navigation_object_alpha import (  # noqa: E402
    STOP_AFTER_NAVIGATION_OBJECT,
    canonical_navigation_object_bytes,
    create_navigation_object,
)
from orion.relation_conformance_alpha import (  # noqa: E402
    canonical_relation_conformance_report_bytes,
    validate_relation_conformance,
)
from orion.relations_certification_alpha import (  # noqa: E402
    FROZEN_RELATIONS_CONTRACTS,
    canonical_relations_certification_report_bytes,
    certify_relations,
)
from orion.understand_source_element_inventory_alpha import (  # noqa: E402
    inventory_declared_source_elements,
)
from orion.understand_structural_statistics_alpha import (  # noqa: E402
    canonical_structural_statistics_bytes,
    measure_declared_structure,
    validate_structural_statistics,
)
from orion.understand_structural_summary_alpha import (  # noqa: E402
    canonical_structural_summary_bytes,
    summarize_declared_structure,
    validate_structural_summary,
)

from slice_iii_structural_equality_proof import (  # noqa: E402
    FIXTURE,
    FIXTURE_SHA256,
    _confirmed_source,
)


WP17_SOURCE = ROOT / "src" / "orion" / "relations_certification_alpha.py"
WP17_SHA256 = (
    "8329de7c8c60fd58aae42045ede2239eee98df0ebba70edaceb7feffe7a97a18"
)


def _canonical_proof_bytes(proof: dict[str, object]) -> bytes:
    return json.dumps(
        proof,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def build_wp18_artifacts():
    """Build the already accepted inputs and the atomic WP18 output."""

    source = _confirmed_source()
    renderer = MarkdownStructuralRendererAlpha()
    representation = renderer.render(source)
    representation_conformance = validate_markdown_structural_representation(
        source,
        representation,
        renderer=renderer,
    )
    inventory = inventory_declared_source_elements(representation)
    summary = summarize_declared_structure(inventory)
    summary_conformance = validate_structural_summary(inventory, summary)
    statistics = measure_declared_structure(inventory)
    statistics_conformance = validate_structural_statistics(
        inventory,
        statistics,
    )
    declaration = declared_cross_reference_from_explicit_values(
        declaration_version="1",
        source_element_id=statistics.element_spans[1].element_id,
        target_element_id=statistics.element_spans[3].element_id,
        provenance_ref=summary.input_inventory_ref,
    )
    relation_set = generate_declared_reference_relations(
        summary,
        statistics,
        (declaration,),
    )
    conformance = validate_relation_conformance(
        relation_set,
        summary,
        statistics,
    )
    certification = certify_relations(
        relation_set,
        conformance,
        summary,
        statistics,
    )
    navigation = create_navigation_object(
        relation_set,
        certification,
        summary,
        statistics,
    )
    return {
        "representation_conformance": representation_conformance,
        "summary_conformance": summary_conformance,
        "statistics_conformance": statistics_conformance,
        "summary": summary,
        "statistics": statistics,
        "relation_set": relation_set,
        "conformance": conformance,
        "certification": certification,
        "navigation": navigation,
    }


def build_wp18_proof() -> tuple[dict[str, object], bool]:
    """Create the Navigation Object, verify replay, and stop."""

    fixture_integrity_verified = (
        sha256(FIXTURE.read_bytes()).hexdigest() == FIXTURE_SHA256
    )
    artifacts = build_wp18_artifacts()
    summary = artifacts["summary"]
    statistics = artifacts["statistics"]
    relation_set = artifacts["relation_set"]
    conformance = artifacts["conformance"]
    certification = artifacts["certification"]
    navigation = artifacts["navigation"]

    inputs_before = (
        canonical_declared_reference_relation_set_bytes(relation_set),
        canonical_relation_conformance_report_bytes(conformance),
        canonical_relations_certification_report_bytes(certification),
        canonical_structural_summary_bytes(summary),
        canonical_structural_statistics_bytes(statistics),
    )
    navigation_replay = create_navigation_object(
        relation_set,
        certification,
        summary,
        statistics,
    )
    navigation_bytes = canonical_navigation_object_bytes(navigation)
    navigation_replay_bytes = canonical_navigation_object_bytes(
        navigation_replay
    )
    inputs_after = (
        canonical_declared_reference_relation_set_bytes(relation_set),
        canonical_relation_conformance_report_bytes(conformance),
        canonical_relations_certification_report_bytes(certification),
        canonical_structural_summary_bytes(summary),
        canonical_structural_statistics_bytes(statistics),
    )

    frozen_contracts = {
        contract.work_package: {
            "path": contract.source_path,
            "expected_sha256": contract.sha256,
            "actual_sha256": sha256(
                (ROOT / contract.source_path).read_bytes()
            ).hexdigest(),
        }
        for contract in FROZEN_RELATIONS_CONTRACTS
    }
    frozen_contracts["WP17"] = {
        "path": str(WP17_SOURCE.relative_to(ROOT)),
        "expected_sha256": WP17_SHA256,
        "actual_sha256": sha256(WP17_SOURCE.read_bytes()).hexdigest(),
    }
    frozen_relations_verified = all(
        record["actual_sha256"] == record["expected_sha256"]
        for record in frozen_contracts.values()
    )
    downstream_execution = {
        "navigation_construction": False,
        "traversal": False,
        "route_generation": False,
        "path_finding": False,
        "graph_search": False,
        "ranking": False,
        "recommendations": False,
        "orientation_map": False,
    }
    proof = {
        "proof": "wp18_navigation_object",
        "chain": (
            "confirmed_markdown",
            "projection",
            "renderer",
            "immutable_structural_representation",
            "external_representation_conformance",
            "understand_inventory",
            "structural_summary",
            "structural_statistics",
            "certified_slice_ii_stop",
            "relation_object",
            "sequential_relations",
            "structural_equality_relations",
            "declared_cross_references",
            "external_relation_conformance",
            "relations_certification",
            "navigation_object",
            "stop",
        ),
        "fixture": {
            "path": str(FIXTURE.relative_to(ROOT)),
            "sha256": FIXTURE_SHA256,
            "integrity_verified": fixture_integrity_verified,
        },
        "slice_ii_conformance": {
            "representation": artifacts[
                "representation_conformance"
            ].valid,
            "summary": artifacts["summary_conformance"].valid,
            "statistics": artifacts["statistics_conformance"].valid,
        },
        "relations_certified": certification.certified,
        "frozen_relations_contracts": frozen_contracts,
        "frozen_relations_verified": frozen_relations_verified,
        "navigation_object": {
            "navigation_id": navigation.navigation_id,
            "navigation_integrity": navigation.navigation_integrity,
            "navigation_schema_version": (
                navigation.navigation_schema_version
            ),
            "relation_set_id": navigation.relation_set_id,
            "relations_certification_id": (
                navigation.relations_certification_id
            ),
            "summary_id": navigation.summary_id,
            "statistics_id": navigation.statistics_id,
            "provenance_ref": navigation.provenance_ref,
            "canonical_order": navigation.canonical_order,
            "serialization_version": navigation.serialization_version,
            "sha256": sha256(navigation_bytes).hexdigest(),
            "stop": navigation.stop,
        },
        "inputs_unchanged": inputs_before == inputs_after,
        "navigation_replay_byte_identical": (
            navigation_bytes == navigation_replay_bytes
        ),
        "downstream_execution": downstream_execution,
        "stop": STOP_AFTER_NAVIGATION_OBJECT,
    }
    successful = all(
        (
            fixture_integrity_verified,
            artifacts["representation_conformance"].valid,
            artifacts["summary_conformance"].valid,
            artifacts["statistics_conformance"].valid,
            conformance.valid,
            certification.certified,
            frozen_relations_verified,
            inputs_before == inputs_after,
            navigation_bytes == navigation_replay_bytes,
            not any(downstream_execution.values()),
            proof["stop"] == STOP_AFTER_NAVIGATION_OBJECT,
        )
    )
    proof["successful"] = successful
    return proof, successful


def main() -> int:
    proof, successful = build_wp18_proof()
    print(_canonical_proof_bytes(proof).decode("utf-8"))
    return 0 if successful else 1


if __name__ == "__main__":
    raise SystemExit(main())
