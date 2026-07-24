# ORION Structural Representation Architecture

- Status: canonical architectural specialization
- Scope: structural Projection, deterministic structural Rendering and
  immutable Structural Representations
- Implementation status: pending
- Public contract impact: none
- Runtime impact: none
- Gateway impact: none
- UNDERSTAND impact: none

## 1. Relationship to the Representation Architecture

Structural Representation is an additive specialization of the existing
[`ORION Representation & Rendering Architecture`](REPRESENTATION_ARCHITECTURE.md).
It introduces no new architectural layer and no second authority.

The existing architecture already permits one Orientation Object to have many
immutable Representations in distinct target domains:

```text
Versioned Orientation Object
        │
        ├── Exact-Text Projection
        │       ↓
        │   Exact-Text Renderer
        │       ↓
        │   Exact-Text Representation
        │
        ├── Structural Projection
        │       ↓
        │   Structural Renderer
        │       ↓
        │   Structural Representation
        │
        └── Future Projection
                ↓
            Future Renderer
                ↓
            Future Representation Profile
```

Structural Representation is therefore:

- an ordinary Representation profile category;
- a target of an explicit, versioned Projection;
- an immutable output of a deterministic Renderer.

It is not:

- a new canonical concept beside Representation;
- a Runtime result;
- a Gateway model;
- an UNDERSTAND object;
- a Library authority;
- an Evidence object;
- a public contract.

The existing Representation Architecture requires no extension. This
specialization defines the bounded structural characteristics that future
format-specific Representation profiles must share.

## 2. Purpose

A Structural Representation provides an immutable, deterministic and
provenance-bound declaration of source structure.

Its purpose is to make already-projected structural units available for later
inventory without requiring the consumer to reopen or parse the source.

It exists to declare:

- which structural units a named Projection preserves;
- where those units occur within an accepted source boundary;
- in which declared order they occur;
- how their identity remains stable for the exact source and Projection
  versions;
- what structural information the Projection omits.

It does not exist to determine:

- what the source means;
- which units are important;
- which claims are true;
- which material is Evidence;
- which concepts or entities occur;
- how a Human should interpret the source.

Structural authority remains narrower than semantic, editorial, Evidence or
Human authority.

## 3. Ownership

Ownership remains distributed across the existing boundaries.

| Responsibility | Owner | Explicit exclusion |
|---|---|---|
| Orientation Object identity, version and originating authority | existing source authority | Renderer does not acquire source authority |
| Structural mapping rules | Structural Projection inside the ORION Representation Boundary | no execution or semantic interpretation |
| Deterministic mapping execution | Structural Renderer inside the ORION Representation Boundary | no reasoning, retrieval or validation |
| Immutable structural declaration | Structural Representation inside the ORION Representation Boundary | no source mutation or semantic authority |
| Replay, integrity and conformance checks | external Representation Conformance boundary | no repair or canonical reinterpretation |
| Inventory of an accepted declaration | UNDERSTAND | no parsing, discovery, creation or repair |

Runtime may coordinate later execution, but it does not own structural rules or
declarations. Gateway may transport references or accepted public objects, but
it does not construct structure. LYRA may faithfully explain an already
published output, but it does not project or render structure.

## 4. Structural Projection

A Structural Projection is the explicit, versioned mapping rule from one
accepted source domain into one structural target domain.

Every format-specific Structural Projection must declare:

- its accepted source domain;
- the accepted source grammar or format version;
- the target structural domain and profile;
- the accepted source-boundary model;
- the syntactic units it preserves;
- the ordering rule;
- the source-locator rule;
- the deterministic element-identity rule;
- preservation guarantees;
- omissions, normalization and declared lossiness;
- deterministic failure conditions.

The Projection defines the mapping. It does not execute it.

### 4.1 What it preserves

At minimum, the Projection preserves:

- Orientation Object identity and version;
- source identity and revision;
- the accepted source boundary;
- traceability from every declared element to that boundary;
- the source order defined by the profile;
- explicitly encoded structural distinctions covered by the profile.

### 4.2 What it may omit

A Projection may omit material outside its declared structural purpose, such
as:

- raw source content;
- presentation styling;
- non-structural whitespace;
- comments or metadata explicitly outside the profile;
- syntactic units the profile does not support.

Every omission must be visible through declared lossiness. An omission may
never be disguised as successful preservation.

### 4.3 What it may never change

A Structural Projection may never:

- change source identity or revision;
- mutate the source;
- invent structural units absent from its declared grammar;
- silently repair malformed input;
- assign conceptual or evidential meaning;
- classify importance or relevance;
- introduce external knowledge;
- choose content through semantic preference.

The word “structural” does not authorize interpretation.

## 5. Structural Renderer

A Structural Renderer is a read-only deterministic executor of one accepted
Structural Projection.

Given identical:

- source identity and revision;
- source content or structured source view;
- accepted boundary;
- Projection identity and version;
- Renderer identity and version;
- declared configuration;

