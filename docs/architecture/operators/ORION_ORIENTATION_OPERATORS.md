# ORION Orientation Operators

- Status: Canonical behavioral specification; runtime implementation pending
- Contract family: `orion.orientation-operators/0.1-draft`
- Scope: mode-level Orientation Request to Orientation Report behavior
- Consumers: NEXAHEDRON and future ORION clients
- Provider policy: model-independent and provider-neutral
- Architecture baseline: frozen ORION v1 (`orion-architecture-v1`)
- Runtime effects: none

## 1. Purpose

This document defines how ORION handles the seven Orientation Modes:

- Wonder;
- Understand;
- Compare;
- Connect;
- Explore;
- Build;
- Reflect.

Each mode is a deterministic workflow contract. The contract fixes required and
optional inputs, clarification behavior, processing stages, structured report
sections and valid continuation paths. It does not prescribe prompts, model
messages, provider APIs, user-interface screens or prose.

The public behavioral flow is:

```text
Orientation Request
  → Orientation Operator
  → working Representations
  → Evidence binding and Validation
  → Orientation Report
  → Continue Orientation options
```

NEXAHEDRON submits a versioned Orientation Request and consumes the resulting
Orientation Report or explicit non-report outcome. It never needs to know which
backend, algorithm or internal component ORION used.

## 2. Architecture continuity

This specification extends ORION v1 without redefining its frozen authority or
terminology.

### 2.1 Qualified meaning of Orientation Operator

An **Orientation Operator** is a mode-level ORION orchestration contract. It
orders existing ORION responsibilities into a declared workflow for one human
intention.

An Orientation Operator is not an Operator from the frozen Operator Registry.

| Orientation Operator | Transition Operator / Operator Registry |
|---|---|
| selected by an Orientation Mode | associated with one registered graph transition |
| orchestrates request readiness, representations, evidence, validation and reporting | declares or implements a transformation capability |
| produces a structured Orientation Report | may eventually produce a Target Representation through an executable transition |
| never executes transition mathematics | owns or declares transition execution capability |
| may report a missing Transition Operator | is itself the capability whose absence may block a route |

The qualified term must always be written as **Orientation Operator** in
normative prose. The unqualified term **Operator** retains its frozen ORION v1
meaning.

### 2.2 Authority boundaries

| Authority | Owner | Orientation Operator relationship |
|---|---|---|
| Orientation Space, canonical objects, relations and invariants | NEXAH | reads approved references; never invents or mutates them |
| request lifecycle, navigation, planning, validation and reports | ORION | owns the workflow defined here |
| human-language translation and faithful explanation | LYRA | translates into approved fields and explains returned fields; never runs the workflow |
| evidence identity and editorial status | Library or source owner | supplies versioned references; never receives an implicit write |
| intention, Reflection, approval and decision | Human | supplies purpose and selects continuations |
| interaction, session flow, visualization and report presentation | NEXAHEDRON | submits and presents; never reproduces operator behavior |
| future Reflection boundary | LUCY | outside every runtime path in this specification |

An Orientation Operator may create ORION-owned, immutable working records and a
report. It may not create canonical NEXAH truth, publish Library material,
mutate the Atlas, approve a decision or interpret human Reflection.

## 3. Normative language and determinism

The terms **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT** and **MAY** are
normative.

Determinism applies to contract structure and control behavior:

- the same normalized request, source versions, registries, operator version,
  evidence policy and configuration MUST select the same Orientation Operator;
- required stages MUST execute in the declared order;
- missing fields MUST produce the same clarification codes in the same order;
- registered routes, issues and continuation types MUST be ordered by declared
  rules, never by provider preference;
- every report MUST use the same common envelope and the mode payload declared
  in this document;
- no unknown value may be silently completed;
- no unavailable capability may be represented as successful.

Deterministic structure does not mean that an untrusted reasoning proposal is
authoritative or necessarily byte-identical across providers. If a Reasoning
Backend participates, its result remains a provider-neutral candidate. ORION
MUST bind claims to evidence, validate them and preserve uncertainty before any
candidate can appear in a report. Provider-specific objects never cross the
public boundary.

## 4. Shared Orientation Request contract

This is a behavioral field specification, not an approved serialization schema.
A future wire contract may encode it only after separate approval.

### 4.1 Required envelope

Every ready Orientation Request MUST contain:

| Field | Meaning | Rule |
|---|---|---|
| `request_id` | stable caller-assigned request identity | non-empty and unique within the caller scope |
| `request_schema_version` | request contract version | supported version required |
| `mode` | one of the seven Orientation Modes | exact registered value; no fuzzy mapping inside ORION |
| `requested_by` | human or authorized caller reference | never inferred from material ownership |
| `orientation_objects` | one or more immutable object references | cardinality depends on mode |
| `intention` | human-owned desired direction | mode-specific readiness rules apply |
| `scope` | explicit inclusion boundary | must distinguish included, excluded and unresolved scope |
| `effects` | requested side effects | MUST be `none` for this contract version |

Each Orientation Object reference MUST preserve, when available:

- object identity and version;
- object kind;
- source owner;
- source reference and revision;
- content digest or equivalent integrity reference;
- rights or access status;
- existing Representation references;
- declared provenance gaps.

Raw material without a stable upstream identity MAY receive a session-local
NEXAHEDRON reference. The reference does not transfer canonical or editorial
authority to NEXAHEDRON or ORION.

### 4.2 Shared optional envelope

An Orientation Request MAY contain:

- `focus` — a narrower aspect inside the intention;
- `audience` — intended reader or use context, without changing truth criteria;
- `constraints` — time, format, domain, method or policy limits;
- `evidence_policy` — minimum acceptable evidence and treatment of unknowns;
- `representation_preferences` — requested approved views, not renderer code;
- `time_boundary` — relevant period or source cutoff;
- `depth_budget` — bounded breadth, depth or route count;
- `prior_report_refs` — earlier reports that remain independently versioned;
- `human_annotations` — caller-owned notes retained verbatim and identified as such;
- `continuation_of` — the report and continuation option that produced this request;
- mode-specific optional fields declared below.

Optional fields MUST NOT introduce hidden defaults. If omitting a value changes
the meaning of the workflow, that value is required and clarification is needed.

## 5. Readiness and clarification contract

### 5.1 Readiness outcomes

Before an Orientation Operator begins, ORION validates the request against the
mode profile. Readiness produces exactly one of:

| Outcome | Meaning | Orientation Report produced? |
|---|---|---:|
| `ready` | all required inputs and versions are usable | yes, after processing |
| `clarification_required` | a human-supplied value is missing or ambiguous | no |
| `unsupported` | mode, object kind, version or requested capability is not supported | no |
| `invalid` | contract, identity, integrity or policy validation failed | no |

An incomplete request MUST NOT enter the Orientation Operator. This preserves
the existing rule that ORION does not receive guessed planning inputs.

### 5.2 Structured clarification

Clarification is data, not dialogue logic and not a prompt. A
`ClarificationRequired` result MUST contain an ordered list of issues with:

- stable `issue_code`;
- `field_path`;
- reason;
- required value kind or allowed values;
- whether one value or several values are required;
- existing values that remain valid;
- any boundary that prevents ORION from choosing on the human's behalf.

LYRA or a consuming application MAY render these fields as a human question.
ORION does not generate conversational turns.

Clarification issues MUST be ordered as follows:

1. caller authority and contract validity;
2. Orientation Object identity and cardinality;
3. human intention;
4. scope and comparison or connection boundaries;
5. required versions, evidence or parameters;
6. optional refinements.

An Orientation Operator MUST NOT:

- guess a missing object, target, audience, comparison axis or build purpose;
- merge distinct objects to remove ambiguity;
- choose a consequential scope on behalf of the Human;
- substitute model knowledge for unavailable evidence;
- turn an unsupported request into the nearest supported mode.

## 6. Shared processing lifecycle

Every ready request follows this outer lifecycle. Mode sections define the
operator-specific stages inside steps 4 through 7.

1. **Validate contract** — verify schema, mode, caller, effects and policy.
2. **Bind identities** — resolve immutable Orientation Object and source versions.
3. **Resolve scope** — freeze inclusions, exclusions, budgets and evidence policy.
4. **Select representations** — reuse approved Representations or declare required
   working views without inventing canonical types.
5. **Execute mode stages** — follow the selected Orientation Operator in its
   declared order.
6. **Bind evidence** — attach source, provenance and derivation references to
   every reportable finding.
7. **Test boundaries** — inspect counterevidence, incompatibility, loss, unknowns
   and missing capabilities.
8. **Validate result** — validate schema, identity, evidence coverage, issue
   completeness and authority boundaries independently of any backend.
9. **Compile report** — create the common report envelope and mode payload.
10. **Derive continuations** — emit only actions supported by report fields,
    registered capabilities and retained context.

Failure is a normal result. Once processing has begun, ORION MAY produce a
`partial` or `blocked` Orientation Report if the report can faithfully show what
was completed and why further work stopped.

## 7. Working Representation contract

