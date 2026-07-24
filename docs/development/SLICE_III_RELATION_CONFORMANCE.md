# Slice III WP16 — External Relation Conformance

Status: Implemented
Work package: WP16
Boundary: External Relation Conformance → STOP
Report schema: `orion.relation-conformance/0.1-alpha`

## Responsibility

WP16 observes one supplied immutable WP15 candidate and decides whether it
conforms to the frozen Slice III relation contracts.

It accepts exactly:

- one immutable `DeclaredReferenceRelationSet`;
- its exact immutable Structural Summary;
- its exact immutable Structural Statistics.

It produces only one immutable `RelationConformanceReport`.

The validator never calls a relation generator. It cannot construct, add,
remove, reorder, normalize, repair, or partially accept a Relation Object or
Relation Set.

## Relation Conformance Report

The report contains:

- deterministic report identity and schema version;
- observed Relation Set identity and canonical reference;
- exact Summary and Statistics references;
- deterministic validity and `accepted` or `rejected` decision;
- ordered validation checks and errors;
- accepted Relation Set reference only when every supplied field is valid;
- explicit confirmation that the input remained unchanged;
- fixed responsibility;
- explicit `after_external_relation_conformance` STOP.

A rejection report never contains an accepted Relation Set reference.

## Validation methodology

The validator independently checks the supplied artifact without invoking
WP12–WP15 construction.

### Object and schema

It verifies:

- exact immutable WP15 object type;
- exact candidate schema, state, identity, counts, and STOP;
- every unchanged WP12 Relation Object;
- relation schema, kind, identifiers, identity, and canonical ordinal;
- canonical UTF-8 serialization and strict round-trip parsing.

### Lineage and provenance

It verifies:

- Summary and Statistics are immutable and internally valid;
- both preserve identical Slice II lineage;
- the Relation Set names their exact canonical references;
- every Relation Object preserves the same exact Inventory, Representation,
  Orientation Object, source, and source-boundary lineage;
- every declared cross-reference has one immutable declaration reference.

### Structural validity

Without creating Relation Objects, it validates the exact declared basis of
each supplied structural relation:

- an immediate predecessor relation names consecutive ordinals;
- an immediate follower relation names the exact reverse adjacency;
- a source reference names the exact preserved source boundary;
- an equal-kind relation names elements with identical declared kinds;
- an equal-heading-level relation names headings with identical declared
  levels and canonical symmetric endpoint order.

Conformance does not enumerate relations that were not supplied. It does not
decide whether any additional relation should exist. Generation completeness
remains exclusively with WP13, WP14, and WP15.

Declared cross-references are not rediscovered. Conformance checks only that
their count, endpoints, WP12 provenance, and immutable declaration-reference
bindings are exact.

### Ordering and duplicates

The validator checks:

- the frozen six-kind relation order;
- contiguous canonical ordinals;
- valid declared endpoints;
- exact source-boundary targets;
- duplicate relation-fact absence;
- duplicate relation-identity absence;
- unique immutable declaration references.

### Responsibility boundary

The observed candidate must contain no semantic, inferred, hierarchy, graph,
Navigation, Orientation Map, ranking, or recommendation fields.

This is structural contract validation, not semantic validation.

## Atomic rejection

Any failed check rejects the entire candidate deterministically.

There is:

- no partial acceptance;
- no fallback;
- no inferred missing relation;
- no reordered output;
- no repaired identity;
- no altered provenance.

Malformed inputs still produce an immutable deterministic rejection report.
They never produce a normalized candidate.

## Determinism and immutability

Report identity is derived from:

- observed artifact references;
- exact decision;
- ordered checks;
- ordered errors;
- accepted reference, when valid;
- input-unchanged observation;
- fixed responsibility and STOP.

Identical immutable inputs produce byte-identical reports. The validator
captures the supplied candidate before and after observation and requires
identical bytes.

## Canonical proof

Run:

```bash
make slice-iii-relation-conformance
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
STOP
```

It validates one generated candidate twice and verifies byte-identical
acceptance. It also verifies that an internally valid supplied subset is
observed without completion or rejection merely because another relation
could exist. It then replays deterministic rejection for:

- malformed input;
- duplicate relation;
- invalid endpoint;
- invalid declared structural basis;
- invalid provenance;
- invalid relation kind;
- invalid ordering.

Every rejection is atomic and byte-identical on replay. The supplied valid
candidate remains byte-identical before and after validation.

Run the focused suite:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest \
  tests.test_relation_conformance_alpha
```

## Explicit exclusions

WP16 performs no:

- relation construction or generation;
- relation completeness determination;
- search for absent or additional relations;
- normalization, mutation, repair, addition, or deletion;
- source access, parsing, Projection, or Rendering;
- semantic or hierarchy validation;
- partial acceptance;
- Relations Certification;
- graph construction;
- Navigation;
- Orientation Map;
- Runtime, Gateway, LYRA, or SIRIUS behavior.

Certified Slice II artifacts and all WP12–WP15 artifacts, contracts, and
generators remain unchanged.
