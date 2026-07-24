"""Metadata-only declared Representation inventory inside UNDERSTAND Stage 2.

The inventory preserves exactly one explicitly declared Representation and
stops before source-structure inspection.  It never opens the Representation
payload and does not complete canonical Stage 2.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from orion.public_contracts import OrientationRequest
from orion.understand_stage1_alpha import UnderstandStage1BindingDiagnostic


INVENTORY_DIAGNOSTIC_VERSION = "0.1-alpha"
CANONICAL_STAGE = "understand/2"
RESPONSIBILITY = "declared_representation_inventory"
STOP_BEFORE_SOURCE_STRUCTURE = "before_source_structure_inventory"


@dataclass(frozen=True, slots=True)
class DeclaredRepresentationInventoryEntry:
    """Exact declared metadata for one already-existing Representation."""

    representation_id: str
    representation_version: str
    representation_schema: str
    projection_id: str
    projection_version: str
    renderer_id: str
    renderer_version: str
    target_domain: str
    media_type: str
    fragment_ref: str
    declared_lossiness: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class DeclaredRepresentationInventoryDiagnostic:
    """Internal inventory evidence; never a public Runtime outcome."""

    diagnostic_version: str
    request_id: str
    request_version: str
    operator_id: str
    operator_version: str
    orientation_object_id: str
    orientation_object_version: str
    canonical_stage: str
    responsibility: str
    ordered_representation_count: int
    representations: tuple[DeclaredRepresentationInventoryEntry, ...]
    responsibility_state: str
    stop: str


def _mapping(value: object, field_name: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{field_name} must be a mapping")
    return value


def _text(value: object, field_name: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{field_name} must be exact non-empty text")
    return value


def _lossiness(value: object) -> tuple[str, ...]:
    if not isinstance(value, (tuple, list)) or not value:
        raise ValueError("declared_lossiness must be a non-empty ordered sequence")
    if any(not isinstance(item, str) or not item for item in value):
        raise ValueError("declared_lossiness entries must be exact non-empty text")
    return tuple(value)


def inventory_declared_representation(
    request: OrientationRequest,
    stage1: UnderstandStage1BindingDiagnostic,
    representation: Mapping[str, object],
) -> DeclaredRepresentationInventoryDiagnostic:
    """Inventory exact declared metadata and stop before source structure."""

    if (
        stage1.stage_id != "understand/1"
        or stage1.completion_state != "completed"
        or stage1.stop != "before_understand/2"
    ):
        raise ValueError("declared inventory requires completed understand/1")
    if (
        request.request_id != stage1.request_id
        or request.request_version != stage1.request_version
    ):
        raise ValueError("Stage 1 request identity mismatch")
    if request.mode != "understand" or len(request.orientation_objects) != 1:
        raise ValueError("declared inventory requires one UNDERSTAND object")

    orientation_object = request.orientation_objects[0]
    if (
        orientation_object.object_id != stage1.orientation_object_id
        or orientation_object.object_version != stage1.orientation_object_version
    ):
        raise ValueError("Stage 1 Orientation Object identity mismatch")
    if len(orientation_object.representation_refs) != 1:
        raise ValueError("Alpha inventory requires exactly one declared Representation")

    representation_id = _text(
        representation.get("representation_id"),
        "representation_id",
    )
    representation_version = _text(
        representation.get("representation_version"),
        "representation_version",
    )
    representation_ref = f"{representation_id}@{representation_version}"
    if orientation_object.representation_refs != (representation_ref,):
        raise ValueError("declared Representation reference mismatch")
    if (
        stage1.representation_id != representation_id
        or stage1.representation_version != representation_version
    ):
        raise ValueError("Stage 1 Representation identity mismatch")

    projection = _mapping(representation.get("projection"), "projection")
    declared_lossiness = _lossiness(
        representation.get("declared_lossiness")
    )
    projection_lossiness = _lossiness(
        projection.get("declared_lossiness")
    )
    if declared_lossiness != projection_lossiness:
        raise ValueError("declared Projection lossiness mismatch")

    entry = DeclaredRepresentationInventoryEntry(
        representation_id=representation_id,
        representation_version=representation_version,
        representation_schema=_text(
            representation.get("schema_version"),
            "schema_version",
        ),
        projection_id=_text(
            projection.get("projection_id"),
            "projection.projection_id",
        ),
        projection_version=_text(
            projection.get("projection_version"),
            "projection.projection_version",
        ),
        renderer_id=_text(
            representation.get("renderer_id"),
            "renderer_id",
        ),
        renderer_version=_text(
            representation.get("renderer_version"),
            "renderer_version",
        ),
        target_domain=_text(
            projection.get("target_domain"),
            "projection.target_domain",
        ),
        media_type=_text(
            projection.get("source_media_type"),
            "projection.source_media_type",
        ),
        fragment_ref=_text(
            representation.get("fragment_ref"),
            "fragment_ref",
        ),
        declared_lossiness=declared_lossiness,
    )
    return DeclaredRepresentationInventoryDiagnostic(
        diagnostic_version=INVENTORY_DIAGNOSTIC_VERSION,
        request_id=request.request_id,
        request_version=request.request_version,
        operator_id=stage1.operator_id,
        operator_version=stage1.operator_version,
        orientation_object_id=orientation_object.object_id,
        orientation_object_version=orientation_object.object_version,
        canonical_stage=CANONICAL_STAGE,
        responsibility=RESPONSIBILITY,
        ordered_representation_count=1,
        representations=(entry,),
        responsibility_state="completed",
        stop=STOP_BEFORE_SOURCE_STRUCTURE,
    )


__all__: tuple[str, ...] = ()