An Orientation Operator may need structured intermediate views. These are
**working Representations**: immutable, report-bound ORION records used to make
the workflow inspectable.

A working Representation MUST contain:

- its own identity and version;
- the referenced Orientation Object identities and versions;
- the Orientation Operator ID and version;
- source Representation references;
- deterministic configuration and scope;
- provenance references;
- fields preserved, derived, aggregated, hidden, lost or unknown;
- validation status;
- explicit non-canonical status.

A working Representation MUST NOT:

- register a new NEXAH Representation type;
- become a Representation Graph edge by implication;
- replace a source object or source Representation;
- hide lossiness or provenance;
- contain provider-specific request or response objects;
- become canonical because it appears in an Orientation Report.

## 8. Evidence, claims and confidence

### 8.1 Evidence binding

Every substantive finding MUST be one of:

| Finding class | Meaning |
|---|---|
| `observed` | directly present in a cited source or Representation |
| `derived` | produced by a declared deterministic rule from cited inputs |
| `proposed` | untrusted interpretation or hypothesis, explicitly labeled |
| `unknown` | cannot be established from available evidence |

Every `observed`, `derived` or `proposed` finding MUST reference its supporting
evidence records. Counterevidence and contradictory sources MUST remain visible.
Library status, source authority and report confidence are separate fields.

The `E0–E4` scale remains the evidence scale for registered Representation
transitions. An Orientation Operator MAY report that scale when a referenced
Transition Contract supplies it. It MUST NOT reuse `E0–E4` as an invented
general truth score.

### 8.2 Confidence profile

Confidence is structured coverage metadata, not a persuasive percentage. A
report confidence profile MUST contain:

- source coverage: `complete`, `partial` or `unknown`;
- evidence coverage: `complete`, `partial` or `unknown`;
- validation status: `valid` or `invalid`;
- inference status: whether proposed findings are present;
- declared uncertainties and missing evidence;
- mode-specific confidence dimensions where defined.

A scalar confidence score is forbidden unless a separately versioned,
validated method defines its meaning.

## 9. Shared Orientation Report contract

Every produced Orientation Report MUST contain:

| Section | Required content |
|---|---|
| Identity | report ID, schema version, operator ID/version, request ID, timestamps or deterministic run references |
| Status | `complete`, `partial` or `blocked`; never implied by prose |
| Orientation | mode, human intention, scope and Orientation Object references |
| Representations | input, working and produced Representation references; explicit `none` where absent |
| Process | ordered completed, skipped and blocked stages |
| Mode payload | the structured sections required by the selected Orientation Operator |
| Evidence | evidence records, provenance, counterevidence and coverage |
| Assumptions | explicit assumptions; no hidden defaults |
| Uncertainties | unknowns, ambiguities and unresolved questions |
| Validation | checks, errors, warnings and boundary conformance |
| Issues | missing contracts, Operators, Renderers, evidence, access or required parameters |
| Confidence | structured profile defined above |
| Continuations | zero or more structured Continue Orientation options |
| Effects | MUST confirm that no canonical, Library or Atlas mutation occurred |

LYRA may produce a faithful explanation attached to this report. The
explanation never replaces the report.

## 10. Continue Orientation contract

Continuation is explicit human choice. ORION MUST NOT automatically run a
continuation or silently change modes.

Each `ContinuationOption` MUST contain:

- stable option ID;
- action type;
- source report ID;
- reason references to report fields, issues or open questions;
- target mode, if the mode changes;
- preserved Orientation Object and Representation references;
- required new or revised inputs;
- scope delta;
- availability: `available`, `clarification_required`, `blocked` or `future`;
- blockers and required capabilities;
- declared effects, which remain `none` in this version.

Allowed action types are:

| Action type | Meaning |
|---|---|
| `inspect_report` | remain in the report and inspect another structured view |
| `inspect_evidence` | follow evidence and provenance references |
| `refine_intention` | revise the human direction while preserving object identity |
| `narrow_scope` | reduce the inclusion boundary |
| `expand_scope` | add an explicit boundary, source or object |
| `add_object` | add another independently identified Orientation Object |
| `follow_representation` | orient from an existing Representation or registered route |
| `switch_mode` | create a proposed request for another Orientation Operator |
| `open_atlas` | open an approved read-only Atlas location |
| `handoff` | prepare a bounded package for a separately authorized system or Human |
| `pause` | retain the report reference without further processing |

A continuation option is not an instruction to NEXAHEDRON to implement ORION
logic. NEXAHEDRON presents available options and submits the selected option as
a new or amended Orientation Request.

---

## 11. Wonder Orientation Operator