the Renderer must produce the same Structural Representation.

### 5.1 Permitted deterministic operations

Subject to the exact format-specific Projection, a Renderer may:

- parse the declared source grammar;
- validate that input belongs to the declared source domain;
- recognize syntactic units defined by that grammar;
- calculate exact source locators;
- preserve or explicitly project declared source order;
- generate deterministic element identities;
- emit the immutable ordered structural declaration;
- record Renderer and Projection provenance;
- stop when deterministic conformance cannot be established.

Parsing is legitimate only when the source domain, grammar and parser behavior
are explicitly bounded by the Projection. Parsing authority does not imply
semantic authority.

### 5.2 Forbidden operations

A Structural Renderer must never:

- reason or infer;
- identify concepts or entities by meaning;
- summarize;
- classify topics, claims, relevance or importance;
- create or bind Evidence;
- rank structural units;
- retrieve additional sources;
- compare alternative interpretations;
- silently repair ambiguity;
- use model knowledge, provider behavior or hidden external state;
- create an Orientation Report or Continuation.

A Renderer that cannot apply its Projection deterministically must fail. It
must not emit a partially authoritative substitute.

## 6. Structural Representation

A Structural Representation is the immutable result of applying one Structural
Projection through one deterministic Structural Renderer.

It retains the existing Representation envelope:

- Orientation Object identity and version;
- source identity and revision;
- target domain and profile;
- Projection identity and version;
- Renderer identity and version;
- deterministic configuration identity where applicable;
- Representation identity and version;
- integrity;
- provenance;
- declared lossiness.

It additionally contains an ordered structural declaration. Architecturally,
each declared source element requires:

- a stable element identity;
- a syntactic element kind defined by the profile;
- a reference to the accepted parent source boundary;
- an exact source locator defined by the profile;
- a declared ordinal.

The first Structural Representation capability does not require:

- parent-element hierarchy;
- inferred relationships;
- semantic labels;
- concepts;
- claims;
- Evidence roles;
- relevance;
- confidence;
- summaries.

The complete ordered declaration is covered by the Representation identity and
integrity. It does not require a second standalone manifest authority.

### 6.1 Bounded authority

A conforming Structural Representation is authoritative only for this claim:

> For this exact source identity and revision, accepted boundary, Projection,
> Renderer version and declared configuration, this is the deterministic
> structural declaration produced by the named profile.

It is not authoritative for meaning, truth, Evidence, interpretation,
importance or Human decision.

## 7. Interaction with UNDERSTAND

Structural Representation must exist before UNDERSTAND begins structural
inventory.

```text
Versioned Source / Orientation Object
        ↓
Declared Structural Projection
        ↓
Deterministic Structural Renderer
        ↓
Immutable Structural Representation
        ↓
External Conformance
        ↓
Representation reference
        ↓
UNDERSTAND exact binding
        ↓
Declared Representation inventory
        ↓
Declared source-boundary inventory
        ↓
Source-element declaration check
        ↓
Declared source-element inventory
```

UNDERSTAND may receive:

- Structural Representation identity and version;
- source identity and revision;
- accepted source boundary;
- Projection and Renderer identity;
- ordered source-element declarations;
- stable element identities, kinds, locators and ordinals;
- provenance, integrity and declared lossiness.

For structural inventory, UNDERSTAND never receives:

- authority to execute a parser;
- unprojected source bytes;
- mutable structural candidates;
- hidden Renderer configuration;
- permission to create element identities;
- permission to normalize or repair declarations;
- inferred hierarchy or relationships;
- semantic labels or interpretations.

UNDERSTAND inventories the declaration. It does not reproduce the process that
created it.

## 8. Parallel Representations

Representations are complementary views of one preserved Orientation Object:

```text
Orientation Object O@V
        │
        ├── Exact-Text Representation
        ├── Structural Representation
        ├── Documentation Representation
        ├── Diagram Representation
        └── Machine Representation
```

No Representation supersedes another merely because it is more structured,
more readable or more detailed.

- Exact-Text preserves the accepted text.
- Structural Representation declares syntactic units and locators.
- Documentation Representation serves publication and reading.
- Diagram Representation serves a graphical target domain.
- Machine Representation serves an explicitly declared machine-readable target
  domain.

Each Representation has its own Projection, Renderer, integrity, provenance
and lossiness. All preserve the same source identity and version.

The frozen Exact-Text profile remains unchanged and continues to declare no
source elements.

## 9. Format-specific profiles

Future source formats fit inside the same architecture:

```text
Format-specific source
        ↓
Format-specific Structural Projection
        ↓
Format-specific Structural Renderer
        ↓
Ordinary Structural Representation
```

Markdown, PDF, HTML, XML, JSON, graphs, CAD objects and mathematical structures
do not require separate architecture branches. They require separate profiles
because their:

- grammars differ;
- element vocabularies differ;
- boundary and locator models differ;
- ordering rules differ;
- conformance conditions differ;
- preservation and lossiness differ.

