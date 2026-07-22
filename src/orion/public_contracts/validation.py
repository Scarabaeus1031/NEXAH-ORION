"""Contract-only validation for the frozen ORION public contract suite."""

from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Iterable

from .models import *  # noqa: F403 - the validator covers the complete public model


MODES = {"wonder", "understand", "compare", "connect", "explore", "build", "reflect"}
ACCESS = {"available", "restricted", "unavailable", "unknown"}
MODE_OUTPUTS = {
    "wonder": {"attention_signal", "observed_features", "repetitions_and_contrasts", "candidate_patterns", "candidate_questions", "possible_frames", "related_observations", "counterexamples", "unknowns", "evidence_map", "confidence_profile", "suggested_continuations"},
    "understand": {"orientation_summary", "key_concepts", "conceptual_structure", "claims_and_support", "evidence_map", "assumptions", "dependencies", "uncertainties", "contradictions", "open_questions", "scope_coverage", "confidence_profile", "suggested_continuations"},
    "compare": {"comparison_subjects", "comparison_lens", "comparison_axes", "subject_profiles", "comparison_matrix", "similarities", "differences", "tensions", "not_comparable", "evidence_by_subject", "evidence_asymmetries", "assumptions_and_limits", "confidence_by_axis", "suggested_continuations"},
    "connect": {"anchors", "relation_scope", "shared_elements", "candidate_connections", "bridge_paths", "intermediary_nodes", "relation_types", "evidence_by_edge", "counterevidence", "broken_or_unknown_edges", "preserved_differences", "confidence_by_connection", "suggested_continuations"},
    "explore": {"starting_point", "exploration_budget", "orientation_map", "landmarks", "branches", "visited_trail", "unvisited_frontier", "unavailable_or_unknown_regions", "evidence_by_route", "coverage_gaps", "stop_conditions", "confidence_profile", "suggested_continuations"},
    "build": {"build_intent", "purpose_and_outcomes", "requirements", "constraints", "assumptions", "capability_and_boundary_map", "dependencies_and_interfaces", "alternatives_and_tradeoffs", "decisions_required", "authority_owners", "risks_and_unknowns", "milestones", "verification_conditions", "evidence_traceability", "suggested_continuations"},
    "reflect": {"reflection_subject", "prior_reference", "current_reference", "human_annotations_verbatim", "system_observed_changes", "unchanged_elements", "added_and_removed_elements", "open_questions", "evidence_revisited", "unresolved_assumptions_and_blockers", "human_meaning", "confidence_profile", "suggested_continuations"},
}
MODE_STAGE_COUNTS = {"wonder": 9, "understand": 11, "compare": 10, "connect": 10, "explore": 10, "build": 10, "reflect": 10}


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    code: str
    path: str
    message: str


@dataclass(frozen=True, slots=True)
class ContractValidationResult:
    errors: tuple[ValidationIssue, ...]

    @property
    def valid(self) -> bool:
        return not self.errors


@dataclass(frozen=True, slots=True)
class ContractSet:
    requests: tuple[OrientationRequest, ...] = ()
    clarifications: tuple[ClarificationResult, ...] = ()
    reports: tuple[OrientationReport, ...] = ()
    continuations: tuple[ContinuationOption, ...] = ()
    evidence: tuple[EvidenceReference, ...] = ()
    runtime_errors: tuple[RuntimeError, ...] = ()


class _Checks:
    def __init__(self) -> None:
        self.errors: list[ValidationIssue] = []

    def require(self, condition: bool, code: str, path: str, message: str) -> None:
        if not condition:
            self.errors.append(ValidationIssue(code, path, message))

    def text(self, value: object, path: str) -> None:
        self.require(isinstance(value, str) and bool(value.strip()), "required_text", path, "must be non-empty text")

    def unique(self, values: Iterable[object], path: str) -> None:
        frozen = tuple(values)
        self.require(len(frozen) == len(set(frozen)), "duplicate", path, "values must be unique")

    def finish(self) -> ContractValidationResult:
        return ContractValidationResult(tuple(self.errors))


def _texts(c: _Checks, values: Iterable[object], path: str) -> None:
    values = tuple(values)
    for index, value in enumerate(values):
        c.text(value, f"{path}[{index}]")
    c.unique(values, path)


def _ref(value: str) -> tuple[str, str] | None:
    if "@" not in value:
        return None
    identity, version = value.rsplit("@", 1)
    return (identity, version) if identity and version else None


