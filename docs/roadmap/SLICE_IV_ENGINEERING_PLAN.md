# Vertical Slice IV — Engineering Plan

- Status: Canonical engineering plan
- Implementation status: Not started
- Target: Vertical Slice IV — Expression Layer
- Architecture status: Approved and frozen
- Calendar schedule: None

## 1. Purpose

This plan decomposes the approved Slice IV Expression Architecture into five
future engineering responsibilities.

It defines implementation order, dependencies, authority, stage boundaries,
and completion gates. It does not define or create an Expression format,
schema, object, implementation, proof, validator, or certification artifact.

Engineering may begin only through a separately authorized work package.

## 2. Governing Architecture

All future Slice IV work must conform to:

- [`SLICE_IV_EXPRESSION_ARCHITECTURE.md`](../architecture/SLICE_IV_EXPRESSION_ARCHITECTURE.md);
- [`SLICE_IV_RESPONSIBILITY_MATRIX.md`](../architecture/SLICE_IV_RESPONSIBILITY_MATRIX.md);
- [`SLICE_IV_BOUNDARIES.md`](../architecture/SLICE_IV_BOUNDARIES.md);
- [`SLICE_IV_EXECUTION_CHAIN.md`](../architecture/SLICE_IV_EXECUTION_CHAIN.md);
- the certified [`ORION_CORE_PLATE.md`](../architecture/ORION_CORE_PLATE.md).

Detailed package boundaries are defined in
[`SLICE_IV_WORK_PACKAGES.md`](SLICE_IV_WORK_PACKAGES.md). Gate order and
certification conditions are defined in
[`SLICE_IV_CERTIFICATION_PATH.md`](SLICE_IV_CERTIFICATION_PATH.md).

If an engineering decision cannot be derived from the frozen architecture,
work stops for review. A planning document cannot expand the architecture.

## 3. Frozen Starting Point

Slice IV begins only after:

```text
Vertical Slice III Certification
        ↓
at_slice_iii_certified
        ↓
Certified Slice III STOP
```

The minimum accepted entry set is:

1. the passed immutable Vertical Slice III Certification Report;
2. the exact immutable Orientation Map Conformance Report it references;
3. the exact immutable Orientation Map Object accepted by that report;
4. the exact immutable Constructed Orientation Map accepted by that report.

Every supplied artifact must belong to the same certified lineage. Slice IV
receives read-only access. It may not reopen, reconstruct, repair, complete,
normalize, or recertify the Core.

## 4. Engineering Decomposition

| Package | One responsibility | Required predecessor | Explicit STOP |
|---|---|---|---|
| WP26 | Establish the Expression Contract responsibility | Certified Slice III STOP and frozen Slice IV architecture | Expression Contract accepted; no construction |
| WP27 | Construct one faithful Expression under the accepted contract | WP26 complete | Candidate Expression constructed; no conformance |
| WP28 | Externally evaluate the candidate against its contract and exact certified inputs | WP27 complete | Expression Conformance decided; no certification |
| WP29 | Certify the completed Expression responsibility | WP28 accepted | Expression Layer certified; no slice closeout |
| WP30 | Certify and close Vertical Slice IV end to end | WP29 complete | Vertical Slice IV certified; STOP |

Each package owns exactly one transition. No package may absorb a predecessor's
or successor's responsibility.

## 5. Dependency Graph

```text
Certified Slice III STOP
        │
        ▼
WP26 — Expression Contract
        │
        ▼
Expression Contract Gate
        │
        ▼
WP27 — Expression Construction
        │
        ▼
Construction STOP
        │
        ▼
WP28 — External Expression Conformance
        │
        ▼
Expression Conformance Gate
        │
        ▼
WP29 — Expression Certification
        │
        ▼
Expression Certification Gate
        │
        ▼
WP30 — Vertical Slice IV Certification
        │
        ▼
Vertical Slice IV Certification Gate
        │
        ▼
STOP
```

The graph is linear and acyclic. There is no alternate path, conditional
shortcut, parallel construction authority, or implicit Runtime dependency.

## 6. Stage Responsibilities

