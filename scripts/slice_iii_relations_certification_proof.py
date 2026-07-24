#!/usr/bin/env python3
"""Replay the bounded WP17 Relations Certification proof."""

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
from orion.relation_conformance_alpha import (  # noqa: E402
    canonical_relation_conformance_report_bytes,
    validate_relation_conformance,
)
from orion.relations_certification_alpha import (  # noqa: E402
    FROZEN_RELATIONS_CONTRACTS,
    PASSED,
    STOP_AT_RELATIONS_CERTIFIED,
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

from slice_ii_certification_proof import build_slice_ii_certification  # noqa: E402
from slice_iii_declared_cross_references_proof import build_wp15_proof  # noqa: E402
from slice_iii_relation_conformance_proof import build_wp16_proof  # noqa: E402
from slice_iii_relation_object_proof import build_wp12_proof  # noqa: E402
from slice_iii_sequential_relations_proof import build_wp13_proof  # noqa: E402
from slice_iii_structural_equality_proof import (  # noqa: E402
    FIXTURE,
    FIXTURE_SHA256,
    _confirmed_source,
    build_wp14_proof,
)


def _canonical_proof_bytes(proof: dict[str, object]) -> bytes:
    return json.dumps(
        proof,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _replay_proof(builder) -> dict[str, object]:
    first, first_success = builder()
    second, second_success = builder()
    first_bytes = _canonical_proof_bytes(first)
    second_bytes = _canonical_proof_bytes(second)
    return {
        "successful": first_success and second_success,
        "byte_identical": first_bytes == second_bytes,
        "sha256": sha256(first_bytes).hexdigest(),
    }


def build_wp17_proof() -> tuple[dict[str, object], bool]:
    """Replay WP12-WP16, certify supplied artifacts, and stop."""

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
    conformance_report = validate_relation_conformance(
        relation_set,
        summary,
        statistics,
    )

    relation_before = canonical_declared_reference_relation_set_bytes(
        relation_set
    )
    conformance_before = canonical_relation_conformance_report_bytes(
        conformance_report
    )
    summary_before = canonical_structural_summary_bytes(summary)
    statistics_before = canonical_structural_statistics_bytes(statistics)
    certification = certify_relations(
        relation_set,
        conformance_report,
        summary,
        statistics,
    )
    certification_replay = certify_relations(
        relation_set,
        conformance_report,
        summary,
        statistics,
    )
    relation_after = canonical_declared_reference_relation_set_bytes(
        relation_set
    )
    conformance_after = canonical_relation_conformance_report_bytes(
        conformance_report
    )
    summary_after = canonical_structural_summary_bytes(summary)
    statistics_after = canonical_structural_statistics_bytes(statistics)

    contract_fingerprints = {
        contract.work_package: {
            "path": contract.source_path,
            "expected_sha256": contract.sha256,
            "actual_sha256": sha256(
                (ROOT / contract.source_path).read_bytes()
            ).hexdigest(),
        }
        for contract in FROZEN_RELATIONS_CONTRACTS
    }
    frozen_contracts_verified = all(
        record["actual_sha256"] == record["expected_sha256"]
        for record in contract_fingerprints.values()
    )
    package_proof_replays = {
        "WP12": _replay_proof(build_wp12_proof),
        "WP13": _replay_proof(build_wp13_proof),
        "WP14": _replay_proof(build_wp14_proof),
        "WP15": _replay_proof(build_wp15_proof),
        "WP16": _replay_proof(build_wp16_proof),
    }
    package_proofs_verified = all(
        replay["successful"] and replay["byte_identical"]
        for replay in package_proof_replays.values()
    )
    slice_ii_first, slice_ii_first_success = build_slice_ii_certification()
    slice_ii_second, slice_ii_second_success = build_slice_ii_certification()
    slice_ii_replay = {
        "certified": (
            slice_ii_first_success
            and slice_ii_second_success
            and slice_ii_first.get("certified") is True
        ),
        "byte_identical": (
            _canonical_proof_bytes(slice_ii_first)
            == _canonical_proof_bytes(slice_ii_second)
        ),
        "stop": slice_ii_first.get("stop"),
    }
    certification_bytes = canonical_relations_certification_report_bytes(
        certification
    )
    certification_replay_bytes = (
        canonical_relations_certification_report_bytes(certification_replay)
    )
    inputs_unchanged = (
        relation_before == relation_after
        and conformance_before == conformance_after
        and summary_before == summary_after
        and statistics_before == statistics_after
    )
    downstream_execution = {
        "navigation_object": False,
        "navigation_traversal": False,
        "orientation_map": False,
        "semantic_validation": False,
        "relation_generation_by_certification": False,
        "relation_validation_by_certification": False,
    }
    proof = {
        "proof": "wp17_relations_certification",
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
        "slice_ii_certification_replay": slice_ii_replay,
        "package_proof_replays": package_proof_replays,
        "frozen_contracts": contract_fingerprints,
        "frozen_contracts_verified": frozen_contracts_verified,
        "certification": {
            "certification_id": certification.certification_id,
            "certification_integrity": (
                certification.certification_integrity
            ),
            "schema_version": certification.schema_version,
            "gate_id": certification.gate_id,
            "status": certification.status,
            "certified": certification.certified,
            "check_count": len(certification.checks),
            "errors": certification.errors,
            "relation_set_ref": certification.relation_set_ref,
            "conformance_report_ref": (
                certification.conformance_report_ref
            ),
            "sha256": sha256(certification_bytes).hexdigest(),
            "stop": certification.stop,
        },
        "inputs_unchanged": inputs_unchanged,
        "certification_replay_byte_identical": (
            certification_bytes == certification_replay_bytes
        ),
        "package_proofs_verified": package_proofs_verified,
        "downstream_execution": downstream_execution,
        "stop": STOP_AT_RELATIONS_CERTIFIED,
    }
    successful = all(
        (
            fixture_integrity_verified,
            representation_conformance.valid,
            summary_conformance.valid,
            statistics_conformance.valid,
            conformance_report.valid,
            certification.certified,
            certification.status == PASSED,
            certification.errors == (),
            inputs_unchanged,
            certification_bytes == certification_replay_bytes,
            frozen_contracts_verified,
            package_proofs_verified,
            slice_ii_replay["certified"],
            slice_ii_replay["byte_identical"],
            not any(downstream_execution.values()),
            proof["stop"] == STOP_AT_RELATIONS_CERTIFIED,
        )
    )
    proof["successful"] = successful
    return proof, successful


def main() -> int:
    proof, successful = build_wp17_proof()
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
