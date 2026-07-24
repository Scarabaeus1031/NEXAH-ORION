"""Declared source-element availability check inside UNDERSTAND Stage 2.

The check recognizes one exact immutable Representation profile and records
that the profile declares no source elements. It performs no I/O, discovery,
or semantic processing and stops before source-element inventory.
"""

from __future__ import annotations

from dataclasses import dataclass

from orion.public_contracts import OrientationRequest
from orion.understand_representation_inventory_alpha import (
    DeclaredRepresentationInventoryDiagnostic,
)
from orion.understand_source_boundary_inventory_alpha import (
    DeclaredSourceBoundaryInventoryDiagnostic,
)
from orion.understand_stage1_alpha import UnderstandStage1BindingDiagnostic


DECLARATION_DIAGNOSTIC_VERSION = "0.1-alpha"
CANONICAL_STAGE = "understand/2"
RESPONSIBILITY = "declared_source_element_declaration_check"
PREDECESSOR_RESPONSIBILITY = "declared_source_boundary_inventory"
PREDECESSOR_STOP = "before_declared_source_element_inventory"
STOP_BEFORE_ELEMENT_INVENTORY = "before_declared_source_element_inventory"
NOT_DECLARED = "not_declared"

EXACT_TEXT_SCHEMA = "orion.representation/exact-text/0.1-alpha"
EXACT_TEXT_PROJECTION_ID = "orion.projection/exact-text"
EXACT_TEXT_PROJECTION_VERSION = "0.1-alpha"
EXACT_TEXT_RENDERER_ID = "orion.renderer/exact-text"
EXACT_TEXT_RENDERER_VERSION = "0.1-alpha"
EXACT_TEXT_TARGET_DOMAIN = "orion.representation.text-exact"
EXACT_TEXT_MEDIA_TYPE = "text/plain;charset=utf-8"
EXACT_TEXT_LOSSINESS = ("none",)


@dataclass(frozen=True, slots=True)
class DeclaredSourceElementDeclarationDiagnostic:
    """Internal declaration evidence; never a public Runtime outcome."""

    diagnostic_version: str
    request_id: str
    request_version: str
    operator_id: str
    operator_version: str
    orientation_object_id: str
    orientation_object_version: str
    representation_id: str
    representation_version: str
    predecessor_responsibility: str
    predecessor_stop: str
    canonical_stage: str
    responsibility: str
    declaration_basis: str
    declaration_state: str
    responsibility_state: str
    canonical_stage_state: str
    stop: str


