#!/usr/bin/env python3
"""Replay the bounded WP9 Structural Summary proof."""

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
from orion.understand_structural_summary_alpha import (  # noqa: E402
    STOP_AFTER_STRUCTURAL_SUMMARY,
    canonical_structural_summary_bytes,
    summarize_declared_structure,
    validate_structural_summary,
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


def _confirmed_source() -> ConfirmedMarkdownSource:
    source_bytes = FIXTURE.read_bytes()
    actual_sha256 = sha256(source_bytes).hexdigest()
    if actual_sha256 != FIXTURE_SHA256:
        raise ValueError(
            "Structural Summary fixture integrity mismatch: "
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
        content=source_bytes.decode("utf-8", errors="strict"),
        confirmed_by="human-alpha-reviewer",
        confirmed_revision=1,
    )


def build_structural_summary_proof() -> tuple[dict[str, object], bool]:
    """Execute one complete path and stop after Structural Summary."""

    source = _confirmed_source()
    renderer = MarkdownStructuralRendererAlpha()
    mapping = renderer.project(source)
    representation = renderer.render(source)
    representation_replay = renderer.render(source)
    representation_conformance = validate_markdown_structural_representation(
        source,
        representation,
        renderer=renderer,
    )
    inventory = inventory_declared_source_elements(representation)
    inventory_replay = inventory_declared_source_elements(representation)
    summary = summarize_declared_structure(inventory)
    summary_replay = summarize_declared_structure(inventory)
    summary_conformance = validate_structural_summary(inventory, summary)

    representation_replay_identical = canonical_representation_bytes(
        representation
    ) == canonical_representation_bytes(representation_replay)
    inventory_replay_identical = canonical_inventory_bytes(
        inventory
    ) == canonical_inventory_bytes(inventory_replay)
    summary_replay_identical = canonical_structural_summary_bytes(
        summary
    ) == canonical_structural_summary_bytes(summary_replay)
    provenance_preserved = (
        summary.orientation_object_id == representation.orientation_object_id
        and summary.orientation_object_version
        == representation.orientation_object_version
        and summary.representation_id == representation.representation_id
        and summary.representation_version
        == representation.representation_version
        and summary.representation_integrity
        == representation.representation_sha256
        and summary.source_id == representation.source.entry_id
        and summary.source_revision == representation.source.revision
        and summary.source_integrity == representation.source.content_sha256
        and summary.source_boundary == representation.boundary_ref
    )
    valid = (
        representation_conformance.valid
        and summary_conformance.valid
        and representation_replay_identical
        and inventory_replay_identical
        and summary_replay_identical
        and provenance_preserved
        and summary.stop == STOP_AFTER_STRUCTURAL_SUMMARY
    )
    proof = {
        "milestone": "WP9 — Structural Summary",
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
            "ordered_block_kinds": tuple(
                block.element_kind for block in mapping.blocks
            ),
            "ordered_block_count": len(mapping.blocks),
        },
        "representation": {
            "representation_id": representation.representation_id,
            "representation_version": representation.representation_version,
            "representation_integrity": (
                representation.representation_sha256
            ),
            "profile_id": representation.profile_id,
            "profile_version": representation.profile_version,
            "renderer_id": representation.renderer_id,
            "renderer_version": representation.renderer_version,
        },
        "external_representation_conformance": asdict(
            representation_conformance
        ),
        "understand_inventory": {
            "input_boundary": inventory.input_boundary,
            "ordered_element_count": inventory.ordered_element_count,
            "representation_id": inventory.representation_id,
            "representation_version": inventory.representation_version,
            "representation_integrity": inventory.representation_integrity,
            "stop": inventory.stop,
        },
        "structural_summary": asdict(summary),
        "external_summary_conformance": asdict(summary_conformance),
        "verification": {
            "representation_byte_identical_replay": (
                representation_replay_identical
            ),
            "inventory_byte_identical_replay": inventory_replay_identical,
            "summary_byte_identical_replay": summary_replay_identical,
            "summary_fields_recomputed_from_inventory": (
                summary_conformance.valid
            ),
            "provenance_preserved": provenance_preserved,
        },
        "summary_boundary": {
            "input": "declared_source_element_inventory",
            "raw_markdown_available": False,
            "source_document_accessed": False,
            "parser_accessed": False,
            "projection_accessed": False,
            "renderer_accessed": False,
            "external_knowledge_accessed": False,
            "semantic_interpretation_performed": False,
        },
        "downstream_execution": {
            "structural_statistics": False,
            "relations": False,
            "navigation": False,
            "orientation_map": False,
            "lyra": False,
            "sirius": False,
            "runtime": False,
            "gateway": False,
        },
        "proof_valid": valid,
        "stop": STOP_AFTER_STRUCTURAL_SUMMARY,
    }
    return proof, valid


def canonical_proof_bytes(proof: dict[str, object]) -> bytes:
    """Serialize the complete proof deterministically."""

    return json.dumps(
        proof,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def main() -> int:
    try:
        proof, valid = build_structural_summary_proof()
    except (OSError, UnicodeError, TypeError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    sys.stdout.buffer.write(canonical_proof_bytes(proof) + b"\n")
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
