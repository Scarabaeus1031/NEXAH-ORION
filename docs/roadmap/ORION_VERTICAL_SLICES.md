# ORION Vertical Slices

- Status: canonical vertical-slice roadmap
- Architecture status: frozen
- Starting point: ORION Alpha Vertical Slice I
- Scope: executable capability progression through the accepted architecture
- Calendar schedule: none

```text
Reality
        ↓
Foundation
        ↓
Slice I — Representation and Inventory
        ↓
Slice II — Structure and Summary
        ↓
Slice III — Relations and Navigation
        ↓
Slice IV — Expression and Communication
        ↓
Slice V — Human Integration and Feedback
```

## 1. Definition of a Vertical Slice

An ORION vertical slice is a complete, executable path through the existing
architecture up to one explicitly bounded capability level.

A slice is not:

- an isolated feature;
- a collection of unrelated modules;
- a conceptual layer without execution;
- a roadmap phase that changes the architecture;
- a demonstration that bypasses normal responsibility boundaries;
- a partial implementation presented as a complete orientation.

A vertical slice proves that an orientation can travel through the system to a
defined level without violating responsibility boundaries.

### 1.1 Why a slice crosses responsibilities

Orientation is produced through bounded transitions. A useful proof must
therefore cross more than one component.

For example, an immutable Representation alone proves Rendering but not
consumption. An inventory alone proves data handling but not that its elements
originated from a confirmed source. A complete slice connects those
responsibilities while keeping their authority separate.

Every slice must identify:

- its exact starting artifact;
- each responsibility crossed;
- each immutable artifact produced;
- each validation boundary;
- its terminal capability;
- its explicit `STOP`.

### 1.2 Why every slice stops

A declared `STOP` makes the demonstrated capability unambiguous.

It shows:

- which responsibility completed;
- which downstream responsibility did not execute;
- which outputs are real;
- which outputs do not yet exist;
- where the next slice must begin.

Without a stop boundary, unimplemented behavior can be mistaken for simulated
or implicit behavior.

### 1.3 Why later slices extend earlier slices

A later slice carries the same orientation path farther. It does not replace
the path already proven.

Therefore:

- Slice II includes and preserves Slice I;
- Slice III includes and preserves Slices I and II;
- Slice IV consumes the validated result of Slice III;
- Slice V begins only after the outputs of Slice IV exist.

Earlier artifacts, identities, provenance and tests remain valid. A later slice
is not accepted if it reassigns an earlier responsibility.

### 1.4 Demonstrability

Every slice must be:

- executable;
- deterministic where its governing specification requires determinism;
- independently reviewable;
- reproducible from immutable inputs;
- externally verifiable;
- protected by positive and negative tests;
- explicit about unsupported and lossy cases.

Every proof must show both what occurred and what did not occur.

## 2. Current Foundation

The architectural Foundation is complete and frozen.

It consists of:

- The Language of Orientation;
- Representation Architecture;
- Structural Representation Architecture;
- Markdown Structural Representation Profile v1;
- Markdown Structural Projection Specification v1;
- Markdown Structural Renderer Alpha;
- External Conformance;
- UNDERSTAND Source Element Inventory Alpha;
- ORION Alpha Vertical Slice I.

The Foundation establishes:

- Projection as the definition of deterministic mapping;
- Rendering as execution of that mapping;
- Representation as an immutable, versioned and traceable artifact;
- Conformance as an external responsibility;
- provenance and integrity across the path;
- canonical element identities, locators and order;
- bounded UNDERSTAND consumption;
- explicit stop boundaries.

The Foundation is not a user-facing slice. It is the stable base that makes
every user-facing capability testable.

No later slice may reopen the Foundation merely to simplify implementation.
Any proposed change to a frozen responsibility requires separate governance
before it can enter this roadmap.

## 3. Slice I — Representation and Inventory

**Status: Completed**

### Canonical path

