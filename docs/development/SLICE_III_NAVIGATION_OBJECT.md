# Slice III WP18 — Navigation Object

Status: Complete
Work package: WP18
Object schema: `orion.navigation/0.1-alpha`
Boundary: Navigation Object → STOP

## Responsibility

WP18 defines one immutable Navigation context. It binds exact references to:

- the certified immutable Relation Set;
- its immutable Relations Certification Report;
- the exact immutable Structural Summary;
- the exact immutable Structural Statistics.

The object does not copy Relations and does not perform Navigation. It provides
the stable contract upon which later, separately bounded Navigation work may
operate.

## Immutable contract

The canonical object contains:

| Field | Definition |
|---|---|
| `navigation_id` | stable identity derived from the canonical identity basis |
| `navigation_integrity` | full SHA-256 digest of the identity basis |
| `navigation_schema_version` | `orion.navigation/0.1-alpha` |
| `relation_set_id` | exact certified Relation Set identity |
| `relation_set_ref` | SHA-256 reference to canonical Relation Set bytes |
| `relations_certification_id` | exact Gate R certification identity |
| `relations_certification_ref` | SHA-256 reference to canonical Gate R bytes |
| `summary_id` / `summary_ref` | exact Summary identity and canonical reference |
| `statistics_id` / `statistics_ref` | exact Statistics identity and canonical reference |
| `provenance_ref` | exact Gate R certification reference |
| `canonical_order` | `0`, the sole atomic object position |
| `serialization_version` | `canonical-json/1` |
| `responsibility` | `navigation_object_contract` |
| `contract_state` | `object_contract` |
| `externally_conformant` | `false`; WP20 has not executed |
| `stop` | `after_navigation_object` |

The identity basis is canonical UTF-8 JSON containing every contract field
except the self-referential `navigation_id` and `navigation_integrity`.
`navigation_id` uses the first 24 hexadecimal characters of that basis digest;
`navigation_integrity` preserves the complete digest. The full object is then
serialized as canonical UTF-8 JSON with sorted keys and no insignificant
whitespace.

## Entry requirements and provenance

Creation succeeds only when:

- Gate R is `passed` and explicitly certified;
- Gate R stopped at `at_relations_certified`;
- the supplied Relation Set is the exact set named by Gate R;
- Summary and Statistics are the exact artifacts named by Gate R;
- Relation Set, Summary, and Statistics share one immutable Inventory lineage;
- every supplied artifact validates its own immutable shape.

The Navigation Object takes Gate R's canonical artifact reference as
`provenance_ref`. Earlier references remain explicit rather than being replaced
or reinterpreted.

## Canonical proof

Run:

```bash
make slice-iii-navigation-object
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
STOP
```

The proof verifies:

- the source fixture and certified Relations implementation fingerprints;
- exact Relation Set, certification, Summary, and Statistics references;
- input immutability before and after object creation;
- deterministic identity and canonical serialization;
- byte-identical object replay;
- the absence of all downstream execution.

Run the focused suite:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest \
  tests.test_navigation_object_alpha
```

## Frozen dependencies

WP18 consumes WP12–WP17 and the certified Slice II artifacts as immutable
dependencies. It does not modify their contracts, content, ordering,
provenance, or certification.

## Explicit exclusions

WP18 defines no:

- relation generation, validation, repair, completion, or mutation;
- Relation catalog or copied Relation payload;
- Navigation address, transition, movement, result, or history;
- traversal, route generation, path finding, graph search, or optimization;
- ranking, heuristic, or recommendation;
- External Navigation Conformance claim;
- Orientation Map;
- source access, Markdown parsing, Projection, or Rendering;
- semantic interpretation;
- Runtime or Gateway behavior.

Those exclusions are observable in the object shape and canonical proof. WP18
ends after the immutable Navigation Object exists.
