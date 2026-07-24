#!/usr/bin/env python3
"""Replay the bounded WP15 Source and Declared Cross References proof."""

from __future__ import annotations

from collections import Counter
from dataclasses import replace
from hashlib import sha256
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from orion.declared_cross_references_alpha import (  # noqa: E402
    COMPLETE_RELATION_KIND_ORDER,
    STOP_AFTER_DECLARED_CROSS_REFERENCES,
    canonical_declared_cross_reference_bytes,
    canonical_declared_reference_relation_set_bytes,
    declared_cross_reference_from_explicit_values,
    generate_declared_reference_relations,
    validate_declared_reference_relation_set,
)
from orion.markdown_structural_renderer_alpha import (  # noqa: E402
    MarkdownStructuralRendererAlpha,
    canonical_representation_bytes,
    validate_markdown_structural_representation,
)
from orion.structural_equality_relations_alpha import (  # noqa: E402
    canonical_structural_equality_relation_set_bytes,
    generate_structural_equality_relations,
)
from orion.structural_relation_alpha import validate_relation_object  # noqa: E402
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

from slice_iii_structural_equality_proof import (  # noqa: E402
    FIXTURE,
    FIXTURE_SHA256,
    _confirmed_source,
)


def _artifact(value: bytes) -> dict[str, object]:
    return {
        "sha256": sha256(value).hexdigest(),
        "byte_length": len(value),
    }


