# Runtime Error

- Status: Canonical public specification; runtime implementation pending
- Contract ID: `orion.runtime-error`
- Contract version: `1.0`
- Scope: public behavioral failure and non-report outcome contract
- Effects: none

## 1. Purpose

A Runtime Error communicates a public failure or non-report outcome without
exposing implementation details or relying on exception behavior.

It tells a consumer what happened, whether any authoritative result exists,
what the consumer must present, whether retry is meaningful and which
Continuation Options remain valid.

A Runtime Error is not an exception model. It does not define stack behavior,
status codes, transport, logging or recovery implementation.

Failure behavior is governed by
[`ORION_ORIENTATION_POLICIES.md`](../operators/ORION_ORIENTATION_POLICIES.md).

### Suite position

This is chapter 6 of the public contract suite. It defines the mutually
exclusive non-report outcomes in the lifecycle established by
[`ORIENTATION_REQUEST.md`](ORIENTATION_REQUEST.md#64-public-lifecycle-and-outcomes).
It inherits that document's canonical vocabulary. It closes the suite; it does
not introduce an alternative lifecycle.

## 2. Scope

This specification defines:

- public runtime outcome kinds;
- stable error envelope;
- required consumer and UI behavior;
- retry behavior;
- Continuation Option behavior;
- public/internal disclosure boundaries;
- compatibility.

It does not define an exception hierarchy, transport mapping, diagnostics,
monitoring or runtime architecture.

## 3. Normative language

The terms **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT** and **MAY** are
normative. Examples use illustrative field notation only.

## 4. Authority boundaries

- ORION owns classification of public runtime outcomes.
- A consumer presents the outcome and preserves Human-owned request context.
- LYRA MAY faithfully explain public fields but MUST NOT conceal or upgrade the
  outcome.
- Internal diagnostics remain ORION-owned and MUST NOT cross this boundary.
- A failure MUST NOT authorize effects, fallback inference or provider
  substitution that changes observable behavior.
- Providers, prompts, orchestration, transport, internal plans and reasoning
  strategies MUST NOT appear in a Runtime Error.

## 5. Public outcome envelope

| Field | Required | Rule |
|---|---:|---|
| `schema_version` | yes | supported `orion.runtime-error/<major>.<minor>` |
| `error_id` | yes | stable public identity for this immutable outcome |
| `error_version` | yes | immutable version of this `error_id` |
| `kind` | yes | one canonical runtime outcome kind |
| `request_id` | no | required when a request identity was accepted |
| `request_version` | no | required when `request_id` is present |
| `request_schema_version` | no | required when `request_id` is present |
| `source_report_ref` | no | exact Orientation Report ID and version; used only when the outcome concerns that report or its Continuation Option |
| `stage` | yes | public behavioral stage |
| `reason_code` | yes | stable public reason; MUST expose no implementation detail |
| `issues` | yes | ordered, possibly empty public issue references |
| `result_presence` | yes | `none` or `clarification_result` |
| `result_ref` | no | exact Clarification Result ID and version; required exactly when `result_presence` is `clarification_result` |
| `retry` | yes | Retry Policy |
| `continuation` | yes | Continuation Policy |
| `consumer_behavior` | yes | required presentation and state-preservation behavior |
| `effects` | yes | MUST be `none` |

### 5.1 Public stages

- `contract_validation`;
- `readiness_validation`;
- `processing`;
- `report_contract_validation`;
- `continuation_validation`;
- `availability`.

Stages describe the public boundary where behavior stopped. They do not expose
internal components.

## 6. Retry Policy

| Field | Required | Allowed values |
|---|---:|---|
| `disposition` | yes | `never`, `after_user_action`, `after_state_change`, `safe`, `manual_review` |
| `same_request_allowed` | yes | `true` or `false` |
| `required_change_refs` | yes | ordered, possibly empty conditions or issue refs |
| `retry_window` | no | public bounded retry guidance without transport semantics |

`safe` means the same immutable request may be retried without changing Human
meaning or creating duplicate effects. Effects are `none` in this version.

## 7. Continuation Policy

| Field | Required | Rule |
|---|---:|---|
| `allowed` | yes | whether any continuation is valid |
| `option_refs` | yes | ordered, possibly empty Continuation Option refs |
| `preserve_request_context` | yes | MUST be `true` unless the request was invalid before identity was accepted |
| `human_action_required` | yes | `true` or `false` |

Runtime Error MUST NOT invent Continuation Options. Every option reference MUST
already exist in the exact source Orientation Report identified by
`source_report_ref`. An error without a source report has no Continuation
Options.

## 8. Canonical runtime outcomes

Exactly one `kind` applies to one Runtime Error. Runtime Error kinds are
mutually exclusive with all Orientation Report statuses. Clarification Required
is one observable outcome: its Runtime Error classification carries exactly one
Clarification Result as the required structured payload.

### 8.1 Unsupported

**Meaning:** The request passed Contract Validation, but a declared mode, object
kind, contract version or capability is not supported by this conforming
runtime.

**Required consumer behavior:** State what is unsupported and preserve the
submitted values. Do not silently replace the value with a supported
alternative.

**Retry behavior:** `never` for an unchanged runtime and unchanged request;
`after_user_action` if the Human chooses a supported value;
`after_state_change` if a declared capability may later become available.

**Continuation behavior:** None, because no report exists from which a valid
Continuation Option can be derived. The consumer MAY present explicit
request-correction alternatives, but MUST NOT label them Continue Orientation.

**Result presence:** `none`.

### 8.2 Blocked

**Meaning:** The request passed Contract Validation, but a declared authority,
access or policy condition prevents Processing from beginning.

**Required consumer behavior:** Present the blocker and confirm that Processing
did not begin and no Orientation Report was produced.

**Retry behavior:** `after_state_change` or `after_user_action`, depending on the
declared resolution condition. Unchanged blind retry is forbidden.

**Continuation behavior:** No Continuation Option originates from this attempt.
Options from an earlier `source_report_ref`, when present, remain unchanged.

**Result presence:** `none`.

### 8.3 Invalid

**Meaning:** The public input violates contract structure, identity, version,
integrity, effects or another canonical invariant.

**Required consumer behavior:** Identify the public invalid fields or invariant
codes. Do not present any candidate output as an Orientation Report.

**Retry behavior:** `after_user_action` when the Human-owned input must change;
otherwise `manual_review`. The corrected request receives a new identity or
explicit revision.

**Continuation behavior:** None. Correction is not Continue Orientation.

**Result presence:** `none`.

### 8.4 Unavailable

**Meaning:** The public ORION capability required to accept or continue the
request is currently unavailable, without claiming the request itself is
unsupported or invalid.

**Required consumer behavior:** State that no orientation result was produced,
preserve the request context and avoid implying progress or completion.

**Retry behavior:** `after_state_change` or `safe` only when the outcome declares
same-request retry safe. Repeated automatic retry is not implied.

**Continuation behavior:** An already valid report-derived option may remain
available. Without a prior report, no Continuation Option is allowed. No fabricated
substitute result.

**Result presence:** `none`.

### 8.5 Clarification Required

**Meaning:** The request passed Contract Validation but is not Ready because one
or more Human-controlled values are missing, ambiguous or require confirmation.

**Required consumer behavior:** Present the complete ordered
[`CLARIFICATION_RESULT.md`](CLARIFICATION_RESULT.md), preserve valid values and
make each required Human action visible. Do not render it as a generic failure.

**Retry behavior:** `after_user_action`. The clarified request is fully
revalidated.

**Continuation behavior:** None until readiness succeeds. The Human may also
withhold the requested value or withdraw the request.

**Result presence:** `clarification_result`.

### 8.6 Validation Failed

**Meaning:** A candidate Orientation Report failed Report Contract Validation or
could not preserve required Identity, Evidence References, authority or
invariants.

**Required consumer behavior:** Do not present the candidate as an Orientation Report.
State that validation failed and expose only approved public issue codes.

**Retry behavior:** `after_state_change` when the invalidating condition is
known; otherwise `manual_review`. Same-request retry is allowed only when
declared safe.

**Continuation behavior:** None from the invalid candidate. Existing prior
Orientation Reports and their valid Continuation Options remain unchanged.

**Result presence:** `none`.

An Orientation Report whose `orientation_validation` is invalid but whose public
contract is valid is not this outcome; it is a valid `blocked` report.

### 8.7 Internal Failure

**Meaning:** ORION could not produce a valid public outcome and cannot safely
classify the cause more specifically at the public boundary.

**Required consumer behavior:** State that no valid result was produced,
preserve Human Orientation Request context when available, retain the public
Runtime Error identity and reveal no private diagnostics.

**Retry behavior:** `safe`, `after_state_change` or `manual_review` exactly as
declared. A consumer MUST NOT assume retry is safe.

**Continuation behavior:** Existing prior Orientation Report Continuation
Options remain valid. No Continuation Option may be derived from the failed
attempt.

**Result presence:** `none`.

## 9. Outcome distinction rules

1. Missing Human input uses Clarification Required, not Invalid.
2. Unsupported capability uses Unsupported, not Internal Failure.
3. Temporary capability absence uses Unavailable, not Unsupported.
4. A blocker before Processing uses Runtime Error `blocked`; a blocker after
   Processing began uses an Orientation Report with status `blocked`.
5. A candidate that fails Report Contract Validation uses Validation Failed and
   is never exposed as an Orientation Report.
6. Internal Failure is the final safe classification, not a substitute for a
   known public reason.
7. One attempt yields at most one terminal Runtime Error or one Orientation
   Report; these outcomes never accompany one another.

## 10. Versioning

`schema_version` uses:

```text
orion.runtime-error/<major>.<minor>
```

A major change alters kind meaning, result presence, retry, continuation or
consumer behavior. A minor change may add optional metadata or a new reason code
within an existing kind when older consumers can preserve required behavior.

`schema_version` versions this contract language. `error_version` versions an
immutable Runtime Error. They are never interchangeable.

## 11. Canonical invariants

1. Runtime Error is a public behavioral outcome, not an exception model.
2. `error_id + error_version` identifies one immutable Runtime Error.
3. Exactly one canonical `kind` applies.
4. Result presence is explicit.
5. Clarification Required preserves its Clarification Result contract.
6. A Blocked Orientation Report is never represented as Runtime Error `blocked`.
7. Required consumer behavior is stable and non-persuasive.
8. Retry safety is explicit; it is never assumed.
9. Continuation Options are pre-existing valid options, never error-derived guesses.
10. Human Orientation Request context is preserved whenever its identity was valid.
11. Internal diagnostics and provider details never cross the boundary.
12. No failure creates effects or weakens authority.

## 12. Examples

### 12.1 ORION capability unavailable

```yaml
schema_version: orion.runtime-error/1.0
error_id: error-unavailable-01
error_version: "1"
kind: unavailable
request_id: request-understand-003
request_version: "1"
request_schema_version: orion.orientation-request/1.0
stage: availability
reason_code: orientation_runtime_unavailable
issues: []
result_presence: none
retry:
  disposition: after_state_change
  same_request_allowed: true
  required_change_refs: [runtime_available]
continuation:
  allowed: false
  option_refs: []
  preserve_request_context: true
  human_action_required: true
consumer_behavior:
  present_kind: true
  preserve_request: true
  present_as_completed: false
effects: none
```

### 12.2 Clarification Required outcome

```yaml
schema_version: orion.runtime-error/1.0
error_id: outcome-clarification-01
error_version: "1"
kind: clarification_required
request_id: request-compare-001
request_version: "1"
request_schema_version: orion.orientation-request/1.0
stage: readiness_validation
reason_code: required_human_values_missing
issues: [issue-object-02, issue-lens-01]
result_presence: clarification_result
result_ref: clarification-compare-001@1
retry:
  disposition: after_user_action
  same_request_allowed: false
  required_change_refs: [issue-object-02, issue-lens-01]
continuation:
  allowed: false
  option_refs: []
  preserve_request_context: true
  human_action_required: true
consumer_behavior:
  present_clarification_result: true
  preserve_valid_fields: true
  auto_complete_actions: false
effects: none
```

## 13. Future compatibility

- Unknown major versions are rejected visibly.
- An unknown runtime kind MUST NOT be mapped to a known kind. The consumer MUST
  present an unrecognized contract outcome, expose no result, retry or
  continuation claim, and require a supported contract version.
- Optional fields may be ignored only when kind, result presence, retry,
  continuation and required consumer behavior remain intact.
- Transport or runtime adapters MUST preserve public kinds and MUST NOT map
  several meanings into one generic failure.
- Private diagnostics MAY evolve independently because they are outside this
  contract.
- Every future ORION runtime must preserve the same observable failure,
  retry and continuation behavior.
- Compatibility is suite-wide; adaptation MUST preserve every referenced
  contract identity, version and invariant.
