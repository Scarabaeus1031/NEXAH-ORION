# Slice II — Structural Expansion I

- Status: implemented
- Renderer: `orion.renderer/markdown-structure@0.2-alpha`
- Profile: `orion.representation/markdown-structure@1.0.0`
- Projection: `orion.projection/markdown-structure@1.0.0`
- Grammar: CommonMark `0.31.2`
- STOP: `after_declared_source_element_inventory`

## Completed work packages

- WP2 — `block_quote`
- WP3 — atomic `ordered_list`, `unordered_list`, `list_item` family
- WP4 — `thematic_break`

The implementation executes only the frozen Projection rules. CommonMark
container state is used for source extent and depth-first pre-order, but no
parent, child, depth or containment field is emitted.

UNDERSTAND consumes the resulting immutable Structural Representation. It
copies already-declared kind, identity, locator, ordinal and lineage fields
without reading Markdown or executing Projection or Renderer.

## Verification

Run focused tests:

```text
PYTHONPATH=src python3 -m unittest \
  tests.test_markdown_structural_renderer_alpha \
  tests.test_understand_source_element_inventory_alpha \
  tests.test_slice_ii_structural_expansion_i
```

Run all three bounded proofs:

```text
PYTHONPATH=src python3 scripts/slice_ii_structural_expansion_i_proofs.py
```

Every proof executes:

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

- fenced or indented code blocks;
- Setext headings;
- Structural Summary or Statistics;
- relations or navigation;
- semantic interpretation;
- Runtime or Gateway behavior;
- public application behavior.

The architecture, public contracts, Runtime and Gateway remain unchanged.
