# Vertical Slice III Work Packages

- Status: Canonical work-package specification
- Implementation status: Not started
- Packages: WP12–WP25
- Governing plan: [`SLICE_III_ENGINEERING_PLAN.md`](SLICE_III_ENGINEERING_PLAN.md)

## 1. Common package requirements

Every package below must deliver:

- the exact bounded implementation named by the package;
- immutable typed objects where the package creates an artifact;
- deterministic canonical serialization;
- focused unit, integration, boundary, negative, tamper, and replay tests as
  applicable;
- one canonical deterministic proof;
- byte-identical repeated execution;
- provenance and lineage verification;
- regression of every earlier completed package and certified slice;
- implementation-level documentation;
- an explicit STOP.

No package is complete merely because its happy path executes.

## 2. Phase A — Relations

### WP12 — Relation Object and Contract

**Objective**

Make the approved Structural Relation Set and Relation declaration shapes
executable without deriving any relation.

“Contract” here means the internal immutable artifact profile approved by the
Slice III architecture. WP12 does not create or modify a Version 1 public
contract.

**Responsibilities**

- implement immutable relation-set, endpoint, relation, basis, provenance,
  lossiness, responsibility-state, and STOP objects;
- implement the exact closed Slice III vocabulary;
- implement canonical relation-type order;
- implement canonical identity inputs, integrity inputs, and serialization;
- reject fields and relation types outside the approved architecture.

**Inputs**

- approved Relations Architecture;
- certified immutable Slice II artifact profiles;
- no source payload and no candidate relations.

**Outputs**

- executable immutable Relation Object and Structural Relation Set contract;
- canonical serialization and validation of object shape only;
- WP12 object-contract fixture containing no derived relation behavior and
  explicitly marked as not externally relation-conformant.

**Dependencies**

- certified Slice II;
- frozen Slice III architecture.

**Implementation scope**

- object construction and immutability;
- exact field, enum, ordering, identity-basis, and serialization definitions;
- source-boundary and element endpoint shapes;
- candidate/conformant/certified state separation.

**Explicit non-goals**

- deriving relations;
- endpoint population from Inventory;
- external conformance;
- Navigation or Orientation Map.

**Acceptance criteria**

- every architecture-required field has one unambiguous executable form;
- the vocabulary accepts exactly six relation types;
- arbitrary and semantic relation types fail;
- canonical serialization is byte-identical under replay;
- attempted mutation fails;
- no Slice II artifact changes.

**Deterministic proof**

Construct the minimal object-contract-valid candidate Structural Relation Set
from explicit immutable test values, mark it as not externally conformant,
serialize it twice, verify identical bytes and integrity, reject one unknown
field and one unknown relation type, then:

```text
Relation Object and Contract
        ↓
Canonical candidate artifact
        ↓
STOP
```

**Regression requirements**

- all certified Slice I and II suites;
- architecture and boundary checks;
- no relation-derivation test.

**Definition of Done**

The object contract is immutable, deterministic, closed, tested, documented,
and introduces no relation behavior.

---

### WP13 — Sequential Relations

**Objective**

Derive only canonical adjacency relations from accepted Inventory ordinals.

**Responsibilities**

- create the endpoint registry from immutable Inventory elements and the exact
  source boundary;
- derive `immediately_precedes`;
- derive `immediately_follows`;
- preserve exact basis, endpoint, Inventory, Representation, and source
  lineage;
- assign deterministic relation identities and canonical order.

**Inputs**

- WP12 object contract;
- one certified immutable Inventory and its certified Slice II lineage.

**Outputs**

- immutable candidate Structural Relation Set containing endpoint declarations
  and only sequential relations.

**Dependencies**

- WP12 complete.

**Implementation scope**

- consecutive canonical ordinal pairs only;
- explicit inverse relation for each adjacent pair;
- first and final boundary behavior;
- empty and single-element sequence behavior where permitted by certified
  inputs.

**Explicit non-goals**

- source references;
- equality relations;
- declared cross-references;
- hierarchy, locator-overlap relations, Navigation, or external conformance.

**Acceptance criteria**

- every adjacent pair has exactly one relation in each direction;
- no relation skips an ordinal;
- no duplicate or out-of-range endpoint exists;
- direction and inverse pairing are exact;
- source text is never read;
- replay is byte-identical.

**Deterministic proof**

Use one certified Inventory with at least three ordered elements, recompute the
two adjacency families independently, verify exact identities, direction,
basis, order, provenance, and bytes, then:

```text
Certified Inventory
        ↓
Sequential Relation Derivation
        ↓
Immutable candidate relation set
        ↓
STOP
```

**Regression requirements**

- WP12;
- Slice I and II;
- tamper tests for changed ordinals, endpoints, direction, and skipped pairs.

**Definition of Done**

The two sequential types are complete and no non-sequential relation has been
introduced.

---

### WP14 — Structural Equality Relations

**Objective**

Add only deterministic equality relations over declared Inventory fields.

**Responsibilities**

- derive `same_element_kind`;
- derive `same_heading_level`;
- emit each unordered pair exactly once;
- preserve symmetric direction and canonical endpoint order;
- preserve exact field-and-value derivation basis.

**Inputs**

- WP13 candidate relation set;
- the same immutable certified Inventory.

**Outputs**

- immutable candidate relation set containing sequential and equality
  relations.

**Dependencies**

- WP13 complete.

**Implementation scope**

- exact equality of declared `element_kind`;
- exact equality of declared integer heading `level`;
- lower ordinal followed by element identity as symmetric endpoint order;
- ATX and Setext heading equality where levels match.

**Explicit non-goals**

- textual equality;
- topic, role, similarity, hierarchy, importance, or semantic equivalence;
- source references, declared cross-references, Navigation, or conformance.

**Acceptance criteria**

- every qualifying unordered pair occurs exactly once;
- every non-qualifying pair is absent;
- symmetric endpoints use canonical order;
- headings without an accepted level never receive a level relation;
- equal kind or level never produces any additional conclusion;
- replay is byte-identical.

**Deterministic proof**

Use a certified mixed-kind Inventory with repeated kinds and heading levels,
independently enumerate qualifying pairs, verify exact set equality, order,
basis, provenance, and bytes, then STOP after the candidate relation set.

**Regression requirements**

- WP12 and WP13;
- Slice I and II;
- negative cases for different kinds, different levels, absent levels, and
  duplicate pairs.

**Definition of Done**

Both equality types are complete and remain purely structural.

---

### WP15 — Source and Declared Cross References

**Objective**

Complete the candidate relation vocabulary with exact source references and
already-declared cross-references.

**Responsibilities**

- derive `source_reference` for every Inventory element;
- preserve `declared_cross_reference` only from accepted immutable
  declarations;
- resolve all endpoints exactly;
- preserve declared direction, declaration identity, version, integrity, and
  provenance;
- produce the complete candidate Structural Relation Set.

**Inputs**

- WP14 candidate relation set;
- exact source-boundary identity from certified Slice II lineage;
- zero or more accepted immutable declared cross-reference inputs.

**Outputs**

- complete immutable candidate Structural Relation Set containing the exact
  approved vocabulary.

**Dependencies**

- WP14 complete.

**Implementation scope**

- one element-to-source-boundary relation per element;
- zero declared cross-references for the current Markdown Profile v1 unless a
  separate accepted immutable declaration is explicitly supplied;
- rejection of unresolved, ambiguous, malformed, or undeclared references.

**Explicit non-goals**

- discovering links in Markdown, labels, URLs, or source text;
- repairing declaration direction or endpoints;
- external retrieval;
- relation conformance, Navigation, or map construction.

**Acceptance criteria**

- every element has exactly one exact source reference;
- no source payload is copied;
- absent cross-reference declarations produce zero cross-reference relations;
- accepted declarations are preserved without reinterpretation;
- unresolved or invented declarations fail the candidate set;
- replay is byte-identical.

**Deterministic proof**

Run two fixtures:

1. current Profile v1 with empty declared-reference input;
2. a bounded accepted declaration fixture with resolvable endpoints.

Verify exact source-reference coverage, declaration preservation, lineage,
order, identity, integrity, and rejection of one undeclared reference, then:

```text
WP14 relation set
        ↓
Source and declared-reference completion
        ↓
Complete candidate Structural Relation Set
        ↓
STOP
```

**Regression requirements**

- WP12–WP14;
- Slice I and II;
- negative cases for missing source boundary, unresolved endpoint, changed
  declaration integrity, and inferred link attempts.

**Definition of Done**

The complete candidate relation vocabulary exists without inference.

---

### WP16 — External Relation Conformance

**Objective**

Externally verify a complete candidate Structural Relation Set without
constructing, repairing, or partially accepting it.

**Responsibilities**