```text
Human-confirmed Markdown
        ↓
Projection
        ↓
Renderer
        ↓
Immutable Structural Representation
        ↓
External Conformance
        ↓
UNDERSTAND
        ↓
Declared Source Element Inventory
        ↓
STOP
```

### Current supported source elements

- `document`
- `atx_heading`
- `paragraph`

### Goal

Prove that a bounded source can become immutable, traceable and inspectable
structure.

The slice validates responsibilities rather than format completeness.

### Deliverables

- deterministic Projection execution;
- deterministic Rendering;
- immutable Structural Representation;
- external Conformance result;
- immutable declared Source Element Inventory;
- preserved Orientation Object identity;
- preserved source identity and revision;
- preserved provenance and integrity;
- preserved element identity, locator and canonical ordering;
- deterministic failure for unsupported block constructs;
- a reproducible end-to-end proof.

### Acceptance criteria

Slice I is complete because:

- repeated proof output is byte-identical;
- execution is deterministic;
- all outputs are immutable;
- unsupported constructs fail explicitly;
- the Representation remains externally conformant;
- UNDERSTAND receives no raw Markdown;
- UNDERSTAND executes neither Projection nor Renderer;
- UNDERSTAND creates no structure;
- no semantics or relations are introduced;
- the proof stops after declared Source Element Inventory.

### Explicit non-goals

- structural summary;
- structural statistics;
- navigation;
- structural relations;
- semantic interpretation;
- entities;
- concepts;
- claims;
- Evidence;
- reasoning;
- LYRA;
- SIRIUS;
- public application.

## 4. Slice II — Structure and Summary

**Status: Complete**

### Canonical path

```text
Human-confirmed Markdown
        ↓
Projection
        ↓
Renderer
        ↓
Immutable Structural Representation
        ↓
External Conformance
        ↓
UNDERSTAND
        ↓
Declared Source Element Inventory
        ↓
Structural Summary
        ↓
Structural Statistics
        ↓
STOP
```

### Goal

Extend Slice I so that complete declared block structure can be summarized and
measured without introducing relations, semantics or interpretation.

Structural Summary describes declared form. It does not summarize source
meaning.

Structural Statistics measures declared fields. It does not evaluate content.

### Dependencies

- completed and frozen Slice I;
- frozen Markdown Structural Representation Profile v1;
- frozen Markdown Structural Projection Specification v1;
- stable canonical locator, identity and ordering rules;
- accepted external Conformance boundary;
- accepted inventory-only UNDERSTAND boundary;
- a passing proof for every previously supported element.

### Required CommonMark capability sequence

Implement one bounded capability at a time:

1. `block_quote`
2. `ordered_list`
3. `unordered_list`
4. `list_item`
5. `thematic_break`
6. `fenced_code_block`
7. `indented_code_block`
8. remaining supported CommonMark block constructs

The remaining profile-defined block construct is `setext_heading`.

The following are not new elements under Profile v1:

- blank lines;
- link reference definitions;
- inline constructs.

Raw HTML blocks remain deterministic source-domain failures. Extension syntax
continues to receive only its CommonMark `0.31.2` interpretation.

### 4.1 Projection changes

For each newly activated block kind, Projection execution must:

- apply only the mapping already defined by the frozen Projection
  Specification;
- recognize every supported CommonMark block node exactly once;
- preserve the existing whole-document source boundary;
- derive full-physical-line locators by the existing rules;
- preserve depth-first pre-order;
- assign contiguous ordinals;
- provide the existing identity basis;
- preserve only the required element-specific property;
- apply the frozen declared lossiness;
- fail rather than invent, repair or approximate structure.

Capability-specific requirements include:

- `block_quote`: preserve each CommonMark block quote container and its extent;
- `ordered_list`: preserve each ordered list container;
- `unordered_list`: preserve each bullet list container;
- `list_item`: preserve each item in canonical container traversal;
- `thematic_break`: apply CommonMark precedence against lists and Setext
  headings;
