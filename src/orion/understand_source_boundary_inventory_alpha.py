"""Declared source-boundary inventory inside UNDERSTAND Stage 2.

This internal Alpha responsibility preserves an already-declared fragment
boundary from immutable predecessor diagnostics.  It performs no I/O and stops
before declared source-element inventory.
"""

from __future__ import annotations

from dataclasses import dataclass

from orion.public_contracts import OrientationRequest
from orion.understand_representation_inventory_alpha import (
    DeclaredRepresentationInventoryDiagnostic,
)
from orion.understand_stage1_alpha import UnderstandStage1BindingDiagnostic


BOUNDARY_DIAGNOSTIC_VERSION = "0.1-alpha"
CANONICAL_STAGE = "understand/2"
RESPONSIBILITY = "declared_source_boundary_inventory"
PREDECESSOR_RESPONSIBILITY = "declared_representation_inventory"
PREDECESSOR_STOP = "before_source_structure_inventory"
STOP_BEFORE_SOURCE_ELEMENTS = "before_declared_source_element_inventory"
WHOLE_FRAGMENT = "whole"


@dataclass(frozen=True, slots=True)
class DeclaredSourceBoundaryEntry:
    """One exact fragment boundary in predecessor Representation order."""

    representation_id: str
    representation_version: str
    source_owner: str
    source_ref: str
    source_revision: str
    fragment_ref: str
    integrity_method: str
    integrity_value: str
    integrity_coverage: str
    integrity_verified: bool


@dataclass(frozen=True, slots=True)
class DeclaredSourceBoundaryInventoryDiagnostic:
    """Internal boundary evidence; never a public Runtime outcome."""

    diagnostic_version: str
    request_id: str
    request_version: str
    operator_id: str
    operator_version: str
    orientation_object_id: str
    orientation_object_version: str
    predecessor_responsibility: str
    predecessor_stop: str
    canonical_stage: str
    responsibility: str
    ordered_boundary_count: int
    boundaries: tuple[DeclaredSourceBoundaryEntry, ...]
    responsibility_state: str
    canonical_stage_state: str
    stop: str


def inventory_declared_source_boundaries(
    request: OrientationRequest,
    stage1: UnderstandStage1BindingDiagnostic,
    representation_inventory: DeclaredRepresentationInventoryDiagnostic,
) -> DeclaredSourceBoundaryInventoryDiagnostic:
    """Preserve the exact declared boundary and stop before source elements."""

    if (
        stage1.stage_id != "understand/1"
        or stage1.completion_state != "completed"
        or stage1.stop != "before_understand/2"
    ):
        raise ValueError("source boundary inventory requires completed understand/1")
    if (
        representation_inventory.canonical_stage != CANONICAL_STAGE
        or representation_inventory.responsibility != PREDECESSOR_RESPONSIBILITY
        or representation_inventory.responsibility_state != "completed"
        or representation_inventory.stop != PREDECESSOR_STOP
    ):
        raise ValueError("source boundary inventory requires the exact predecessor")
    if (
        request.request_id != stage1.request_id
        or request.request_version != stage1.request_version
        or request.request_id != representation_inventory.request_id
        or request.request_version != representation_inventory.request_version
    ):
        raise ValueError("request identity mismatch")
    if request.mode != "understand" or len(request.orientation_objects) != 1:
        raise ValueError("source boundary inventory requires one UNDERSTAND object")

    orientation_object = request.orientation_objects[0]
    if (
        orientation_object.object_id != stage1.orientation_object_id
        or orientation_object.object_version != stage1.orientation_object_version
        or orientation_object.object_id
        != representation_inventory.orientation_object_id
        or orientation_object.object_version
        != representation_inventory.orientation_object_version
    ):
        raise ValueError("Orientation Object identity mismatch")
    if (
        stage1.operator_id != representation_inventory.operator_id
        or stage1.operator_version != representation_inventory.operator_version
    ):
        raise ValueError("operator identity mismatch")
    if (
        representation_inventory.ordered_representation_count != 1
        or len(representation_inventory.representations) != 1
    ):
        raise ValueError("Alpha boundary inventory requires one Representation")

    declared_representation = representation_inventory.representations[0]
    if (
        declared_representation.representation_id != stage1.representation_id
        or declared_representation.representation_version
        != stage1.representation_version
    ):
        raise ValueError("Representation identity mismatch")
    representation_ref = (
        f"{declared_representation.representation_id}"
        f"@{declared_representation.representation_version}"
    )
    if orientation_object.representation_refs != (representation_ref,):
        raise ValueError("declared Representation order or identity mismatch")
    if (
        orientation_object.source_owner != stage1.source_owner
        or orientation_object.source_ref != stage1.source_ref
        or orientation_object.source_revision != stage1.source_revision
    ):
        raise ValueError("source identity or revision mismatch")

    integrity = orientation_object.integrity_ref
    if integrity is None:
        raise ValueError("declared boundary requires integrity lineage")
    if (
        integrity.method != stage1.integrity_method
        or integrity.value != stage1.integrity_value
        or integrity.coverage != stage1.integrity_coverage
        or integrity.verified != stage1.integrity_verified
    ):
        raise ValueError("integrity lineage mismatch")
    if (
        declared_representation.fragment_ref != WHOLE_FRAGMENT
        or integrity.coverage != WHOLE_FRAGMENT
        or integrity.verified is not True
    ):
        raise ValueError("declared whole-source boundary is inconsistent")

    boundary = DeclaredSourceBoundaryEntry(
        representation_id=declared_representation.representation_id,
        representation_version=declared_representation.representation_version,
        source_owner=stage1.source_owner,
        source_ref=stage1.source_ref,
        source_revision=stage1.source_revision,
        fragment_ref=declared_representation.fragment_ref,
        integrity_method=stage1.integrity_method,
        integrity_value=stage1.integrity_value,
        integrity_coverage=stage1.integrity_coverage,
        integrity_verified=stage1.integrity_verified,
    )
    return DeclaredSourceBoundaryInventoryDiagnostic(
        diagnostic_version=BOUNDARY_DIAGNOSTIC_VERSION,
        request_id=request.request_id,
        request_version=request.request_version,
        operator_id=stage1.operator_id,
        operator_version=stage1.operator_version,
        orientation_object_id=orientation_object.object_id,
        orientation_object_version=orientation_object.object_version,
        predecessor_responsibility=representation_inventory.responsibility,
        predecessor_stop=representation_inventory.stop,
        canonical_stage=CANONICAL_STAGE,
        responsibility=RESPONSIBILITY,
        ordered_boundary_count=1,
        boundaries=(boundary,),
        responsibility_state="completed",
        canonical_stage_state="incomplete",
        stop=STOP_BEFORE_SOURCE_ELEMENTS,
    )


__all__: tuple[str, ...] = ()
