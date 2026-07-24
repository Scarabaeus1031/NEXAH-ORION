#!/usr/bin/env python3
"""Replay the bounded WP21 Navigation Certification proof."""

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
    PASSED,
    STOP_AT_NAVIGATION_CERTIFIED,
    canonical_navigation_certification_report_bytes,
    certify_navigation,
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
from orion.relations_certification_alpha import (  # noqa: E402
    canonical_relations_certification_report_bytes,
)
from orion.understand_structural_statistics_alpha import (  # noqa: E402
    canonical_structural_statistics_bytes,
)
from orion.understand_structural_summary_alpha import (  # noqa: E402
    canonical_structural_summary_bytes,
)

from slice_iii_navigation_conformance_proof import (  # noqa: E402
    FIXTURE,
    FIXTURE_SHA256,
    build_wp20_artifacts,
    build_wp20_proof,
)
from slice_iii_navigation_construction_proof import build_wp19_proof  # noqa: E402
from slice_iii_navigation_object_proof import build_wp18_proof  # noqa: E402


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


def build_wp21_artifacts():
    """Build the accepted inputs and observational certification report."""

    artifacts = build_wp20_artifacts()
    artifacts["navigation_certification"] = certify_navigation(
        artifacts["navigation"],
        artifacts["constructed_navigation"],
        artifacts["navigation_conformance"],
        artifacts["relation_set"],
        artifacts["certification"],
        artifacts["summary"],
        artifacts["statistics"],
    )
    return artifacts


def build_wp21_proof() -> tuple[dict[str, object], bool]:
    """Certify WP18-WP20 replay, verify frozen contracts, and stop."""

    fixture_integrity_verified = (
        sha256(FIXTURE.read_bytes()).hexdigest() == FIXTURE_SHA256
    )
    artifacts = build_wp21_artifacts()
    navigation = artifacts["navigation"]
    constructed = artifacts["constructed_navigation"]
    conformance = artifacts["navigation_conformance"]
    relation_set = artifacts["relation_set"]
    relations_certification = artifacts["certification"]
    summary = artifacts["summary"]
    statistics = artifacts["statistics"]
    certification = artifacts["navigation_certification"]

    inputs_before = (
        canonical_navigation_object_bytes(navigation),
        canonical_constructed_navigation_bytes(constructed),
        canonical_navigation_conformance_report_bytes(conformance),
        canonical_declared_reference_relation_set_bytes(relation_set),
        canonical_relations_certification_report_bytes(
            relations_certification
        ),
        canonical_structural_summary_bytes(summary),
        canonical_structural_statistics_bytes(statistics),
    )
    certification_replay = certify_navigation(
        navigation,
        constructed,
        conformance,
        relation_set,
        relations_certification,
        summary,
        statistics,
    )
    certification_bytes = canonical_navigation_certification_report_bytes(
        certification
    )
    replay_bytes = canonical_navigation_certification_report_bytes(
        certification_replay
    )
    inputs_after = (
        canonical_navigation_object_bytes(navigation),
        canonical_constructed_navigation_bytes(constructed),
        canonical_navigation_conformance_report_bytes(conformance),
        canonical_declared_reference_relation_set_bytes(relation_set),
        canonical_relations_certification_report_bytes(
            relations_certification
        ),
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
        for contract in FROZEN_NAVIGATION_CONTRACTS
    }
    frozen_contracts_verified = all(
        item["actual_sha256"] == item["expected_sha256"]
        for item in frozen_contracts.values()
    )
    package_replays = {
        "WP18": _replay_proof(build_wp18_proof),
        "WP19": _replay_proof(build_wp19_proof),
        "WP20": _replay_proof(build_wp20_proof),
    }
    package_replays_verified = all(
        item["successful"] and item["byte_identical"]
        for item in package_replays.values()
    )
    downstream_execution = {
        "navigation_construction_by_certification": False,
        "navigation_validation_by_certification": False,
        "traversal": False,
        "route_computation": False,
        "orientation_map": False,
    }
    proof = {
        "proof": "wp21_navigation_certification",
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
            "stop",
        ),
        "fixture": {
            "path": str(FIXTURE.relative_to(ROOT)),
            "sha256": FIXTURE_SHA256,
            "integrity_verified": fixture_integrity_verified,
        },
        "frozen_navigation_contracts": frozen_contracts,
        "frozen_navigation_contracts_verified": (
            frozen_contracts_verified
        ),
        "package_proof_replays": package_replays,
        "package_proof_replays_verified": package_replays_verified,
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
            "navigation_ref": certification.navigation_ref,
            "construction_ref": certification.construction_ref,
            "conformance_report_ref": (
                certification.conformance_report_ref
            ),
            "sha256": sha256(certification_bytes).hexdigest(),
            "stop": certification.stop,
        },
        "inputs_unchanged": inputs_before == inputs_after,
        "certification_replay_byte_identical": (
            certification_bytes == replay_bytes
        ),
        "provenance_preserved": certification.provenance_preserved,
        "downstream_execution": downstream_execution,
        "stop": STOP_AT_NAVIGATION_CERTIFIED,
    }
    successful = all(
        (
            fixture_integrity_verified,
            certification.certified,
            certification.status == PASSED,
            not certification.errors,
            frozen_contracts_verified,
            package_replays_verified,
            inputs_before == inputs_after,
            certification_bytes == replay_bytes,
            certification.provenance_preserved,
            not any(downstream_execution.values()),
            proof["stop"] == STOP_AT_NAVIGATION_CERTIFIED,
        )
    )
    proof["successful"] = successful
    return proof, successful


def main() -> int:
    proof, successful = build_wp21_proof()
    print(_canonical_proof_bytes(proof).decode("utf-8"))
    return 0 if successful else 1


if __name__ == "__main__":
    raise SystemExit(main())
