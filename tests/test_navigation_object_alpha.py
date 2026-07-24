"""Focused tests for the atomic WP18 Navigation Object contract."""

from __future__ import annotations

import ast
from dataclasses import FrozenInstanceError, asdict, fields
from hashlib import sha256
from pathlib import Path
import subprocess
import sys
import unittest

from orion.declared_cross_references_alpha import (
    canonical_declared_reference_relation_set_bytes,
)
from orion.navigation_object_alpha import (
    CONTRACT_STATE,
    NAVIGATION_SCHEMA_VERSION,
    RESPONSIBILITY,
    SERIALIZATION_VERSION,
    STOP_AFTER_NAVIGATION_OBJECT,
    NavigationObject,
    canonical_navigation_object_bytes,
    create_navigation_object,
    navigation_object_as_dict,
    navigation_object_from_dict,
)
from orion.relations_certification_alpha import (
    FROZEN_RELATIONS_CONTRACTS,
    canonical_relations_certification_report_bytes,
)
from orion.understand_structural_statistics_alpha import (
    canonical_structural_statistics_bytes,
)
from orion.understand_structural_summary_alpha import (
    canonical_structural_summary_bytes,
)


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from slice_iii_navigation_object_proof import (  # noqa: E402
    WP17_SHA256,
    WP17_SOURCE,
    build_wp18_artifacts,
    build_wp18_proof,
)


PROOF = ROOT / "scripts" / "slice_iii_navigation_object_proof.py"


def unsafe_replace(value: object, **changes: object) -> object:
    clone = object.__new__(type(value))
    for field in fields(value):
        object.__setattr__(
            clone,
            field.name,
            changes.get(field.name, getattr(value, field.name)),
        )
    return clone


