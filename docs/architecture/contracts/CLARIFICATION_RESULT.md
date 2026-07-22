# Clarification Result

- Status: Canonical public specification; runtime implementation pending
- Contract ID: `orion.clarification-result`
- Contract version: `1.0`
- Scope: public readiness result for a valid but incomplete Orientation Request
- Effects: none

## 1. Purpose

A Clarification Result tells a consumer exactly why a structurally valid
Orientation Request is not ready and what Human input is required before it may
proceed.

Clarification is a public structured result. It is not dialogue behavior and it
does not authorize ORION to guess, infer or choose missing Human values.

Policy is defined in
[`ORION_ORIENTATION_POLICIES.md`](../operators/ORION_ORIENTATION_POLICIES.md).
Mode-specific readiness is defined in
[`ORION_ORIENTATION_OPERATORS.md`](../operators/ORION_ORIENTATION_OPERATORS.md).

## 2. Scope

This specification defines:

- readiness states;
- clarification issue structure;
- deterministic issue ordering;
- required Human action types;
- retained request context;
- resubmission and compatibility behavior.

It does not define wording, interaction design, transport or execution.

## 3. Normative language

The terms **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT** and **MAY** are
normative. Examples use illustrative field notation only.

## 4. Authority boundaries

- ORION identifies missing, ambiguous or conflicting required fields.
- The Human supplies, chooses, confirms, corrects or withholds the requested
  value.
- LYRA MAY translate issue semantics into faithful Human language but MUST NOT
  resolve an issue.
- A consumer MAY collect the Human response but MUST NOT preselect a
  consequential answer.
- Clarification produces no Orientation Report and no effects.

## 5. Readiness states

Readiness is evaluated after structural request validation.

| State | Meaning | Public outcome |
|---|---|---|
| `ready` | every required mode input is usable | Orientation Operator may begin; no Clarification Result |
| `clarification_required` | one or more Human-controlled values are missing, ambiguous or require confirmation | Clarification Result |
| `unsupported` | a declared mode, kind, version or capability is unsupported | Runtime Error `unsupported` |
| `invalid` | the request violates contract structure or invariants | Runtime Error `invalid` |

A Clarification Result MUST have state `clarification_required` and at least one
blocking issue.

## 6. Common envelope

| Field | Required | Rule |
|---|---:|---|
| `schema_version` | yes | supported `orion.clarification-result/<major>.<minor>` |
| `result_id` | yes | stable identity for this immutable result |
| `request_id` | yes | exact originating request ID |
| `request_schema_version` | yes | exact request version evaluated |
| `mode` | yes | exact requested Orientation Mode |
| `readiness` | yes | MUST be `clarification_required` |
| `issues` | yes | non-empty ordered Clarification Issue list |
| `retained_context` | yes | references to valid request values that remain usable |
| `required_user_actions` | yes | ordered unique action references derived from issues |
| `effects` | yes | MUST be `none` |

## 7. Clarification Issue model

Each issue contains:

| Field | Required | Rule |
|---|---:|---|
| `issue_id` | yes | stable within the result |
| `issue_code` | yes | canonical issue kind |
| `field_path` | yes | contract field requiring Human attention |
| `priority_tier` | yes | canonical ordering tier |
| `reason` | yes | structured reason code; MUST NOT imply a guessed value |
| `expected_value` | yes | accepted kind, cardinality or approved values |
| `current_value_refs` | yes | ordered, possibly empty references to retained values |
| `required_action` | yes | one canonical Human action |
| `blocking` | yes | MUST be `true` in version `1.0` |
| `allowed_values` | no | finite approved values when applicable |
| `conflicts_with` | no | issue or field references that create the ambiguity |

### 7.1 Issue codes

| Code | Meaning |
|---|---|
| `missing_required` | a required Human-controlled value is absent |
| `ambiguous_value` | more than one materially different reading remains possible |
| `identity_unresolved` | object identity or version cannot be selected safely |
| `cardinality_incomplete` | the selected mode requires more objects or anchors |
| `scope_unresolved` | a consequential inclusion, exclusion or boundary is open |
| `choice_required` | several valid possibilities require Human selection |
| `confirmation_required` | an explicit value exists but requires Human confirmation |
| `access_required` | Human action is required to make an identified source available |
| `conflicting_values` | supplied Human-controlled values cannot all apply together |

Unsupported values and malformed contract fields are not clarification issues.
They use the applicable Runtime Error behavior.

## 8. Issue ordering

Issues MUST be ordered by `priority_tier`:

1. `authority` — Human authority or required authorization;
2. `identity` — Orientation Object identity, version and cardinality;
3. `intention` — Human direction and focus;
4. `scope` — inclusions, exclusions, boundaries and mode lens;
5. `required_parameter` — other mode-required Human values;
6. `optional_refinement` — non-blocking refinements, reserved for a future
   compatible version.

