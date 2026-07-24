#!/usr/bin/env python3
"""Replay the three bounded proofs for Slice II Structural Expansion I."""

from __future__ import annotations

from dataclasses import asdict
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


WORK_PACKAGES = (
    (
        "WP2",
        "block_quote",
        "> Orientation begins here.\n"
        "A lazy continuation remains inside the quote.\n"
        ">\n"
        "> > A nested quote remains distinct.\n",
        ("block_quote",),
    ),
    (
        "WP3",
        "atomic_list_family",
        "1. Observe\n"
        "2. Orient\n"
        "   - preserve identity\n"
        "   - preserve order\n"
        "\n"
        "+ Continue\n",
        ("ordered_list", "unordered_list", "list_item"),
    ),
    (
        "WP4",
        "thematic_break",
        "***\n"
        "\n"
        "- This remains a list item.\n"
        "\n"
        "- - -\n",
        ("thematic_break",),
    ),
)


def _proof(
    work_package: str,
    capability: str,
    content: str,
    required_kinds: tuple[str, ...],
) -> tuple[dict[str, object], bool]:
    source = ConfirmedMarkdownSource.create(
        orientation_object_id=f"orientation-object-{work_package.lower()}",
        orientation_object_version="1",
        source_id=f"markdown-source-{work_package.lower()}",
        source_owner="human-alpha-reviewer",
        source_ref=f"local:{capability}.md",
        content=content,
        confirmed_by="human-alpha-reviewer",
        confirmed_revision=1,
    )
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
    element_kinds = tuple(element.element_kind for element in inventory.elements)
    representation_byte_identical = canonical_representation_bytes(
        representation
    ) == canonical_representation_bytes(representation_replay)
    inventory_byte_identical = canonical_inventory_bytes(
        inventory
    ) == canonical_inventory_bytes(inventory_replay)
    required_kinds_present = all(kind in element_kinds for kind in required_kinds)
    valid = (
        conformance.valid
        and representation_byte_identical
        and inventory_byte_identical
        and required_kinds_present
    )
    return (
        {
            "work_package": work_package,
            "capability": capability,
            "source": {
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
            "representation": {
                "representation_id": representation.representation_id,
                "representation_version": representation.representation_version,
                "representation_integrity": (
                    representation.representation_sha256
                ),
                "renderer_id": representation.renderer_id,
                "renderer_version": representation.renderer_version,
                "element_kinds": element_kinds,
            },
            "external_conformance": asdict(conformance),
            "inventory": asdict(inventory),
            "determinism": {
                "representation_byte_identical_replay": (
                    representation_byte_identical
                ),
                "inventory_byte_identical_replay": inventory_byte_identical,
            },
            "required_kinds": required_kinds,
            "required_kinds_present": required_kinds_present,
            "raw_markdown_available_to_understand": False,
            "projection_executed_by_understand": False,
            "renderer_executed_by_understand": False,
            "summary_executed": False,
            "statistics_executed": False,
            "relations_created": False,
            "semantic_processing": "none",
            "runtime_executed": False,
            "gateway_executed": False,
            "stop": "after_declared_source_element_inventory",
        },
        valid,
    )


def main() -> int:
    proofs: list[dict[str, object]] = []
    all_valid = True
    for work_package in WORK_PACKAGES:
        proof, valid = _proof(*work_package)
        proofs.append(proof)
        all_valid = all_valid and valid
    print(
        json.dumps(
            {
                "milestone": "Slice II — Structural Expansion I",
                "proofs": proofs,
                "all_proofs_valid": all_valid,
                "stop": "after_declared_source_element_inventory",
            },
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )
    )
    return 0 if all_valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
