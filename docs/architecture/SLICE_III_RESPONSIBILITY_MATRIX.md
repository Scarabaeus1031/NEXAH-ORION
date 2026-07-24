# Vertical Slice III — Responsibility Matrix

Status: Canonical architecture
Implementation status: Not started
Scope: Relations, Navigation, Orientation Map

## 1. Architecture overview

Vertical Slice III extends the certified Slice II boundary without reopening
it.

Slice II describes and measures immutable declared structure. Slice III makes
that structure navigable through an exact relation vocabulary and one
deterministic derived map.

The governing rule is:

> A component may consume the accepted output of the preceding responsibility,
> but it may neither repeat that responsibility nor silently perform the next
> one.

## 2. Complete responsibility matrix

| Component | One responsibility | Input | Output | Must never |
|---|---|---|---|---|
| Projection | Define the frozen source-to-structure mapping rules | Accepted CommonMark source-domain and target-profile definitions | Deterministic Projection specification and mapping contract | Execute Rendering, interpret content, create relations, navigate, or construct maps |
| Renderer | Execute and materialize the Projection mapping exactly | Human-confirmed source plus frozen Projection | Immutable Structural Representation | Add structural decisions, semantics, relations, or navigation |
| Representation | Preserve declared structure, identity, provenance, ordering, locators, and lossiness | Renderer declarations | Immutable Structural Representation artifact | Become source authority, infer relations, or execute UNDERSTAND |
| External Conformance | Validate an artifact outside the authority that constructed it | Artifact plus its exact immutable inputs and governing profile | Immutable conformance result | Construct, repair, complete, interpret, or partially accept an artifact |
| Inventory | Preserve already-declared Representation elements in canonical order | Externally conformant immutable Structural Representation | Immutable Declared Source Element Inventory | Parse source, discover structure, infer relations, summarize, or measure |
| Structural Summary | Describe exact declared organization | Immutable Inventory | Immutable Structural Summary | Read source, infer hierarchy, measure Statistics, create relations, or interpret meaning |
| Structural Statistics | Measure exact declared fields | Immutable Inventory | Immutable Structural Statistics | Read source, infer hierarchy or relations, rank, estimate, or interpret |
| Relations | Produce the exact immutable relation set permitted by the Slice III vocabulary | Certified Slice II artifact references plus accepted relation declarations | Immutable Structural Relation Set awaiting external conformance | Modify Slice II artifacts, infer hierarchy or semantics, navigate, validate itself, or map |
| Navigation | Index and expose deterministic possible movement over validated Relations | Externally conformant immutable Structural Relation Set | Immutable Navigation Object | Add, remove, reverse, rank, recommend, persist, or reinterpret relations |
| Orientation Map | Project accepted nodes, relations, and navigation boundaries into one immutable derived view | Externally conformant immutable Navigation Object | Immutable Orientation Map | Store source material, create relations, execute navigation, choose layout, or infer meaning |

Each responsibility appears exactly once.

External Conformance is one architectural responsibility instantiated for
different artifact profiles:

- Representation Conformance remains the certified Slice II validator;
- Relation Conformance validates the Structural Relation Set;
- Navigation Conformance validates the Navigation Object;
- Map Conformance validates the Orientation Map.

New validator instances do not change or broaden the certified Slice II
Representation Conformance implementation.

## 3. Complete deterministic execution chain

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
════════════════════════════════════════
Slice III boundary
════════════════════════════════════════
        ↓
Relations
        ↓
External Relation Conformance
        ↓
Navigation
        ↓
External Navigation Conformance
        ↓
Orientation Map
        ↓
External Map Conformance
        ↓
STOP
```

The abbreviated public chain is:

```text
Confirmed Markdown
        ↓
Projection
        ↓
Renderer
        ↓
Representation
        ↓
Inventory
        ↓
Structural Summary
        ↓
Structural Statistics
        ↓
Relations
        ↓
Navigation
        ↓
Orientation Map
        ↓
