#!/usr/bin/env python3
"""Replay the bounded WP19 Navigation Construction proof."""

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
from orion.navigation_construction_alpha import (  # noqa: E402
    ADJACENCY_RELATION_KINDS,
    STOP_AFTER_NAVIGATION_CONSTRUCTION,
    canonical_constructed_navigation_bytes,
    construct_navigation,
)
from orion.navigation_object_alpha import (  # noqa: E402
    canonical_navigation_object_bytes,
)
from orion.relations_certification_alpha import (  # noqa: E402
    FROZEN_RELATIONS_CONTRACTS,
    canonical_relations_certification_report_bytes,
)
from orion.structural_relation_alpha import (  # noqa: E402
    canonical_relation_object_bytes,
)
from orion.understand_structural_statistics_alpha import (  # noqa: E402
    canonical_structural_statistics_bytes,
)
from orion.understand_structural_summary_alpha import (  # noqa: E402
    canonical_structural_summary_bytes,
)

from slice_iii_navigation_object_proof import (  # noqa: E402
    FIXTURE,
    FIXTURE_SHA256,
    WP17_SHA256,
    WP17_SOURCE,
    build_wp18_artifacts,
)


WP18_SOURCE = ROOT / "src" / "orion" / "navigation_object_alpha.py"
WP18_SHA256 = (
    "d9c99cc09f041fc166739d3954818c1096d6028926d99125e5d17f9eb18b2036"
)


