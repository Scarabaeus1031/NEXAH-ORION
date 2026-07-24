# Vertical Slice III Engineering Plan

- Status: Canonical engineering plan
- Implementation status: Not started
- Target: Vertical Slice III — Relations, Navigation, and Orientation Map
- Architecture status: Approved and frozen
- Calendar schedule: None

## 1. Purpose

This plan decomposes the approved Vertical Slice III architecture into
independently verifiable engineering increments.

It authorizes no implementation by itself. A work package may begin only after
its dependencies and preceding certification gate are satisfied.

The governing rule is:

> Each package creates or verifies exactly one bounded capability, proves it
> deterministically, and stops before the next responsibility begins.

## 2. Governing specifications

Implementation must follow:

- [`Slice III Relations Architecture`](../architecture/SLICE_III_RELATIONS.md);
- [`Slice III Navigation Architecture`](../architecture/SLICE_III_NAVIGATION.md);
- [`Slice III Orientation Map Architecture`](../architecture/SLICE_III_ORIENTATION_MAP.md);
- [`Slice III Responsibility Matrix`](../architecture/SLICE_III_RESPONSIBILITY_MATRIX.md);
- [`Vertical Slices`](ORION_VERTICAL_SLICES.md).

The detailed work-package requirements are canonical in
[`SLICE_III_WORK_PACKAGES.md`](SLICE_III_WORK_PACKAGES.md). Certification and
phase-entry rules are canonical in
[`SLICE_III_CERTIFICATION_PATH.md`](SLICE_III_CERTIFICATION_PATH.md).

If this plan conflicts with the approved architecture, implementation must
stop. The plan cannot reinterpret or expand the architecture.

## 3. Frozen starting point

Slice III begins only after the certified Slice II STOP:

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
```

The following remain immutable inputs:

- confirmed source identity, revision, integrity, and boundary;
- Structural Representation identity, version, integrity, elements, locators,
  ordinals, and provenance;
- Declared Source Element Inventory identity, integrity, and order;
- Structural Summary identity and integrity;
- Structural Statistics identity and integrity;
- certified Slice II proofs and STOP.

No Slice III package may modify, repair, recreate, or enrich these artifacts.

The Slice III Relation, Navigation, and Map object contracts are internal
artifact profiles governed by the approved architecture. They are not new
Version 1 public contracts. The corresponding Slice III conformance validators
are new validator instances for new artifact profiles; they must not modify or
broaden certified Representation Conformance.

## 4. Engineering phases

### Phase A — Relations

**Goal:** Produce and externally certify the one immutable Structural Relation
Set permitted by the approved closed vocabulary.

| Package | Capability | Required predecessor | STOP |
|---|---|---|---|
| WP12 | Relation Object and Contract | Certified Slice II | Relation schema and canonical serialization |
| WP13 | Sequential Relations | WP12 | Candidate set with adjacency relations |
| WP14 | Structural Equality Relations | WP13 | Candidate set with equality relations |
| WP15 | Source and Declared Cross References | WP14 | Complete candidate Structural Relation Set |
| WP16 | External Relation Conformance | WP15 | Accepted conformance result |
| WP17 | Relations Certification | WP16 | Certified Relations STOP |

No Navigation work begins before the Relations Certification Gate passes.

### Phase B — Navigation

**Goal:** Produce and externally certify one immutable, stateless Navigation
Object over the certified Structural Relation Set.

| Package | Capability | Required predecessor | STOP |
|---|---|---|---|
| WP18 | Navigation Object | Relations Certification Gate | Navigation schema and canonical serialization |
| WP19 | Deterministic Traversal | WP18 | Candidate Navigation Object |
| WP20 | External Navigation Conformance | WP19 | Accepted conformance result |
| WP21 | Navigation Certification | WP20 | Certified Navigation STOP |

No Orientation Map work begins before the Navigation Certification Gate
passes.

### Phase C — Orientation Map

**Goal:** Produce and externally certify one immutable derived Orientation Map
from certified Navigation.

| Package | Capability | Required predecessor | STOP |
|---|---|---|---|
| WP22 | Orientation Map Object | Navigation Certification Gate | Map schema and canonical serialization |
| WP23 | Deterministic Map Construction | WP22 | Candidate Orientation Map |
| WP24 | External Map Conformance | WP23 | Accepted conformance result and Map Gate |
| WP25 | Vertical Slice III Certification | Orientation Map Certification Gate | Certified Slice III STOP |

WP25 introduces no capability. It certifies the complete chain and closes the
slice.

## 5. Dependency graph

```text
Certified Slice II STOP
        │
        ▼
WP12 Relation Object and Contract
        │
        ▼
WP13 Sequential Relations
        │
        ▼
WP14 Structural Equality Relations
        │
        ▼
WP15 Source and Declared Cross References
        │
        ▼
WP16 External Relation Conformance
        │
        ▼
WP17 Relations Certification
        │
        ▼
Relations Certification Gate
        │
        ▼
WP18 Navigation Object
        │
        ▼
WP19 Deterministic Traversal
        │
        ▼
WP20 External Navigation Conformance
        │
        ▼
WP21 Navigation Certification
        │
        ▼
Navigation Certification Gate
        │
        ▼
WP22 Orientation Map Object
        │
        ▼