def _path_exists(root: object, path: str) -> bool:
    current = root
    for match in re.finditer(r"(?:^|\.)([^.\[]+)|\[([0-9]+)\]", path):
        name, index = match.groups()
        if name is not None:
            if isinstance(current, dict):
                if name not in current:
                    return False
                current = current[name]
            elif hasattr(current, name):
                current = getattr(current, name)
            else:
                return False
        else:
            if not isinstance(current, (tuple, list)) or int(index) >= len(current):
                return False
            current = current[int(index)]
    return True


def _validate_integrity(c: _Checks, item: IntegrityReference, path: str) -> None:
    for name in ("method", "value", "coverage"):
        c.text(getattr(item, name), f"{path}.{name}")
    c.require(item.verified in {True, False, "unknown"}, "enum", f"{path}.verified", "must be true, false, or unknown")


def validate_orientation_request(item: OrientationRequest) -> ContractValidationResult:
    c = _Checks()
    c.require(item.schema_version == ORIENTATION_REQUEST_SCHEMA, "schema_version", "schema_version", "unsupported Orientation Request schema")
    for name in ("request_id", "request_version"):
        c.text(getattr(item, name), name)
    c.require(item.mode in MODES, "mode", "mode", "unknown Orientation Mode")
    for name in ("requester_id", "authority_domain"):
        c.text(getattr(item.requested_by, name), f"requested_by.{name}")
    c.require(item.requested_by.requester_kind in {"human", "authorized_consumer"}, "enum", "requested_by.requester_kind", "invalid requester kind")
    c.text(item.human_authority.human_ref, "human_authority.human_ref")
    _texts(c, item.human_authority.authority_scope, "human_authority.authority_scope")
    c.require({"intention", "scope", "continuation"}.issubset(item.human_authority.authority_scope), "authority_scope", "human_authority.authority_scope", "must preserve intention, scope, and continuation")
    object_keys = []
    for index, obj in enumerate(item.orientation_objects):
        p = f"orientation_objects[{index}]"
        for name in ("object_id", "object_version", "object_kind", "source_owner", "source_ref", "source_revision"):
            c.text(getattr(obj, name), f"{p}.{name}")
        c.require(obj.identity_scope in {"canonical", "external", "session_local"}, "enum", f"{p}.identity_scope", "invalid identity scope")
        if obj.access_status is not None:
            c.require(obj.access_status in ACCESS, "enum", f"{p}.access_status", "invalid access status")
        _texts(c, obj.representation_refs, f"{p}.representation_refs")
        if obj.provenance_gaps is not None:
            _texts(c, obj.provenance_gaps, f"{p}.provenance_gaps")
        if obj.integrity_ref:
            _validate_integrity(c, obj.integrity_ref, f"{p}.integrity_ref")
        object_keys.append((obj.object_id, obj.object_version))
    c.unique(object_keys, "orientation_objects")
    c.text(item.intention.direction, "intention.direction")
    for name in ("focus", "success_boundary"):
        value = getattr(item.intention, name)
        if value is not None:
            c.text(value, f"intention.{name}")
    for name in ("include", "exclude", "unresolved"):
        _texts(c, getattr(item.scope, name), f"scope.{name}")
    for name in ("depth", "breadth", "time_boundary"):
        value = getattr(item.scope, name)
        if value is not None:
            c.text(value, f"scope.{name}")
    c.require(item.effects == NO_EFFECTS, "effects", "effects", "version 1.0 permits no effects")
    _texts(c, item.prior_report_refs, "prior_report_refs")
    for ref in item.prior_report_refs:
        c.require(_ref(ref) is not None, "versioned_ref", "prior_report_refs", "report references require identity and version")
    if item.clarification_of:
        c.text(item.clarification_of.result_id, "clarification_of.result_id")
        c.text(item.clarification_of.result_version, "clarification_of.result_version")
    if item.continuation_of:
        for name in ("option_id", "option_version", "source_report_id", "source_report_version"):
            c.text(getattr(item.continuation_of, name), f"continuation_of.{name}")
    return c.finish()


