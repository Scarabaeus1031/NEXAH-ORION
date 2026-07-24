#!/usr/bin/env python3
"""Replay the bounded WP16 External Relation Conformance proof."""

from __future__ import annotations

from dataclasses import fields
from hashlib import sha256
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

import orion.declared_cross_references_alpha as declared_reference_module  # noqa: E402
from orion.declared_cross_references_alpha import (  # noqa: E402
    declared_cross_reference_from_explicit_values,
    generate_declared_reference_relations,
)
from orion.markdown_structural_renderer_alpha import (  # noqa: E402
    MarkdownStructuralRendererAlpha,
    validate_markdown_structural_representation,
)
from orion.relation_conformance_alpha import (  # noqa: E402
    ACCEPTED,
    REJECTED,
    STOP_AFTER_RELATION_CONFORMANCE,
    canonical_relation_conformance_report_bytes,
    validate_relation_conformance,
)
from orion.understand_source_element_inventory_alpha import (  # noqa: E402
    inventory_declared_source_elements,
)
from orion.understand_structural_statistics_alpha import (  # noqa: E402
    measure_declared_structure,
    validate_structural_statistics,
)
from orion.understand_structural_summary_alpha import (  # noqa: E402
    summarize_declared_structure,
    validate_structural_summary,
)

from slice_iii_structural_equality_proof import (  # noqa: E402
    FIXTURE,
    FIXTURE_SHA256,
    _confirmed_source,
)


def _unsafe_replace(value: object, **changes: object) -> object:
    """Create test-only malformed input without invoking frozen constructors."""

    clone = object.__new__(type(value))
    for field in fields(value):
        object.__setattr__(
            clone,
            field.name,
            changes.get(field.name, getattr(value, field.name)),
        )
    return clone


