# Vertical Slice IV — Execution Chain

Status: Canonical architecture
Implementation status: Not started
Scope: Deterministic transition from certified Core to Expression

## 1. Starting Chain

Slice IV inherits, but does not reopen, the certified Core:

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
Relations
        ↓
Relations Certification
        ↓
Navigation
        ↓
Navigation Certification
        ↓
Orientation Map
        ↓
External Orientation Map Conformance
        ↓
Vertical Slice III Certification
        ↓
at_slice_iii_certified
        ↓
STOP
```

No Core component executes again when Slice IV begins.

## 2. Slice IV Transition

The architectural transition is:

```text
Passed Vertical Slice III Certification
        +
Exact accepted Orientation Map artifacts
        ↓
Expression input gate
        ↓
Faithful Expression
        ↓
External Expression Conformance
        ↓
Future Slice IV Certification
        ↓
Slice IV STOP
```

The names of future implementation contracts, artifacts, schemas, versions,
proofs, and STOP identifiers are intentionally undefined.

## 3. Transition Responsibilities

### Certified Core → Expression input gate

The gate verifies that the supplied final certification passed and that the
supplied Map artifacts are the exact accepted artifacts named by that
certification.

The gate does not validate the Map again. It observes the accepted WP24 result.

### Expression input gate → Faithful Expression

Expression receives immutable certified information read-only. It may change
communicative form only under declared scope and fidelity constraints.

It performs no Core operation.

### Faithful Expression → External Expression Conformance

Conformance must compare the expression with its exact certified inputs outside
the responsibility that produced it.

Conformance must not repair, normalize, complete, or reinterpret the
expression.

### External Expression Conformance → Future Slice IV Certification

A future certification may verify only:

- deterministic replay;
- immutable inputs and outputs;
- stable identity and canonical serialization;
- provenance continuity;
- accepted conformance;
- frozen responsibilities;
- the final Slice IV STOP.

Certification may add no communicative content or behavior.

This document defines the architectural transition only. It creates no
certification or implementation.

## 4. Repeated Cross-Layer Pattern

Slice IV continues:

```text
Contract
        ↓
Construction
        ↓
External Conformance
        ↓
Certification
```

The pattern remains sufficient because Expression changes form without
changing authority:

| Stage | Slice IV responsibility | Exclusion |
|---|---|---|
| Contract | Bound permitted certified inputs, scope, fidelity, provenance, and declared lossiness | No format or implementation in this architecture phase |
| Construction | Produce a faithful communicable expression | No inference, repair, decision, or action |
| External Conformance | Verify exact fidelity to certified inputs | No construction or interpretation |
| Certification | Verify replay and frozen boundaries | No new content or downstream execution |

No additional layer or architectural principle is required.

## 5. Deterministic Conditions

A conforming future execution must depend only on:

- exact canonical certified input bytes;
- explicit Expression scope;
- explicit language or other communicative constraints already authorized by
  the Expression Contract;
- explicit declared lossiness.

It must not depend on:

- time;
- randomness;
- locale unless explicitly constrained;
- provider output;
- hidden prompts;
- hidden state;
- user profiling;
- external search;
- mutable caches;
- application presentation state.

Equal canonical inputs and equal declared constraints must produce equal
canonical output.

## 6. Failure Conditions

Expression must not begin when:

- Slice III Certification did not pass;
- the final certification is malformed;
- an Orientation Map artifact is missing;
- WP24 did not accept the exact supplied Map artifacts;
- supplied references do not resolve to one certified lineage;
- required provenance is absent;
- the requested communicative scope requires unavailable or excluded
  information;
- fidelity cannot be preserved.

Failure must not trigger repair, reconstruction, retrieval, interpretation, or
fallback output.

## 7. Closing Boundary

Slice IV ends after faithful Expression has been externally verified and, in a
future implementation, certified under the existing cross-layer pattern.

Nothing after that boundary is part of Slice IV:

- SIRIUS;
- Runtime integration;
- application behavior;
- NEXAHEDRON presentation;
- Human interpretation or action.

## 8. Execution Invariant

> The Expression chain may change how certified Orientation is communicated.
> It may not change what the certified Core established, what it left unknown,
> or who owns interpretation.
