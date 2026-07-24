# ORION Capability Roadmap v1

- Status: canonical implementation roadmap
- Starting point: ORION Alpha Vertical Slice I
- Architecture status: frozen
- Scope: capability expansion within accepted responsibility boundaries
- Architecture impact: none

## 1. Purpose

This roadmap defines the implementation sequence from the proven Alpha
Vertical Slice toward a complete ORION Kernel.

It does not redesign the architecture. It assumes the following foundations
remain unchanged:

- The Language of Orientation;
- Representation Architecture;
- Structural Representation Architecture;
- Markdown Structural Representation Profile v1;
- Markdown Structural Projection Specification v1;
- the boundary between Projection, Renderer, Representation, Conformance and
  UNDERSTAND;
- Human, NEXAH, Library, ORION, LYRA and NEXAHEDRON authority boundaries.

Each implementation phase must preserve the engineering discipline established
by Vertical Slice I:

1. one bounded capability;
2. deterministic execution;
3. immutable outputs;
4. external conformance;
5. explicit stop boundaries;
6. no simulated downstream behavior;
7. reproducible proof before expansion.

## 2. Proven Baseline

The current executable baseline is:

```text
Human-confirmed Markdown
        ↓
Markdown Structural Projection
        ↓
Markdown Structural Renderer Alpha
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

The baseline supports:

- `document`;
- `atx_heading`;
- `paragraph`.

It already proves:

- deterministic Projection execution;
- deterministic Rendering;
- canonical locators;
- canonical ordinals;
- deterministic element identities;
- immutable Structural Representation;
- external replay and conformance;
- renderer-free, parser-free UNDERSTAND inventory.

All later work builds on this baseline. No phase may reopen it merely to make a
later capability easier to implement.

## 3. Phase 1 — Complete CommonMark Block Support

### Goal

Implement the complete block-level vocabulary already defined by Markdown
Structural Representation Profile v1.

Phase 1 expands capability only. It does not change:

- the accepted CommonMark `0.31.2` grammar;
- the whole-document source boundary;
- the locator model;
- identity inputs;
- depth-first pre-order;
- declared lossiness;
- the Projection/Renderer boundary;
- UNDERSTAND's inventory-only authority.

### Dependencies

- accepted Markdown Structural Representation Profile v1;
- accepted Markdown Structural Projection Specification v1;
- accepted Renderer Alpha;
- accepted external Conformance boundary;
- accepted Source Element Inventory Alpha;
- passing Vertical Slice I proof.

### 3.1 `block_quote`

#### Projection changes

- activate the frozen `block_quote` mapping rule;
- recognize exactly one mapped element for each CommonMark block quote
  container;
- preserve CommonMark container extent, including valid lazy continuation;
- retain no marker count, indentation or nesting property;
- retain the existing whole-source boundary reference.

#### Renderer changes

- execute the activated mapping rule;
- emit `block_quote` in canonical depth-first pre-order;
- generate identity from the existing canonical basis;
- make no parent-element or inferred hierarchy declaration.

#### Conformance additions

- verify one-to-one correspondence with CommonMark block quote containers;
- verify full-line locator boundaries;
- verify nested block quote order;
- verify that equal or overlapping locators do not create undeclared
  relationships;
- reject missing, duplicated or invented block quote declarations.

#### UNDERSTAND inventory additions

- accept `block_quote` as an already-declared element kind;
- preserve identity, locator, ordinal and boundary unchanged;
- create no containment or quotation meaning.

#### Required tests

- single block quote;
- multi-line block quote;
- empty block quote;
- nested block quote;
- lazy continuation;
- adjacent but separate block quotes;
- marker-like text that remains a paragraph;
- deterministic rejection for unsupported ambiguity.

#### Proof requirements

- one immutable Representation containing `block_quote`;
- byte-identical repeated Rendering;
- external conformance success;
- byte-identical UNDERSTAND inventory;
- explicit proof that UNDERSTAND receives no Markdown and creates no hierarchy.

### 3.2 `ordered_list`

#### Projection changes

- activate the frozen `ordered_list` mapping rule;
- preserve each CommonMark ordered list container as one element;
- let CommonMark `0.31.2` determine list boundaries;
- omit starting number, delimiter, marker width and tightness as already
  declared.

#### Renderer changes

- emit each ordered list before its declared item descendants;
- retain canonical source order and whole-line locator extent;
- add no list numbering or presentation metadata.

#### Conformance additions

- verify one declaration per CommonMark ordered list container;
- verify separation when CommonMark establishes separate list containers;
- verify canonical placement before descendant items;
- verify that omitted list details remain absent.

#### UNDERSTAND inventory additions

- accept and preserve `ordered_list`;
- retain its identity, locator, ordinal and boundary;
- attach no sequence meaning beyond the declared structural kind and order.

#### Required tests

- one ordered item;
- multiple ordered items;
- non-default starting number;
- delimiter changes;
- list interruption boundaries;
- nested ordered lists;
- ordered list inside a block quote;
- numeral-like paragraph text.

#### Proof requirements

- deterministic Representation and inventory containing an ordered list;
- stable identities across identical replay;
- conformance proof for list boundaries and ordering;
- explicit absence of inferred numbering semantics.

### 3.3 `unordered_list`

#### Projection changes

- activate the frozen `unordered_list` mapping rule;
- preserve each CommonMark bullet list container as one element;
- rely only on CommonMark list-boundary rules;
- omit bullet character, marker width and tightness.

#### Renderer changes

- emit each unordered list before its declared item descendants;
- preserve canonical order and locator extent;
- introduce no task-list or checklist interpretation.

#### Conformance additions

- verify one declaration per CommonMark bullet list container;
- verify container separation across marker changes where required by the
  grammar;
- verify canonical ordering with nested structures;
- reject task or extension semantics.

#### UNDERSTAND inventory additions

- accept and preserve `unordered_list`;
- create no task state, priority or grouping interpretation.

#### Required tests

- each CommonMark bullet marker;
- multiple items;
- marker changes;
- nested unordered lists;
- unordered list inside an ordered item;
- empty item;
- task-like text preserved only as inline source content;
- bullet-like paragraph text.

#### Proof requirements

- deterministic Representation and inventory containing an unordered list;
- external conformance of boundaries and order;
- explicit proof that no task semantics were introduced.

### 3.4 `list_item`

#### Projection changes

- activate the frozen `list_item` mapping rule;
- map every CommonMark list item exactly once;
- preserve item source extent;
- omit item number, marker, indentation width and task-like inline content.

#### Renderer changes

- emit each item after its list container and before its own block descendants;
- preserve canonical ordinal and locator;
- emit no parent-list reference.

#### Conformance additions

- verify one declaration per CommonMark list item;
- verify canonical pre-order for items and descendants;
- verify empty-item handling;
- verify that no item-to-list edge is emitted.

#### UNDERSTAND inventory additions

- accept and preserve `list_item`;
- inventory only the declaration;
- do not reconstruct item membership or nesting.

#### Required tests

- ordered item;
- unordered item;
- empty item;
- item with paragraph;
- item with multiple blocks;
- nested list item;
- continuation indentation;
- adjacent independent lists.

#### Proof requirements

- deterministic list and item declaration sequence;
- stable identity and locator preservation through UNDERSTAND;
- explicit proof that containment is not reconstructed.

### 3.5 `thematic_break`

#### Projection changes

- activate the frozen `thematic_break` mapping rule;
- apply CommonMark precedence against list markers and Setext headings;
- preserve the recognized block as a single-line structural element;
- omit marker character, count and spacing.

#### Renderer changes

- emit one element for each recognized thematic break;
- preserve its full-line locator and canonical ordinal;
- assign no section or transition meaning.

#### Conformance additions

- verify grammar precedence;
- verify exact single-line locator;
- reject conversion between thematic break, list and heading kinds;
- verify omission of delimiter details.

#### UNDERSTAND inventory additions

- accept and preserve `thematic_break`;
- do not interpret it as a conceptual boundary.

#### Required tests

- asterisk, hyphen and underscore forms;
- permitted spacing;
- Setext-heading precedence;
- list-marker precedence;
- marker-like paragraph text;
- thematic break inside supported containers.

#### Proof requirements

- byte-identical declaration and inventory;
- conformance proof for each permitted syntax family;
- explicit absence of inferred section semantics.

### 3.6 `fenced_code_block`

#### Projection changes

- activate the frozen `fenced_code_block` mapping rule;
- preserve opening-to-closing extent under CommonMark;
- preserve opening-to-end-of-document extent for a valid unclosed fence;
- omit fence character, length, info string and code content.

#### Renderer changes

- emit one element per CommonMark fenced code block;
- preserve full-line locator and canonical ordinal;
- perform no syntax highlighting or language classification.

#### Conformance additions

- verify opening and closing extent;
- verify valid unclosed-fence behavior;
- verify fence precedence and container placement;
- verify absence of content, info-string and language metadata.

#### UNDERSTAND inventory additions

- accept and preserve `fenced_code_block`;
- do not inspect code content or infer programming language.

#### Required tests

- backtick fence;
- tilde fence;
- varying valid fence lengths;
- matching and non-matching closing fences;
- unclosed fence;
- info string;
- fence inside a block quote or list item;
- fence-like paragraph content.

#### Proof requirements

- deterministic closed- and unclosed-fence Representations;
- external conformance of locators and omissions;
- renderer-free UNDERSTAND inventory proof.

### 3.7 `indented_code_block`

#### Projection changes

- activate the frozen `indented_code_block` mapping rule;
- apply CommonMark indentation and continuation rules;
- preserve the assigned physical-line extent;
- omit indentation width, blank-line detail and code content.

#### Renderer changes

- emit one element per CommonMark indented code block;
- preserve canonical locator and ordinal;
- perform no content inspection.

#### Conformance additions

- verify CommonMark paragraph and container precedence;
- verify tab and space indentation behavior;
- verify assigned internal blank lines;
- verify that indentation details and content remain absent.

#### UNDERSTAND inventory additions

- accept and preserve `indented_code_block`;
- do not inspect content or infer language.

#### Required tests

- four-space indentation;
- tab-equivalent indentation;
- multiple lines;
- internal blank lines;
- indentation following a paragraph;
- indentation inside list items;
- distinction from fenced code;
- ordinary indented continuation that is not a code block.

#### Proof requirements

- deterministic space- and tab-based examples;
- exact byte-locator verification;
- external conformance and inventory replay;
- explicit no-content-access proof.

### 3.8 Remaining CommonMark block constructs

The remaining profile-defined block capability is:

- `setext_heading`.

CommonMark constructs intentionally omitted by the frozen profile do not become
new elements:

- blank lines;
- link reference definitions;
- inline constructs.

Raw HTML blocks remain deterministic source-domain failures. They are not a
missing capability under Profile v1.

#### Projection changes

- activate `setext_heading`;
- preserve `level = 1` for the `=` form and `level = 2` for the `-` form;
- apply CommonMark precedence with paragraphs and thematic breaks;
- retain the complete content-to-underline physical-line extent.

#### Renderer changes

- emit `setext_heading` with its required level;
- preserve locator, ordinal and deterministic identity;
- do not emit underline length, indentation or inline content.

#### Conformance additions

- verify both valid levels;
- verify paragraph promotion and thematic-break precedence;
- verify complete multi-line heading extent;
- verify that omitted CommonMark constructs do not receive declarations;
- verify deterministic HTML-block rejection.

#### UNDERSTAND inventory additions

- accept and preserve `setext_heading` and level;
- do not equate ATX and Setext syntax;
- do not infer conceptual importance from heading level.

#### Required tests

- level-one and level-two Setext headings;
- multi-line heading content;
- thematic-break ambiguity;
- link reference definitions with and without a remaining paragraph;
- blank lines;
- empty document;
- front-matter-like CommonMark text;
- raw HTML deterministic failure;
- extension-like syntax interpreted only as CommonMark.

#### Proof requirements

- one complete block-vocabulary Representation;
- external conformance across every profile-defined block kind;
- byte-identical complete UNDERSTAND inventory;
- negative proofs for raw HTML, unknown extensions and partial declarations.

### Phase 1 Deliverables

- complete deterministic execution of the frozen block Projection;
- Renderer support for every Profile v1 block element;
- complete block conformance matrix;
- UNDERSTAND inventory acceptance for every declared element kind;
- canonical fixture corpus covering valid, boundary and failure cases;
- one reproducible complete-block Vertical Slice proof.

### Phase 1 Acceptance Criteria

Phase 1 is complete when:

- every Profile v1 block kind maps exactly once when present;
- all identical accepted inputs produce byte-identical Representations;
- all identities, locators and ordinals pass external replay;
- UNDERSTAND preserves every declaration without source access;
- raw HTML and unsupported profiles still fail deterministically;
- no inline, semantic, Evidence or hierarchy capability has appeared;
- all existing Vertical Slice I proofs remain unchanged and green.

### Phase 1 Explicit Non-goals

- inline structure;
- GFM or other Markdown extensions;
- raw HTML support;
- parent-element hierarchy;
- semantic interpretation;
- Evidence;
- relations;
- summaries;
- Runtime or Gateway integration;
- LYRA.

## 4. Phase 2 — UNDERSTAND Expansion

### Goal

Extend UNDERSTAND from exact element inventory to deterministic structural
orientation over already-declared Representation data.

Phase 2 must remain source-free. UNDERSTAND continues to receive immutable,
externally conformant Representations and inventories. It does not parse
Markdown or create missing structure.

### Dependencies

- completed Phase 1;
- complete block-vocabulary conformance;
- immutable Source Element Inventory;
- stable canonical ordering, locators and identities;
- explicit approval for each bounded UNDERSTAND responsibility.

### 4.1 Structural Summary

Produce a deterministic structural synopsis from inventory fields only.

The summary may state:

- declared element count;
- ordered sequence of declared kinds;
- declared heading levels;
- source-boundary coverage;
- locations of declared structural units.

It must not summarize source content or infer subject matter.

### 4.2 Structural Statistics

Produce deterministic measurements such as:

- count by declared element kind;
- heading-level distribution;
- number of declared containers and leaf blocks;
- byte and line coverage from locators;
- first and last declared ordinals;
- repeated-kind frequency.

Every statistic must be reproducible from the accepted inventory alone.

### 4.3 Declared Relations

Inventory relations only when they already exist explicitly in an accepted
Representation or accepted relation declaration.

For the current profile:

- no parent-element hierarchy is declared;
- locator overlap is not a declared relation;
- apparent nesting must not be reconstructed;
- an empty declared-relation set is valid.

Phase 2 provides consumption and preservation of declared relations. It does
not create the first relation rules; that responsibility belongs to Phase 3.

### 4.4 Navigation Primitives

Provide deterministic navigation over declared inventory:

- address element by exact identity;
- address element by canonical ordinal;
- move to previous or next ordinal;
- retrieve a declared locator;
- select an inclusive ordinal range;
- return to the document root.

Navigation does not interpret content or choose a route for the Human.

### Deliverables

- immutable Structural Summary diagnostic;
- immutable Structural Statistics diagnostic;
- declared-relation inventory capable of preserving an empty set;
- deterministic identity-, ordinal- and locator-based navigation primitives;
- focused proofs for each responsibility;
- negative tests preventing raw-source and Renderer access.

### Acceptance Criteria

Phase 2 is complete when:

- all outputs derive only from accepted inventory fields;
- repeated execution is byte-identical;
- no output contains source text, concepts, claims or Evidence;
- navigation never changes canonical order;
- empty relation input remains empty;
- each responsibility has an explicit stop boundary;
- Phase 1 outputs remain unchanged.

### Explicit Non-goals

- source parsing;
- content summaries;
- hierarchy reconstruction;
- relation creation;
- semantic labels;
- relevance or ranking;
- concepts, claims or Evidence;
- LYRA language generation;
- user-specific route selection.

## 5. Phase 3 — Relation Layer

### Goal

Implement the first deterministic structural relations from explicit,
externally conformant structural values without semantic interpretation.

The Relation Layer makes reproducible structural connections available while
preserving endpoint identity, source lineage and relation basis.

### Dependencies

- completed Phase 2;
- stable element identities and canonical ordinals;
- accepted inventory navigation;
- an explicit bounded relation vocabulary reviewed against existing
  architecture;
- external conformance rules for relation outputs.

### Initial Structural Relations

The first relation capabilities should be limited to values directly provable
from declarations:

- immediate ordinal predecessor;
- immediate ordinal successor;
- shared accepted source boundary;
- equal declared element kind;
- equal declared heading level where both endpoints explicitly carry a level.

Every relation must identify:

- relation identity;
- exact endpoint element identities;
- direction where applicable;
- the declared fields that form its basis;
- Representation identity and version;
- source identity and revision;
- deterministic relation order;
- provenance and integrity.

The following are not valid first structural relations:

- inferred parent or child;
- conceptual similarity;
- topical connection;
- causal relation;
- evidential support;
- importance;
- relevance;
- confidence.

Locator containment or overlap must not be promoted to hierarchy because the
frozen Markdown profile explicitly does not declare that relationship.

### Deliverables

- one bounded deterministic structural relation vocabulary;
- immutable relation declarations;
- deterministic relation identities and ordering;
- external relation conformance;
- UNDERSTAND relation inventory;
- proofs for relation creation and preservation;
- negative tests for hierarchy and semantic inference.

### Acceptance Criteria

Phase 3 is complete when:

- every relation is reproducible from explicit declared fields;
- every endpoint resolves to an immutable declared element;
- no relation changes endpoint or source identity;
- relation basis remains inspectable;
- repeated execution is byte-identical;
- external conformance rejects invented or unresolved endpoints;
- no semantic or evidential relationship is emitted;
- existing Representations remain unchanged.

### Explicit Non-goals

- parent-element hierarchy;
- semantic similarity;
- causal or evidential relations;
- entity and concept graphs;
- ranking;
- graph traversal based on inferred edges;
- Atlas mutation;
- reports;
- reasoning;
- provider integration.

## 6. Phase 4 — Semantic Layer

### Status

**Future. Explicitly out of scope for the current ORION Kernel.**

No Phase 4 implementation is authorized by this roadmap.

### Goal

Record the future capability boundary that may eventually address meaning after
the deterministic structural kernel has been completed, evaluated and frozen.

### Dependencies

Any future semantic work requires:

- completed and stable Phases 1 through 3;
- separate architecture and governance review;
- explicit authority definitions;
- explicit contracts for semantic proposals and validation;
- clear Evidence and Library participation;
- evaluation demonstrating that the work cannot remain structural;
- a new implementation authorization.

### Future capability areas

- entities;
- concepts;
- claims;
- Evidence;
- reasoning.

These capabilities must remain distinct:

- an entity is not automatically a concept;
- a concept is not automatically a claim;
- a claim is not automatically Evidence;
- Evidence does not automatically establish truth;
- reasoning output does not automatically acquire authority.

### Deliverables

No current deliverable.

Possible future deliverables may be defined only after governance reopens this
scope.

### Acceptance Criteria

No current acceptance criteria.

Before future implementation begins, an approved specification must define:

- ownership;
- inputs;
- outputs;
- authority;
- uncertainty;
- validation;
- provenance;
- failure;
- compatibility with frozen structural capabilities.

### Explicit Non-goals

For the current kernel, all Phase 4 capabilities are non-goals:

- entity recognition;
- concept extraction;
- claim extraction;
- Evidence creation or binding;
- semantic graphs;
- semantic search;
- inference;
- model or provider reasoning;
- confidence generation.

## 7. Phase 5 — LYRA Integration

### Goal

Make validated structural summaries and relations available through faithful,
Human-oriented language and visual outputs without changing ORION
responsibilities.

LYRA consumes accepted outputs. It does not:

- execute Projection or Rendering;
- inspect undeclared source material;
- create structural relations;
- alter ORION results;
- choose Human meaning;
- perform semantic reasoning.

Phase 5 is a structural-output integration track. It does not depend on
implementing the future Semantic Layer.

### Dependencies

- completed Phases 1 through 3;
- externally conformant structural summaries, statistics and relations;
- stable provenance and uncertainty fields;
- accepted LYRA language boundary;
- presentation mappings that preserve ORION identity and ordering;
- explicit accessibility and visual fidelity criteria.

### Deliverables

- faithful language projection of structural summaries;
- faithful language projection of structural statistics;
- faithful explanation of declared relation endpoints and basis;
- accessible ordered outlines;
- locator-aware source navigation labels;
- restrained structural diagrams derived only from validated relations;
- trace-back from every language or visual unit to the ORION output it
  expresses;
- negative tests preventing LYRA from adding findings or changing order.

### Acceptance Criteria

Phase 5 is complete when:

- every expressed statement traces to a validated ORION field;
- element and relation identities remain available;
- declared order and uncertainty are preserved;
- an omitted or empty value remains visibly omitted or empty;
- language and visual outputs add no structural or semantic claim;
- identical accepted input produces the configured faithful output
  deterministically where the LYRA profile requires determinism;
- ORION code, contracts and ownership remain unchanged;
- Human interpretation and decision remain outside LYRA.

### Explicit Non-goals

- semantic interpretation;
- persuasive rewriting;
- hidden prioritization;
- automatic instrument selection;
- Human-intention inference;
- report invention;
- Evidence creation;
- Runtime behavior changes;
- provider-specific authority;
- replacing source material with explanation.

## 8. Cross-phase Verification Rules

Every capability milestone must include:

### Determinism

- identical immutable inputs produce identical outputs;
- canonical bytes are reproducible;
- identity inputs remain explicit;
- ordering is stable.

### Traceability

- Orientation Object identity survives;
- Representation identity survives;
- source identity and revision survive;
- every derived item points to its declared basis.

### Boundary protection

- Projection defines;
- Renderer executes;
- Representation preserves;
- Conformance validates;
- UNDERSTAND consumes and derives only within its approved responsibility;
- LYRA expresses accepted outputs faithfully;
- the Human retains meaning and decisions.

### Negative proof

Tests must prove not only what occurred, but what did not occur:

- no hidden parsing;
- no source repair;
- no Renderer invocation inside UNDERSTAND;
- no semantic inference in structural phases;
- no Evidence creation;
- no Runtime or Gateway responsibility drift;
- no public-contract mutation.

### Regression

Every completed proof remains executable. A new capability is not accepted when
it invalidates a previously frozen proof.

## 9. Status Dashboard

| Status | Capability |
|---|---|
| **Completed** | The Language of Orientation |
| **Completed** | Representation Architecture |
| **Completed** | Structural Representation Architecture |
| **Completed** | Markdown Structural Representation Profile v1 |
| **Completed** | Markdown Structural Projection Specification v1 |
| **Completed** | Markdown Structural Renderer Alpha: `document`, `atx_heading`, `paragraph` |
| **Completed** | External Conformance Alpha |
| **Completed** | UNDERSTAND Source Element Inventory Alpha |
| **Completed** | ORION Alpha Vertical Slice I |
| **In Progress** | None. No capability implementation begins through publication of this roadmap alone. |
| **Planned** | Phase 1 — Complete CommonMark block support |
| **Planned** | Phase 2 — UNDERSTAND Expansion |
| **Planned** | Phase 3 — deterministic structural Relation Layer |
| **Planned** | Phase 5 — structural LYRA Integration after its dependencies |
| **Future** | Phase 4 — Semantic Layer: entities, concepts, claims, Evidence and reasoning |

## 10. Roadmap Completion Statement

The roadmap is complete when it makes the next implementation responsibility
unambiguous without changing the frozen architecture.

Capability should expand in this order:

```text
Complete declared structure
        ↓
Orient over declared structure
        ↓
Establish deterministic structural relations
        ↓
Express validated structure faithfully
```

Semantic work remains a separately governed future boundary.

The ORION Kernel advances by adding one proven responsibility at a time. The
architecture remains stable while capability grows.
