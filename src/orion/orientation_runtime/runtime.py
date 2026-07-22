"""The minimal in-process ORION Runtime for the Understand operator only.

The runtime consumes and returns only frozen Version 1.0 public contracts.  It
contains no transport, persistence, provider, prompt, or gateway behavior.
"""

from __future__ import annotations

from orion.public_contracts import (
    CLARIFICATION_RESULT_SCHEMA,
    CONTINUATION_OPTION_SCHEMA,
    NO_EFFECTS,
    ORIENTATION_REPORT_SCHEMA,
    ORIENTATION_REQUEST_SCHEMA,
    RUNTIME_ERROR_SCHEMA,
    AbsentRepresentation,
    ClarificationIssue,
    ClarificationResult,
    ConfidenceProfile,
    ContinuationOption,
    ContinuationPolicy,
    ContractSet,
    EvidenceReference,
    ModePayload,
    OrientationReport,
    OrientationRequest,
    OrientationValidation,
    PreservedContext,
    ProcessStage,
    PublicContract,
    ReportIdentity,
    ReportIssue,
    ReportLifecycle,
    ReportOrientation,
    ReportRepresentations,
    ReportUncertainty,
    ReportValidation,
    RetryPolicy,
    RuntimeError,
    validate_contract_set,
    validate_evidence_reference,
    validate_orientation_request,
    validate_public_contract,
)


