# Slice III WP14 — Structural Equality Relations

Status: Implemented
Work package: WP14
Boundary: Structural Equality Relations → STOP
Schema: `orion.relation-set/structural-equality/0.1-alpha`

## Responsibility

WP14 adds the second deterministic relation family.

It consumes only one immutable Structural Summary and its matching immutable
Structural Statistics. It compares only the declared Profile v1 element kind
and, for headings, the declared heading level.

WP14 creates a new immutable candidate `StructuralEqualityRelationSet`. The
candidate preserves the complete WP13 Sequential Relation Set as an unchanged
prefix and appends only WP12 `RelationObject` instances of these kinds:

- `same_element_kind`;
- `same_heading_level`.

It does not read Markdown, source text, Representation, or Inventory. It does
not compare content, infer hierarchy, or establish semantic similarity.

## Equality rules

### Same element kind

For every unordered pair of canonical elements whose exact declared Profile v1
kind is equal, WP14 creates exactly one relation:

```text
element[n] same_element_kind element[m]
```

The lower canonical ordinal is always the source endpoint. Different kinds are
never related.

### Same heading level

For every unordered pair of declared headings whose exact integer heading
level is equal, WP14 creates exactly one relation:

```text
heading[n] same_heading_level heading[m]
```

The lower canonical ordinal is always the source endpoint. A shared element
kind is not sufficient: the declared heading levels must also be identical.
No parent, child, section, or hierarchy relation is inferred.

## Relation Set

`StructuralEqualityRelationSet` contains:

- deterministic Relation Set identity;
- exact internal schema version;
- canonical SHA-256 reference to the unchanged WP13 candidate set;
- exact Structural Summary and Structural Statistics references;
- shared input Inventory reference;
- separate sequential and equality relation counts;
- total relation count;
- immutable ordered tuple of unchanged WP12 Relation Objects;
- responsibility and candidate state;
- explicit `after_structural_equality_relations` STOP.

It remains a candidate Slice III artifact. WP14 does not perform the External
Relation Conformance responsibility planned for WP16.

## Deterministic ordering

The complete WP14 type order is:

1. `immediately_precedes`;
2. `immediately_follows`;
3. `same_element_kind`;
4. `same_heading_level`.

Within each equality kind, pairs follow increasing source ordinal and then
increasing target ordinal. Symmetric reverse duplicates are never emitted.
`canonical_order` is contiguous from zero across the complete candidate set.

Identical Summary and Statistics bytes produce identical:

- qualifying pairs;
- Relation Objects and identities;
- canonical order;
- Relation Set identity;
- canonical Relation Set bytes.

## Validation

Construction and validation reject:

- unknown or forbidden relation kinds;
- duplicate relation identities;
- duplicate `(kind, source, target)` declarations;
- reverse or non-canonical equality endpoints;
- different element kinds declared as equal;
- different heading levels declared as equal;
- missing or repeated canonical ordinals;
- changed WP13 sequential prefix;
- mismatched Summary, Statistics, or Inventory lineage;
- count or identity mismatches;
- unknown or missing serialized fields.

`validate_structural_equality_relation_set` independently regenerates the
complete expected candidate from the two accepted Slice II inputs. Every
contained relation is also validated against the unchanged WP12 Relation
Object contract.

## Provenance

The candidate preserves exact canonical references to:

- the WP13 Sequential Relation Set;
- Structural Summary;
- Structural Statistics;
- their shared Inventory.

Every contained WP12 Relation Object preserves the accepted Orientation
Object, Representation, source, Summary, Statistics, and Inventory lineage.
WP14 adds no semantic or external provenance.

## Canonical serialization

`canonical_structural_equality_relation_set_bytes` emits compact, sorted-key
UTF-8 JSON. Ordered relations remain arrays in canonical order. Strict
deserialization rejects unknown fields.

No time, randomness, locale, provider, source content, UI state, or unordered
iteration contributes to the output.

## Canonical proof

Run:

```bash
make slice-iii-structural-equality
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
Structural Equality Relations
        ↓
STOP
```

It independently recomputes every qualifying equality pair and verifies the
unchanged WP13 prefix, canonical endpoint and type ordering, duplicate absence,
WP12 validation, provenance, fixture integrity, and byte-identical replay.

Run the focused suite:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest \
  tests.test_structural_equality_relations_alpha
```

## Explicit exclusions

WP14 generates no:

- `source_reference`;
- `declared_cross_reference`;
- semantic, lexical, or content similarity;
- parent, child, contains, or hierarchy relation;
- relation graph;
- traversal or Navigation;
- Orientation Map;
- ranking or recommendation.

It performs no Markdown parsing, Projection, Rendering, source access,
Inventory mutation, Runtime, Gateway, LYRA, or SIRIUS behavior.

The certified Slice II artifacts, WP12 Relation Object contract, and WP13
Sequential Relation Set contract remain unchanged.
