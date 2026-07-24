# ORION Core Plate

Status: Canonical frozen cross-layer reference
Baseline: Certified ORION Core after WP25
Certified STOP: `at_slice_iii_certified`

## Purpose

The ORION Core Plate assembles the already certified Foundation and Vertical
Slices I–III into one architectural view.

It records the deterministic dependency chain, repeated layer pattern,
certification boundaries, implemented capabilities, explicit exclusions, and
the boundary between the certified Core and future work.

This document introduces no component, responsibility, contract, behavior, or
terminology. The detailed frozen architecture and certified implementation
artifacts remain authoritative for their individual responsibilities. This
plate is the canonical reference for how those responsibilities form one Core.

## 1. Current Certified State

| Assembly | Work packages | Certified responsibility | Closing boundary |
|---|---:|---|---|
| Foundation | Unnumbered prerequisite | Frozen ownership, Representation, Structural Representation, Markdown profile, Projection, identity, provenance, and conformance boundaries | Foundation freeze |
| Vertical Slice I | WP1 and the accepted Alpha baseline | Deterministic Projection and Rendering into an immutable Structural Representation, followed by external Representation Conformance and UNDERSTAND Inventory | Inventory proof STOP |
| Vertical Slice II | WP2–WP11 | Complete Profile v1 block vocabulary, immutable Structural Summary, immutable Structural Statistics, and Slice II closure | `at_slice_ii_complete` |
| Slice III-A — Relations | WP12–WP17 | Immutable Relation Object, deterministic structural and declared Relations, External Relation Conformance, and Relations Certification | `at_relations_certified` |
| Slice III-B — Navigation | WP18–WP21 | Immutable Navigation Object, deterministic Navigation Construction, External Navigation Conformance, and Navigation Certification | `at_navigation_certified` |
| Slice III-C — Orientation Map | WP22–WP24 | Immutable Orientation Map Object, deterministic Orientation Map Construction, and External Orientation Map Conformance | `after_external_orientation_map_conformance` |
| Vertical Slice III Certification | WP25 | Reproducibility certification of Relations, Navigation, and Orientation Map as one immutable chain | `at_slice_iii_certified` |

Foundation is a prerequisite rather than a user-facing capability. WP1–WP25
form the numbered certified implementation sequence assembled by this plate.

## 2. Complete Dependency Chain

```text
Human Confirmed Source
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
Slice II Certification
        │  Gate: at_slice_ii_complete
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
        │  Gate: at_relations_certified
        ↓
Navigation Object
        ↓
Navigation Construction
        ↓
External Navigation Conformance
        ↓
Navigation Certification
        │  Gate: at_navigation_certified
        ↓
Orientation Map Object
        ↓
Orientation Map Construction
        ↓
External Orientation Map Conformance
        ↓
Vertical Slice III Certification
        │  Gate: at_slice_iii_certified
        ↓
       STOP
```

### Foundation and Slice I boundary

The Human-confirmed source enters the frozen Representation Boundary with
explicit identity, revision, integrity, and scope.

Projection defines the accepted CommonMark-to-structure mapping. Renderer
executes that mapping. The immutable Structural Representation preserves only
the declared structure, order, locators, identity, provenance, integrity, and
lossiness.

External Representation Conformance validates the Representation outside
Renderer authority. UNDERSTAND consumes only that immutable Representation and
inventories only already-declared elements. It never receives raw Markdown.

### Slice II Certification Gate

Structural Summary describes declared organization. Structural Statistics
measures declared fields. Neither interprets content.

The Slice II gate certifies the complete Profile v1 structural vocabulary,
Inventory, Summary, Statistics, provenance, determinism, immutability, and
replay. Slice III begins only after `at_slice_ii_complete`.

### Relations Certification Gate

Relations consume certified Slice II artifacts. They preserve immediate
sequence, declared structural equality, and already-authoritative references
within the closed certified relation vocabulary.

External Relation Conformance validates the supplied immutable Relation Set
without constructing or repairing it. Relations Certification freezes the
layer at `at_relations_certified`.

### Navigation Certification Gate

The Navigation Object binds certified Relations. Navigation Construction
materializes an ordered immutable navigation context that preserves exact
Relation references and structural adjacency references.

