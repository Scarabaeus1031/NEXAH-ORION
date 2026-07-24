# Slice II — Structural Expansion II

- Status: implemented
- Renderer: `orion.renderer/markdown-structure@0.3-alpha`
- Profile: `orion.representation/markdown-structure@1.0.0`
- Projection: `orion.projection/markdown-structure@1.0.0`
- Grammar: CommonMark `0.31.2`
- STOP: `after_declared_source_element_inventory`

## Completed work packages

- WP5 — `fenced_code_block`
- WP6 — `indented_code_block`
- WP7 — `setext_heading`

The implementation executes only the frozen Projection rules:

- fenced blocks preserve their opening-to-closing or opening-to-EOF physical
  extent;
- indented blocks preserve their assigned physical extent;
- Setext headings preserve level `1` or `2` and their content-to-underline
  extent.

No code content, fence metadata, indentation width, inline content or parser
metadata enters the Structural Representation.

UNDERSTAND continues to consume only the immutable Structural Representation.
It preserves already-declared kinds, heading levels, identities, locators,
ordinals and lineage without opening source material.

## Verification

Run focused tests:

```text
PYTHONPATH=src python3 -m unittest \
  tests.test_markdown_structural_renderer_alpha \
  tests.test_understand_source_element_inventory_alpha \
  tests.test_slice_ii_structural_expansion_ii
```

Run all three bounded proofs:

```text
PYTHONPATH=src python3 scripts/slice_ii_structural_expansion_ii_proofs.py
```

Each proof follows:

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
STOP
```

## Preserved exclusions

This milestone does not implement:

- complete-vocabulary proof;
- Structural Summary or Statistics;
- relations, navigation or Orientation Map;
- semantic interpretation;
- Runtime or Gateway behavior;
- public application behavior.

The architecture, public contracts, Runtime and Gateway remain unchanged.
