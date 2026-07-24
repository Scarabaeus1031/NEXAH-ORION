# Slice II Structural Summary

Status: Implemented
Work package: WP9
Boundary: Structural Summary → STOP

## Responsibility

The Structural Summary is an immutable internal UNDERSTAND diagnostic. It
describes only organization already declared by an accepted immutable Source
Element Inventory.

The Summary accepts exactly one input:

```text
Declared Source Element Inventory
```

That Inventory is the accepted, identity-preserving view of one immutable
Structural Representation. The Summary therefore remains fully traceable to
the Representation without receiving raw Markdown, source text, Projection
state, Renderer state, parser output, or external knowledge.

The Summary does not describe what a document means. It records only what the
Representation has structurally declared.

## Summary object

`StructuralSummaryDiagnostic` is frozen and contains:

- deterministic Summary identity and diagnostic version;
- UNDERSTAND operator identity, responsibility, and input boundary;
- SHA-256 reference to the exact canonical input Inventory;
- Orientation Object identity and version;
- Representation identity, version, and integrity;
- source identity, revision, integrity, and boundary;
- total declared element count;
- the complete ordered sequence of declared element kinds;
- heading kind, identity, ordinal, and level for declared headings;
- first and final canonical ordinal;
- block kinds in their first declared order;
- Profile v1 kinds absent from the Inventory;
- the complete frozen Profile v1 vocabulary;
- responsibility state and the explicit `after_structural_summary` STOP.

No raw text or excerpt is copied. Because Profile v1 declares no parent
hierarchy or source text, WP9 does not invent a title, section hierarchy,
nesting depth, list hierarchy, or semantic outline.

## Deterministic derivation

Every field derives from either:

1. an exact immutable Inventory field; or
2. the frozen Profile v1 vocabulary constant.

The input reference is:

```text
sha256:<canonical Inventory bytes>
```

The Summary identity uses only that input reference, the diagnostic version,
the UNDERSTAND operator identity and version, and the responsibility identity.
No clock, locale, randomness, environment state, or unordered iteration enters
the derivation.

Equal canonical Inventory bytes therefore produce equal Summary objects and
byte-identical canonical Summary serialization.

## Provenance and external verification

`validate_structural_summary` independently recomputes the expected Summary
from the accepted Inventory and verifies:

- diagnostic identity and version;
- responsibility and STOP boundary;
- exact Inventory reference;
- Orientation Object lineage;
- Representation lineage and integrity;
- source lineage, revision, integrity, and boundary;
- element count and canonical order;
- declared heading identities, ordinals, kinds, and levels;
- declared and absent Profile v1 vocabulary;
- absence of semantic and downstream fields.

Any changed field fails deterministic conformance. The verifier does not repair
or normalize a Summary.

## Canonical proof

The WP9 proof executes:

```text
Confirmed Markdown
        ↓
Projection
        ↓
Renderer
        ↓
Immutable Structural Representation
        ↓
External Conformance
        ↓
UNDERSTAND
        ↓
Declared Source Element Inventory
        ↓
Structural Summary
        ↓
STOP
```

Run it with:

```bash
make slice-ii-structural-summary
```

Run the focused suite with:

```bash
PYTHONPATH=src python3 -m unittest \
  tests.test_understand_structural_summary_alpha
```

Two proof executions must emit byte-identical canonical JSON. The output
contains the exact input, Representation, Inventory, Summary, conformance,
lineage, replay verification, exclusions, and STOP marker.

## Explicit exclusions

WP9 performs no:

- Structural Statistics;
- relation inference;
- navigation or Orientation Map generation;
- source parsing, Projection, or Rendering inside Summary;
- semantic interpretation;
- topic, entity, concept, claim, Evidence, intent, or meaning inference;
- LYRA, SIRIUS, Runtime, or Gateway execution;
- AI-generated summarization.

The frozen architecture, public contracts, Markdown profile, Projection
specification, Renderer, Runtime, and Gateway remain unchanged.
