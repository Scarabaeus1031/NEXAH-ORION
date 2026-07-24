#!/usr/bin/env python3
"""Execute the bounded UNDERSTAND Source Element Inventory Alpha proof."""

from __future__ import annotations

from dataclasses import asdict
from hashlib import sha256
import json
from pathlib import Path
import sys
from typing import Mapping


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from orion.contracts import ProvenanceRef  # noqa: E402
from orion.markdown_structural_renderer_alpha import (  # noqa: E402
    DeclaredStructuralElement,
    ImmutableMarkdownStructuralRepresentation,
    MarkdownStructuralProjection,
    SourceLocator,
)
from orion.representation_alpha import RepresentationProvenanceStep  # noqa: E402
from orion.understand_source_element_inventory_alpha import (  # noqa: E402
    canonical_inventory_bytes,
    inventory_declared_source_elements,
)


FIXTURE = (
    ROOT
    / "examples"
    / "markdown_structural_renderer_alpha"
    / "immutable_representation.json"
)
FIXTURE_SHA256 = "a04eea46759a19e3e4e9bfc3a59db593e89751f4c9f463c02ae372da9d2edf9f"


def _mapping(value: object, field_name: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{field_name} must be a mapping")
    return value


def _sequence(value: object, field_name: str) -> list[object]:
    if not isinstance(value, list):
        raise ValueError(f"{field_name} must be an ordered sequence")
    return value


def _text(value: Mapping[str, object], field_name: str) -> str:
    item = value.get(field_name)
    if not isinstance(item, str) or not item:
        raise ValueError(f"{field_name} must be exact non-empty text")
    return item


def _integer(value: Mapping[str, object], field_name: str) -> int:
    item = value.get(field_name)
    if type(item) is not int:
        raise ValueError(f"{field_name} must be an integer")
    return item


def _optional_integer(value: Mapping[str, object], field_name: str) -> int | None:
    item = value.get(field_name)
    if item is None:
        return None
    if type(item) is not int:
        raise ValueError(f"{field_name} must be an integer or null")
    return item


def _text_tuple(value: object, field_name: str) -> tuple[str, ...]:
    items = _sequence(value, field_name)
    if any(not isinstance(item, str) or not item for item in items):
        raise ValueError(f"{field_name} entries must be exact non-empty text")
    return tuple(items)  # type: ignore[arg-type]


def _load_immutable_representation() -> ImmutableMarkdownStructuralRepresentation:
    fixture_bytes = FIXTURE.read_bytes()
    if sha256(fixture_bytes).hexdigest() != FIXTURE_SHA256:
        raise ValueError("immutable Structural Representation fixture hash mismatch")
    value = _mapping(json.loads(fixture_bytes), "representation")
    source_value = _mapping(value.get("source"), "source")
    projection_value = _mapping(value.get("projection"), "projection")
    elements = []
    for item in _sequence(value.get("elements"), "elements"):
        element = _mapping(item, "element")
        locator_value = _mapping(element.get("locator"), "element.locator")
        elements.append(
            DeclaredStructuralElement(
                element_id=_text(element, "element_id"),
                element_kind=_text(element, "element_kind"),
                boundary_ref=_text(element, "boundary_ref"),
                locator=SourceLocator(
                    start_byte=_integer(locator_value, "start_byte"),
                    end_byte=_integer(locator_value, "end_byte"),
                    start_line=_integer(locator_value, "start_line"),
                    end_line=_integer(locator_value, "end_line"),
                ),
                ordinal=_integer(element, "ordinal"),
                level=_optional_integer(element, "level"),
            )
        )
    provenance = []
    for item in _sequence(value.get("provenance"), "provenance"):
        step = _mapping(item, "provenance step")
        provenance.append(
            RepresentationProvenanceStep(
                sequence=_integer(step, "sequence"),
                step_id=_text(step, "step_id"),
                step_kind=_text(step, "step_kind"),
                owner=_text(step, "owner"),
                input_refs=_text_tuple(step.get("input_refs"), "input_refs"),
                output_ref=_text(step, "output_ref"),
                declared_lossiness=_text_tuple(
                    step.get("declared_lossiness"),
                    "provenance declared_lossiness",
                ),
            )
        )
    projection = MarkdownStructuralProjection(
        projection_id=_text(projection_value, "projection_id"),
        projection_version=_text(projection_value, "projection_version"),
        profile_id=_text(projection_value, "profile_id"),
        profile_version=_text(projection_value, "profile_version"),
        source_media_type=_text(projection_value, "source_media_type"),
        source_grammar=_text(projection_value, "source_grammar"),
        source_grammar_version=_text(
            projection_value,
            "source_grammar_version",
        ),
        source_boundary=_text(projection_value, "source_boundary"),
        target_domain=_text(projection_value, "target_domain"),
        declared_lossiness=_text_tuple(
            projection_value.get("declared_lossiness"),
            "Projection declared_lossiness",
        ),
    )
    representation = ImmutableMarkdownStructuralRepresentation(
        representation_id=_text(value, "representation_id"),
        representation_version=_text(value, "representation_version"),
        representation_sha256=_text(value, "representation_sha256"),
        orientation_object_id=_text(value, "orientation_object_id"),
        orientation_object_version=_text(value, "orientation_object_version"),
        source=ProvenanceRef(
            entry_id=_text(source_value, "entry_id"),
            owner=_text(source_value, "owner"),
            source_ref=_text(source_value, "source_ref"),
            revision=_text(source_value, "revision"),
            content_sha256=_text(source_value, "content_sha256"),
        ),
        boundary_ref=_text(value, "boundary_ref"),
        profile_id=_text(value, "profile_id"),
        profile_version=_text(value, "profile_version"),
        target_domain=_text(value, "target_domain"),
        projection=projection,
        renderer_id=_text(value, "renderer_id"),
        renderer_version=_text(value, "renderer_version"),
        elements=tuple(elements),
        provenance=tuple(provenance),
        declared_lossiness=_text_tuple(
            value.get("declared_lossiness"),
            "Representation declared_lossiness",
        ),
        schema_version=_text(value, "schema_version"),
    )
    representation.__post_init__()
    return representation


def main() -> int:
    try:
        representation = _load_immutable_representation()
        first = inventory_declared_source_elements(representation)
        second = inventory_declared_source_elements(representation)
        byte_identical = canonical_inventory_bytes(
            first
        ) == canonical_inventory_bytes(second)
    except (
        KeyError,
        OSError,
        TypeError,
        ValueError,
        json.JSONDecodeError,
    ) as error:
        print(f"[UNDERSTAND Source Element Inventory Alpha] {error}", file=sys.stderr)
        return 1

    proof = {
        "diagnostic_kind": "internal_declared_source_element_inventory",
        "input": {
            "fixture_sha256": FIXTURE_SHA256,
            "representation_id": representation.representation_id,
            "representation_version": representation.representation_version,
            "representation_integrity": representation.representation_sha256,
        },
        "inventory": asdict(first),
        "determinism": {
            "byte_identical_replay": byte_identical,
        },
        "raw_markdown_available": False,
        "raw_markdown_accessed": False,
        "projection_executed": False,
        "renderer_executed": False,
        "structure_created": False,
        "semantic_processing": "none",
        "runtime_executed": False,
        "gateway_executed": False,
        "stop": "after_declared_source_element_inventory",
    }
    print(
        json.dumps(
            proof,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )
    )
    return 0 if byte_identical else 1


if __name__ == "__main__":
    raise SystemExit(main())