A universal parser or universal source-element vocabulary is not part of this
architecture.

Graph nodes and edges may be declared structural units in a graph-specific
profile. Their existence and explicit connectivity may be structural; inferred
meaning or relevance remains semantic and therefore outside the Representation
Boundary.

## 10. Permanent invariants

1. Structural Representation is an ordinary Representation profile.
2. Structural Representation introduces no new architectural layer or
   authority.
3. Representation precedes UNDERSTAND.
4. UNDERSTAND inventories only already-declared immutable structure.
5. Structural discovery never occurs inside UNDERSTAND.
6. Projection defines the mapping; Renderer executes the mapping.
7. Every Projection and Renderer is explicit and versioned.
8. Renderer execution is deterministic and read-only.
9. Renderer execution performs no reasoning or semantic interpretation.
10. Structural Representation creates no subject-matter claims.
11. Source identity, source revision and accepted boundaries remain preserved.
12. Every declared element traces to an exact source locator.
13. Declared ordering is reproducible.
14. Provenance and declared lossiness survive every structural Projection.
15. Unknown formats, profiles and grammar versions fail deterministically.
16. Malformed or ambiguous input is never silently repaired.
17. Structural Representation never mutates or supersedes its source.
18. Multiple Representations preserve one Orientation Object without becoming
    interchangeable.
19. Conformance validation remains external to the Renderer.
20. Structural authority never becomes Evidence, editorial or semantic
    authority.
21. Runtime and Gateway do not create structural declarations.
22. LYRA does not perform Projection or Rendering.
23. The Exact-Text Representation remains frozen and unchanged.
24. No Structural Representation changes a Version 1 public contract.

## 11. Selection of the first profile

The first Version 1 Structural Representation profile should minimize
architectural ambiguity rather than maximize format coverage.

Selection criteria are:

1. **Explicit grammar** — structural units are defined by a public,
   version-addressable grammar.
2. **Deterministic parsing** — identical source bytes and grammar version yield
   identical structural units.
3. **Stable source locations** — elements can be traced to unambiguous source
   ranges or structural paths.
4. **Declared ordering** — the source format provides a reproducible order.
5. **Human inspectability** — a reviewer can compare source and declaration
   without specialized opaque tooling.
6. **Minimal normalization** — the Projection requires few implicit rewrite
   rules.
7. **Bounded failure behavior** — malformed or unsupported input can fail
   explicitly.
8. **Low implementation surface** — the profile proves the architecture
   without introducing layout analysis, retrieval or semantic interpretation.
9. **Reproducible conformance** — an independent implementation can replay and
   verify the declaration.
10. **No authority expansion** — the format does not require Library, Runtime,
    Gateway, Evidence or Human-meaning decisions.

Under these criteria, version-pinned CommonMark Markdown is the strongest
candidate for the first profile:

- its block grammar is explicit;
- source order is inherent;
- source locations can remain inspectable;
- headings, paragraphs, lists, quotations and code blocks are syntactically
  encoded;
- it avoids PDF layout interpretation and HTML browser behavior;
- it remains directly reviewable by a Human.

This recommendation does not define the profile. Before implementation, the
profile must still declare its exact accepted grammar version, element kinds,
locator model, identity rules, preservation, lossiness and failure behavior.

Plain text is not an acceptable substitute: line breaks alone do not constitute
an authoritative Structural Representation. The existing Exact-Text profile
must not be silently reinterpreted as Markdown.

## 12. Out of scope

This architecture does not define or implement:

- the first format-specific profile;
- parser selection or parser code;
- serialization or schemas;
- APIs, transport or persistence;
- Runtime or Gateway behavior;
- public-contract changes;
- UNDERSTAND changes;
- Source Element Inventory execution;
- semantic interpretation;
- concept or entity extraction;
- Evidence lookup, creation or binding;
- summarization or reasoning;
- hierarchy reconstruction;
- relevance or confidence;
- source retrieval or Library integration;
- LYRA or LUCY behavior;
- NTO, Atlas mutation or alternative Orientation Space geometry.

## 13. Acceptance criteria

This architecture is complete when an independent reviewer can verify that:

- Structural Representation fits entirely inside the existing Representation
  Architecture;
- it is an additive profile category rather than a new layer;
- every structural declaration originates from an explicit Projection and
  deterministic Renderer;
- no architectural authority has moved;
- Runtime and Gateway have acquired no structural responsibility;
- UNDERSTAND remains an inventory consumer and performs no discovery;
- Exact-Text remains frozen and declares no source elements;
- structural authority is limited to deterministic, traceable source
  structure;
- semantic, Evidence, editorial and Human authority remain outside the
  Representation Boundary;
- future format-specific profiles can be added without redesigning the
  architecture;
- a future Declared Source Element Inventory can consume a conforming
  Structural Representation without interpreting source content.

No implementation may begin until one format-specific profile has been reviewed
against these invariants.