- Operator ID: `orion.orientation-operator/wonder`
- Purpose: orient an attention signal before requiring a well-formed question
- Working Representation: `Wonder Field` (non-canonical report-bound view)

### 11.1 Required input

- exactly one starting Orientation Object representing an observation, note,
  image, passage, idea, question or other supported attention signal;
- the Human's statement of what caught their attention, which may be incomplete;
- a scope boundary sufficient to identify where the signal was noticed;
- source identity or an explicit session-local source reference.

A formal question is not required.

### 11.2 Optional input

- time or place of observation;
- adjacent notes or materials;
- prior occurrences;
- known interpretations supplied by the Human;
- excluded interpretations or domains;
- desired breadth and evidence threshold;
- prior Wonder or Understand report references.

### 11.3 Clarification strategy

Clarification is required when no attention signal can be identified, the
material boundary is ambiguous, or the supplied object cannot be referenced.
ORION asks for the noticed material before asking for a question.

ORION MUST NOT require the Human to explain why the signal matters. It MUST NOT
name the signal as a pattern, cause or concept before the evidence supports that
classification.

### 11.4 Orientation process

1. Bind the attention signal and its source context.
2. Record directly observable features without interpretation.
3. Separate Human-supplied interpretations from source observations.
4. Identify repetition, contrast, anomaly, tension or absence as candidate
   noticing structures.
5. Search approved context for related observations and counterexamples.
6. Form candidate questions and possible frames as `proposed`, never as facts.
7. Identify what cannot yet be named or tested.
8. Build a bounded Wonder Field linking observations, proposals and unknowns.
9. Validate that every named pattern is labeled by evidence class.

### 11.5 Structured output

The mode payload MUST contain:

- `attention_signal`;
- `observed_features`;
- `repetitions_and_contrasts`;
- `candidate_patterns`;
- `candidate_questions`;
- `possible_frames`;
- `related_observations`;
- `counterexamples`;
- `unknowns`;
- `evidence_map`;
- `confidence_profile`;
- `suggested_continuations`.

The report MUST distinguish what was noticed from what was proposed about it.

### 11.6 Continue Orientation

Natural continuations include:

- choose one candidate question and switch to Understand;
- add another observation;
- Compare two possible frames;
- Connect the signal with a related observation;
- Explore one concept or Atlas neighborhood;
- inspect counterexamples or missing evidence;
- pause without resolving the Wonder Field.

---

## 12. Understand Orientation Operator

- Operator ID: `orion.orientation-operator/understand`
- Purpose: make the structure, support and limits of one subject understandable
- Working Representation: `Understanding Frame` (non-canonical report-bound view)

### 12.1 Required input

- exactly one primary Orientation Object;
- a human-owned understanding intention or focus;
- scope, including the part or whole to be considered;
- source version and available provenance;
- requested depth sufficient to bound the workflow.

### 12.2 Optional input

- audience or prior familiarity;
- specific concepts, passages or claims to emphasize;
- known questions or misunderstandings;
- excluded topics;
- time boundary;
- evidence threshold;
- preferred approved Representations;
- prior reports or related Orientation Objects.

Audience may change explanation depth. It MUST NOT change evidence or validation.

### 12.3 Clarification strategy

Clarification is required when the primary object, intended understanding,
scope, source version or required access is missing. If the request uses
"understand" without saying whether the Human wants structure, evidence,
history, application or another focus, ORION may return a finite list of
supported focus kinds. It does not choose one silently.

### 12.4 Orientation process

1. Identify and version-bind the Orientation Object.
2. Inventory available Representations and source structure.
3. Resolve the requested focus and scope.
4. Identify major concepts, terms, claims and components.
5. Determine conceptual, argumentative, procedural or system structure.
6. Bind supporting evidence and provenance to each material claim.
7. Identify assumptions, dependencies and omitted premises.
8. Separate agreement, interpretation, uncertainty and contradiction.
9. Identify limitations, unresolved questions and missing evidence.
10. Determine registered routes for deeper exploration.
11. Validate coverage, evidence binding and scope conformance.

### 12.5 Structured output

The mode payload MUST contain:

- `orientation_summary`;
- `key_concepts`;
- `conceptual_structure`;
- `claims_and_support`;
- `evidence_map`;
- `assumptions`;
- `dependencies`;
- `uncertainties`;
- `contradictions`;
- `open_questions`;
- `scope_coverage`;
- `confidence_profile`;
- `suggested_continuations`.

Summary text MUST remain traceable to the structured sections and evidence.

### 12.6 Continue Orientation

Natural continuations include:

- follow one concept;
- inspect the evidence for one claim;
- narrow or expand the scope;
- Compare the object with another theory, document or perspective;
- Connect one concept with another domain;
- Explore a registered Representation or Atlas neighborhood;
- Build from the resulting requirements or structure;
- revisit an assumption or open question;
- pause and Reflect on what changed for the Human.

---

## 13. Compare Orientation Operator

- Operator ID: `orion.orientation-operator/compare`
- Purpose: expose similarities, differences and non-comparability without
  collapsing distinct objects
- Working Representation: `Comparison Frame` (non-canonical report-bound view)

### 13.1 Required input

- at least two independently identified Orientation Objects;
- the comparison intention;
- at least one comparison lens or an explicit request for available lenses;
- scope and source versions for every object;
- an ordering or stable identity for each comparison side.

### 13.2 Optional input

- Human-supplied comparison axes;
- baseline or reference object;
- weighting rules, only when explicitly declared;
- audience and use context;
- equivalence profile;
- exclusions;
- evidence threshold and time boundary;
- prior Understand reports for either object.

### 13.3 Clarification strategy

Clarification is required when fewer than two objects exist, a side lacks a
version or boundary, the comparison lens is consequentially ambiguous, or the
objects have no approved comparable Representation.

ORION MUST NOT force equivalence. If an axis applies to one side but not the
other, the field is `not_comparable`, not empty and not a negative score.

### 13.4 Orientation process

1. Bind every object independently and preserve side identity.
2. Establish comparable source and Representation versions.
3. Resolve the comparison lens and axes.
4. Produce a separate structured profile for each side.
5. Align only fields permitted by the declared equivalence profile.
6. Compare field by field across structure, claims, evidence and limitations.
7. Identify similarities, differences, tensions and non-comparable fields.
8. Test evidence symmetry so one side is not supported by a lower standard
   without disclosure.
9. Record assumptions, missing fields and version asymmetries.
10. Validate that no side was rewritten to fit the other.

### 13.5 Structured output

The mode payload MUST contain:

- `comparison_subjects`;
- `comparison_lens`;
- `comparison_axes`;
- `subject_profiles`;
- `comparison_matrix`;
- `similarities`;
- `differences`;
- `tensions`;
- `not_comparable`;
- `evidence_by_subject`;
- `evidence_asymmetries`;
- `assumptions_and_limits`;
- `confidence_by_axis`;
- `suggested_continuations`.

No aggregate winner or ranking may be emitted unless the Human supplied an
approved decision rule and the report exposes that rule.

### 13.6 Continue Orientation

Natural continuations include:

- Understand one decisive difference;
- change or add a comparison axis;
- inspect evidence on either side;
- add a third Orientation Object;
- Connect a shared concept or bridge;
- Explore a non-comparable region;
- Build explicit evaluation criteria;
- narrow the comparison to one claim or Representation.

---

## 14. Connect Orientation Operator

- Operator ID: `orion.orientation-operator/connect`
- Purpose: inspect possible relationships and bridges while preserving the
  independence of every anchor
- Working Representation: `Connection Map` (non-canonical report-bound view)

### 14.1 Required input

- at least two independently identified Orientation Objects or anchor
  Representations;
- a connection intention;
- scope for acceptable relation domains;
- source versions and provenance for every anchor.

### 14.2 Optional input

- candidate relation type;
- known intermediary concepts or objects;
- maximum bridge length or graph depth;
- excluded relation types;
- temporal, causal, structural, analogical or provenance constraints;
- evidence threshold;
- prior Compare, Understand or Explore reports.

### 14.3 Clarification strategy

Clarification is required when fewer than two anchors are present, anchor
identity is unclear, or the allowed relation domain is too broad to bound.
ORION may return registered relation families as allowed values. It MUST NOT
invent an edge because two labels resemble one another.

### 14.4 Orientation process

1. Bind anchors independently.
2. Inventory approved Representations and registered relations for each anchor.
3. Resolve allowable relation types and traversal depth.
4. Identify shared concepts, structures, provenance or intermediaries.
5. Construct candidate bridge paths from registered relations and explicit
   proposed relations.
6. Classify every path edge as observed, derived, proposed or unknown.
7. Search for counterevidence, broken edges and category mistakes.
8. Preserve the differences and lossiness at every bridge.
9. Rank paths by declared evidence and route rules, not rhetorical plausibility.
10. Validate that proposed connections did not become canonical graph edges.

### 14.5 Structured output

The mode payload MUST contain:

- `anchors`;
- `relation_scope`;
- `shared_elements`;
- `candidate_connections`;
- `bridge_paths`;
- `intermediary_nodes`;
- `relation_types`;
- `evidence_by_edge`;
- `counterevidence`;
- `broken_or_unknown_edges`;
- `preserved_differences`;
- `confidence_by_connection`;
- `suggested_continuations`.

A candidate connection MUST remain non-canonical unless accepted through a
separate NEXAH authority path.

### 14.6 Continue Orientation

Natural continuations include:

- inspect one bridge edge;
- Understand an intermediary concept;
- Compare the anchors directly;
- add or remove an anchor;
- change the allowed relation type or depth;
- Explore the neighborhood around one anchor;
- inspect counterevidence;
- hand off a candidate relation for separate human and NEXAH review.

---

## 15. Explore Orientation Operator

- Operator ID: `orion.orientation-operator/explore`
- Purpose: reveal a bounded field of possible directions from a known starting
  point without pretending that exploration has one required destination
- Working Representation: `Exploration Map` (non-canonical report-bound view)

### 15.1 Required input

- at least one starting Orientation Object, Representation or approved Atlas
  reference;
- an exploration intention;
- a bounded depth, breadth, time or evidence budget;
- source version and provenance for the starting point.

### 15.2 Optional input

- preferred directions or relation families;
- concepts, sources or domains to exclude;
- minimum evidence threshold;
- visited or known locations;
- novelty preference;
- time boundary;
- prior exploration trail or report.

### 15.3 Clarification strategy

Clarification is required when no starting point exists or no traversal budget
can bound the request. A destination is optional. ORION MUST NOT turn the lack
of a destination into a guessed target.

If the starting point is an Atlas reference, ORION verifies access and version.
It never mutates Atlas state.

### 15.4 Orientation process

1. Bind the starting point and existing trail.
2. Resolve the exploration budget and exclusions.
3. Map the approved local neighborhood and available Representations.
4. Identify landmarks, clusters, branches and boundary nodes.
5. Attach evidence and provenance to every navigable relation.
6. Distinguish visited, unvisited, unavailable and unknown regions.
7. Identify coverage gaps and alternative routes.
8. Order branches by the declared exploration policy.
9. Record stop conditions and the path already traversed.
10. Validate that no unregistered path is presented as navigable.

### 15.5 Structured output

The mode payload MUST contain:

- `starting_point`;
- `exploration_budget`;
- `orientation_map`;
- `landmarks`;
- `branches`;
- `visited_trail`;
- `unvisited_frontier`;
- `unavailable_or_unknown_regions`;
- `evidence_by_route`;
- `coverage_gaps`;
- `stop_conditions`;
- `confidence_profile`;
- `suggested_continuations`.

### 15.6 Continue Orientation

Natural continuations include:

- follow one branch;
- return to a prior landmark;
- expand or narrow the traversal budget;
- Understand one node;
- Compare two branches;
- Connect two landmarks;
- inspect route evidence;
- open an approved Atlas view in read-only mode;
- pause and preserve the current trail reference.

---

## 16. Build Orientation Operator

- Operator ID: `orion.orientation-operator/build`
- Purpose: orient purpose, requirements, constraints, evidence and decisions
  before authorized construction begins
- Working Representation: `Build Orientation` (non-canonical report-bound view)

### 16.1 Required input

- the intended work or artifact;
- the purpose or outcome it must enable;
- one or more source Orientation Objects, requirements or observations;
- explicit scope and constraints;
- the Human or external authority responsible for consequential decisions;
- acceptance conditions sufficient to distinguish success from completion theater.

### 16.2 Optional input

- audience and stakeholders;
- resources, timeline and dependencies;
- standards and policies;
- existing architecture or implementation references;
- alternatives already considered;
- risk tolerance;
- prior Understand, Compare or Connect reports;
- authorized handoff target.

### 16.3 Clarification strategy

Clarification is required when the intended work, purpose, decision owner,
scope or acceptance conditions are missing. Conflicting constraints are
reported as conflicts; ORION does not silently prioritize them.

The Build Orientation Operator does not implement, publish, deploy or mutate
the intended artifact.

### 16.4 Orientation process

1. Bind the intended work, sources and decision authority.
2. Separate purpose, desired outcomes and proposed form.
3. Inventory requirements, evidence, constraints and assumptions.
4. Decompose the work into capabilities, boundaries and dependencies.
5. Identify interfaces, decisions and authority owners.
6. Construct bounded alternatives where the evidence supports them.
7. Compare tradeoffs without selecting a consequential option for the Human.
8. Identify risks, unknowns and missing evidence.
9. Derive milestones and verification conditions from accepted requirements.
10. Validate traceability from every proposed element to purpose, constraint or
    evidence.

