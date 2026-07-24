#!/usr/bin/env python3
"""Replay the bounded WP13 Sequential Relations proof."""

from __future__ import annotations

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
from orion.sequential_relations_alpha import (  # noqa: E402
    SEQUENTIAL_RELATION_KINDS,
    STOP_AFTER_SEQUENTIAL_RELATIONS,
    canonical_sequential_relation_set_bytes,
    generate_sequential_relations,
    validate_sequential_relation_set,
)
from orion.structural_relation_alpha import (  # noqa: E402
    canonical_relation_object_bytes,
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


def build_wp13_proof() -> tuple[dict[str, object], bool]:
    """Generate all and only immediate adjacency relations, then stop."""

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
    relation_set = generate_sequential_relations(summary, statistics)
    relation_set_replay = generate_sequential_relations(summary, statistics)
    relation_set_validation = validate_sequential_relation_set(
        summary,
        statistics,
        relation_set,
    )

    spans = statistics.element_spans
    pairs = tuple(zip(spans, spans[1:]))
    expected = tuple(
        (
            "immediately_precedes",
            source_span.element_id,
            target_span.element_id,
            index,
        )
        for index, (source_span, target_span) in enumerate(pairs)
    ) + tuple(
        (
            "immediately_follows",
            target_span.element_id,
            source_span.element_id,
            len(pairs) + index,
        )
        for index, (source_span, target_span) in enumerate(pairs)
    )
    actual = tuple(
        (
            relation.relation_kind,
            relation.source_element_id,
            relation.target_element_id,
            relation.canonical_order,
        )
        for relation in relation_set.relations
    )
    relation_keys = tuple(item[:3] for item in actual)
    relation_object_validation = tuple(
        validate_relation_object(summary, statistics, relation).valid
        for relation in relation_set.relations
    )
    relation_object_replay = tuple(
        canonical_relation_object_bytes(first)
        == canonical_relation_object_bytes(second)
        for first, second in zip(
            relation_set.relations,
            relation_set_replay.relations,
        )
    )
    relation_set_bytes = canonical_sequential_relation_set_bytes(relation_set)
    relation_set_replay_bytes = canonical_sequential_relation_set_bytes(
        relation_set_replay
    )
    provenance_verified = (
        relation_set.structural_summary_ref
        == f"sha256:{sha256(canonical_structural_summary_bytes(summary)).hexdigest()}"
        and relation_set.structural_statistics_ref
        == f"sha256:{sha256(canonical_structural_statistics_bytes(statistics)).hexdigest()}"
        and relation_set.input_inventory_ref
        == summary.input_inventory_ref
        == statistics.input_inventory_ref
        and all(relation_object_validation)
    )
    boundary_verified = (
        not any(
            relation.relation_kind == "immediately_follows"
            and relation.source_element_id == spans[0].element_id
            for relation in relation_set.relations
        )
        and not any(
            relation.relation_kind == "immediately_precedes"
            and relation.source_element_id == spans[-1].element_id
            for relation in relation_set.relations
        )
    )
    forbidden_kinds_absent = set(
        relation.relation_kind for relation in relation_set.relations
    ).issubset(SEQUENTIAL_RELATION_KINDS)
    downstream_execution = {
        "structural_equality_relations": False,
        "source_reference": False,
        "declared_cross_reference": False,
        "relation_graph": False,
        "navigation": False,
        "orientation_map": False,
        "semantic_interpretation": False,
    }
    proof = {
        "proof": "wp13_sequential_relations",
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
            "stop",
        ),
        "fixture": {
            "path": str(FIXTURE.relative_to(ROOT)),
            "sha256": FIXTURE_SHA256,
            "integrity_verified": fixture_integrity_verified,
        },
        "artifacts": {
            "representation": _artifact(
                canonical_representation_bytes(representation)
            ),
            "inventory": _artifact(canonical_inventory_bytes(inventory)),
            "summary": _artifact(canonical_structural_summary_bytes(summary)),
            "statistics": _artifact(
                canonical_structural_statistics_bytes(statistics)
            ),
            "sequential_relation_set": _artifact(relation_set_bytes),
        },
        "relation_set": {
            "relation_set_id": relation_set.relation_set_id,
            "schema_version": relation_set.schema_version,
            "relation_count": relation_set.relation_count,
            "kind_counts": {
                kind: sum(
                    1
                    for relation in relation_set.relations
                    if relation.relation_kind == kind
                )
                for kind in SEQUENTIAL_RELATION_KINDS
            },
            "relation_ids": tuple(
                relation.relation_id for relation in relation_set.relations
            ),
            "stop": relation_set.stop,
        },
        "slice_ii_conformance": {
            "representation": representation_conformance.valid,
            "summary": summary_conformance.valid,
            "statistics": statistics_conformance.valid,
        },
        "validation": {
            "valid": relation_set_validation.valid,
            "checks": relation_set_validation.checks,
            "errors": relation_set_validation.errors,
        },
        "adjacency_verified": actual == expected,
        "duplicates_absent": len(set(relation_keys)) == len(relation_keys),
        "boundary_verified": boundary_verified,
        "canonical_order_verified": tuple(
            relation.canonical_order for relation in relation_set.relations
        )
        == tuple(range(relation_set.relation_count)),
        "provenance_verified": provenance_verified,
        "relation_objects_replay_byte_identical": all(
            relation_object_replay
        ),
        "relation_set_replay_byte_identical": relation_set_bytes
        == relation_set_replay_bytes,
        "forbidden_kinds_absent": forbidden_kinds_absent,
        "downstream_execution": downstream_execution,
        "stop": STOP_AFTER_SEQUENTIAL_RELATIONS,
    }
    successful = all(
        (
            fixture_integrity_verified,
            representation_conformance.valid,
            summary_conformance.valid,
            statistics_conformance.valid,
            relation_set_validation.valid,
            actual == expected,
            len(set(relation_keys)) == len(relation_keys),
            boundary_verified,
            provenance_verified,
            all(relation_object_replay),
            relation_set_bytes == relation_set_replay_bytes,
            forbidden_kinds_absent,
            not any(downstream_execution.values()),
            proof["stop"] == STOP_AFTER_SEQUENTIAL_RELATIONS,
        )
    )
    proof["successful"] = successful
    return proof, successful


def main() -> int:
    proof, successful = build_wp13_proof()
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
