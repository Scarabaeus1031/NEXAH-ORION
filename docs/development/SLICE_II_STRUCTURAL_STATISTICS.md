# Slice II Structural Statistics

Status: Implemented
Work package: WP10
Boundary: Structural Statistics → STOP

## Responsibility

Structural Statistics is an immutable internal UNDERSTAND diagnostic derived
from exactly one accepted immutable Declared Source Element Inventory.

It measures fields already declared by the Inventory. It does not consume the
Structural Representation directly and has no access to raw Markdown, source
content, Projection, Renderer, parser state, external knowledge, relations, or
semantic information.

## Statistics object

`StructuralStatisticsDiagnostic` preserves:

- deterministic Statistics identity and diagnostic version;
- exact canonical input Inventory SHA-256 reference;
- Orientation Object identity and version;
- Representation identity, version, and integrity;
- source identity, revision, integrity, and boundary;
- UNDERSTAND operator, responsibility, and STOP state.

It contains only the statistics frozen by the Slice II completion plan:

1. total ordered elements;
2. count by Profile v1 kind in frozen vocabulary order;
3. ATX heading-level counts for levels 1–6;
4. Setext heading-level counts for levels 1–2;
5. declared container-kind and leaf-kind counts;
6. exact byte and physical-line span per element identity and ordinal;
7. first and final canonical ordinals;
8. root document byte boundary and width;
9. union-based non-document byte coverage;
10. union-based non-document physical-line coverage;
11. present and absent Profile v1 kind counts;
12. explicit `nesting_depth = unavailable`.

All values are integers or explicit availability text. No floating-point
coverage, estimate, score, percentage, ranking, or complexity measure exists.

## Deterministic derivation

Element counts are exact counts over `elements`. Heading distributions retain
zero counts in fixed profile order. Byte spans use:

```text
end_byte - start_byte
```

Physical-line spans use zero for zero-width locators and otherwise:

```text
end_line - start_line + 1
```

Non-document byte coverage is the union length of half-open declared locator
intervals. Line coverage is the union length of inclusive physical-line
intervals. Overlapping container and descendant locators are never counted
twice and never interpreted as hierarchy.

The empty-document root has zero byte width, zero available physical lines,
zero covered units, and zero uncovered units.

Nesting depth is always `unavailable` because Profile v1 declares no parent
hierarchy or depth. Statistics never reconstructs it from order, kind, locator
overlap, indentation, or source text.

## Validation and provenance

Before measurement, the input Inventory is validated for:

- immutable diagnostic shape;
- canonical ordinals;
- known Profile v1 kinds and valid heading levels;
- a first `document` declaration;
- root byte boundary beginning at zero;
- element locators within the root byte and line boundaries;
- positive width for non-document declarations;
- root-only structure for an empty document.

`validate_structural_statistics` independently verifies:

- deterministic Statistics identity and version;
- exact input Inventory reference;
- responsibility and `after_structural_statistics` STOP;
- Orientation Object, Representation, and source lineage;
- every element measurement;
- every coverage measurement;
- explicit unavailable nesting depth;
- absence of semantic, relation, and navigation fields.

Invalid or changed input is rejected. No value is repaired or inferred.

## Canonical proof

Run:

```bash
make slice-ii-structural-statistics
```

The proof executes both a complete-vocabulary UTF-8 document and an empty
document:

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
Structural Statistics
        ↓
STOP
```

The complete source includes every Profile v1 kind, nested container locators,
blank physical lines, and multi-byte UTF-8 content. The proof independently
recomputes every statistic from Inventory fields, validates provenance, and
replays Representation, Inventory, Summary, and Statistics byte-identically.

Run the focused suite:

```bash
PYTHONPATH=src python3 -m unittest \
  tests.test_understand_structural_statistics_alpha
```

## Explicit exclusions

WP10 performs no:

- Slice II closure;
- relation inference;
- navigation or Orientation Map generation;
- semantic interpretation;
- topic, entity, concept, claim, Evidence, intent, or meaning inference;
- content extraction;
- hierarchy reconstruction;
- LYRA, SIRIUS, Runtime, or Gateway execution.

Architecture, Runtime, Gateway, contracts, Profile, Projection, Renderer,
Representation, and existing UNDERSTAND responsibilities remain unchanged.
