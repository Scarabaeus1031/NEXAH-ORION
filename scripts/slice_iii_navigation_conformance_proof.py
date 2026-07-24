#!/usr/bin/env python3
"""Replay the bounded WP20 External Navigation Conformance proof."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from orion.declared_cross_references_alpha import (  # noqa: E402
    canonical_declared_reference_relation_set_bytes,
)
from orion.navigation_conformance_alpha import (  # noqa: E402
    ACCEPTED,
    STOP_AFTER_NAVIGATION_CONFORMANCE,
    canonical_navigation_conformance_report_bytes,
    validate_navigation_conformance,
)
from orion.navigation_construction_alpha import (  # noqa: E402
    canonical_constructed_navigation_bytes,
)
from orion.navigation_object_alpha import (  # noqa: E402
    canonical_navigation_object_bytes,
)
from orion.relations_certification_alpha import (  # noqa: E402
    FROZEN_RELATIONS_CONTRACTS,
    canonical_relations_certification_report_bytes,
)
from orion.understand_structural_statistics_alpha import (  # noqa: E402
    canonical_structural_statistics_bytes,
)
from orion.understand_structural_summary_alpha import (  # noqa: E402
    canonical_structural_summary_bytes,
)

from slice_iii_navigation_construction_proof import (  # noqa: E402
    FIXTURE,
    FIXTURE_SHA256,
    WP17_SHA256,
    WP17_SOURCE,
    WP18_SHA256,
    WP18_SOURCE,
    build_wp19_artifacts,
)


WP19_SOURCE = ROOT / "src" / "orion" / "navigation_construction_alpha.py"
WP19_SHA256 = (
    "32f48449fe48f00b6b72d76142dee892a079962bcb47e1ed910d7950509b0336"
)


def _canonical_proof_bytes(proof: dict[str, object]) -> bytes:
    return json.dumps(
        proof,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def build_wp20_artifacts():
    """Build accepted WP19 inputs and observe them once."""

    artifacts = build_wp19_artifacts()
    artifacts["navigation_conformance"] = validate_navigation_conformance(
        artifacts["constructed_navigation"],
        artifacts["navigation"],
        artifacts["relation_set"],
        artifacts["certification"],
        artifacts["summary"],
        artifacts["statistics"],
    )
    return artifacts


def build_wp20_proof() -> tuple[dict[str, object], bool]:
    """Validate supplied Navigation artifacts, replay, and stop."""

    fixture_integrity_verified = (
        sha256(FIXTURE.read_bytes()).hexdigest() == FIXTURE_SHA256
    )
    artifacts = build_wp20_artifacts()
    constructed = artifacts["constructed_navigation"]
    navigation = artifacts["navigation"]
    relation_set = artifacts["relation_set"]
    certification = artifacts["certification"]
    summary = artifacts["summary"]
    statistics = artifacts["statistics"]
    report = artifacts["navigation_conformance"]

    inputs_before = (
        canonical_constructed_navigation_bytes(constructed),
        canonical_navigation_object_bytes(navigation),
        canonical_declared_reference_relation_set_bytes(relation_set),
        canonical_relations_certification_report_bytes(certification),
        canonical_structural_summary_bytes(summary),
        canonical_structural_statistics_bytes(statistics),
    )
    report_replay = validate_navigation_conformance(
        constructed,
        navigation,
        relation_set,
        certification,
        summary,
        statistics,
    )
    report_bytes = canonical_navigation_conformance_report_bytes(report)
    report_replay_bytes = canonical_navigation_conformance_report_bytes(
        report_replay
    )
    inputs_after = (
        canonical_constructed_navigation_bytes(constructed),
        canonical_navigation_object_bytes(navigation),
        canonical_declared_reference_relation_set_bytes(relation_set),
        canonical_relations_certification_report_bytes(certification),
        canonical_structural_summary_bytes(summary),
        canonical_structural_statistics_bytes(statistics),
    )

    frozen_dependencies = {
        contract.work_package: {
            "path": contract.source_path,
            "expected_sha256": contract.sha256,
            "actual_sha256": sha256(
                (ROOT / contract.source_path).read_bytes()
            ).hexdigest(),
        }
        for contract in FROZEN_RELATIONS_CONTRACTS
    }
    for work_package, path, expected in (
        ("WP17", WP17_SOURCE, WP17_SHA256),
        ("WP18", WP18_SOURCE, WP18_SHA256),
        ("WP19", WP19_SOURCE, WP19_SHA256),
    ):
        frozen_dependencies[work_package] = {
            "path": str(path.relative_to(ROOT)),
            "expected_sha256": expected,
            "actual_sha256": sha256(path.read_bytes()).hexdigest(),
        }
    frozen_dependencies_verified = all(
        item["actual_sha256"] == item["expected_sha256"]
        for item in frozen_dependencies.values()
    )
    downstream_execution = {
        "navigation_construction_by_conformance": False,
        "navigation_repair": False,
        "navigation_certification": False,
        "traversal": False,
        "route_computation": False,
        "graph_search": False,
        "orientation_map": False,
    }
    proof = {
        "proof": "wp20_external_navigation_conformance",
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
            "navigation_construction",
            "external_navigation_conformance",
            "stop",
        ),
        "fixture": {
            "path": str(FIXTURE.relative_to(ROOT)),
            "sha256": FIXTURE_SHA256,
            "integrity_verified": fixture_integrity_verified,
        },
        "frozen_dependencies": frozen_dependencies,
        "frozen_dependencies_verified": frozen_dependencies_verified,
        "conformance": {
            "report_id": report.report_id,
            "schema_version": report.schema_version,
            "construction_id": report.construction_id,
            "valid": report.valid,
            "decision": report.decision,
            "check_count": len(report.checks),
            "errors": report.errors,
            "accepted_construction_ref": (
                report.accepted_construction_ref
            ),
            "sha256": sha256(report_bytes).hexdigest(),
            "stop": report.stop,
        },
        "inputs_unchanged": inputs_before == inputs_after,
        "report_replay_byte_identical": (
            report_bytes == report_replay_bytes
        ),
        "provenance_verified": (
            "provenance_preservation" in report.checks
            and report.relations_certification_ref
            == constructed.provenance_ref
        ),
        "downstream_execution": downstream_execution,
        "stop": STOP_AFTER_NAVIGATION_CONFORMANCE,
    }
    successful = all(
        (
            fixture_integrity_verified,
            report.valid,
            report.decision == ACCEPTED,
            not report.errors,
            frozen_dependencies_verified,
            inputs_before == inputs_after,
            report_bytes == report_replay_bytes,
            proof["provenance_verified"],
            not any(downstream_execution.values()),
            proof["stop"] == STOP_AFTER_NAVIGATION_CONFORMANCE,
        )
    )
    proof["successful"] = successful
    return proof, successful


def main() -> int:
    proof, successful = build_wp20_proof()
    print(_canonical_proof_bytes(proof).decode("utf-8"))
    return 0 if successful else 1


if __name__ == "__main__":
    raise SystemExit(main())