def validate_clarification_result(item: ClarificationResult) -> ContractValidationResult:
    c = _Checks()
    c.require(item.schema_version == CLARIFICATION_RESULT_SCHEMA, "schema_version", "schema_version", "unsupported Clarification Result schema")
    for name in ("result_id", "result_version", "request_id", "request_version"):
        c.text(getattr(item, name), name)
    c.require(item.request_schema_version == ORIENTATION_REQUEST_SCHEMA, "request_schema", "request_schema_version", "must reference Orientation Request 1.0")
    c.require(item.mode in MODES, "mode", "mode", "unknown Orientation Mode")
    c.require(item.readiness == "clarification_required", "readiness", "readiness", "must be clarification_required")
    c.require(bool(item.issues), "issues", "issues", "at least one issue is required")
    codes = {"missing_required", "ambiguous_value", "identity_unresolved", "cardinality_incomplete", "scope_unresolved", "choice_required", "confirmation_required", "access_required", "conflicting_values"}
    actions = {"provide", "choose", "confirm", "correct", "add_object", "authorize_access", "remove_conflict", "withhold"}
    tier_order = {"authority": 0, "identity": 1, "intention": 2, "scope": 3, "required_parameter": 4}
    keys = []
    issue_ids = []
    for index, issue in enumerate(item.issues):
        p = f"issues[{index}]"
        for name in ("issue_id", "field_path", "reason", "expected_value"):
            c.text(getattr(issue, name), f"{p}.{name}")
        c.require(issue.issue_code in codes, "issue_code", f"{p}.issue_code", "unknown clarification issue code")
        c.require(issue.priority_tier in tier_order, "priority_tier", f"{p}.priority_tier", "invalid version 1.0 priority tier")
        c.require(issue.required_action in actions, "required_action", f"{p}.required_action", "unknown Human action")
        c.require(issue.blocking is True, "blocking", f"{p}.blocking", "version 1.0 issues must block")
        issue_ids.append(issue.issue_id)
        keys.append((tier_order.get(issue.priority_tier, 99), issue.field_path, issue.issue_id))
    c.unique(issue_ids, "issues.issue_id")
    c.require(keys == sorted(keys), "issue_order", "issues", "issues are not in canonical order")
    c.require(item.required_user_actions == tuple(issue_ids), "user_actions", "required_user_actions", "must reference each issue in canonical order")
    c.require(item.effects == NO_EFFECTS, "effects", "effects", "version 1.0 permits no effects")
    return c.finish()


def validate_evidence_reference(item: EvidenceReference) -> ContractValidationResult:
    c = _Checks()
    c.require(item.schema_version == EVIDENCE_REFERENCE_SCHEMA, "schema_version", "schema_version", "unsupported Evidence Reference schema")
    for name in ("evidence_id", "evidence_version"):
        c.text(getattr(item, name), name)
    for name in ("source_id", "source_version", "identity_domain", "source_owner", "source_ref"):
        c.text(getattr(item.source, name), f"source.{name}")
    c.require(item.evidence_id != item.source.source_id, "identity", "evidence_id", "evidence identity and source identity must remain distinct")
    if item.source.integrity_ref:
        _validate_integrity(c, item.source.integrity_ref, "source.integrity_ref")
    for name in ("authority_owner", "authority_domain", "authority_version"):
        c.text(getattr(item.authority, name), f"authority.{name}")
    c.require(item.authority.editorial_status in {"draft", "reviewed", "published", "withdrawn", "unclassified", "unknown"}, "editorial_status", "authority.editorial_status", "invalid editorial status")
    c.require(item.evidence_class in {"observed", "derived", "proposed", "unknown"}, "evidence_class", "evidence_class", "invalid evidence class")
    c.require(item.relationship in {"supports", "counters", "contextualizes", "limits"}, "relationship", "relationship", "invalid evidence relationship")
    step_ids = []
    for index, step in enumerate(item.provenance):
        p = f"provenance[{index}]"
        for name in ("step_id", "output_ref", "owner"):
            c.text(getattr(step, name), f"{p}.{name}")
        c.require(step.step_kind in {"source", "representation", "transition", "derivation", "proposal"}, "step_kind", f"{p}.step_kind", "invalid provenance step kind")
        c.require((step.contract_id is None) == (step.contract_version is None), "contract_pair", p, "contract ID and version must appear together")
        c.require(step.lossiness == "none" or step.lossiness == "unknown" or isinstance(step.lossiness, tuple), "lossiness", f"{p}.lossiness", "lossiness must be none, unknown, or declared items")
        step_ids.append(step.step_id)
    c.unique(step_ids, "provenance.step_id")
    if item.evidence_class == "observed":
        c.require(item.source.fragment_ref is not None and any(s.step_kind == "source" for s in item.provenance), "observed_provenance", "provenance", "observed evidence requires an inspectable source fragment")
    if item.evidence_class == "derived":
        c.require(any(s.step_kind in {"transition", "derivation"} and s.contract_id for s in item.provenance), "derived_provenance", "provenance", "derived evidence requires a versioned governing rule")
    c.require(item.validation.status in {"valid", "invalid", "unverified"}, "validation_status", "validation.status", "invalid Evidence Validation status")
    if item.validation.status == "valid":
        c.require(bool(item.validation.checks) and not item.validation.issues, "valid_evidence", "validation", "valid evidence requires checks and no issues")
    c.require(bool(item.validation.validated_against), "validated_against", "validation.validated_against", "validation basis is required")
    c.require(bool(item.traceability), "traceability", "traceability", "at least one target is required")
    trace_keys = []
    for index, target in enumerate(item.traceability):
        for name in ("report_id", "report_version", "target_path"):
            c.text(getattr(target, name), f"traceability[{index}].{name}")
        trace_keys.append((target.report_id, target.report_version, target.target_path))
    c.unique(trace_keys, "traceability")
    c.require(item.access_status in ACCESS, "access_status", "access_status", "invalid access status")
    scale = (item.evidence_level, item.evidence_scale_id, item.evidence_scale_version)
    c.require(all(v is None for v in scale) or all(v is not None for v in scale), "evidence_scale", "evidence_scale", "evidence scale fields must appear together")
    return c.finish()