`optional_refinement` MUST NOT appear in a version `1.0` Clarification Result,
because every issue in this contract is blocking.

Within one tier, issues are ordered by canonical field order, then `field_path`,
then `issue_id`. The order MUST NOT express importance beyond this policy.

## 9. Required user actions

| Action | Meaning | Resubmission requirement |
|---|---|---|
| `provide` | supply a missing value | new value and source of Human authority |
| `choose` | select among explicit valid alternatives | selected alternative identity |
| `confirm` | affirm or reject an explicit value or boundary | confirmation result |
| `correct` | replace a conflicting or unusable Human value | replacement value |
| `add_object` | supply an additional independently identified Orientation Object | complete object reference |
| `authorize_access` | perform a separate access action outside ORION | resulting access status; no credentials in this contract |
| `remove_conflict` | decide which incompatible Human constraints remain | revised confirmed fields |
| `withhold` | decline to provide the value | request remains unready or is withdrawn by the Human |

The consumer MUST present every blocking action. It MUST NOT complete one
automatically.

## 10. Retained context and resubmission

`retained_context` contains references to request fields that passed validation
and remain unchanged. It MUST NOT copy source content unnecessarily.

A clarified request:

- MUST use a new `request_id` or an explicitly versioned request revision;
- MUST reference the Clarification Result it answers;
- MUST preserve retained values unless the Human explicitly changes them;
- MUST declare every changed field;
- MUST be validated from the beginning;
- MUST NOT be treated as ready merely because all prior issue IDs were answered.

## 11. Versioning

`schema_version` uses:

```text
orion.clarification-result/<major>.<minor>
```

A major change alters issue meaning, priority, required actions or retained
context semantics. A minor change may add optional issue metadata or a new issue
code that existing consumers can safely present as unknown without guessing.

## 12. Canonical invariants

1. Clarification follows structural validation and precedes operator execution.
2. At least one blocking issue is required.
3. Every issue identifies one field and one required Human action.
4. Issues are ordered deterministically.
5. Valid request context is preserved by reference.
6. ORION, LYRA and the consumer never answer clarification for the Human.
7. No Orientation Report, evidence finding or continuation is produced.
8. No effect occurs.
9. Resubmission is fully revalidated.
10. Declining clarification is a valid Human choice.

## 13. Examples

### 13.1 Understand focus requires a Human choice

```yaml
schema_version: orion.clarification-result/1.0
result_id: clarification-understand-001
request_id: request-understand-002
request_schema_version: orion.orientation-request/1.0
mode: understand
readiness: clarification_required
issues:
  - issue_id: issue-focus-01
    issue_code: choice_required
    field_path: intention.focus
    priority_tier: intention
    reason: multiple_supported_focus_kinds
    expected_value: one focus kind
    current_value_refs: []
    required_action: choose
    blocking: true
    allowed_values: [structure, evidence, assumptions, application]
retained_context:
  orientation_objects: [object-paper-01@1]
required_user_actions: [issue-focus-01]
effects: none
```

### 13.2 Compare requires a second object and lens

```yaml
schema_version: orion.clarification-result/1.0
result_id: clarification-compare-001
request_id: request-compare-001
request_schema_version: orion.orientation-request/1.0
mode: compare
readiness: clarification_required
issues:
  - issue_id: issue-object-02
    issue_code: cardinality_incomplete
    field_path: orientation_objects[1]
    priority_tier: identity
    reason: compare_requires_two_objects
    expected_value: one Orientation Object Reference
    current_value_refs: [object-theory-a@2]
    required_action: add_object
    blocking: true
  - issue_id: issue-lens-01
    issue_code: missing_required
    field_path: mode_parameters.comparison_lens
    priority_tier: scope
    reason: comparison_lens_required
    expected_value: one approved comparison lens
    current_value_refs: []
    required_action: provide
    blocking: true
retained_context:
  orientation_objects: [object-theory-a@2]
required_user_actions: [issue-object-02, issue-lens-01]
effects: none
```

The identity issue appears before the scope issue by canonical ordering.

## 14. Future compatibility

- Unknown major versions are rejected visibly.
- New optional issue metadata may be ignored only when issue meaning, ordering
  and required Human action remain intact.
- A consumer that does not recognize an issue code MUST present it as an
  unsupported clarification type; it MUST NOT guess its meaning.
- New action types require a compatibility declaration proving that existing
  consumers can preserve Human authority.
- Adapters MUST preserve issue IDs, order, field paths and action semantics.
- Clarification MUST never degrade into an unstructured generic error.
