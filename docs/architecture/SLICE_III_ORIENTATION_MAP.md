# Vertical Slice III — Orientation Map Architecture

Status: Canonical architecture
Implementation status: Not started
Input boundary: Externally conformant immutable Navigation Object
Output boundary: Immutable Orientation Map; accepted only after External Map Conformance → STOP

## 1. Purpose

The Orientation Map is the first complete derived view of declared structure,
validated relations, and available navigation.

It answers:

> What structural positions exist, how are they explicitly connected, and
> which movements are available or unavailable?

The map is not a knowledge graph, semantic model, source repository, analysis
result, route recommendation, or visual layout.

## 2. Derived-view principle

The Orientation Map is a deterministic projection of one accepted Navigation
Object and the immutable relation catalog preserved within it.

It:

- copies stable node and relation references;
- exposes navigation transitions;
- preserves origin, direction, ordering, provenance, and boundaries;
- shows unavailable transitions where the absence is architecturally
  meaningful.

It does not own or persist source material, Relations, Navigation, or Human
state.

If the input Navigation Object changes, a new Orientation Map is created with
a new identity and version. An existing map is never updated in place.

## 3. Orientation Map object

The immutable map envelope contains:

- map identity, version, and integrity;
- map profile identity and version;
- exact Navigation Object identity, version, and integrity;
- exact Structural Relation Set identity, version, and integrity;
- Orientation Object identity and version;
- Representation identity, version, and integrity;
- source identity, revision, integrity, and boundary;
- canonical origin node identity;
- ordered node declarations;
- ordered edge declarations;
- ordered navigation transition declarations;
- ordered unavailable transition declarations;
- provenance;
- declared lossiness;
- responsibility state;
- explicit `after_orientation_map` STOP.

## 4. Node structure

The map contains two node classes.

### 4.1 Element nodes

Every immutable Inventory element appears exactly once.

An element node contains only:

- endpoint identity;
- element identity;
- element kind;
- canonical ordinal;
- exact locator;
- declared heading level when present;
- source-boundary reference;
- Representation lineage.

No source text, title, topic, label inferred from content, importance, or
display position is added.

### 4.2 Source-boundary node

The exact source-boundary reference appears once as a provenance node.

It contains:

- boundary identity;
- source identity and revision;
- source integrity;
- boundary reference;
- source owner reference where already declared.

It contains no source payload and grants no source authority to the map.

## 5. Edge structure

Every map edge corresponds one-to-one with one externally conformant relation.

An edge contains:

- edge identity;
- exact relation identity and ordinal;
- relation type and class;
- direction;
- source node identity;
- target node identity;
- exact relation-basis reference;
- provenance and integrity.

The map cannot synthesize, merge, omit, reverse, or relabel a validated
relation.

Symmetric relations remain explicitly symmetric. Directed relations preserve
their exact direction.

## 6. Navigation structure

Every available map transition corresponds one-to-one with one Navigation
transition declaration.

It contains:

- transition identity and ordinal;
- action;
- current and target node identities;
- relation identity where applicable;
- availability state `available`;
- Navigation Object reference.

Unavailable transitions preserve:

- attempted action;
- current node;
- required relation type;
- availability state `unavailable`;
- deterministic blocker code.

Unavailable hierarchy is represented as a boundary, not as an absent UI
feature or a guessed edge.

## 7. Canonical construction

Construction performs only these steps:

1. verify the immutable Navigation Object externally;
2. copy endpoint declarations into map nodes;
3. copy validated relation declarations into map edges;
4. copy available Navigation transitions;
5. copy required unavailable Navigation transitions;
6. preserve canonical origin and all lineage references;
7. assign deterministic map identity, version, integrity, and STOP.

Construction performs no source access, relation derivation, traversal,
selection, filtering, grouping, clustering, or layout.

## 8. Deterministic ordering

Nodes are ordered:

1. element nodes by canonical ordinal;
2. source-boundary node last.

Edges preserve canonical relation order.

Available transitions preserve canonical Navigation order.

Unavailable transitions preserve canonical Navigation unavailable order.

Serialization order is:

1. envelope;
2. nodes;
3. edges;
4. available transitions;
5. unavailable transitions;
6. provenance;
7. declared lossiness;
8. STOP.

Identical Navigation Object bytes produce identical Orientation Map bytes.

## 9. Identity and versioning

Map identity is derived only from:

- map profile identity and version;
- Navigation Object identity, version, and integrity;
- Structural Relation Set identity, version, and integrity;
- Orientation Object and Representation identities;
- canonical origin;
- ordered node, edge, and transition identities;
- declared lossiness.

Map version identifies the exact canonical serialized map bytes.

A change to any referenced node, relation, transition, source revision, input
integrity, or map profile creates a new version.

## 10. Provenance

Every map object remains traceable:

```text
Map node
    ↓
Navigation endpoint
    ↓
Relation Set endpoint
    ↓
Inventory element
    ↓
Structural Representation
    ↓
Confirmed source
```

```text
Map edge
    ↓
Navigation transition
    ↓
Validated relation and exact basis
    ↓
Inventory declaration or accepted declared relation
```

The map exposes these references. It does not replace them.

## 11. Serialization

The canonical serialization is deterministic UTF-8 JSON using:

- exact field names;
- fixed sequence order;
- sorted object keys;
- no insignificant whitespace;
- integers for ordinals and locator values;
- explicit `null` only where the profile permits absence;
- lowercase hexadecimal SHA-256 integrity values;
- no floating-point coordinates or percentages.

Presentation formats, diagrams, HTML, SVG, canvas, and spatial layouts are
non-canonical views derived later. They do not alter map identity.

## 12. Declared lossiness

The first Orientation Map explicitly does not preserve:

- raw source content;
- parser state;
- visual styling or coordinates;
- interaction history;
- Human annotations or preferences;
- semantic labels;
- undeclared hierarchy;
- relation derivation working state;
- alternative presentation layouts.

These omissions are deliberate and do not authorize reconstruction.

## 13. External map conformance

An external validator verifies:

- map profile identity and version;
- exact Navigation and Relation Set references;
- one node per accepted endpoint;
- one edge per validated relation;
- one transition per accepted Navigation transition;
- canonical origin;
- endpoint resolution;
- direction and relation identity preservation;
- unavailable blocker preservation;
- deterministic order, identity, version, and integrity;
- source and Representation lineage;
- declared lossiness;
- explicit STOP;
- absence of semantic, ranking, recommendation, layout, and storage fields.

Invalid maps are rejected. There is no partial map, silent omission, inferred
edge, or fallback layout.

## 14. Explicit exclusions

The Orientation Map performs no:

- source storage, ingestion, retrieval, or indexing;
- Relation or Navigation mutation;
- graph database behavior;
- semantic or knowledge-graph construction;
- entity, concept, claim, or Evidence processing;
- similarity, clustering, ranking, recommendation, or route selection;
- visual layout or coordinate generation;
- Human session or history persistence;
- LYRA or SIRIUS expression;
- Runtime or Gateway behavior change.

## 15. Acceptance conditions

The Orientation Map architecture is implementable only if:

- every node resolves to one accepted endpoint;
- every edge resolves to one validated relation;
- every transition resolves to one immutable Navigation declaration;
- unavailable movement remains explicit;
- all ordering and identities replay deterministically;
- map bytes are immutable and source-traceable;
- the map remains a derived view rather than storage;
- no semantic, inferred, ranked, or recommended content exists;
- execution stops immediately after the Orientation Map.
