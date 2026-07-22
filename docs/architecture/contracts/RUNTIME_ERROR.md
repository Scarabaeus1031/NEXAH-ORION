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
continuations remain valid.

A Runtime Error is not an exception model. It does not define stack behavior,
status codes, transport, logging or recovery implementation.

Failure behavior is governed by
[`ORION_ORIENTATION_POLICIES.md`](../operators/ORION_ORIENTATION_POLICIES.md).

## 2. Scope

This specification defines:

- public runtime outcome kinds;
- stable error envelope;
- required consumer and UI behavior;
- retry behavior;
- continuation behavior;
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

## 5. Public outcome envelope

| Field | Required | Rule |
|---|---:|---|
| `schema_version` | yes | supported `orion.runtime-error/<major>.<minor>` |
| `error_id` | yes | stable public identity for this immutable outcome |
| `kind` | yes | one canonical runtime outcome kind |
| `request_id` | no | required when a request identity was accepted |
| `request_schema_version` | no | required when `request_id` is present |
| `source_report_ref` | no | used only when the failure concerns a known report or continuation |
| `stage` | yes | public behavioral stage |
| `reason_code` | yes | stable public reason; MUST expose no implementation detail |
| `issues` | yes | ordered, possibly empty public issue references |
| `result_presence` | yes | `none`, `clarification_result` or `orientation_report` |
| `result_ref` | no | required unless `result_presence` is `none` |
| `retry` | yes | Retry Policy |
| `continuation` | yes | Continuation Policy |
| `consumer_behavior` | yes | required presentation and state-preservation behavior |
| `correlation_ref` | no | opaque support reference with no diagnostic content |
| `effects` | yes | MUST be `none` |

### 5.1 Public stages

- `contract_validation`;
- `readiness`;
- `orientation`;
- `report_validation`;
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

Runtime Error MUST NOT invent continuations. Every option reference must exist
in a valid Orientation Report or a separately valid availability result.

## 8. Canonical runtime outcomes

### 8.1 Unsupported

**Meaning:** The request is structurally valid, but a declared mode, object
kind, contract version or capability is not supported by this conforming
runtime.

**Required UI behavior:** State what is unsupported and preserve the submitted
values. Do not silently replace the value with a supported alternative.

**Retry behavior:** `never` for an unchanged runtime and unchanged request;
`after_user_action` if the Human chooses a supported value;
`after_state_change` if a declared capability may later become available.

**Continuation behavior:** None, because no report exists from which a valid
Continuation Option can be derived. The consumer MAY present explicit
request-correction alternatives, but MUST NOT label them Continue Orientation.

**Result presence:** `none`.

### 8.2 Blocked

**Meaning:** A declared capability, authority, source, evidence or policy
condition prevents further orientation.

**Required UI behavior:** If processing produced a valid blocked Orientation
Report, present that report and its blockers. Otherwise present the blocker and
confirm that no report was produced.

**Retry behavior:** `after_state_change` or `after_user_action`, depending on the
declared resolution condition. Unchanged blind retry is forbidden.

**Continuation behavior:** Use only Continuation Options attached to the blocked
report. Without a report, no continuation is allowed.

**Result presence:** `orientation_report` when processing began and a valid
blocked report exists; otherwise `none`.

### 8.3 Invalid

**Meaning:** The public input violates contract structure, identity, version,
integrity, effects or another canonical invariant.

**Required UI behavior:** Identify the public invalid fields or invariant codes.
Do not present any candidate output as an Orientation Report.

**Retry behavior:** `after_user_action` when the Human-owned input must change;
otherwise `manual_review`. The corrected request receives a new identity or
explicit revision.

**Continuation behavior:** None. Correction is not Continue Orientation.

**Result presence:** `none`.

### 8.4 Unavailable

**Meaning:** The public ORION capability required to accept or continue the
request is currently unavailable, without claiming the request itself is
unsupported or invalid.

**Required UI behavior:** State that no orientation result was produced,
preserve the request context and avoid implying progress or completion.

**Retry behavior:** `after_state_change` or `safe` only when the outcome declares
same-request retry safe. Repeated automatic retry is not implied.