- `fenced_code_block`: preserve opening-to-closing or valid opening-to-EOF
  extent;
- `indented_code_block`: apply CommonMark indentation and continuation rules;
- `setext_heading`: preserve `level` and the content-to-underline extent.

No Projection change may introduce:

- inline elements;
- parent-element references;
- inferred hierarchy;
- source content values;
- semantic fields.

### 4.2 Renderer changes

The Renderer must:

- execute each activated mapping without adding a structural decision;
- emit every new element in canonical order;
- generate identity from the unchanged canonical basis;
- preserve source, profile, Projection and Renderer lineage;
- include every new element in Representation integrity;
- remain read-only and deterministic;
- emit no partial Representation after a failure.

The Renderer must not:

- select content;
- normalize source;
- repair Markdown;
- infer structure not declared by Projection;
- add hierarchy or relations;
- inspect meaning.

### 4.3 Conformance additions

External Conformance must add, for every supported kind:

- one-to-one source-node-to-declaration verification;
- canonical locator replay;
- canonical ordinal replay;
- deterministic element-identity replay;
- nested-container ordering checks where CommonMark declares containers;
- omission checks for profile-declared lossiness;
- negative checks for unsupported and ambiguous forms;
- unchanged provenance and Representation integrity checks.

The complete Conformance matrix must cover:

- all supported block kinds;
- valid nesting combinations;
- empty containers where CommonMark permits them;
- valid unclosed fenced code blocks;
- tab and space indentation behavior;
- CommonMark precedence boundaries;
- empty documents;
- link reference definition omission;
- raw HTML rejection;
- extension-like input without extension semantics.

### 4.4 UNDERSTAND additions

UNDERSTAND must extend its accepted inventory vocabulary to every declared
Profile v1 block kind.

It must preserve:

- element identity;
- element kind;
- required heading level;
- locator;
- ordinal;
- source boundary;
- Representation and source lineage.

UNDERSTAND must continue to:

- receive only immutable Structural Representations;
- avoid raw Markdown;
- avoid Projection and Renderer execution;
- avoid structural discovery;
- avoid hierarchy reconstruction;
- avoid semantic interpretation.

### 4.5 Structural Summary

The first Structural Summary may contain only deterministic statements derived
from inventory fields:

- total declared element count;
- ordered list of declared element kinds;
- heading levels where explicitly declared;
- first and final canonical ordinal;
- source-boundary identifier;
- declared block-kind coverage.

It must not contain:

- source excerpts;
- topic summaries;
- importance;
- conclusions;
- inferred sections;
- inferred containment;
- relations.

### 4.6 Structural Statistics

The first Structural Statistics may contain:

- count by element kind;
- heading-level distribution;
- count of profile-declared container kinds;
- count of profile-declared leaf kinds;
- byte range covered by each declared locator;
- line range covered by each declared locator;
- document source-boundary coverage;
- ordered element count.

Nesting-depth statistics are available only where depth is explicitly declared
by an accepted Representation.

The current Markdown Structural Representation Profile v1 does not declare
parent-element hierarchy or depth. Therefore Slice II must report nesting depth
as unavailable rather than reconstructing it from:

- locator overlap;
- traversal order;
- CommonMark parsing;
- element-kind assumptions.

### 4.7 Test requirements

Each capability must include:

- valid single-element cases;
- multi-element cases;
- boundary cases;
- permitted nesting cases;
- precedence cases;
- UTF-8 byte-locator cases;
- immutable-output tests;
- byte-identical replay;
- tamper rejection;
- explicit unsupported-input failures;
- static and runtime tests preventing source access inside UNDERSTAND;
- static and runtime tests preventing Projection or Renderer calls inside
  UNDERSTAND;
- regression execution of all Slice I proofs.

Structural Summary and Statistics tests must prove that every value is
recomputable from inventory fields alone.

