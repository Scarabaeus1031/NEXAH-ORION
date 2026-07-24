#!/usr/bin/env python3
"""Replay the bounded WP12 Relation Object proof."""

from __future__ import annotations

from dataclasses import asdict
from hashlib import sha256
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from orion.markdown_structural_renderer_alpha import (  # noqa: E402
    MarkdownStructuralRendererAlpha,
    canonical_representation_bytes,
    validate_markdown_structural_representation,
)
from orion.structural_relation_alpha import (  # noqa: E402
    STOP_AFTER_RELATION_OBJECT,
    canonical_relation_object_bytes,
    create_relation_object,
    validate_relation_object,
)
from orion.understand_source_element_inventory_alpha import (  # noqa: E402
    canonical_inventory_bytes,
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
from slice_ii_structural_statistics_proof import (  # noqa: E402
    FIXTURE,
    FIXTURE_SHA256,
    _full_source,
)


def _artifact(value: bytes) -> dict[str, object]:
    return {
        "sha256": sha256(value).hexdigest(),
        "byte_length": len(value),
    }


def build_wp12_proof() -> tuple[dict[str, object], bool]:
    """Build one explicit Relation Object and stop before relation generation."""

    source = _full_source()
    fixture_integrity_verified = (
        sha256(FIXTURE.read_bytes()).hexdigest() == FIXTURE_SHA256
    )
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

    source_element_id = statistics.element_spans[0].element_id
    target_element_id = statistics.element_spans[1].element_id
    relation = create_relation_object(
        summary,
        statistics,
        relation_kind="immediately_precedes",
        source_element_id=source_element_id,
        target_element_id=target_element_id,
        canonical_order=0,
    )
    relation_replay = create_relation_object(
        summary,
        statistics,
        relation_kind="immediately_precedes",
        source_element_id=source_element_id,
        target_element_id=target_element_id,
        canonical_order=0,
    )
    relation_validation = validate_relation_object(
        summary,
        statistics,
        relation,
    )

    representation_bytes = canonical_representation_bytes(representation)
    inventory_bytes = canonical_inventory_bytes(inventory)
    summary_bytes = canonical_structural_summary_bytes(summary)
    statistics_bytes = canonical_structural_statistics_bytes(statistics)
    relation_bytes = canonical_relation_object_bytes(relation)
    relation_replay_bytes = canonical_relation_object_bytes(relation_replay)

    provenance_verified = all(
        (
            relation.provenance.structural_summary_id == summary.summary_id,
            relation.provenance.structural_summary_ref
            == f"sha256:{sha256(summary_bytes).hexdigest()}",
            relation.provenance.structural_statistics_id
            == statistics.statistics_id,
            relation.provenance.structural_statistics_ref
            == f"sha256:{sha256(statistics_bytes).hexdigest()}",
            relation.provenance.input_inventory_ref
            == summary.input_inventory_ref
            == statistics.input_inventory_ref,
            relation.provenance.orientation_object_id
            == summary.orientation_object_id,
            relation.provenance.representation_id
            == summary.representation_id,
            relation.provenance.representation_integrity
            == summary.representation_integrity,
            relation.provenance.source_id == summary.source_id,
            relation.provenance.source_revision == summary.source_revision,
            relation.provenance.source_integrity == summary.source_integrity,
            relation.provenance.source_boundary == summary.source_boundary,
        )
    )
    downstream_execution = {
        "relation_generation": False,
        "relation_set": False,
        "graph_construction": False,
        "navigation": False,
        "orientation_map": False,
        "semantic_interpretation": False,
    }
    proof = {
        "proof": "wp12_relation_object",
        "schema_version": relation.schema_version,
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
            "stop",
        ),
        "fixture": {
            "path": str(FIXTURE.relative_to(ROOT)),
            "sha256": FIXTURE_SHA256,
            "integrity_verified": fixture_integrity_verified,
        },
        "artifacts": {
            "representation": _artifact(representation_bytes),
            "inventory": _artifact(inventory_bytes),
            "summary": _artifact(summary_bytes),
            "statistics": _artifact(statistics_bytes),
            "relation_object": _artifact(relation_bytes),
        },
        "relation_object": asdict(relation),
        "validation": {
            "valid": relation_validation.valid,
            "checks": relation_validation.checks,
            "errors": relation_validation.errors,
        },
        "slice_ii_conformance": {
            "representation": representation_conformance.valid,
            "summary": summary_conformance.valid,
            "statistics": statistics_conformance.valid,
        },
        "immutable": (
            getattr(type(relation), "__dataclass_params__").frozen
            and getattr(type(relation.provenance), "__dataclass_params__").frozen
        ),
        "provenance_verified": provenance_verified,
        "relation_replay_byte_identical": relation_bytes
        == relation_replay_bytes,
        "downstream_execution": downstream_execution,
        "stop": STOP_AFTER_RELATION_OBJECT,
    }
    successful = all(
        (
            fixture_integrity_verified,
            representation_conformance.valid,
            summary_conformance.valid,
            statistics_conformance.valid,
            relation_validation.valid,
            proof["immutable"],
            provenance_verified,
            relation_bytes == relation_replay_bytes,
            not any(downstream_execution.values()),
            proof["stop"] == STOP_AFTER_RELATION_OBJECT,
        )
    )
    proof["successful"] = successful
    return proof, successful


def main() -> int:
    proof, successful = build_wp12_proof()
    print(
        json.dumps(
            proof,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )
    )
    return 0 if successful else 1


if __name__ == "__main__":
    raise SystemExit(main())
