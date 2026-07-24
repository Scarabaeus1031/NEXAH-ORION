# Orientation Request

- Status: Frozen Version 1.0 public specification; executable model and validation implemented
- Contract ID: `orion.orientation-request`
- Contract version: `1.0`
- Scope: public request from an authorized consumer to ORION
- Effects: none

## 1. Purpose

An Orientation Request is the only public input that may begin an ORION
orientation. It identifies the Human's intention, the Orientation Objects, the
confirmed scope and the policies under which orientation may proceed.

The contract carries meaning, not transport. It does not define serialization,
delivery, endpoints, sessions or execution.

Behavior is governed by
[`ORION_ORIENTATION_POLICIES.md`](../operators/ORION_ORIENTATION_POLICIES.md).
Mode readiness and processing are governed by
[`ORION_ORIENTATION_OPERATORS.md`](../operators/ORION_ORIENTATION_OPERATORS.md).

### Suite position

This is chapter 1 of the public contract suite and its only entry contract. Read
next: [`CLARIFICATION_RESULT.md`](CLARIFICATION_RESULT.md). The suite-wide
lifecycle is defined in Section 6.4 and its vocabulary in Section 6.5.

The six specifications are one normative language between ORION and every
authorized consumer, including NEXAHEDRON. References between them are part of
the contract, not optional extensions. Conformance is evaluated across the
whole suite; an implementation cannot claim conformance to a convenient subset.

## 2. Scope

This specification defines:

- public request identity;
- required and optional fields;
- Orientation Object references;
- scope and intention boundaries;
- continuation linkage;
- validation outcomes;
- version and compatibility behavior.

It does not define an ORION runtime, gateway, provider, protocol, persistence
model or user interaction.

## 3. Normative language

The terms **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT** and **MAY** are
normative.

Field notation in examples is illustrative. Ordering, punctuation and encoding
are not part of this contract.

## 4. Authority boundaries

- The Human owns `intention`, consequential scope choices and continuation
  selection.
- The consumer captures and submits the request but MUST NOT derive ORION-owned
  findings, routes, confidence or continuations.
- ORION owns request validation, readiness and orientation behavior.
- LYRA MAY translate Human language into approved request fields but MUST NOT
  invent missing values.
- Orientation Object identity, version and source authority remain with their
  authoritative owners.
- A request MUST NOT authorize NEXAH, Library or Atlas mutation.
- Only declared behavioral fields cross this boundary. Providers, prompts,
  orchestration, transport, internal plans and reasoning strategies MUST NOT
  appear in any public contract object.

## 5. Contract shape

### 5.1 Required fields

| Field | Type | Rule |
|---|---|---|
| `schema_version` | contract identifier | MUST equal a supported `orion.orientation-request/<major>.<minor>` version |
| `request_id` | opaque stable identifier | MUST identify one request lineage within the caller's identity domain; reuse is allowed only with a distinct `request_version` |
| `request_version` | immutable object version | MUST identify the exact version of `request_id` submitted for Validation |
| `mode` | Orientation Mode | MUST be exactly `wonder`, `understand`, `compare`, `connect`, `explore`, `build` or `reflect` |
| `requested_by` | Requester Reference | MUST identify the submitting actor without implying Human authority |
| `human_authority` | Human Authority Reference | MUST identify the Human who owns intention and consequential choices |
| `orientation_objects` | ordered Orientation Object Reference list | MUST satisfy the cardinality and kinds required by the selected Orientation Operator |
| `intention` | Intention | MUST state the Human-owned direction and MUST NOT be empty |
| `scope` | Scope | MUST declare inclusions, exclusions and unresolved boundaries |
| `effects` | Effect Declaration | MUST be `none` in version `1.0` |

### 5.2 Requester Reference

A Requester Reference contains:

| Field | Required | Rule |
|---|---:|---|
| `requester_id` | yes | opaque, stable within the requester's identity domain |
| `requester_kind` | yes | `human` or `authorized_consumer` |
| `authority_domain` | yes | names the domain in which `requester_id` is unique |

`requested_by` records who submitted the request. It does not transfer the
Human's authority to that requester.

### 5.3 Human Authority Reference

A Human Authority Reference contains:

| Field | Required | Rule |
|---|---:|---|
| `human_ref` | yes | opaque reference sufficient to preserve decision ownership |
| `authority_scope` | yes | MUST include `intention`, `scope` and `continuation`; MAY include separately approved scopes |

ORION MUST NOT derive personal identity from source material. An anonymous or
session-local Human reference is valid when the authority scope remains clear.

### 5.4 Orientation Object Reference

Each item in `orientation_objects` contains:

| Field | Required | Rule |
|---|---:|---|
| `object_id` | yes | stable object identity; a session-local identity MUST be explicitly marked |
| `object_version` | yes | exact version or explicit `unknown` |
| `object_kind` | yes | approved object kind |
| `source_owner` | yes | authoritative source owner or explicit `unknown` |
| `source_ref` | yes | traceable source reference |
| `source_revision` | yes | exact revision or explicit `unknown` |
| `identity_scope` | yes | `canonical`, `external` or `session_local` |
| `representation_refs` | no | ordered references to existing Representations |
| `integrity_ref` | no | content integrity reference when available |
| `access_status` | no | `available`, `restricted`, `unavailable` or `unknown` |
| `provenance_gaps` | no | explicit ordered gaps; absence means none declared, not none exist |

Two references with different `object_id` values MUST remain different objects
even when their material is identical. Two versions of one object MUST remain
distinct versions.

### 5.5 Intention

`intention` contains:

| Field | Required | Rule |
|---|---:|---|
| `direction` | yes | Human-owned statement of the desired orientation |
| `focus` | no | narrower aspect within the direction |
| `success_boundary` | no | Human description of what would make the orientation useful |

The intention is not an expected answer and MUST NOT be rewritten as one.

### 5.6 Scope

`scope` contains:

| Field | Required | Rule |
|---|---:|---|
| `include` | yes | ordered, possibly empty list of explicit inclusions |
| `exclude` | yes | ordered, possibly empty list of explicit exclusions |
| `unresolved` | yes | ordered, possibly empty list of boundaries still requiring confirmation |
| `depth` | no | declared bounded depth profile |
| `breadth` | no | declared bounded breadth profile |
| `time_boundary` | no | applicable source or subject period |

A ready request MUST have no consequential unresolved scope. Empty inclusion or
exclusion lists are explicit values, not omitted defaults.

### 5.7 Optional fields

| Field | Meaning | Constraint |
|---|---|---|
| `audience` | intended reader or use context | MAY change explanation depth; MUST NOT change evidence or status |
| `constraints` | declared method, policy, domain or format boundaries | MUST remain visible in the report |
| `evidence_policy` | requested minimum evidence and unknown handling | MUST use an approved policy identifier and version |
| `representation_preferences` | approved preferred views | MUST NOT name an implementation |
| `depth_budget` | bounded orientation depth or route count | MUST be explicit; no hidden default may change meaning |
| `prior_report_refs` | earlier immutable Orientation Reports | MUST include report version |
| `human_annotations` | Human-owned notes | MUST remain verbatim and separately labeled |
| `clarification_of` | Clarification Result answered by this request revision | MUST identify exact Clarification Result ID and version |
| `continuation_of` | accepted Continuation Option reference | MUST identify exact option ID and version plus exact source report ID and version |
| `mode_parameters` | fields declared by the selected Orientation Operator | unknown fields follow compatibility rules |
| `consumer_context` | non-authoritative presentation context | MUST NOT alter ORION behavior or authority |

## 6. Validation and readiness

Validation occurs before an Orientation Operator begins. **Contract
Validation** determines whether the public object conforms to this contract.
**Readiness Validation** determines whether a contract-valid request contains
the Human-controlled values required by its Orientation Operator.

### 6.1 Contract validation

The request is `invalid` when:

- `schema_version` is malformed;
- a required field is absent or structurally invalid;
- identifiers are empty or duplicate where uniqueness is required;
- `effects` is not `none`;
- object identity or integrity fields contradict one another;
- the request contains incompatible contract versions;
- a `clarification_of` reference does not resolve to the exact Clarification
  Result answered by this revision;
- a Request Delta identified by `continuation_of` violates its source
  Continuation Option.

An invalid request produces the public behavior defined in
[`RUNTIME_ERROR.md`](RUNTIME_ERROR.md). ORION MUST NOT process it.

### 6.2 Readiness validation