- implement the separate Relation Conformance validator profile;
- replay every permitted relation from exact immutable inputs;
- verify vocabulary, endpoints, basis, direction, symmetric ordering,
  canonical relation ordering, contiguous ordinals, identities, integrity,
  provenance, declared lossiness, and exclusions;
- reject the relation set atomically on any failure.

**Inputs**

- complete WP15 candidate Structural Relation Set;
- its exact certified Slice II inputs;
- accepted declared-reference inputs, if any;
- frozen Relations Architecture.

**Outputs**

- immutable external Relation Conformance result;
- accepted relation-set reference on success;
- deterministic rejection result on failure.

**Dependencies**

- WP15 complete.

**Implementation scope**

- positive, boundary, malformed, duplicate, reordered, tampered, and prohibited
  relation cases;
- independent identity and integrity recomputation;
- complete-set acceptance only.

**Explicit non-goals**

- changing the existing Representation Conformance implementation;
- constructing or repairing relations;
- partial acceptance;
- Navigation.

**Acceptance criteria**

- valid complete sets pass;
- missing, duplicate, reordered, malformed, prohibited, or tampered relations
  fail deterministically;
- validation outcome replay is byte-identical;
- the validator adds no relation and changes no input.

**Deterministic proof**

Validate one complete candidate twice, independently recompute its relations
and integrity, verify byte-identical acceptance, replay a canonical tamper
matrix with deterministic rejections, then STOP after the conformance result.

**Regression requirements**

- WP12–WP15;
- all earlier external-conformance regression;
- Slice I and II;
- boundary checks proving the new validator is a separate instance.

**Definition of Done**

Relation Conformance accepts exactly the canonical complete relation set and
has no construction authority.

---

### WP17 — Relations Certification

**Objective**

Certify the complete Relations phase without adding behavior.

**Responsibilities**

- replay WP12–WP16 from certified Slice II artifacts;
- verify complete vocabulary coverage and exclusions;
- verify independent recomputation, immutable artifacts, exact lineage,
  byte-identical replay, regression, and STOP;
- create the canonical Relations Certification record.

**Inputs**

- all WP12–WP16 artifacts, tests, proofs, and documentation.

**Outputs**

- immutable Relations Certification record;
- passed or failed Relations Certification Gate.

**Dependencies**

- WP16 complete.

**Implementation scope**

- certification, consolidation, and proof replay only.

**Explicit non-goals**

- new relation types;
- Navigation Object or traversal;
- changes to any earlier package.

**Acceptance criteria**

- WP12–WP16 each satisfy their Definition of Done;
- the complete accepted Structural Relation Set independently recomputes
  byte-identically;
- every relation resolves to an exact accepted basis;
- all regressions and frozen-boundary checks pass;
- execution stops before Navigation.

**Deterministic proof**

```text
Certified Slice II artifacts
        ↓
Complete candidate Structural Relation Set
        ↓
External Relation Conformance
        ↓
Relations Certification
        ↓
STOP
```

**Regression requirements**

- full repository verification required by the development baseline;
- every certified Slice I and II proof;
- WP12–WP16 proof replay.

**Definition of Done**

The Relations Certification Gate is recorded as passed. Otherwise Phase B is
blocked.

## 3. Phase B — Navigation

### WP18 — Navigation Object

**Objective**

Make the approved immutable Navigation Object executable without performing
traversal.

**Responsibilities**

- implement immutable Navigation envelope, relation catalog, address index,
  transition, unavailable transition, blocker, policy, provenance, integrity,
  and STOP objects;
- implement exact entry-point and action vocabularies;
- implement canonical identity inputs, ordering, and serialization.

**Inputs**

- frozen Navigation Architecture;
- certified Structural Relation Set profile;
- no traversal request.

**Outputs**

- executable immutable Navigation Object contract;
- canonical minimal object-contract fixture explicitly marked as not
  externally navigation-conformant.

**Dependencies**

- passed Relations Certification Gate.

**Implementation scope**

- object shapes, enums, immutability, serialization, and closed vocabularies;
- relation catalog preserved without alteration.

**Explicit non-goals**

- populating transitions;
- executing or selecting movement;
- Navigation Conformance;
- Orientation Map.

**Acceptance criteria**

- all required fields have one executable form;
- unknown actions, blockers, and fields fail;
- relation catalog cannot be changed;
- serialization and integrity replay byte-identically;
- no persistent cursor, history, ranking, or recommendation exists.

