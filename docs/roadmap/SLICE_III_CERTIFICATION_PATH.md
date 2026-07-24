# Vertical Slice III Certification Path

- Status: Canonical certification plan
- Implementation status: Not started
- Scope: Relations, Navigation, Orientation Map, and Slice III closeout

## 1. Purpose

This document defines the gates that control movement between Slice III
engineering phases.

Certification is not artifact construction, conformance validation, or feature
development. It is the independent, reproducible decision that a completed
phase satisfies its frozen responsibility and may become an immutable
dependency of the next phase.

## 2. Gate rules

Every gate must:

- consume only completed package artifacts, conformance results, tests,
  proofs, and implementation documentation;
- independently replay the phase from exact immutable inputs;
- compare canonical bytes, identities, versions, integrity, ordering,
  provenance, lossiness, responsibility states, and STOP;
- verify all positive, negative, malformed, and tamper cases;
- replay all earlier certified slices and phases;
- verify frozen ownership and responsibility boundaries;
- produce one immutable pass-or-fail certification record;
- fail closed with exact blockers.

A gate must never:

- construct or repair the artifact it certifies;
- waive a failed test or missing proof;
- partially certify a phase;
- change architecture or artifact semantics;
- allow the next phase to begin conditionally.

## 3. Canonical certification record

Every gate record must contain:

- certification identity, version, and integrity;
- gate identity and version;
- status: `passed` or `failed`;
- exact input artifact identities, versions, and integrity;
- exact conformance-result identities and integrity;
- exact proof and replay identities;
- test and regression result references;
- boundary-verification result;
- immutable-file and ownership-verification result;
- canonical byte-comparison result;
- deterministic recomputation result;
- known external issue references that do not affect the gate;
- exact blocker list when failed;
- certified STOP identity;
- provenance;
- canonical serialization information.

The record contains results and references. It does not copy source content or
become authority for earlier artifacts.

## 4. Gate R — Relations Certification

**Entry requirements**

- WP12 through WP16 are complete;
- the complete candidate Structural Relation Set exists;
- External Relation Conformance has accepted that exact set;
- all focused and phase regressions are green.

**Required verification**

- relation vocabulary is exactly closed;
- every endpoint resolves to the accepted registry;
- sequential, equality, source, and declared-reference coverage is complete;
- every relation basis independently recomputes;
- direction, symmetric endpoint order, canonical relation order, and ordinals
  are exact;
- duplicates, malformed relations, unresolved references, prohibited
  hierarchy, semantic relations, and inferred relations reject;
- source, Representation, Inventory, Summary, and Statistics lineage resolves;
- relation set, conformance result, and proof replay byte-identically;
- execution stops before Navigation.

**Canonical proof**

```text
Certified Slice II STOP
        ↓
Complete candidate Structural Relation Set
        ↓
External Relation Conformance
        ↓
Independent relation recomputation
        ↓
Byte-identical Relations proof replay
        ↓
Relations Certification
        ↓
STOP
```

**Pass condition**

Every required check passes with no exception or waiver.

**Failure consequence**

Phase B remains blocked. The failed record identifies the exact WP12–WP16
defect; no Navigation work begins.

## 5. Gate N — Navigation Certification

**Entry requirements**

- Gate R passed;
- WP18 through WP20 are complete;
- External Navigation Conformance accepted the exact Navigation Object;
- all focused and phase regressions are green.

**Required verification**

- canonical origin is exact;
- address index preserves endpoint order;
- relation catalog is byte-faithfully preserved;
- every entry point resolves deterministically;
- every available transition cites an accepted relation or origin;
- action-to-relation compatibility and direction are exact;
- locator resolution uses exact declared locators only;
- required unavailable transitions contain exact blockers;
- missing, reversed, invented, ranked, recommended, semantic, stateful, and
  persistent behavior rejects;
- Navigation Object, conformance result, and proof replay byte-identically;
- certified Relations and Slice II remain unchanged;
- execution stops before Orientation Map.

**Canonical proof**

```text
Relations Certification
        ↓
Candidate Navigation Object
        ↓
External Navigation Conformance
        ↓
Independent transition recomputation
        ↓
Byte-identical Navigation proof replay
        ↓
Navigation Certification
        ↓
STOP
```

**Pass condition**

Every required check passes and the Relations certification remains valid.

**Failure consequence**

Phase C remains blocked. No Orientation Map object or construction work begins.

## 6. Gate M — Orientation Map Certification

**Entry requirements**

- Gate N passed;
- WP22 through WP24 are complete;
- External Map Conformance accepted the exact Orientation Map;
- all focused and phase regressions are green.

**Required verification**

