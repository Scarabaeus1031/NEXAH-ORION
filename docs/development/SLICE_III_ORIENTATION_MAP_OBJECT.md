# Slice III WP22 — Orientation Map Object

Status: Complete
Work package: WP22
Object schema: `orion.orientation-map/0.1-alpha`
Boundary: Orientation Map Object → STOP

## Responsibility

WP22 defines one immutable Orientation Map contract. It binds exact references
to the certified Navigation chain, certified Relations, and their exact Slice
II Summary and Statistics.

The object contains no constructed map content and performs no mapping,
positioning, navigation, interpretation, or visualization.

## Immutable contract

The canonical object records:

- deterministic Orientation Map identity and integrity;
- immutable schema and serialization versions;
- exact Navigation Certification identity and reference;
- exact WP18 Navigation Object identity and reference;
- exact WP19 Navigation Construction identity and reference;
- exact WP20 Navigation Conformance identity and reference;
- exact Relation Set and Relations Certification identities and references;
- exact Structural Summary and Structural Statistics identities and
  references;
- Navigation Certification as the canonical provenance reference;
- atomic canonical order `0`;
- `object_contract` state;
- `externally_conformant: false`;
- explicit `after_orientation_map_object` STOP.

The identity basis is canonical UTF-8 JSON containing every contract field
except the self-referential `orientation_map_id` and
`orientation_map_integrity`. The identity uses the first 24 hexadecimal
characters of the basis SHA-256 digest; integrity preserves the complete
digest.

## Entry requirements and provenance

Creation succeeds only when:

- Gate N is `passed` and explicitly certified;
- Gate N stopped at `at_navigation_certified`;
- Gate N names the exact WP18, WP19, and WP20 artifacts supplied;
- the Navigation chain names the exact certified Relation Set;
- Relations Certification, Summary, and Statistics references remain exact;
- the complete immutable lineage is internally consistent.

The Orientation Map Object uses the canonical Navigation Certification
reference as `provenance_ref`. It preserves earlier artifact references
explicitly without copying or interpreting their content.

## Canonical proof

Run:

```bash
make slice-iii-orientation-map-object
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
External Navigation Conformance
        ↓
Navigation Certification
        ↓
Orientation Map Object
        ↓
STOP
```

The proof verifies:

- source-fixture integrity;
- frozen WP18–WP21 fingerprints;
- exact identity and artifact references;
- input immutability;
- deterministic identity and canonical serialization;
- byte-identical replay;
- absence of Map Construction and all downstream behavior.

Run the focused suite:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest \
  tests.test_orientation_map_object_alpha
```

## Frozen dependencies

WP22 consumes the certified Navigation and Relations layers plus certified
Slice II artifacts as immutable dependencies. It does not change their
contracts, bytes, ordering, provenance, or responsibilities.

## Explicit exclusions

WP22 defines no:

- map nodes, edges, transitions, regions, clusters, or routes;
- map construction, derived map structure, or content;
- geometry, coordinates, positioning, scale, or layout;
- rendering, visualization, presentation, or storage;
- Navigation behavior;
- semantic interpretation;
- Map Conformance or Map Certification;
- Runtime or Gateway behavior.

WP22 ends immediately after the immutable Orientation Map Object exists.