**Deterministic proof**

Construct and replay the minimal object-contract-valid Navigation candidate
from explicit certified relation references, mark it as not externally
conformant, verify immutability and closed vocabularies, then STOP after the
object contract.

**Regression requirements**

- Relations certification;
- Slice I and II;
- no traversal test.

**Definition of Done**

The Navigation Object contract is executable without Navigation behavior.

---

### WP19 — Deterministic Traversal

**Objective**

Construct the complete candidate Navigation Object from one certified
Structural Relation Set.

**Responsibilities**

- establish the canonical document origin;
- create the exact address index;
- expose identity, ordinal, exact-locator, relation, and source-boundary entry
  points;
- construct available transitions for the approved actions;
- construct required unavailable transitions and canonical blockers;
- preserve relation direction and relation catalog unchanged.

**Inputs**

- WP18 object contract;
- one certified immutable Structural Relation Set.

**Outputs**

- complete immutable candidate Navigation Object.

**Dependencies**

- WP18 complete.

**Implementation scope**

- `open_origin`;
- `resolve_identity`;
- `resolve_ordinal`;
- `resolve_locator`;
- `next`;
- `previous`;
- `follow_relation`;
- `inspect_source_reference`;
- `return_to_origin`;
- explicit unavailable hierarchy and undeclared-reference cases.

**Explicit non-goals**

- route choice, ranking, recommendation, search, inference, history, cursor
  persistence, UI navigation, or map construction.

**Acceptance criteria**

- every available movement cites an exact accepted relation or canonical
  origin;
- every target resolves exactly;
- direction and symmetric traversal behavior are correct;
- locator resolution uses exact equality only;
- unavailable movement has the exact deterministic blocker;
- relation bytes remain unchanged;
- repeated construction is byte-identical.

**Deterministic proof**

Resolve every entry-point class and exercise every available action against one
certified relation set, verify the complete ordered transition declarations
and blockers independently, serialize twice, then:

```text
Certified Structural Relation Set
        ↓
Deterministic Navigation construction
        ↓
Candidate Navigation Object
        ↓
STOP
```

**Regression requirements**

- WP18 and certified Relations;
- Slice I and II;
- negative cases for missing endpoints, exact-locator misses, forbidden
  direction, unavailable hierarchy, and absent cross-reference.

**Definition of Done**

All and only approved deterministic movements are represented without route
selection.

---

### WP20 — External Navigation Conformance

**Objective**

Externally verify the candidate Navigation Object.

**Responsibilities**

- replay origin, address index, relation catalog, actions, transitions,
  direction, blockers, identity, ordering, provenance, integrity, and
  serialization;
- reject malformed or incomplete Navigation atomically.

**Inputs**

- WP19 candidate Navigation Object;
- exact certified Structural Relation Set;
- frozen Navigation policy.

**Outputs**

- immutable external Navigation Conformance result.

**Dependencies**

- WP19 complete.

**Implementation scope**

- positive, missing, duplicate, reordered, redirected, malformed, semantic,
  ranked, session, and tamper cases;
- independent recomputation.

**Explicit non-goals**

- executing Navigation for a Human;
- repairing or adding transitions;
- modifying Relations;
- constructing a map.

**Acceptance criteria**

- canonical Navigation passes;
- every malformed, missing, invented, reversed, ranked, or stateful field
  fails deterministically;
- acceptance and rejection replay byte-identically;
- validation leaves all inputs unchanged.

**Deterministic proof**

Validate the complete candidate twice, independently recompute transitions and
integrity, replay the canonical tamper matrix, then STOP after the immutable
conformance result.

**Regression requirements**

- WP18–WP19;
- certified Relations;
- all prior conformance and Slice I/II checks.

**Definition of Done**

Navigation Conformance accepts exactly the canonical Navigation Object and
owns no traversal behavior.

---

### WP21 — Navigation Certification

**Objective**

Certify the complete Navigation phase without adding capability.

**Responsibilities**

- replay WP18–WP20;
- verify all entry points, actions, blockers, direction, immutability,
  provenance, independent recomputation, and regression;
- create the canonical Navigation Certification record.

**Inputs**

- all WP18–WP20 artifacts, tests, proofs, and documentation.

**Outputs**

- immutable Navigation Certification record;
- passed or failed Navigation Certification Gate.

**Dependencies**

- WP20 complete.

**Implementation scope**

- certification only.

**Explicit non-goals**

