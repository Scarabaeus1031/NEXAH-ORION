"""Canonical Phase III fixtures derived from the frozen contract examples."""

from __future__ import annotations

from .models import *  # noqa: F403 - fixtures intentionally exercise the full suite


REQUESTER = RequesterReference("nexahedron-alpha", "authorized_consumer", "nexahedron.local-session")
AUTHORITY = HumanAuthorityReference("human-alpha", ("intention", "scope", "continuation"))
OBJECT = OrientationObjectReference(
    object_id="object-paper-01",
    object_version="1",
    object_kind="Research Paper",
    source_owner="author-team-01",
    source_ref="source-paper-01",
    source_revision="3",
    identity_scope="external",
    representation_refs=("representation-paper-01@1",),
    access_status="available",
)
INTENTION = Intention("Understand the structure and evidence of this paper.", "structure and evidence")
SCOPE = Scope(("claims", "structure", "evidence"), ("implementation advice",), (), depth="focused")


def _request(request_id: str, *, obj: OrientationObjectReference = OBJECT) -> OrientationRequest:
    return OrientationRequest(
        schema_version=ORIENTATION_REQUEST_SCHEMA,
        request_id=request_id,
        request_version="1",
        mode="understand",
        requested_by=REQUESTER,
        human_authority=AUTHORITY,
        orientation_objects=(obj,),
        intention=INTENTION,
        scope=SCOPE,
        effects=NO_EFFECTS,
    )


VALID_REQUEST = _request("request-understand-valid-01")
COMPLETE_REQUEST = _request("request-understand-complete-01")
PARTIAL_REQUEST = _request("request-understand-partial-01")
BLOCKED_REPORT_REQUEST = _request("request-understand-blocked-report-01")
BLOCKED_BEFORE_REQUEST = _request(
    "request-understand-blocked-before-01",
    obj=OrientationObjectReference(
        object_id="object-restricted-01",
        object_version="1",
        object_kind="Document",
        source_owner="source-owner-01",
        source_ref="restricted-source-01",
        source_revision="1",
        identity_scope="external",
        access_status="restricted",
    ),
)
UNSUPPORTED_REQUEST = _request(
    "request-understand-unsupported-01",
    obj=OrientationObjectReference(
        object_id="object-unsupported-01",
        object_version="1",
        object_kind="Unsupported Object Kind",
        source_owner="source-owner-01",
        source_ref="unsupported-source-01",
        source_revision="1",
        identity_scope="external",
        access_status="available",
    ),
)
ERROR_REQUEST = _request("request-understand-error-01")

CLARIFICATION_REQUEST = OrientationRequest(
    schema_version=ORIENTATION_REQUEST_SCHEMA,
    request_id="request-compare-clarification-01",
    request_version="1",
    mode="compare",
    requested_by=REQUESTER,
    human_authority=AUTHORITY,
    orientation_objects=(OBJECT,),
    intention=Intention("Compare these theories."),
    scope=Scope((), (), ("second comparison subject", "comparison lens")),
    effects=NO_EFFECTS,
)

CLARIFICATION_REQUIRED = ClarificationResult(
    schema_version=CLARIFICATION_RESULT_SCHEMA,
    result_id="clarification-compare-01",
    result_version="1",
    request_id=CLARIFICATION_REQUEST.request_id,
    request_version=CLARIFICATION_REQUEST.request_version,
    request_schema_version=CLARIFICATION_REQUEST.schema_version,
    mode="compare",
    readiness="clarification_required",
    issues=(
        ClarificationIssue("issue-object-02", "cardinality_incomplete", "orientation_objects[1]", "identity", "compare_requires_two_objects", "one Orientation Object Reference", ("object-paper-01@1",), "add_object", True),
        ClarificationIssue("issue-lens-01", "missing_required", "mode_parameters.comparison_lens", "scope", "comparison_lens_required", "one approved comparison lens", (), "provide", True),
    ),
    retained_context={"orientation_objects": ("object-paper-01@1",)},
    required_user_actions=("issue-object-02", "issue-lens-01"),
    effects=NO_EFFECTS,
)


def _understand_content(summary: str, *, coverage: str, evidence: tuple[str, ...]) -> dict[str, object]:
    return {
        "orientation_summary": summary,
        "key_concepts": ("structure", "evidence"),
        "conceptual_structure": "claim and support structure",
        "claims_and_support": evidence,
        "evidence_map": evidence,
        "assumptions": (),
        "dependencies": (),
        "uncertainties": (),
        "contradictions": (),
        "open_questions": (),
        "scope_coverage": coverage,
        "confidence_profile": coverage,
        "suggested_continuations": (),
    }


