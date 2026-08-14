"""Gateway validation for frozen Version 1.1 wire contracts."""

from __future__ import annotations

from dataclasses import asdict
from hashlib import sha256
from typing import Any, Mapping

from orion.public_contracts import (
    ClarificationIssue,
    ClarificationReference,
    ClarificationResult,
    ContinuationReference,
    ContractSet,
    HumanAuthorityReference,
    IntegrityReference,
    Intention,
    NO_EFFECTS,
    OrientationObjectReference,
    OrientationRequest,
    RequesterReference,
    Scope,
    validate_clarification_result,
    validate_contract_set,
    validate_orientation_request,
)

from .canonical import canonical_bytes, digest_ref
from .constants import (
    API_VERSION,
    LINEAGE_SCHEMA,
    MATERIAL_SCHEMA,
    MAX_CONTENT_BYTES,
    MAX_LINEAGE_BYTES,
    MAX_LINEAGE_DEPTH,
    MAX_SOURCE_LINES,
)
from .errors import RuntimeBoundaryError


ENVELOPE_FIELDS = {
    "api_version",
    "request",
    "confirmed_material",
    "lineage",
    "evidence",
}
REQUEST_REQUIRED = {
    "schema_version",
    "request_id",
    "request_version",
    "mode",
    "requested_by",
    "human_authority",
    "orientation_objects",
    "intention",
    "scope",
    "effects",
}
REQUEST_OPTIONAL = {
    "audience",
    "constraints",
    "evidence_policy",
    "representation_preferences",
    "depth_budget",
    "prior_report_refs",
    "human_annotations",
    "clarification_of",
    "continuation_of",
    "mode_parameters",
    "consumer_context",
}


def _mapping(value: object, path: str) -> Mapping[str, Any]:
    if not isinstance(value, dict):
        _invalid(path, "object_required")
    return value


def _exact(
    value: object,
    required: set[str],
    optional: set[str],
    path: str,
) -> Mapping[str, Any]:
    item = _mapping(value, path)
    keys = set(item)
    missing = required - keys
    unknown = keys - required - optional
    if missing:
        _invalid(path, f"missing:{','.join(sorted(missing))}")
    if unknown:
        _invalid(path, f"unknown:{','.join(sorted(unknown))}")
    return item


def _text(value: object, path: str) -> str:
    if not isinstance(value, str) or not value.strip():
        _invalid(path, "non_empty_text_required")
    return value


def _strings(value: object, path: str) -> tuple[str, ...]:
    if not isinstance(value, list):
        _invalid(path, "array_required")
    result = tuple(_text(item, f"{path}[{index}]") for index, item in enumerate(value))
    return result


def _invalid(path: str, rule: str, *, lineage: bool = False) -> None:
    raise RuntimeBoundaryError(
        status=422,
        category="lineage_validation" if lineage else "request_validation",
        code="contract_invalid",
        detail_refs=(f"{path}:{rule}",),
    )


def _profile_invalid(path: str, *, lineage: bool = False) -> None:
    raise RuntimeBoundaryError(
        status=422,
        category="lineage_validation" if lineage else "request_validation",
        code="operational_profile_exceeded",
        detail_refs=(path,),
    )


