#!/usr/bin/env python3
"""Replay the bounded WP25 Vertical Slice III Certification proof."""

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
    canonical_orientation_map_conformance_report_bytes,
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
from orion.slice_iii_certification_alpha import (  # noqa: E402
    FROZEN_SLICE_III_CONTRACTS,
    PASSED,
    STOP_AT_SLICE_III_CERTIFIED,
    canonical_slice_iii_certification_report_bytes,
    certify_slice_iii,
)
from orion.understand_structural_statistics_alpha import (  # noqa: E402
    canonical_structural_statistics_bytes,
)
from orion.understand_structural_summary_alpha import (  # noqa: E402
    canonical_structural_summary_bytes,
)

from slice_iii_navigation_certification_proof import (  # noqa: E402
    build_wp21_proof,
)
from slice_iii_orientation_map_conformance_proof import (  # noqa: E402
    FIXTURE,
    FIXTURE_SHA256,
    build_wp24_artifacts,
    build_wp24_proof,
)
from slice_iii_relations_certification_proof import (  # noqa: E402
    build_wp17_proof,
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


def _input_artifact_bytes(artifacts) -> tuple[bytes, ...]:
    return (
        canonical_declared_reference_relation_set_bytes(
            artifacts["relation_set"]
        ),
        canonical_relations_certification_report_bytes(
            artifacts["certification"]
        ),
        canonical_navigation_object_bytes(artifacts["navigation"]),
        canonical_constructed_navigation_bytes(
            artifacts["constructed_navigation"]
        ),
        canonical_navigation_conformance_report_bytes(
            artifacts["navigation_conformance"]
        ),
        canonical_navigation_certification_report_bytes(
            artifacts["navigation_certification"]
        ),
        canonical_orientation_map_object_bytes(
            artifacts["orientation_map_object"]
        ),
        canonical_constructed_orientation_map_bytes(
            artifacts["constructed_orientation_map"]
        ),
        canonical_orientation_map_conformance_report_bytes(
            artifacts["orientation_map_conformance"]
        ),
        canonical_structural_summary_bytes(artifacts["summary"]),
        canonical_structural_statistics_bytes(artifacts["statistics"]),
    )


def _certify(artifacts):
    return certify_slice_iii(
        artifacts["relation_set"],
        artifacts["certification"],
        artifacts["navigation"],
        artifacts["constructed_navigation"],
        artifacts["navigation_conformance"],
        artifacts["navigation_certification"],
        artifacts["orientation_map_object"],
        artifacts["constructed_orientation_map"],
        artifacts["orientation_map_conformance"],
        artifacts["summary"],
        artifacts["statistics"],
    )


def build_wp25_artifacts():
    """Build the accepted WP24 inputs and observational certification."""

    artifacts = build_wp24_artifacts()
    artifacts["slice_iii_certification"] = _certify(artifacts)
    return artifacts


def build_wp25_proof() -> tuple[dict[str, object], bool]:
    """Certify Slice III replay, verify frozen contracts, and stop."""

    fixture_integrity_verified = (
        sha256(FIXTURE.read_bytes()).hexdigest() == FIXTURE_SHA256
    )
    artifacts = build_wp25_artifacts()
    certification = artifacts["slice_iii_certification"]
    inputs_before = _input_artifact_bytes(artifacts)
    replay = _certify(artifacts)
    certification_bytes = canonical_slice_iii_certification_report_bytes(
        certification
    )
    replay_bytes = canonical_slice_iii_certification_report_bytes(replay)
    inputs_after = _input_artifact_bytes(artifacts)

    frozen_contracts = {
        contract.work_package: {
            "path": contract.source_path,
            "expected_sha256": contract.sha256,
            "actual_sha256": sha256(
                (ROOT / contract.source_path).read_bytes()
            ).hexdigest(),
        }
        for contract in FROZEN_SLICE_III_CONTRACTS
    }
    frozen_contracts_verified = all(
        item["actual_sha256"] == item["expected_sha256"]
        for item in frozen_contracts.values()
    )
    certification_stage_replays = {
        "WP17": _replay_proof(build_wp17_proof),
        "WP21": _replay_proof(build_wp21_proof),
        "WP24": _replay_proof(build_wp24_proof),
    }
    certification_stages_verified = all(
        item["successful"] and item["byte_identical"]
        for item in certification_stage_replays.values()
    )
    downstream_execution = {
        "relations_execution": False,
        "navigation_execution": False,
        "orientation_map_construction": False,
        "orientation_map_validation": False,
        "traversal": False,
        "visualization": False,
        "slice_iv": False,
        "lyra": False,
        "sirius": False,
    }
    proof = {
        "proof": "wp25_vertical_slice_iii_certification",
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
            "vertical_slice_iii_certification",
            "stop",
        ),
        "fixture": {
            "path": str(FIXTURE.relative_to(ROOT)),
            "sha256": FIXTURE_SHA256,
            "integrity_verified": fixture_integrity_verified,
        },
        "frozen_contracts": frozen_contracts,
        "frozen_contracts_verified": frozen_contracts_verified,
        "certification_stage_replays": certification_stage_replays,
        "certification_stages_verified": certification_stages_verified,
        "certification": {
            "certification_id": certification.certification_id,
            "certification_integrity": certification.certification_integrity,
            "schema_version": certification.schema_version,
            "gate_id": certification.gate_id,
            "status": certification.status,
            "certified": certification.certified,
            "check_count": len(certification.checks),
            "errors": certification.errors,
            "sha256": sha256(certification_bytes).hexdigest(),
            "stop": certification.stop,
        },
        "inputs_unchanged": inputs_before == inputs_after,
        "certification_replay_byte_identical": (
            certification_bytes == replay_bytes
        ),
        "relations_replay_byte_identical": (
            certification.relations_replay_byte_identical
        ),
        "navigation_replay_byte_identical": (
            certification.navigation_replay_byte_identical
        ),
        "orientation_map_replay_byte_identical": (
            certification.orientation_map_replay_byte_identical
        ),
        "provenance_preserved": certification.provenance_preserved,
        "downstream_execution": downstream_execution,
        "stop": STOP_AT_SLICE_III_CERTIFIED,
    }
    successful = all(
        (
            fixture_integrity_verified,
            certification.certified,
            certification.status == PASSED,
            not certification.errors,
            frozen_contracts_verified,
            certification_stages_verified,
            inputs_before == inputs_after,
            certification_bytes == replay_bytes,
            certification.relations_replay_byte_identical,
            certification.navigation_replay_byte_identical,
            certification.orientation_map_replay_byte_identical,
            certification.provenance_preserved,
            not any(downstream_execution.values()),
            proof["stop"] == STOP_AT_SLICE_III_CERTIFIED,
        )
    )
    proof["successful"] = successful
    return proof, successful


def main() -> int:
    proof, successful = build_wp25_proof()
    print(_canonical_proof_bytes(proof).decode("utf-8"))
    return 0 if successful else 1


if __name__ == "__main__":
    raise SystemExit(main())