class NavigationObjectAlphaTests(unittest.TestCase):
    def test_navigation_object_references_exact_certified_artifacts(self) -> None:
        artifacts = build_wp18_artifacts()
        navigation = artifacts["navigation"]
        relation_set = artifacts["relation_set"]
        certification = artifacts["certification"]
        summary = artifacts["summary"]
        statistics = artifacts["statistics"]

        self.assertIsInstance(navigation, NavigationObject)
        self.assertEqual(
            navigation.navigation_schema_version,
            NAVIGATION_SCHEMA_VERSION,
        )
        self.assertEqual(navigation.relation_set_id, relation_set.relation_set_id)
        self.assertEqual(
            navigation.relations_certification_id,
            certification.certification_id,
        )
        self.assertEqual(navigation.summary_id, summary.summary_id)
        self.assertEqual(navigation.statistics_id, statistics.statistics_id)
        self.assertEqual(
            navigation.provenance_ref,
            navigation.relations_certification_ref,
        )
        self.assertEqual(navigation.canonical_order, 0)
        self.assertEqual(navigation.serialization_version, SERIALIZATION_VERSION)
        self.assertEqual(navigation.responsibility, RESPONSIBILITY)
        self.assertEqual(navigation.contract_state, CONTRACT_STATE)
        self.assertFalse(navigation.externally_conformant)
        self.assertEqual(navigation.stop, STOP_AFTER_NAVIGATION_OBJECT)

    def test_navigation_object_is_immutable_and_strict(self) -> None:
        navigation = build_wp18_artifacts()["navigation"]
        payload = navigation_object_as_dict(navigation)

        with self.assertRaises(FrozenInstanceError):
            navigation.navigation_id = "navigation-" + "0" * 24
        self.assertEqual(navigation_object_from_dict(payload), navigation)
        with self.assertRaises(ValueError):
            navigation_object_from_dict({**payload, "routes": ()})

    def test_identity_and_serialization_replay_are_byte_identical(self) -> None:
        first = build_wp18_artifacts()
        second = build_wp18_artifacts()
        first_navigation = first["navigation"]
        second_navigation = second["navigation"]

        self.assertEqual(first_navigation, second_navigation)
        self.assertEqual(
            canonical_navigation_object_bytes(first_navigation),
            canonical_navigation_object_bytes(second_navigation),
        )

    def test_identity_tampering_is_rejected(self) -> None:
        navigation = build_wp18_artifacts()["navigation"]
        payload = navigation_object_as_dict(navigation)

        with self.assertRaises(ValueError):
            navigation_object_from_dict(
                {**payload, "navigation_id": "navigation-" + "0" * 24}
            )
        with self.assertRaises(ValueError):
            navigation_object_from_dict(
                {**payload, "navigation_integrity": "0" * 64}
            )

    def test_uncertified_relations_are_rejected(self) -> None:
        artifacts = build_wp18_artifacts()
        certification = unsafe_replace(
            artifacts["certification"],
            certified=False,
            status="failed",
            errors=("not certified",),
        )

        with self.assertRaises(ValueError):
            create_navigation_object(
                artifacts["relation_set"],
                certification,
                artifacts["summary"],
                artifacts["statistics"],
            )

    def test_inconsistent_artifact_lineage_is_rejected(self) -> None:
        artifacts = build_wp18_artifacts()
        certification = unsafe_replace(
            artifacts["certification"],
            relation_set_id="relation-set-" + "0" * 24,
        )

        with self.assertRaises(ValueError):
            create_navigation_object(
                artifacts["relation_set"],
                certification,
                artifacts["summary"],
                artifacts["statistics"],
            )

    def test_constructor_rejects_non_artifact_inputs(self) -> None:
        artifacts = build_wp18_artifacts()

        with self.assertRaises(TypeError):
            create_navigation_object(
                {},
                artifacts["certification"],
                artifacts["summary"],
                artifacts["statistics"],
            )

    def test_creation_does_not_modify_inputs(self) -> None:
        artifacts = build_wp18_artifacts()
        relation_set = artifacts["relation_set"]
        certification = artifacts["certification"]
        summary = artifacts["summary"]
        statistics = artifacts["statistics"]
        before = (
            canonical_declared_reference_relation_set_bytes(relation_set),
            canonical_relations_certification_report_bytes(certification),
            canonical_structural_summary_bytes(summary),
            canonical_structural_statistics_bytes(statistics),
        )

        create_navigation_object(
            relation_set,
            certification,
            summary,
            statistics,
        )
        after = (
            canonical_declared_reference_relation_set_bytes(relation_set),
            canonical_relations_certification_report_bytes(certification),
            canonical_structural_summary_bytes(summary),
            canonical_structural_statistics_bytes(statistics),
        )

        self.assertEqual(before, after)

    def test_object_contains_no_navigation_behavior_or_relation_copy(self) -> None:
        keys = set(asdict(build_wp18_artifacts()["navigation"]))

        self.assertFalse(
            keys
            & {
                "relations",
                "relation_catalog",
                "addresses",
                "transitions",
                "routes",
                "traversal",
                "paths",
                "graph",
                "ranking",
                "recommendations",
                "orientation_map",
            }
        )

    def test_module_imports_no_source_or_downstream_capability(self) -> None:
        path = ROOT / "src" / "orion" / "navigation_object_alpha.py"
        tree = ast.parse(path.read_text(encoding="utf-8"))
        modules = {
            node.module
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and node.module
        }
        prohibited = (
            "markdown_structural_renderer",
            "source_element_inventory",
            "navigation_traversal",
            "orientation_map",
            "gateway",
            "orientation_runtime",
            "lyra",
            "sirius",
        )

        self.assertFalse(
            any(
                fragment in module
                for module in modules
                for fragment in prohibited
            )
        )

    def test_module_calls_no_navigation_algorithm(self) -> None:
        path = ROOT / "src" / "orion" / "navigation_object_alpha.py"
        tree = ast.parse(path.read_text(encoding="utf-8"))
        called_names = {
            node.func.id
            for node in ast.walk(tree)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
        }
        prohibited = (
            "traverse",
            "route",
            "find_path",
            "search_graph",
            "rank",
            "recommend",
            "construct_orientation_map",
        )

        self.assertFalse(set(prohibited) & called_names)

    def test_frozen_relations_sources_match_certified_fingerprints(self) -> None:
        contracts = tuple(FROZEN_RELATIONS_CONTRACTS) + (
            unsafe_contract_wp17(),
        )
        for contract in contracts:
            with self.subTest(work_package=contract.work_package):
                self.assertEqual(
                    sha256((ROOT / contract.source_path).read_bytes()).hexdigest(),
                    contract.sha256,
                )

    def test_canonical_proof_creates_only_object_and_stops(self) -> None:
        proof, successful = build_wp18_proof()

        self.assertTrue(successful)
        self.assertTrue(proof["relations_certified"])
        self.assertTrue(proof["frozen_relations_verified"])
        self.assertTrue(proof["inputs_unchanged"])
        self.assertTrue(proof["navigation_replay_byte_identical"])
        self.assertFalse(any(proof["downstream_execution"].values()))
        self.assertEqual(proof["stop"], STOP_AFTER_NAVIGATION_OBJECT)

    def test_executable_proof_replays_byte_identically(self) -> None:
        command = [sys.executable, str(PROOF)]
        first = subprocess.run(
            command,
            cwd=ROOT,
            check=False,
            capture_output=True,
        )
        second = subprocess.run(
            command,
            cwd=ROOT,
            check=False,
            capture_output=True,
        )

        self.assertEqual(first.returncode, 0, first.stderr.decode())
        self.assertEqual(second.returncode, 0, second.stderr.decode())
        self.assertEqual(first.stderr, b"")
        self.assertEqual(first.stdout, second.stdout)


def unsafe_contract_wp17():
    """Return the WP17 fingerprint in the frozen-contract test shape."""

    sample = FROZEN_RELATIONS_CONTRACTS[0]
    return type(sample)(
        work_package="WP17",
        component="Relations Certification",
        source_path=str(WP17_SOURCE.relative_to(ROOT)),
        sha256=WP17_SHA256,
    )


if __name__ == "__main__":
    unittest.main()
