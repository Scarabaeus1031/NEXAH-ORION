# Orientation Report

- Status: Frozen Version 1.0 public specification; executable model and validation implemented
- Contract ID: `orion.orientation-report`
- Contract version: `1.0`
- Scope: public authoritative ORION result for one processed Orientation Request
- Effects: none

## 1. Purpose

An Orientation Report is ORION's immutable public account of one orientation.
It states what was oriented, what process stages completed, which
Representations and evidence were used, what became visible, what remains
uncertain or blocked, and which Continuation Options are valid.

The report is authoritative for ORION's navigation, validation and reporting
result. It is not canonical NEXAH truth, Human meaning or a consequential
decision.

Policy is governed by
[`ORION_ORIENTATION_POLICIES.md`](../operators/ORION_ORIENTATION_POLICIES.md).
Mode payload meaning is governed by
[`ORION_ORIENTATION_OPERATORS.md`](../operators/ORION_ORIENTATION_OPERATORS.md).

### Suite position

This is chapter 4 of the public contract suite. It defines the only successful
or Processing-blocked terminal result. It consumes the Evidence References in
chapter 3 and supplies the source for every Continuation Option in chapter 5.
It inherits the canonical vocabulary in
[`ORIENTATION_REQUEST.md`](ORIENTATION_REQUEST.md#65-canonical-suite-vocabulary).
Read next: [`CONTINUATION_OPTION.md`](CONTINUATION_OPTION.md).

## 2. Scope

This specification defines:

- report identity and lifecycle;
- common public envelope;
- required report sections;
- mode payload binding;
- Evidence Reference and Continuation Option references;
- validation and issue behavior;
- invariants and compatibility.

It does not define generation, storage, delivery, rendering or explanation.

## 3. Normative language

The terms **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT** and **MAY** are
normative. Examples use illustrative field notation only.

## 4. Authority boundaries

- ORION owns report identity, process status, Validation, issues, confidence
  profile and Continuation Options.
- NEXAH and source owners retain authority over referenced objects,
  Representations and invariants.
- Evidence and editorial authority remain with their declared owners.
- LYRA MAY attach a faithful explanation but MUST NOT replace or modify report
  fields.
- A consumer MAY project and present report fields but MUST NOT repair,
  reinterpret or promote them.
- The Human owns meaning, Continuation Option selection and decisions.
- Providers, prompts, orchestration, transport, internal plans and reasoning
  strategies MUST NOT appear in an Orientation Report.

## 5. Report identity

| Field | Required | Rule |
|---|---:|---|
| `schema_version` | yes | supported `orion.orientation-report/<major>.<minor>` |
| `report_id` | yes | stable report identity |
| `report_version` | yes | immutable version of this report identity |
| `request_id` | yes | exact originating Orientation Request |
| `request_version` | yes | exact originating Orientation Request version |
| `request_schema_version` | yes | exact request contract version |
| `operator_id` | yes | exact Orientation Operator |
| `operator_version` | yes | exact operator behavior version |
| `supersedes` | no | prior report identity and version corrected or replaced prospectively |

The tuple `report_id + report_version` identifies one immutable report. A
correction creates a new report version or new report identity with
`supersedes`; it never rewrites history.

## 6. Common envelope

`schema_version` is the root contract discriminator. Every other report field
is contained in one of the following sections.

Every report contains these sections in canonical order:

| Section | Required | Content |
|---|---:|---|
| `identity` | yes | report identity fields in Section 5 other than the root `schema_version` |
| `lifecycle` | yes | public lifecycle state and reason |
| `status` | yes | orientation result status |
| `orientation` | yes | mode, Human intention, scope and Orientation Object refs |
| `representations` | yes | input, working and produced Representation refs |
| `process` | yes | ordered public stage outcomes |
| `mode_payload` | yes | payload required by the selected Orientation Operator |
| `evidence` | yes | ordered Evidence References |
| `assumptions` | yes | ordered, possibly empty explicit assumptions |
| `uncertainties` | yes | ordered, possibly empty unknowns and ambiguities |
| `issues` | yes | ordered, possibly empty report issues |
| `confidence` | yes | structured coverage profile |
| `validation` | yes | contract and orientation validation |
| `continuations` | yes | ordered, possibly empty Continuation Options |
| `effects` | yes | MUST confirm `none` |

## 7. Lifecycle and status

### 7.1 Public lifecycle

| Lifecycle state | Meaning |
|---|---|
| `current` | this is the current issued version known to ORION |
| `superseded` | a newer report explicitly supersedes this version |
| `withdrawn` | ORION has invalidated this report for a declared reason; history remains |

A report is issued only after Report Contract Validation succeeds. Lifecycle is
not processing progress and MUST NOT expose internal execution states.

`superseded` requires a replacement reference. `withdrawn` requires a reason and
MUST NOT cause deletion or silent replacement.

### 7.2 Orientation status

| Status | Meaning |
|---|---|
| `complete` | every required public operator stage completed and required outputs are present |
| `partial` | a valid report exists, but declared coverage or optional routes remain incomplete |
| `blocked` | processing began and stopped at a declared blocker; absent outputs remain explicit |

`complete` does not mean final truth or completed Human understanding. `blocked`
is a valid report status and MUST NOT be converted into a Runtime Error when a
faithful report exists.

Clarification Required, Unsupported and Invalid outcomes do not produce an
Orientation Report.

The three report statuses are mutually exclusive. A Blocked Orientation Report
means Processing began and a contract-valid report exists. It MUST NOT be
accompanied by Runtime Error `blocked`, `validation_failed` or
`internal_failure` for the same attempt.

## 8. Orientation section

`orientation` contains:

- exact `mode`;
- exact Human `intention` received;
- exact confirmed `scope`;
- exact `human_authority_ref` from the originating Orientation Request;
- ordered Orientation Object identities and versions;
- prior Orientation Report or Continuation Option references, when applicable;
- declared constraints and evidence policy references.

The report MUST NOT substitute a rewritten Intention for the Human Intention.

## 9. Representations section

`representations` contains ordered lists:

| Field | Rule |
|---|---|
| `input` | every source Representation used, with identity and version |
| `working` | every non-canonical ORION working Representation used in the report |
| `produced` | produced Representations, or explicit empty list |
| `requested_but_absent` | requested Representations not produced and reason refs |

Every Representation reference MUST preserve source Orientation Object identity,
version, provenance and declared lossiness.

## 10. Process section

`process` is an ordered list of public Orientation Operator stages. Each stage
contains:

- `stage_id` in the form `<mode>/<one-based process-step number>`, interpreted
  against the report's exact Orientation Operator version;
- `state`: `completed`, `skipped` or `blocked`;
- input and output Representation refs, when present;
- Evidence Reference IDs, when present;
- issue refs, when present;
- declared reason when skipped or blocked.

The process section exposes behavioral conformance. It MUST NOT expose internal
components, provider details, prompts, orchestration, internal plans, reasoning
strategies, timing traces or private diagnostics.

## 11. Mode payload

`mode_payload` is a discriminated public section:

| Field | Rule |
|---|---|
| `mode` | MUST equal `orientation.mode` |
| `payload_version` | exact mode-payload version |
| `content` | MUST contain every required structured output section declared by the selected Orientation Operator |

This specification does not repeat mode payload fields. Their normative meaning
is defined only in Sections 11–17 of
[`ORION_ORIENTATION_OPERATORS.md`](../operators/ORION_ORIENTATION_OPERATORS.md).

Unknown payload fields follow compatibility rules. A consumer MUST NOT infer a
missing required section from explanation text.

## 12. Evidence, assumptions and uncertainty

### 12.1 Evidence

Every item in `evidence` is the exact identity and version of a public record
that conforms to [`EVIDENCE_REFERENCE.md`](EVIDENCE_REFERENCE.md).
Every substantive finding MUST have an Evidence Reference or an explicit
unknown-evidence issue.

Supporting, countering, contextualizing and limiting evidence remain distinct.

### 12.2 Assumptions

Each assumption contains:

- stable assumption ID;
- exact statement;
- source or Human declaration reference;
- affected report paths;
- status: `declared`, `contested` or `invalidated`.

Hidden assumptions are forbidden.

### 12.3 Uncertainties

Each uncertainty contains:

- stable uncertainty ID;
- kind;
- affected report paths;
- evidence or issue refs;
- possible resolution condition, if known;
- status: `open`, `bounded` or `irreducible`.

Uncertainty MUST remain visible in summaries and Continuation Options when material.

## 13. Issues

Each report issue contains:

| Field | Required | Rule |
|---|---:|---|
| `issue_id` | yes | stable within report version |
| `kind` | yes | approved issue kind |
| `stage_id` | yes | public stage where issue applies |
| `reason` | yes | structured, non-persuasive reason |
| `affected_paths` | yes | report fields affected |
| `evidence_refs` | yes | ordered, possibly empty Evidence References |
| `blocking` | yes | whether the issue caused `blocked` status |
| `resolution_condition` | no | condition required to resolve |

Issue kinds include missing contract, missing Transition Operator, missing
Renderer, missing evidence, unavailable source, unknown Representation,
incompatible version, violated invariant, validation failure and policy
boundary.

## 14. Confidence

`confidence` contains:

| Field | Allowed values |
|---|---|
| `source_coverage` | `complete`, `partial`, `unknown` |
| `evidence_coverage` | `complete`, `partial`, `unknown` |
| `orientation_validation_status` | `valid`, `invalid` |
| `inference_status` | `none`, `proposed_present` |
| `uncertainty_refs` | ordered, possibly empty list |
| `missing_evidence_refs` | ordered, possibly empty list |

A scalar confidence score is forbidden unless a separately versioned and
validated public method is approved.

## 15. Validation

Validation contains two distinct results.

### 15.1 Report Contract Validation

`contract_validation` MUST be `valid` for an issued Orientation Report. It
confirms:

- required envelope and sections;
- identity and version integrity;
- mode and payload agreement;
- Evidence and Continuation contract conformance;
- invariant and authority-boundary fields;
- absence of implementation-specific public fields.

An invalid public envelope is not an Orientation Report. It produces Runtime
Error `validation_failed`.

### 15.2 Orientation validation

`orientation_validation` contains:

- `status`: `valid` or `invalid`;
- ordered check IDs;
- ordered errors and warnings;
- preserved and violated invariants;
- absent outputs.

A contract-valid report MAY have invalid orientation validation and status
`blocked`. The distinction MUST remain visible.

## 16. Continuations

Every Continuation Option conforms to
[`CONTINUATION_OPTION.md`](CONTINUATION_OPTION.md).

Continuation Options MUST be derived from report fields, ordered by declared policy and
selected only by the Human. A Complete Orientation Report MAY have no
Continuation Option. A Blocked Orientation Report SHOULD offer only options
that remain behaviorally valid.

## 17. Versioning

`schema_version` uses:

```text
orion.orientation-report/<major>.<minor>
```

A major change alters section meaning, lifecycle, status, validation,
confidence, authority or required mode-payload behavior. A minor change may add
optional metadata or compatible sections whose omission cannot alter meaning.

Report schema version, report version, operator version, request version,
Evidence Reference version and Representation versions remain independent and
explicit.

`schema_version` versions this contract language. `report_version` versions an
immutable Orientation Report. They are never interchangeable.

## 18. Canonical invariants

1. A report binds one request and one Orientation Operator version.
2. Reports and report versions are immutable.
3. Corrections preserve history through `supersedes`.
4. Human intention and confirmed scope remain exact.
5. Source and working Representations remain non-interchangeable.
6. Every substantive finding is evidence-bound or explicitly unknown.
7. Assumptions, uncertainty, counterevidence and loss remain visible.
8. Contract validation and orientation validation remain distinct.
9. `blocked` is a valid report status when processing began.
10. Missing outputs are explicit; substitutes are forbidden.
11. Continuations are report-derived and Human-selected.
12. No canonical, Library, Atlas or Human decision effect occurs.
13. A terminal attempt yields either one Orientation Report or one Runtime Error
    outcome, never both.
14. The originating Human authority remains explicit and unchanged.

## 19. Examples

### 19.1 Blocked Understand report

```yaml
schema_version: orion.orientation-report/1.0
identity:
  report_id: report-understand-blocked-01
  report_version: "1"
  request_id: request-understand-001
  request_version: "1"
  request_schema_version: orion.orientation-request/1.0
  operator_id: orion.orientation-operator/understand
  operator_version: 1.0
lifecycle:
  state: current
status: blocked
orientation:
  mode: understand
  intention: Understand how this observation reaches the calendar projection.
  human_authority_ref: request-understand-001@1.human_authority
  scope:
    include: [registered representation routes, evidence, blockers]
    exclude: [canonical mutation, unsupported inference]
    unresolved: []
    depth: focused
  orientation_object_refs: [object-observation-01@1]
representations:
  input: [representation-observation-01@1]
  working: [understanding-frame-01@1]
  produced: [understanding-frame-01@1]
  requested_but_absent:
    - representation: Evidence-bound Understanding Frame
      reason_refs: [issue-missing-evidence-01]
process:
  - stage_id: understand/1
    state: completed
  - stage_id: understand/2
    state: completed
  - stage_id: understand/3
    state: completed
  - stage_id: understand/4
    state: completed
  - stage_id: understand/5
    state: completed
  - stage_id: understand/6
    state: blocked
    reason: required_evidence_unavailable
    issue_refs: [issue-missing-evidence-01]
  - stage_id: understand/7
    state: skipped
    reason: evidence_binding_incomplete
  - stage_id: understand/8
    state: skipped
    reason: evidence_binding_incomplete
  - stage_id: understand/9
    state: skipped
    reason: evidence_binding_incomplete
  - stage_id: understand/10
    state: completed
  - stage_id: understand/11
    state: completed
mode_payload:
  mode: understand
  payload_version: 1.0
  content:
    orientation_summary: The source structure is visible; material evidence remains unavailable.
    key_concepts: [Observation, Calendar Projection]
    conceptual_structure: The observation proposes a route toward a calendar projection.
    claims_and_support: []
    evidence_map: []
    assumptions: []
    dependencies: [source evidence]
    uncertainties: [the proposed route is not evidence-bound]
    contradictions: []
    open_questions: ["Which source evidence supports the proposed route?"]
    scope_coverage: partial
    confidence_profile: partial
    suggested_continuations: [continuation-find-evidence-01]
evidence: []
assumptions: []
uncertainties:
  - uncertainty_id: uncertainty-evidence-gap-01
    kind: evidence_gap
    affected_report_paths: [mode_payload.content.conceptual_structure]
    evidence_or_issue_refs: [issue-missing-evidence-01]
    possible_resolution_condition: provide traceable source evidence
    status: open
issues:
  - issue_id: issue-missing-evidence-01
    kind: missing_evidence
    stage_id: understand/6
    reason: no traceable source evidence supports the proposed route
    affected_paths: [mode_payload.content.conceptual_structure]
    evidence_refs: []
    blocking: true
    resolution_condition: traceable source evidence becomes available
confidence:
  source_coverage: complete
  evidence_coverage: partial
  orientation_validation_status: invalid
  inference_status: none
  uncertainty_refs: [uncertainty-evidence-gap-01]
  missing_evidence_refs: [evidence-required-for-proposed-route]
validation:
  contract_validation: valid
  orientation_validation:
    status: invalid
    checks: [object_bound, scope_conformant, evidence_bound]
    errors: [missing_evidence]
    warnings: []
    preserved_invariants: [identity, provenance]
    violated_invariants: []
    absent_outputs: [Evidence-bound Understanding Frame]
continuations: [continuation-find-evidence-01@1]
effects: none
```

## 20. Future compatibility

- Unknown major versions are rejected visibly.
- A consumer MAY ignore an unknown optional field only when every required
  section, status, identity, evidence, validation and continuation meaning
  remains intact.
- Unknown status, lifecycle or mode-payload versions MUST NOT be coerced.
- Adapters MUST preserve field identity, order where normative, evidence refs,
  issues, validation and absent outputs.
- Explanation text is never a compatibility substitute for missing structured
  fields.
- Older reports remain immutable and inspectable after newer contract versions
  are introduced.
- Every future ORION runtime must produce observably equivalent public report
  behavior for the same contract and operator versions.
- Compatibility is suite-wide; adaptation MUST preserve every referenced
  contract identity, version and invariant.
