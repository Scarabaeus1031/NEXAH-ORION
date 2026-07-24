# Slice III WP20 — External Navigation Conformance

Status: Complete
Work package: WP20
Report schema: `orion.navigation-conformance/0.1-alpha`
Boundary: External Navigation Conformance → STOP

## Responsibility

WP20 observes the immutable WP18 Navigation Object and immutable WP19
Constructed Navigation Object against their exact certified dependencies. It
produces one immutable `NavigationConformanceReport`.

Conformance does not construct, repair, normalize, complete, reorder, mutate,
traverse, or certify Navigation.

## Inputs

The validator accepts only:

- one immutable WP19 Constructed Navigation Object;
- its exact immutable WP18 Navigation Object;
- the exact certified immutable Relation Set;
- the immutable Relations Certification Report;
- the exact immutable Structural Summary;
- the exact immutable Structural Statistics.

It has no access to Markdown, source text, Projection, or Renderer.

## Conformance report

The report records:

- deterministic report identity and schema;
- observed construction and Navigation identities and references;
- exact Relation Set and Gate R identities and references;
- exact Summary and Statistics references;
- ordered checks and deterministic errors;
- `accepted` or `rejected` decision;
- the accepted construction reference only after complete acceptance;
- input immutability;
- fixed responsibility;
- explicit `after_external_navigation_conformance` STOP.

A rejected report never accepts or modifies a supplied artifact.

## Validation methodology

WP20 independently observes:

- WP18 and WP19 schema, identity, integrity, state, and STOP boundaries;
- canonical serialization replay for both Navigation artifacts;
- the passed Relations Certification Gate;
- exact Relation Set, Gate R, Summary, and Statistics references;
- contiguous Navigation Entry order equal to certified Relation order;
- duplicate absence across entry, Relation identity, and Relation reference;
- exact one-to-one immutable Relation references;
- adjacency references only for the two certified sequential Relation kinds;
- object-level Gate R and entry-level Inventory provenance;
- absence of traversal, routes, search, ranking, heuristics, and map state;
- byte-identical inputs before and after observation.

The validator does not call WP19 construction. Missing or malformed metadata is
rejected; it is never regenerated.

## Rejection rules

Acceptance is atomic. Any failed check rejects the supplied construction,
including:

- malformed identity, integrity, schema, state, or STOP;
- uncertified or inconsistent dependencies;
- duplicate, missing, reordered, or redirected entries;
- invalid Relation or adjacency references;
- altered provenance;
- noncanonical serialization;
- forbidden behavioral or downstream fields;
- any mutation during observation.

## Canonical proof

Run:

```bash
make slice-iii-navigation-conformance
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
STOP
```

The proof verifies canonical report replay, provenance, input immutability,
frozen WP12–WP19 fingerprints, and absence of downstream execution.

Run the focused suite:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest \
  tests.test_navigation_conformance_alpha
```

## Frozen dependencies

WP20 observes WP18, WP19, and the certified Relations and Slice II artifacts.
It does not change their contracts, bytes, ordering, provenance, or
responsibility.

## Explicit exclusions

WP20 performs no:

- Navigation construction, regeneration, repair, normalization, or completion;
- entry or Relation reordering;
- Relation generation, validation, or mutation;
- traversal, route calculation, path finding, or graph search;
- ranking, heuristic, recommendation, or optimization;
- Navigation Certification;
- Orientation Map;
- semantic interpretation;
- Runtime or Gateway behavior.

External Navigation Conformance validates integrity only and stops before
WP21.
