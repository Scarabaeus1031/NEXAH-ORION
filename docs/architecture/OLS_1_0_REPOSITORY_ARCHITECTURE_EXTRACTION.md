# OLS 1.0 — Repository Architecture Extraction

## Orientation Language Specification: architectural synthesis and navigation draft

- Status: first repository-extraction draft; informative
- Date: 2026-07-25
- Scope: NEXAH Research & Framework, NEXAH-ORION, NEXAH Experience, Library,
  Living Concepts, JANUS, IEEE validation, applications, research, and visual
  architecture
- Semantic authority: the published `OLS-RELEASE-1.0.0` suite in
  `NEXAH/ORIENTATION_LANGUAGE/SPECIFICATION/RELEASES/OLS-RELEASE-1.0.0/`
- ORION authority: the certified ORION Version 1 baseline and its accepted
  architecture
- Purpose: reveal and connect existing language; no new terminology,
  semantics, operator, profile, transition, or implementation authority

> This document is not a replacement copy of OLS 1.0. The repository already
> contains a released, checksum-backed Orientation Language Specification:
> OLS-0 through OLS-6 and the informative OLS-I companion. This extraction
> supplies the cross-repository architectural layer requested for contributors.
> If this document conflicts with the released OLS suite, the released suite
> governs OLS semantics. If it conflicts with ORION's certified baseline, that
> baseline governs ORION.

## 0. Archaeological method and evidence status

This extraction follows the repository's own separation of authority:

1. released OLS clauses and registries establish Orientation Language meaning;
2. accepted architecture establishes subsystem responsibilities and
   boundaries;
3. executable contracts and tests establish bounded implementation behavior;
4. validation records establish only the claims within their declared scope;
5. research, Works, diagrams, and historical artifacts supply evidence,
   hypotheses, recurrence, and rationale without silently becoming normative
   language.

Terms are classified in this document as:

| Status | Meaning |
| --- | --- |
| **Universal primitive** | One of the fourteen concepts owned by OLS-1 |
| **Declaration** | One of the ten instance-level declarations owned by OLS-2 |
| **Primitive operator** | One of the ten operator contracts owned by OLS-2 |
| **Profile primitive** | One of the four concepts owned by an OLS-3 profile |
| **Semantic product** | One of the eleven products registered by OLS-4 |
| **Accepted derivation** | A distinction registered unconditionally under its OLS-4 inputs and conditions |
| **Conditional derivation** | A distinction available only when its OLS-4 conditions are explicit |
| **Conceptual architecture term** | An established term outside the OLS 1.0 primitive inventory |
| **Research or domain term** | A term whose meaning remains local to research, an application, a Work, or a declared representation |
| **Historical term** | Preserved evidence that does not define current semantics |

Repository recurrence alone is not enough to promote a term. The Living
Concepts boundary says that finding a term does not authorize the system to
decide its meaning. The OLS suite similarly requires one owner for each
primitive and preserves historical language without importing it silently.

---

## 1. High-level overview

### 1.1 What OLS is

The Orientation Language Specification is the semantic contract for describing
orientation across NEXAH.

Its Universal Base Language describes orientation as situated,
representation-dependent, perspective-dependent, context-bound, and
evidence-bounded. It preserves provenance and uncertainty while separating:

- observation from evidence;
- representation from reality;
- relation from causality;
- comparison from preference;
- orientation from recommendation;
- selection from authorization;
- transformation from improvement;
- validation from truth;
- recording from learning;
- software capability from Human authority.

The released suite is organized as:

| Part | Existing responsibility |
| --- | --- |
| OLS-0 | Suite conventions, stable identifiers, references, registries, and publication rules |
| OLS-1 | Universal Base Language |
| OLS-2 | Declarations and primitive operator contracts |
| OLS-3 | Semantic profiles, ownership, activation, dependency, and composition |
| OLS-4 | Semantic products, derivations, transitions, outcomes, recording, and learning boundaries |
| OLS-5 | Conformance targets, tests, evidence, reporting, and certification boundaries |
| OLS-6 | Extensions, compatibility, versioning, deprecation, publication, and governance |
| OLS-I | Informative explanation, examples, mappings, implementation guidance, history, and research trace |

### 1.2 What problem it solves

The repository repeatedly uses the same words across different authority
domains: Research, OLS, the Orientation Kernel, ORION, NEXAHEDRON, the Library,
Living Concepts, JANUS, IEEE applications, and visual Works. Without an
explicit language boundary, a recurring label can be mistaken for:

- a universal semantic primitive;
- an executable software type;
- a validated scientific mechanism;
- a canonical Library identity;
- an authorized action;
- or a general truth.

OLS solves this by assigning semantic ownership, making declarations explicit,
typing operator responsibilities, governing legal composition, preserving
status through transitions, and requiring conformance evidence.

### 1.3 Why it exists

NEXAH's recurring principle is **Understanding before action**. OLS gives that
principle a stable semantic foundation that can be used by Humans, documents,
applications, and implementations without transferring authority among them.

The public ecosystem architecture states the separation directly:

```text
Research                 → evidence
Orientation Language     → semantics
Implementations          → executable behavior
Applications             → domain use and validation
Living Library           → editorial communication
Editorial Operating System → governance and controlled execution
```

OLS exists so these responsibilities can coordinate through shared references
without collapsing into one another.

### 1.4 The shortest faithful model

The canonical universal process is:

```text
OBSERVE
  ↓
REPRESENT
  ↓
COMPARE
  ↓
ORIENT
  ↓
EXPLAIN
```

This is semantic order, not a required software deployment topology. A complete
universal process contains all five stages in that order. Repetition may return
to an earlier stage when new observations or uncertainties arise.

The sequence does **not** imply recommendation, authorization, execution,
validation, outcome, learning, control, certainty, or empirical truth.

### 1.5 Relationship to the older general Orientation Grammar

ORION contains a canonical conceptual document, `The Language of Orientation`,
whose sequence is:

```text
Reality
  ↓
Reference Space
  ↓
Coordinate System
  ↓
Representation
  ↓
Structural Representation
  ↓
Relations
  ↓
Expression
  ↓
Integration
  ↓
Observation Again
```

This remains useful conceptual architecture, especially for the distinctions
among Reference Space, Coordinate System, Representation, and Reality. It is
not the released OLS 1.0 primitive inventory or operator grammar.

The two sequences are compatible at the level of intent but are not identical:

| General Orientation Grammar | Released OLS 1.0 reading |
| --- | --- |
| Reality | Outside the language; representation must remain distinct from it |
| Reference Space | Composite conceptual condition; see Section 8 |
| Coordinate System | Accepted `coordinate` derivation plus applicable declarations |
| Representation | Universal primitive and `OP-REPRESENT` product |
| Structural Representation | Representation specialization; certified ORION concern |
| Relations | Universal `relation` primitive |
| Expression | Primarily `OP-EXPLAIN`; ORION has a separately certified Expression boundary |
| Integration | Human/application responsibility; not a universal OLS operator |
| Observation Again | Permitted recursive return to `OP-OBSERVE` |

This mapping is interpretive navigation. It does not rename OLS elements.

---

## 2. Design principles supported by repository evidence

### 2.1 Included principles