- one node exists per accepted endpoint;
- one edge exists per accepted relation;
- one map transition exists per accepted Navigation transition;
- unavailable transitions and blockers are preserved;
- origin, direction, identity, order, provenance, lossiness, and lineage are
  exact;
- no endpoint, edge, or transition is omitted, duplicated, merged, reversed,
  relabeled, or filtered;
- semantic, ranking, recommendation, layout, coordinate, storage, and
  presentation fields reject;
- canonical UTF-8 JSON, identity, version, and integrity independently replay;
- Map, conformance result, and proof are byte-identical;
- Navigation, Relations, and Slice II artifacts remain unchanged;
- explicit `after_orientation_map` STOP is present.

**Canonical proof**

```text
Navigation Certification
        ↓
Candidate Orientation Map
        ↓
External Map Conformance
        ↓
Independent one-to-one coverage recomputation
        ↓
Byte-identical Map proof replay
        ↓
Orientation Map Certification
        ↓
STOP
```

**Pass condition**

Every required check passes and both earlier Slice III gates remain valid.

**Failure consequence**

WP25 remains blocked. Slice III cannot be described as complete.

## 7. Gate S3 — Vertical Slice III Certification

**Entry requirements**

- Gates R, N, and M passed in order;
- WP25 closeout inputs are complete;
- all package documentation and proof artifacts are present;
- full repository regression is green.

**Required verification**

- WP12 through WP25 satisfy their Definitions of Done;
- the complete chain independently executes from certified Slice II artifacts
  to accepted Orientation Map Conformance;
- every intermediate and final artifact is immutable and source-traceable;
- two clean replays produce byte-identical artifacts, conformance results,
  phase certifications, and final certification inputs;
- all negative and tamper matrices reject deterministically;
- certified Slice I and II proofs remain byte-identical;
- architecture, ownership, responsibility, Runtime, Gateway, public-contract,
  and frozen-file checks pass;
- no source parsing, semantic interpretation, inference, ranking,
  recommendation, persistence, presentation, LYRA, SIRIUS, or Slice IV
  capability executes;
- the final execution state is exactly the Slice III STOP.

**Canonical proof**

```text
Certified Slice II STOP
        ↓
Relations
        ↓
External Relation Conformance
        ↓
Relations Certification
        ↓
Navigation
        ↓
External Navigation Conformance
        ↓
Navigation Certification
        ↓
Orientation Map
        ↓
External Map Conformance
        ↓
Orientation Map Certification
        ↓
Vertical Slice III Certification
        ↓
STOP
```

**Pass condition**

All checks pass without waiver. The certification record states:

> Vertical Slice III is certified complete.

**Failure consequence**

The record states:

> Vertical Slice III certification failed.

It lists exact blockers. Slice III remains incomplete and no downstream phase
may begin.

## 8. Replay requirements

At every gate, replay must use:

- the same immutable input bytes;
- a clean process state;
- no network;
- no clock or random input;
- no locale-dependent behavior;
- no unordered collection dependence;
- no mutable cache;
- no hidden fixture replacement;
- the exact accepted implementation and profile versions.

Byte-identical comparison covers:

- canonical artifact serialization;
- artifact identity and version;
- integrity values;
- conformance result;
- proof manifest;
- certification input manifest.

Human-readable logs need not be identity-bearing, but they must not substitute
for canonical artifacts.

## 9. Regression requirements by gate

| Gate | Focused packages | Earlier Slice III | Slice I/II | Full boundary suite |
|---|---|---|---|---|
| Relations | WP12–WP16 | None | Required | Required |
| Navigation | WP18–WP20 | Relations certification | Required | Required |
| Orientation Map | WP22–WP24 | Relations and Navigation certifications | Required | Required |
| Slice III | WP12–WP25 | All phase certifications | Required | Required |

Skipped required tests fail the gate. Expected exclusions must be asserted as
absent or rejected; they cannot be treated as untested future behavior.

## 10. Failure and correction policy

A failed gate permits only:

- correction within the already approved package responsibility;
- focused tests proving the correction;
- complete replay of the affected package and gate;
- replay of any already-certified downstream phase, if one exists.

A failure does not permit:

- broadening a relation vocabulary;
- weakening a conformance rule;
- changing an immutable input profile;
- bypassing a STOP;
- introducing an adapter, fallback, repair, or alternate execution path.

If correction requires an architecture change, implementation stops for
governance review.

## 11. Certification status

| Gate | Required packages | Current status |
|---|---|---|
| Relations Certification | WP12–WP17 | Not started |
| Navigation Certification | WP18–WP21 | Not started |
| Orientation Map Certification | WP22–WP24 | Not started |
| Vertical Slice III Certification | WP12–WP25 | Not started |

No gate has been executed or passed by the creation of this plan.