def build_wp16_proof() -> tuple[dict[str, object], bool]:
    """Validate one candidate and canonical tamper matrix, then stop."""

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
    candidate_before = json.dumps(
        relation_set,
        default=lambda value: {
            field.name: getattr(value, field.name)
            for field in fields(value)
        },
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    report = validate_relation_conformance(relation_set, summary, statistics)
    replay = validate_relation_conformance(relation_set, summary, statistics)
    candidate_after = json.dumps(
        relation_set,
        default=lambda value: {
            field.name: getattr(value, field.name)
            for field in fields(value)
        },
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")

    complete_without_declarations = generate_declared_reference_relations(
        summary,
        statistics,
    )
    supplied_relations = complete_without_declarations.relations[:-1]
    subset_basis = declared_reference_module._set_identity_basis(
        structural_equality_relation_set_ref=(
            complete_without_declarations.structural_equality_relation_set_ref
        ),
        structural_summary_ref=(
            complete_without_declarations.structural_summary_ref
        ),
        structural_statistics_ref=(
            complete_without_declarations.structural_statistics_ref
        ),
        input_inventory_ref=(
            complete_without_declarations.input_inventory_ref
        ),
        accepted_declaration_refs=(),
        source_reference_count=(
            complete_without_declarations.source_reference_count
        ),
        declared_cross_reference_count=0,
        relations=supplied_relations,
    )
    supplied_subset = _unsafe_replace(
        complete_without_declarations,
        relation_set_id=(
            "relation-set-"
            + declared_reference_module._digest(subset_basis)[:24]
        ),
        relation_count=len(supplied_relations),
        relations=supplied_relations,
    )
    supplied_subset.__post_init__()
    subset_before = tuple(
        relation.relation_id for relation in supplied_subset.relations
    )
    subset_report = validate_relation_conformance(
        supplied_subset,
        summary,
        statistics,
    )
    completion_not_evaluated = (
        subset_report.valid
        and subset_before
        == tuple(
            relation.relation_id
            for relation in supplied_subset.relations
        )
    )

    duplicate_set = _unsafe_replace(
        relation_set,
        relations=relation_set.relations + (relation_set.relations[0],),
        relation_count=relation_set.relation_count + 1,
    )
    invalid_endpoint_relation = _unsafe_replace(
        relation_set.relations[0],
        target_element_id="element-000000000000000000000000",
    )
    invalid_endpoint_set = _unsafe_replace(
        relation_set,
        relations=(invalid_endpoint_relation,) + relation_set.relations[1:],
    )
    invalid_basis_relation = _unsafe_replace(
        relation_set.relations[0],
        target_element_id=statistics.element_spans[2].element_id,
    )
    invalid_basis_set = _unsafe_replace(
        relation_set,
        relations=(invalid_basis_relation,) + relation_set.relations[1:],
    )
    invalid_provenance = _unsafe_replace(
        relation_set.relations[0].provenance,
        source_id="tampered-source",
    )
    invalid_provenance_relation = _unsafe_replace(
        relation_set.relations[0],
        provenance=invalid_provenance,
    )
    invalid_provenance_set = _unsafe_replace(
        relation_set,
        relations=(invalid_provenance_relation,) + relation_set.relations[1:],
    )
    invalid_kind_relation = _unsafe_replace(
        relation_set.relations[0],
        relation_kind="semantic_similarity",
    )
    invalid_kind_set = _unsafe_replace(
        relation_set,
        relations=(invalid_kind_relation,) + relation_set.relations[1:],
    )
    reordered_set = _unsafe_replace(
        relation_set,
        relations=(
            relation_set.relations[1],
            relation_set.relations[0],
        )
        + relation_set.relations[2:],
    )
    tamper_inputs = (
        ("malformed_input", {"relations": ()}),
        ("duplicate_relation", duplicate_set),
        ("invalid_endpoint", invalid_endpoint_set),
        ("invalid_declared_basis", invalid_basis_set),
        ("invalid_provenance", invalid_provenance_set),
        ("invalid_relation_kind", invalid_kind_set),
        ("invalid_order", reordered_set),
    )
    tamper_reports = tuple(
        (
            name,
            validate_relation_conformance(value, summary, statistics),
            validate_relation_conformance(value, summary, statistics),
        )
        for name, value in tamper_inputs
    )
    tamper_matrix = {
        name: {
            "decision": first.decision,
            "valid": first.valid,
            "errors": first.errors,
            "replay_byte_identical": (
                canonical_relation_conformance_report_bytes(first)
                == canonical_relation_conformance_report_bytes(second)
            ),
        }
        for name, first, second in tamper_reports
    }
    tamper_matrix_rejected = all(
        not first.valid
        and first.decision == REJECTED
        and first.accepted_relation_set_ref is None
        and canonical_relation_conformance_report_bytes(first)
        == canonical_relation_conformance_report_bytes(second)
        for _, first, second in tamper_reports
    )
    report_bytes = canonical_relation_conformance_report_bytes(report)
    replay_bytes = canonical_relation_conformance_report_bytes(replay)
    downstream_execution = {
        "relations_certification": False,
        "navigation": False,
        "orientation_map": False,
        "semantic_validation": False,
    }
    proof = {
        "proof": "wp16_external_relation_conformance",
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
            "stop",
        ),
        "fixture": {
            "path": str(FIXTURE.relative_to(ROOT)),
            "sha256": FIXTURE_SHA256,
            "integrity_verified": fixture_integrity_verified,
        },
        "slice_ii_conformance": {
            "representation": representation_conformance.valid,
            "summary": summary_conformance.valid,
            "statistics": statistics_conformance.valid,
        },
        "relation_set": {
            "relation_set_id": relation_set.relation_set_id,
            "relation_count": relation_set.relation_count,
        },
        "conformance_report": {
            "report_id": report.report_id,
            "schema_version": report.schema_version,
            "decision": report.decision,
            "valid": report.valid,
            "accepted_relation_set_ref": report.accepted_relation_set_ref,
            "check_count": len(report.checks),
            "errors": report.errors,
            "stop": report.stop,
            "sha256": sha256(report_bytes).hexdigest(),
        },
        "candidate_unchanged": candidate_before == candidate_after,
        "completion_not_evaluated": completion_not_evaluated,
        "report_replay_byte_identical": report_bytes == replay_bytes,
        "tamper_matrix": tamper_matrix,
        "tamper_matrix_rejected": tamper_matrix_rejected,
        "downstream_execution": downstream_execution,
        "stop": STOP_AFTER_RELATION_CONFORMANCE,
    }
    successful = all(
        (
            fixture_integrity_verified,
            representation_conformance.valid,
            summary_conformance.valid,
            statistics_conformance.valid,
            report.valid,
            report.decision == ACCEPTED,
            report.accepted_relation_set_ref == report.relation_set_ref,
            report.input_unchanged,
            candidate_before == candidate_after,
            completion_not_evaluated,
            report_bytes == replay_bytes,
            tamper_matrix_rejected,
            not any(downstream_execution.values()),
            proof["stop"] == STOP_AFTER_RELATION_CONFORMANCE,
        )
    )
    proof["successful"] = successful
    return proof, successful


def main() -> int:
    proof, successful = build_wp16_proof()
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