### 4.8 Proof requirements

Each new block kind requires one bounded proof:

```text
Confirmed source containing the new block kind
        ↓
Deterministic Representation
        ↓
External Conformance
        ↓
Immutable Inventory
        ↓
STOP
```

Slice II completion additionally requires one complete-vocabulary proof:

```text
Confirmed CommonMark document
        ↓
Complete Profile v1 block declaration
        ↓
External Conformance
        ↓
Complete immutable inventory
        ↓
Structural Summary
        ↓
Structural Statistics
        ↓
STOP
```

The proof must expose:

- input and artifact identities;
- provenance;
- element count and order;
- Summary basis;
- Statistics basis;
- byte-identical replay;
- explicit downstream non-execution.

### Acceptance criteria

Slice II is complete when:

- every Profile v1 block kind is supported;
- every supported block maps exactly once;
- identical inputs produce byte-identical Representations, inventories,
  summaries and statistics;
- external Conformance covers every block kind and failure boundary;
- summaries contain structure only;
- statistics derive only from declared fields;
- unavailable hierarchy remains unavailable;
- unsupported and lossy cases remain explicit;
- no relation is produced;
- no semantic interpretation occurs;
- every Slice I proof remains green;
- execution stops after Structural Statistics.

### Explicit non-goals

- inline structure;
- raw HTML support;
- GFM or other extensions;
- hierarchy reconstruction;
- structural relation creation;
- navigation;
- semantic interpretation;
- entity, concept or claim detection;
- Evidence;
- reasoning;
- LYRA;
- SIRIUS;
- public application.

## 5. Slice III — Relations and Navigation

**Status: Architecture and Engineering Plan Complete — Implementation Not Started**

Canonical architecture:

- [`Slice III Relations`](../architecture/SLICE_III_RELATIONS.md);
- [`Slice III Navigation`](../architecture/SLICE_III_NAVIGATION.md);
- [`Slice III Orientation Map`](../architecture/SLICE_III_ORIENTATION_MAP.md);
- [`Slice III Responsibility Matrix`](../architecture/SLICE_III_RESPONSIBILITY_MATRIX.md).

Canonical engineering plan:

- [`Slice III Engineering Plan`](SLICE_III_ENGINEERING_PLAN.md);
- [`Slice III Work Packages`](SLICE_III_WORK_PACKAGES.md);
- [`Slice III Certification Path`](SLICE_III_CERTIFICATION_PATH.md).

Implementation is decomposed into WP12–WP25. No work package or certification
gate has started.

### Canonical path

```text
Confirmed Markdown
        ↓
Projection
        ↓
Renderer
        ↓
Immutable Structural Representation
        ↓
Inventory
        ↓
Structural Summary
        ↓
Structural Statistics
        ↓
Certified Slice II STOP
        ↓
Structural Relations
        ↓
Navigation
        ↓
Orientation Map
        ↓
STOP
```

### Goal

Make declared structure navigable through deterministic relations.

Slice III remains structural. It introduces no entity, concept, claim,
Evidence or semantic interpretation.

### Dependencies

- completed and frozen Slices I and II;
- complete Profile v1 block support;
- externally conformant immutable inventories;
- stable Structural Summary and Statistics;
- the canonical closed relation vocabulary;
- deterministic relation identity and ordering rules;
- external Relation, Navigation and Map Conformance specifications;
- the canonical bounded Orientation Map architecture.

No implementation begins until every relation can identify its exact declared
basis without source parsing or semantic inference.

### 5.1 Structural relation boundary

Every relation must preserve:

- endpoint identity;
- relation type;
- derivation basis;
- source scope;
- Representation identity and version;
- source identity and revision;
- provenance;
- ordering where relevant;
- integrity.

A relation may be emitted only when its basis is explicit and reproducible.

The exact Slice III vocabulary is:

