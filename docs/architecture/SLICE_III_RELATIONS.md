# Vertical Slice III — Relations Architecture

Status: Canonical architecture
Implementation status: Not started
Input boundary: Certified Vertical Slice II artifacts
Output boundary: Immutable Structural Relation Set; accepted only after External Relation Conformance

## 1. Purpose

Relations makes the structure declared by Vertical Slice II traversable without
interpreting source content.

It answers only:

> Which connections are exactly reproducible from accepted structural
> declarations?

Relations does not determine meaning, relevance, importance, similarity,
causality, Evidence, or a preferred route.

## 2. Position after Slice II

Relations begins after the certified Slice II STOP.

It consumes exact references to:

- one immutable Declared Source Element Inventory;
- its deterministic Structural Summary;
- its deterministic Structural Statistics;
- the immutable Structural Representation and source lineage preserved by
  those artifacts.

Summary and Statistics are completion and lineage gates. Relation derivation
uses only fields already declared by the Inventory or an accepted immutable
relation declaration. It does not reinterpret Summary or Statistics.

No Slice II artifact is changed, reopened, or enriched.

## 3. Relation classes

Slice III distinguishes three classes.

### 3.1 Structural relations

A structural relation is deterministically derived from exact immutable
structural fields.

Its complete basis must be present in the accepted Inventory. The derivation is
mechanical and byte-reproducible. It is not semantic inference.

### 3.2 Declared relations

A declared relation already exists in an accepted immutable declaration before
the Relations responsibility begins.

Relations may validate and preserve it. Relations does not create, repair,
complete, reinterpret, or translate it.

The Markdown Structural Representation Profile v1 declares no cross-references
or hierarchy. Its accepted declared-relation input is therefore empty.

Future Representation profiles may supply declared relations without changing
the Slice III relation object, provided each declaration conforms externally
and resolves to accepted endpoints.

### 3.3 Inferred relations

An inferred relation depends on interpretation, heuristics, probability,
similarity, external knowledge, or an undeclared structural assumption.

Inferred relations are prohibited in Slice III.

This includes treating locator containment, locator overlap, source order,
element kind, indentation, or visual proximity as parenthood or meaning.

## 4. Canonical Slice III relation vocabulary

Slice III permits exactly these relation types:

| Relation type | Class | Direction | Exact basis |
|---|---|---|---|
| `immediately_precedes` | Structural | Directed | Consecutive canonical ordinals `n` and `n + 1` |
| `immediately_follows` | Structural | Directed | Exact inverse declaration for consecutive canonical ordinals |
| `source_reference` | Structural | Directed | Element `boundary_ref` and the exact immutable source-boundary identity |
| `same_element_kind` | Structural | Symmetric | Equal declared `element_kind` values |
| `same_heading_level` | Structural | Symmetric | Both endpoints declare a heading `level` with the same integer value |
| `declared_cross_reference` | Declared | As declared | One accepted immutable cross-reference declaration with two resolvable endpoints |

No synonym is a second relation type. Navigation actions named `next` and
`previous` consume `immediately_precedes` and `immediately_follows`; they do
not create additional edges.

### 4.1 Directed ordinal relations

For every adjacent pair in canonical Inventory order:

- one `immediately_precedes` relation points from ordinal `n` to `n + 1`;
- one `immediately_follows` relation points from ordinal `n + 1` to `n`.

No edge skips an ordinal. The final element has no `immediately_precedes`
target. The document root has no `immediately_follows` target.

### 4.2 Source references

Every declared element receives one `source_reference` relation to the exact
source-boundary reference preserved by the Inventory.

The source boundary is a reference endpoint, not a new source and not a copy
of source content.

### 4.3 Equal-kind relations

`same_element_kind` relates each unordered pair of distinct elements whose
declared kinds are exactly equal.

The canonical stored endpoint order is lower ordinal first, then element
identity as a tie breaker. The relation is traversable in both directions.

Equal kind does not imply equal meaning, role, parent, or importance.

### 4.4 Equal-heading-level relations

`same_heading_level` relates each unordered pair of distinct heading elements
whose declared integer levels are equal.

ATX and Setext headings may share this relation because the basis is only the
declared numeric level. No outline, section, parent, sibling, or topical
relation follows from it.

### 4.5 Declared cross-references

A `declared_cross_reference` exists only when:

- an accepted immutable input explicitly declares it;
- both endpoint identities resolve;
- direction is explicit;
- the declaration identity, version, integrity, and provenance are available;
- external relation conformance succeeds.

Absent declaration means absent relation. Slice III never discovers a
cross-reference from Markdown text, URLs, labels, or source parsing.

