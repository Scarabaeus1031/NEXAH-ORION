#!/usr/bin/env python3
"""Replay the bounded WP29 Expression Certification proof."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from orion.expression_certification_alpha import (  # noqa: E402
    CERTIFIED,
    STOP_AT_EXPRESSION_CERTIFIED,
    canonical_expression_certification_report_bytes,
    certify_expression,
)
from orion.expression_conformance_alpha import (  # noqa: E402
    canonical_expression_conformance_report_bytes,
)

from slice_iv_expression_conformance_proof import (  # noqa: E402
    build_wp28_artifacts,
)


WP28_SOURCE = ROOT / "src" / "orion" / "expression_conformance_alpha.py"
WP28_SHA256 = (
    "b452af1386362fdeaaac63a6b4dd1eaf3fc12f02247573a7d801afbe1cc8d805"
)


def _canonical_proof_bytes(proof: dict[str, object]) -> bytes:
    return json.dumps(
        proof,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def build_wp29_artifacts() -> dict[str, object]:
    """Build the accepted WP28 report and its immutable certification."""

    artifacts = build_wp28_artifacts()
    artifacts["expression_certification"] = certify_expression(
        artifacts["expression_conformance"]
    )
    return artifacts


def build_wp29_proof() -> tuple[dict[str, object], bool]:
    """Certify one accepted WP28 report, replay, and stop."""

    artifacts = build_wp29_artifacts()
    conformance = artifacts["expression_conformance"]
    certification = artifacts["expression_certification"]
    input_before = canonical_expression_conformance_report_bytes(conformance)
    replay = certify_expression(conformance)
    certification_bytes = canonical_expression_certification_report_bytes(
        certification
    )
    replay_bytes = canonical_expression_certification_report_bytes(replay)
    input_after = canonical_expression_conformance_report_bytes(conformance)
    actual_wp28_sha256 = sha256(WP28_SOURCE.read_bytes()).hexdigest()
    frozen_wp28_verified = actual_wp28_sha256 == WP28_SHA256
    downstream_execution = {
        "contract_reconstruction": False,
        "expression_construction": False,
        "expression_conformance": False,
        "vertical_slice_iv_certification": False,
        "language_generation": False,
        "lyra": False,
        "sirius": False,
        "runtime": False,
        "gateway": False,
        "applications": False,
        "presentation": False,
        "human_report": False,
    }
    proof = {
        "proof": "wp29_expression_certification",
        "chain": (
            "accepted_expression_conformance",
            "expression_certification",
            "canonical_certification_report",
            "at_expression_certified",
            "stop",
        ),
        "frozen_wp28": {
            "path": str(WP28_SOURCE.relative_to(ROOT)),
            "expected_sha256": WP28_SHA256,
            "actual_sha256": actual_wp28_sha256,
            "verified": frozen_wp28_verified,
        },
        "expression_certification": {
            "certification_id": certification.certification_id,
            "certification_integrity": (
                certification.certification_integrity
            ),
            "schema_version": certification.schema_version,
            "certification_version": certification.certification_version,
            "expression_conformance_report_id": (
                certification.expression_conformance_report_id
            ),
            "expression_conformance_report_integrity": (
                certification.expression_conformance_report_integrity
            ),
            "expression_ref": certification.expression_ref,
            "decision": certification.decision,
            "provenance_ref": certification.provenance_ref,
            "sha256": sha256(certification_bytes).hexdigest(),
            "stop": certification.stop,
        },
        "input_unchanged": input_before == input_after,
        "certification_replay_byte_identical": (
            certification_bytes == replay_bytes
        ),
        "wp28_references_verified": (
            certification.expression_conformance_report_id
            == conformance.report_id
            and certification.expression_conformance_report_integrity
            == sha256(input_before).hexdigest()
            and certification.expression_ref
            == conformance.accepted_expression_ref
        ),
        "provenance_preserved": (
            certification.provenance_ref
            == certification.expression_conformance_report_ref
        ),
        "downstream_execution": downstream_execution,
        "stop": STOP_AT_EXPRESSION_CERTIFIED,
    }
    successful = all(
        (
            frozen_wp28_verified,
            conformance.valid,
            certification.decision == CERTIFIED,
            input_before == input_after,
            certification_bytes == replay_bytes,
            proof["wp28_references_verified"],
            proof["provenance_preserved"],
            not any(downstream_execution.values()),
            proof["stop"] == STOP_AT_EXPRESSION_CERTIFIED,
        )
    )
    proof["successful"] = successful
    return proof, successful


def main() -> int:
    proof, successful = build_wp29_proof()
    print(_canonical_proof_bytes(proof).decode("utf-8"))
    return 0 if successful else 1


if __name__ == "__main__":
    raise SystemExit(main())
