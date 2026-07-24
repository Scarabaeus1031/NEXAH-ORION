#!/usr/bin/env python3
"""Replay the bounded WP14 Structural Equality Relations proof."""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from orion.markdown_structural_renderer_alpha import (  # noqa: E402
    ConfirmedMarkdownSource,
    MarkdownStructuralRendererAlpha,
    canonical_representation_bytes,
    validate_markdown_structural_representation,
)
from orion.sequential_relations_alpha import (  # noqa: E402
    canonical_sequential_relation_set_bytes,
    generate_sequential_relations,
)
from orion.structural_equality_relations_alpha import (  # noqa: E402
    STOP_AFTER_STRUCTURAL_EQUALITY,
    STRUCTURAL_EQUALITY_KINDS,
    canonical_structural_equality_relation_set_bytes,
    generate_structural_equality_relations,
    validate_structural_equality_relation_set,
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


FIXTURE = (
    ROOT
    / "examples"
    / "markdown_structural_renderer_alpha"
    / "structural_equality.md"
)
FIXTURE_SHA256 = (
    "35bb487e7cf27681fa6321e49fd0c3a0a9ea0d6284787dff6b7406d4d758311a"
)


def _confirmed_source() -> ConfirmedMarkdownSource:
    source_bytes = FIXTURE.read_bytes()
    actual_sha256 = sha256(source_bytes).hexdigest()
    if actual_sha256 != FIXTURE_SHA256:
        raise ValueError(
            "Structural Equality fixture integrity mismatch: "
            f"expected {FIXTURE_SHA256}, received {actual_sha256}"
        )
    return ConfirmedMarkdownSource.create(
        orientation_object_id="orientation-object-structural-equality",
        orientation_object_version="1",
        source_id="markdown-source-structural-equality",
        source_owner="human-alpha-reviewer",
        source_ref=(
            "local:examples/markdown_structural_renderer_alpha/"
            "structural_equality.md"
        ),
        content=source_bytes.decode("utf-8", errors="strict"),
        confirmed_by="human-alpha-reviewer",
        confirmed_revision=1,
    )


def _artifact(value: bytes) -> dict[str, object]:
    return {
        "sha256": sha256(value).hexdigest(),
        "byte_length": len(value),
    }


def build_wp14_proof() -> tuple[dict[str, object], bool]:
    """Generate exact kind and heading-level equality, then stop."""

    source = _confirmed_source()
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
    sequential_set = generate_sequential_relations(summary, statistics)
    relation_set = generate_structural_equality_relations(summary, statistics)
    replay = generate_structural_equality_relations(summary, statistics)
    validation = validate_structural_equality_relation_set(
        summary,
        statistics,
        relation_set,
    )

    records = tuple(
        (
            span.ordinal,
            span.element_id,
            summary.ordered_element_kinds[span.ordinal],
        )
        for span in statistics.element_spans
    )
    expected_same_kind = tuple(
        (source_id, target_id)
        for source_index, (_, source_id, source_kind) in enumerate(records)
        for _, target_id, target_kind in records[source_index + 1 :]
        if source_kind == target_kind
    )
    headings = tuple(
        sorted(summary.declared_headings, key=lambda item: item.ordinal)
    )
    expected_same_level = tuple(
        (source_heading.element_id, target_heading.element_id)
        for source_index, source_heading in enumerate(headings)
        for target_heading in headings[source_index + 1 :]
        if source_heading.level == target_heading.level
    )
    equality_suffix = relation_set.relations[
        relation_set.sequential_relation_count :
    ]
    actual_same_kind = tuple(
        (relation.source_element_id, relation.target_element_id)
        for relation in equality_suffix
        if relation.relation_kind == "same_element_kind"
    )
    actual_same_level = tuple(
        (relation.source_element_id, relation.target_element_id)
        for relation in equality_suffix
        if relation.relation_kind == "same_heading_level"
    )
    relation_keys = tuple(
        (
            relation.relation_kind,
            relation.source_element_id,
            relation.target_element_id,
        )
        for relation in relation_set.relations
    )
    relation_set_bytes = canonical_structural_equality_relation_set_bytes(
        relation_set
    )
    replay_bytes = canonical_structural_equality_relation_set_bytes(replay)
    sequential_prefix_preserved = (
        relation_set.relations[: relation_set.sequential_relation_count]
        == sequential_set.relations
        and relation_set.sequential_relation_set_ref
        == "sha256:"
        + sha256(
            canonical_sequential_relation_set_bytes(sequential_set)
        ).hexdigest()
    )
    relation_objects_valid = all(
        validate_relation_object(summary, statistics, relation).valid
        for relation in relation_set.relations
    )
    relation_objects_replay = all(
        canonical_relation_object_bytes(first)
        == canonical_relation_object_bytes(second)
        for first, second in zip(relation_set.relations, replay.relations)
    )
    provenance_verified = (
        relation_set.structural_summary_ref
        == "sha256:"
        + sha256(canonical_structural_summary_bytes(summary)).hexdigest()
        and relation_set.structural_statistics_ref
        == "sha256:"
        + sha256(canonical_structural_statistics_bytes(statistics)).hexdigest()
        and relation_set.input_inventory_ref
        == summary.input_inventory_ref
        == statistics.input_inventory_ref
        and relation_objects_valid
    )
    kind_counts = Counter(
        relation.relation_kind for relation in relation_set.relations
    )
    forbidden_kinds_absent = not (
        set(kind_counts)
        & {"source_reference", "declared_cross_reference"}
    )
    downstream_execution = {
        "source_reference": False,
        "declared_cross_reference": False,
        "relation_graph": False,
        "navigation": False,
        "orientation_map": False,
        "semantic_interpretation": False,
        "hierarchy_inference": False,
    }
    proof = {
        "proof": "wp14_structural_equality_relations",
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
            "sequential_relation_set": _artifact(
                canonical_sequential_relation_set_bytes(sequential_set)
            ),
            "structural_equality_relation_set": _artifact(relation_set_bytes),
        },
        "relation_set": {
            "relation_set_id": relation_set.relation_set_id,
            "schema_version": relation_set.schema_version,
            "relation_count": relation_set.relation_count,
            "sequential_relation_count": relation_set.sequential_relation_count,
            "equality_relation_count": relation_set.equality_relation_count,
            "kind_counts": {
                kind: kind_counts[kind]
                for kind in (
                    "immediately_precedes",
                    "immediately_follows",
                    *STRUCTURAL_EQUALITY_KINDS,
                )
            },
            "stop": relation_set.stop,
        },
        "slice_ii_conformance": {
            "representation": representation_conformance.valid,
            "summary": summary_conformance.valid,
            "statistics": statistics_conformance.valid,
        },
        "validation": {
            "valid": validation.valid,
            "checks": validation.checks,
            "errors": validation.errors,
        },
        "same_element_kind_verified": actual_same_kind == expected_same_kind,
        "same_heading_level_verified": actual_same_level
        == expected_same_level,
        "symmetric_endpoint_order_verified": all(
            next(
                span.ordinal
                for span in statistics.element_spans
                if span.element_id == relation.source_element_id
            )
            < next(
                span.ordinal
                for span in statistics.element_spans
                if span.element_id == relation.target_element_id
            )
            for relation in equality_suffix
        ),
        "duplicates_absent": len(set(relation_keys)) == len(relation_keys),
        "canonical_order_verified": tuple(
            relation.canonical_order for relation in relation_set.relations
        )
        == tuple(range(relation_set.relation_count)),
        "sequential_prefix_preserved": sequential_prefix_preserved,
        "provenance_verified": provenance_verified,
        "relation_objects_replay_byte_identical": relation_objects_replay,
        "relation_set_replay_byte_identical": relation_set_bytes == replay_bytes,
        "forbidden_kinds_absent": forbidden_kinds_absent,
        "downstream_execution": downstream_execution,
        "stop": STOP_AFTER_STRUCTURAL_EQUALITY,
    }
    successful = all(
        (
            fixture_integrity_verified,
            representation_conformance.valid,
            summary_conformance.valid,
            statistics_conformance.valid,
            validation.valid,
            actual_same_kind == expected_same_kind,
            actual_same_level == expected_same_level,
            proof["symmetric_endpoint_order_verified"],
            proof["duplicates_absent"],
            proof["canonical_order_verified"],
            sequential_prefix_preserved,
            provenance_verified,
            relation_objects_replay,
            relation_set_bytes == replay_bytes,
            forbidden_kinds_absent,
            not any(downstream_execution.values()),
            proof["stop"] == STOP_AFTER_STRUCTURAL_EQUALITY,
        )
    )
    proof["successful"] = successful
    return proof, successful


def main() -> int:
    proof, successful = build_wp14_proof()
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
