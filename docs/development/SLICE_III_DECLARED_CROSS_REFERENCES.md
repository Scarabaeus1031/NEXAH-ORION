# Slice III WP15 — Source and Declared Cross References

Status: Implemented
Work package: WP15
Boundary: Declared Cross References → STOP
Candidate schema: `orion.relation-set/declared-references/0.1-alpha`

## Responsibility

WP15 completes the candidate Slice III relation vocabulary using only
authoritative references that exist before relation generation.

It consumes:

- one immutable Structural Summary;
- its matching immutable Structural Statistics;
- the deterministic WP14 candidate derived from those same artifacts;
- zero or more explicit immutable accepted cross-reference declarations.

It produces one immutable `DeclaredReferenceRelationSet`.

WP15 does not read Markdown, inspect source text, discover links, approximate
identifiers, or infer a relationship.

## Source references

Every certified Inventory element already preserves the exact immutable source
boundary through Slice II lineage.

WP15 creates exactly one directed relation for each declared element:

```text
element source_reference exact source boundary
```

Elements follow canonical Inventory order. Every target is the one canonical
source-boundary identity derived from the accepted source identity, revision,
integrity, and boundary.

No source payload is copied.

## Declared cross references

A `declared_cross_reference` exists only when an
`AcceptedDeclaredCrossReference` is supplied explicitly before generation.

The immutable declaration preserves:

- deterministic declaration identity;
- explicit declaration version;
- exact source and target element identities;
- explicit directed orientation;
- exact accepted Inventory provenance reference;
- deterministic integrity;
- exact declaration schema version.

Its identity and integrity are derived from the same complete declaration
basis. Generation rejects:

- raw endpoint pairs;
- mappings that have not become accepted immutable declarations;
- unresolved endpoints;
- self-references;
- missing or inferred direction;
- duplicate identities or endpoint pairs;
- changed integrity;
- provenance naming another Inventory.

The frozen Markdown Structural Representation Profile v1 declares no
cross-references. With no separate accepted declaration, WP15 therefore emits
zero `declared_cross_reference` relations. Absence never triggers discovery.

## Complete candidate ordering

WP15 constructs the first complete candidate Structural Relation Set in the
frozen Slice III relation-type order:

1. `immediately_precedes`;
2. `immediately_follows`;
3. `source_reference`;
4. `same_element_kind`;
5. `same_heading_level`;
6. `declared_cross_reference`.

WP13 and WP14 remain unchanged. WP15 imports their exact relation facts—kind,
endpoints, and Slice II provenance—without rediscovery. It binds fresh
contiguous candidate ordinals because the frozen complete type order places
`source_reference` before the equality families. WP12 includes canonical order
in Relation identity, so complete-candidate Relation identities are
deterministically rebound; no earlier contract or artifact is mutated.

Source references follow element ordinal. Accepted declarations follow source
ordinal, target ordinal, and declaration identity. Reordering the same
accepted declaration inputs therefore cannot change the candidate bytes.

## Provenance

Every contained WP12 Relation Object preserves exact Summary, Statistics,
Inventory, Orientation Object, Representation, source, and source-boundary
lineage.

The complete candidate additionally preserves:

- the canonical WP14 candidate reference;
- one canonical reference per accepted declaration;
- the positional correspondence between canonically ordered accepted
  declarations and canonically ordered `declared_cross_reference` relations.

No external content or semantic provenance is added.

## Validation

Construction and deterministic validation verify:

- exact matching Slice II lineage;
- exact source-reference coverage;
- accepted declaration integrity and Inventory provenance;
- resolvable endpoints;
- exact relation vocabulary;
- canonical type and endpoint ordering;
- contiguous relation ordinals;
- duplicate absence;
- valid unchanged WP12 Relation Objects;
- candidate identity and counts;
- explicit `after_declared_cross_references` STOP.

WP15 does not perform External Relation Conformance. That responsibility begins
only in WP16.

## Canonical serialization

Declarations and the complete candidate use compact, sorted-key UTF-8 JSON.
Relations and declaration references remain canonically ordered arrays.
Unknown fields are rejected during strict deserialization.

No clock, randomness, locale, provider, UI state, source content, fuzzy
matching, or unordered input iteration contributes to output.

## Canonical proof

Run:

```bash
make slice-iii-declared-cross-references
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
Relation Object
        ↓
Sequential Relations
        ↓
Structural Equality Relations
        ↓
Declared Cross References
        ↓
STOP
```

It proves two deterministic cases:

1. the current Profile v1 with empty declared-reference input;
2. one explicit immutable accepted declaration with resolvable endpoints.

It verifies complete source-boundary coverage, exact declaration preservation,
prior relation-fact preservation, deterministic ordering, duplicate absence,
WP12 validation, provenance, integrity, rejection of undeclared and tampered
inputs, and byte-identical replay.

Run the focused suite:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest \
  tests.test_declared_cross_references_alpha
```

## Explicit exclusions

WP15 performs no:

- reference discovery from links, labels, URLs, or text;
- fuzzy matching or identifier approximation;
- semantic interpretation or hierarchy inference;
- external retrieval;
- graph construction;
- External Relation Conformance;
- traversal or Navigation;
- Orientation Map;
- ranking or recommendation;
- Runtime, Gateway, LYRA, or SIRIUS behavior.

Certified Slice II artifacts and the WP12–WP14 contracts and generators remain
unchanged.
