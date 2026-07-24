# Slice III WP17 — Relations Certification

Status: Certified
Work package: WP17
Gate: Relations Certification (Gate R)
Report schema: `orion.relations-certification/0.1-alpha`
Boundary: Relations Certification → STOP

## Responsibility

WP17 certifies the completed Relations layer without adding behavior.

The certification function accepts only:

- one supplied immutable WP15 Relation Set;
- the immutable WP16 Relation Conformance Report that accepted that exact set;
- the exact immutable Structural Summary;
- the exact immutable Structural Statistics.

It produces one immutable `RelationsCertificationReport`.

Certification does not call WP12–WP15 generators. It does not call the WP16
validator. It does not reconstruct, regenerate, validate, normalize, repair,
complete, reorder, or interpret relations.

## Certification report

The immutable report records:

- deterministic certification identity and full integrity;
- Gate R identity and version;
- exact Relation Set identity and canonical reference;
- exact WP16 report identity and canonical reference;
- exact Summary and Statistics references;
- frozen WP12–WP16 implementation fingerprints;
- `passed` or `failed` status;
- ordered observations and blockers;
- byte-replay results;
- identifier, hash, serialization, and ordering stability;
- provenance preservation;
- input immutability;
- fixed responsibility;
- explicit `at_relations_certified` STOP.

A failed entry requirement produces a deterministic failed certification
record. It never produces a partially certified layer.

## Certification methodology

### Entry consistency

Certification verifies that:

- every supplied artifact has its accepted immutable shape;
- WP16 accepted the exact supplied Relation Set;
- the WP16 accepted reference equals the canonical supplied-set hash;
- WP16 names the exact supplied Summary and Statistics;
- the Relation Set, Summary, and Statistics preserve one Inventory lineage;
- the WP16 STOP is exact.

This is artifact-reference consistency. It is not additional Relation
Conformance.

### Deterministic replay

Certification serializes the supplied Relation Set and WP16 report repeatedly.
It requires:

- byte-identical Relation Set serialization;
- byte-identical WP16 report serialization;
- stable identities;
- stable SHA-256 references;
- stable canonical ordering already observed and accepted by WP16;
- stable provenance observations already accepted by WP16.

Certification never regenerates either artifact.

### Input immutability

The canonical bytes of all four inputs are captured before and after
certification. Any difference blocks Gate R.

### Frozen contracts

The certification baseline records exact source fingerprints for:

| Package | Component |
|---|---|
| WP12 | Relation Object |
| WP13 | Sequential Relations |
| WP14 | Structural Equality Relations |
| WP15 | Declared Cross References |
| WP16 | External Relation Conformance |

The canonical proof and focused tests compare each recorded fingerprint with
the repository file. The certification function itself performs no filesystem
access.

## Canonical proof

Run:

```bash
make slice-iii-relations-certification
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
STOP
```

Outside the certification function, the proof:

- replays the certified Slice II proof twice;
- replays each WP12–WP16 canonical proof twice;
- compares every replay byte-for-byte;
- compares WP12–WP16 source hashes with the frozen baseline;
- verifies the four supplied inputs remain byte-identical;
- serializes the certification report twice;
- verifies byte-identical certification;
- confirms execution stops before Navigation.

Run the focused suite:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest \
  tests.test_relations_certification_alpha
```

## Reproducibility guarantees

Given the same four supplied immutable artifacts and the same frozen contract
fingerprints, certification produces the same:

- status;
- checks and blockers;
- artifact references;
- certification identity;
- certification integrity;
- canonical UTF-8 JSON bytes.

No clock, randomness, locale, network, provider, cache, or mutable state
contributes to the result.

## Frozen Relations layer

After Gate R passes:

- WP12–WP16 become the frozen Relations foundation;
- the accepted Relation Set remains immutable;
- the WP16 report remains immutable;
- WP17 becomes the sole certification record for that accepted pair;
- later Navigation work may consume the certified references;
- later work may not reinterpret or mutate them.

Reopening these packages requires an explicit future governance decision and a
new certification baseline. It cannot occur implicitly through Navigation.

## Explicit exclusions

WP17 performs no:

- relation construction, generation, validation, or completion;
- Relation Set or WP16 report regeneration;
- repair, normalization, mutation, addition, deletion, or reordering;
- semantic or hierarchy interpretation;
- source access, parsing, Projection, or Rendering;
- Runtime or Gateway behavior;
- Navigation Object or traversal;
- Orientation Map;
- LYRA or SIRIUS behavior.

Gate R certifies the Relations layer only. It introduces no Navigation
capability.