It performs no traversal, routing, ranking, or recommendation.

External Navigation Conformance validates the supplied Navigation artifacts.
Navigation Certification freezes the layer at `at_navigation_certified`.

### Orientation Map and final certification gates

The Orientation Map Object binds the certified Navigation and Relations
lineage. Orientation Map Construction creates one ordered immutable Map Entry
for each certified Navigation Entry.

It creates no coordinates, geometry, layout, rendering, visualization, route,
or semantic neighborhood.

External Orientation Map Conformance validates only the supplied Map
artifacts. WP25 then replays the Relations, Navigation, and Orientation Map
certification stages and freezes their complete dependency chain at
`at_slice_iii_certified`.

## 3. Cross-Layer Pattern

The certified Core repeats one architectural pattern:

```text
Contract
        ↓
Construction
        ↓
External Conformance
        ↓
Certification
```

Each term has one meaning:

- **Contract** defines the accepted immutable shape, vocabulary, identity,
  version, provenance, serialization, and boundary.
- **Construction** deterministically materializes only what that contract
  permits.
- **External Conformance** observes and validates the supplied immutable
  artifact outside the constructing responsibility. It never repairs or
  completes it.
- **Certification** verifies reproducibility, frozen dependencies, canonical
  replay, and the closing STOP. It introduces no behavior.

The pattern appears as follows:

| Layer | Contract | Construction | External Conformance | Certification |
|---|---|---|---|---|
| Representation and Structure | Structural Representation Profile and Projection Specification | Renderer and immutable Structural Representation | External Representation Conformance | Slice I proof boundary and Slice II Certification |
| Relations | Relation Object and closed relation vocabulary | Sequential, Structural Equality, and Declared Cross-Reference generation | External Relation Conformance | Relations Certification |
| Navigation | Navigation Object | Navigation Construction | External Navigation Conformance | Navigation Certification |
| Orientation Map | Orientation Map Object | Orientation Map Construction | External Orientation Map Conformance | Vertical Slice III Certification |

Construction never certifies itself. Conformance never constructs. Certification
never adds capability.

## 4. Cross-Layer Guarantees

The following guarantees hold across the certified Core:

- **Deterministic** — equal canonical inputs produce equal canonical outputs.
- **Immutable** — completed artifacts cannot be modified in place.
- **Canonically serialized** — artifacts use stable canonical UTF-8 JSON.
- **Stably identified** — identities derive from declared canonical bases.
- **Integrity preserving** — integrity values bind the complete declared
  artifact basis.
- **Provenance preserving** — every layer retains exact references to its
  accepted predecessors.
- **Canonically ordered** — ordering is explicit, stable, and replayable.
- **Externally conformant** — constructed artifacts are validated outside
  their construction responsibility.
- **Independently certifiable** — layer proofs and certification gates can be
  replayed without downstream execution.
- **Boundary respecting** — no stage performs the work of another stage.
- **Free of hidden inference** — every structural output follows explicit
  declared input and closed deterministic rules.
- **Non-mutating** — validators and certifiers leave supplied artifacts
  byte-identical.
- **Failure explicit** — malformed, unsupported, or inconsistent inputs are
  rejected rather than repaired or approximated.
- **STOP bounded** — each certified layer terminates at its declared boundary.

## 5. Certified Capabilities

The certified Core can currently:

1. accept one exact Human-confirmed CommonMark `0.31.2` source within the frozen
   source domain;
2. deterministically project and render the complete Markdown Structural
   Representation Profile v1 block vocabulary:
   - `document`;
   - `atx_heading`;
   - `setext_heading`;
   - `paragraph`;
   - `block_quote`;
   - `ordered_list`;
   - `unordered_list`;
   - `list_item`;
   - `thematic_break`;
   - `fenced_code_block`;
   - `indented_code_block`;
3. preserve immutable structural elements, canonical locators, ordinals,
   identities, provenance, integrity, and declared lossiness;
4. externally validate the resulting Structural Representation;
5. inventory every already-declared source element without reading source
   text;
6. produce a deterministic document-level Structural Summary;
7. produce deterministic Structural Statistics derived only from certified
   structural fields;