| Principle | Repository-supported meaning | Evidence |
| --- | --- | --- |
| Human-readable | The normative suite, companion, examples, diagrams, and reports are written for inspection and citation by Humans. | OLS-0 reading paths and citation rules; OLS-I; Library reader paths |
| Implementation-independent | Contracts state semantic obligations independently of software, storage, interface, provider, or execution technology. | OLS-2 Primitive Operator Contract Model; OLS-5 target classes |
| Composable | Profiles compose only through explicit activation, dependency resolution, ownership, and conflict rules. | OLS-3 |
| Reference-oriented | Stable IDs, versions, source references, identities, and cross-references survive path changes. | OLS-0; OLS-6; Library Registry; ORION contracts |
| Extensible | New profiles, operators, declarations, and informative components enter through governed registration and versioning. | OLS-6 |
| Provenance-aware | Provenance is a universal primitive/status preserved through applicable operations and products. | OLS-1; OLS-2; OLS-4 |
| Evidence-preserving | Evidence class, source, uncertainty, disagreement, and limitations remain distinguishable through orientation and explanation. | OLS-1/2; Orientation Brief; ORION evidence contracts |
| Difference-preserving | Comparison and composition must not erase incompatible perspectives, sources, or statuses. | OLS-1 `difference`; OLS-3 conflict rules; JANUS principle |
| Boundary-preserving | Every operator has prohibited implications; later stages cannot silently acquire another stage's authority. | OLS-1 Universal Boundary Matrix; OLS-2 contracts; OLS-4 prohibitions |
| Determinately assessable | OLS defines stable requirements, tests, statuses, and conformance reports that make a claim assessable. | OLS-5 |
| Open to multiple realizations | Documents, diagrams, graphs, databases, software services, AI systems, and repeatable Human procedures may realize the language. | OLS-I implementation guidance |
| Historically preserving | Deprecated and superseded terms, records, and releases remain visible instead of being rewritten. | OLS-0; OLS-6; repository archive policies |
| Human-governed | Intention, meaning, consequential decision, approval scope, and action remain Human-governed. | OLS-2 authority scope; OLS-3 Editorial Governance; ORION policies |

### 2.2 Candidate principles that require qualification

The following requested examples are only partially supported and should not be
stated without qualification:

| Candidate | Finding |
| --- | --- |
| Machine-readable | Supported as a possible realization and by machine-readable registries/contracts, but OLS 1.0 defines no single normative serialization or schema. |
| Deterministic | ORION's certified core is deterministic. OLS itself specifies semantics and conformance; it does not require every realization or domain process to execute deterministically. |
| Provider-independent | Accurate when read as implementation/provider independence. Providers cannot define semantics, but the released OLS wording generally uses implementation independence. |
| Open | The repository publishes documentation under its declared documentation license and governs extensions openly; “open” is not itself a registered OLS semantic primitive or conformance class. |

---

## 3. Vocabulary

### 3.1 Universal concept primitives

The following fourteen terms are the complete OLS 1.0 universal primitive
inventory.

| Term | Definition | Purpose | Related concepts | Minimal example | Primary reference |
| --- | --- | --- | --- | --- | --- |
| observation | Noticed or captured source material admitted as an observation while retaining declared source status | Separates source material from later representation, claim, evidence, and outcome | observer, provenance, evidence, uncertainty | A recorded voltage sample with source and time | OLS-1 §7.1 |
| observer | Situated role associated with noticing/capturing observations and constructing or reading a representation under perspective and context | Makes the locus of observing explicit | observation, context, perspective, position | A researcher reading an IEEE result from a declared analytical view | OLS-1 §7.2 |
| context | Situational conditions, domain, and scope under which an assertion is interpreted | Bounds applicability and interpretation | perspective, representation, evidence, orientation | “IEEE-14 held-out campaign under the frozen scan design” | OLS-1 §7.3 |
| perspective | Condition or view under which a representation is constructed or read | Preserves viewpoint and disagreement | observer, representation, comparison | Physical-threshold view and graph-topology view of one case | OLS-1 §7.4 |
| representation | Structured, analyzable form constructed from declared observations or data while preserving provenance and status | Makes material inspectable without identifying it with reality | observation, perspective, position, provenance | A state graph, field, table, map, or structural Markdown object | OLS-1 §7.5 |
| position | Location of an observer, focus, or system relative to a declared representation and context | Supports location-dependent orientation | representation, context, state, navigation | Focus node `normal_operation` in a directed graph | OLS-1 §7.6 |
| relation | Declared association between two or more items within a context or representation | Makes connection inspectable without asserting mechanism | position, state, transition, evidence | “Node A has a declared route to Node B” | OLS-1 §7.7 |
| state | Declared condition of an identified subject or represented item within context and, where applicable, time | Separates condition from change or operation | identity, time, transition | IEEE system condition at load scale 1.4 | OLS-1 §7.8 |
| transition | Declared change from one state to another under context, identity, and temporal order | Separates represented change from cause or transformation operator | state, difference, time, identity | A label change between two ordered states | OLS-1 §7.9 |
| evidence | Declared material used to support a claim while retaining provenance, epistemic status, and uncertainty | Keeps support distinct from observation, claim, and validation | observation, provenance, uncertainty | A computed result supporting a bounded software claim | OLS-1 §7.10 |
| provenance | Declared information identifying origin and relevant history/status of observation, representation, or evidence | Preserves trace to source and status | evidence, identity, time, representation | Source revision, method, artifact digest, and owner | OLS-1 §7.11 |
| uncertainty | Unresolved or bounded lack of knowledge, including limitation, missing information, disagreement, or unresolved status | Prevents silent conversion of absence into confidence | evidence, comparison, orientation | “Held-out generalization remains unestablished” | OLS-1 §7.12 |
| orientation | Situated understanding produced from declared observations, representation, context, perspective, focus, evidence, provenance, and uncertainty | States what can be understood before downstream decision or action | all preceding primitives | A report of current position, visible options, evidence, and limits | OLS-1 §7.13 |
| difference | Declared distinction between items, states, perspectives, or representations relative to a basis | Makes non-equivalence available to comparison | comparison, perspective, state | Difference between computed event and physical threshold crossing | OLS-1 §7.14 |

### 3.2 Frozen declarations

Declarations provide instance-level values, assumptions, statuses, and
boundaries. They do not redefine their associated concepts. OLS 1.0 defines
exactly ten.

| Declaration | Purpose | Required when | Key relation |
| --- | --- | --- | --- |
| time | Makes temporal position, order, interval, history, or recurrence explicit | A transition, trajectory, provenance history, outcome, learning, or before/after relation is asserted | state, transition, identity |
| identity | Makes same-subject/work/system continuity explicit | Items across states, times, records, outcomes, trajectories, or editions are treated as continuing | time, provenance |
| scale | Declares level or dimensionality of reading | Meaning, compatibility, pattern, map, geometry, navigation, or transition depends on level | representation type, context |
| context | Declares applicable conditions, domain, and scope | Every orientation act and every representation reading | perspective, representation type |
| perspective | Declares construction or reading view | Every representation and orientation claim | observer, context, position |
| position | Declares the location of observer, focus, or system in a representation | A location, reachability, blocked region, or navigation claim is made | representation type, context |
| representation type | Declares the kind of structured form | Every `REPRESENT` output and represented `ORIENT` input | context, perspective, scale |
| evidence class | Declares epistemic status of supporting material | Material is admitted as evidence | provenance, uncertainty |
| uncertainty status | Declares unresolved status and known limitations | A comparison, orientation, explanation, validation, or report finding is produced | evidence class, provenance |
| authority scope | Declares actor/role, governed operation, target, and scope | Approval, recommendation, publication, execution, or AI pre-action handoff occurs | authority, Human governance |

No declaration has an inferred default. Omission is valid only when no claim in
scope depends on that distinction. Changing a declaration produces an explicit
new state or reference; it does not erase the prior one.

