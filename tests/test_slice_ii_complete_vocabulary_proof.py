from __future__ import annotations

from dataclasses import FrozenInstanceError
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from orion.markdown_structural_renderer_alpha import (  # noqa: E402
    MarkdownStructuralRendererAlpha,
    canonical_representation_bytes,
)
from orion.understand_source_element_inventory_alpha import (  # noqa: E402
    canonical_inventory_bytes,
    inventory_declared_source_elements,
)
from slice_ii_complete_vocabulary_proof import (  # noqa: E402
    PROFILE_V1_VOCABULARY,
    STOP,
    _read_confirmed_source,
    build_complete_vocabulary_proof,
    canonical_proof_bytes,
)


class SliceIICompleteVocabularyProofTests(unittest.TestCase):
    def test_complete_vocabulary_matrix_covers_every_frozen_kind(self) -> None:
        proof, valid = build_complete_vocabulary_proof()

        self.assertTrue(valid)
        matrix = proof["coverage_matrix"]
        self.assertEqual(
            tuple(row["block_kind"] for row in matrix),
            PROFILE_V1_VOCABULARY,
        )
        for row in matrix:
            self.assertTrue(row["projection"])
            self.assertTrue(row["representation"])
            self.assertTrue(row["external_conformance"])
            self.assertTrue(row["understand_inventory"])
            self.assertTrue(row["proof"])

    def test_proof_preserves_identity_provenance_order_and_stop(self) -> None:
        proof, valid = build_complete_vocabulary_proof()

        self.assertTrue(valid)
        self.assertTrue(all(proof["verification"].values()))
        self.assertTrue(proof["complete_vocabulary_verified"])
        self.assertEqual(proof["stop"], STOP)
        self.assertEqual(
            proof["understand_boundary"]["input"],
            "immutable_structural_representation",
        )
        self.assertFalse(
            any(
                value
                for key, value in proof["understand_boundary"].items()
                if key != "input"
            )
        )
        self.assertFalse(any(proof["downstream_execution"].values()))

    def test_representation_and_inventory_remain_immutable(self) -> None:
        source = _read_confirmed_source()
        representation = MarkdownStructuralRendererAlpha().render(source)
        inventory = inventory_declared_source_elements(representation)

        with self.assertRaises(FrozenInstanceError):
            representation.renderer_version = "changed"
        with self.assertRaises(FrozenInstanceError):
            inventory.responsibility_state = "changed"
        with self.assertRaises(FrozenInstanceError):
            representation.elements[0].ordinal = 1
        with self.assertRaises(FrozenInstanceError):
            inventory.elements[0].ordinal = 1

    def test_direct_replay_is_byte_identical(self) -> None:
        source = _read_confirmed_source()
        renderer = MarkdownStructuralRendererAlpha()
        first_representation = renderer.render(source)
        second_representation = renderer.render(source)
        first_inventory = inventory_declared_source_elements(first_representation)
        second_inventory = inventory_declared_source_elements(
            second_representation
        )
        first_proof, first_valid = build_complete_vocabulary_proof()
        second_proof, second_valid = build_complete_vocabulary_proof()

        self.assertTrue(first_valid and second_valid)
        self.assertEqual(
            canonical_representation_bytes(first_representation),
            canonical_representation_bytes(second_representation),
        )
        self.assertEqual(
            canonical_inventory_bytes(first_inventory),
            canonical_inventory_bytes(second_inventory),
        )
        self.assertEqual(
            canonical_proof_bytes(first_proof),
            canonical_proof_bytes(second_proof),
        )

    def test_executable_proof_replays_byte_identically(self) -> None:
        command = [
            sys.executable,
            str(ROOT / "scripts" / "slice_ii_complete_vocabulary_proof.py"),
        ]
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
        self.assertEqual(second.stderr, b"")
        self.assertEqual(first.stdout, second.stdout)
        replay = json.loads(first.stdout)
        self.assertTrue(replay["complete_vocabulary_verified"])
        self.assertEqual(replay["stop"], STOP)


if __name__ == "__main__":
    unittest.main()