- `immediately_precedes`;
- `immediately_follows`;
- `source_reference`;
- `same_element_kind`;
- `same_heading_level`;
- `declared_cross_reference`, only when an accepted immutable input explicitly
  declares the reference.

The first five are deterministic structural relations. The sixth is preserved
declared input. Inferred relations are prohibited.

`next` and `previous` are Navigation actions over the two exact ordinal
relations. They are not additional relation types.

The frozen Markdown Structural Representation Profile v1 does not declare
parent-element hierarchy. Therefore these relations must not be reconstructed
from:

- locator containment;
- locator overlap;
- canonical order;
- element kind;
- reparsing Markdown.

If no accepted Representation explicitly declares hierarchy, hierarchical
relations and their navigation operations remain unavailable.

### 5.2 Navigation primitives

Navigation over currently declared fields may include:

- move to next canonical element;
- move to previous canonical element;
- return to the document root;
- resolve an exact element identity;
- resolve an exact canonical ordinal;
- resolve an exact locator;
- follow any traversable validated Slice III relation;
- inspect the exact source-boundary reference;
- follow an explicitly declared cross-reference;
- return to the navigation origin.

The following primitives become available only with explicit hierarchical
relations:

- enter container;
- leave container;
- move to parent;
- move to child.

Navigation does not choose what the Human should inspect. It provides
deterministic possible movement over accepted relations.

The immutable Navigation Object, canonical entry points, transition ordering,
availability states and blocker codes are defined by
[`SLICE_III_NAVIGATION.md`](../architecture/SLICE_III_NAVIGATION.md).

### 5.3 Orientation Map

The first Orientation Map is a bounded structural view containing:

- declared element nodes;
- validated structural relation edges;
- stable identities;
- source locators;
- canonical origin;
- available navigation transitions;
- provenance;
- visible unavailable or blocked transitions;
- an explicit `STOP`.

The map must not contain:

- inferred topics;
- conceptual clusters;
- evidential weight;
- semantic similarity;
- hidden ranking;
- suggested meaning.

The map remains an immutable derived view, not a storage layer. Its canonical
nodes, edges, transitions, serialization, provenance and lossiness are defined
by
[`SLICE_III_ORIENTATION_MAP.md`](../architecture/SLICE_III_ORIENTATION_MAP.md).

### Test requirements

- deterministic relation identity;
- endpoint resolution;
- direction preservation;
- canonical relation order;
- previous/next inverse checks;
- source-reference traceability;
- missing-endpoint rejection;
- undeclared-cross-reference rejection;
- unavailable hierarchy behavior;
- no locator-overlap hierarchy;
- no source parsing;
- immutable Orientation Map;
- byte-identical navigation proof;
- regression of all Slice I and II proofs.

### Proof requirements

The minimum Slice III proof is:

```text
Real confirmed source
        ↓
Externally conformant Structural Representation
        ↓
Immutable Inventory and Summary
        ↓
Validated Structural Relations
        ↓
Deterministic Navigation
        ↓
Immutable Orientation Map
        ↓
STOP
```

The proof must demonstrate:

- a real source can be represented;
- every mapped element remains traceable;
- relations use only declared bases;
- navigation preserves identities and direction;
- the map exposes provenance and stop boundaries;
- no semantic interpretation occurred.

### Acceptance criteria

Slice III is complete when:

- every relation is deterministic and externally conformant;
- every endpoint resolves to an accepted immutable element;
- every relation exposes its derivation basis;
- navigation is reproducible;
- unavailable hierarchical navigation remains visibly unavailable;
- the Orientation Map is immutable and source-traceable;
- no semantic or probabilistic edge exists;
- all earlier slice proofs remain green;
- the proof can traverse one real source deterministically through Navigation
  and construct its immutable Orientation Map;
- execution stops after the Orientation Map.

### Explicit exclusions