STOP
```

## 4. Transition definitions

### 4.1 Confirmed Markdown → Projection

One accepted Human-confirmed source enters the existing Representation
boundary. Identity, revision, integrity, and whole-source boundary are explicit.

No Slice III responsibility participates.

### 4.2 Projection → Renderer

Projection supplies the deterministic mapping already frozen for Profile v1.
Renderer executes it without adding decisions.

No relation exists yet.

### 4.3 Renderer → Representation

Renderer emits immutable declared elements with stable identities, locators,
ordinals, provenance, and integrity.

Representation remains relation-free for the current profile.

### 4.4 Representation → Inventory

External Representation Conformance succeeds first. Inventory then preserves
the exact element declarations without source access or discovery.

### 4.5 Inventory → Structural Summary

Summary derives only the certified structural synopsis. It creates no edge,
route, or map node.

### 4.6 Structural Summary → Structural Statistics

The canonical chain reaches Statistics after Summary. Both retain the same
Inventory lineage; Statistics continues to measure Inventory fields directly
as certified by Slice II.

### 4.7 Certified Slice II STOP → Relations

The Slice II artifacts are accepted as immutable inputs. Relations verifies
their identities and produces a new Slice III artifact.

Relations derives only the permitted structural relation vocabulary and
preserves any accepted declared relations. It neither changes Slice II nor
executes navigation.

### 4.8 Relations → Navigation

External Relation Conformance must succeed.

Navigation consumes the complete immutable endpoint registry and validated
edges. It creates deterministic address and transition declarations without
modifying the relation set.

### 4.9 Navigation → Orientation Map

External Navigation Conformance must succeed.

Orientation Map copies nodes, validated relation edges, available transitions,
and required unavailable transitions into one immutable derived view.

### 4.10 Orientation Map → STOP

External Map Conformance verifies identity, ordering, integrity, lineage,
boundaries, and exclusions.

Execution stops. No LYRA, SIRIUS, semantic layer, report, Runtime extension,
Gateway change, or public application follows inside Slice III.

## 5. Ownership and authority

### Human

The Human continues to own:

- source selection and confirmation;
- intention and meaning;
- the decision to navigate;
- interpretation of any map;
- acceptance of any continuation outside Slice III.

### Source and Library authority

External source ownership and Library authority remain unchanged.

Slice III stores only immutable references. It never becomes source,
editorial, Evidence, or Library authority.

### ORION

ORION owns deterministic execution of the accepted Slice III responsibilities:

- relation construction from explicit bases;
- external artifact validation;
- deterministic navigation declarations;
- Orientation Map construction.

ORION does not own Human meaning or source authority.

### NEXAHEDRON

NEXAHEDRON may later present the accepted Orientation Map and allow the Human
to request declared Navigation actions.

It must not construct relations, change Navigation, infer routes, or reinterpret
the map.

Presentation is not part of Slice III architecture implementation.

## 6. Determinism invariants

Every Slice III artifact must preserve:

- exact input identities and versions;
- source revision and integrity;
- Representation identity, version, and integrity;
- Inventory integrity;
- canonical endpoint identities and order;
- exact relation basis and direction;
- deterministic identity and serialization;
- declared lossiness;
- complete provenance;
- explicit responsibility and STOP.

The following inputs are forbidden:

- time;
- randomness;
- locale;
- unordered iteration;
- provider output;
- UI state;
- Human profile;
- hidden cache state;
- external search or retrieval.

Equal canonical input bytes must produce equal canonical output bytes.

## 7. Boundary matrix

| Capability | Slice III status | Reason |
|---|---|---|
| Deterministic structural relations | Included | Exact declared fields provide the complete basis |
| Accepted declared cross-references | Included when present | They already exist and are preserved, not discovered |
| Previous and next navigation | Included | Exact inverse ordinal relations exist |
| Identity, ordinal, locator resolution | Included | Exact accepted references exist |
| Explicit unavailable hierarchy | Included | Makes the profile boundary visible without inventing hierarchy |
| Immutable structural Orientation Map | Included | Derived directly from Relations and Navigation |
| Parent, child, contains, sibling | Excluded | Profile v1 declares no hierarchy |
| Semantic relation inference | Excluded | Requires meaning beyond structural declarations |
| Knowledge graph | Excluded | Requires entities, concepts, or semantic edges |
| AI interpretation | Excluded | Non-deterministic and outside structural authority |
| Ranking or recommendation | Excluded | Chooses a route rather than exposing declared movement |
| Evidence and claims | Excluded | Belong to a future semantic/evidence responsibility |
| Search and retrieval | Excluded | Introduce external information |
| Visual layout | Excluded | Presentation is not canonical map structure |
| Session history and persistence | Excluded | Navigation Object is immutable and stateless |
| Runtime or Gateway redesign | Excluded | Certified boundaries remain unchanged |
| LYRA and SIRIUS | Excluded | Expression and downstream behavior begin after this slice |

## 8. Cross-document consistency

The canonical Slice III architecture consists of:

- [`SLICE_III_RELATIONS.md`](SLICE_III_RELATIONS.md);
- [`SLICE_III_NAVIGATION.md`](SLICE_III_NAVIGATION.md);
- [`SLICE_III_ORIENTATION_MAP.md`](SLICE_III_ORIENTATION_MAP.md);
- this responsibility matrix.

If a future implementation choice conflicts with these documents, execution
must stop for architecture review. Implementation may not resolve ambiguity by
granting a component additional responsibility.

## 9. Architecture acceptance

Slice III architecture is internally complete only when:

- the relation vocabulary is exact and closed;
- structural, declared, and inferred relation classes are unambiguous;
- every artifact has one owner and one responsibility;
- Navigation consumes Relations without mutation;
- Orientation Map remains a derived view;
- all identities, order, integrity, provenance, and serialization rules are
  deterministic;
- hierarchical and semantic boundaries remain explicit;
- every Slice II artifact and responsibility remains unchanged;
- implementation remains not started.

At this checkpoint, those conditions are satisfied at specification level
only. No executable Slice III artifact exists.