### 3.3 Profile primitives

OLS-3 owns four additional primitives through exactly one profile each:

| Term | Definition | Owner | Boundary |
| --- | --- | --- | --- |
| constraint | Declared condition limiting alternatives, paths, selections, or bounded change | Navigation | Not recommendation, optimality, authority, execution, or validation |
| outcome | Declared observed result whose candidate, validation, and admission status is governed | Evidence/Validation | A transformed state or validation result is not thereby admitted |
| memory | Declared retained record of an observation or admitted outcome with identity, time, provenance, evidence class, and status | Memory/Learning | A record is not thereby validated, canonical, experiential, or learned |
| authority | Declared permission held by an actor/role for a governed operation on a target within scope | Editorial Governance | Evidence, validation, orientation, explanation, selection, or capability is not authority |

### 3.4 Important derived vocabulary

OLS-4 registers existing recurring distinctions rather than promoting all of
them to primitives.

**Accepted derivations**

`comparison`, `signal`, `perception`, `coordinate`, `slice`, `model`, `map`,
`structure`, `system`, `direction`, `change`, `motion`, `transformation`,
`block`, `route`, `navigation`, `journey`, and `operator`.

**Conditional derivations**

`information`, `interpretation`, `meaning`, `knowledge`, `layer`,
`continuity`, `stability`, `emergence`, `flow`, `potential`, `possibility`,
`recurrence`, `pattern`, `boundary`, `threshold`, `path`, `bridge`, and
`composition`.

The conditions matter. For example:

- `boundary` requires difference, relation, representation, and constraint,
  plus a declared classification or constraint rule;
- `stability` requires continuity, state, transition, constraint, a declared
  interval, and perturbation/test criteria;
- `path` is an ordered relation among positions/states and transitions; it is
  not a selected route or recommendation;
- `bridge` connects differentiated sides across a boundary; it is not a causal
  mechanism or a guarantee of safe crossing;
- `knowledge` remains evidence-, provenance-, context-, and
  uncertainty-bounded rather than becoming certainty.

### 3.5 Established terms that remain outside the primitive inventory

| Term | Current repository role | OLS relationship |
| --- | --- | --- |
| Reference Space | Conceptual field within which positions, distinctions, and valid comparisons can be stated | Composite architecture term; see Section 8 |
| Coordinate System | Declared method for locating/measuring within a Reference Space | Related to accepted `coordinate` derivation and declarations |
| Structural Representation | Inspectable declared structure without semantic interpretation | Representation specialization; certified ORION responsibility |
| Orientation Object | Versioned subject and source identity that representations refer to | ORION/public-contract identity construct, not OLS primitive |
| Orientation Report | Immutable public account of an ORION orientation | ORION contract; related to OLS orientation/explanation products but not identical |
| Orientation Brief | Compact Human-facing synthesis of report, perspectives, evidence, disagreements, and boundary | NEXAH implementation contract |
| Reference Frame | Orientation Layer input and software-contract vocabulary | Application/implementation term; not automatically `Reference Space` |
| regime | Research/application classification of system behavior | Domain term; may be represented as state/structure under declarations |
| field | Research representation of structure from dynamics | Representation type/domain model; not a universal primitive |
| landscape | Research or editorial arrangement of positions, regions, and relations | Representation form; no OLS 1.0 primitive status |
| topology | Research/application structure of connectivity and neighborhood | Representation/domain semantics; no universal OLS topology |
| geometry | Research/application spatial or state-space structure | Representation/domain semantics; no universal OLS geometry |
| atlas | Collection or arrangement of declared maps/representations | Informative realization form; not an OLS primitive |
| gate / aperture / corridor | Research terms for transition geometry and constrained passage | Domain distinctions that may use boundary, threshold, path, block, or constraint |
| JANUS | Complementary-perspective principle | Conceptual principle, not a primitive operator |
| Janus Bridge | Architectural translation interface between representations | Possible bridge realization; planned architecture |
| Janus Directional Coherence Operator | Scientific forward/backward trajectory analysis | Experimental scientific operator; not an OLS primitive operator by name |
| LYRA | Historical ORION Human-language translation/explanation boundary | Not OLS semantic authority |
| LUCY | Non-normative reflection concept exploration | Outside certified ORION and OLS authority |

---

## 4. Grammar

### 4.1 Normative universal grammar

OLS 1.0 combines concepts through declared operator contracts:

```text
identifiable source material
  + applicable declarations
        ↓ OP-OBSERVE
observation
        ↓ OP-REPRESENT
representation
        ↓ OP-COMPARE
comparison finding
        ↓ OP-ORIENT
orientation finding
        ↓ OP-EXPLAIN
explanation
```

At every stage, applicable context, perspective, representation type, evidence
class, uncertainty status, provenance, and any required time, identity, scale,
or position remain attached.

### 4.2 Question-shaped application grammar

The repository often begins with a Human question. `question` is not an OLS
primitive, but it is an application input that bounds purpose and scope:

```text
Human question / intention
  ↓ declare context, scope, perspective, and authority
identifiable source material
  ↓ OBSERVE
observations
  ↓ REPRESENT within a declared representation type
representation
  ↓ COMPARE under an explicit basis
differences, agreements, and mismatches
  ↓ ORIENT
supported findings + disagreements + unknowns + limits
  ↓ EXPLAIN
Human-readable or machine-carried expression
  ↓ Human integration
decision, revised question, continuation, action, or stop
```

Human integration is outside the universal operator grammar. A decision must
not be inserted between `ORIENT` and `EXPLAIN` as though OLS made it.

### 4.3 Profile composition grammar

Profiles extend the base only after explicit activation and dependency
resolution:

```text
Universal Base Language
  + active profile(s)
  + compatible declarations
  + owner-respecting operator contracts
  + preserved boundaries
  = legal OLS construction
```

Seven Version 1.0 profiles exist:

| Profile | Purpose | Owned primitive/operator | Dependencies |
| --- | --- | --- | --- |
| Representation | Type and construct structured forms | none / none | Universal Base |
| Navigation | Locate positions; construct or select paths/routes under constraints | constraint / SELECT | Representation |
| Transformation | Change a declared form or state | none / TRANSFORM | Representation |
| Evidence/Validation | Test declared subjects against criteria and evidence; govern outcome status | outcome / VALIDATE | Universal Base; conditional others |
| Memory/Learning | Persist observations or admitted outcomes; support bounded experiential learning | memory / RECORD | Evidence/Validation when admitted experience is claimed |
| Editorial Governance | Govern identity, proposal, review, approval, publication, and Human authority | authority / APPROVE | Conditional Memory/Learning or Evidence/Validation |
| Education | Organize learner/reader entry, practice, reflection, navigation, and fluency | none / none | Navigation |

### 4.4 Experiential grammar

The canonical experiential order is:

```text
observation
  ↓ optional transformation
transformation result
  ↓ post-transformation observation with same identity and later time
candidate outcome
  ↓ validation against declared criteria and evidence
validation result
  ↓ admission status transition
admitted outcome
  ↓ RECORD
recorded experience
  ↓ COMPARE with prior memory/knowledge + RECORD resulting change
learned knowledge
```

Each arrow is conditional on the owning profile and declarations. No later
state repairs a missing earlier state.

### 4.5 Grammar invariants

1. Every semantic element has one owner.
2. Applicable declarations precede the claim or operation that depends on them.
3. Operators preserve relevant source status, provenance, evidence class,
   uncertainty, disagreement, and limitations.