def build_wp15_proof() -> tuple[dict[str, object], bool]:
    """Generate exact source and declared references, then stop."""

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
    wp14 = generate_structural_equality_relations(summary, statistics)

    empty_declaration_set = generate_declared_reference_relations(
        summary,
        statistics,
    )
    empty_replay = generate_declared_reference_relations(summary, statistics)
    empty_validation = validate_declared_reference_relation_set(
        summary,
        statistics,
        (),
        empty_declaration_set,
    )

    declaration = declared_cross_reference_from_explicit_values(
        declaration_version="1",
        source_element_id=statistics.element_spans[1].element_id,
        target_element_id=statistics.element_spans[3].element_id,
        provenance_ref=summary.input_inventory_ref,
    )
    declarations = (declaration,)
    declared_set = generate_declared_reference_relations(
        summary,
        statistics,
        declarations,
    )
    declared_replay = generate_declared_reference_relations(
        summary,
        statistics,
        declarations,
    )
    declared_validation = validate_declared_reference_relation_set(
        summary,
        statistics,
        declarations,
        declared_set,
    )

    element_ids = tuple(
        span.element_id for span in statistics.element_spans
    )
    source_relations = tuple(
        relation
        for relation in empty_declaration_set.relations
        if relation.relation_kind == "source_reference"
    )
    source_boundary_ids = {
        relation.target_element_id for relation in source_relations
    }
    source_reference_coverage = (
        tuple(relation.source_element_id for relation in source_relations)
        == element_ids
        and len(source_boundary_ids) == 1
        and all(
            relation.target_element_id
            == relation.provenance.source_boundary_id
            for relation in source_relations
        )
    )
    cross_relations = tuple(
        relation
        for relation in declared_set.relations
        if relation.relation_kind == "declared_cross_reference"
    )
    declaration_preserved = (
        len(cross_relations) == 1
        and cross_relations[0].source_element_id
        == declaration.source_element_id
        and cross_relations[0].target_element_id
        == declaration.target_element_id
        and declared_set.accepted_declaration_refs
        == (
            "sha256:"
            + sha256(
                canonical_declared_cross_reference_bytes(declaration)
            ).hexdigest(),
        )
    )
    prior_triples = {
        (
            relation.relation_kind,
            relation.source_element_id,
            relation.target_element_id,
        )
        for relation in wp14.relations
    }
    complete_prior_triples = {
        (
            relation.relation_kind,
            relation.source_element_id,
            relation.target_element_id,
        )
        for relation in declared_set.relations
        if relation.relation_kind
        not in {"source_reference", "declared_cross_reference"}
    }
    prior_relations_preserved = prior_triples == complete_prior_triples
    rank = {
        kind: index for index, kind in enumerate(COMPLETE_RELATION_KIND_ORDER)
    }
    deterministic_order_verified = (
        tuple(
            relation.canonical_order for relation in declared_set.relations
        )
        == tuple(range(declared_set.relation_count))
        and tuple(
            rank[relation.relation_kind]
            for relation in declared_set.relations
        )
        == tuple(
            sorted(
                rank[relation.relation_kind]
                for relation in declared_set.relations
            )
        )
    )
    relation_keys = tuple(
        (
            relation.relation_kind,
            relation.source_element_id,
            relation.target_element_id,
        )
        for relation in declared_set.relations
    )
    duplicates_absent = len(set(relation_keys)) == len(relation_keys)
    wp12_objects_valid = all(
        validate_relation_object(summary, statistics, relation).valid
        for relation in declared_set.relations
    )
    provenance_verified = (
        wp12_objects_valid
        and all(
            relation.provenance.input_inventory_ref
            == summary.input_inventory_ref
            for relation in declared_set.relations
        )
        and declaration.provenance_ref == summary.input_inventory_ref
    )
    undeclared_reference_rejected = False
    try:
        generate_declared_reference_relations(
            summary,
            statistics,
            (
                {
                    "source_element_id": statistics.element_spans[0].element_id,
                    "target_element_id": statistics.element_spans[2].element_id,
                },
            ),
        )
    except (TypeError, ValueError):
        undeclared_reference_rejected = True
    tampered_declaration_rejected = False
    try:
        generate_declared_reference_relations(
            summary,
            statistics,
            (
                replace(
                    declaration,
                    declaration_integrity="0" * 64,
                ),
            ),
        )
    except (TypeError, ValueError):
        tampered_declaration_rejected = True

    empty_bytes = canonical_declared_reference_relation_set_bytes(
        empty_declaration_set
    )
    declared_bytes = canonical_declared_reference_relation_set_bytes(
        declared_set
    )
    replay_byte_identical = (
        empty_bytes
        == canonical_declared_reference_relation_set_bytes(empty_replay)
        and declared_bytes
        == canonical_declared_reference_relation_set_bytes(declared_replay)
    )
    kind_counts = Counter(
        relation.relation_kind for relation in declared_set.relations
    )
    downstream_execution = {
        "external_relation_conformance": False,
        "relation_graph": False,
        "navigation": False,
        "orientation_map": False,
        "semantic_interpretation": False,
        "hierarchy_inference": False,
    }
    proof = {
        "proof": "wp15_declared_cross_references",
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
            "wp14_relation_set": _artifact(
                canonical_structural_equality_relation_set_bytes(wp14)
            ),
            "empty_declaration_relation_set": _artifact(empty_bytes),
            "declared_reference_relation_set": _artifact(declared_bytes),
            "accepted_declaration": _artifact(
                canonical_declared_cross_reference_bytes(declaration)
            ),
        },
        "complete_candidate": {
            "relation_set_id": declared_set.relation_set_id,
            "schema_version": declared_set.schema_version,
            "relation_count": declared_set.relation_count,
            "source_reference_count": declared_set.source_reference_count,
            "declared_cross_reference_count": (
                declared_set.declared_cross_reference_count
            ),
            "kind_counts": {
                kind: kind_counts[kind]
                for kind in COMPLETE_RELATION_KIND_ORDER
            },
            "stop": declared_set.stop,
        },
        "slice_ii_conformance": {
            "representation": representation_conformance.valid,
            "summary": summary_conformance.valid,
            "statistics": statistics_conformance.valid,
        },
        "candidate_validation": {
            "empty_declarations": empty_validation.valid,
            "one_declaration": declared_validation.valid,
        },
        "profile_v1_declared_cross_references_empty": (
            empty_declaration_set.declared_cross_reference_count == 0
        ),
        "source_reference_coverage_verified": source_reference_coverage,
        "declaration_preserved": declaration_preserved,
        "prior_relations_preserved": prior_relations_preserved,
        "deterministic_order_verified": deterministic_order_verified,
        "duplicates_absent": duplicates_absent,
        "provenance_verified": provenance_verified,
        "undeclared_reference_rejected": undeclared_reference_rejected,
        "tampered_declaration_rejected": tampered_declaration_rejected,
        "replay_byte_identical": replay_byte_identical,
        "downstream_execution": downstream_execution,
        "stop": STOP_AFTER_DECLARED_CROSS_REFERENCES,
    }
    successful = all(
        (
            fixture_integrity_verified,
            representation_conformance.valid,
            summary_conformance.valid,
            statistics_conformance.valid,
            empty_validation.valid,
            declared_validation.valid,
            proof["profile_v1_declared_cross_references_empty"],
            source_reference_coverage,
            declaration_preserved,
            prior_relations_preserved,
            deterministic_order_verified,
            duplicates_absent,
            provenance_verified,
            undeclared_reference_rejected,
            tampered_declaration_rejected,
            replay_byte_identical,
            not any(downstream_execution.values()),
            proof["stop"] == STOP_AFTER_DECLARED_CROSS_REFERENCES,
        )
    )
    proof["successful"] = successful
    return proof, successful


def main() -> int:
    proof, successful = build_wp15_proof()
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
