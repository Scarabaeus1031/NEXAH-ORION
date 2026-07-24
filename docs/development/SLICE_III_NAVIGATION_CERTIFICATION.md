# Slice III WP21 — Navigation Certification

Status: Certified
Work package: WP21
Gate: Navigation Certification (Gate N)
Report schema: `orion.navigation-certification/0.1-alpha`
Boundary: Navigation Certification → STOP

## Responsibility

WP21 certifies the complete Navigation layer without adding behavior.

The certification function accepts only:

- the immutable WP18 Navigation Object;
- the immutable WP19 Constructed Navigation Object;
- the immutable WP20 Navigation Conformance Report;
- the exact certified Relation Set;
- the immutable Relations Certification Report;
- the exact Structural Summary;
- the exact Structural Statistics.

It produces one immutable `NavigationCertificationReport`.

Certification does not call WP19 construction or the WP20 validator. It does
not reconstruct, regenerate, validate, normalize, repair, complete, traverse,
or interpret Navigation.

## Certification report

The report records:

- deterministic certification identity and full integrity;
- Gate N identity and version;
- exact WP18, WP19, and WP20 identities and canonical references;
- exact Relation Set, Relations Certification, Summary, and Statistics
  references;
- frozen WP18–WP20 implementation fingerprints;
- `passed` or `failed` status;
- ordered observations and blockers;
- byte-replay results for all three Navigation artifacts;
- identity, hash, serialization, and ordering stability;
- provenance preservation;
- input immutability;
- explicit `at_navigation_certified` STOP.

A failed entry requirement produces a deterministic failed certification
record. It never produces a partially certified Navigation layer.

## Certification methodology

### Entry consistency

Certification verifies that:

- every supplied artifact has its accepted immutable shape;
- WP20 accepted the exact supplied WP19 construction;
- WP18, WP19, and WP20 name one exact artifact chain;
- Gate R names the exact supplied Relation Set;
- Summary and Statistics references remain unchanged;
- provenance resolves through Gate R;
- every prior STOP is exact.

This is artifact-reference consistency, not additional Navigation
Conformance.

### Deterministic replay

Certification serializes the supplied WP18, WP19, and WP20 artifacts
repeatedly. It requires:

- byte-identical Navigation Object serialization;
- byte-identical Navigation Construction serialization;
- byte-identical Navigation Conformance Report serialization;
- stable identities and SHA-256 references;
- stable canonical ordering already observed by WP20;
- stable provenance already accepted by WP20.

Certification never regenerates any of these artifacts.

### Frozen contracts

The certification baseline records exact source fingerprints for:

| Package | Component |
|---|---|
| WP18 | Navigation Object |
| WP19 | Navigation Construction |
| WP20 | External Navigation Conformance |

The canonical proof and focused tests compare each fingerprint against the
repository. The certification function performs no filesystem access.

## Canonical proof

Run:

```bash
make slice-iii-navigation-certification
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
STOP
```

Outside the certification function, the proof:

- replays each WP18–WP20 canonical proof twice;
- compares those replays byte-for-byte;
- compares WP18–WP20 source hashes with the frozen baseline;
- verifies all seven supplied artifacts remain byte-identical;
- serializes the certification report twice;
- confirms execution stops before Orientation Map.

Run the focused suite:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest \
  tests.test_navigation_certification_alpha
```

## Reproducibility guarantees

Given the same seven supplied immutable artifacts and the same frozen contract
fingerprints, certification produces the same:

- status, checks, and blockers;
- artifact references;
- certification identity and integrity;
- canonical UTF-8 JSON bytes.

No clock, randomness, locale, network, provider, cache, source text, or mutable
state contributes to the result.

## Frozen Navigation layer

After Gate N passes:

- WP18–WP20 become the frozen Navigation foundation;
- their accepted artifacts remain immutable;
- WP21 becomes the sole certification record for that accepted chain;
- later Orientation Map work may consume certified Navigation references;
- later work may not reinterpret or mutate Navigation.

Reopening these packages requires an explicit future governance decision and a
new certification baseline.

## Explicit exclusions

WP21 performs no:

- Navigation construction, validation, regeneration, repair, or completion;
- traversal, route computation, path finding, or graph search;
- ranking, heuristics, recommendations, or optimization;
- semantic interpretation;
- Relation or Slice II mutation;
- Orientation Map;
- Runtime or Gateway behavior.

Gate N certifies the Navigation layer only and introduces no new capability.
