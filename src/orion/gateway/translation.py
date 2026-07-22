"""Structural translation from external mappings to public contracts.

This module assigns no Orientation meaning.  It only constructs the frozen
Version 1.0 request shape from explicitly supplied values.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import cast

from orion.public_contracts import (
    NO_EFFECTS,
    ORIENTATION_REQUEST_SCHEMA,
    AccessStatus,
    ClarificationReference,
    ContinuationReference,
    EffectDeclaration,
    HumanAuthorityReference,
    IdentityScope,
    IntegrityReference,
    Intention,
    OrientationMode,
    OrientationObjectReference,
    OrientationRequest,
    PublicValue,
    RequesterKind,
    RequesterReference,
    Scope,
)


class GatewayInputError(ValueError):
    """Private structural error caught at the Gateway boundary."""

    def __init__(self, path: str, reason: str) -> None:
        super().__init__(f"{path}: {reason}")
        self.path = path
        self.reason = reason


def construct_orientation_request(payload: Mapping[str, object]) -> OrientationRequest:
    """Construct an Orientation Request 1.0 without interpreting its content."""

    root = _mapping(payload, "request")
    objects = _sequence(root.get("orientation_objects"), "orientation_objects")
    return OrientationRequest(
        schema_version=_optional_text(root.get("schema_version"), "schema_version")
        or ORIENTATION_REQUEST_SCHEMA,
        request_id=_text(root.get("request_id"), "request_id"),
        request_version=_text(root.get("request_version"), "request_version"),
        mode=cast(OrientationMode, _text(root.get("mode"), "mode")),
        requested_by=_requester(root.get("requested_by")),
        human_authority=_human_authority(root.get("human_authority")),
        orientation_objects=tuple(
            _orientation_object(value, f"orientation_objects[{index}]")
            for index, value in enumerate(objects)
        ),
        intention=_intention(root.get("intention")),
        scope=_scope(root.get("scope")),
        effects=cast(EffectDeclaration, root.get("effects", NO_EFFECTS)),
        audience=_optional_text(root.get("audience"), "audience"),
        constraints=_texts(root.get("constraints", ()), "constraints"),
        evidence_policy=_optional_text(root.get("evidence_policy"), "evidence_policy"),
        representation_preferences=_texts(
            root.get("representation_preferences", ()),
            "representation_preferences",
        ),
        depth_budget=_optional_text(root.get("depth_budget"), "depth_budget"),
        prior_report_refs=_texts(root.get("prior_report_refs", ()), "prior_report_refs"),
        human_annotations=_texts(root.get("human_annotations", ()), "human_annotations"),
        clarification_of=_clarification_reference(root.get("clarification_of")),
        continuation_of=_continuation_reference(root.get("continuation_of")),
        mode_parameters=_public_mapping(root.get("mode_parameters", {}), "mode_parameters"),
        consumer_context=_public_mapping(root.get("consumer_context", {}), "consumer_context"),
    )


def _requester(value: object) -> RequesterReference:
    item = _mapping(value, "requested_by")
    return RequesterReference(
        _text(item.get("requester_id"), "requested_by.requester_id"),
        cast(RequesterKind, _text(item.get("requester_kind"), "requested_by.requester_kind")),
        _text(item.get("authority_domain"), "requested_by.authority_domain"),
    )


def _human_authority(value: object) -> HumanAuthorityReference:
    item = _mapping(value, "human_authority")
    return HumanAuthorityReference(
        _text(item.get("human_ref"), "human_authority.human_ref"),
        _texts(item.get("authority_scope"), "human_authority.authority_scope"),
    )


def _orientation_object(value: object, path: str) -> OrientationObjectReference:
    item = _mapping(value, path)
    return OrientationObjectReference(
        object_id=_text(item.get("object_id"), f"{path}.object_id"),
        object_version=_text(item.get("object_version"), f"{path}.object_version"),
        object_kind=_text(item.get("object_kind"), f"{path}.object_kind"),
        source_owner=_text(item.get("source_owner"), f"{path}.source_owner"),
        source_ref=_text(item.get("source_ref"), f"{path}.source_ref"),
        source_revision=_text(item.get("source_revision"), f"{path}.source_revision"),
        identity_scope=cast(
            IdentityScope,
            _text(item.get("identity_scope"), f"{path}.identity_scope"),
        ),
        representation_refs=_texts(
            item.get("representation_refs", ()),
            f"{path}.representation_refs",
        ),
        integrity_ref=_integrity(item.get("integrity_ref"), f"{path}.integrity_ref"),
        access_status=cast(
            AccessStatus | None,
            _optional_text(item.get("access_status"), f"{path}.access_status"),
        ),
        provenance_gaps=(
            _texts(item.get("provenance_gaps"), f"{path}.provenance_gaps")
            if item.get("provenance_gaps") is not None
            else None
        ),
    )


def _integrity(value: object, path: str) -> IntegrityReference | None:
    if value is None:
        return None
    item = _mapping(value, path)
    verified = item.get("verified")
    if verified not in {True, False, "unknown"}:
        raise GatewayInputError(f"{path}.verified", "must be true, false, or unknown")
    return IntegrityReference(
        _text(item.get("method"), f"{path}.method"),
        _text(item.get("value"), f"{path}.value"),
        _text(item.get("coverage"), f"{path}.coverage"),
        cast(bool | str, verified),
    )


def _intention(value: object) -> Intention:
    item = _mapping(value, "intention")
    return Intention(
        _text(item.get("direction"), "intention.direction"),
        _optional_text(item.get("focus"), "intention.focus"),
        _optional_text(item.get("success_boundary"), "intention.success_boundary"),
    )


def _scope(value: object) -> Scope:
    item = _mapping(value, "scope")
    return Scope(
        _texts(item.get("include"), "scope.include"),
        _texts(item.get("exclude"), "scope.exclude"),
        _texts(item.get("unresolved"), "scope.unresolved"),
        _optional_text(item.get("depth"), "scope.depth"),
        _optional_text(item.get("breadth"), "scope.breadth"),
        _optional_text(item.get("time_boundary"), "scope.time_boundary"),
    )


def _clarification_reference(value: object) -> ClarificationReference | None:
    if value is None:
        return None
    item = _mapping(value, "clarification_of")
    return ClarificationReference(
        _text(item.get("result_id"), "clarification_of.result_id"),
        _text(item.get("result_version"), "clarification_of.result_version"),
    )


def _continuation_reference(value: object) -> ContinuationReference | None:
    if value is None:
        return None
    item = _mapping(value, "continuation_of")
    return ContinuationReference(
        _text(item.get("option_id"), "continuation_of.option_id"),
        _text(item.get("option_version"), "continuation_of.option_version"),
        _text(item.get("source_report_id"), "continuation_of.source_report_id"),
        _text(item.get("source_report_version"), "continuation_of.source_report_version"),
    )


def _mapping(value: object, path: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping) or not all(isinstance(key, str) for key in value):
        raise GatewayInputError(path, "must be an object with string field names")
    return cast(Mapping[str, object], value)


def _sequence(value: object, path: str) -> Sequence[object]:
    if not isinstance(value, (list, tuple)):
        raise GatewayInputError(path, "must be a list")
    return value


def _text(value: object, path: str) -> str:
    if not isinstance(value, str):
        raise GatewayInputError(path, "must be text")
    return value


def _optional_text(value: object, path: str) -> str | None:
    if value is None:
        return None
    return _text(value, path)


def _texts(value: object, path: str) -> tuple[str, ...]:
    items = _sequence(value, path)
    return tuple(_text(item, f"{path}[{index}]") for index, item in enumerate(items))


def _public_mapping(value: object, path: str) -> Mapping[str, PublicValue]:
    item = _mapping(value, path)
    return {
        key: _public_value(nested, f"{path}.{key}")
        for key, nested in item.items()
    }


def _public_value(value: object, path: str) -> PublicValue:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, (list, tuple)):
        return tuple(
            _public_value(nested, f"{path}[{index}]")
            for index, nested in enumerate(value)
        )
    if isinstance(value, Mapping):
        return _public_mapping(value, path)
    raise GatewayInputError(path, "must contain only public contract values")


__all__ = ["GatewayInputError", "construct_orientation_request"]