WP23 Deterministic Map Construction
        │
        ▼
WP24 External Map Conformance
        │
        ▼
Orientation Map Certification Gate
        │
        ▼
WP25 Vertical Slice III Certification
        │
        ▼
Vertical Slice III Certification Gate
        │
        ▼
STOP
```

There are no optional shortcuts, parallel phase entries, or alternate paths.
Tests for a later package may not substitute for certification of an earlier
phase.

## 6. Artifact states

Every new artifact has an explicit state:

1. **Candidate** — deterministically constructed but not yet externally
   accepted.
2. **Conformant** — accepted by the corresponding external Slice III
   conformance validator.
3. **Certified** — its full phase proof, regression, boundary, replay, and
   Definition-of-Done checks have passed.

Construction code cannot mark its own output conformant. Conformance cannot
repair or complete a candidate. Certification cannot introduce fields or
behavior.

## 7. Package execution discipline

Each package must complete this cycle before the next begins:

```text
Frozen specification
        ↓
Bounded implementation
        ↓
Focused positive and negative tests
        ↓
Immutable artifact or verification result
        ↓
Deterministic proof
        ↓
Byte-identical replay
        ↓
Earlier-slice regression
        ↓
Boundary verification
        ↓
Implementation documentation
        ↓
Package STOP
```

A package is incomplete if any stage is absent, skipped, non-reproducible, or
delegated to a later package.

## 8. Cross-package invariants

Every package must preserve:

- equal canonical input bytes produce equal canonical output bytes;
- all output collections use their architecture-defined canonical order;
- all identities, versions, integrity values, and provenance are explicit;
- no output is mutated after construction;
- every derived field resolves to an accepted immutable input field;
- external validation remains outside construction authority;
- rejected input produces no partially accepted output;
- every proof terminates at its declared STOP;
- certified Slice I and II proofs remain green and byte-identical;
- Runtime, Gateway, Projection, Renderer, Representation, and UNDERSTAND
  responsibilities remain unchanged.

Forbidden determinants include clocks, randomness, locale, unordered
iteration, provider output, UI state, Human profiles, caches, retrieval, and
network state.

## 9. Regression policy

Every work package must run:

- its focused unit tests;
- its focused integration and negative tests;
- deterministic and byte-identical replay;
- immutability and tamper checks;
- provenance and lineage checks;
- all completed packages in its current phase;
- all certified Slice I and Slice II regression and proof suites;
- architecture and frozen-boundary checks;
- repository diff hygiene checks.

At certification gates, the full repository verification suite required by the
current development baseline must pass.

A failure in an earlier certified proof blocks the current package even when
the new focused tests pass.

## 10. Slice III Definition of Done

Vertical Slice III is complete only when all of the following are true:

- [ ] WP12 through WP25 are individually complete.
- [ ] The Relations, Navigation, Orientation Map, and Slice III certification
      gates have passed in order.
- [ ] The complete closed relation vocabulary is implemented without inferred
      relations.
- [ ] One externally conformant immutable Structural Relation Set exists.
- [ ] One externally conformant immutable Navigation Object exists.
- [ ] One externally conformant immutable Orientation Map exists.
- [ ] Every artifact preserves exact Slice II lineage.
- [ ] Independent recomputation produces byte-identical artifacts and
      conformance results.
- [ ] Every negative and malformed case fails deterministically without repair
      or partial acceptance.
- [ ] All Slice I and Slice II proofs replay unchanged.
- [ ] Runtime, Gateway, Projection, Renderer, Representation, existing
      Conformance, UNDERSTAND, and public contracts remain unchanged.
- [ ] No semantic, probabilistic, ranked, recommended, or inferred content is
      present.
- [ ] The canonical complete proof terminates after accepted Orientation Map
      conformance.
- [ ] The repository is regression-green and diff-clean.
- [ ] The final certification record explicitly states that Slice IV did not
      execute.

Approximate completion, partial vocabulary, skipped replay, or deferred
certification cannot satisfy this Definition of Done.

## 11. Explicit non-goals

Slice III implementation must not include:

- semantic interpretation;
- parent, child, contains, or sibling relations;
- inferred hierarchy;
- entities, concepts, claims, or Evidence;
- knowledge graphs;
- semantic similarity or clustering;
- ranking, recommendation, route choice, or relevance;
- source parsing, retrieval, search, or indexing;
- raw source storage;
- visual layout, coordinates, diagrams, or presentation;
- user sessions, history, persistence, or synchronization;
- Runtime or Gateway redesign;
- changes to public contracts;
- LYRA, SIRIUS, or LUCY;
- NTO or additional Projection mathematics;
- browser or public application work;
- Slice IV capability.

## 12. Change control

An implementation discrepancy must be classified before work continues:

- **Implementation defect:** correct within the active package.
- **Fixture or test defect:** correct without changing canonical behavior.
- **Specification ambiguity:** stop and request architecture review.
- **Architecture conflict:** stop; do not solve through implementation.

No work package may silently broaden its scope to remove a blocker.

## 13. Canonical closing statement

A Slice III capability is complete only when its one responsibility is
implemented, externally verified where required, reproducible, regression
clean, and stopped at its declared boundary. A later responsibility begins
only after the preceding certification gate has passed.