- new actions;
- Orientation Map object or construction;
- changes to Relations.

**Acceptance criteria**

- WP18–WP20 satisfy their Definition of Done;
- the accepted Navigation Object recomputes byte-identically;
- all relation references and transitions remain traceable;
- all regressions pass;
- execution stops before Orientation Map.

**Deterministic proof**

```text
Certified Structural Relation Set
        ↓
Candidate Navigation Object
        ↓
External Navigation Conformance
        ↓
Navigation Certification
        ↓
STOP
```

**Regression requirements**

- full development-baseline verification;
- certified Relations and all earlier slices;
- WP18–WP20 proof replay.

**Definition of Done**

The Navigation Certification Gate is recorded as passed. Otherwise Phase C is
blocked.

## 4. Phase C — Orientation Map

### WP22 — Orientation Map Object

**Objective**

Make the approved immutable Orientation Map object executable without
constructing a map.

**Responsibilities**

- implement immutable map envelope, node, edge, transition, unavailable
  transition, provenance, lossiness, integrity, and STOP objects;
- implement element-node and source-boundary-node classes;
- implement canonical identity inputs, ordering, versioning, and UTF-8 JSON
  serialization.

**Inputs**

- frozen Orientation Map Architecture;
- certified Navigation Object profile;
- no map construction.

**Outputs**

- executable immutable Orientation Map contract;
- canonical minimal object-contract fixture explicitly marked as not
  externally map-conformant.

**Dependencies**

- passed Navigation Certification Gate.

**Implementation scope**

- exact object shapes and canonical serialization;
- explicit absence of layout and presentation fields.

**Explicit non-goals**

- creating nodes or edges from inputs;
- layout, coordinates, visualization, storage, or Map Conformance.

**Acceptance criteria**

- required fields and node/edge classes are executable and closed;
- unknown, semantic, ranking, layout, and storage fields fail;
- mutation fails;
- serialization and integrity replay byte-identically.

**Deterministic proof**

Construct and replay the minimal object-contract-valid map candidate from
explicit certified references, mark it as not externally conformant, verify
excluded fields and immutability, then STOP after the object contract.

**Regression requirements**

- Navigation certification;
- certified Relations and Slice I/II;
- no map-construction test.

**Definition of Done**

The Orientation Map contract is executable without derived-view behavior.

---

### WP23 — Deterministic Map Construction

**Objective**

Construct one complete immutable candidate Orientation Map exclusively from
one certified Navigation Object.

**Responsibilities**

- copy every accepted endpoint into exactly one map node;
- copy every validated relation into exactly one map edge;
- copy every available and required unavailable Navigation transition;
- preserve origin, identity, order, direction, basis, blockers, provenance,
  lossiness, integrity, and STOP;
- assign deterministic map identity and version.

**Inputs**

- WP22 object contract;
- one certified immutable Navigation Object and its preserved relation catalog.

**Outputs**

- complete immutable candidate Orientation Map.

**Dependencies**

- WP22 complete.

**Implementation scope**

- one-to-one deterministic derived-view construction;
- canonical node, edge, transition, provenance, lossiness, and serialization
  order.

**Explicit non-goals**

- source access;
- relation derivation;
- traversal execution;
- filtering, grouping, clustering, layout, coordinates, diagrams, storage, or
  presentation.

**Acceptance criteria**

- every accepted endpoint appears exactly once;
- every relation and transition appears exactly once and unchanged;
- the source-boundary node is last;
- all ordering and references are exact;
- no input is omitted, merged, reversed, relabeled, or mutated;
- replay is byte-identical.

**Deterministic proof**

Construct a map twice from one certified Navigation Object, independently
compare node, edge, transition, blocker, lineage, and integrity coverage, then:

```text
Certified Navigation Object
        ↓
Deterministic derived-view construction
        ↓
Candidate Orientation Map
        ↓
STOP
```

**Regression requirements**

- WP22 and Navigation certification;
- certified Relations and Slice I/II;
- negative cases for duplicate, omitted, reordered, reversed, relabeled, or
  layout-bearing data.

**Definition of Done**

The complete candidate map is a faithful immutable derived view and nothing
else.

---

### WP24 — External Map Conformance

**Objective**

Externally verify the complete candidate Orientation Map.

**Responsibilities**

- replay map profile, nodes, edges, transitions, blockers, origin, identity,
  version, ordering, provenance, lossiness, integrity, serialization, and
  STOP;