def _stages(state: str) -> tuple[ProcessStage, ...]:
    stages = []
    for number in range(1, 12):
        if state == "complete":
            stages.append(ProcessStage(f"understand/{number}", "completed"))
        elif state == "partial" and number in {9, 10}:
            stages.append(ProcessStage(f"understand/{number}", "skipped", reason="outside_confirmed_depth"))
        elif state == "blocked" and number == 6:
            stages.append(ProcessStage(f"understand/{number}", "blocked", issue_refs=("issue-missing-evidence-01",), reason="required_evidence_unavailable"))
        elif state == "blocked" and 7 <= number <= 9:
            stages.append(ProcessStage(f"understand/{number}", "skipped", reason="evidence_binding_incomplete"))
        else:
            stages.append(ProcessStage(f"understand/{number}", "completed"))
    return tuple(stages)


def _orientation(request: OrientationRequest) -> ReportOrientation:
    return ReportOrientation(
        mode=request.mode,
        intention=request.intention,
        human_authority_ref=f"{request.request_id}@{request.request_version}.human_authority",
        scope=request.scope,
        orientation_object_refs=tuple(f"{x.object_id}@{x.object_version}" for x in request.orientation_objects),
    )


def _representations(absent: bool = False) -> ReportRepresentations:
    return ReportRepresentations(
        input=("representation-paper-01@1",),
        working=("understanding-frame-01@1",),
        produced=("understanding-frame-01@1",),
        requested_but_absent=(AbsentRepresentation("Evidence-bound Understanding Frame", ("issue-missing-evidence-01",)),) if absent else (),
    )


EVIDENCE = EvidenceReference(
    schema_version=EVIDENCE_REFERENCE_SCHEMA,
    evidence_id="evidence-complete-01",
    evidence_version="1",
    source=SourceReference("paper-01", "3", "library.publications", "author-team-01", "source-paper-01", "section-4.paragraph-2"),
    authority=AuthorityDeclaration("library-editorial", "library.publications", "published", "7"),
    evidence_class="observed",
    relationship="supports",
    provenance=(ProvenanceStep("source-step-01", "source", (), "source-paper-01-section-4-paragraph-2", "author-team-01", "none"),),
    validation=EvidenceValidation("valid", ("source_resolved", "version_resolved", "fragment_resolved"), (), (EVIDENCE_REFERENCE_SCHEMA,)),
    traceability=(TraceabilityTarget("report-understand-complete-01", "1", "mode_payload.content.claims_and_support[0]", "finding-claim-01"),),
    access_status="available",
)

CONTINUATION = ContinuationOption(
    schema_version=CONTINUATION_OPTION_SCHEMA,
    option_id="continuation-understand-evidence-01",
    option_version="1",
    source_report_id="report-understand-complete-01",
    source_report_version="1",
    action_type="inspect_evidence",
    reason_refs=("mode_payload.content.claims_and_support[0]", "evidence[0]"),
    target_mode="understand",
    preserved_context=PreservedContext(
        ("object-paper-01@1",),
        f"{COMPLETE_REQUEST.request_id}@1.intention",
        f"{COMPLETE_REQUEST.request_id}@1.scope",
        f"{COMPLETE_REQUEST.request_id}@1.human_authority",
        ("report-understand-complete-01@1",),
        ("representation-paper-01@1",),
        ("evidence-complete-01@1",),
        (),
        (),
    ),
    request_delta=(RequestDeltaOperation("intention.focus", "set", "mode_payload.content.claims_and_support[0]", "required", value_ref="evidence-complete-01@1"),),
    availability="available",
    blockers=(),
    required_user_actions=("select_option",),
    effects=NO_EFFECTS,
)