def parse_orientation_request(value: object) -> OrientationRequest:
    item = _exact(value, REQUEST_REQUIRED, REQUEST_OPTIONAL, "request")
    requester = _exact(
        item["requested_by"],
        {"requester_id", "requester_kind", "authority_domain"},
        set(),
        "request.requested_by",
    )
    authority = _exact(
        item["human_authority"],
        {"human_ref", "authority_scope"},
        set(),
        "request.human_authority",
    )
    objects_raw = item["orientation_objects"]
    if not isinstance(objects_raw, list) or len(objects_raw) != 1:
        _invalid("request.orientation_objects", "exactly_one_required")
    objects = tuple(_parse_orientation_object(obj, index) for index, obj in enumerate(objects_raw))
    intention = _exact(
        item["intention"],
        {"direction"},
        {"focus", "success_boundary"},
        "request.intention",
    )
    scope = _exact(
        item["scope"],
        {"include", "exclude", "unresolved"},
        {"depth", "breadth", "time_boundary"},
        "request.scope",
    )
    clarification = None
    if item.get("clarification_of") is not None:
        ref = _exact(
            item["clarification_of"],
            {"result_id", "result_version"},
            set(),
            "request.clarification_of",
        )
        clarification = ClarificationReference(
            _text(ref["result_id"], "request.clarification_of.result_id"),
            _text(ref["result_version"], "request.clarification_of.result_version"),
        )
    continuation = None
    if item.get("continuation_of") is not None:
        ref = _exact(
            item["continuation_of"],
            {"option_id", "option_version", "source_report_id", "source_report_version"},
            set(),
            "request.continuation_of",
        )
        continuation = ContinuationReference(
            *(
                _text(ref[name], f"request.continuation_of.{name}")
                for name in (
                    "option_id",
                    "option_version",
                    "source_report_id",
                    "source_report_version",
                )
            )
        )
    request = OrientationRequest(
        schema_version=_text(item["schema_version"], "request.schema_version"),
        request_id=_text(item["request_id"], "request.request_id"),
        request_version=_text(item["request_version"], "request.request_version"),
        mode=_text(item["mode"], "request.mode"),
        requested_by=RequesterReference(
            _text(requester["requester_id"], "request.requested_by.requester_id"),
            _text(requester["requester_kind"], "request.requested_by.requester_kind"),
            _text(requester["authority_domain"], "request.requested_by.authority_domain"),
        ),
        human_authority=HumanAuthorityReference(
            _text(authority["human_ref"], "request.human_authority.human_ref"),
            _strings(authority["authority_scope"], "request.human_authority.authority_scope"),
        ),
        orientation_objects=objects,
        intention=Intention(
            _text(intention["direction"], "request.intention.direction"),
            intention.get("focus"),
            intention.get("success_boundary"),
        ),
        scope=Scope(
            _strings(scope["include"], "request.scope.include"),
            _strings(scope["exclude"], "request.scope.exclude"),
            _strings(scope["unresolved"], "request.scope.unresolved"),
            scope.get("depth"),
            scope.get("breadth"),
            scope.get("time_boundary"),
        ),
        effects=_text(item["effects"], "request.effects"),
        audience=item.get("audience"),
        constraints=_strings(item.get("constraints", []), "request.constraints"),
        evidence_policy=item.get("evidence_policy"),
        representation_preferences=_strings(
            item.get("representation_preferences", []),
            "request.representation_preferences",
        ),
        depth_budget=item.get("depth_budget"),
        prior_report_refs=_strings(item.get("prior_report_refs", []), "request.prior_report_refs"),
        human_annotations=_strings(item.get("human_annotations", []), "request.human_annotations"),
        clarification_of=clarification,
        continuation_of=continuation,
        mode_parameters=_mapping(item.get("mode_parameters", {}), "request.mode_parameters"),
        consumer_context=_mapping(item.get("consumer_context", {}), "request.consumer_context"),
    )
    result = validate_orientation_request(request)
    if not result.valid:
        issue = result.errors[0]
        _invalid(f"request.{issue.path}", issue.code)
    return request