- enforce one-to-one coverage of certified Navigation;
- reject the map atomically on any discrepancy.

**Inputs**

- WP23 candidate Orientation Map;
- exact certified Navigation Object and preserved relation catalog.

**Outputs**

- immutable external Map Conformance result;
- accepted Orientation Map reference on success.

**Dependencies**

- WP23 complete.

**Implementation scope**

- positive, missing, duplicate, reordered, redirected, malformed, semantic,
  ranked, layout, storage, and tamper cases;
- independent recomputation.

**Explicit non-goals**

- repairing maps;
- rendering or displaying a map;
- graph persistence;
- Slice IV behavior.

**Acceptance criteria**

- canonical map passes;
- every omitted, duplicated, reordered, altered, semantic, layout, storage,
  or tampered field fails deterministically;
- conformance replay is byte-identical;
- input Navigation and Relations remain unchanged;
- explicit Slice III STOP is present.

**Deterministic proof**

Validate the map twice, independently recompute all coverage and integrity,
replay the canonical tamper matrix, verify the STOP, then terminate after the
immutable conformance result.

**Regression requirements**

- WP22–WP23;
- Navigation and Relations certifications;
- all earlier conformance and Slice I/II checks.

**Definition of Done**

Map Conformance accepts exactly the canonical Orientation Map. The Orientation
Map Certification Gate may then be evaluated.

---

### WP25 — Vertical Slice III Certification

**Objective**

Certify and close Vertical Slice III without adding functionality.

**Responsibilities**

- replay the complete chain from certified Slice II artifacts through accepted
  Orientation Map Conformance;
- verify all package, phase, architecture, ownership, provenance, immutability,
  determinism, regression, and STOP requirements;
- create the canonical Slice III Certification record;
- update implementation status only after successful certification.

**Inputs**

- WP12–WP24 artifacts, proofs, tests, documentation, and phase certifications;
- certified Slice I and II baselines.

**Outputs**

- immutable Vertical Slice III Certification record;
- passed or failed Slice III Certification Gate.

**Dependencies**

- passed Orientation Map Certification Gate after WP24.

**Implementation scope**

- certification, proof replay, and closeout only.

**Explicit non-goals**

- any new relation, action, map field, presentation, Runtime behavior, public
  interface, or Slice IV capability.

**Acceptance criteria**

- every package Definition of Done is satisfied;
- all four certification gates pass in order;
- every canonical artifact independently recomputes byte-identically;
- exact lineage resolves from map to certified Slice II source boundary;
- all negative matrices reject deterministically;
- all frozen-boundary and regression checks pass;
- execution stops after accepted Map Conformance;
- no downstream component executes.

**Deterministic proof**

```text
Certified Slice II STOP
        ↓
Structural Relation Set
        ↓
External Relation Conformance
        ↓
Relations Certification
        ↓
Navigation Object
        ↓
External Navigation Conformance
        ↓
Navigation Certification
        ↓
Orientation Map
        ↓
External Map Conformance
        ↓
Vertical Slice III Certification
        ↓
STOP
```

Run the canonical proof and an independent replay from the same immutable
inputs. All canonical artifacts, validation results, and certification records
must be byte-identical.

**Regression requirements**

- full repository verification suite;
- every certified Slice I and II proof;
- every WP12–WP24 focused and proof suite;
- architecture, public-boundary, frozen-file, link, and diff checks.

**Definition of Done**

Vertical Slice III is recorded as certified complete only if every criterion
passes. Otherwise certification fails with exact blockers and the slice remains
incomplete.

## 5. Work-package status table

| Package | Capability | Status |
|---|---|---|
| WP12 | Relation Object and Contract | Not started |
| WP13 | Sequential Relations | Not started |
| WP14 | Structural Equality Relations | Not started |
| WP15 | Source and Declared Cross References | Not started |
| WP16 | External Relation Conformance | Not started |
| WP17 | Relations Certification | Not started |
| WP18 | Navigation Object | Not started |
| WP19 | Deterministic Traversal | Not started |
| WP20 | External Navigation Conformance | Not started |
| WP21 | Navigation Certification | Not started |
| WP22 | Orientation Map Object | Not started |
| WP23 | Deterministic Map Construction | Not started |
| WP24 | External Map Conformance | Not started |
| WP25 | Vertical Slice III Certification | Not started |

No package may be marked complete without implementation, focused tests,
canonical proof, replay, regression, documentation, and its declared STOP.