- inferred meaning;
- entity extraction;
- concept detection;
- claim detection;
- Evidence evaluation;
- semantic similarity;
- probabilistic relations;
- inferred hierarchy;
- content-based recommendations;
- reasoning;
- LYRA expression.

### Public resurfacing point

Completion of Slice III is the preferred resurfacing point for the first
interactive nexahedron.com implementation.

The minimum justification is concrete:

> A real source can be represented, inventoried, related and navigated through
> a visible orientation map.

Before this proof exists, a large interactive application would outpace the
kernel capability it is meant to expose.

## 6. Slice IV — Expression and Communication

**Status: Future**

### Canonical path

```text
Validated Structural Relations
        ↓
Orientation Map
        ↓
LYRA
        ↓
Faithful Human Expression
        ↓
STOP
```

### Goal

Turn validated orientation structures into communicable Human-facing forms.

Expression makes accepted ORION outputs readable and visible. It does not
change their identity, relation basis or authority.

### Dependencies

- completed and frozen Slices I through III;
- externally conformant Structural Relations;
- immutable Orientation Map;
- accepted LYRA boundary;
- explicit faithful-expression profiles;
- stable traceability from expression units to ORION outputs;
- accessible visual and language requirements.

### Deliverables

Possible faithful outputs include:

- explanations;
- maps;
- diagrams;
- readable navigation summaries;
- visual pathways;
- teaching views;
- comparison views.

Every output must preserve:

- source and Representation identity;
- element and relation identity;
- relation direction;
- declared order where relevant;
- uncertainty and unavailable paths;
- provenance;
- the distinction between validated structure and Human interpretation.

### Fidelity requirements

LYRA must not:

- invent source facts;
- modify structural identities;
- silently change relations;
- hide uncertainty;
- make decisions for the Human;
- become the authority over ORION outputs;
- add a relation absent from the Orientation Map;
- present an unavailable path as available.

Faithful expression may reorganize presentation only under an explicit
expression profile. Presentation changes do not alter ORION artifacts.

### Traceability requirements

Every language or visual unit must resolve to:

- one or more accepted ORION output identities;
- the relevant source scope;
- the expression profile used;
- any declared presentation lossiness.

An explanation that cannot be traced to validated structure is not a
conforming Slice IV output.

### Test strategy

- field-to-expression traceability;
- element-identity preservation;
- relation-direction preservation;
- uncertainty visibility;
- empty and unavailable-state fidelity;
- stable output under the configured profile;
- no additional findings or relations;
- accessible reading and navigation order;
- visual equivalence against the accepted Orientation Map;
- negative tests for hidden prioritization and unsupported claims;
- regression of all earlier slice proofs.

### Acceptance criteria

Slice IV is complete when:

- one externally conformant Orientation Map produces a faithful Human-facing
  explanation;
- one externally conformant Orientation Map produces a faithful visual view;
- every expression unit remains traceable;
- no identity or relation is changed;
- uncertainty and stop boundaries remain visible;
- the Human can return from expression to the validated structural basis;
- execution stops after faithful expression.

### Explicit non-goals

- semantic inference;
- new relations;
- Evidence evaluation;
- persuasion;
- hidden summarization priorities;
- Human decision-making;
- automatic action;
- SIRIUS mechanics;
- feedback-loop implementation.

## 7. Slice V — Human Integration and Feedback

**Status: Future / Research Boundary**

### Canonical path

```text
Validated Orientation
        ↓
LYRA Expression
        ↓
Human Review
        ↓
SIRIUS Integration Context
        ↓
Decision or Action
        ↓
Feedback
        ↓
New Observation
        ↓
STOP
```

### Goal

Close the recursive orientation loop without transferring Human authority to
software.

This slice is conceptually identified but lies beyond the current kernel
roadmap.

### Permanent Human boundary

- Humans retain interpretation authority.
- Humans retain acceptance authority.
- Humans retain decision authority.
- Software may prepare orientation but does not own meaning.
- Integration may produce action, rejection, revision or a new inquiry.
- Feedback may create a new Orientation Object and begin another cycle.

