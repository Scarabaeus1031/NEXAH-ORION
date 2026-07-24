#!/usr/bin/env python3
"""Prove complete deterministic coverage of the frozen Markdown vocabulary."""

from __future__ import annotations

from dataclasses import asdict
from hashlib import sha256
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from orion.markdown_structural_renderer_alpha import (  # noqa: E402
    ConfirmedMarkdownSource,
    MarkdownStructuralRendererAlpha,
    canonical_representation_bytes,
    validate_markdown_structural_representation,
)
from orion.understand_source_element_inventory_alpha import (  # noqa: E402
    canonical_inventory_bytes,
    inventory_declared_source_elements,
)


PROFILE_V1_VOCABULARY = (
    "document",
    "block_quote",
    "ordered_list",
    "unordered_list",
    "list_item",
    "atx_heading",
    "setext_heading",
    "paragraph",
    "thematic_break",
    "fenced_code_block",
    "indented_code_block",
)
FIXTURE = (
    ROOT
    / "examples"
    / "markdown_structural_renderer_alpha"
    / "complete_vocabulary.md"
)
FIXTURE_SHA256 = (
    "e44bcf3c8e93d7371318f22b459d75b0cf56d7e581ac5fa41ab855ee49ecc87d"
)
STOP = "after_complete_vocabulary_verification"


def _read_confirmed_source() -> ConfirmedMarkdownSource:
    fixture_bytes = FIXTURE.read_bytes()
    actual_sha256 = sha256(fixture_bytes).hexdigest()
    if actual_sha256 != FIXTURE_SHA256:
        raise ValueError(
            "complete-vocabulary fixture integrity mismatch: "
            f"expected {FIXTURE_SHA256}, received {actual_sha256}"
        )
    return ConfirmedMarkdownSource.create(
        orientation_object_id="orientation-object-complete-vocabulary",
        orientation_object_version="1",
        source_id="markdown-source-complete-vocabulary",
        source_owner="human-alpha-reviewer",
        source_ref=(
            "local:examples/markdown_structural_renderer_alpha/"
            "complete_vocabulary.md"
        ),
        content=fixture_bytes.decode("utf-8", errors="strict"),
        confirmed_by="human-alpha-reviewer",
        confirmed_revision=1,
    )