def _parse_orientation_object(value: object, index: int) -> OrientationObjectReference:
    path = f"request.orientation_objects[{index}]"
    item = _exact(
        value,
        {
            "object_id",
            "object_version",
            "object_kind",
            "source_owner",
            "source_ref",
            "source_revision",
            "identity_scope",
        },
        {"representation_refs", "integrity_ref", "access_status", "provenance_gaps"},
        path,
    )
    integrity = None
    if item.get("integrity_ref") is not None:
        ref = _exact(
            item["integrity_ref"],
            {"method", "value", "coverage", "verified"},
            set(),
            f"{path}.integrity_ref",
        )
        integrity = IntegrityReference(
            _text(ref["method"], f"{path}.integrity_ref.method"),
            _text(ref["value"], f"{path}.integrity_ref.value"),
            _text(ref["coverage"], f"{path}.integrity_ref.coverage"),
            ref["verified"],
        )
    gaps = item.get("provenance_gaps")
    return OrientationObjectReference(
        object_id=_text(item["object_id"], f"{path}.object_id"),
        object_version=_text(item["object_version"], f"{path}.object_version"),
        object_kind=_text(item["object_kind"], f"{path}.object_kind"),
        source_owner=_text(item["source_owner"], f"{path}.source_owner"),
        source_ref=_text(item["source_ref"], f"{path}.source_ref"),
        source_revision=_text(item["source_revision"], f"{path}.source_revision"),
        identity_scope=_text(item["identity_scope"], f"{path}.identity_scope"),
        representation_refs=_strings(item.get("representation_refs", []), f"{path}.representation_refs"),
        integrity_ref=integrity,
        access_status=item.get("access_status"),
        provenance_gaps=None if gaps is None else _strings(gaps, f"{path}.provenance_gaps"),
    )


def validate_confirmed_material(value: object, request: OrientationRequest) -> dict[str, Any]:
    material = _exact(
        value,
        {
            "schema_version",
            "orientation_object_id",
            "orientation_object_version",
            "source",
            "confirmation",
        },
        set(),
        "confirmed_material",
    )
    if material["schema_version"] != MATERIAL_SCHEMA:
        _invalid("confirmed_material.schema_version", "unsupported")
    source = _exact(
        material["source"],
        {
            "entry_id",
            "source_owner",
            "source_ref",
            "source_version",
            "fragment_ref",
            "media_type",
            "grammar",
            "grammar_version",
            "content",
            "integrity_sha256",
        },
        set(),
        "confirmed_material.source",
    )
    confirmation = _exact(
        material["confirmation"],
        {"confirmed_by", "confirmed_revision", "confirmation_id"},
        set(),
        "confirmed_material.confirmation",
    )
    for name in ("orientation_object_id", "orientation_object_version"):
        _text(material[name], f"confirmed_material.{name}")
    for name in ("entry_id", "source_owner", "source_ref", "source_version", "content", "integrity_sha256"):
        if name == "content":
            if not isinstance(source[name], str):
                _invalid(f"confirmed_material.source.{name}", "text_required")
        else:
            _text(source[name], f"confirmed_material.source.{name}")
    if source["fragment_ref"] != "whole":
        _invalid("confirmed_material.source.fragment_ref", "must_equal_whole")
    if source["media_type"] != "text/markdown;charset=utf-8":
        _invalid("confirmed_material.source.media_type", "unsupported")
    if source["grammar"] != "CommonMark" or source["grammar_version"] != "0.31.2":
        _invalid("confirmed_material.source.grammar", "unsupported")
    content = source["content"]
    if "\ufeff" in content[:1] or "\x00" in content or "\r" in content:
        _invalid("confirmed_material.source.content", "encoding_or_newline")
    try:
        content_bytes = content.encode("utf-8", errors="strict")
    except UnicodeEncodeError:
        _invalid("confirmed_material.source.content", "invalid_utf8")
    if len(content_bytes) > MAX_CONTENT_BYTES or len(content.splitlines()) > MAX_SOURCE_LINES:
        _profile_invalid("confirmed_material.source.content")
    integrity = sha256(content_bytes).hexdigest()
    if source["integrity_sha256"] != integrity:
        _invalid("confirmed_material.source.integrity_sha256", "mismatch")
    if source["source_version"] != f"sha256:{integrity}":
        _invalid("confirmed_material.source.source_version", "mismatch")
    if not isinstance(confirmation["confirmed_revision"], int) or isinstance(
        confirmation["confirmed_revision"], bool
    ) or not 1 <= confirmation["confirmed_revision"] <= 2_147_483_647:
        _invalid("confirmed_material.confirmation.confirmed_revision", "range")
    _text(confirmation["confirmed_by"], "confirmed_material.confirmation.confirmed_by")
    basis = {
        "orientation_object_id": material["orientation_object_id"],
        "orientation_object_version": material["orientation_object_version"],
        "source_id": source["entry_id"],
        "source_revision": source["source_version"],
        "confirmed_by": confirmation["confirmed_by"],
        "confirmed_revision": confirmation["confirmed_revision"],
        "boundary_ref": "whole",
    }
    expected_confirmation = f"confirmation-{sha256(canonical_bytes(basis)).hexdigest()[:16]}"
    if confirmation["confirmation_id"] != expected_confirmation:
        _invalid("confirmed_material.confirmation.confirmation_id", "mismatch")
    obj = request.orientation_objects[0]
    if (
        material["orientation_object_id"] != obj.object_id
        or material["orientation_object_version"] != obj.object_version
        or source["source_owner"] != obj.source_owner
        or source["source_ref"] != obj.source_ref
        or source["source_version"] != obj.source_revision
    ):
        _invalid("confirmed_material", "request_material_mismatch")
    return dict(material)


