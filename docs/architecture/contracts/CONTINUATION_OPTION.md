# Continuation Option

- Status: Frozen Version 1.0 public specification; executable model and validation implemented
- Contract ID: `orion.continuation-option`
- Contract version: `1.0`
- Scope: public, report-derived option for continuing an orientation
- Effects: none

## 1. Purpose

A Continuation Option identifies one meaningful next orientation supported by
an Orientation Report. It preserves valid context and declares what the Human
must confirm, revise or add before another Orientation Request may begin.

A Continuation Option is not an automatic action. It is an immutable proposal
that becomes active only through explicit Human selection. An option that
starts another orientation additionally requires a validated Orientation
Request; inspection, handoff and pause options do not impersonate such a
request.

Continuation behavior is governed by
[`ORION_ORIENTATION_POLICIES.md`](../operators/ORION_ORIENTATION_POLICIES.md)
and the cross-mode rules in
[`ORION_ORIENTATION_OPERATORS.md`](../operators/ORION_ORIENTATION_OPERATORS.md).

### Suite position

This is chapter 5 of the public contract suite. Every Continuation Option is
derived from exactly one Orientation Report in chapter 4. The canonical name
for that origin is **source report**. It inherits the canonical vocabulary in
[`ORIENTATION_REQUEST.md`](ORIENTATION_REQUEST.md#65-canonical-suite-vocabulary).
Read next:
[`RUNTIME_ERROR.md`](RUNTIME_ERROR.md).

## 2. Scope

This specification defines:

- continuation identity and source report binding;
- action types;
- preserved context;
- Request Deltas;
- availability and blockers;
- required Human actions;
- compatibility behavior.

It does not define interaction, navigation, transport, execution or persistence.

## 3. Normative language

The terms **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT** and **MAY** are
normative. Examples use illustrative field notation only.

## 4. Authority boundaries

- ORION derives options only from report fields, issues, evidence and registered
  capabilities.
- The Human chooses whether and how to continue.
- A consumer presents options and submits the accepted request; it MUST NOT
  invent, rank or execute options independently.
- LYRA MAY explain an option faithfully but MUST NOT select it.
- A handoff option does not authorize the receiving boundary to act.
- Providers, prompts, orchestration, transport, internal plans and reasoning
  strategies MUST NOT appear in a Continuation Option.

## 5. Common envelope

| Field | Required | Rule |
|---|---:|---|
| `schema_version` | yes | supported `orion.continuation-option/<major>.<minor>` |
| `option_id` | yes | stable option identity within the source report |
| `option_version` | yes | immutable option version |
| `source_report_id` | yes | exact source Orientation Report |
| `source_report_version` | yes | exact source report version |
| `action_type` | yes | one canonical action type |
| `reason_refs` | yes | non-empty ordered report paths supporting the option |
| `target_mode` | no | required when the option starts another orientation; otherwise absent |
| `target_boundary` | no | required only for `handoff`; MUST NOT imply authority to act |
| `preserved_context` | yes | context that remains valid |
| `request_delta` | yes | changes required to form the next request |
| `availability` | yes | availability state |
| `blockers` | yes | ordered, possibly empty Blocker list |
| `required_user_actions` | yes | ordered, possibly empty Human action list |
| `effects` | yes | MUST be `none` |

## 6. Action types

| Action type | Meaning | Default target mode |
|---|---|---|
| `inspect_report` | inspect another structured report section | unchanged |
| `inspect_evidence` | follow evidence and provenance references | unchanged |
| `refine_intention` | revise Human direction while preserving object identity | unchanged |
| `narrow_scope` | reduce confirmed scope | unchanged |
| `expand_scope` | add an explicit boundary, source or object | unchanged |
| `add_object` | add another independently identified Orientation Object | mode-specific |
| `follow_representation` | orient from an existing approved Representation or route | mode-specific |
| `switch_mode` | begin a different Orientation Operator with explicit Human confirmation | declared target |
| `open_atlas` | open an approved read-only Atlas reference | unchanged or `explore` |
| `handoff` | prepare references for a separately authorized boundary | declared target boundary, not a mode |
| `pause` | retain references without further orientation | unchanged |

Action type meaning is stable. A consumer MUST NOT assign local behavior that
changes its semantics.

## 7. Preserved context

`preserved_context` contains ordered references, never silent copies, to:

| Field | Required | Rule |
|---|---:|---|
| `orientation_object_refs` | yes | exact IDs and versions preserved |
| `intention_ref` | yes | prior intention reference; may require revision by delta |
| `scope_ref` | yes | prior scope reference; may require revision by delta |
| `human_authority_ref` | yes | exact Human authority reference from the source report's request |
| `report_refs` | yes | MUST include the source report |
| `representation_refs` | yes | ordered, possibly empty approved Representations |
| `evidence_refs` | yes | ordered, possibly empty Evidence References |
| `provenance_refs` | yes | ordered, possibly empty provenance records not already carried by Evidence References |
| `human_annotation_refs` | yes | ordered, possibly empty Human-owned annotation refs |

Preservation means the referenced context remains available for Validation. It
does not mean that every value remains applicable after the Request Delta. A
Request Delta MUST declare any change to preserved Scope, Intention,
Orientation Object or Human authority. It MUST NOT remove an Evidence Reference
or provenance reference silently.

## 8. Request delta

A Request Delta is a semantic description of how to form the next
[`ORIENTATION_REQUEST.md`](ORIENTATION_REQUEST.md). It is not a transport patch.
It MUST be empty for `inspect_report`, `inspect_evidence`, `open_atlas`,
`handoff` and `pause` unless that specific option explicitly starts another
orientation. When empty, selection does not create an Orientation Request.

The delta contains ordered operations:

| Operation | Meaning | Human confirmation |
|---|---|---|
| `preserve` | retain an exact prior field and version | not required unless policy changed |
| `set` | replace one field with an explicit proposed value | required for Human-owned fields |
| `add` | add an explicit object, source, boundary or reference | required when scope or meaning changes |
| `remove` | remove an explicit inclusion, object or constraint | required when scope or meaning changes |
| `require` | identify a field the Human must provide before readiness | always required |
| `confirm` | require confirmation of an explicit proposed field | always required |

Each operation contains:

- `field_path`;
- `operation`;
- `value_ref` or `required_value_kind`;
- `reason_ref`;
- `human_confirmation` — `required` or `not_required`.

The resulting request MUST receive a new identity or explicit revision and MUST
be fully validated. A delta MUST NOT bypass readiness.

## 9. Availability states

| State | Meaning | Selection behavior |
|---|---|---|
| `available` | required capability exists and the delta can form a request | Human may select; resulting request still validates |
| `clarification_required` | meaningful option exists but requires Human input | present required actions; do not run |
| `blocked` | a declared blocker prevents the option | preserve option and blockers; retry only after resolution |
| `future` | option is behaviorally valid but no approved capability exists | present only when future capability visibility is permitted; never simulate availability |

Availability is evaluated against declared capabilities and source versions.
Popularity or presentation MUST NOT change it.

## 10. Blockers

Each Blocker contains:

| Field | Required | Rule |
|---|---:|---|
| `blocker_id` | yes | stable within the option |
| `kind` | yes | approved blocker kind |
| `reason_ref` | yes | report issue, validation or capability reference |
| `required_resolution` | yes | condition that must become true |
| `retry_after_resolution` | yes | `allowed` or `not_allowed` |

Approved blocker kinds include missing contract, missing Transition Operator,
missing Renderer, unavailable source, insufficient evidence, unresolved
identity, unsupported version, policy boundary and Human approval required.

## 11. Required Human actions

Actions are limited to:

- `select_option`;
- `confirm_mode`;
- `confirm_scope_change`;
- `provide_required_field`;
- `add_object`;
- `choose_alternative`;
- `authorize_separate_handoff`;
- `pause`;
- `decline`.

Selecting an option does not confirm other consequential fields unless the
option explicitly identifies them and the Human confirms them.

## 12. Versioning

`schema_version` uses:

```text
orion.continuation-option/<major>.<minor>
```

A major change alters action meaning, preservation semantics, request-delta
operations, availability or Human authority. A minor change may add optional
metadata or an action type guarded by explicit capability compatibility.

`schema_version` versions this contract language. `option_version` versions an
immutable Continuation Option. They are never interchangeable.

## 13. Canonical invariants

1. Every Continuation Option is derived from one exact source report version.
2. Every Continuation Option has report-grounded justification in `reason_refs`.
3. Context is preserved by identity and version.
4. Scope and mode changes require explicit Human confirmation.
5. A Request Delta never executes and never bypasses request validation.
6. Availability and blockers remain explicit.
7. `future` never appears as `available`.
8. Consumers do not invent, reorder by hidden preference or auto-select options.
9. Declining or pausing is always valid.
10. Effects remain `none`.
11. An orientation-producing option names `target_mode`; a handoff names
    `target_boundary`; neither field substitutes for the other.
12. Source report identity, Scope, Orientation Object references, Evidence
    References, provenance and Human authority remain traceable through every
    accepted Request Delta.

## 14. Examples

### 14.1 Inspect evidence in the same Understand orientation

```yaml
schema_version: orion.continuation-option/1.0
option_id: continuation-understand-evidence-01
option_version: "1"
source_report_id: report-understand-01
source_report_version: "1"
action_type: inspect_evidence
reason_refs: ["mode_payload.open_questions[0]", "evidence[2]"]
target_mode: understand
preserved_context:
  orientation_object_refs: [object-observation-01@1]
  intention_ref: request-understand-001@1.intention
  scope_ref: request-understand-001@1.scope
  human_authority_ref: request-understand-001@1.human_authority
  report_refs: [report-understand-01@1]
  representation_refs: [representation-observation-01@1]
  evidence_refs: [evidence-route-02@1]
  provenance_refs: []
  human_annotation_refs: []
request_delta:
  - field_path: intention.focus
    operation: set
    value_ref: evidence-route-02
    reason_ref: mode_payload.open_questions[0]
    human_confirmation: required
availability: available
blockers: []
required_user_actions: [select_option]
effects: none
```

### 14.2 Compare continuation requiring another object

```yaml
schema_version: orion.continuation-option/1.0
option_id: continuation-understand-compare-01
option_version: "1"
source_report_id: report-understand-theory-01
source_report_version: "1"
action_type: switch_mode
reason_refs: ["mode_payload.suggested_continuations[1]"]
target_mode: compare
preserved_context:
  orientation_object_refs: [object-theory-a@2]
  intention_ref: request-understand-theory-001@1.intention
  scope_ref: request-understand-theory-001@1.scope
  human_authority_ref: request-understand-theory-001@1.human_authority
  report_refs: [report-understand-theory-01@1]
  representation_refs: []
  evidence_refs: []
  provenance_refs: []
  human_annotation_refs: []
request_delta:
  - field_path: orientation_objects[1]
    operation: require
    required_value_kind: Orientation Object Reference
    reason_ref: mode-requirement.compare.minimum-objects
    human_confirmation: required
  - field_path: mode
    operation: set
    value_ref: compare
    reason_ref: mode_payload.suggested_continuations[1]
    human_confirmation: required
availability: clarification_required
blockers: []
required_user_actions: [confirm_mode, add_object]
effects: none
```

## 15. Future compatibility

- Unknown major versions are rejected visibly.
- Unknown action types MUST NOT be mapped to a familiar action by name
  similarity.
- Optional metadata may be ignored only when action, context preservation,
  availability, blockers and Human confirmation remain unchanged.
- Adapters MUST preserve report binding and delta semantics exactly.
- A new delta operation requires a major version unless existing consumers can
  safely reject it before Human selection.
- Continuation Option selection remains an explicit Human choice across every
  future ORION runtime.
- Compatibility is suite-wide; adaptation MUST preserve every referenced
  contract identity, version and invariant.