A contract-valid request is `clarification_required` when a Human-controlled
value is missing, ambiguous or consequentially unresolved. It produces
[`CLARIFICATION_RESULT.md`](CLARIFICATION_RESULT.md), not an Orientation Report.

A contract-valid request is `unsupported` when a declared mode, object kind,
version or requested capability is not supported. ORION MUST NOT coerce it to a
nearby supported request.

A contract-valid request is `blocked` before Processing only when a declared
authority, access or policy boundary prevents the Orientation Operator from
beginning. It produces Runtime Error `blocked`, never a Blocked Orientation
Report.

A request is `ready` only when the selected Orientation Operator's required
inputs are satisfied.

### 6.3 Validation order

ORION MUST evaluate in this order:

1. schema and version support;
2. requester and Human authority;
3. request identity and effects;
4. Orientation Object identity, version and cardinality;
5. intention;
6. scope;
7. mode-specific required fields;
8. optional compatibility.

### 6.4 Public lifecycle and outcomes

The suite defines one deterministic public lifecycle:

```text
Orientation Request
  → Contract Validation
    → Invalid | Unsupported
  → Readiness Validation
    → Clarification Required | Unsupported | Blocked | Ready
  → Processing
  → Report Contract Validation
    → Validation Failed
    → Orientation Report: complete | partial | blocked
      → Continuation Options
```

`Ready` and `Processing` are lifecycle states, not terminal public objects.
Unavailable or Internal Failure may interrupt any named stage before a terminal
object exists; the Runtime Error `stage` field identifies that exact boundary.
Every terminal outcome has exactly one public discriminator:

| Observable outcome | Public discriminator | Public object |
|---|---|---|
| Clarification Required | `kind: clarification_required` | Runtime Error with exactly one Clarification Result payload |
| Invalid | `kind: invalid` | Runtime Error |
| Unsupported | `kind: unsupported` | Runtime Error |
| Blocked before Processing | `kind: blocked` | Runtime Error; no Orientation Report |
| Unavailable | `kind: unavailable` | Runtime Error |
| Validation Failed | `kind: validation_failed` | Runtime Error; no Orientation Report |
| Internal Failure | `kind: internal_failure` | Runtime Error |
| Complete Orientation Report | `status: complete` | Orientation Report |
| Partial Orientation Report | `status: partial` | Orientation Report |
| Blocked Orientation Report | `status: blocked` | Orientation Report |

Clarification Required is one observable outcome whose structured payload is a
Clarification Result. A Blocked Orientation Report exists only after Processing
began. Runtime Error `blocked` exists only before Processing began. These states
MUST NOT overlap.

### 6.5 Canonical suite vocabulary

These terms apply unchanged throughout all six contracts:

| Term | Canonical meaning |
|---|---|
| Orientation Request | immutable public input carrying Orientation Objects, Human Intention and Scope |
| Validation | umbrella term; a contract MUST name the specific subtype when behavior differs |
| Contract Validation | validation of an Orientation Request against its public contract |
| Readiness Validation | validation that a contract-valid Orientation Request may enter Processing |
| Report Contract Validation | validation of a candidate Orientation Report against its public contract |
| Orientation Validation | validation of orientation coverage, evidence and invariants inside a contract-valid Orientation Report |
| Evidence Validation | validation of one Evidence Reference |
| Continuation Validation | validation of a selected Continuation Option and its Request Delta before a new Orientation Request is accepted |
| Clarification Required | mutually exclusive public outcome for missing, ambiguous or unconfirmed Human-controlled values |
| Clarification Result | immutable structured payload of Clarification Required |
| Ready | non-terminal lifecycle state permitting Processing |
| Processing | public lifecycle boundary after Ready and before a terminal outcome; not an internal plan or trace |
| Orientation Report | immutable public ORION result with exactly one status: `complete`, `partial` or `blocked` |
| Blocked Orientation Report | contract-valid Orientation Report produced after Processing began but could not complete |
| Continuation Option | immutable, Human-selectable option derived from exactly one source report |
| source report | exact Orientation Report ID and version from which a Continuation Option originates |
| Evidence Reference | immutable traceability record; not evidence content or transferred authority |
| Runtime Error | immutable public non-report outcome; not an exception model |
| Identity | stable public distinction that similarity MUST NOT replace |
| Version | exact immutable object version; distinct from `schema_version` |
| Scope | Human-controlled inclusions, exclusions and boundaries of an orientation |
| Intention | Human-controlled direction of an orientation |