def parse_clarification_result(value: object, index: int) -> ClarificationResult:
    path = f"lineage.clarifications[{index}]"
    item = _exact(
        value,
        {
            "schema_version",
            "result_id",
            "result_version",
            "request_id",
            "request_version",
            "request_schema_version",
            "mode",
            "readiness",
            "issues",
            "retained_context",
            "required_user_actions",
            "effects",
        },
        set(),
        path,
    )
    raw_issues = item["issues"]
    if not isinstance(raw_issues, list):
        _invalid(f"{path}.issues", "array_required", lineage=True)
    issues = []
    for issue_index, raw in enumerate(raw_issues):
        issue_path = f"{path}.issues[{issue_index}]"
        issue = _exact(
            raw,
            {
                "issue_id",
                "issue_code",
                "field_path",
                "priority_tier",
                "reason",
                "expected_value",
                "current_value_refs",
                "required_action",
                "blocking",
            },
            {"allowed_values", "conflicts_with"},
            issue_path,
        )
        issues.append(
            ClarificationIssue(
                issue_id=_text(issue["issue_id"], f"{issue_path}.issue_id"),
                issue_code=_text(issue["issue_code"], f"{issue_path}.issue_code"),
                field_path=_text(issue["field_path"], f"{issue_path}.field_path"),
                priority_tier=_text(issue["priority_tier"], f"{issue_path}.priority_tier"),
                reason=_text(issue["reason"], f"{issue_path}.reason"),
                expected_value=_text(issue["expected_value"], f"{issue_path}.expected_value"),
                current_value_refs=_strings(issue["current_value_refs"], f"{issue_path}.current_value_refs"),
                required_action=_text(issue["required_action"], f"{issue_path}.required_action"),
                blocking=issue["blocking"],
                allowed_values=None if issue.get("allowed_values") is None else _strings(issue["allowed_values"], f"{issue_path}.allowed_values"),
                conflicts_with=None if issue.get("conflicts_with") is None else _strings(issue["conflicts_with"], f"{issue_path}.conflicts_with"),
            )
        )
    retained_raw = _mapping(item["retained_context"], f"{path}.retained_context")
    result = ClarificationResult(
        schema_version=_text(item["schema_version"], f"{path}.schema_version"),
        result_id=_text(item["result_id"], f"{path}.result_id"),
        result_version=_text(item["result_version"], f"{path}.result_version"),
        request_id=_text(item["request_id"], f"{path}.request_id"),
        request_version=_text(item["request_version"], f"{path}.request_version"),
        request_schema_version=_text(item["request_schema_version"], f"{path}.request_schema_version"),
        mode=_text(item["mode"], f"{path}.mode"),
        readiness=_text(item["readiness"], f"{path}.readiness"),
        issues=tuple(issues),
        retained_context={
            str(key): _strings(value, f"{path}.retained_context.{key}")
            for key, value in retained_raw.items()
        },
        required_user_actions=_strings(item["required_user_actions"], f"{path}.required_user_actions"),
        effects=_text(item["effects"], f"{path}.effects"),
    )
    validation = validate_clarification_result(result)
    if not validation.valid:
        issue = validation.errors[0]
        _invalid(f"{path}.{issue.path}", issue.code, lineage=True)
    return result