4. A relation does not imply cause.
5. A representation does not imply reality.
6. A possible path does not imply a selected, recommended, authorized, or
   executed path.
7. Validation is criterion- and scope-bounded.
8. Approval changes governed status; it does not change empirical truth.
9. Recording preserves status; it does not produce learning.
10. Composition cannot legalize a prohibited implication.

---

## 5. Primitive concepts

The smallest released OLS building blocks are not all terms found in the
repository. They are the explicitly owned inventories:

```text
Universal concepts (14)
├── observation
├── observer
├── context
├── perspective
├── representation
├── position
├── relation
├── state
├── transition
├── evidence
├── provenance
├── uncertainty
├── orientation
└── difference

Profile concepts (4)
├── constraint        [Navigation]
├── outcome           [Evidence/Validation]
├── memory            [Memory/Learning]
└── authority         [Editorial Governance]
```

Time, identity, and scale are intentionally declarations rather than universal
concept primitives. Boundary, path, bridge, map, coordinate, and navigation are
derivations. Geometry, topology, landscape, Reference Space, regime, gate, and
atlas remain architecture, representation, research, or domain vocabulary.

This classification prevents the repository's richest metaphors and scientific
models from being mistaken for universal language axioms.

---

## 6. Operators

### 6.1 Universal operators

| Operator | Inputs | Output | Purpose | Principal boundary |
| --- | --- | --- | --- | --- |
| OBSERVE | Identifiable source material with source/provenance status and applicable declarations | Observation(s) linked to source and declarations | Notice or capture signals, events, measurements, or context | Does not establish truth, evidence, causality, completeness, or outcome |
| REPRESENT | Declared observations/data with source, provenance, and status | Declared representation with type, perspective, provenance, and statuses | Construct a structured, analyzable form | Does not establish reality, completeness, causal mechanism, or validation |
| COMPARE | Two or more compatible declared items plus comparison basis | Findings of difference, agreement, or mismatch | Make distinctions inspectable | Does not establish causality, preference, selection, prediction, validation, or law |
| ORIENT | Observations, representation, comparison findings, context, perspective, focus/position, evidence, provenance, uncertainty, and limits | Orientation finding with supported, disputed, unsupported, uncertain, and limited statuses | Produce situated understanding | Does not establish recommendation, authorization, execution, outcome, learning, control, or certainty |
| EXPLAIN | Findings/orientation and all relevant statuses | Explanation retaining support, disagreement, uncertainty, unsupported conclusions, and limits | Communicate structured findings faithfully | Does not establish truth, proof, consensus, authority, recommendation, or approval |

### 6.2 Profile operators

| Operator | Owner | Inputs | Output | Purpose | Principal boundary |
| --- | --- | --- | --- | --- | --- |
| SELECT | Navigation | Alternatives, selection basis/constraint, and representation | Selection result with alternatives, basis, evidence, provenance, and uncertainty | Choose under a declared basis | Not recommendation, authority, execution, or optimality |
| TRANSFORM | Transformation | Input form/state, transformation description, and applicable constraint | Resulting form/state linked to input and declarations | Change form or state while preserving input/output distinction | Not improvement, stability, validation, admitted outcome, authorization, or success |
| VALIDATE | Evidence/Validation | Claim/model/change/candidate, criteria, and evidence | Scoped validation result | Test a declared subject against declared criteria and evidence | Not causality, universality, truth, authority, publication, or automatic admission |
| RECORD | Memory/Learning | Observation or admitted outcome with identity, time, provenance, evidence, status, and uncertainty | Record reference/state preserving all statuses | Persist declared material | Not validation, canonical status, experiential status, or learning merely from storage |
| APPROVE | Editorial Governance | Governed proposal/item, actor/role, target, authority scope, and relevant evidence/status | Approval or rejection status with actor, scope, target, and provenance | Perform a governed Human-authority status change | Not empirical truth, validation, outcome admission, or automatic execution |

### 6.3 Relationship to recurring non-OLS operator collections

The repository contains at least three other operator families:

1. **ORION Orientation Operators** — Wonder, Understand, Compare, Connect,
   Explore, Build, and Reflect. These are mode-level behavioral contracts that
   orchestrate orientation work; they are not replacements for the OLS
   primitive operator registry.
2. **ORION Transition Operator Registry** — immutable metadata for candidate
   T01–T15 representation transformations. Version 1 entries are non-executable
   capability declarations.
3. **Library Editorial Operators** — controlled concepts used to navigate and
   relate Works. The public Atlas explicitly states that these are not
   executable ORION operators.

Scientific operators such as the Janus Directional Coherence Operator remain a
fourth, method-specific family. Their evidence and implementation status must
not be promoted by the shared word “operator.”

---

## 7. Orientation records

### 7.1 Finding: no single universal Orientation Record type

The repository has an implicit record model, but OLS 1.0 does not define one
universal serialized `OrientationRecord`. Instead, it defines:

- semantic products and their preserved statuses;
- `OP-RECORD`;
- recording eligibility;
- conformance evidence and reports;
- identity, time, provenance, evidence, uncertainty, and authority rules.

Implementations then realize those responsibilities through different bounded
records.

### 7.2 Minimal implicit record anatomy

Across OLS, ORION, the Orientation Layer, Library, validation, and research
templates, an orientation-preserving record contains:

| Record concern | Existing field or semantic source |
| --- | --- |
| Stable identity | Product, request, report, evidence, Work, Edition, episode, or artifact identity plus version |
| Subject | Identifiable source material or Orientation Object |
| Question/intention | Human-owned purpose, focus, and success boundary where applicable |
| Scope/context | Declared context, inclusions, exclusions, and unresolved scope |
| Perspective | Construction and/or reading perspective |
| Representation | Type, version, source link, scale, and declared lossiness |
| Position/focus | Location relative to the representation when applicable |
| Process | Ordered operator/stage references and statuses |
| Findings | Supported, disputed, unsupported, blocked, or unknown conclusions |
| Relations/transitions | Typed endpoints, basis, order, and applicable conditions |
| Evidence | Evidence references and classes |
| Provenance | Source, owner, history, method, transformation steps, and digests |
| Uncertainty | Known limitations, missing information, disagreement, and unresolved status |
| Validation | Criteria, scope, checks, result, and issues |
| Authority/effects | Actor/role, authority scope, governed status, and explicit effects |
| Continuation | New question, continuation option, clarification, or stop |
| Immutability/history | Supersedes/reference chain rather than in-place rewriting |

### 7.3 Existing record realizations

| Record | Location/owner | Preserves | Explicit boundary |
| --- | --- | --- | --- |
| OLS semantic products | OLS-4 | Product type, owner, origin, declarations, statuses | Products do not inherit prohibited downstream meanings |
| ORION Orientation Request | ORION public contracts | Human intention, scope, authority, objects, constraints | Request is not a completed orientation |
| ORION Evidence Reference | ORION public contracts | Source identity, authority, class, provenance, validation, traceability | Evidence reference does not transfer source authority |
| ORION Orientation Report | ORION public contracts | Process, representations, findings, evidence, uncertainty, validation, continuations | Not NEXAH truth, Human meaning, or decision |
| Orientation Brief | NEXAH Orientation Layer | Question, perspectives, agreement/disagreement, evidence, boundaries, reproduction | Not recommendation, prediction, command, or decision |
| Episode | NEXAH Orientation Layer | Immutable State–Report–Outcome lineage | No observed outcome means no episodic memory update |
| Library Entity/Work/Edition | Library Registry | Stable editorial identity, classification, relationships, source resolution | Editorial identity is not OLS semantics or scientific truth |
| Living Concept occurrence/dossier | Editorial Operating System | Discovery, definition provenance, and claim support separately | Occurrence does not establish meaning or validity |
| Validation record | `validation/` campaigns | Frozen method, artifacts, metrics, failures, conclusion, reproduction | Passing scope does not generalize to domain truth or operational safety |
| Research/experiment record | templates and Research | Question, method, evidence, limitations, status | Hypothesis or recurrence is not released semantics |

