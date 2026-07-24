#!/usr/bin/env python3
"""Execute the bounded Markdown Structural Renderer Alpha proof."""

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
    representation_as_dict,
    validate_markdown_structural_representation,
)


SOURCE_CONTENT = (
    "# Orientation\n"
    "\n"
    "Information already exists.\n"
    "Orientation is what is missing.\n"
    "\n"
    "### Continue\n"
    "\n"
    "Bring one exact question.\n"
)


def main() -> int:
    source = ConfirmedMarkdownSource.create(
        orientation_object_id="orientation-object-alpha",
        orientation_object_version="1",
        source_id="markdown-source-alpha",
        source_owner="human-alpha-reviewer",
        source_ref="local:orientation.md",
        content=SOURCE_CONTENT,
        confirmed_by="human-alpha-reviewer",
        confirmed_revision=1,
    )
    renderer = MarkdownStructuralRendererAlpha()
    mapping = renderer.project(source)
    representation = renderer.render(source)
    replay = renderer.render(source)
    conformance = validate_markdown_structural_representation(
        source,
        representation,
        renderer=renderer,
    )
    byte_identical = canonical_representation_bytes(
        representation
    ) == canonical_representation_bytes(replay)
    output = {
        "profile": "Markdown Structural Renderer Alpha",
        "scope": ["document", "atx_heading", "paragraph"],
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
            "profile_id": renderer.projection.profile_id,
            "profile_version": renderer.projection.profile_version,
            "grammar": renderer.projection.source_grammar,
            "grammar_version": renderer.projection.source_grammar_version,
            "blocks": [asdict(block) for block in mapping.blocks],
        },
        "representation": representation_as_dict(representation),
        "determinism": {
            "byte_identical_replay": byte_identical,
        },
        "conformance": asdict(conformance),
        "runtime_executed": False,
        "gateway_executed": False,
        "understand_executed": False,
        "stop": "after_immutable_representation",
    }
    print(
        json.dumps(
            output,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if conformance.valid and byte_identical else 1


if __name__ == "__main__":
    raise SystemExit(main())