8. produce immutable Relations for the closed certified vocabulary:
   - `immediately_precedes`;
   - `immediately_follows`;
   - `same_element_kind`;
   - `same_heading_level`;
   - `source_reference` when explicitly declared;
   - `declared_cross_reference` when explicitly declared;
9. externally validate and certify the immutable Relation Set;
10. construct an immutable Navigation context that preserves certified
    Relation order, identities, references, endpoints, adjacency, and
    provenance;
11. externally validate and certify the Navigation layer;
12. construct an immutable structural Orientation Map whose entries preserve
    certified Navigation order and exact references;
13. externally validate the Orientation Map Object and Constructed Orientation
    Map;
14. independently replay and certify the complete Slice III chain.

These capabilities describe declared structure and its exact deterministic
relationships. They do not establish meaning.

## 6. Explicit Non-Capabilities

The certified Core intentionally does not implement:

- semantic interpretation;
- semantic relation inference;
- entities, concepts, claims, or reasoning;
- Evidence generation or Evidence Binding;
- knowledge graphs;
- source retrieval, search, or indexing;
- LLM or provider behavior;
- hidden classification or topic detection;
- hierarchy inference beyond declared Profile v1 structure;
- route execution, traversal, pathfinding, ranking, or recommendation;
- decision making or agent behavior;
- coordinates, geometry, spatial layout, or projection mathematics beyond the
  frozen structural Projection;
- graphical rendering or visualization;
- interaction, animation, camera state, or presentation state;
- Runtime execution of an Orientation;
- Gateway execution;
- reports or continuations;
- LYRA;
- SIRIUS;
- persistence, sessions, or application workflow;
- NEXAHEDRON presentation or browser behavior.

Absence is explicit. No excluded capability is simulated by the certified
proofs.

## 7. Future Boundary

```text
┌──────────────────────────────────────────────────────┐
│ Certified ORION Core                                │
│                                                      │
│ Foundation                                           │
│ Representation → Inventory → Summary → Statistics    │
│ Relations → Navigation → Orientation Map             │
│ Certification STOP: at_slice_iii_certified           │
└──────────────────────────────────────────────────────┘
                         │
                         │ explicit future boundary
                         ▼
┌──────────────────────────────────────────────────────┐
│ Future Layers                                        │
│                                                      │
│ Slice IV                                             │
│ Runtime execution                                    │
│ LYRA                                                 │
│ SIRIUS                                               │
│ Applications                                         │
│ NEXAHEDRON                                           │
└──────────────────────────────────────────────────────┘
```

The lower region is outside the certified Core assembled by this plate.

- **Slice IV** is not defined or implemented here.
- **Runtime** execution beyond the certified structural pipeline remains
  outside this baseline.
- **LYRA** remains outside deterministic structural authority.
- **SIRIUS** remains outside this execution chain.
- **Applications** may consume future accepted outputs but receive no Core
  authority.
- **NEXAHEDRON** remains the Human laboratory and presentation boundary, not a
  constructor of certified ORION artifacts.

This separation does not authorize any future implementation and does not
assign new responsibilities.

## 8. Frozen Baseline

The frozen ORION Core baseline consists conceptually of:

- the accepted Foundation ownership and authority boundaries;
- the certified Slice I Representation and Inventory path;
- the certified Slice II structural vocabulary, Summary, Statistics, and
  closure;
- the certified Slice III Relations, Navigation, and Orientation Map layers;
- every external Conformance boundary;
- the Slice II, Relations, Navigation, and Vertical Slice III certification
  gates;
- every canonical proof and replay procedure;
- every recorded frozen implementation fingerprint;
- every immutable identity, integrity, provenance, ordering, serialization,
  and STOP invariant.

The hashes remain recorded in their certification artifacts and proofs. This
plate does not duplicate them.

The baseline may be consumed by later work. It may not be silently
reinterpreted, weakened, or reopened. Any proposed change to a frozen
responsibility requires explicit architecture governance before
implementation.

## Canonical Assembly Statement

The certified ORION Core transforms one Human-confirmed source into immutable,
externally conformant structural artifacts; inventories, summarizes, and
measures their declared structure; assembles deterministic Relations,
Navigation, and an Orientation Map; and certifies the complete chain without
semantic interpretation or mutation.

The Core ends at `at_slice_iii_certified`.
