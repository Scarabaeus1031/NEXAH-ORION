# Slice II Complete Vocabulary Proof

Status: Implemented
Work package: WP8
Boundary: Complete Vocabulary Verified → STOP

## Purpose

WP8 verifies that the frozen Markdown Structural Representation Profile v1 is
implemented across its complete block vocabulary. It adds no Markdown
capability. The proof reuses the accepted Projection, Renderer, immutable
Structural Representation, External Conformance validator, and UNDERSTAND
Declared Source Element Inventory.

The canonical source fixture is
[`complete_vocabulary.md`](../../examples/markdown_structural_renderer_alpha/complete_vocabulary.md).
Its UTF-8 SHA-256 digest is:

```text
e44bcf3c8e93d7371318f22b459d75b0cf56d7e581ac5fa41ab855ee49ecc87d
```

The fixture contains at least one declaration of every Profile v1 block kind.

## Canonical coverage matrix

| Block kind | Projection | Representation | External Conformance | UNDERSTAND Inventory | Proof |
|---|---:|---:|---:|---:|---:|
| `document` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `block_quote` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `ordered_list` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `unordered_list` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `list_item` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `atx_heading` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `setext_heading` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `paragraph` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `thematic_break` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `fenced_code_block` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `indented_code_block` | ✓ | ✓ | ✓ | ✓ | ✓ |

This matrix is canonical implementation evidence for the Profile v1 block
vocabulary. It reports executable coverage, not an extension of the frozen
profile.

## Proof method

The executable proof performs exactly this chain:

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
Complete Vocabulary Verified
        ↓
STOP
```

For every declared kind, the proof verifies:

- presence in the deterministic Projection mapping;
- presence in the immutable Structural Representation;
- acceptance by External Conformance;
- presence in the UNDERSTAND inventory;
- stable identity and canonical order on replay;
- preserved source and Representation provenance;
- byte-identical Representation, inventory, and proof replay.

The proof also requires the projected, represented, and inventoried vocabulary
sets to equal the frozen Profile v1 vocabulary exactly. A subset or a superset
fails verification.

## Replay

Run the canonical proof:

```bash
make slice-ii-complete-vocabulary
```

Run the focused verification:

```bash
PYTHONPATH=src python3 -m unittest \
  tests.test_slice_ii_complete_vocabulary_proof
```

Two executions of the proof must emit byte-identical canonical JSON. The
fixture digest, source revision, Representation integrity, element identities,
inventory lineage, and STOP marker remain inspectable in that output.

## UNDERSTAND boundary

UNDERSTAND receives only the immutable Structural Representation. It does not
receive raw Markdown and performs no parsing, Projection, Rendering, semantic
interpretation, summarization, statistical aggregation, or relation inference.

The proof stops after complete vocabulary verification. Structural Summary,
Structural Statistics, Relations, Navigation, Orientation Map, Runtime,
Gateway, LYRA, and SIRIUS remain unexecuted.

## Integrity

The proof fails if the canonical fixture digest changes, if any declared kind
is missing or added, if conformance fails, if identity or ordering changes, if
provenance is lost, or if any deterministic replay differs.

No architecture, Runtime, Gateway, public contract, profile, Projection
specification, Renderer responsibility, or UNDERSTAND responsibility is
modified by WP8.