def _canonical_proof_bytes(proof: dict[str, object]) -> bytes:
    return json.dumps(
        proof,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def build_wp19_artifacts():
    """Build accepted WP18 inputs and the behavior-free WP19 output."""

    artifacts = build_wp18_artifacts()
    artifacts["constructed_navigation"] = construct_navigation(
        artifacts["navigation"],
        artifacts["relation_set"],
        artifacts["certification"],
        artifacts["summary"],
        artifacts["statistics"],
    )
    return artifacts


def build_wp19_proof() -> tuple[dict[str, object], bool]:
    """Construct ordered Navigation metadata, replay it, and stop."""

    fixture_integrity_verified = (
        sha256(FIXTURE.read_bytes()).hexdigest() == FIXTURE_SHA256
    )
    artifacts = build_wp19_artifacts()
    navigation = artifacts["navigation"]
    relation_set = artifacts["relation_set"]
    certification = artifacts["certification"]
    summary = artifacts["summary"]
    statistics = artifacts["statistics"]
    constructed = artifacts["constructed_navigation"]

    inputs_before = (
        canonical_navigation_object_bytes(navigation),
        canonical_declared_reference_relation_set_bytes(relation_set),
        canonical_relations_certification_report_bytes(certification),
        canonical_structural_summary_bytes(summary),
        canonical_structural_statistics_bytes(statistics),
        tuple(
            canonical_relation_object_bytes(relation)
            for relation in relation_set.relations
        ),
    )
    replay = construct_navigation(
        navigation,
        relation_set,
        certification,
        summary,
        statistics,
    )
    constructed_bytes = canonical_constructed_navigation_bytes(constructed)
    replay_bytes = canonical_constructed_navigation_bytes(replay)
    inputs_after = (
        canonical_navigation_object_bytes(navigation),
        canonical_declared_reference_relation_set_bytes(relation_set),
        canonical_relations_certification_report_bytes(certification),
        canonical_structural_summary_bytes(summary),
        canonical_structural_statistics_bytes(statistics),
        tuple(
            canonical_relation_object_bytes(relation)
            for relation in relation_set.relations
        ),
    )

    expected_relation_refs = tuple(
        f"sha256:{sha256(canonical_relation_object_bytes(item)).hexdigest()}"
        for item in relation_set.relations
    )
    actual_relation_refs = tuple(
        entry.relation_ref for entry in constructed.entries
    )
    expected_adjacency_refs = tuple(
        expected_relation_refs[index]
        for index, relation in enumerate(relation_set.relations)
        if relation.relation_kind in ADJACENCY_RELATION_KINDS
    )
    actual_adjacency_refs = tuple(
        entry.structural_adjacency_ref
        for entry in constructed.entries
        if entry.structural_adjacency_ref is not None
    )
    frozen_contracts = {
        contract.work_package: {
            "path": contract.source_path,
            "expected_sha256": contract.sha256,
            "actual_sha256": sha256(
                (ROOT / contract.source_path).read_bytes()
            ).hexdigest(),
        }
        for contract in FROZEN_RELATIONS_CONTRACTS
    }
    frozen_contracts["WP17"] = {
        "path": str(WP17_SOURCE.relative_to(ROOT)),
        "expected_sha256": WP17_SHA256,
        "actual_sha256": sha256(WP17_SOURCE.read_bytes()).hexdigest(),
    }
    frozen_contracts["WP18"] = {
        "path": str(WP18_SOURCE.relative_to(ROOT)),
        "expected_sha256": WP18_SHA256,
        "actual_sha256": sha256(WP18_SOURCE.read_bytes()).hexdigest(),
    }
    frozen_dependencies_verified = all(
        record["actual_sha256"] == record["expected_sha256"]
        for record in frozen_contracts.values()
    )
    downstream_execution = {
        "navigation_validation": False,
        "navigation_certification": False,
        "traversal": False,
        "route_generation": False,
        "path_finding": False,
        "graph_algorithms": False,
        "ranking": False,
        "recommendations": False,
        "orientation_map": False,
    }
    proof = {
        "proof": "wp19_navigation_construction",
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
            "stop",
        ),
        "fixture": {
            "path": str(FIXTURE.relative_to(ROOT)),
            "sha256": FIXTURE_SHA256,
            "integrity_verified": fixture_integrity_verified,
        },
        "frozen_dependencies": frozen_contracts,
        "frozen_dependencies_verified": frozen_dependencies_verified,
        "construction": {
            "construction_id": constructed.construction_id,
            "construction_integrity": constructed.construction_integrity,
            "schema_version": constructed.schema_version,
            "navigation_id": constructed.navigation_id,
            "relation_set_id": constructed.relation_set_id,
            "entry_count": constructed.entry_count,
            "adjacency_reference_count": len(actual_adjacency_refs),
            "sha256": sha256(constructed_bytes).hexdigest(),
            "state": constructed.construction_state,
            "externally_conformant": constructed.externally_conformant,
            "stop": constructed.stop,
        },
        "canonical_relation_order_preserved": (
            tuple(entry.canonical_order for entry in constructed.entries)
            == tuple(relation.canonical_order for relation in relation_set.relations)
            and tuple(entry.relation_id for entry in constructed.entries)
            == tuple(relation.relation_id for relation in relation_set.relations)
        ),
        "relation_references_exact": (
            actual_relation_refs == expected_relation_refs
        ),
        "adjacency_references_exact": (
            actual_adjacency_refs == expected_adjacency_refs
        ),
        "provenance_preserved": (
            constructed.provenance_ref
            == navigation.relations_certification_ref
            and all(
                entry.provenance_ref == relation.provenance.input_inventory_ref
                for entry, relation in zip(
                    constructed.entries,
                    relation_set.relations,
                    strict=True,
                )
            )
        ),
        "inputs_unchanged": inputs_before == inputs_after,
        "construction_replay_byte_identical": (
            constructed_bytes == replay_bytes
        ),
        "downstream_execution": downstream_execution,
        "stop": STOP_AFTER_NAVIGATION_CONSTRUCTION,
    }
    successful = all(
        (
            fixture_integrity_verified,
            certification.certified,
            frozen_dependencies_verified,
            proof["canonical_relation_order_preserved"],
            proof["relation_references_exact"],
            proof["adjacency_references_exact"],
            proof["provenance_preserved"],
            proof["inputs_unchanged"],
            proof["construction_replay_byte_identical"],
            not any(downstream_execution.values()),
            proof["stop"] == STOP_AFTER_NAVIGATION_CONSTRUCTION,
        )
    )
    proof["successful"] = successful
    return proof, successful


def main() -> int:
    proof, successful = build_wp19_proof()
    print(_canonical_proof_bytes(proof).decode("utf-8"))
    return 0 if successful else 1


if __name__ == "__main__":
    raise SystemExit(main())