Normative prose MUST qualify `blocked` as either Runtime Error `blocked` or
Blocked Orientation Report whenever the surrounding contract does not already
make the distinction explicit. Synonyms MUST NOT replace these canonical terms
when they denote the same public concept.

## 7. Versioning

`schema_version` uses:

```text
orion.orientation-request/<major>.<minor>
```

- A major version changes meaning, required fields, authority, invariants or
  previously valid behavior.
- A minor version may add optional fields, enum values guarded by capability
  declaration, or stricter validation that corrects ambiguity without changing
  accepted meaning.
- Documentation corrections that do not change contract meaning do not change
  the schema version.

The request schema version is independent of ORION release, Orientation
Operator version and source object versions.

`schema_version` versions this contract language. `request_version` versions an
immutable Orientation Request. They are never interchangeable.

## 8. Canonical invariants

1. One request selects exactly one Orientation Mode.
2. `request_id + request_version` identifies one immutable Orientation Request.
3. One request preserves exactly one Human authority reference.
4. Required Human values are never inferred.
5. Object identity, version and source authority remain explicit.
6. Similarity never replaces identity.
7. Scope changes require declaration and, when consequential, Human confirmation.
8. `effects` remains `none` in version `1.0`.
9. Provider and implementation fields are forbidden at the public boundary.
10. An Orientation Request identified by `continuation_of` preserves every field
    required by its accepted Continuation Option.
11. Invalid, Unsupported, Blocked and Clarification Required outcomes do not
    enter Processing.
12. A request answering Clarification Required identifies the exact
    Clarification Result through `clarification_of`.

## 9. Examples

Examples use transport-neutral field notation.

### 9.1 Ready Understand request

```yaml
schema_version: orion.orientation-request/1.0
request_id: request-understand-001
request_version: "1"
mode: understand
requested_by:
  requester_id: nexahedron-session-01
  requester_kind: authorized_consumer
  authority_domain: nexahedron.local-session
human_authority:
  human_ref: human-session-01
  authority_scope: [intention, scope, continuation]
orientation_objects:
  - object_id: object-observation-01
    object_version: "1"
    object_kind: Observation
    source_owner: human-session-01
    source_ref: session-material-01
    source_revision: "1"
    identity_scope: session_local
intention:
  direction: Understand how this observation reaches the calendar projection.
scope:
  include: [registered representation routes, evidence, blockers]
  exclude: [canonical mutation, unsupported inference]
  unresolved: []
  depth: focused
effects: none
```

### 9.2 Compare request requiring clarification

```yaml
schema_version: orion.orientation-request/1.0
request_id: request-compare-001
request_version: "1"
mode: compare
requested_by:
  requester_id: nexahedron-session-02
  requester_kind: authorized_consumer
  authority_domain: nexahedron.local-session
human_authority:
  human_ref: human-session-02
  authority_scope: [intention, scope, continuation]
orientation_objects:
  - object_id: theory-a
    object_version: "2"
    object_kind: Theory
    source_owner: source-a
    source_ref: source-a/theory
    source_revision: "2"
    identity_scope: external
intention:
  direction: Compare these theories.
scope:
  include: []
  exclude: []
  unresolved: [second comparison subject, comparison lens]
effects: none
```

The request is not ready because Compare requires at least two independently
identified Orientation Objects and a confirmed comparison lens.

## 10. Future compatibility

- Consumers MUST declare the highest request version they produce.
- ORION MUST reject unknown major versions visibly.
- Unknown minor fields MAY be ignored only when the producer declares them
  optional and ignoring them cannot change intention, authority, evidence,
  scope, identity or effects.
- A version adapter MAY be used only when it preserves meaning and all canonical
  invariants; adaptation MUST remain visible in provenance.
- Silent coercion of modes, identifiers, versions, evidence roles, scope or
  effects is forbidden.
- Deprecation and removal follow the canonical ORION Compatibility Policy.

The same contract meaning MUST remain stable across every conforming ORION
runtime.

Compatibility is suite-wide; adaptation MUST preserve every referenced
contract identity, version and invariant.
