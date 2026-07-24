#!/usr/bin/env python3
"""Replay the bounded WP26 Expression Contract proof."""

from __future__ import annotations

from dataclasses import asdict
from hashlib import sha256
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from orion.expression_contract_alpha import (  # noqa: E402
    STOP_AT_EXPRESSION_CONTRACT,
    canonical_expression_contract_bytes,
    create_expression_contract,
    validate_expression_contract,
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
from orion.slice_iii_certification_alpha import (  # noqa: E402
    FROZEN_SLICE_III_CONTRACTS,
    canonical_slice_iii_certification_report_bytes,
)

from slice_iii_certification_proof import (  # noqa: E402
    FIXTURE,
    FIXTURE_SHA256,
    build_wp25_artifacts,
)


WP25_SOURCE = ROOT / "src" / "orion" / "slice_iii_certification_alpha.py"
WP25_SHA256 = (
    "59229e6abaa6f996e325a013edccf249711ab40f4cd3bec4b3dc91ea43a20168"
)
COMMUNICATIVE_SCOPE = (
    "canonical_order",
    "orientation_map_entries",
    "orientation_map_identity",
    "provenance",
    "structural_adjacency",
)
DECLARED_LOSSINESS = (
    "human_interpretation",
    "semantic_meaning",
    "visual_layout",
)
DECLARED_EXCLUSIONS = (
    "actions",
    "generated_language",
    "recommendations",
    "semantic_reasoning",
)


def _canonical_proof_bytes(proof: dict[str, object]) -> bytes:
    return json.dumps(
        proof,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _input_bytes(artifacts: dict[str, object]) -> tuple[bytes, ...]:
    return (
        canonical_slice_iii_certification_report_bytes(
            artifacts["slice_iii_certification"]
        ),
        canonical_orientation_map_conformance_report_bytes(
            artifacts["orientation_map_conformance"]
        ),
        canonical_orientation_map_object_bytes(
            artifacts["orientation_map_object"]
        ),
        canonical_constructed_orientation_map_bytes(
            artifacts["constructed_orientation_map"]
        ),
    )


def _create(artifacts: dict[str, object]):
    return create_expression_contract(
        artifacts["slice_iii_certification"],
        artifacts["orientation_map_conformance"],
        artifacts["orientation_map_object"],
        artifacts["constructed_orientation_map"],
        communicative_scope=COMMUNICATIVE_SCOPE,
        declared_lossiness=DECLARED_LOSSINESS,
        declared_exclusions=DECLARED_EXCLUSIONS,
    )


def build_wp26_artifacts() -> dict[str, object]:
    """Build certified Slice III inputs and the immutable WP26 contract."""

    artifacts = build_wp25_artifacts()
    artifacts["expression_contract"] = _create(artifacts)
    artifacts["expression_contract_validation"] = validate_expression_contract(
        artifacts["slice_iii_certification"],
        artifacts["orientation_map_conformance"],
        artifacts["orientation_map_object"],
        artifacts["constructed_orientation_map"],
        artifacts["expression_contract"],
    )
    return artifacts


def build_wp26_proof() -> tuple[dict[str, object], bool]:
    """Create, validate, serialize, replay, and stop at the contract."""

    fixture_integrity_verified = (
        sha256(FIXTURE.read_bytes()).hexdigest() == FIXTURE_SHA256
    )
    artifacts = build_wp26_artifacts()
    contract = artifacts["expression_contract"]
    validation = artifacts["expression_contract_validation"]
    inputs_before = _input_bytes(artifacts)
    replay = _create(artifacts)
    contract_bytes = canonical_expression_contract_bytes(contract)
    replay_bytes = canonical_expression_contract_bytes(replay)
    inputs_after = _input_bytes(artifacts)

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
    frozen_contracts["WP25"] = {
        "path": str(WP25_SOURCE.relative_to(ROOT)),
        "expected_sha256": WP25_SHA256,
        "actual_sha256": sha256(WP25_SOURCE.read_bytes()).hexdigest(),
    }
    frozen_slice_iii_verified = all(
        item["actual_sha256"] == item["expected_sha256"]
        for item in frozen_contracts.values()
    )
    downstream_execution = {
        "expression_construction": False,
        "expression_conformance": False,
        "expression_certification": False,
        "vertical_slice_iv_certification": False,
        "generated_language": False,
        "lyra": False,
        "sirius": False,
        "runtime": False,
        "gateway": False,
        "presentation": False,
    }
    proof = {
        "proof": "wp26_expression_contract",
        "chain": (
            "certified_slice_iii_stop",
            "expression_contract",
            "contract_validation",
            "canonical_serialization",
            "at_expression_contract",
            "stop",
        ),
        "fixture": {
            "path": str(FIXTURE.relative_to(ROOT)),
            "sha256": FIXTURE_SHA256,
            "integrity_verified": fixture_integrity_verified,
        },
        "frozen_slice_iii_contracts": frozen_contracts,
        "frozen_slice_iii_verified": frozen_slice_iii_verified,
        "expression_contract": {
            "contract_id": contract.contract_id,
            "contract_integrity": contract.contract_integrity,
            "schema_version": contract.schema_version,
            "contract_version": contract.contract_version,
            "slice_iii_certification_id": (
                contract.slice_iii_certification_id
            ),
            "orientation_map_conformance_id": (
                contract.orientation_map_conformance_id
            ),
            "orientation_map_id": contract.orientation_map_id,
            "orientation_map_construction_id": (
                contract.orientation_map_construction_id
            ),
            "communicative_scope": contract.communicative_scope,
            "declared_lossiness": contract.declared_lossiness,
            "declared_exclusions": contract.declared_exclusions,
            "sha256": sha256(contract_bytes).hexdigest(),
            "stop": contract.stop,
        },
        "validation": asdict(validation),
        "inputs_unchanged": inputs_before == inputs_after,
        "contract_replay_byte_identical": contract_bytes == replay_bytes,
        "provenance_preserved": (
            contract.provenance_ref
            == contract.slice_iii_certification_ref
            and contract.orientation_map_ref
            == artifacts["slice_iii_certification"].orientation_map_ref
            and contract.orientation_map_construction_ref
            == artifacts[
                "slice_iii_certification"
            ].orientation_map_construction_ref
        ),
        "downstream_execution": downstream_execution,
        "stop": STOP_AT_EXPRESSION_CONTRACT,
    }
    successful = all(
        (
            fixture_integrity_verified,
            artifacts["slice_iii_certification"].certified,
            frozen_slice_iii_verified,
            validation.valid,
            inputs_before == inputs_after,
            contract_bytes == replay_bytes,
            proof["provenance_preserved"],
            not any(downstream_execution.values()),
            proof["stop"] == STOP_AT_EXPRESSION_CONTRACT,
        )
    )
    proof["successful"] = successful
    return proof, successful


def main() -> int:
    proof, successful = build_wp26_proof()
    print(_canonical_proof_bytes(proof).decode("utf-8"))
    return 0 if successful else 1


if __name__ == "__main__":
    raise SystemExit(main())
