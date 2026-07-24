# Slice III WP19 — Navigation Construction

Status: Complete
Work package: WP19
Construction schema: `orion.navigation-construction/0.1-alpha`
Boundary: Navigation Construction → STOP

## Responsibility

WP19 deterministically materializes structural Navigation metadata from the
frozen WP18 contract and the exact Relations artifacts certified by Gate R.

It produces one immutable `ConstructedNavigationObject`. Construction does not
validate or certify Navigation and does not perform Navigation behavior.

## Inputs

Construction accepts only:

- the immutable WP18 Navigation Object;
- the certified immutable WP15 Relation Set;
- the immutable WP17 Relations Certification Report;
- the exact immutable Structural Summary;
- the exact immutable Structural Statistics.

Every artifact must name the same certified lineage. Construction has no access
to Markdown, source text, Projection, Renderer, or mutable state.

## Deterministic construction

Construction creates one `NavigationEntry` for each certified Relation Object,
in the Relation Set's existing canonical order.

Each entry records only:

- its deterministic entry identity and schema;
- the unchanged Relation canonical ordinal;
- the exact Relation identity and canonical SHA-256 reference;
- the declared Relation kind;
- the exact declared source and target endpoint identities;
- an adjacency reference only for `immediately_precedes` and
  `immediately_follows`;
- the Relation's exact Inventory provenance reference.

The entry does not contain a movement, route, resolution result, or traversal
state. An adjacency reference states only that the cited certified Relation is
one of the two frozen structural adjacency kinds.

## Constructed object

The immutable output records:

- deterministic construction identity and integrity;
- exact WP18 Navigation Object identity and reference;
- exact Relation Set identity and reference;
- exact Relations Certification identity and reference;
- exact Summary and Statistics references;
- the ordered immutable Navigation Entries;
- Gate R provenance;
- canonical serialization version;
- `constructed_unvalidated` state;
- `externally_conformant: false`;
- the explicit `after_navigation_construction` STOP.

The construction identity is derived from canonical UTF-8 JSON containing all
output fields except the self-referential construction identity and integrity.
The complete object is serialized with sorted keys and no insignificant
whitespace.

## Canonical ordering

WP19 never sorts or reorders Relations. Entry ordinal, Relation identity, kind,
endpoints, and reference are copied deterministically from each Relation at the
same tuple position. The proof compares both ordered sequences exactly.

## Provenance and immutability

The object-level provenance reference is the exact Gate R certification
reference. Each entry preserves the immutable Inventory provenance carried by
its Relation.

The proof captures canonical bytes for the WP18 contract, Relation Set,
Relations Certification, Summary, Statistics, and every Relation before and
after construction. All must remain byte-identical.

## Canonical proof

Run:

```bash
make slice-iii-navigation-construction
```

The proof terminates at:

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
External Relation Conformance
        ↓
Relations Certification
        ↓
Navigation Object
        ↓
Navigation Construction
        ↓
STOP
```

Run the focused suite:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest \
  tests.test_navigation_construction_alpha
```

## Explicit exclusions

WP19 performs no:

- Relation generation, validation, repair, mutation, or reordering;
- Navigation validation or certification;
- movement execution or traversal;
- route generation, path finding, breadth-first or depth-first traversal;
- graph algorithm, ranking, heuristic, recommendation, or optimization;
- persistent cursor, history, or session behavior;
- semantic interpretation;
- Orientation Map;
- Runtime or Gateway behavior.

WP19 constructs deterministic structural metadata only and stops before WP20.