def validate_orientation_report(item: OrientationReport) -> ContractValidationResult:
    c = _Checks()
    c.require(item.schema_version == ORIENTATION_REPORT_SCHEMA, "schema_version", "schema_version", "unsupported Orientation Report schema")
    for name in ("report_id", "report_version", "request_id", "request_version", "operator_id", "operator_version"):
        c.text(getattr(item.identity, name), f"identity.{name}")
    c.require(item.identity.request_schema_version == ORIENTATION_REQUEST_SCHEMA, "request_schema", "identity.request_schema_version", "must reference Orientation Request 1.0")
    c.require(item.lifecycle.state in {"current", "superseded", "withdrawn"}, "lifecycle", "lifecycle.state", "invalid lifecycle state")
    c.require(item.lifecycle.state != "superseded" or item.lifecycle.replacement_ref is not None, "replacement", "lifecycle.replacement_ref", "superseded reports require replacement")
    c.require(item.lifecycle.state != "withdrawn" or item.lifecycle.reason is not None, "withdrawal_reason", "lifecycle.reason", "withdrawn reports require reason")
    c.require(item.status in {"complete", "partial", "blocked"}, "status", "status", "invalid report status")
    c.require(item.orientation.mode in MODES, "mode", "orientation.mode", "unknown mode")
    c.require(item.mode_payload.mode == item.orientation.mode, "mode", "mode_payload.mode", "payload mode must match orientation mode")
    c.require(item.identity.operator_id == f"orion.orientation-operator/{item.orientation.mode}", "operator", "identity.operator_id", "operator must match mode")
    c.text(item.orientation.human_authority_ref, "orientation.human_authority_ref")
    _texts(c, item.orientation.orientation_object_refs, "orientation.orientation_object_refs")
    required = MODE_OUTPUTS.get(item.orientation.mode, set())
    c.require(required.issubset(item.mode_payload.content), "mode_payload", "mode_payload.content", "required operator output sections are missing")
    stage_ids = []
    blocked_stages = []
    for index, stage in enumerate(item.process):
        expected = f"{item.orientation.mode}/{index + 1}"
        c.require(stage.stage_id == expected, "stage_order", f"process[{index}].stage_id", f"expected {expected}")
        c.require(stage.state in {"completed", "skipped", "blocked"}, "stage_state", f"process[{index}].state", "invalid stage state")
        c.require(stage.state == "completed" or bool(stage.reason), "stage_reason", f"process[{index}].reason", "skipped and blocked stages require reason")
        stage_ids.append(stage.stage_id)
        if stage.state == "blocked":
            blocked_stages.append(stage.stage_id)
    c.require(bool(item.process), "process", "process", "public process stages are required")
    c.require(len(item.process) == MODE_STAGE_COUNTS.get(item.orientation.mode), "stage_count", "process", "process must contain every public Orientation Operator stage")
    c.require(item.validation.contract_validation == "valid", "contract_validation", "validation.contract_validation", "an issued report must be contract-valid")
    ov = item.validation.orientation_validation
    c.require(ov.status in {"valid", "invalid"}, "orientation_validation", "validation.orientation_validation.status", "invalid status")
    c.require(item.confidence.orientation_validation_status == ov.status, "validation_alignment", "confidence.orientation_validation_status", "must match Orientation Validation")
    c.require(item.confidence.source_coverage in {"complete", "partial", "unknown"}, "coverage", "confidence.source_coverage", "invalid coverage")
    c.require(item.confidence.evidence_coverage in {"complete", "partial", "unknown"}, "coverage", "confidence.evidence_coverage", "invalid coverage")
    c.require(item.confidence.inference_status in {"none", "proposed_present"}, "inference", "confidence.inference_status", "invalid inference status")
    issue_ids = tuple(issue.issue_id for issue in item.issues)
    c.unique(issue_ids, "issues.issue_id")
    issue_kinds = {"missing_contract", "missing_transition_operator", "missing_renderer", "missing_evidence", "unavailable_source", "unknown_representation", "incompatible_version", "violated_invariant", "validation_failure", "policy_boundary"}
    for issue in item.issues:
        c.require(issue.kind in issue_kinds, "issue_kind", issue.issue_id, "unknown report issue kind")
    c.unique((a.assumption_id for a in item.assumptions), "assumptions.assumption_id")
    c.unique((u.uncertainty_id for u in item.uncertainties), "uncertainties.uncertainty_id")
    for assumption in item.assumptions:
        c.require(assumption.status in {"declared", "contested", "invalidated"}, "assumption_status", assumption.assumption_id, "invalid assumption status")
    for uncertainty in item.uncertainties:
        c.require(uncertainty.status in {"open", "bounded", "irreducible"}, "uncertainty_status", uncertainty.uncertainty_id, "invalid uncertainty status")
    if item.status == "complete":
        c.require(not blocked_stages and all(s.state == "completed" for s in item.process), "complete_process", "process", "complete reports require completed stages")
        c.require(ov.status == "valid", "complete_validation", "validation.orientation_validation", "complete reports require valid orientation")
        c.require(not any(i.blocking for i in item.issues), "complete_blocker", "issues", "complete reports cannot contain blocking issues")
        c.require(bool(item.evidence), "complete_evidence", "evidence", "complete reports require Evidence References")
    if item.status == "blocked":
        c.require(bool(blocked_stages), "blocked_stage", "process", "blocked reports require a blocked stage")
        c.require(any(i.blocking for i in item.issues), "blocked_issue", "issues", "blocked reports require a blocking issue")
        c.require(bool(ov.absent_outputs), "absent_output", "validation.orientation_validation.absent_outputs", "blocked reports require absent outputs")
    c.require(item.effects == NO_EFFECTS, "effects", "effects", "version 1.0 permits no effects")
    for path, refs in (("evidence", item.evidence), ("continuations", item.continuations)):
        _texts(c, refs, path)
        for ref in refs:
            c.require(_ref(ref) is not None, "versioned_ref", path, "references require identity and version")
    return c.finish()


