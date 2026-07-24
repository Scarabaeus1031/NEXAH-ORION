#!/usr/bin/env python3
"""Replay the bounded WP22 Orientation Map Object proof."""

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
from orion.orientation_map_object_alpha import (  # noqa: E402
    STOP_AFTER_ORIENTATION_MAP_OBJECT,
    canonical_orientation_map_object_bytes,
    create_orientation_map_object,
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

from slice_iii_navigation_certification_proof import (  # noqa: E402
    FIXTURE,
    FIXTURE_SHA256,
    build_wp21_artifacts,
)


WP21_SOURCE = ROOT / "src" / "orion" / "navigation_certification_alpha.py"
WP21_SHA256 = (
    "444aa58f06c4e6d8c11384a06b8dae0b1e9fbb666719f90c535b9780bff02e33"
)


def _canonical_proof_bytes(proof: dict[str, object]) -> bytes:
    return json.dumps(
        proof,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def build_wp22_artifacts():
    """Build accepted inputs and the atomic Orientation Map contract."""

    artifacts = build_wp21_artifacts()
    artifacts["orientation_map_object"] = create_orientation_map_object(
        artifacts["navigation_certification"],
        artifacts["navigation"],
        artifacts["constructed_navigation"],
        artifacts["navigation_conformance"],
        artifacts["relation_set"],
        artifacts["certification"],
        artifacts["summary"],
        artifacts["statistics"],
    )
    return artifacts


def build_wp22_proof() -> tuple[dict[str, object], bool]:
    """Create the Orientation Map Object, verify replay, and stop."""

    fixture_integrity_verified = (
        sha256(FIXTURE.read_bytes()).hexdigest() == FIXTURE_SHA256
    )
    artifacts = build_wp22_artifacts()
    navigation_certification = artifacts["navigation_certification"]
    navigation = artifacts["navigation"]
    constructed = artifacts["constructed_navigation"]
    navigation_conformance = artifacts["navigation_conformance"]
    relation_set = artifacts["relation_set"]
    relations_certification = artifacts["certification"]
    summary = artifacts["summary"]
    statistics = artifacts["statistics"]
    orientation_map = artifacts["orientation_map_object"]

    inputs_before = (
        canonical_navigation_certification_report_bytes(
            navigation_certification
        ),
        canonical_navigation_object_bytes(navigation),
        canonical_constructed_navigation_bytes(constructed),
        canonical_navigation_conformance_report_bytes(
            navigation_conformance
        ),
        canonical_declared_reference_relation_set_bytes(relation_set),
        canonical_relations_certification_report_bytes(
            relations_certification
        ),
        canonical_structural_summary_bytes(summary),
        canonical_structural_statistics_bytes(statistics),
    )
    replay = create_orientation_map_object(
        navigation_certification,
        navigation,
        constructed,
        navigation_conformance,
        relation_set,
        relations_certification,
        summary,
        statistics,
    )
    orientation_map_bytes = canonical_orientation_map_object_bytes(
        orientation_map
    )
    replay_bytes = canonical_orientation_map_object_bytes(replay)
    inputs_after = (
        canonical_navigation_certification_report_bytes(
            navigation_certification
        ),
        canonical_navigation_object_bytes(navigation),
        canonical_constructed_navigation_bytes(constructed),
        canonical_navigation_conformance_report_bytes(
            navigation_conformance
        ),
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
    frozen_contracts["WP21"] = {
        "path": str(WP21_SOURCE.relative_to(ROOT)),
        "expected_sha256": WP21_SHA256,
        "actual_sha256": sha256(WP21_SOURCE.read_bytes()).hexdigest(),
    }
    frozen_navigation_verified = all(
        item["actual_sha256"] == item["expected_sha256"]
        for item in frozen_contracts.values()
    )
    downstream_execution = {
        "orientation_map_construction": False,
        "orientation_map_conformance": False,
        "orientation_map_certification": False,
        "node_generation": False,
        "edge_generation": False,
        "layout": False,
        "coordinates": False,
        "visualization": False,
        "navigation_behavior": False,
    }
    proof = {
        "proof": "wp22_orientation_map_object",
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
            "stop",
        ),
        "fixture": {
            "path": str(FIXTURE.relative_to(ROOT)),
            "sha256": FIXTURE_SHA256,
            "integrity_verified": fixture_integrity_verified,
        },
        "frozen_navigation_contracts": frozen_contracts,
        "frozen_navigation_verified": frozen_navigation_verified,
        "orientation_map_object": {
            "orientation_map_id": orientation_map.orientation_map_id,
            "orientation_map_integrity": (
                orientation_map.orientation_map_integrity
            ),
            "schema_version": (
                orientation_map.orientation_map_schema_version
            ),
            "navigation_certification_id": (
                orientation_map.navigation_certification_id
            ),
            "navigation_object_id": orientation_map.navigation_object_id,
            "navigation_construction_id": (
                orientation_map.navigation_construction_id
            ),
            "navigation_conformance_id": (
                orientation_map.navigation_conformance_id
            ),
            "relation_set_id": orientation_map.relation_set_id,
            "provenance_ref": orientation_map.provenance_ref,
            "canonical_order": orientation_map.canonical_order,
            "serialization_version": orientation_map.serialization_version,
            "sha256": sha256(orientation_map_bytes).hexdigest(),
            "stop": orientation_map.stop,
        },
        "inputs_unchanged": inputs_before == inputs_after,
        "orientation_map_replay_byte_identical": (
            orientation_map_bytes == replay_bytes
        ),
        "provenance_preserved": (
            orientation_map.provenance_ref
            == orientation_map.navigation_certification_ref
            and orientation_map.navigation_certification_id
            == navigation_certification.certification_id
        ),
        "downstream_execution": downstream_execution,
        "stop": STOP_AFTER_ORIENTATION_MAP_OBJECT,
    }
    successful = all(
        (
            fixture_integrity_verified,
            navigation_certification.certified,
            frozen_navigation_verified,
            inputs_before == inputs_after,
            orientation_map_bytes == replay_bytes,
            proof["provenance_preserved"],
            not any(downstream_execution.values()),
            proof["stop"] == STOP_AFTER_ORIENTATION_MAP_OBJECT,
        )
    )
    proof["successful"] = successful
    return proof, successful


def main() -> int:
    proof, successful = build_wp22_proof()
    print(_canonical_proof_bytes(proof).decode("utf-8"))
    return 0 if successful else 1


if __name__ == "__main__":
    raise SystemExit(main())
