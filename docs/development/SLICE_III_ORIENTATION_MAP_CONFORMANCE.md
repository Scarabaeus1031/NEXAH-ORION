# Slice III WP24 — External Orientation Map Conformance

Status: Complete
Work package: WP24
Conformance schema: `orion.orientation-map-conformance/0.1-alpha`
Boundary: External Orientation Map Conformance → STOP

## Responsibility

WP24 observes the immutable WP22 Orientation Map Object, the immutable WP23
Constructed Orientation Map, and their complete certified lineage.

It produces one immutable `OrientationMapConformanceReport` containing only an
`accepted` or `rejected` decision, deterministic checks, detected errors, exact
artifact references, and the conformance STOP.

The validator does not construct, repair, normalize, reorder, complete,
visualize, or interpret either Orientation Map artifact.

## Inputs

The validator accepts only:

- the immutable Orientation Map Object;
- the immutable Constructed Orientation Map;
- the immutable Navigation Certification Report;
- the immutable Navigation Object;
- the immutable Constructed Navigation Object;
- the immutable Navigation Conformance Report;
- the certified immutable Relation Set;
- the immutable Relations Certification Report;
- the exact Structural Summary and Structural Statistics.

It has no access to Markdown, source text, Projection, or Renderer.

## Validation methodology

The report deterministically verifies:

- every supplied immutable type and its internal object invariants;
- WP22 and WP23 schema, serialization, state, identity, integrity, and STOP;
- passed Navigation and Relations certification gates;
- exact references across Map, Navigation, Relations, Summary, and Statistics;
- one-to-one Map Entry references to certified Navigation Entries;
- exact certified Relation references and endpoints;
- unchanged structural adjacency references;
- canonical entry ordering and duplicate absence;
- exact provenance lineage;
- canonical UTF-8 JSON replay for WP22 and WP23;
- absence of geometry, layout, rendering, visualization, interaction,
  animation, clustering, ranking, recommendation, routing, traversal, and
  semantic state;
- byte-identical inputs before and after observation.

The validator imports no WP23 constructor and invokes no WP25 certification.

## Decisions

`accepted` means every declared check passed. The report then records exact
accepted references for both supplied Map artifacts.

`rejected` means at least one declared check failed. Errors describe only the
observed inconsistency. Accepted references remain absent, and the rejected
artifacts remain unchanged.

Conformance never determines whether additional entries, adjacency references,
or structures ought to exist.

## Identity and serialization

The report identity is derived from canonical UTF-8 JSON containing all
observations and results except its own identifier. Serialization uses sorted
keys and no insignificant whitespace.

Identical supplied artifacts produce a byte-identical report. Identically
malformed supplied artifacts produce a byte-identical rejection report.

## Canonical proof

Run:

```bash
make slice-iii-orientation-map-conformance
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
External Orientation Map Conformance
        ↓
STOP
```

The proof verifies the accepted decision, exact provenance, input immutability,
frozen WP18–WP23 fingerprints, and byte-identical report replay.

Run the focused suite:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest \
  tests.test_orientation_map_conformance_alpha
```

## Frozen dependencies

WP24 observes but does not alter:

- certified Slice II artifacts;
- the certified Relations layer;
- the certified Navigation layer;
- the WP22 Orientation Map Object contract;
- the WP23 Orientation Map Construction.

Their exact references are validated in the supplied lineage, and their
implementation fingerprints are replayed by the canonical proof.

## Explicit exclusions

WP24 performs no:

- Orientation Map construction, regeneration, repair, normalization, or
  completion;
- final Slice III or Orientation Map certification;
- coordinate, geometry, layout, positioning, or scale computation;
- drawing, rendering, visualization, camera, interaction, or animation;
- clustering, route computation, traversal, ranking, recommendation, or
  optimization;
- semantic validation, interpretation, usefulness assessment, or visualization
  assessment;
- mutation of Map, Navigation, Relations, Summary, or Statistics artifacts;
- Runtime or Gateway behavior.

WP24 validates supplied immutable Orientation Map artifacts and stops at
`after_external_orientation_map_conformance`.