def validate_continuation_option(item: ContinuationOption) -> ContractValidationResult:
    c = _Checks()
    c.require(item.schema_version == CONTINUATION_OPTION_SCHEMA, "schema_version", "schema_version", "unsupported Continuation Option schema")
    for name in ("option_id", "option_version", "source_report_id", "source_report_version"):
        c.text(getattr(item, name), name)
    actions = {"inspect_report", "inspect_evidence", "refine_intention", "narrow_scope", "expand_scope", "add_object", "follow_representation", "switch_mode", "open_atlas", "handoff", "pause"}
    c.require(item.action_type in actions, "action_type", "action_type", "unknown action type")
    _texts(c, item.reason_refs, "reason_refs")
    c.require(bool(item.reason_refs), "reason_refs", "reason_refs", "report-grounded justification is required")
    if item.target_mode is not None:
        c.require(item.target_mode in MODES, "target_mode", "target_mode", "unknown target mode")
    c.require(item.action_type != "handoff" or (item.target_boundary is not None and item.target_mode is None), "handoff_target", "target_boundary", "handoff requires only a target boundary")
    _texts(c, item.preserved_context.report_refs, "preserved_context.report_refs")
    source_ref = f"{item.source_report_id}@{item.source_report_version}"
    c.require(source_ref in item.preserved_context.report_refs, "source_report", "preserved_context.report_refs", "source report must be preserved")
    for name in ("intention_ref", "scope_ref", "human_authority_ref"):
        c.text(getattr(item.preserved_context, name), f"preserved_context.{name}")
    operations = {"preserve", "set", "add", "remove", "require", "confirm"}
    for index, delta in enumerate(item.request_delta):
        p = f"request_delta[{index}]"
        c.require(delta.operation in operations, "delta_operation", f"{p}.operation", "unknown Request Delta operation")
        c.text(delta.field_path, f"{p}.field_path")
        c.text(delta.reason_ref, f"{p}.reason_ref")
        c.require((delta.value_ref is None) != (delta.required_value_kind is None), "delta_value", p, "exactly one value form is required")
        c.require(delta.human_confirmation in {"required", "not_required"}, "confirmation", f"{p}.human_confirmation", "invalid confirmation value")
        if delta.operation in {"require", "confirm"} or delta.field_path == "mode" or delta.field_path.startswith(("scope", "orientation_objects", "intention", "human_authority")):
            c.require(delta.human_confirmation == "required", "human_authority", f"{p}.human_confirmation", "Human-controlled changes require confirmation")
    if item.action_type in {"inspect_report", "inspect_evidence", "open_atlas", "handoff", "pause"} and item.request_delta:
        c.require(item.target_mode is not None, "orientation_delta", "target_mode", "a non-empty Request Delta must explicitly start another orientation")
    c.require(item.availability in {"available", "clarification_required", "blocked", "future"}, "availability", "availability", "invalid availability")
    c.require(item.availability == "blocked" or not item.blockers, "blockers", "blockers", "blockers require blocked availability")
    c.require(item.availability != "blocked" or bool(item.blockers), "blockers", "blockers", "blocked availability requires blockers")
    allowed_actions = {"select_option", "confirm_mode", "confirm_scope_change", "provide_required_field", "add_object", "choose_alternative", "authorize_separate_handoff", "pause", "decline"}
    c.require(set(item.required_user_actions).issubset(allowed_actions), "user_actions", "required_user_actions", "unknown Human action")
    c.require(item.effects == NO_EFFECTS, "effects", "effects", "version 1.0 permits no effects")
    return c.finish()