### 16.5 Structured output

The mode payload MUST contain:

- `build_intent`;
- `purpose_and_outcomes`;
- `requirements`;
- `constraints`;
- `assumptions`;
- `capability_and_boundary_map`;
- `dependencies_and_interfaces`;
- `alternatives_and_tradeoffs`;
- `decisions_required`;
- `authority_owners`;
- `risks_and_unknowns`;
- `milestones`;
- `verification_conditions`;
- `evidence_traceability`;
- `suggested_continuations`.

The output is an orientation for building, not the built artifact and not an
authorization to act.

### 16.6 Continue Orientation

Natural continuations include:

- Understand one requirement or constraint;
- Compare architecture or implementation alternatives;
- Connect a requirement to supporting evidence;
- refine scope or acceptance conditions;
- inspect a risk or unresolved decision;
- orient the next milestone;
- hand off an immutable build package to a separately authorized Builder or Human;
- Reflect after a milestone without rewriting the original plan.

---

## 17. Reflect Orientation Operator

- Operator ID: `orion.orientation-operator/reflect`
- Purpose: make explicit changes, continuities and open questions visible while
  preserving Human authority over meaning
- Working Representation: `Reflection Frame` (non-canonical report-bound view)

### 17.1 Required input

- one prior Orientation Report, Orientation Object or bounded experience
  reference;
- a Human-owned reflection intention;
- an explicit reference point for "before", "then" or the earlier state;
- current Human-supplied observations or a current version for comparison;
- scope for what may be compared.

When the Human chooses only to pause with an existing report, ORION processing
is not required. NEXAHEDRON may present a Human Reflection space without
submitting a request.

### 17.2 Optional input

- a second report or current object version;
- Human annotations retained verbatim;
- questions the Human wants to keep open;
- decisions or outcomes to revisit;
- time boundary;
- evidence or provenance to re-inspect;
- excluded personal material;
- desired continuation boundary.

### 17.3 Clarification strategy

Clarification is required when the reflection subject, reference point or Human
intention is absent. ORION MUST NOT infer a psychological state, emotion,
personal meaning or decision. It MUST NOT require the Human to disclose any of
them.

If no structured before/current comparison exists, the report may preserve
Human annotations and open questions but MUST mark system-observed change as
`unknown`.

### 17.4 Orientation process

1. Bind the prior subject, report or object version.
2. Bind the current comparison point, if one exists.
3. Preserve Human annotations verbatim and separately from ORION findings.
4. Compare only explicit structured fields and source versions.
5. Identify changed, unchanged, added, removed and unresolved fields.
6. Re-inspect evidence, provenance, assumptions and blockers when requested.
7. Surface open questions without resolving them automatically.
8. Distinguish system-observed deltas from Human-described meaning.
9. Identify possible next orientations without choosing one.
10. Validate that no Human meaning, approval or decision was inferred.

### 17.5 Structured output

The mode payload MUST contain:

- `reflection_subject`;
- `prior_reference`;
- `current_reference` or explicit `none`;
- `human_annotations_verbatim`;
- `system_observed_changes`;
- `unchanged_elements`;
- `added_and_removed_elements`;
- `open_questions`;
- `evidence_revisited`;
- `unresolved_assumptions_and_blockers`;
- `human_meaning` set to `not_inferred`;
- `confidence_profile` limited to comparison completeness;
- `suggested_continuations`.

This report is not LUCY. LUCY remains a future boundary, and the Human remains
the sole authority over Reflection and decision.

### 17.6 Continue Orientation

Natural continuations include:

- return to the prior report;
- Understand one explicit change;
- Compare two report or object versions;
- inspect evidence or provenance again;
- continue one open question;
- revise the Human's intention;
- begin a new orientation with an explicitly selected mode;
- pause and leave the question open.

---

## 18. Cross-mode continuation rules

Mode changes MUST be explicit and traceable:

| From | Natural target modes | Preserved context |
|---|---|---|
| Wonder | Understand, Compare, Connect, Explore, Reflect | attention signal, observations, candidate question |
| Understand | Compare, Connect, Explore, Build, Reflect | primary object, concepts, evidence, open questions |
| Compare | Understand, Connect, Explore, Build, Reflect | all subject identities, lens, differences, evidence |
| Connect | Understand, Compare, Explore, Build, Reflect | anchors, candidate bridges, evidence by edge |
| Explore | Understand, Compare, Connect, Build, Reflect | starting point, trail, selected landmark or branch |
| Build | Understand, Compare, Connect, Reflect | purpose, requirements, constraints, decisions, evidence |
| Reflect | any explicitly selected mode | prior report, explicit changes, open questions, Human annotations |