## 5. Prohibited relation types

Slice III must not emit:

- `contains`, `contained_by`, `parent`, `child`, or `sibling`;
- semantic similarity or conceptual connection;
- topical, causal, temporal, evidential, or argumentative relations;
- relevance, importance, confidence, ranking, or recommendation edges;
- entity, concept, claim, or knowledge-graph edges;
- a relation inferred from locator overlap, indentation, or canonical order
  beyond the two exact adjacency types;
- a relation derived from raw source text or external knowledge.

Hierarchy remains unavailable for the current profile.

## 6. Structural Relation Set

Relations produces one immutable Structural Relation Set.

Its envelope contains:

- relation-set identity, version, and integrity;
- relation vocabulary identity and version;
- exact Inventory reference and integrity;
- exact Summary and Statistics references;
- Orientation Object identity and version;
- Representation identity, version, and integrity;
- source identity, revision, integrity, and boundary;
- ordered endpoint registry;
- ordered relation declarations;
- declared lossiness;
- provenance;
- responsibility state;
- explicit STOP after Relations.

### 6.1 Endpoint registry

The registry contains:

- every Inventory element exactly once, in canonical ordinal order;
- one exact source-boundary reference endpoint.

Element endpoint entries preserve:

- element identity;
- element kind;
- canonical ordinal;
- locator;
- declared heading level when present.

No content or new structural property is added.

### 6.2 Relation declaration

Every relation declaration contains:

- deterministic relation identity;
- canonical relation ordinal;
- relation type;
- relation class: `structural` or `declared`;
- direction: `directed` or `symmetric`;
- source endpoint identity;
- target endpoint identity;
- exact derivation basis;
- input Inventory reference;
- Representation and source lineage;
- declaration provenance where applicable;
- relation integrity.

The derivation basis names the exact input fields and values. It never contains
an explanation or conclusion.

## 7. Deterministic identity and ordering

Relation identity is derived only from:

- relation vocabulary identity and version;
- Orientation Object identity and version;
- Representation identity and version;
- input Inventory integrity;
- relation type and class;
- canonical endpoint identities;
- direction;
- exact derivation basis;
- accepted declaration identity for declared relations.

The same immutable inputs produce the same relation identity.

Canonical relation ordering is:

1. relation-type order as listed in Section 4;
2. source endpoint canonical ordinal;
3. target endpoint canonical ordinal;
4. source endpoint identity;
5. target endpoint identity;
6. relation identity.

The source-boundary endpoint sorts after all element ordinals.

Unordered iteration, clocks, locale, randomness, UI state, and provider output
must not affect identity or order.

## 8. External relation conformance

Relation validation remains external to relation construction.

A conforming validator verifies:

- accepted vocabulary identity and version;
- exact input artifact identities and integrity;
- endpoint existence and uniqueness;
- relation-type-specific basis;
- direction;
- canonical symmetric endpoint order;
- canonical relation order and contiguous ordinals;
- deterministic identity and integrity replay;
- declaration provenance for declared relations;
- absence of duplicate relations;
- absence of prohibited hierarchy and semantic fields;
- empty declared-relation input remains empty.

Invalid relations are rejected as a set. There is no partial acceptance,
repair, completion, or fallback.

External Relation Conformance is a new validator instance for a Slice III
artifact. It does not change the certified Slice II Representation Conformance
responsibility or implementation.

## 9. Provenance

Every relation resolves through:

```text
Relation
    ↓
Relation basis
    ↓
Inventory entry or accepted relation declaration
    ↓
Immutable Structural Representation
    ↓
Confirmed source identity and revision
```

The relation set preserves references. It does not copy source content or
become source authority.

## 10. Explicit exclusions

Relations performs no:

- source parsing or retrieval;
- Projection or Rendering;
- Representation, Inventory, Summary, or Statistics modification;
- hierarchy reconstruction;
- semantic interpretation;
- Evidence processing;
- reasoning;
- ranking or recommendation;
- navigation;
- Orientation Map construction;
- LYRA or SIRIUS invocation;
- Runtime or Gateway behavior change.

## 11. Acceptance conditions

The Relations architecture is implementable only if:

- every emitted relation belongs to the exact Slice III vocabulary;
- every endpoint resolves to the immutable endpoint registry;
- every relation has an inspectable exact basis;
- structural relations independently recompute from Inventory fields;
- declared relations replay from accepted declarations without alteration;
- inferred relations remain impossible;
- identity, ordering, integrity, and serialization are deterministic;
- external conformance rejects missing, invented, or ambiguous relations;
- all Slice II artifacts remain byte-identical and unchanged.
