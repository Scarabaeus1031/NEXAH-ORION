#!/usr/bin/env python3
"""Replay the bounded WP27 Expression Construction proof."""

from __future__ import annotations

from dataclasses import asdict
from hashlib import sha256
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from orion.expression_construction_alpha import (  # noqa: E402
    STOP_AFTER_EXPRESSION_CONSTRUCTION,
    canonical_expression_artifact_bytes,
    construct_expression,
    expression_artifact_from_dict,
)
from orion.expression_contract_alpha import (  # noqa: E402
    canonical_expression_contract_bytes,
)

from slice_iv_expression_contract_proof import (  # noqa: E402
    build_wp26_artifacts,
)


WP26_SOURCE = ROOT / "src" / "orion" / "expression_contract_alpha.py"
WP26_SHA256 = (
    "dff4030db357125e2dd3217157905c81b3ebfecb02d0915b849105b21e289c00"
)


def _canonical_proof_bytes(proof: dict[str, object]) -> bytes:
    return json.dumps(
        proof,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def build_wp27_artifacts() -> dict[str, object]:
    """Build the frozen WP26 input and one immutable Expression Artifact."""

    artifacts = build_wp26_artifacts()
    artifacts["expression_artifact"] = construct_expression(
        artifacts["expression_contract"]
    )
    return artifacts


def build_wp27_proof() -> tuple[dict[str, object], bool]:
    """Construct, structurally validate, serialize, replay, and stop."""

    artifacts = build_wp27_artifacts()
    contract = artifacts["expression_contract"]
    artifact = artifacts["expression_artifact"]
    contract_bytes_before = canonical_expression_contract_bytes(contract)
    replay = construct_expression(contract)
    artifact_bytes = canonical_expression_artifact_bytes(artifact)
    replay_bytes = canonical_expression_artifact_bytes(replay)
    round_trip = expression_artifact_from_dict(asdict(artifact))
    contract_bytes_after = canonical_expression_contract_bytes(contract)
    frozen_wp26_verified = (
        sha256(WP26_SOURCE.read_bytes()).hexdigest() == WP26_SHA256
    )
    downstream_execution = {
        "external_expression_conformance": False,
        "expression_certification": False,
        "vertical_slice_iv_certification": False,
        "language_generation": False,
        "lyra": False,
        "sirius": False,
        "runtime": False,
        "gateway": False,
        "presentation": False,
        "html": False,
        "markdown_rendering": False,
        "graphics": False,
        "reports": False,
    }
    proof = {
        "proof": "wp27_expression_construction",
        "chain": (
            "at_expression_contract",
            "expression_construction",
            "construction_validation",
            "canonical_serialization",
            "after_expression_construction",
            "stop",
        ),
        "frozen_wp26": {
            "path": str(WP26_SOURCE.relative_to(ROOT)),
            "expected_sha256": WP26_SHA256,
            "actual_sha256": sha256(WP26_SOURCE.read_bytes()).hexdigest(),
            "verified": frozen_wp26_verified,
        },
        "expression_artifact": {
            "expression_id": artifact.expression_id,
            "expression_integrity": artifact.expression_integrity,
            "schema_version": artifact.schema_version,
            "expression_contract_id": artifact.expression_contract_id,
            "expression_contract_ref": artifact.expression_contract_ref,
            "orientation_map_id": artifact.orientation_map_id,
            "orientation_map_construction_id": (
                artifact.orientation_map_construction_id
            ),
            "communicative_scope": artifact.communicative_scope,
            "declared_lossiness": artifact.declared_lossiness,
            "declared_exclusions": artifact.declared_exclusions,
            "canonical_order": artifact.canonical_order,
            "construction_state": artifact.construction_state,
            "externally_conformant": artifact.externally_conformant,
            "sha256": sha256(artifact_bytes).hexdigest(),
            "stop": artifact.stop,
        },
        "construction_validation": {
            "strict_round_trip": round_trip == artifact,
            "identity_preserved": (
                artifact.expression_contract_id == contract.contract_id
                and artifact.expression_contract_integrity
                == contract.contract_integrity
            ),
            "scope_preserved": (
                artifact.communicative_scope
                == contract.communicative_scope
            ),
            "lossiness_preserved": (
                artifact.declared_lossiness == contract.declared_lossiness
            ),
            "exclusions_preserved": (
                artifact.declared_exclusions == contract.declared_exclusions
            ),
        },
        "contract_unchanged": contract_bytes_before == contract_bytes_after,
        "artifact_replay_byte_identical": artifact_bytes == replay_bytes,
        "provenance_preserved": (
            artifact.provenance_ref == contract.provenance_ref
            and artifact.slice_iii_certification_ref
            == contract.slice_iii_certification_ref
            and artifact.orientation_map_ref == contract.orientation_map_ref
            and artifact.orientation_map_construction_ref
            == contract.orientation_map_construction_ref
        ),
        "downstream_execution": downstream_execution,
        "stop": STOP_AFTER_EXPRESSION_CONSTRUCTION,
    }
    validation = proof["construction_validation"]
    successful = all(
        (
            frozen_wp26_verified,
            all(validation.values()),
            contract_bytes_before == contract_bytes_after,
            artifact_bytes == replay_bytes,
            proof["provenance_preserved"],
            not artifact.externally_conformant,
            not any(downstream_execution.values()),
            proof["stop"] == STOP_AFTER_EXPRESSION_CONSTRUCTION,
        )
    )
    proof["successful"] = successful
    return proof, successful


def main() -> int:
    proof, successful = build_wp27_proof()
    print(_canonical_proof_bytes(proof).decode("utf-8"))
    return 0 if successful else 1


if __name__ == "__main__":
    raise SystemExit(main())