def check_declared_source_element_declaration(
    request: OrientationRequest,
    stage1: UnderstandStage1BindingDiagnostic,
    representation_inventory: DeclaredRepresentationInventoryDiagnostic,
    boundary_inventory: DeclaredSourceBoundaryInventoryDiagnostic,
) -> DeclaredSourceElementDeclarationDiagnostic:
    """Determine declaration availability and stop before element inventory."""

    if (
        stage1.stage_id != "understand/1"
        or stage1.completion_state != "completed"
        or stage1.stop != "before_understand/2"
    ):
        raise ValueError("declaration check requires completed understand/1")
    if (
        representation_inventory.canonical_stage != CANONICAL_STAGE
        or representation_inventory.responsibility
        != "declared_representation_inventory"
        or representation_inventory.responsibility_state != "completed"
        or representation_inventory.stop != "before_source_structure_inventory"
    ):
        raise ValueError("declaration check requires Representation Inventory")
    if (
        boundary_inventory.canonical_stage != CANONICAL_STAGE
        or boundary_inventory.responsibility != PREDECESSOR_RESPONSIBILITY
        or boundary_inventory.responsibility_state != "completed"
        or boundary_inventory.canonical_stage_state != "incomplete"
        or boundary_inventory.stop != PREDECESSOR_STOP
    ):
        raise ValueError("declaration check requires the exact boundary predecessor")
    if (
        request.request_id != stage1.request_id
        or request.request_version != stage1.request_version
        or request.request_id != representation_inventory.request_id
        or request.request_version != representation_inventory.request_version
        or request.request_id != boundary_inventory.request_id
        or request.request_version != boundary_inventory.request_version
    ):
        raise ValueError("request identity mismatch")
    if request.mode != "understand" or len(request.orientation_objects) != 1:
        raise ValueError("declaration check requires one UNDERSTAND object")

    orientation_object = request.orientation_objects[0]
    object_identity = (
        orientation_object.object_id,
        orientation_object.object_version,
    )
    if object_identity != (
        stage1.orientation_object_id,
        stage1.orientation_object_version,
    ) or object_identity != (
        representation_inventory.orientation_object_id,
        representation_inventory.orientation_object_version,
    ) or object_identity != (
        boundary_inventory.orientation_object_id,
        boundary_inventory.orientation_object_version,
    ):
        raise ValueError("Orientation Object identity mismatch")
    operator_identity = (stage1.operator_id, stage1.operator_version)
    if operator_identity != (
        representation_inventory.operator_id,
        representation_inventory.operator_version,
    ) or operator_identity != (
        boundary_inventory.operator_id,
        boundary_inventory.operator_version,
    ):
        raise ValueError("operator identity mismatch")
    if (
        representation_inventory.ordered_representation_count != 1
        or len(representation_inventory.representations) != 1
        or boundary_inventory.ordered_boundary_count != 1
        or len(boundary_inventory.boundaries) != 1
    ):
        raise ValueError("Alpha declaration check requires one bound Representation")

    representation = representation_inventory.representations[0]
    boundary = boundary_inventory.boundaries[0]
    representation_identity = (
        representation.representation_id,
        representation.representation_version,
    )
    if representation_identity != (
        stage1.representation_id,
        stage1.representation_version,
    ) or representation_identity != (
        boundary.representation_id,
        boundary.representation_version,
    ):
        raise ValueError("Representation identity mismatch")
    representation_ref = f"{representation_identity[0]}@{representation_identity[1]}"
    if orientation_object.representation_refs != (representation_ref,):
        raise ValueError("declared Representation identity or order mismatch")
    if (
        orientation_object.source_owner != boundary.source_owner
        or orientation_object.source_ref != boundary.source_ref
        or orientation_object.source_revision != boundary.source_revision
        or representation.fragment_ref != boundary.fragment_ref
    ):
        raise ValueError("source boundary lineage mismatch")

    accepted_profile = (
        representation.representation_schema,
        representation.projection_id,
        representation.projection_version,
        representation.renderer_id,
        representation.renderer_version,
        representation.target_domain,
        representation.media_type,
        representation.declared_lossiness,
    )
    exact_text_profile = (
        EXACT_TEXT_SCHEMA,
        EXACT_TEXT_PROJECTION_ID,
        EXACT_TEXT_PROJECTION_VERSION,
        EXACT_TEXT_RENDERER_ID,
        EXACT_TEXT_RENDERER_VERSION,
        EXACT_TEXT_TARGET_DOMAIN,
        EXACT_TEXT_MEDIA_TYPE,
        EXACT_TEXT_LOSSINESS,
    )
    if accepted_profile != exact_text_profile:
        raise ValueError("unknown Representation profile declaration behavior")

    return DeclaredSourceElementDeclarationDiagnostic(
        diagnostic_version=DECLARATION_DIAGNOSTIC_VERSION,
        request_id=request.request_id,
        request_version=request.request_version,
        operator_id=stage1.operator_id,
        operator_version=stage1.operator_version,
        orientation_object_id=orientation_object.object_id,
        orientation_object_version=orientation_object.object_version,
        representation_id=representation.representation_id,
        representation_version=representation.representation_version,
        predecessor_responsibility=boundary_inventory.responsibility,
        predecessor_stop=boundary_inventory.stop,
        canonical_stage=CANONICAL_STAGE,
        responsibility=RESPONSIBILITY,
        declaration_basis=representation.representation_schema,
        declaration_state=NOT_DECLARED,
        responsibility_state="completed",
        canonical_stage_state="incomplete",
        stop=STOP_BEFORE_ELEMENT_INVENTORY,
    )


__all__: tuple[str, ...] = ()
