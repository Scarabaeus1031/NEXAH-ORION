#!/usr/bin/env python3
"""Replay the bounded WP30 Vertical Slice IV Certification proof."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from orion.expression_certification_alpha import (  # noqa: E402
    canonical_expression_certification_report_bytes,
)
from orion.slice_iv_certification_alpha import (  # noqa: E402
    CERTIFIED,
    STOP_AT_SLICE_IV_CERTIFIED,
    canonical_slice_iv_certification_report_bytes,
    certify_slice_iv,
)

from slice_iv_expression_certification_proof import (  # noqa: E402
    build_wp29_artifacts,
)


FROZEN_SLICE_IV_SOURCES = (
    (
        "WP26",
        "src/orion/expression_contract_alpha.py",
        "dff4030db357125e2dd3217157905c81b3ebfecb02d0915b849105b21e289c00",
    ),
    (
        "WP27",
        "src/orion/expression_construction_alpha.py",
        "50fccddf748ef8910bedb3b82c7a3ced8af263873b0aaf0e33409fa168d1f42f",
    ),
    (
        "WP28",
        "src/orion/expression_conformance_alpha.py",
        "b452af1386362fdeaaac63a6b4dd1eaf3fc12f02247573a7d801afbe1cc8d805",
    ),
    (
        "WP29",
        "src/orion/expression_certification_alpha.py",
        "4f877dbc87592f32259f5537da04bedec2c4387813e6fa8df491d12f98873c7f",
    ),
)


def _canonical_proof_bytes(proof: dict[str, object]) -> bytes:
    return json.dumps(
        proof,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def build_wp30_artifacts() -> dict[str, object]:
    """Build the accepted WP29 input and its Slice IV certification."""

    artifacts = build_wp29_artifacts()
    artifacts["slice_iv_certification"] = certify_slice_iv(
        artifacts["expression_certification"]
    )
    return artifacts


def build_wp30_proof() -> tuple[dict[str, object], bool]:
    """Certify one WP29 report, verify frozen sources, and stop."""

    artifacts = build_wp30_artifacts()
    expression_certification = artifacts["expression_certification"]
    slice_certification = artifacts["slice_iv_certification"]
    input_before = canonical_expression_certification_report_bytes(
        expression_certification
    )
    replay = certify_slice_iv(expression_certification)
    certification_bytes = canonical_slice_iv_certification_report_bytes(
        slice_certification
    )
    replay_bytes = canonical_slice_iv_certification_report_bytes(replay)
    input_after = canonical_expression_certification_report_bytes(
        expression_certification
    )
    frozen_sources = {
        work_package: {
            "path": source_path,
            "expected_sha256": expected_sha256,
            "actual_sha256": sha256(
                (ROOT / source_path).read_bytes()
            ).hexdigest(),
        }
        for work_package, source_path, expected_sha256
        in FROZEN_SLICE_IV_SOURCES
    }
    frozen_sources_verified = all(
        observed["actual_sha256"] == observed["expected_sha256"]
        for observed in frozen_sources.values()
    )
    downstream_execution = {
        "contract_reconstruction": False,
        "expression_construction": False,
        "expression_conformance": False,
        "expression_recertification": False,
        "runtime": False,
        "gateway": False,
        "lyra": False,
        "sirius": False,
        "applications": False,
        "presentation": False,
        "language_generation": False,
        "semantic_interpretation": False,
    }
    proof = {
        "proof": "wp30_vertical_slice_iv_certification",
        "chain": (
            "expression_contract",
            "expression_construction",
            "external_expression_conformance",
            "expression_certification",
            "vertical_slice_iv_certification",
            "at_slice_iv_certified",
            "stop",
        ),
        "frozen_sources": frozen_sources,
        "frozen_sources_verified": frozen_sources_verified,
        "slice_iv_certification": {
            "certification_id": slice_certification.certification_id,
            "certification_integrity": (
                slice_certification.certification_integrity
            ),
            "schema_version": slice_certification.schema_version,
            "certification_version": (
                slice_certification.certification_version
            ),
            "expression_certification_id": (
                slice_certification.expression_certification_id
            ),
            "expression_certification_integrity": (
                slice_certification.expression_certification_integrity
            ),
            "decision": slice_certification.decision,
            "provenance_ref": slice_certification.provenance_ref,
            "sha256": sha256(certification_bytes).hexdigest(),
            "stop": slice_certification.stop,
        },
        "input_unchanged": input_before == input_after,
        "certification_replay_byte_identical": (
            certification_bytes == replay_bytes
        ),
        "wp29_references_verified": (
            slice_certification.expression_certification_id
            == expression_certification.certification_id
            and slice_certification.expression_certification_integrity
            == expression_certification.certification_integrity
            and slice_certification.provenance_ref
            == f"sha256:{sha256(input_before).hexdigest()}"
        ),
        "provenance_preserved": (
            slice_certification.provenance_ref
            == f"sha256:{sha256(input_before).hexdigest()}"
        ),
        "downstream_execution": downstream_execution,
        "stop": STOP_AT_SLICE_IV_CERTIFIED,
    }
    successful = all(
        (
            frozen_sources_verified,
            slice_certification.decision == CERTIFIED,
            input_before == input_after,
            certification_bytes == replay_bytes,
            proof["wp29_references_verified"],
            proof["provenance_preserved"],
            not any(downstream_execution.values()),
            proof["stop"] == STOP_AT_SLICE_IV_CERTIFIED,
        )
    )
    proof["successful"] = successful
    return proof, successful


def main() -> int:
    proof, successful = build_wp30_proof()
    print(_canonical_proof_bytes(proof).decode("utf-8"))
    return 0 if successful else 1


if __name__ == "__main__":
    raise SystemExit(main())