class OrientationRuntime:
    """Execute one deterministic, evidence-bound Understand orientation."""

    operator_id = "orion.orientation-operator/understand"
    operator_version = "0.1-draft"

    def orient(
        self,
        request: OrientationRequest,
        evidence: tuple[EvidenceReference, ...] = (),
    ) -> tuple[PublicContract, ...]:
        """Return validated public outcomes; never expose an internal exception."""

        try:
            return self._orient(request, evidence)
        except Exception:
            # The public boundary communicates failure behavior, not Python
            # exception types or internal execution details.
            return (self._validated_internal_failure(request),)

    def _orient(
        self,
        request: OrientationRequest,
        evidence: tuple[EvidenceReference, ...],
    ) -> tuple[PublicContract, ...]:
        request_validation = validate_orientation_request(request)
        if not request_validation.valid:
            issues = tuple(error.code for error in request_validation.errors)
            outcome = self._error(request, "invalid", "contract_validation", "orientation_request_invalid", issues, "after_user_action")
            return self._validated_error(outcome, request)

        if request.mode != "understand":
            outcome = self._error(request, "unsupported", "readiness_validation", "orientation_mode_unsupported", (), "never")
            return self._publish(ContractSet(requests=(request,), runtime_errors=(outcome,)), (outcome,), request)

        clarification = self._clarification(request)
        if clarification is not None:
            outcome = RuntimeError(
                schema_version=RUNTIME_ERROR_SCHEMA,
                error_id=f"error-clarification-{request.request_id}-{request.request_version}",
                error_version="1",
                kind="clarification_required",
                request_id=request.request_id,
                request_version=request.request_version,
                request_schema_version=request.schema_version,
                stage="readiness_validation",
                reason_code="required_human_values_missing",
                issues=tuple(issue.issue_id for issue in clarification.issues),
                result_presence="clarification_result",
                result_ref=f"{clarification.result_id}@{clarification.result_version}",
                retry=RetryPolicy("after_user_action", False, tuple(issue.issue_id for issue in clarification.issues)),
                continuation=ContinuationPolicy(False, (), True, True),
                consumer_behavior={"present_clarification_result": True, "preserve_valid_fields": True, "auto_complete_actions": False},
                effects=NO_EFFECTS,
            )
            graph = ContractSet(requests=(request,), clarifications=(clarification,), runtime_errors=(outcome,))
            return self._publish(graph, (outcome, clarification), request)

        orientation_object = request.orientation_objects[0]
        if orientation_object.access_status in {"restricted", "unavailable"}:
            outcome = self._error(request, "blocked", "readiness_validation", "orientation_object_access_blocked", (orientation_object.source_ref,), "after_user_action")
            return self._publish(ContractSet(requests=(request,), runtime_errors=(outcome,)), (outcome,), request)

        report_id = self._report_id(request)
        usable_evidence = tuple(
            item
            for item in evidence
            if validate_evidence_reference(item).valid
            and item.validation.status == "valid"
            and item.access_status == "available"
            and item.source.source_ref == orientation_object.source_ref
            and item.source.source_version == orientation_object.source_revision
            and any(target.report_id == report_id and target.report_version == "1" for target in item.traceability)
        )
        if not usable_evidence:
            report = self._blocked_report(request, report_id)
            return self._publish(ContractSet(requests=(request,), reports=(report,)), (report,), request)

        continuation = self._continuation(request, report_id, usable_evidence)
        report = self._complete_report(request, report_id, usable_evidence, continuation)
        graph = ContractSet(
            requests=(request,),
            reports=(report,),
            continuations=(continuation,),
            evidence=usable_evidence,
        )
        return self._publish(graph, (report, continuation), request)

    def _clarification(self, request: OrientationRequest) -> ClarificationResult | None:
        issues: list[ClarificationIssue] = []
        if len(request.orientation_objects) != 1:
            issues.append(ClarificationIssue("issue-primary-object", "cardinality_incomplete", "orientation_objects", "identity", "understand_requires_exactly_one_primary_object", "one Orientation Object Reference", tuple(f"{x.object_id}@{x.object_version}" for x in request.orientation_objects), "choose" if request.orientation_objects else "add_object", True))
        else:
            obj = request.orientation_objects[0]
            if obj.object_version == "unknown" or obj.source_revision == "unknown":
                issues.append(ClarificationIssue("issue-object-version", "identity_unresolved", "orientation_objects[0].object_version", "identity", "source_version_required", "exact object and source version", (f"{obj.object_id}@{obj.object_version}",), "provide", True))
            if obj.access_status in {None, "unknown"}:
                issues.append(ClarificationIssue("issue-source-access", "access_required", "orientation_objects[0].access_status", "authority", "source_access_requires_confirmation", "available, restricted, or unavailable", (), "authorize_access", True))
        if request.scope.unresolved:
            issues.append(ClarificationIssue("issue-scope", "scope_unresolved", "scope.unresolved", "scope", "consequential_scope_boundaries_unresolved", "confirmed Scope", request.scope.unresolved, "confirm", True))
        if not request.scope.include:
            issues.append(ClarificationIssue("issue-scope-include", "missing_required", "scope.include", "scope", "understand_requires_part_or_whole_scope", "at least one included subject boundary", (), "provide", True))
        if request.scope.depth is None:
            issues.append(ClarificationIssue("issue-depth", "missing_required", "scope.depth", "required_parameter", "understand_requires_bounded_depth", "bounded depth profile", (), "provide", True))
        if not issues:
            return None
        tier = {"authority": 0, "identity": 1, "intention": 2, "scope": 3, "required_parameter": 4}
        ordered = tuple(sorted(issues, key=lambda issue: (tier[issue.priority_tier], issue.field_path, issue.issue_id)))
        retained = {
            "orientation_objects": tuple(f"{x.object_id}@{x.object_version}" for x in request.orientation_objects),
            "intention": (f"{request.request_id}@{request.request_version}.intention",),
        }
        return ClarificationResult(
            schema_version=CLARIFICATION_RESULT_SCHEMA,
            result_id=f"clarification-{request.request_id}-{request.request_version}",
            result_version="1",
            request_id=request.request_id,
            request_version=request.request_version,
            request_schema_version=request.schema_version,
            mode="understand",
            readiness="clarification_required",
            issues=ordered,
            retained_context=retained,
            required_user_actions=tuple(issue.issue_id for issue in ordered),
            effects=NO_EFFECTS,
        )

    def _complete_report(
        self,
        request: OrientationRequest,
        report_id: str,
        evidence: tuple[EvidenceReference, ...],
        continuation: ContinuationOption,
    ) -> OrientationReport:
        evidence_refs = tuple(f"{item.evidence_id}@{item.evidence_version}" for item in evidence)
        content = self._content(request, "complete", evidence_refs, (continuation.option_id,))
        return self._report(
            request,
            report_id,
            "complete",
            tuple(ProcessStage(f"understand/{index}", "completed", evidence_refs=evidence_refs if index == 6 else ()) for index in range(1, 12)),
            content,
            evidence_refs,
            (),
            (),
            "valid",
            (),
            (f"{continuation.option_id}@{continuation.option_version}",),
        )

    def _blocked_report(self, request: OrientationRequest, report_id: str) -> OrientationReport:
        stages = []
        for index in range(1, 12):
            if index == 6:
                stages.append(ProcessStage("understand/6", "blocked", issue_refs=("issue-missing-evidence",), reason="required_evidence_unavailable"))
            elif 7 <= index <= 9:
                stages.append(ProcessStage(f"understand/{index}", "skipped", reason="evidence_binding_incomplete"))
            else:
                stages.append(ProcessStage(f"understand/{index}", "completed"))
        issue = ReportIssue("issue-missing-evidence", "missing_evidence", "understand/6", "no contract-valid Evidence Reference traces to this report", ("mode_payload.content.claims_and_support",), (), True, "provide a traceable Evidence Reference")
        uncertainty = ReportUncertainty("uncertainty-evidence-gap", "evidence_gap", ("mode_payload.content.conceptual_structure",), (issue.issue_id,), "open", "provide a traceable Evidence Reference")
        return self._report(
            request,
            report_id,
            "blocked",
            tuple(stages),
            self._content(request, "partial", (), ()),
            (),
            (uncertainty,),
            (issue,),
            "invalid",
            ("Evidence-bound Understanding Frame",),
            (),
        )

    def _report(
        self,
        request: OrientationRequest,
        report_id: str,
        status: str,
        stages: tuple[ProcessStage, ...],
        content: dict[str, object],
        evidence_refs: tuple[str, ...],
        uncertainties: tuple[ReportUncertainty, ...],
        issues: tuple[ReportIssue, ...],
        orientation_validation_status: str,
        absent_outputs: tuple[str, ...],
        continuations: tuple[str, ...],
    ) -> OrientationReport:
        obj = request.orientation_objects[0]
        input_refs = obj.representation_refs or (f"{obj.source_ref}@{obj.source_revision}",)
        working_ref = f"understanding-frame-{request.request_id}@1"
        return OrientationReport(
            schema_version=ORIENTATION_REPORT_SCHEMA,
            identity=ReportIdentity(report_id, "1", request.request_id, request.request_version, request.schema_version, self.operator_id, self.operator_version),
            lifecycle=ReportLifecycle("current"),
            status=status,  # type: ignore[arg-type]
            orientation=ReportOrientation("understand", request.intention, f"{request.request_id}@{request.request_version}.human_authority", request.scope, (f"{obj.object_id}@{obj.object_version}",), constraints=request.constraints, evidence_policy_refs=(request.evidence_policy,) if request.evidence_policy else ()),
            representations=ReportRepresentations(input_refs, (working_ref,), (working_ref,), (AbsentRepresentation("Evidence-bound Understanding Frame", tuple(issue.issue_id for issue in issues)),) if absent_outputs else ()),
            process=stages,
            mode_payload=ModePayload("understand", self.operator_version, content),
            evidence=evidence_refs,
            assumptions=(),
            uncertainties=uncertainties,
            issues=issues,
            confidence=ConfidenceProfile("complete", "complete" if evidence_refs else "partial", orientation_validation_status, "none", tuple(x.uncertainty_id for x in uncertainties), () if evidence_refs else ("evidence-required",)),  # type: ignore[arg-type]
            validation=ReportValidation("valid", OrientationValidation(orientation_validation_status, ("object_bound", "scope_conformant", "evidence_bound"), () if orientation_validation_status == "valid" else ("missing_evidence",), (), ("identity", "scope", "authority"), (), absent_outputs)),  # type: ignore[arg-type]
            continuations=continuations,
            effects=NO_EFFECTS,
        )

    def _content(self, request: OrientationRequest, coverage: str, evidence_refs: tuple[str, ...], continuations: tuple[str, ...]) -> dict[str, object]:
        obj = request.orientation_objects[0]
        return {
            "orientation_summary": f"{obj.object_kind} {obj.object_id}@{obj.object_version} oriented within the confirmed Scope.",
            "key_concepts": request.scope.include,
            "conceptual_structure": f"Orientation Object {obj.object_id}@{obj.object_version} bounded by the submitted Scope.",
            "claims_and_support": evidence_refs,
            "evidence_map": evidence_refs,
            "assumptions": (),
            "dependencies": obj.representation_refs,
            "uncertainties": request.scope.unresolved,
            "contradictions": (),
            "open_questions": (),
            "scope_coverage": coverage,
            "confidence_profile": coverage,
            "suggested_continuations": continuations,
        }

    def _continuation(self, request: OrientationRequest, report_id: str, evidence: tuple[EvidenceReference, ...]) -> ContinuationOption:
        obj = request.orientation_objects[0]
        evidence_refs = tuple(f"{item.evidence_id}@{item.evidence_version}" for item in evidence)
        input_refs = obj.representation_refs or (f"{obj.source_ref}@{obj.source_revision}",)
        return ContinuationOption(
            schema_version=CONTINUATION_OPTION_SCHEMA,
            option_id=f"continuation-inspect-evidence-{request.request_id}",
            option_version="1",
            source_report_id=report_id,
            source_report_version="1",
            action_type="inspect_evidence",
            reason_refs=("evidence[0]",),
            preserved_context=PreservedContext((f"{obj.object_id}@{obj.object_version}",), f"{request.request_id}@{request.request_version}.intention", f"{request.request_id}@{request.request_version}.scope", f"{request.request_id}@{request.request_version}.human_authority", (f"{report_id}@1",), input_refs, evidence_refs, (), tuple(request.human_annotations)),
            request_delta=(),
            availability="available",
            blockers=(),
            required_user_actions=("select_option",),
            effects=NO_EFFECTS,
        )

    def _error(self, request: OrientationRequest, kind: str, stage: str, reason: str, issues: tuple[str, ...], retry: str) -> RuntimeError:
        identity_valid = bool(request.request_id and request.request_version and request.schema_version == ORIENTATION_REQUEST_SCHEMA)
        return RuntimeError(
            schema_version=RUNTIME_ERROR_SCHEMA,
            error_id=f"error-{kind}-{request.request_id or 'unidentified'}-{request.request_version or 'unversioned'}",
            error_version="1",
            kind=kind,  # type: ignore[arg-type]
            request_id=request.request_id if identity_valid else None,
            request_version=request.request_version if identity_valid else None,
            request_schema_version=request.schema_version if identity_valid else None,
            stage=stage,  # type: ignore[arg-type]
            reason_code=reason,
            issues=issues,
            result_presence="none",
            retry=RetryPolicy(retry, retry == "safe", issues),  # type: ignore[arg-type]
            continuation=ContinuationPolicy(False, (), identity_valid, retry == "after_user_action"),
            consumer_behavior={"present_kind": True, "preserve_request": identity_valid, "present_as_completed": False},
            effects=NO_EFFECTS,
        )

    def _publish(self, graph: ContractSet, outcome: tuple[PublicContract, ...], request: OrientationRequest) -> tuple[PublicContract, ...]:
        if validate_contract_set(graph).valid and all(validate_public_contract(item).valid for item in outcome):
            return outcome
        failure = self._error(request, "validation_failed", "report_contract_validation", "public_contract_validation_failed", (), "manual_review")
        return self._validated_error(failure, request)

    def _validated_error(
        self,
        error: RuntimeError,
        request: OrientationRequest,
    ) -> tuple[PublicContract, ...]:
        if validate_public_contract(error).valid:
            return (error,)
        return (self._validated_internal_failure(request),)

    def _validated_internal_failure(self, request: object) -> RuntimeError:
        request_id = getattr(request, "request_id", None)
        request_version = getattr(request, "request_version", None)
        request_schema_version = getattr(request, "schema_version", None)
        identity_valid = bool(
            request_id
            and request_version
            and request_schema_version == ORIENTATION_REQUEST_SCHEMA
        )
        failure = RuntimeError(
            schema_version=RUNTIME_ERROR_SCHEMA,
            error_id=f"error-internal-failure-{request_id or 'unidentified'}-{request_version or 'unversioned'}",
            error_version="1",
            kind="internal_failure",
            request_id=request_id if identity_valid else None,
            request_version=request_version if identity_valid else None,
            request_schema_version=request_schema_version if identity_valid else None,
            stage="processing",
            reason_code="runtime_failed_without_public_result",
            issues=(),
            result_presence="none",
            retry=RetryPolicy("manual_review", False, ()),
            continuation=ContinuationPolicy(False, (), identity_valid, False),
            consumer_behavior={
                "present_kind": True,
                "preserve_request": identity_valid,
                "present_as_completed": False,
            },
            effects=NO_EFFECTS,
        )
        # This static fallback is itself a frozen public contract. Keeping the
        # assertion internal prevents any non-contract object crossing the API.
        assert validate_public_contract(failure).valid
        return failure

    @staticmethod
    def _report_id(request: OrientationRequest) -> str:
        return f"report-{request.request_id}-{request.request_version}"
