"""Semantically free UNDERSTAND Stage 1 identity binding proof.

Stage 1 reads only declared identity, version, source, revision and integrity
metadata.  It does not inspect Representation content, interpret material, or
enter UNDERSTAND Stage 2.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from orion.orientation_runtime.runtime import OrientationRuntime
from orion.public_contracts import OrientationRequest
from orion.readiness_alpha import RuntimeReadinessDiagnostic


BINDING_DIAGNOSTIC_VERSION = "0.1-alpha"
UNDERSTAND_STAGE_1 = "understand/1"
STOP_BEFORE_UNDERSTAND_2 = "before_understand/2"


@dataclass(frozen=True, slots=True)
class UnderstandStage1BindingDiagnostic:
    """Internal identity-binding evidence; never a public Runtime outcome."""

    diagnostic_version: str
    request_id: str
    request_version: str
    operator_id: str
    operator_version: str
    orientation_object_id: str
    orientation_object_version: str
    representation_id: str
    representation_version: str
    source_owner: str
    source_ref: str
    source_revision: str
    integrity_method: str
    integrity_value: str
    integrity_coverage: str
    integrity_verified: bool
    stage_id: str
    completion_state: str
    stop: str


def _mapping(value: object, field_name: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{field_name} must be a mapping")
    return value


def _text(value: object, field_name: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{field_name} must be exact non-empty text")
    return value


def bind_understand_stage1(
    request: OrientationRequest,
    readiness: RuntimeReadinessDiagnostic,
    representation: Mapping[str, object],
) -> UnderstandStage1BindingDiagnostic:
    """Bind exact declared metadata and stop before semantic processing."""

    if readiness.decision != "ready" or readiness.stop != "before_processing":
        raise ValueError("UNDERSTAND Stage 1 requires an exact ready diagnostic")
    if (
        readiness.request_id != request.request_id
        or readiness.request_version != request.request_version
        or readiness.request_schema_version != request.schema_version
        or readiness.mode != request.mode
    ):
        raise ValueError("readiness identity does not match the request")
    if request.mode != "understand":
        raise ValueError("UNDERSTAND Stage 1 accepts only understand requests")
    if len(request.orientation_objects) != 1:
        raise ValueError("UNDERSTAND Stage 1 requires exactly one Orientation Object")

    orientation_object = request.orientation_objects[0]
    if len(orientation_object.representation_refs) != 1:
        raise ValueError("UNDERSTAND Stage 1 requires exactly one Representation")
    if orientation_object.integrity_ref is None:
        raise ValueError("UNDERSTAND Stage 1 requires explicit integrity lineage")

    representation_id = _text(
        representation.get("representation_id"),
        "representation_id",
    )
    representation_version = _text(
        representation.get("representation_version"),
        "representation_version",
    )
    representation_sha256 = _text(
        representation.get("representation_sha256"),
        "representation_sha256",
    )
    representation_ref = f"{representation_id}@{representation_version}"
    if orientation_object.representation_refs != (representation_ref,):
        raise ValueError("Representation reference mismatch")
    if representation_version != f"sha256:{representation_sha256}":
        raise ValueError("Representation version mismatch")

    represented_object_id = _text(
        representation.get("orientation_object_id"),
        "orientation_object_id",
    )
    represented_object_version = _text(
        representation.get("orientation_object_version"),
        "orientation_object_version",
    )
    if (
        orientation_object.object_id != represented_object_id
        or orientation_object.object_version != represented_object_version
    ):
        raise ValueError("Orientation Object identity mismatch")

    source = _mapping(representation.get("source"), "source")
    source_owner = _text(source.get("owner"), "source.owner")
    source_ref = _text(source.get("source_ref"), "source.source_ref")
    source_revision = _text(source.get("revision"), "source.revision")
    if (
        orientation_object.source_owner != source_owner
        or orientation_object.source_ref != source_ref
        or orientation_object.source_revision != source_revision
    ):
        raise ValueError("source identity or revision mismatch")

    payload = _mapping(representation.get("payload"), "payload")
    content_sha256 = _text(
        payload.get("content_sha256"),
        "payload.content_sha256",
    )
    integrity = orientation_object.integrity_ref
    if (
        integrity.method != "sha256"
        or integrity.value != content_sha256
        or integrity.coverage != "whole"
        or integrity.verified is not True
    ):
        raise ValueError("integrity reference mismatch")

    return UnderstandStage1BindingDiagnostic(
        diagnostic_version=BINDING_DIAGNOSTIC_VERSION,
        request_id=request.request_id,
        request_version=request.request_version,
        operator_id=OrientationRuntime.operator_id,
        operator_version=OrientationRuntime.operator_version,
        orientation_object_id=orientation_object.object_id,
        orientation_object_version=orientation_object.object_version,
        representation_id=representation_id,
        representation_version=representation_version,
        source_owner=source_owner,
        source_ref=source_ref,
        source_revision=source_revision,
        integrity_method=integrity.method,
        integrity_value=integrity.value,
        integrity_coverage=integrity.coverage,
        integrity_verified=integrity.verified,
        stage_id=UNDERSTAND_STAGE_1,
        completion_state="completed",
        stop=STOP_BEFORE_UNDERSTAND_2,
    )


__all__: tuple[str, ...] = ()
