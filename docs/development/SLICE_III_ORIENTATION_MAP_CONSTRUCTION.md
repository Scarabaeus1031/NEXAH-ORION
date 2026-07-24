# Slice III WP23 — Orientation Map Construction

Status: Complete
Work package: WP23
Construction schema: `orion.orientation-map-construction/0.1-alpha`
Boundary: Orientation Map Construction → STOP

## Responsibility

WP23 deterministically materializes structural Orientation Map metadata from
the frozen WP22 contract and certified Navigation artifacts.

It produces one immutable `ConstructedOrientationMap`. Construction does not
validate, certify, lay out, render, visualize, navigate, or interpret the map.

## Inputs

Construction accepts only:

- the immutable WP22 Orientation Map Object;
- the immutable Navigation Certification Report;
- the immutable WP18 Navigation Object;
- the immutable WP19 Navigation Construction;
- the immutable WP20 Navigation Conformance Report;
- the certified immutable Relation Set;
- the immutable Relations Certification Report;
- the exact Structural Summary and Structural Statistics.

Every artifact must name the same certified lineage. Construction has no access
to Markdown, source text, Projection, or Renderer.

## Deterministic construction

WP23 creates one `OrientationMapEntry` for each certified Navigation Entry, in
the exact existing Navigation order.

Each map entry records only:

- deterministic entry identity and schema;
- unchanged canonical ordinal;
- exact Navigation Entry identity and canonical reference;
- unchanged Relation identity, reference, kind, and endpoints;
- unchanged structural adjacency reference;
- unchanged Inventory provenance reference.

No entry contains a coordinate, position, shape, visual style, route,
recommendation, or semantic neighborhood.

## Constructed Orientation Map

The immutable output records:

- deterministic construction identity and integrity;
- exact WP22 contract identity and reference;
- exact Navigation Certification identity and reference;
- exact Navigation Construction identity and reference;
- ordered immutable Orientation Map Entries;
- Navigation Certification provenance;
- canonical serialization version;
- `constructed_unvalidated` state;
- `externally_conformant: false`;
- explicit `after_orientation_map_construction` STOP.

Identity derives from canonical UTF-8 JSON containing all output fields except
the self-referential construction identity and integrity. The complete artifact
uses sorted keys and no insignificant whitespace.

## Ordering and provenance

WP23 never sorts or reorders Navigation Entries. Map entry ordinal, Navigation
Entry identity, Relation metadata, adjacency reference, and provenance remain
at the same tuple position.

Object provenance resolves to Navigation Certification. Entry provenance
remains the exact Inventory reference already carried by certified Navigation.

## Canonical proof

Run:

```bash
make slice-iii-orientation-map-construction
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
Orientation Map Construction
        ↓
STOP
```

The proof verifies exact entry coverage, ordering, immutable references,
adjacency, provenance, input immutability, frozen WP18–WP22 fingerprints, and
byte-identical replay.

Run the focused suite:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest \
  tests.test_orientation_map_construction_alpha
```

## Explicit exclusions

WP23 performs no:

- Map Conformance or Map Certification;
- coordinate, geometry, layout, positioning, or scale generation;
- drawing, rendering, visualization, camera, interaction, or animation;
- clustering, force-directed graph, or graphical edge construction;
- shortest path, route, ranking, recommendation, or optimization;
- semantic interpretation or semantic neighborhood;
- Navigation or Relation mutation;
- Runtime or Gateway behavior.

WP23 constructs immutable structural metadata only and stops before WP24.