def validate_runtime_error(item: RuntimeError) -> ContractValidationResult:
    c = _Checks()
    c.require(item.schema_version == RUNTIME_ERROR_SCHEMA, "schema_version", "schema_version", "unsupported Runtime Error schema")
    for name in ("error_id", "error_version", "reason_code"):
        c.text(getattr(item, name), name)
    kinds = {"unsupported", "blocked", "invalid", "unavailable", "clarification_required", "validation_failed", "internal_failure"}
    stages = {"contract_validation", "readiness_validation", "processing", "report_contract_validation", "continuation_validation", "availability"}
    c.require(item.kind in kinds, "kind", "kind", "unknown Runtime Error kind")
    c.require(item.stage in stages, "stage", "stage", "unknown public stage")
    request_fields = (item.request_id, item.request_version, item.request_schema_version)
    c.require(all(v is None for v in request_fields) or all(v is not None for v in request_fields), "request_identity", "request_id", "request identity fields must appear together")
    if item.request_schema_version is not None:
        c.require(item.request_schema_version == ORIENTATION_REQUEST_SCHEMA, "request_schema", "request_schema_version", "must reference Orientation Request 1.0")
    c.require(item.result_presence in {"none", "clarification_result"}, "result_presence", "result_presence", "invalid result presence")
    c.require((item.result_presence == "clarification_result") == (item.result_ref is not None), "result_ref", "result_ref", "Clarification Result presence and reference must agree")
    c.require((item.kind == "clarification_required") == (item.result_presence == "clarification_result"), "clarification_result", "result_presence", "Clarification Required must carry exactly one Clarification Result")
    c.require(item.kind != "blocked" or item.stage in {"contract_validation", "readiness_validation", "availability"}, "blocked_stage", "stage", "Runtime Error blocked must occur before Processing")
    c.require(item.kind != "validation_failed" or item.stage == "report_contract_validation", "validation_stage", "stage", "Validation Failed belongs to Report Contract Validation")
    c.require(item.retry.disposition in {"never", "after_user_action", "after_state_change", "safe", "manual_review"}, "retry", "retry.disposition", "invalid retry disposition")
    retry_by_kind = {
        "unsupported": {"never", "after_user_action", "after_state_change"},
        "blocked": {"after_user_action", "after_state_change"},
        "invalid": {"after_user_action", "manual_review"},
        "unavailable": {"after_state_change", "safe"},
        "clarification_required": {"after_user_action"},
        "validation_failed": {"after_state_change", "manual_review"},
        "internal_failure": {"safe", "after_state_change", "manual_review"},
    }
    c.require(item.retry.disposition in retry_by_kind.get(item.kind, set()), "retry_kind", "retry.disposition", "retry behavior does not conform to outcome kind")
    c.require(item.request_id is None or item.continuation.preserve_request_context, "preserve_request", "continuation.preserve_request_context", "accepted request context must be preserved")
    c.require(not item.continuation.allowed or (item.source_report_ref is not None and bool(item.continuation.option_refs)), "continuation", "continuation", "allowed Continuation Options require a source report and refs")
    c.require(item.continuation.allowed or not item.continuation.option_refs, "continuation", "continuation.option_refs", "disallowed continuation must have no refs")
    c.require(item.effects == NO_EFFECTS, "effects", "effects", "version 1.0 permits no effects")
    return c.finish()