### 7.4 Preservation and decision history

Knowledge is preserved through:

- immutable identity plus version;
- append-only or superseding records rather than silent mutation;
- explicit source and provenance chains;
- separation of observation, computation, inference, proposal, validation, and
  observed outcome;
- retained counterevidence and failure cases;
- explicit uncertainty and blocked states;
- checksum-backed releases and reproducible commands;
- Human-governed approval and publication status.

Decisions are documented through accepted ADRs, authority-scoped approval,
Library/Editorial review, release manifests, validation records, and ORION
report/continuation lineage. A later decision does not rewrite the evidence
that preceded it.

---

## 8. Reference spaces

### 8.1 Reference Space is a composite architecture term

The general Orientation Grammar defines Reference Space as the field within
which positions, differences, and comparisons can be stated. It determines
membership, relevant distinctions, valid comparisons, and boundaries.

Released OLS 1.0 does not register `Reference Space` as a universal primitive,
declaration, or profile primitive. Its responsibility is distributed across:

```text
Reference Space
├── context              situational conditions, domain, and scope
├── representation       structured form in which items become inspectable
├── perspective          construction/reading condition
├── scale declaration    level or dimensionality of reading
├── position declaration located focus relative to representation
├── relation             associations that are valid in the declared field
├── difference           distinctions relative to a basis
├── constraint           admissible alternatives or bounded change
└── boundary derivation  separation/interface under an explicit rule
```

This is the strongest repository-supported mapping, but it remains a mapping.
A future normative alias or composite contract would require OLS governance.

### 8.2 Reference

`reference` appears in several non-equivalent forms:

- stable semantic IDs and clause references in OLS;
- source/evidence references in ORION;
- reference frames in the Orientation Layer;
- canonical Work/Edition resolution in the Library;
- comparison bases and coordinate references in research;
- public URLs and repository paths in documentation.

All share an addressing role. They do not share one universal type.

### 8.3 Scale

Scale is an OLS-2 declaration. It makes level or dimensionality explicit where
meaning depends on it. Cross-scale comparison requires an explicit compatible
basis and must preserve the source scale.

IEEE scaling validation demonstrates why this matters: a pattern appearing
across several systems did not establish a resolution-independent universal
precursor, and the held-out large system closed as a boundary of validity
rather than cross-scale support.

### 8.4 Boundary

Boundary is an OLS-4 conditional derivation from difference, relation,
representation, and constraint under an explicit classification or constraint
rule. It means a separation or interface, not necessarily a wall, mechanism,
or impermeable barrier.

The repository also uses authority boundaries, repository boundaries, source
boundaries, rendering boundaries, validation boundaries, outcome firewalls,
and scientific boundaries of validity. Each must declare its basis; their
shared label does not make them interchangeable.

### 8.5 Context

Context is both a universal primitive and an OLS-2 declaration. It bounds every
orientation act and representation reading. A claim cannot be generalized
beyond context without a separately declared and supported context.

### 8.6 Perspective

Perspective is both a universal primitive and an OLS-2 declaration. JANUS
reinforces the need for complementary perspectives without forced fusion.
Multiple perspectives may agree, contradict, or remain incomparable. Majority
agreement does not create truth.

### 8.7 Landscape

Landscape recurs in research, applications, visual communication, and the
public Atlas. It usually describes a representation containing regions,
positions, relations, gradients, routes, or transition possibilities.

It is not an OLS primitive or frozen representation type. A specific landscape
must declare its representation type, scale, context, perspective, provenance,
and the meaning of its geometry.

### 8.8 Topology

Topology appears in:

- research on connectivity, neighborhood, gates, and emergent structure;
- graph representations and network orientation;
- Möbius topology in the historical ORION Transform Stack;
- public relationship maps.

OLS can describe topology through representation, relation, structure, system,
boundary, path, connectivity-specific domain semantics, and declarations.
OLS 1.0 does not define a universal topology or topological equivalence.

The ORION Transform Stack explicitly says it does not claim a new geometry or
scientific theory; most historical edges remain at low evidence levels.

### 8.9 Geometry

Geometry appears in state-space reconstruction, transition geometry, observer
geometry, IEEE Geometry, Lissajous geometry, atlas work, and visual Works.

Geometry is therefore a family of declared representations and domain methods,
not one OLS primitive. A geometry claim must identify:

- represented subject and identity;
- coordinate/reference basis;
- scale and dimensionality;
- perspective;
- relations, distances, or neighborhood rules;
- method and provenance;
- validation scope;
- uncertainty and prohibited interpretations.

IEEE Geometry validation establishes reproducibility of a frozen campaign and
its artifacts. It explicitly does not validate operational-grid behavior,
prediction, physical stability, causal control, or real-world generalization.

### 8.10 Coordinate System

The general Orientation Grammar distinguishes a Coordinate System from its
Reference Space. Changing coordinates may change notation, origin, units, or
scale while preserving referents and relations. If the valid comparisons
change, the repository treats that as more than a coordinate change.

OLS-4 derives `coordinate` from position and representation through
`REPRESENT`, with representation type and scale. Coordinates do not imply
physical location or equivalence across representation types.

---

## 9. Relationship to ORION

### 9.1 Hypothesis assessment

> Hypothesis: OLS describes orientation. ORION processes orientation.

**Finding: broadly supported, but too broad without ORION's certified scope.**

A more exact statement is:

> OLS defines the semantics and boundaries of orientation constructions.
> ORION Version 1 deterministically constructs and certifies a bounded
> structural navigation and expression chain over accepted representations.

The distinction is evidenced by both repositories:

| OLS | ORION |
| --- | --- |
| Owns released semantic concepts, declarations, primitive operator contracts, profiles, derivations, transitions, and conformance model | Owns the certified Structural Representation, UNDERSTAND inventory, Relations, Navigation, Orientation Map, and Expression boundaries |
| Is implementation-independent | Has a certified deterministic implementation baseline |
| Does not execute applications or establish domain validity | Executes only its certified responsibilities and stops at explicit boundaries |
| Permits multiple realization technologies and Human procedures | Uses immutable artifacts, canonical serialization, provenance chains, and deterministic replay |
| Does not grant recommendation, authority, execution, outcome, or certainty | Does not own Human meaning, decisions, applications, presentation, LYRA execution, Runtime, or Gateway in certified v1 |

### 9.2 Important non-equivalence

ORION Version 1 is not documented as a conforming implementation of the entire
OLS 1.0 suite. It predates or independently freezes several public and
historical contract families, and its certified scope is deliberately narrower
than all OLS profiles/operators.

Therefore:

- OLS conformance must not be inferred from semantic similarity;
- ORION's deterministic certification must not be generalized to every OLS
  realization;
- ORION Orientation Operators must not be treated as OLS primitive operators;
- an ORION Orientation Report must not be treated as the one universal OLS
  record type;
- the T01–T15 representation graph must not be treated as the universal OLS
  transition graph.

### 9.3 ORION processing correspondence

