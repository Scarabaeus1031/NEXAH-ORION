# Slice III WP13 — Sequential Relations

Status: Implemented
Work package: WP13
Boundary: Sequential Relations → STOP
Schema: `orion.relation-set/sequential/0.1-alpha`

## Responsibility

WP13 creates the first deterministic relation family.

It consumes only one immutable Structural Summary and its matching immutable
Structural Statistics. It reads the canonical element identities and ordinals
already preserved by Statistics.

It produces one immutable candidate `SequentialRelationSet` containing WP12
`RelationObject` instances.

WP13 does not read Markdown, source content, Representation, or Inventory. It
does not discover semantic neighbours or create a graph.

## Adjacency rule

For each adjacent canonical pair:

```text
element[n]
        ↓
element[n + 1]
```

WP13 creates exactly:

```text
element[n] immediately_precedes element[n + 1]
element[n + 1] immediately_follows element[n]
```

No pair may skip an ordinal. No transitive relation is emitted.

For `N` declared elements:

```text
adjacent pairs = max(N - 1, 0)
relations = 2 × adjacent pairs
```

The first element never has an `immediately_follows` relation. The final
element never has an `immediately_precedes` relation.

A one-element empty-document structure therefore produces a valid immutable
candidate set containing zero relations.

## Relation Set

`SequentialRelationSet` contains:

- deterministic Relation Set identity;
- exact internal schema version;
- exact Structural Summary SHA-256 reference;
- exact Structural Statistics SHA-256 reference;
- shared input Inventory SHA-256 reference;
- relation count;
- immutable ordered tuple of WP12 Relation Objects;
- responsibility and candidate state;
- explicit `after_sequential_relations` STOP.

It is a candidate Slice III artifact. WP13 does not perform the External
Relation Conformance responsibility planned for WP16.

## Deterministic ordering

The frozen relation-type order is preserved:

1. every `immediately_precedes` relation ordered by increasing source ordinal;
2. every `immediately_follows` relation ordered by increasing source ordinal.

`canonical_order` is contiguous from zero across the complete set.

This is intentionally not pair-interleaved ordering. It follows the approved
Slice III Relations Architecture, where relation type precedes endpoint order.

Identical Summary and Statistics bytes produce identical:

- Relation Objects;
- Relation identities;
- canonical order;
- Relation Set identity;
- canonical Relation Set bytes.

## Duplicate rejection

Construction and schema validation reject:

- duplicate relation identities;
- duplicate `(kind, source, target)` declarations;
- missing or repeated canonical ordinals;
- relations outside the two permitted WP13 kinds;
- kind order that differs from the canonical type order;
- relation count mismatches;
- unknown or missing serialized fields.

Deterministic regeneration independently verifies complete adjacency. There is
no fallback, partial set, or repair.

## Provenance

The Relation Set preserves exact canonical references to Summary, Statistics,
and their shared Inventory.

Every contained WP12 Relation Object independently preserves:

- Summary identity and canonical reference;
- Statistics identity and canonical reference;
- Inventory reference;
- Orientation Object identity and version;
- Representation identity, version, and integrity;
- source identity, revision, integrity, and boundary.

`validate_sequential_relation_set` recomputes the complete expected set from
the two accepted Slice II inputs and validates every contained Relation Object
against the unchanged WP12 contract.

## Canonical serialization

`canonical_sequential_relation_set_bytes` emits compact, sorted-key UTF-8 JSON.
Ordered relations remain arrays in canonical order. Unknown fields are
rejected by strict deserialization.

No clock, randomness, locale, provider, UI state, source content, or unordered
iteration contributes to output.

## Canonical proof

Run:

```bash
make slice-iii-sequential-relations
```

The proof executes:

```text
Confirmed Markdown
        ↓
Projection
        ↓
Renderer
        ↓
Immutable Structural Representation
        ↓
External Representation Conformance
        ↓
UNDERSTAND Inventory
        ↓
Structural Summary
        ↓
Structural Statistics
        ↓
Certified Slice II STOP
        ↓
WP12 Relation Objects
        ↓
Sequential Relations
        ↓
STOP
```

It independently recomputes all adjacency pairs, verifies first and final
boundaries, duplicate absence, canonical order, provenance, contained WP12
validation, and byte-identical replay.

Run the focused suite:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest \
  tests.test_sequential_relations_alpha
```

## Explicit exclusions

WP13 generates no:

- `same_element_kind`;
- `same_heading_level`;
- `source_reference`;
- `declared_cross_reference`;
- parent, child, contains, or sibling relation;
- transitive or inferred neighbour;
- relation graph;
- traversal or Navigation;
- Orientation Map;
- semantic interpretation;
- ranking or recommendation.

It performs no Markdown parsing, Projection, Rendering, source access,
Inventory mutation, Runtime, Gateway, LYRA, or SIRIUS behavior.

The WP12 Relation Object contract remains unchanged.