A cross-mode continuation creates a proposed request delta. The Human confirms
the new intention and scope before the target Orientation Operator runs.

## 19. Failure and blocked-report behavior

An Orientation Operator MUST stop or block when it encounters:

- missing or incompatible source versions;
- inaccessible evidence;
- an unknown Representation;
- no registered route;
- a missing Transition Contract;
- a missing executable Transition Operator;
- a missing Renderer when a requested Representation requires one;
- unresolved required parameters;
- invalid identity or provenance;
- violated invariants;
- unsupported effects or requested mutations;
- a policy or Human approval boundary.

A blocked report MUST include completed stages, the exact stop stage, issues,
available partial Representations, evidence gathered before the block, absent
outputs and continuations that remain valid. It MUST NOT fabricate a substitute
Representation or generic answer.

## 20. NEXAHEDRON consumer boundary

NEXAHEDRON may:

- collect Human-owned request fields;
- submit a versioned Orientation Request through the approved ORION gateway;
- render `ClarificationRequired`, `Unsupported` and `Invalid` outcomes;
- present an Orientation Report and faithful LYRA explanation;
- visualize working Representation and evidence references;
- present available continuation options;
- submit the Human's selected continuation as a new or amended request;
- preserve local interaction state according to an approved session contract.

NEXAHEDRON must not:

- select or execute an Orientation Operator internally;
- reproduce the processing stages as application logic;
- repair, enrich or reinterpret report fields;
- derive its own confidence, evidence rank or continuation;
- convert blocked status into a successful experience claim;
- mutate Library, Atlas or NEXAH state through this contract;
- expose provider-specific behavior as product semantics.

## 21. Conformance requirements

Any ORION implementation—rule-based, algorithmic, OpenAI-backed,
Claude-backed, Llama-backed, local-model-backed or hybrid—conforms only if it:

1. accepts the same approved structured request fields;
2. applies the same readiness and clarification rules;
3. selects exactly one registered Orientation Operator;
4. executes the required stages in order;
5. preserves object identity, version and provenance;
6. labels observed, derived, proposed and unknown findings;
7. validates independently of provider output;
8. emits the common report envelope and correct mode payload;
9. emits only evidence-supported continuation options;
10. preserves every authority and no-effect boundary in this document;
11. passes canonical success, partial, blocked, clarification, unsupported and
    invalid cases for every mode;
12. produces no provider-specific field at the public boundary.

Conformance is behavioral, not vendor-based. A provider change may alter
non-canonical proposed content. It may not alter contract fields, stage order,
status semantics, evidence requirements, validation or authority.

## 22. Required future specifications before implementation

This behavioral contract intentionally does not approve runtime code. The
following remain separate implementation milestones:

- a versioned public Orientation Request wire schema;
- a versioned Orientation Report wire schema;
- a `ClarificationRequired` result schema;
- working Representation schemas for each mode;
- evidence and provenance exchange schemas;
- continuation option schema and request-delta rules;
- an Orientation Operator registry and version compatibility policy distinct
  from the Transition Operator Registry;
- per-mode canonical fixtures and conformance tests;
- deterministic ordering and budget algorithms;
- backend proposal and validation profiles;
- approved NEXAHEDRON gateway compatibility and error semantics;
- security, access, cancellation, audit and retention policy;
- an ADR only if a future implementation changes a frozen ORION v1 term,
  responsibility, authority, dependency or public contract decision.

Until those specifications are approved, the NEXAHEDRON ORION gateway remains
unavailable and deterministic fixtures remain the only Laboratory runtime data.

## 23. Canonical invariants

1. One request selects one Orientation Operator.
2. Orientation Mode expresses Human intention; it is not an identity or role.
3. Missing required input produces clarification, never guessing.
4. Orientation Objects retain identity, version, ownership and provenance.
5. Working Representations are immutable, traceable and non-canonical.
6. Evidence remains distinct from interpretation and confidence.
7. Unknown, unsupported, partial and blocked are valid explicit outcomes.
8. No report field outruns its evidence.
9. Continue Orientation is suggested by ORION and chosen by the Human.
10. Continuation preserves references but never silently changes mode or scope.
11. NEXAHEDRON presents the contract and never reimplements it.
12. LYRA translates and explains but never operates, routes or validates.
13. Library and Atlas remain read-only under this contract.
14. Reflection meaning and consequential decisions remain Human authority.
15. Providers are replaceable; the behavioral contract is not.