| ORION certified stage | Closest OLS responsibility | Difference |
| --- | --- | --- |
| Structural Representation | representation / REPRESENT | ORION certifies a particular structural domain and construction |
| UNDERSTAND inventory | observation/representation inspection | Inventory establishes declared structure, not general interpretation |
| Relations | relation / COMPARE-adjacent structure | ORION creates certified structural/declared relations under its contracts |
| Navigation | Navigation profile concepts | ORION navigation has its own immutable contract and certified construction |
| Orientation Map | map derivation and Representation/Navigation profiles | ORION certifies one bounded map object |
| Expression | EXPLAIN-adjacent communication | ORION's Expression boundary is a certified structural communicative contract, not Human meaning |

### 9.4 LYRA naming collision

Historical ORION documents call LYRA “The Language of Orientation.” Current
ecosystem architecture assigns LYRA a narrower translation and faithful
explanation role, while OLS is the released semantic authority.

The current interpretation is:

```text
OLS   = semantic language specification
LYRA  = Human-language translation/explanation boundary
ORION = deterministic structural navigation/expression processor
```

LYRA may change phrasing but not identity, status, evidence, provenance, route,
validation, or blockers. This distinction should remain explicit in future
documentation.

---

## 10. Relationship to NEXAHEDRON and the wider ecosystem

### 10.1 Language, engine, workspace, and applications

The repository supports the following responsibility map:

| Layer | Current identity | Responsibility | Does not own |
| --- | --- | --- | --- |
| Language | OLS 1.0 | Semantics, declarations, operator contracts, profiles, derivations, conformance, evolution | Execution or domain truth |
| Research programme | Orientation Science / NEXAH Research | Hypotheses, models, experiments, evidence, limitations | Released semantics by itself |
| Framework / implementation engine | NEXAH Orientation Kernel and bounded backends | Executable orientation behavior and application contracts | OLS semantic authority |
| Certified processor | ORION | Deterministic structural representation, relations, navigation, maps, and expression in its frozen scope | Human meaning, decision, broad runtime/application state |
| Human Workspace | NEXAHEDRON | Presentation, interaction, session state, transport adaptation, reflection and continuation UX | Orientation semantics or autonomous decision |
| Applications | Network Orientation, IEEE Geometry, power systems, Orientation Translation, and other domain programs | Select and validate declared semantics in a domain | Generalization beyond evidence or redefinition of OLS |
| Library | Living Library and Registry | Work/Edition identity, curation, relationships, source resolution, reader paths | OLS meaning or ORION navigation |
| Editorial Operating System | Editorial governance and controlled execution | Review, approval, publication, and bounded knowledge contracts | Specification Governance or empirical truth |
| Public Experience | NEXAH Experience | Visitor entry, Atlas, Library, Laboratory, reading and orientation presentation | Hidden inference or semantic authority |

### 10.2 NEXAHEDRON boundary

NEXAHEDRON is the Human-facing Orientation Laboratory/Workspace. It:

- receives Human material, intention, and scope;
- maintains interaction and session state;
- presents clarification, reports, evidence, and continuations;
- adapts transport without changing contracts;
- leaves interpretation, reflection, and decision with the Human.

It does not become the language, the semantic engine, ORION, the Library, or
the source of canonical truth.

### 10.3 End-to-end ecosystem path

```text
Human intention
  ↓
NEXAHEDRON interaction and confirmation
  ↓
OLS-governed semantic references and declared boundaries
  ↓
Framework / Library resolution
  ↓
ORION public request boundary
  ↓
ORION certified structural processing within supported scope
  ↓
public outcomes, evidence, uncertainty, blockers, continuations
  ↓
LYRA faithful explanation
  ↓
NEXAHEDRON presentation
  ↓
Human interpretation, continuation, decision, or stop
```

This path is an ecosystem architecture, not one runtime already certified in
full.

---

## 11. Relationship to external standards and models

OLS is not equivalent to any of the following. The comparison identifies
possible carrier or modeling relationships only.

| External form | Similarity | Difference from OLS | Plausible relationship |
| --- | --- | --- | --- |
| JSON | Textual, language-independent carrier for structured values | JSON defines data interchange syntax, not orientation semantics, provenance rules, authority, evidence classes, profiles, or derivation legality | A JSON schema could encode an OLS expression or conformance report, but OLS 1.0 defines no single normative JSON encoding |
| RDF | Stable identifiers, relations, graphs, provenance-friendly ecosystem, multiple serializations | RDF's graph data model does not by itself impose OLS operator order, declarations, boundary conditions, status preservation, or Human authority | OLS concepts/products could be mapped to RDF resources and statements through a governed profile |
| Property Graphs | Nodes, typed relationships, properties, paths, graph navigation | A property graph is a data model; its labels/properties do not automatically carry OLS evidence, uncertainty, provenance, semantic ownership, or prohibited implications | Useful representation type for relations, maps, paths, records, and application-specific navigation |
| Knowledge Graphs | Connected entities, concepts, relations, identifiers, and provenance may be represented | “Knowledge graph” is a broad architectural category, not one uniform standard; OLS does not claim that every represented relation is knowledge or truth | A knowledge graph may be one OLS realization if it preserves OLS declarations, evidence/status, ownership, and boundaries |
| DSLs | Controlled vocabulary, grammar, contracts, profiles, and conformance rules are domain-specific | OLS 1.0 is primarily a semantic specification and does not freeze one concrete textual or executable syntax | OLS can govern one or more future DSL syntaxes without becoming identical to their parsers or runtimes |
| glTF | Versioned, extensible, machine-readable representation format with explicit scene/asset structure | glTF is specialized for runtime 3D asset delivery; it does not define evidence-bounded orientation semantics | A glTF asset may realize a geometric or visual OLS representation if identity, provenance, scale, perspective, and lossiness are carried separately |
| Markdown / CommonMark | Human-readable structured documents; headings, lists, links, and code blocks support explanation and citation | Markdown defines document syntax/presentation, not semantic identity, evidence status, operator contracts, or conformance | Markdown is an informative or application carrier for specifications, reports, briefs, and examples |

Primary external references used for this comparison:

- JSON: IETF [RFC 8259](https://www.rfc-editor.org/info/rfc8259/)
- RDF: W3C [RDF 1.2 Concepts and Abstract Data Model](https://www.w3.org/TR/rdf12-concepts/)
- Property graph query/model standard: [ISO/IEC 39075:2024 — GQL](https://www.iso.org/standard/76120.html)
- glTF: Khronos [glTF 2.0 Specification](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html)
- Markdown: [CommonMark Specification](https://spec.commonmark.org/current/)

No external format becomes OLS-conformant merely because it can carry similar
shapes.

---

## 12. Repository map

Paths below use repository-qualified prefixes:

- `NEXAH/` — Research & Framework repository
- `ORION/` — NEXAH-ORION repository
- `EXPERIENCE/` — NEXAH Experience repository

### 12.1 Canonical language

| Component | Current location | Status |
| --- | --- | --- |
| OLS entry point | `NEXAH/ORIENTATION_LANGUAGE/README.md` | Canonical subsystem navigation |
| Ecosystem overview | `NEXAH/ORIENTATION_LANGUAGE/OVERVIEW.md` | Informative architecture |
| OLS architecture | `NEXAH/ORIENTATION_LANGUAGE/ARCHITECTURE.md` | Architecture without semantic redefinition |
| OLS repository architecture | `NEXAH/ORIENTATION_LANGUAGE/REPOSITORY_ARCHITECTURE.md` | Canonical-copy and directory rules |
| Published suite | `NEXAH/ORIENTATION_LANGUAGE/SPECIFICATION/RELEASES/OLS-RELEASE-1.0.0/` | Immutable release unit |
| OLS-0 | `.../DOCUMENTS/OLS-0_SPECIFICATION_CONVENTIONS_AND_SUITE_OVERVIEW_V1.0.md` | Normative as marked |
| OLS-1 | `.../DOCUMENTS/OLS-1_UNIVERSAL_BASE_LANGUAGE_V1.0.md` | Universal primitives and process |
| OLS-2 | `.../DOCUMENTS/OLS-2_DECLARATIONS_AND_OPERATOR_CONTRACTS_V1.0.md` | Declarations and primitive contracts |
| OLS-3 | `.../DOCUMENTS/OLS-3_SEMANTIC_PROFILES_AND_COMPOSITION_V1.0.md` | Profiles and composition |
| OLS-4 | `.../DOCUMENTS/OLS-4_DERIVATIONS_AND_SEMANTIC_TRANSITIONS_V1.0.md` | Products, derivations, transitions |
| OLS-5 | `.../DOCUMENTS/OLS-5_CONFORMANCE_AND_TESTING_V1.0.md` | Conformance |
| OLS-6 | `.../DOCUMENTS/OLS-6_EXTENSIONS_VERSIONING_AND_GOVERNANCE_V1.0.md` | Evolution and governance |
| OLS-I | `.../DOCUMENTS/OLS-I_INFORMATIVE_COMPANION_V1.0.md` | Informative companion |
| Release evidence | `.../RELEASE_MANIFEST.md`, `DOCUMENT_SHA256SUMS`, `PACKAGE_SHA256SUMS`, `REVIEW/` | Publication identity and verification |
| Visual ecosystem map | `NEXAH/ORIENTATION_LANGUAGE/VISUALS/CANONICAL/orientation-language-ecosystem-ols-1.0.0.png` | Informative visual |

### 12.2 Conceptual and scientific origins

| Component | Current location | Status |
| --- | --- | --- |
| Research portal | `NEXAH/RESEARCH/README.md` | Evidence and hypothesis navigation |
| Concept relations | `NEXAH/RESEARCH/CORE_CONCEPT_MAP.md` | Research synthesis |
| Foundation | `NEXAH/RESEARCH/FOUNDATION/` | Assumptions and structural grammar |
| Field, vessel, geometry, phase | `NEXAH/RESEARCH/CORE_CONCEPTS/` | Active research vocabulary |
| JANUS research | `NEXAH/RESEARCH/CORE_CONCEPTS/JANUS_OPERATOR/` | Experimental scientific mechanism |
| JANUS identity decision | `NEXAH/ARCHITECTURE/orientation_layer/DECISIONS/0001-janus-identities.md` | Accepted architecture distinction |
| JANUS concept evidence | `NEXAH/EDITORIAL_OPERATING_SYSTEM/living_concepts/dossiers/` | Non-canonical reviewed concept evidence |
| Research papers | `NEXAH/RESEARCH/PAPER_DRAFT.md` and Research index paths | Integrated research argument |
| Visual research | `NEXAH/RESEARCH/FIGURES/`, `NEXAH/ARCHITECTURE/visuals/` | Visual evidence/synthesis under local status |

### 12.3 Implementation and applications

| Component | Current location | Status |
| --- | --- | --- |
| Orientation Layer | `NEXAH/ARCHITECTURE/orientation_layer/ORIENTATION_LAYER_SPEC.md` | Normative implementation architecture baseline |
| Orientation Brief | `NEXAH/ARCHITECTURE/orientation_layer/ORIENTATION_BRIEF_CONTRACT.md` | Implemented typed contract |
| Concept traceability | `NEXAH/ARCHITECTURE/orientation_layer/CONCEPT_TRACEABILITY.md` | Status and identity boundary |
| Orientation Kernel | `NEXAH/nexah/` | Maintained bounded implementation collection |
| Orientation contracts | `NEXAH/nexah/orientation/` | Typed software realization |
| Applications | `NEXAH/APPLICATIONS/` | Domain use and validation |
| IEEE Orientation validation | `NEXAH/validation/ieee_orientation_v1/` | Frozen bounded validation |
| IEEE Geometry validation | `NEXAH/validation/ieee_geometry_v1/` | Frozen bounded validation |
| IEEE scaling validations | `NEXAH/validation/ieee_scaling_pattern_v1/`, `..._v2/` | Frozen pattern/boundary findings |
| Experimental labs | `NEXAH/EXPERIMENTAL/` | Non-canonical/experimental |
| Demonstrator | `NEXAH/PROTO_CORE/NEXAH_DEMONSTRATOR/` | Preferred executable research path |

### 12.4 ORION

| Component | Current location | Status |
| --- | --- | --- |
| Certified baseline | `ORION/docs/releases/ORION_V1_CERTIFIED_BASELINE.md` | Canonical and frozen |
| Coherent architecture | `ORION/docs/architecture/ORION_ARCHITECTURE.md` | Accepted architecture |
| General Orientation Grammar | `ORION/docs/concepts/THE_LANGUAGE_OF_ORIENTATION.md` | Canonical conceptual definition |
| Representation architecture | `ORION/docs/architecture/REPRESENTATION_ARCHITECTURE.md` | Accepted specialization |
| Structural Representation | `ORION/docs/architecture/STRUCTURAL_REPRESENTATION_ARCHITECTURE.md` | Certified-domain architecture |
| Relations, Navigation, Orientation Map | `ORION/docs/architecture/SLICE_III_*.md` | Certified Slice III architecture |
| Expression | `ORION/docs/architecture/SLICE_IV_*.md` | Certified Slice IV architecture |
| Public contracts | `ORION/docs/architecture/contracts/` | Frozen public contract language |
| Orientation policies/operators | `ORION/docs/architecture/operators/ORION_ORIENTATION_*.md` | Version 1 behavioral architecture |
| Transition graph/contracts | `ORION/docs/architecture/transformations/` | Historical/frozen cartography; no executable transitions |
| Operator registry | `ORION/docs/architecture/operators/OPERATOR_ARCHITECTURE.md` | Declarative non-executable capability inventory |
| LYRA | `ORION/docs/architecture/lyra/LYRA_ARCHITECTURE.md` | Historical/separately governed translation boundary |
| LUCY | `ORION/docs/architecture/lucy/` | Non-normative concept exploration |
| Architecture plates | `ORION/docs/architecture/plates/` | Informative generated visuals with canonical SVG sources |
| Executable proof | `ORION/src/orion/`, `ORION/tests/`, `ORION/scripts/` | Certified and historical scopes as locally documented |

### 12.5 Library, Atlas, and Living Concepts

| Component | Current location | Status |
| --- | --- | --- |
| Library architecture | `NEXAH/LIBRARY/README.md`, `NEXAH/LIBRARY/architecture/` | Editorial identity and reader architecture |
| Canonical Registry | `NEXAH/LIBRARY/registry/` | Human-reviewed Work/Edition/Operator identity |
| Atlas of Atlases | `NEXAH/docs/library/atlas-of-atlases/` | Visual Library entrance and approved reader sequence |
| Living Concepts | `NEXAH/EDITORIAL_OPERATING_SYSTEM/living_concepts/` | Non-canonical review and explanation layer |
| Concept Overlay | `.../living_concepts/overlay/` | Accepted editorial pilot, not Concept Graph |
| Public Atlas | `EXPERIENCE/src/pages/atlas.astro` | Declared relationship presentation |
| Public Library | `EXPERIENCE/src/pages/library.astro` | Reader presentation |
| Public orientation flow | `EXPERIENCE/src/pages/orientation.astro` | Human-facing boundary and evidence presentation |

### 12.6 Cross-repository navigation

```text
NEXAH/README.md
  ↓
NEXAH/REPOSITORY_MAP.md
  ├── ORIENTATION_LANGUAGE/     semantics
  ├── RESEARCH/                 evidence and hypotheses
  ├── nexah/                    implementations
  ├── APPLICATIONS/             domain realizations
  ├── LIBRARY/                  Works and editorial identity
  └── EDITORIAL_OPERATING_SYSTEM/ governance and controlled execution

ORION/README.md
  ↓
ORION/docs/releases/ORION_V1_READING_ORDER.md
  ↓
ORION/docs/releases/ORION_V1_CERTIFIED_BASELINE.md

EXPERIENCE/README.md
  ↓
public Experience, Atlas, Library, Laboratory, and orientation presentation
```

---

## 13. Missing components

The following are documentation/specification gaps revealed by the extraction.
They are not implemented by this draft.

### 13.1 Missing specifications

1. **Normative OLS serialization** — no single JSON, RDF, graph, Markdown, or
   other machine encoding is defined by OLS 1.0.
2. **Orientation expression/record schema** — OLS defines products and record
   semantics but no universal serialized Orientation Record.
3. **Reference Space mapping** — no normative OLS alias or composite contract
   connects the conceptual Reference Space to context, representation,
   perspective, scale, position, relation, constraint, and boundary.
4. **OLS-to-ORION conformance profile** — no governed document states which OLS
   requirements ORION v1 implements, does not implement, or maps differently.
5. **OLS-to-Orientation-Layer mapping** — software contracts such as
   `OrientationState`, `OrientationReport`, `OrientationBrief`, and Episode
   lack one released OLS conformance mapping.
6. **Operator-family namespace specification** — OLS primitive operators,
   ORION mode operators, transition capability operators, Library editorial
   operators, and scientific operators need an explicit cross-family naming
   boundary.
7. **Research-vocabulary profiles** — field, regime, topology, geometry,
   landscape, gate, aperture, corridor, and atlas have no released OLS
   domain-profile mapping.
8. **Concrete representation-type registry** — OLS requires representation
   type declarations but Version 1 does not register an exhaustive graph,
   field, map, table, document, geometric, or atlas type vocabulary.
9. **Provenance carrier profile** — provenance is semantically required, but
   there is no one cross-repository carrier profile for digests, source steps,
   owners, licenses, versions, and lossiness.
10. **Authority handoff contract across the full ecosystem** — Human,
    NEXAHEDRON, LYRA, ORION, Library, Framework, and application authority are
    documented architecturally but not as one released OLS binding.

### 13.2 Missing documentation

1. One public page explaining that OLS and LYRA are not synonyms.
2. One versioned OLS/ORION/NEXAHEDRON responsibility matrix at ecosystem level.
3. A glossary that labels every entry as primitive, declaration, product,
   derivation, architecture term, domain term, or historical term.
4. A crosswalk from the general Orientation Grammar to released OLS elements.
5. A crosswalk from OLS semantic products to ORION public contracts.
6. A contributor guide for deciding whether a new term belongs in Research,
   OLS, an application profile, Library, Living Concepts, or implementation.
7. A documentation status legend shared across repositories.
8. A stable public link strategy for cross-repository clause references.

### 13.3 Missing examples

1. One minimal complete OLS expression carried as JSON without claiming the
   JSON shape is normative.
2. One complete OLS-to-ORION `OrientationRequest`/`OrientationReport` example.
3. One IEEE case showing observation, representation, comparison, orientation,
   explanation, validation, and boundary of validity without status promotion.
4. One JANUS example preserving two perspectives without merging them.
5. One Reference Space change versus Coordinate System change example.
6. One graph/property-graph realization preserving evidence, uncertainty, and
   provenance.
7. One illegal-transition corpus demonstrating every OLS-4 prohibition.
8. One Human approval example proving the separation of validation, approval,
   authorization, execution, and observed outcome.

### 13.4 Missing diagrams

1. Canonical cross-repository OLS–Framework–ORION–NEXAHEDRON–Library authority
   diagram.
2. Primitive/declaration/profile/product/derivation ownership diagram.
3. Orientation Record lineage diagram from observation to learned knowledge.
4. Reference Space composite diagram with explicit non-equivalence status.
5. Operator-family map separating OLS, ORION, Library, and scientific
   operators.
6. Evidence-state diagram separating observed, computed, simulated, inferred,
   proposed, validated, admitted, approved, published, and learned statuses.
7. Research term promotion path showing why recurrence does not create
   normative language.

### 13.5 Missing RFCs or ADRs

1. **Adopt OLS 1.0 references inside ORION without reopening the certified
   baseline.**
2. **Resolve LYRA “Language of Orientation” historical naming against current
   OLS authority.**
3. **Define or reject a normative Reference Space composite in a future OLS
   release.**
4. **Define the first OLS machine carrier while preserving
   implementation-independence.**
5. **Define an OLS conformance target for ORION or explicitly declare that no
   such target is intended.**
6. **Define cross-repository stable URI/identifier resolution.**
7. **Register a domain profile for Orientation Science geometry/topology, or
   preserve those terms as application-owned.**
8. **Define the lifecycle and owner of a universal Orientation Record, or
   explicitly retain multiple bounded record types.**

---

## 14. Consolidated findings

1. OLS 1.0 already exists as a complete released suite. The needed new layer is
   cross-repository extraction and navigation, not semantic reinvention.
2. The language's smallest stable base is fourteen universal concepts, ten
   declarations, ten primitive operators, seven profiles, four profile
   primitives, eleven products, and governed derivations.
3. The repository's richer scientific vocabulary is real and recurring, but
   most of it remains representation-, research-, or application-specific.
4. Reference Space is central conceptual architecture but is not a released
   OLS primitive. The repository currently supports a composite mapping rather
   than equivalence.
5. The hypothesis “OLS describes orientation; ORION processes orientation” is
   directionally correct. ORION's actual certified processing scope is narrower
   and must remain explicit.
6. LYRA is now best understood as a translation/explanation boundary, not the
   semantic Orientation Language.
7. No single Orientation Record exists across the ecosystem. A shared implicit
   anatomy is visible through identity, declarations, products, provenance,
   evidence, uncertainty, validation, authority, and immutable lineage.
8. NEXAHEDRON is the Human Workspace, not the language or engine. Applications
   realize domain use; the Library preserves editorial identity; the Human
   retains meaning and decision.
9. JSON, RDF, property graphs, knowledge graphs, DSLs, glTF, and Markdown may
   carry or realize parts of OLS. None is equivalent to OLS, and none supplies
   its evidence, authority, provenance, or transition boundaries automatically.
10. The main future work is not vocabulary invention. It is conformance
    mapping, carrier specification, cross-repository identifiers, examples,
    diagrams, and authority-preserving documentation.

## Canonical extraction statement

> Orientation Language describes how situated understanding is formed and
> communicated from declared observations, representations, comparisons,
> evidence, provenance, perspective, context, and uncertainty. It preserves
> the differences among seeing, representing, relating, orienting, explaining,
> selecting, transforming, validating, recording, approving, acting, and
> learning. Implementations may realize these responsibilities; applications
> may bind them to domains; ORION may process its certified subset;
> NEXAHEDRON may present them; the Library may communicate them. None acquires
> another layer's authority merely by participating in the same orientation.