### SIRIUS boundary

This roadmap does not define, implement or freeze SIRIUS mechanics.

`SIRIUS Integration Context` names only the future position in the canonical
path where a reviewed expression may enter an integration context. Its
responsibilities, contracts, authority and execution remain subject to separate
future architectural definition.

No current implementation may infer those mechanics from this roadmap.

### Dependencies

Before Slice V can move beyond research:

- Slice IV must be complete and evaluated;
- Human review must remain explicit;
- SIRIUS must have an accepted architectural definition;
- action and feedback authority must be governed;
- privacy, consent and reversibility requirements must be defined;
- new-Observation and new-Orientation-Object lineage must be specified.

### Conceptual deliverables

No executable deliverable is currently authorized.

A future approved slice would need to demonstrate:

- explicit Human review;
- explicit Human acceptance or rejection;
- traceable decision context;
- bounded action handoff;
- feedback provenance;
- creation of a new observation without overwriting the previous cycle.

### Acceptance criteria

No current acceptance criteria are defined.

Future criteria must be approved only after SIRIUS and Human-integration
responsibilities are explicitly specified.

### Explicit non-goals

- current SIRIUS implementation;
- autonomous decisions;
- automatic action;
- silent feedback capture;
- Human-intention inference;
- replacement of Human judgment;
- current-kernel expansion into integration workflows.

## 8. Relationship to nexahedron.com

The public experience should resurface only capabilities that the kernel can
demonstrate honestly.

### Before Slice III

nexahedron.com may contain only:

- project introduction;
- the Orientation Grammar;
- architecture views;
- roadmap;
- static demonstrations;
- links to the repository and Library.

Static demonstrations must remain visibly static. They must not imply that
relations, navigation or live orientation already exist.

### At Slice III

Begin the first interactive implementation:

- source viewer;
- structural inventory;
- relation explorer;
- navigation path;
- Orientation Map;
- visible provenance;
- visible `STOP` boundaries.

The interface should expose validated kernel capability directly. It must not
simulate semantic understanding or LYRA output.

### After Slice IV

Add:

- Human-readable explanations;
- visual transformations;
- guided exploration;
- teaching views;
- comparison views.

Every presentation remains traceable to validated structural outputs.

### After Slice V

Only after explicit architectural definition, consider:

- integration workflows;
- feedback loops;
- action contexts.

No large platform build should begin before Slice III is complete.

## 9. Status Dashboard

| Level | Status | Meaning |
|---|---|---|
| **Foundation** | **Complete / Frozen** | Conceptual grammar, Representation boundaries, Markdown profile and Projection, Renderer Alpha, Conformance, Inventory and milestone proof exist. |
| **Slice I — Representation and Inventory** | **Complete** | The first complete executable architecture path stops at immutable Source Element Inventory. |
| **Slice II — Structure and Summary** | **Complete / Certified** | Complete Profile v1 structure, deterministic Summary and Statistics replay through the certified Slice II STOP. |
| **Slice III — Relations and Navigation** | **Architecture and Engineering Plan Complete / Implementation Not Started** | Canonical architecture, WP12–WP25, and four certification gates exist; no Slice III code or tests exist. |
| **Slice III public milestone** | **Planned** | First interactive nexahedron.com resurfacing. |
| **Slice IV — Expression and Communication** | **Future** | Add faithful LYRA language and visual expression after validated relations exist. |
| **Slice V — Human Integration and Feedback** | **Research boundary** | Requires explicit future SIRIUS and Human-integration architecture. |

## 10. Canonical Closing Statement

> A vertical slice is not a feature layer.
>
> It is a complete orientation path reaching one defined level of capability.
>
> Each new slice carries Reality farther through the same grammar while
> preserving the boundaries proven by every earlier slice.
