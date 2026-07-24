#!/usr/bin/env python3
"""Replay the bounded WP28 External Expression Conformance proof."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from orion.expression_conformance_alpha import (  # noqa: E402
    ACCEPTED,
    STOP_AFTER_EXPRESSION_CONFORMANCE,
    canonical_expression_conformance_report_bytes,
    validate_expression_conformance,
)
from orion.expression_construction_alpha import (  # noqa: E402
    canonical_expression_artifact_bytes,
)
from orion.expression_contract_alpha import (  # noqa: E402
    canonical_expression_contract_bytes,
)

from slice_iv_expression_construction_proof import (  # noqa: E402
    build_wp27_artifacts,
)


WP26_SOURCE = ROOT / "src" / "orion" / "expression_contract_alpha.py"
WP26_SHA256 = (
    "dff4030db357125e2dd3217157905c81b3ebfecb02d0915b849105b21e289c00"
)
WP27_SOURCE = ROOT / "src" / "orion" / "expression_construction_alpha.py"
WP27_SHA256 = (
    "50fccddf748ef8910bedb3b82c7a3ced8af263873b0aaf0e33409fa168d1f42f"
)


def _canonical_proof_bytes(proof: dict[str, object]) -> bytes:
    return json.dumps(
        proof,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def build_wp28_artifacts() -> dict[str, object]:
    """Build frozen WP26/WP27 inputs and one conformance report."""

    artifacts = build_wp27_artifacts()
    artifacts["expression_conformance"] = validate_expression_conformance(
        artifacts["expression_contract"],
        artifacts["expression_artifact"],
    )
    return artifacts


def build_wp28_proof() -> tuple[dict[str, object], bool]:
    """Observe exact Expression inputs, report, replay, and stop."""

    artifacts = build_wp28_artifacts()
    contract = artifacts["expression_contract"]
    artifact = artifacts["expression_artifact"]
    report = artifacts["expression_conformance"]
    inputs_before = (
        canonical_expression_contract_bytes(contract),
        canonical_expression_artifact_bytes(artifact),
    )
    replay = validate_expression_conformance(contract, artifact)
    report_bytes = canonical_expression_conformance_report_bytes(report)
    replay_bytes = canonical_expression_conformance_report_bytes(replay)
    inputs_after = (
        canonical_expression_contract_bytes(contract),
        canonical_expression_artifact_bytes(artifact),
    )
    frozen_sources = {
        "WP26": {
            "path": str(WP26_SOURCE.relative_to(ROOT)),
            "expected_sha256": WP26_SHA256,
            "actual_sha256": sha256(WP26_SOURCE.read_bytes()).hexdigest(),
        },
        "WP27": {
            "path": str(WP27_SOURCE.relative_to(ROOT)),
            "expected_sha256": WP27_SHA256,
            "actual_sha256": sha256(WP27_SOURCE.read_bytes()).hexdigest(),
        },
    }
    frozen_sources_verified = all(
        item["actual_sha256"] == item["expected_sha256"]
        for item in frozen_sources.values()
    )
    downstream_execution = {
        "expression_construction": False,
        "expression_certification": False,
        "vertical_slice_iv_certification": False,
        "language_generation": False,
        "lyra": False,
        "sirius": False,
        "runtime": False,
        "gateway": False,
        "presentation": False,
        "human_report": False,
    }
    proof = {
        "proof": "wp28_external_expression_conformance",
        "chain": (
            "expression_contract",
            "expression_artifact",
            "external_observation",
            "conformance_validation",
            "canonical_conformance_report",
            "after_expression_conformance",
            "stop",
        ),
        "frozen_sources": frozen_sources,
        "frozen_sources_verified": frozen_sources_verified,
        "conformance_report": {
            "report_id": report.report_id,
            "schema_version": report.schema_version,
            "expression_contract_id": report.expression_contract_id,
            "expression_id": report.expression_id,
            "valid": report.valid,
            "decision": report.decision,
            "checks": report.checks,
            "errors": report.errors,
            "accepted_expression_ref": report.accepted_expression_ref,
            "inputs_unchanged": report.inputs_unchanged,
            "sha256": sha256(report_bytes).hexdigest(),
            "stop": report.stop,
        },
        "inputs_unchanged": inputs_before == inputs_after,
        "report_replay_byte_identical": report_bytes == replay_bytes,
        "authority_references_verified": (
            report.expression_contract_id == contract.contract_id
            and report.expression_contract_integrity
            == contract.contract_integrity
            and report.expression_id == artifact.expression_id
            and report.expression_integrity == artifact.expression_integrity
        ),
        "provenance_verified": (
            artifact.provenance_ref == contract.provenance_ref
            and artifact.slice_iii_certification_ref
            == contract.slice_iii_certification_ref
        ),
        "downstream_execution": downstream_execution,
        "stop": STOP_AFTER_EXPRESSION_CONFORMANCE,
    }
    successful = all(
        (
            frozen_sources_verified,
            report.valid,
            report.decision == ACCEPTED,
            not report.errors,
            report.inputs_unchanged,
            inputs_before == inputs_after,
            report_bytes == replay_bytes,
            proof["authority_references_verified"],
            proof["provenance_verified"],
            not any(downstream_execution.values()),
            proof["stop"] == STOP_AFTER_EXPRESSION_CONFORMANCE,
        )
    )
    proof["successful"] = successful
    return proof, successful


def main() -> int:
    proof, successful = build_wp28_proof()
    print(_canonical_proof_bytes(proof).decode("utf-8"))
    return 0 if successful else 1


if __name__ == "__main__":
    raise SystemExit(main())