def validate_lineage(
    value: object,
    current: OrientationRequest,
) -> dict[str, Any]:
    lineage = _exact(
        value,
        {"schema_version", "requests", "clarifications"},
        set(),
        "lineage",
    )
    if lineage["schema_version"] != LINEAGE_SCHEMA:
        _invalid("lineage.schema_version", "unsupported", lineage=True)
    requests_raw = lineage["requests"]
    clarifications_raw = lineage["clarifications"]
    if not isinstance(requests_raw, list) or not isinstance(clarifications_raw, list):
        _invalid("lineage", "arrays_required", lineage=True)
    if len(requests_raw) != len(clarifications_raw):
        _invalid("lineage", "depth_or_cardinality", lineage=True)
    if len(requests_raw) > MAX_LINEAGE_DEPTH:
        _profile_invalid("lineage.depth", lineage=True)
    if len(canonical_bytes(lineage)) > MAX_LINEAGE_BYTES:
        _profile_invalid("lineage.size", lineage=True)
    if current.clarification_of is None:
        if requests_raw or clarifications_raw:
            _invalid("lineage", "unrelated_history", lineage=True)
        return dict(lineage)
    if not requests_raw:
        _invalid("lineage", "required_chain_missing", lineage=True)
    try:
        requests = tuple(parse_orientation_request(item) for item in requests_raw)
    except RuntimeBoundaryError as exc:
        raise RuntimeBoundaryError(
            status=422,
            category="lineage_validation",
            code="contract_invalid",
            detail_refs=exc.detail_refs,
        ) from exc
    clarifications = tuple(
        parse_clarification_result(item, index)
        for index, item in enumerate(clarifications_raw)
    )
    for index, (request, clarification) in enumerate(zip(requests, clarifications)):
        if (
            clarification.request_id != request.request_id
            or clarification.request_version != request.request_version
            or clarification.request_schema_version != request.schema_version
            or clarification.mode != request.mode
        ):
            _invalid(f"lineage[{index}]", "request_result_mismatch", lineage=True)
        if index and (
            request.clarification_of is None
            or request.clarification_of.result_id != clarifications[index - 1].result_id
            or request.clarification_of.result_version != clarifications[index - 1].result_version
        ):
            _invalid(f"lineage.requests[{index}]", "chain_gap", lineage=True)
    final = clarifications[-1]
    if (
        current.clarification_of.result_id != final.result_id
        or current.clarification_of.result_version != final.result_version
    ):
        _invalid("request.clarification_of", "final_reference_mismatch", lineage=True)
    request_keys = [(item.request_id, item.request_version) for item in requests]
    result_keys = [(item.result_id, item.result_version) for item in clarifications]
    if len(set(request_keys)) != len(request_keys) or len(set(result_keys)) != len(result_keys):
        _invalid("lineage", "duplicate_identity", lineage=True)
    set_validation = validate_contract_set(
        ContractSet(requests=(*requests, current), clarifications=clarifications)
    )
    if not set_validation.valid:
        issue = set_validation.errors[0]
        _invalid(f"lineage.{issue.path}", issue.code, lineage=True)
    return dict(lineage)


def validate_envelope(value: object) -> tuple[dict[str, Any], OrientationRequest, str]:
    envelope = _exact(value, ENVELOPE_FIELDS, set(), "envelope")
    if envelope["api_version"] != API_VERSION:
        raise RuntimeBoundaryError(
            status=400,
            category="version",
            code="api_version_unsupported",
        )
    if envelope["evidence"] != []:
        _invalid("evidence", "must_be_empty")
    request = parse_orientation_request(envelope["request"])
    material = validate_confirmed_material(envelope["confirmed_material"], request)
    lineage = validate_lineage(envelope["lineage"], request)
    canonical_envelope = {
        "api_version": API_VERSION,
        "request": asdict(request),
        "confirmed_material": material,
        "lineage": lineage,
        "evidence": [],
    }
    request_digest = digest_ref(canonical_bytes(canonical_envelope))
    return canonical_envelope, request, request_digest