### WP26 — Expression Contract

WP26 will establish the bounded rules under which already-certified
information may become communicable. Those rules must cover the architecture's
required concerns: accepted certified inputs, fidelity, declared scope,
provenance continuity, declared lossiness, determinism, and visible absence.

WP26 will not choose or define a schema, object model, API, presentation,
language implementation, or serialization design in this plan.

### WP27 — Expression Construction

WP27 will apply the accepted Expression Contract to the exact certified input
lineage. It will produce a candidate faithful Expression without interpreting,
repairing, ranking, enriching, or mutating certified information.

Construction cannot accept its own result as conformant or certified.

### WP28 — External Expression Conformance

WP28 will observe whether the supplied candidate satisfies the accepted
Expression Contract against the exact certified inputs. It will not construct,
repair, normalize, complete, rephrase, or replace the candidate.

Conformance decides acceptance or rejection only.

### WP29 — Expression Certification

WP29 will certify the completed Expression responsibility. It will verify that
the accepted contract, construction, and conformance stages preserve the
frozen Slice IV guarantees and are deterministically reproducible.

WP29 does not close the full vertical slice and does not introduce content.

### WP30 — Vertical Slice IV Certification

WP30 will certify the complete boundary transition from the frozen Slice III
STOP through the certified Expression Layer. It will verify cross-layer
compatibility, unchanged Core fingerprints, ordered gate completion, and the
final Slice IV STOP.

WP30 introduces no new Expression behavior.

## 7. Inputs, Outputs, and Authority

| Package | Accepted inputs | Planned output responsibility | Forbidden inputs | Forbidden outputs | Authority |
|---|---|---|---|---|---|
| WP26 | Frozen Slice IV architecture and certified Slice III entry requirements | Accepted Expression Contract | Raw source, mutable material, provider state, Runtime state | Expression content, conformance result, certification status | Bound future Expression without extending Core authority |
| WP27 | Accepted Expression Contract and exact certified Slice III lineage | Candidate faithful Expression | Raw Markdown, source text, mutable workspace material, unvalidated artifacts, hidden state | Conformance decision, certification, action | Change communicative form only |
| WP28 | Accepted contract, exact certified lineage, candidate Expression | External acceptance or rejection | Raw source, unrelated lineage, Runtime state | Repaired or replacement Expression, certification | Observe fidelity only |
| WP29 | Completed WP26–WP28 results and their immutable lineage | Expression Layer certification status | Unaccepted candidate, missing conformance, downstream state | New content, repaired artifacts, Slice IV closeout | Certify the Expression responsibility only |
| WP30 | Certified Core baseline and completed Expression certification | Vertical Slice IV certification status and final STOP | SIRIUS, Runtime, application, or Human action state | New capability or downstream authorization | Certify cross-layer completion only |

The concrete form of every future output remains an implementation-stage
decision constrained by architecture. This plan assigns responsibility without
designing artifacts.

## 8. Responsibility Matrix

| Package | Owns | Reads | Certifies | Forbidden responsibilities |
|---|---|---|---|---|
| WP26 | Expression boundary contract | Frozen Slice IV architecture and Core entry boundary | Nothing | Construction, conformance, certification, presentation |
| WP27 | Faithful Expression construction | Contract and exact certified artifacts | Nothing | Interpretation, validation, repair, certification |
| WP28 | External fidelity conformance | Contract, candidate, exact certified artifacts | Nothing; it accepts or rejects conformance | Construction, completion, certification |
| WP29 | Expression Layer certification | Contract, candidate, conformance result, lineage | Expression Layer only | Construction, conformance re-execution, slice closeout |
| WP30 | Vertical Slice IV closeout | Certified Core and certified Expression Layer | Complete Slice IV boundary | Expression content, downstream execution |

No responsibility appears in more than one owner column.

## 9. STOP Discipline

Every work package terminates before the next responsibility begins:

- WP26 stops before any Expression is constructed.
- WP27 stops before any external conformance decision.
- WP28 stops before Expression certification.
- WP29 stops before vertical-slice certification.
- WP30 stops before SIRIUS, Runtime, applications, or Human action.

