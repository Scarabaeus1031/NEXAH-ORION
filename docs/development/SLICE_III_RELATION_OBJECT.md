# Slice III WP12 — Relation Object and Contract

Status: Implemented
Work package: WP12
Boundary: Relation Object → STOP
Schema: `orion.relation/0.1-alpha`

## Responsibility

WP12 implements one immutable atomic `RelationObject`.

It accepts exact certified Slice II Structural Summary and Structural
Statistics artifacts only to establish provenance and validate endpoint
references. The caller supplies the relation kind, endpoints, and canonical
order explicitly.

WP12 does not scan artifacts, discover a relation, generate a collection, or
decide whether two elements should be related.

## Relation Object schema

The object contains exactly:

| Field | Deterministic definition |
|---|---|
| `relation_id` | `relation-` plus the first 24 hexadecimal characters of the SHA-256 digest of the complete canonical identity basis |
| `relation_kind` | One exact member of the frozen six-kind Slice III vocabulary |
| `source_element_id` | One canonical `element-` identifier |
| `target_element_id` | One canonical `element-` identifier, or the exact `source-boundary-` identifier for `source_reference` |
| `provenance` | Immutable exact Summary, Statistics, Inventory, Orientation Object, Representation, source, and boundary lineage |
| `canonical_order` | Explicit non-negative integer; WP12 preserves it but does not order a collection |
| `schema_version` | Exact value `orion.relation/0.1-alpha` |

No field is optional. Unknown fields fail deterministic deserialization.

The permitted kinds are:

1. `immediately_precedes`;
2. `immediately_follows`;
3. `source_reference`;
4. `same_element_kind`;
5. `same_heading_level`;
6. `declared_cross_reference`.

The vocabulary is closed. An unknown kind fails construction.

## Immutable provenance

`RelationProvenance` preserves:

- exact Structural Summary identity and canonical SHA-256 reference;
- exact Structural Statistics identity and canonical SHA-256 reference;
- shared input Inventory SHA-256 reference;
- Orientation Object identity and version;
- Representation identity, version, and integrity;
- source identity, revision, integrity, and declared boundary;
- deterministic source-boundary endpoint identity.

Construction first verifies that Summary and Statistics preserve identical
Inventory, Orientation Object, Representation, source, count, and ordinal
boundaries.

The source-boundary endpoint identity is derived only from source identity,
revision, integrity, and declared boundary. No source payload is accessed.

## Deterministic identity

The identity basis contains:

```text
schema_version
relation_kind
source_element_id
target_element_id
provenance
canonical_order
```

The basis is serialized as canonical UTF-8 JSON and hashed with SHA-256.
Changing any identity-bearing field produces a different Relation identity.

Identity does not depend on time, randomness, locale, process state, source
text, parser state, UI state, or provider output.

## Canonical serialization

`canonical_relation_object_bytes` emits:

- UTF-8 JSON;
- lexicographically sorted object keys;
- compact separators;
- Unicode preserved directly;
- no insignificant whitespace;
- exact integer representation for `canonical_order`.

Identical objects produce byte-identical serialization.

`relation_object_from_dict` requires the exact top-level and provenance field
sets. Missing and unknown fields are rejected.

## Validation

`validate_relation_object` verifies:

- accepted immutable Summary and Statistics shapes;
- exact shared Slice II lineage;
- exact provenance recomputation;
- deterministic Relation identity;
- declared source endpoint;
- declared target endpoint, or exact source-boundary endpoint for
  `source_reference`;
- non-negative integer canonical order;
- exact schema version and closed relation vocabulary.

This is WP12 object-contract validation. It is not the External Relation
Conformance responsibility planned for WP16.

WP12 does not verify adjacency, equal kind, equal heading level, or an external
cross-reference declaration. Doing so would generate or establish a relation
basis and belongs to later bounded work packages.

## Canonical proof

Run:

```bash
make slice-iii-relation-object
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
One explicitly constructed Relation Object
        ↓
STOP
```

It verifies certified Slice II conformance, immutable provenance, deterministic
identity, schema validation, and byte-identical Relation replay. It records all
downstream execution states as false.

Run the focused suite:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest \
  tests.test_structural_relation_alpha
```

## Explicit exclusions

WP12 performs no:

- relation discovery or generation;
- relation collection or Structural Relation Set construction;
- graph construction;
- endpoint registry construction;
- traversal or Navigation;
- Orientation Map construction;
- source content access;
- Markdown parsing, Projection, or Rendering;
- Inventory mutation;
- semantic interpretation;
- hierarchy inference;
- ranking or recommendation;
- Runtime, Gateway, LYRA, or SIRIUS execution.

The root ORION public surface is unchanged. The Relation Object remains an
explicit internal Slice III module until a later accepted boundary states
otherwise.
