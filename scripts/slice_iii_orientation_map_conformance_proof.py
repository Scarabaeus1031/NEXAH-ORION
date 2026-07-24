#!/usr/bin/env python3
"""Replay the bounded WP24 External Orientation Map Conformance proof."""

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
from orion.navigation_certification_alpha import (  # noqa: E402
    FROZEN_NAVIGATION_CONTRACTS,
    canonical_navigation_certification_report_bytes,
)
from orion.navigation_conformance_alpha import (  # noqa: E402
    canonical_navigation_conformance_report_bytes,
)
from orion.navigation_construction_alpha import (  # noqa: E402
    canonical_constructed_navigation_bytes,
)
from orion.navigation_object_alpha import (  # noqa: E402
    canonical_navigation_object_bytes,
)
from orion.orientation_map_conformance_alpha import (  # noqa: E402
    ACCEPTED,
    STOP_AFTER_ORIENTATION_MAP_CONFORMANCE,
    canonical_orientation_map_conformance_report_bytes,
    validate_orientation_map_conformance,
)
from orion.orientation_map_construction_alpha import (  # noqa: E402
    canonical_constructed_orientation_map_bytes,
)
from orion.orientation_map_object_alpha import (  # noqa: E402
    canonical_orientation_map_object_bytes,
)
from orion.relations_certification_alpha import (  # noqa: E402
    canonical_relations_certification_report_bytes,
)
from orion.understand_structural_statistics_alpha import (  # noqa: E402
    canonical_structural_statistics_bytes,
)
from orion.understand_structural_summary_alpha import (  # noqa: E402
    canonical_structural_summary_bytes,
)

from slice_iii_orientation_map_construction_proof import (  # noqa: E402
    FIXTURE,
    FIXTURE_SHA256,
    WP21_SHA256,
    WP21_SOURCE,
    WP22_SHA256,
    WP22_SOURCE,
    build_wp23_artifacts,
)


WP23_SOURCE = ROOT / "src" / "orion" / "orientation_map_construction_alpha.py"
WP23_SHA256 = (
    "0c6ea6001183d4feb8eee84779b1d0777"
    "1a0d85d15c00d77e1b5f580de43d1eb"
)


def _canonical_proof_bytes(proof: dict[str, object]) -> bytes:
    return json.dumps(
        proof,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _input_artifact_bytes(artifacts) -> tuple[bytes, ...]:
    return (
        canonical_orientation_map_object_bytes(
            artifacts["orientation_map_object"]
        ),
        canonical_constructed_orientation_map_bytes(
            artifacts["constructed_orientation_map"]
        ),
        canonical_navigation_certification_report_bytes(
            artifacts["navigation_certification"]
        ),
        canonical_navigation_object_bytes(artifacts["navigation"]),
        canonical_constructed_navigation_bytes(
            artifacts["constructed_navigation"]
        ),
        canonical_navigation_conformance_report_bytes(
            artifacts["navigation_conformance"]
        ),
        canonical_declared_reference_relation_set_bytes(
            artifacts["relation_set"]
        ),
        canonical_relations_certification_report_bytes(
            artifacts["certification"]
        ),
        canonical_structural_summary_bytes(artifacts["summary"]),
        canonical_structural_statistics_bytes(artifacts["statistics"]),
    )


def _validate(artifacts):
    return validate_orientation_map_conformance(
        artifacts["orientation_map_object"],
        artifacts["constructed_orientation_map"],
        artifacts["navigation_certification"],
        artifacts["navigation"],
        artifacts["constructed_navigation"],
        artifacts["navigation_conformance"],
        artifacts["relation_set"],
        artifacts["certification"],
        artifacts["summary"],
        artifacts["statistics"],
    )


def build_wp24_artifacts():
    """Build accepted WP23 inputs and observe them once."""

    artifacts = build_wp23_artifacts()
    artifacts["orientation_map_conformance"] = _validate(artifacts)
    return artifacts


def build_wp24_proof() -> tuple[dict[str, object], bool]:
    """Validate supplied Orientation Map artifacts, replay, and stop."""

    fixture_integrity_verified = (
        sha256(FIXTURE.read_bytes()).hexdigest() == FIXTURE_SHA256
    )
    artifacts = build_wp24_artifacts()
    report = artifacts["orientation_map_conformance"]
    inputs_before = _input_artifact_bytes(artifacts)
    replay = _validate(artifacts)
    report_bytes = canonical_orientation_map_conformance_report_bytes(report)
    replay_bytes = canonical_orientation_map_conformance_report_bytes(replay)
    inputs_after = _input_artifact_bytes(artifacts)

    frozen_dependencies = {
        contract.work_package: {
            "path": contract.source_path,
            "expected_sha256": contract.sha256,
            "actual_sha256": sha256(
                (ROOT / contract.source_path).read_bytes()
            ).hexdigest(),
        }
        for contract in FROZEN_NAVIGATION_CONTRACTS
    }
    for work_package, path, expected in (
        ("WP21", WP21_SOURCE, WP21_SHA256),
        ("WP22", WP22_SOURCE, WP22_SHA256),
        ("WP23", WP23_SOURCE, WP23_SHA256),
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
        "orientation_map_construction_by_conformance": False,
        "orientation_map_repair": False,
        "orientation_map_completion": False,
        "orientation_map_certification": False,
        "geometry": False,
        "layout": False,
        "rendering": False,
        "visualization": False,
        "route_computation": False,
        "traversal_execution": False,
        "semantic_interpretation": False,
    }
    proof = {
        "proof": "wp24_external_orientation_map_conformance",
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
            "navigation_certification",
            "orientation_map_object",
            "orientation_map_construction",
            "external_orientation_map_conformance",
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
            "orientation_map_id": report.orientation_map_id,
            "construction_id": report.construction_id,
            "valid": report.valid,
            "decision": report.decision,
            "check_count": len(report.checks),
            "errors": report.errors,
            "accepted_orientation_map_ref": (
                report.accepted_orientation_map_ref
            ),
            "accepted_construction_ref": report.accepted_construction_ref,
            "sha256": sha256(report_bytes).hexdigest(),
            "stop": report.stop,
        },
        "inputs_unchanged": inputs_before == inputs_after,
        "report_replay_byte_identical": report_bytes == replay_bytes,
        "provenance_verified": (
            "provenance_preservation" in report.checks
            and report.navigation_certification_ref
            == artifacts["constructed_orientation_map"].provenance_ref
        ),
        "downstream_execution": downstream_execution,
        "stop": STOP_AFTER_ORIENTATION_MAP_CONFORMANCE,
    }
    successful = all(
        (
            fixture_integrity_verified,
            report.valid,
            report.decision == ACCEPTED,
            not report.errors,
            frozen_dependencies_verified,
            inputs_before == inputs_after,
            report_bytes == replay_bytes,
            proof["provenance_verified"],
            not any(downstream_execution.values()),
            proof["stop"] == STOP_AFTER_ORIENTATION_MAP_CONFORMANCE,
        )
    )
    proof["successful"] = successful
    return proof, successful


def main() -> int:
    proof, successful = build_wp24_proof()
    print(_canonical_proof_bytes(proof).decode("utf-8"))
    return 0 if successful else 1


if __name__ == "__main__":
    raise SystemExit(main())