def _report(
    request: OrientationRequest,
    report_id: str,
    status: str,
) -> OrientationReport:
    complete = status == "complete"
    blocked = status == "blocked"
    evidence = ("evidence-complete-01@1",) if complete else ()
    issues = ()
    uncertainties = ()
    absent_outputs = ()
    orientation_status = "valid"
    if blocked:
        issues = (ReportIssue("issue-missing-evidence-01", "missing_evidence", "understand/6", "no traceable evidence is available", ("mode_payload.content.conceptual_structure",), (), True, "traceable source evidence becomes available"),)
        uncertainties = (ReportUncertainty("uncertainty-evidence-gap-01", "evidence_gap", ("mode_payload.content.conceptual_structure",), ("issue-missing-evidence-01",), "open", "provide traceable source evidence"),)
        absent_outputs = ("Evidence-bound Understanding Frame",)
        orientation_status = "invalid"
    if status == "partial":
        uncertainties = (ReportUncertainty("uncertainty-depth-01", "bounded_scope", ("mode_payload.content.scope_coverage",), (), "bounded", "expand Scope"),)
    return OrientationReport(
        schema_version=ORIENTATION_REPORT_SCHEMA,
        identity=ReportIdentity(report_id, "1", request.request_id, request.request_version, request.schema_version, "orion.orientation-operator/understand", "0.1-draft"),
        lifecycle=ReportLifecycle("current"),
        status=status,
        orientation=_orientation(request),
        representations=_representations(blocked),
        process=_stages(status),
        mode_payload=ModePayload("understand", "0.1-draft", _understand_content(f"{status} understanding", coverage="complete" if complete else "partial", evidence=evidence)),
        evidence=evidence,
        assumptions=(),
        uncertainties=uncertainties,
        issues=issues,
        confidence=ConfidenceProfile("complete", "complete" if complete else "partial", orientation_status, "none", tuple(x.uncertainty_id for x in uncertainties), () if complete else ("evidence-gap",)),
        validation=ReportValidation("valid", OrientationValidation(orientation_status, ("object_bound", "scope_conformant"), ("missing_evidence",) if blocked else (), (), ("identity", "provenance"), (), absent_outputs)),
        continuations=("continuation-understand-evidence-01@1",) if complete else (),
        effects=NO_EFFECTS,
    )


COMPLETE_REPORT = _report(COMPLETE_REQUEST, "report-understand-complete-01", "complete")
PARTIAL_REPORT = _report(PARTIAL_REQUEST, "report-understand-partial-01", "partial")
BLOCKED_REPORT = _report(BLOCKED_REPORT_REQUEST, "report-understand-blocked-01", "blocked")


def _runtime_error(error_id: str, kind: str, request: OrientationRequest, stage: str, reason: str, retry: str) -> RuntimeError:
    return RuntimeError(
        schema_version=RUNTIME_ERROR_SCHEMA,
        error_id=error_id,
        error_version="1",
        kind=kind,
        request_id=request.request_id,
        request_version=request.request_version,
        request_schema_version=request.schema_version,
        stage=stage,
        reason_code=reason,
        issues=(),
        result_presence="none",
        retry=RetryPolicy(retry, retry == "safe", ()),
        continuation=ContinuationPolicy(False, (), True, retry == "after_user_action"),
        consumer_behavior={"present_kind": True, "preserve_request": True, "present_as_completed": False},
        effects=NO_EFFECTS,
    )


UNSUPPORTED = _runtime_error("error-unsupported-01", "unsupported", UNSUPPORTED_REQUEST, "readiness_validation", "object_kind_unsupported", "never")
BLOCKED_BEFORE_PROCESSING = _runtime_error("error-blocked-before-01", "blocked", BLOCKED_BEFORE_REQUEST, "readiness_validation", "source_access_restricted", "after_user_action")
RUNTIME_ERROR = _runtime_error("error-internal-01", "internal_failure", ERROR_REQUEST, "processing", "public_outcome_unavailable", "manual_review")
CLARIFICATION_REQUIRED_ERROR = RuntimeError(
    schema_version=RUNTIME_ERROR_SCHEMA,
    error_id="error-clarification-01",
    error_version="1",
    kind="clarification_required",
    request_id=CLARIFICATION_REQUEST.request_id,
    request_version=CLARIFICATION_REQUEST.request_version,
    request_schema_version=CLARIFICATION_REQUEST.schema_version,
    stage="readiness_validation",
    reason_code="required_human_values_missing",
    issues=("issue-object-02", "issue-lens-01"),
    result_presence="clarification_result",
    result_ref="clarification-compare-01@1",
    retry=RetryPolicy("after_user_action", False, ("issue-object-02", "issue-lens-01")),
    continuation=ContinuationPolicy(False, (), True, True),
    consumer_behavior={"present_clarification_result": True, "preserve_valid_fields": True, "auto_complete_actions": False},
    effects=NO_EFFECTS,
)

CANONICAL_CONTRACT_SET = (
    VALID_REQUEST,
    COMPLETE_REQUEST,
    PARTIAL_REQUEST,
    BLOCKED_REPORT_REQUEST,
    BLOCKED_BEFORE_REQUEST,
    UNSUPPORTED_REQUEST,
    ERROR_REQUEST,
    CLARIFICATION_REQUEST,
    CLARIFICATION_REQUIRED,
    EVIDENCE,
    COMPLETE_REPORT,
    PARTIAL_REPORT,
    BLOCKED_REPORT,
    CONTINUATION,
    UNSUPPORTED,
    BLOCKED_BEFORE_PROCESSING,
    RUNTIME_ERROR,
    CLARIFICATION_REQUIRED_ERROR,
)