**Continuation behavior:** An already valid report-derived option may remain
available. Without a prior report, no continuation is allowed. No fabricated
substitute result.

**Result presence:** `none`.

### 8.5 Clarification Required

**Meaning:** The request is structurally valid but not ready because one or more
Human-controlled values are missing, ambiguous or require confirmation.

**Required UI behavior:** Present the complete ordered
[`CLARIFICATION_RESULT.md`](CLARIFICATION_RESULT.md), preserve valid values and
make each required Human action visible. Do not render it as a generic failure.

**Retry behavior:** `after_user_action`. The clarified request is fully
revalidated.

**Continuation behavior:** None until readiness succeeds. The Human may also
withhold the requested value or withdraw the request.

**Result presence:** `clarification_result`.

### 8.6 Validation Failed

**Meaning:** A produced candidate public result failed contract validation or
could not preserve required identity, evidence, authority or invariants.

**Required UI behavior:** Do not present the candidate as an Orientation Report.
State that validation failed and expose only approved public issue codes.

**Retry behavior:** `after_state_change` when the invalidating condition is
known; otherwise `manual_review`. Same-request retry is allowed only when
declared safe.

**Continuation behavior:** None from the invalid candidate. Existing prior
reports and their valid continuations remain unchanged.

**Result presence:** `none`.

An Orientation Report whose `orientation_validation` is invalid but whose public
contract is valid is not this outcome; it is a valid `blocked` report.

### 8.7 Internal Failure

**Meaning:** ORION could not produce a valid public outcome and cannot safely
classify the cause more specifically at the public boundary.

**Required UI behavior:** State that no valid result was produced, preserve
Human request context when available, expose an opaque correlation reference
when present and reveal no private diagnostics.

**Retry behavior:** `safe`, `after_state_change` or `manual_review` exactly as
declared. A consumer MUST NOT assume retry is safe.

**Continuation behavior:** Existing prior report continuations remain valid.
No continuation may be derived from the failed attempt.

**Result presence:** `none`.

## 9. Outcome distinction rules

1. Missing Human input uses Clarification Required, not Invalid.
2. Unsupported capability uses Unsupported, not Internal Failure.
3. Temporary capability absence uses Unavailable, not Unsupported.
4. A valid report stopped by a known blocker remains an Orientation Report with
   status `blocked`.
5. A candidate that fails public report validation uses Validation Failed and is
   never exposed as a report.
6. Internal Failure is the final safe classification, not a substitute for a
   known public reason.

## 10. Versioning

`schema_version` uses:

```text
orion.runtime-error/<major>.<minor>
```

A major change alters kind meaning, result presence, retry, continuation or
consumer behavior. A minor change may add optional metadata or a new reason code
within an existing kind when older consumers can preserve required behavior.

## 11. Canonical invariants

1. Runtime Error is a public behavioral outcome, not an exception model.
2. Exactly one canonical `kind` applies.
3. Result presence is explicit.
4. Clarification and blocked reports preserve their specialized contracts.
5. Required consumer behavior is stable and non-persuasive.
6. Retry safety is explicit; it is never assumed.
7. Continuations are pre-existing valid options, never error-derived guesses.
8. Human request context is preserved whenever its identity was valid.
9. Internal diagnostics and provider details never cross the boundary.
10. No failure creates effects or weakens authority.

## 12. Examples

### 12.1 ORION capability unavailable

```yaml
schema_version: orion.runtime-error/1.0
error_id: error-unavailable-01
kind: unavailable
request_id: request-understand-003
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
kind: clarification_required
request_id: request-compare-001
request_schema_version: orion.orientation-request/1.0
stage: readiness
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
- Unknown runtime kinds MUST fall back to safe Internal Failure presentation;
  they MUST NOT be guessed from wording.
- Optional fields may be ignored only when kind, result presence, retry,
  continuation and required consumer behavior remain intact.
- Transport or runtime adapters MUST preserve public kinds and MUST NOT map
  several meanings into one generic failure.
- Private diagnostics MAY evolve independently because they are outside this
  contract.
- Every future ORION runtime must preserve the same observable failure,
  retry and continuation behavior.