def validate_public_contract(item: PublicContract) -> ContractValidationResult:
    validators = {
        OrientationRequest: validate_orientation_request,
        ClarificationResult: validate_clarification_result,
        EvidenceReference: validate_evidence_reference,
        OrientationReport: validate_orientation_report,
        ContinuationOption: validate_continuation_option,
        RuntimeError: validate_runtime_error,
    }
    validator = validators.get(type(item))
    if validator is None:
        return ContractValidationResult((ValidationIssue("contract_type", "", "unknown public contract type"),))
    return validator(item)  # type: ignore[arg-type]


def validate_contract_set(items: ContractSet) -> ContractValidationResult:
    c = _Checks()
    groups = (items.requests, items.clarifications, items.reports, items.continuations, items.evidence, items.runtime_errors)
    for group in groups:
        for item in group:
            result = validate_public_contract(item)
            c.errors.extend(result.errors)
    request_index = {(x.request_id, x.request_version): x for x in items.requests}
    report_index = {(x.identity.report_id, x.identity.report_version): x for x in items.reports}
    clarification_index = {(x.result_id, x.result_version): x for x in items.clarifications}
    continuation_index = {(x.option_id, x.option_version): x for x in items.continuations}
    evidence_index = {(x.evidence_id, x.evidence_version): x for x in items.evidence}
    for name, group, index in (("request", items.requests, request_index), ("report", items.reports, report_index), ("clarification", items.clarifications, clarification_index), ("continuation", items.continuations, continuation_index), ("evidence", items.evidence, evidence_index)):
        c.require(len(group) == len(index), "duplicate_identity", name, f"duplicate {name} identity and version")
    for clarification in items.clarifications:
        request = request_index.get((clarification.request_id, clarification.request_version))
        c.require(request is not None, "request_ref", clarification.result_id, "originating Orientation Request not found")
        if request:
            c.require(request.mode == clarification.mode and request.schema_version == clarification.request_schema_version, "request_lineage", clarification.result_id, "Clarification Result request lineage differs")
            retained_objects = clarification.retained_context.get("orientation_objects", ())
            known_objects = {f"{x.object_id}@{x.object_version}" for x in request.orientation_objects}
            c.require(set(retained_objects).issubset(known_objects), "retained_context", clarification.result_id, "Clarification Result retained unknown Orientation Objects")
    for report in items.reports:
        identity = report.identity
        request = request_index.get((identity.request_id, identity.request_version))
        c.require(request is not None, "request_ref", identity.report_id, "originating Orientation Request not found")
        if request:
            expected_intention = request.intention if isinstance(report.orientation.intention, Intention) else request.intention.direction
            c.require(report.orientation.mode == request.mode, "mode_lineage", identity.report_id, "report mode differs from request")
            c.require(report.orientation.intention == expected_intention, "intention_lineage", identity.report_id, "report Intention differs from request")
            c.require(report.orientation.scope == request.scope, "scope_lineage", identity.report_id, "report Scope differs from request")
            c.require(report.orientation.human_authority_ref == f"{request.request_id}@{request.request_version}.human_authority", "authority_lineage", identity.report_id, "Human authority reference differs")
            expected_objects = tuple(f"{x.object_id}@{x.object_version}" for x in request.orientation_objects)
            c.require(report.orientation.orientation_object_refs == expected_objects, "object_lineage", identity.report_id, "Orientation Object lineage differs")
        for ref in report.evidence:
            parsed = _ref(ref)
            evidence = evidence_index.get(parsed) if parsed else None
            c.require(evidence is not None, "evidence_ref", identity.report_id, f"Evidence Reference not found: {ref}")
            if evidence:
                c.require(any(t.report_id == identity.report_id and t.report_version == identity.report_version for t in evidence.traceability), "evidence_trace", ref, "Evidence Reference does not trace to report")
                for target in evidence.traceability:
                    if (target.report_id, target.report_version) == (identity.report_id, identity.report_version):
                        c.require(_path_exists(report, target.target_path), "evidence_path", target.target_path, "Evidence Reference target path does not exist")
        for ref in report.continuations:
            parsed = _ref(ref)
            option = continuation_index.get(parsed) if parsed else None
            c.require(option is not None, "continuation_ref", identity.report_id, f"Continuation Option not found: {ref}")
            if option:
                c.require((option.source_report_id, option.source_report_version) == (identity.report_id, identity.report_version), "continuation_source", ref, "Continuation Option source report differs")
    for option in items.continuations:
        report = report_index.get((option.source_report_id, option.source_report_version))
        c.require(report is not None, "source_report", option.option_id, "source report not found")
        if report:
            p = option.preserved_context
            c.require(p.orientation_object_refs == report.orientation.orientation_object_refs, "preserved_objects", option.option_id, "Orientation Objects were lost or changed")
            c.require(p.scope_ref == f"{report.identity.request_id}@{report.identity.request_version}.scope", "preserved_scope", option.option_id, "Scope lineage differs")
            c.require(p.intention_ref == f"{report.identity.request_id}@{report.identity.request_version}.intention", "preserved_intention", option.option_id, "Intention lineage differs")
            c.require(p.human_authority_ref == report.orientation.human_authority_ref, "preserved_authority", option.option_id, "Human authority lineage differs")
            c.require(p.evidence_refs == report.evidence, "preserved_evidence", option.option_id, "Evidence References were silently changed")
            c.require(f"{report.identity.report_id}@{report.identity.report_version}" in p.report_refs, "preserved_report", option.option_id, "source report identity was lost")
            for reason_ref in option.reason_refs:
                c.require(_path_exists(report, reason_ref), "reason_ref", reason_ref, "Continuation Option reason path does not exist in source report")
            known_provenance = set()
            for evidence_ref in p.evidence_refs:
                parsed = _ref(evidence_ref)
                evidence = evidence_index.get(parsed) if parsed else None
                if evidence:
                    known_provenance.update(step.step_id for step in evidence.provenance)
                    known_provenance.update(step.output_ref for step in evidence.provenance)
            c.require(set(p.provenance_refs).issubset(known_provenance), "preserved_provenance", option.option_id, "provenance reference is not carried by preserved Evidence References")
    for error in items.runtime_errors:
        if error.request_id is not None:
            c.require((error.request_id, error.request_version) in request_index, "request_ref", error.error_id, "Runtime Error request not found")
        if error.result_ref:
            parsed = _ref(error.result_ref)
            clarification = clarification_index.get(parsed) if parsed else None
            c.require(clarification is not None, "clarification_ref", error.error_id, "Clarification Result not found")
            if clarification:
                c.require((error.request_id, error.request_version) == (clarification.request_id, clarification.request_version), "clarification_lineage", error.error_id, "Runtime Error and Clarification Result request lineage differs")
                c.require(error.issues == tuple(x.issue_id for x in clarification.issues), "clarification_issues", error.error_id, "Runtime Error issue refs differ from Clarification Result")
        if error.source_report_ref:
            parsed = _ref(error.source_report_ref)
            c.require(parsed in report_index, "source_report", error.error_id, "Runtime Error source report not found")
            for ref in error.continuation.option_refs:
                option_ref = _ref(ref)
                option = continuation_index.get(option_ref) if option_ref else None
                c.require(option is not None and parsed == (option.source_report_id, option.source_report_version), "continuation_ref", error.error_id, "Runtime Error continuation does not belong to source report")
    for request in items.requests:
        if request.clarification_of:
            key = (request.clarification_of.result_id, request.clarification_of.result_version)
            clarification = clarification_index.get(key)
            c.require(clarification is not None, "clarification_of", request.request_id, "Clarification Result not found")
        if request.continuation_of:
            ref = request.continuation_of
            option = continuation_index.get((ref.option_id, ref.option_version))
            c.require(option is not None, "continuation_of", request.request_id, "Continuation Option not found")
            if option:
                c.require((ref.source_report_id, ref.source_report_version) == (option.source_report_id, option.source_report_version), "continuation_lineage", request.request_id, "source report lineage differs")
    return c.finish()