def build_complete_vocabulary_proof() -> tuple[dict[str, object], bool]:
    """Build the canonical WP8 proof without crossing its STOP boundary."""

    source = _read_confirmed_source()
    renderer = MarkdownStructuralRendererAlpha()
    mapping = renderer.project(source)
    representation = renderer.render(source)
    representation_replay = renderer.render(source)
    conformance = validate_markdown_structural_representation(
        source,
        representation,
        renderer=renderer,
    )
    inventory = inventory_declared_source_elements(representation)
    inventory_replay = inventory_declared_source_elements(representation)

    projected_kinds = tuple(block.element_kind for block in mapping.blocks)
    represented_kinds = tuple(
        element.element_kind for element in representation.elements
    )
    inventoried_kinds = tuple(
        element.element_kind for element in inventory.elements
    )
    declared_vocabulary = set(PROFILE_V1_VOCABULARY)
    complete_projection_vocabulary = set(projected_kinds) == declared_vocabulary
    complete_representation_vocabulary = (
        set(represented_kinds) == declared_vocabulary
    )
    complete_inventory_vocabulary = set(inventoried_kinds) == declared_vocabulary

    representation_byte_identical = canonical_representation_bytes(
        representation
    ) == canonical_representation_bytes(representation_replay)
    inventory_byte_identical = canonical_inventory_bytes(
        inventory
    ) == canonical_inventory_bytes(inventory_replay)
    identities_stable = tuple(
        element.element_id for element in representation.elements
    ) == tuple(element.element_id for element in representation_replay.elements)
    identities_unique = len(
        {element.element_id for element in representation.elements}
    ) == len(representation.elements)
    canonical_order_preserved = (
        tuple(block.ordinal for block in mapping.blocks)
        == tuple(range(len(mapping.blocks)))
        and tuple(element.ordinal for element in representation.elements)
        == tuple(range(len(representation.elements)))
        and tuple(element.ordinal for element in inventory.elements)
        == tuple(range(len(inventory.elements)))
        and tuple(
            (
                element.element_id,
                element.element_kind,
                element.locator,
                element.ordinal,
                element.level,
            )
            for element in representation.elements
        )
        == tuple(
            (
                element.element_id,
                element.element_kind,
                element.locator,
                element.ordinal,
                element.level,
            )
            for element in inventory.elements
        )
    )
    provenance_preserved = (
        representation.source.entry_id == source.source_id
        and representation.source.revision == source.source_revision
        and representation.source.content_sha256 == source.content_sha256
        and inventory.source_id == source.source_id
        and inventory.source_revision == source.source_revision
        and inventory.source_integrity == source.content_sha256
        and inventory.representation_id == representation.representation_id
        and inventory.representation_version
        == representation.representation_version
        and inventory.representation_integrity
        == representation.representation_sha256
    )

    matrix = []
    for kind in PROFILE_V1_VOCABULARY:
        row = {
            "block_kind": kind,
            "projection": kind in projected_kinds,
            "representation": kind in represented_kinds,
            "external_conformance": conformance.valid
            and kind in represented_kinds,
            "understand_inventory": kind in inventoried_kinds,
            "proof": (
                kind in projected_kinds
                and kind in represented_kinds
                and conformance.valid
                and kind in inventoried_kinds
                and representation_byte_identical
                and inventory_byte_identical
                and identities_stable
                and identities_unique
                and canonical_order_preserved
                and provenance_preserved
            ),
        }
        matrix.append(row)

    complete_vocabulary_verified = (
        complete_projection_vocabulary
        and complete_representation_vocabulary
        and complete_inventory_vocabulary
        and conformance.valid
        and representation_byte_identical
        and inventory_byte_identical
        and identities_stable
        and identities_unique
        and canonical_order_preserved
        and provenance_preserved
        and all(
            all(value for key, value in row.items() if key != "block_kind")
            for row in matrix
        )
    )
    proof = {
        "milestone": "WP8 — Complete Vocabulary Proof",
        "profile": {
            "profile_id": representation.profile_id,
            "profile_version": representation.profile_version,
            "declared_block_vocabulary": PROFILE_V1_VOCABULARY,
        },
        "confirmed_markdown": {
            "fixture": str(FIXTURE.relative_to(ROOT)),
            "fixture_sha256": FIXTURE_SHA256,
            "orientation_object_id": source.orientation_object_id,
            "orientation_object_version": source.orientation_object_version,
            "source_id": source.source_id,
            "source_revision": source.source_revision,
            "source_integrity": source.content_sha256,
            "boundary_ref": source.boundary_ref,
            "confirmation_id": source.confirmation_id,
        },
        "projection": {
            "projection_id": renderer.projection.projection_id,
            "projection_version": renderer.projection.projection_version,
            "blocks": [asdict(block) for block in mapping.blocks],
        },
        "representation": asdict(representation),
        "external_conformance": asdict(conformance),
        "understand_inventory": asdict(inventory),
        "coverage_matrix": matrix,
        "verification": {
            "complete_projection_vocabulary": complete_projection_vocabulary,
            "complete_representation_vocabulary": (
                complete_representation_vocabulary
            ),
            "complete_inventory_vocabulary": complete_inventory_vocabulary,
            "representation_byte_identical_replay": (
                representation_byte_identical
            ),
            "inventory_byte_identical_replay": inventory_byte_identical,
            "immutable_element_identities_stable": identities_stable,
            "immutable_element_identities_unique": identities_unique,
            "provenance_preserved": provenance_preserved,
            "stable_ordering_preserved": canonical_order_preserved,
        },
        "understand_boundary": {
            "input": "immutable_structural_representation",
            "raw_markdown_available": False,
            "parsing_performed": False,
            "projection_performed": False,
            "rendering_performed": False,
            "semantic_interpretation_performed": False,
            "summarization_performed": False,
            "statistical_aggregation_performed": False,
            "relation_inference_performed": False,
        },
        "downstream_execution": {
            "structural_summary": False,
            "structural_statistics": False,
            "relations": False,
            "navigation": False,
            "orientation_map": False,
            "runtime": False,
            "gateway": False,
        },
        "complete_vocabulary_verified": complete_vocabulary_verified,
        "stop": STOP,
    }
    return proof, complete_vocabulary_verified


def canonical_proof_bytes(proof: dict[str, object]) -> bytes:
    """Serialize the proof deterministically for independent replay."""

    return json.dumps(
        proof,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def main() -> int:
    try:
        proof, valid = build_complete_vocabulary_proof()
    except (OSError, UnicodeError, TypeError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    sys.stdout.buffer.write(canonical_proof_bytes(proof) + b"\n")
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