A failed stage fails closed. Failure must not activate a fallback path, repair,
completion, alternate producer, or downstream stage.

## 10. Cross-Package Guarantees

Future implementation of every package must preserve:

- certified inputs only;
- immutable, read-only Core artifacts;
- fidelity to exact certified fields and declared absence;
- explicit scope and declared lossiness;
- deterministic behavior under equal canonical inputs and constraints;
- stable identity and canonical serialization where the future contract
  requires them;
- provenance continuity;
- independent conformance;
- replayability;
- no hidden inference;
- no mutation of certified artifacts;
- Human ownership of meaning, interpretation, judgment, and action.

Time, randomness, hidden prompts, external search, provider output, mutable
caches, application state, or implicit locale must not become undeclared
determinants.

## 11. Certification Gates

Slice IV uses five ordered gates:

1. **Expression Contract Gate** — the Expression responsibility is bounded
   without creating content.
2. **Construction STOP** — one candidate exists under the accepted contract;
   it is not yet accepted.
3. **Expression Conformance Gate** — the exact candidate is externally accepted
   or rejected without repair.
4. **Expression Certification Gate** — the Expression Layer is reproducible
   and its responsibilities remain frozen.
5. **Vertical Slice IV Certification Gate** — the complete transition from the
   certified Core to the final Slice IV STOP is certified.

Only a passed gate unlocks its successor. Detailed conditions are defined in
the certification path.

## 12. Definition of Done

Vertical Slice IV may be declared complete only when:

- [ ] WP26 through WP30 are individually complete in order.
- [ ] The exact certified Slice III entry lineage is preserved unchanged.
- [ ] The Expression Contract responsibility is accepted without expanding
      Core, Human, LYRA, SIRIUS, Runtime, or application authority.
- [ ] Construction produces no interpretation, semantic enrichment, decision,
      or action.
- [ ] External Conformance is independent and performs no repair or completion.
- [ ] Expression Certification verifies deterministic replay and frozen
      responsibilities without adding content.
- [ ] Vertical Slice IV Certification verifies the complete ordered chain and
      final STOP.
- [ ] All earlier certifications remain valid and unchanged.
- [ ] Provenance, explicit boundaries, declared scope, lossiness, and absence
      remain visible.
- [ ] No SIRIUS, Runtime, application, or NEXAHEDRON execution occurs.
- [ ] No downstream capability begins.

Partial acceptance, conditional certification, deferred conformance, or an
implicit fallback cannot satisfy this Definition of Done.

## 13. Explicit Non-Goals

This plan does not authorize or plan:

- schemas, object fields, formats, APIs, or serialization mechanics;
- Expression implementation;
- LYRA implementation or internals;
- visual design or rendering;
- semantic inference, interpretation, Evidence, claims, or reasoning;
- relation, Navigation, or Orientation Map changes;
- SIRIUS behavior;
- Runtime behavior or integration;
- application or NEXAHEDRON behavior;
- persistence, transport, sessions, or provider integration;
- Human decisions or actions;
- Slice V or any later capability.

## 14. Future Boundary

```text
Certified ORION Core
        ↓
Vertical Slice IV Expression
        ↓
Vertical Slice IV Certification
        ↓
STOP
════════════════════════════════════
Outside this engineering plan
════════════════════════════════════
SIRIUS
        ↓
Runtime
        ↓
Applications
        ↓
Human interpretation and action
```

The diagram preserves separation only. It does not define future behavior,
dependencies, or implementation order beyond Slice IV.

## 15. Change Control

Future engineering must classify any discrepancy before continuing:

- an implementation defect is corrected within the active package;
- a verification defect is corrected without changing canonical behavior;
- a planning ambiguity stops the package for review;
- an architecture conflict stops all affected work.

No package may silently broaden its responsibility to remove a blocker.

## 16. Canonical Closing Statement

Slice IV engineering follows the frozen Expression Architecture through five
separate responsibilities: contract, construction, external conformance,
Expression certification, and vertical-slice certification. Each stage must
finish at its own STOP before the next begins.
