#!/usr/bin/env python3
"""Replay the bounded WP23 Orientation Map Construction proof."""

from __future__ import annotations

from dataclasses import asdict
from hashlib import sha256
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

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
from orion.orientation_map_construction_alpha import (  # noqa: E402
    STOP_AFTER_ORIENTATION_MAP_CONSTRUCTION,
    canonical_constructed_orientation_map_bytes,
    construct_orientation_map,
)
from orion.orientation_map_object_alpha import (  # noqa: E402
    canonical_orientation_map_object_bytes,
)
from orion.declared_cross_references_alpha import (  # noqa: E402
    canonical_declared_reference_relation_set_bytes,
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

from slice_iii_orientation_map_object_proof import (  # noqa: E402
    FIXTURE,
    FIXTURE_SHA256,
    WP21_SHA256,
    WP21_SOURCE,
    build_wp22_artifacts,
)


WP22_SOURCE = ROOT / "src" / "orion" / "orientation_map_object_alpha.py"
WP22_SHA256 = (
    "6d743c773c813d3d56719f30fea66e78aa354f7665f2d4befdcc341aaa844fcb"
)


def _canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def build_wp23_artifacts():
    """Build accepted inputs and the deterministic structural map."""

    artifacts = build_wp22_artifacts()
    artifacts["constructed_orientation_map"] = construct_orientation_map(
        artifacts["orientation_map_object"],
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


def _input_artifact_bytes(artifacts) -> tuple[bytes, ...]:
    return (
        canonical_orientation_map_object_bytes(
            artifacts["orientation_map_object"]
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


def build_wp23_proof() -> tuple[dict[str, object], bool]:
    """Construct exact structural map entries, replay, and stop."""

    fixture_integrity_verified = (
        sha256(FIXTURE.read_bytes()).hexdigest() == FIXTURE_SHA256
    )
    artifacts = build_wp23_artifacts()
    orientation_map = artifacts["orientation_map_object"]
    navigation_certification = artifacts["navigation_certification"]
    constructed_navigation = artifacts["constructed_navigation"]
    constructed_map = artifacts["constructed_orientation_map"]

    inputs_before = _input_artifact_bytes(artifacts)
    replay = construct_orientation_map(
        orientation_map,
        navigation_certification,
        artifacts["navigation"],
        constructed_navigation,
        artifacts["navigation_conformance"],
        artifacts["relation_set"],
        artifacts["certification"],
        artifacts["summary"],
        artifacts["statistics"],
    )
    map_bytes = canonical_constructed_orientation_map_bytes(constructed_map)
    replay_bytes = canonical_constructed_orientation_map_bytes(replay)
    inputs_after = _input_artifact_bytes(artifacts)

    expected_navigation_refs = tuple(
        f"sha256:{sha256(_canonical_bytes(asdict(entry))).hexdigest()}"
        for entry in constructed_navigation.entries
    )
    actual_navigation_refs = tuple(
        entry.navigation_entry_ref for entry in constructed_map.entries
    )
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
    canonical_order_preserved = (
        tuple(entry.canonical_order for entry in constructed_map.entries)
        == tuple(
            entry.canonical_order for entry in constructed_navigation.entries
        )
        and tuple(
            entry.navigation_entry_id for entry in constructed_map.entries
        )
        == tuple(entry.entry_id for entry in constructed_navigation.entries)
    )
    structural_references_preserved = (
        actual_navigation_refs == expected_navigation_refs
        and tuple(entry.relation_ref for entry in constructed_map.entries)
        == tuple(entry.relation_ref for entry in constructed_navigation.entries)
        and tuple(
            entry.structural_adjacency_ref
            for entry in constructed_map.entries
        )
        == tuple(
            entry.structural_adjacency_ref
            for entry in constructed_navigation.entries
        )
    )
    downstream_execution = {
        "orientation_map_conformance": False,
        "orientation_map_certification": False,
        "coordinates": False,
        "geometry": False,
        "layout": False,
        "rendering": False,
        "visualization": False,
        "clustering": False,
        "route_computation": False,
        "semantic_neighborhoods": False,
    }
    proof = {
        "proof": "wp23_orientation_map_construction",
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
            "stop",
        ),
        "fixture": {
            "path": str(FIXTURE.relative_to(ROOT)),
            "sha256": FIXTURE_SHA256,
            "integrity_verified": fixture_integrity_verified,
        },
        "frozen_dependencies": frozen_dependencies,
        "frozen_dependencies_verified": frozen_dependencies_verified,
        "construction": {
            "construction_id": constructed_map.construction_id,
            "construction_integrity": constructed_map.construction_integrity,
            "schema_version": constructed_map.schema_version,
            "orientation_map_id": constructed_map.orientation_map_id,
            "navigation_certification_id": (
                constructed_map.navigation_certification_id
            ),
            "navigation_construction_id": (
                constructed_map.navigation_construction_id
            ),
            "entry_count": constructed_map.entry_count,
            "adjacency_reference_count": sum(
                entry.structural_adjacency_ref is not None
                for entry in constructed_map.entries
            ),
            "sha256": sha256(map_bytes).hexdigest(),
            "state": constructed_map.construction_state,
            "externally_conformant": constructed_map.externally_conformant,
            "stop": constructed_map.stop,
        },
        "canonical_navigation_order_preserved": canonical_order_preserved,
        "navigation_entry_references_exact": (
            actual_navigation_refs == expected_navigation_refs
        ),
        "structural_references_preserved": (
            structural_references_preserved
        ),
        "provenance_preserved": (
            constructed_map.provenance_ref
            == orientation_map.navigation_certification_ref
            and all(
                map_entry.provenance_ref == navigation_entry.provenance_ref
                for map_entry, navigation_entry in zip(
                    constructed_map.entries,
                    constructed_navigation.entries,
                    strict=True,
                )
            )
        ),
        "inputs_unchanged": inputs_before == inputs_after,
        "construction_replay_byte_identical": map_bytes == replay_bytes,
        "downstream_execution": downstream_execution,
        "stop": STOP_AFTER_ORIENTATION_MAP_CONSTRUCTION,
    }
    successful = all(
        (
            fixture_integrity_verified,
            navigation_certification.certified,
            frozen_dependencies_verified,
            canonical_order_preserved,
            actual_navigation_refs == expected_navigation_refs,
            structural_references_preserved,
            proof["provenance_preserved"],
            inputs_before == inputs_after,
            map_bytes == replay_bytes,
            not any(downstream_execution.values()),
            proof["stop"] == STOP_AFTER_ORIENTATION_MAP_CONSTRUCTION,
        )
    )
    proof["successful"] = successful
    return proof, successful


def main() -> int:
    proof, successful = build_wp23_proof()
    print(_canonical_bytes(proof).decode("utf-8"))
    return 0 if successful else 1


if __name__ == "__main__":
    raise SystemExit(main())
