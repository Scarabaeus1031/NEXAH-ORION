"""Typed, immutable representations of the frozen ORION public contracts.

The canonical Markdown specifications remain the source of truth.  These
models contain no execution, transport, persistence, or provider behavior.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, Mapping, TypeAlias


ContractScalar: TypeAlias = str | int | float | bool | None
PublicValue: TypeAlias = (
    ContractScalar
    | tuple["PublicValue", ...]
    | Mapping[str, "PublicValue"]
)

ORIENTATION_REQUEST_SCHEMA = "orion.orientation-request/1.0"
CLARIFICATION_RESULT_SCHEMA = "orion.clarification-result/1.0"
ORIENTATION_REPORT_SCHEMA = "orion.orientation-report/1.0"
CONTINUATION_OPTION_SCHEMA = "orion.continuation-option/1.0"
EVIDENCE_REFERENCE_SCHEMA = "orion.evidence-reference/1.0"
RUNTIME_ERROR_SCHEMA = "orion.runtime-error/1.0"
NO_EFFECTS = "none"

OrientationMode: TypeAlias = Literal["wonder", "understand", "compare", "connect", "explore", "build", "reflect"]
EffectDeclaration: TypeAlias = Literal["none"]
RequesterKind: TypeAlias = Literal["human", "authorized_consumer"]
IdentityScope: TypeAlias = Literal["canonical", "external", "session_local"]
AccessStatus: TypeAlias = Literal["available", "restricted", "unavailable", "unknown"]
ReadinessState: TypeAlias = Literal["clarification_required"]
EvidenceClass: TypeAlias = Literal["observed", "derived", "proposed", "unknown"]
EvidenceRelationship: TypeAlias = Literal["supports", "counters", "contextualizes", "limits"]
EditorialStatus: TypeAlias = Literal["draft", "reviewed", "published", "withdrawn", "unclassified", "unknown"]
EvidenceValidationStatus: TypeAlias = Literal["valid", "invalid", "unverified"]
ReportLifecycleState: TypeAlias = Literal["current", "superseded", "withdrawn"]
ReportStatus: TypeAlias = Literal["complete", "partial", "blocked"]
ProcessStageState: TypeAlias = Literal["completed", "skipped", "blocked"]
BinaryValidationStatus: TypeAlias = Literal["valid", "invalid"]
CoverageStatus: TypeAlias = Literal["complete", "partial", "unknown"]
InferenceStatus: TypeAlias = Literal["none", "proposed_present"]
ContinuationAvailability: TypeAlias = Literal["available", "clarification_required", "blocked", "future"]
HumanConfirmation: TypeAlias = Literal["required", "not_required"]
RuntimeErrorKind: TypeAlias = Literal["unsupported", "blocked", "invalid", "unavailable", "clarification_required", "validation_failed", "internal_failure"]
RuntimeStage: TypeAlias = Literal["contract_validation", "readiness_validation", "processing", "report_contract_validation", "continuation_validation", "availability"]
ResultPresence: TypeAlias = Literal["none", "clarification_result"]
RetryDisposition: TypeAlias = Literal["never", "after_user_action", "after_state_change", "safe", "manual_review"]
ClarificationIssueCode: TypeAlias = Literal["missing_required", "ambiguous_value", "identity_unresolved", "cardinality_incomplete", "scope_unresolved", "choice_required", "confirmation_required", "access_required", "conflicting_values"]
ClarificationPriorityTier: TypeAlias = Literal["authority", "identity", "intention", "scope", "required_parameter"]
ClarificationAction: TypeAlias = Literal["provide", "choose", "confirm", "correct", "add_object", "authorize_access", "remove_conflict", "withhold"]
ProvenanceStepKind: TypeAlias = Literal["source", "representation", "transition", "derivation", "proposal"]
AssumptionStatus: TypeAlias = Literal["declared", "contested", "invalidated"]
UncertaintyStatus: TypeAlias = Literal["open", "bounded", "irreducible"]
ContinuationActionType: TypeAlias = Literal["inspect_report", "inspect_evidence", "refine_intention", "narrow_scope", "expand_scope", "add_object", "follow_representation", "switch_mode", "open_atlas", "handoff", "pause"]
RequestDeltaOperationKind: TypeAlias = Literal["preserve", "set", "add", "remove", "require", "confirm"]


@dataclass(frozen=True, slots=True)
class VersionedRef:
    identity: str
    version: str

    @property
    def value(self) -> str:
        return f"{self.identity}@{self.version}"


@dataclass(frozen=True, slots=True)
class RequesterReference:
    requester_id: str
    requester_kind: RequesterKind
    authority_domain: str


@dataclass(frozen=True, slots=True)
class HumanAuthorityReference:
    human_ref: str
    authority_scope: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class IntegrityReference:
    method: str
    value: str
    coverage: str
    verified: bool | str


@dataclass(frozen=True, slots=True)
class OrientationObjectReference:
    object_id: str
    object_version: str
    object_kind: str
    source_owner: str
    source_ref: str
    source_revision: str
    identity_scope: IdentityScope
    representation_refs: tuple[str, ...] = ()
    integrity_ref: IntegrityReference | None = None
    access_status: AccessStatus | None = None
    provenance_gaps: tuple[str, ...] | None = None


@dataclass(frozen=True, slots=True)
class Intention:
    direction: str
    focus: str | None = None
    success_boundary: str | None = None


@dataclass(frozen=True, slots=True)
class Scope:
    include: tuple[str, ...]
    exclude: tuple[str, ...]
    unresolved: tuple[str, ...]
    depth: str | None = None
    breadth: str | None = None
    time_boundary: str | None = None


@dataclass(frozen=True, slots=True)
class ClarificationReference:
    result_id: str
    result_version: str


@dataclass(frozen=True, slots=True)
class ContinuationReference:
    option_id: str
    option_version: str
    source_report_id: str
    source_report_version: str


@dataclass(frozen=True, slots=True)
class OrientationRequest:
    schema_version: str
    request_id: str
    request_version: str
    mode: OrientationMode
    requested_by: RequesterReference
    human_authority: HumanAuthorityReference
    orientation_objects: tuple[OrientationObjectReference, ...]
    intention: Intention
    scope: Scope
    effects: EffectDeclaration
    audience: str | None = None
    constraints: tuple[str, ...] = ()
    evidence_policy: str | None = None
    representation_preferences: tuple[str, ...] = ()
    depth_budget: str | None = None
    prior_report_refs: tuple[str, ...] = ()
    human_annotations: tuple[str, ...] = ()
    clarification_of: ClarificationReference | None = None
    continuation_of: ContinuationReference | None = None
    mode_parameters: Mapping[str, PublicValue] = field(default_factory=dict)
    consumer_context: Mapping[str, PublicValue] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class ClarificationIssue:
    issue_id: str
    issue_code: ClarificationIssueCode
    field_path: str
    priority_tier: ClarificationPriorityTier
    reason: str
    expected_value: str
    current_value_refs: tuple[str, ...]
    required_action: ClarificationAction
    blocking: bool
    allowed_values: tuple[str, ...] | None = None
    conflicts_with: tuple[str, ...] | None = None


@dataclass(frozen=True, slots=True)
class ClarificationResult:
    schema_version: str
    result_id: str
    result_version: str
    request_id: str
    request_version: str
    request_schema_version: str
    mode: OrientationMode
    readiness: ReadinessState
    issues: tuple[ClarificationIssue, ...]
    retained_context: Mapping[str, tuple[str, ...]]
    required_user_actions: tuple[str, ...]
    effects: EffectDeclaration


@dataclass(frozen=True, slots=True)
class SourceReference:
    source_id: str
    source_version: str
    identity_domain: str
    source_owner: str
    source_ref: str
    fragment_ref: str | None = None
    integrity_ref: IntegrityReference | None = None


@dataclass(frozen=True, slots=True)
class AuthorityDeclaration:
    authority_owner: str
    authority_domain: str
    editorial_status: EditorialStatus
    authority_version: str
    declared_at: str | None = None


@dataclass(frozen=True, slots=True)
class ProvenanceStep:
    step_id: str
    step_kind: ProvenanceStepKind
    input_refs: tuple[str, ...]
    output_ref: str
    owner: str
    lossiness: str | tuple[str, ...]
    contract_id: str | None = None
    contract_version: str | None = None


@dataclass(frozen=True, slots=True)
class EvidenceValidation:
    status: EvidenceValidationStatus
    checks: tuple[str, ...]
    issues: tuple[str, ...]
    validated_against: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class TraceabilityTarget:
    report_id: str
    report_version: str
    target_path: str
    finding_id: str | None = None


@dataclass(frozen=True, slots=True)
class EvidenceReference:
    schema_version: str
    evidence_id: str
    evidence_version: str
    source: SourceReference
    authority: AuthorityDeclaration
    evidence_class: EvidenceClass
    relationship: EvidenceRelationship
    provenance: tuple[ProvenanceStep, ...]
    validation: EvidenceValidation
    traceability: tuple[TraceabilityTarget, ...]
    access_status: AccessStatus
    evidence_level: str | None = None
    evidence_scale_id: str | None = None
    evidence_scale_version: str | None = None


@dataclass(frozen=True, slots=True)
class ReportIdentity:
    report_id: str
    report_version: str
    request_id: str
    request_version: str
    request_schema_version: str
    operator_id: str
    operator_version: str
    supersedes: str | None = None


@dataclass(frozen=True, slots=True)
class ReportLifecycle:
    state: ReportLifecycleState
    reason: str | None = None
    replacement_ref: str | None = None


@dataclass(frozen=True, slots=True)
class ReportOrientation:
    mode: OrientationMode
    intention: Intention | str
    human_authority_ref: str
    scope: Scope
    orientation_object_refs: tuple[str, ...]
    prior_report_refs: tuple[str, ...] = ()
    continuation_option_refs: tuple[str, ...] = ()
    constraints: tuple[str, ...] = ()
    evidence_policy_refs: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class AbsentRepresentation:
    representation: str
    reason_refs: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ReportRepresentations:
    input: tuple[str, ...]
    working: tuple[str, ...]
    produced: tuple[str, ...]
    requested_but_absent: tuple[AbsentRepresentation, ...]


@dataclass(frozen=True, slots=True)
class ProcessStage:
    stage_id: str
    state: ProcessStageState
    input_representation_refs: tuple[str, ...] = ()
    output_representation_refs: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()
    issue_refs: tuple[str, ...] = ()
    reason: str | None = None


@dataclass(frozen=True, slots=True)
class ModePayload:
    mode: OrientationMode
    payload_version: str
    content: Mapping[str, PublicValue]


@dataclass(frozen=True, slots=True)
class ReportAssumption:
    assumption_id: str
    statement: str
    declaration_ref: str
    affected_report_paths: tuple[str, ...]
    status: AssumptionStatus


@dataclass(frozen=True, slots=True)
class ReportUncertainty:
    uncertainty_id: str
    kind: str
    affected_report_paths: tuple[str, ...]
    evidence_or_issue_refs: tuple[str, ...]
    status: UncertaintyStatus
    possible_resolution_condition: str | None = None


@dataclass(frozen=True, slots=True)
class ReportIssue:
    issue_id: str
    kind: str
    stage_id: str
    reason: str
    affected_paths: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    blocking: bool
    resolution_condition: str | None = None


@dataclass(frozen=True, slots=True)
class ConfidenceProfile:
    source_coverage: CoverageStatus
    evidence_coverage: CoverageStatus
    orientation_validation_status: BinaryValidationStatus
    inference_status: InferenceStatus
    uncertainty_refs: tuple[str, ...]
    missing_evidence_refs: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class OrientationValidation:
    status: BinaryValidationStatus
    checks: tuple[str, ...]
    errors: tuple[str, ...]
    warnings: tuple[str, ...]
    preserved_invariants: tuple[str, ...]
    violated_invariants: tuple[str, ...]
    absent_outputs: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ReportValidation:
    contract_validation: str
    orientation_validation: OrientationValidation


@dataclass(frozen=True, slots=True)
class OrientationReport:
    schema_version: str
    identity: ReportIdentity
    lifecycle: ReportLifecycle
    status: ReportStatus
    orientation: ReportOrientation
    representations: ReportRepresentations
    process: tuple[ProcessStage, ...]
    mode_payload: ModePayload
    evidence: tuple[str, ...]
    assumptions: tuple[ReportAssumption, ...]
    uncertainties: tuple[ReportUncertainty, ...]
    issues: tuple[ReportIssue, ...]
    confidence: ConfidenceProfile
    validation: ReportValidation
    continuations: tuple[str, ...]
    effects: EffectDeclaration


@dataclass(frozen=True, slots=True)
class PreservedContext:
    orientation_object_refs: tuple[str, ...]
    intention_ref: str
    scope_ref: str
    human_authority_ref: str
    report_refs: tuple[str, ...]
    representation_refs: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    provenance_refs: tuple[str, ...]
    human_annotation_refs: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class RequestDeltaOperation:
    field_path: str
    operation: RequestDeltaOperationKind
    reason_ref: str
    human_confirmation: HumanConfirmation
    value_ref: str | None = None
    required_value_kind: str | None = None


@dataclass(frozen=True, slots=True)
class ContinuationBlocker:
    blocker_id: str
    kind: str
    reason_ref: str
    required_resolution: str
    retry_after_resolution: str


@dataclass(frozen=True, slots=True)
class ContinuationOption:
    schema_version: str
    option_id: str
    option_version: str
    source_report_id: str
    source_report_version: str
    action_type: ContinuationActionType
    reason_refs: tuple[str, ...]
    preserved_context: PreservedContext
    request_delta: tuple[RequestDeltaOperation, ...]
    availability: ContinuationAvailability
    blockers: tuple[ContinuationBlocker, ...]
    required_user_actions: tuple[str, ...]
    effects: EffectDeclaration
    target_mode: OrientationMode | None = None
    target_boundary: str | None = None


@dataclass(frozen=True, slots=True)
class RetryPolicy:
    disposition: RetryDisposition
    same_request_allowed: bool
    required_change_refs: tuple[str, ...]
    retry_window: str | None = None


@dataclass(frozen=True, slots=True)
class ContinuationPolicy:
    allowed: bool
    option_refs: tuple[str, ...]
    preserve_request_context: bool
    human_action_required: bool


@dataclass(frozen=True, slots=True)
class RuntimeError:
    schema_version: str
    error_id: str
    error_version: str
    kind: RuntimeErrorKind
    stage: RuntimeStage
    reason_code: str
    issues: tuple[str, ...]
    result_presence: ResultPresence
    retry: RetryPolicy
    continuation: ContinuationPolicy
    consumer_behavior: Mapping[str, bool]
    effects: EffectDeclaration
    request_id: str | None = None
    request_version: str | None = None
    request_schema_version: str | None = None
    source_report_ref: str | None = None
    result_ref: str | None = None


PublicContract: TypeAlias = (
    OrientationRequest
    | ClarificationResult
    | EvidenceReference
    | OrientationReport
    | ContinuationOption
    | RuntimeError
)


__all__ = [
    "AbsentRepresentation", "AccessStatus", "AssumptionStatus", "AuthorityDeclaration", "BinaryValidationStatus", "CLARIFICATION_RESULT_SCHEMA",
    "CONTINUATION_OPTION_SCHEMA", "ClarificationAction", "ClarificationIssue", "ClarificationIssueCode", "ClarificationPriorityTier", "ClarificationReference",
    "ClarificationResult", "ConfidenceProfile", "ContinuationBlocker",
    "ContinuationActionType", "ContinuationOption", "ContinuationPolicy", "ContinuationReference",
    "ContractScalar", "CoverageStatus", "EVIDENCE_REFERENCE_SCHEMA", "EditorialStatus", "EffectDeclaration", "EvidenceClass", "EvidenceReference", "EvidenceRelationship",
    "EvidenceValidation", "HumanAuthorityReference", "IntegrityReference",
    "EvidenceValidationStatus", "HumanConfirmation", "IdentityScope", "InferenceStatus", "Intention", "ModePayload", "NO_EFFECTS", "ORIENTATION_REPORT_SCHEMA",
    "ORIENTATION_REQUEST_SCHEMA", "OrientationObjectReference", "OrientationReport",
    "OrientationMode", "OrientationRequest", "OrientationValidation", "ProcessStage", "ProcessStageState", "ProvenanceStep", "ProvenanceStepKind",
    "PublicContract", "PublicValue", "PreservedContext", "RUNTIME_ERROR_SCHEMA",
    "ReadinessState", "ReportAssumption", "ReportIdentity", "ReportIssue", "ReportLifecycle", "ReportLifecycleState", "ReportStatus",
    "ReportOrientation", "ReportRepresentations", "ReportUncertainty", "RequestDeltaOperationKind",
    "ReportValidation", "RequesterReference", "RequestDeltaOperation", "RetryPolicy",
    "RequesterKind", "ResultPresence", "RetryDisposition", "RuntimeError", "RuntimeErrorKind", "RuntimeStage", "Scope", "SourceReference", "TraceabilityTarget", "UncertaintyStatus", "VersionedRef", "ContinuationAvailability",
]
