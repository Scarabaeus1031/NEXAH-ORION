# Vertical Slice IV — Expression Architecture

Status: Canonical architecture
Implementation status: Not started
Scope: Expression Boundary after the certified ORION Core

## 1. Purpose

Vertical Slice IV defines the boundary at which certified Orientation may
become communicable without changing the authority, provenance, identity,
ordering, or deterministic structure established by the ORION Core.

**Expression** is the faithful transformation of already-certified information
into a communicable form.

Expression exists because the certified Core and a Human-facing explanation
have different responsibilities:

- the Core constructs and certifies deterministic structural Orientation;
- Expression makes that certified Orientation accessible without becoming a
  second source of truth;
- the Human interprets, accepts, rejects, or acts on what is communicated.

Slice IV solves the architectural problem of communicability. It does not solve
interpretation, decision making, action, presentation design, or Runtime
orchestration.

## 2. Starting Boundary

Slice III ends at the immutable Vertical Slice III Certification Report with:

```text
at_slice_iii_certified
```

Slice IV begins only when that gate has passed and the exact certified
Orientation Map artifacts named by the certification are available.

```text
Certified ORION Core
        ↓
Vertical Slice III Certification
        ↓
at_slice_iii_certified
════════════════════════════════════
Expression Boundary
════════════════════════════════════
        ↓
Vertical Slice IV
```

The transition grants Slice IV read-only access to certified artifacts. It
grants no authority to reopen, repair, complete, reinterpret, or supersede
them.

## 3. Accepted Inputs

The minimum accepted authority for Expression is:

1. a passed immutable Vertical Slice III Certification Report;
2. the exact immutable Orientation Map Conformance Report referenced by that
   certification;
3. the exact immutable Orientation Map Object accepted by that conformance
   report;
4. the exact immutable Constructed Orientation Map accepted by that
   conformance report.

Together, these establish:

- the final certified gate;
- the exact communicable structural content;
- the accepted status of that content;
- the complete upstream lineage by immutable reference.

Expression may consume an upstream certified artifact only when:

- the artifact is named by the accepted Slice III lineage;
- its exact field is required in the expression;
- the expression preserves its identity, status, order, provenance, and
  declared absence.

Permitted upstream artifacts are limited to the already-certified Navigation,
Relations, Structural Summary, and Structural Statistics artifacts referenced
by the certified chain.

Expression may not consume raw Markdown, source text, Projection state,
Renderer state, mutable workspace material, provider output, or unvalidated
artifacts.

## 4. Permitted Outputs

Slice IV may produce a communicable expression of certified information.

An Expression output may:

- state certified identities, labels, kinds, ordering, and boundaries;
- state certified Relations and structural adjacency;
- state certified Summary and Statistics fields;
- make provenance and exact source references visible;
- make unavailable, unknown, absent, or excluded information visible;
- use faithful Human language through LYRA;
- present a bounded view when its scope and omissions remain explicit.

An Expression output must remain traceable to the exact certified inputs from
which it was produced.

This architecture does not define an output format, schema, API, object,
renderer, visual form, or implementation.

## 5. Authority

Expression is authoritative only for this claim:

> This communication is a faithful, traceable expression of the cited
> certified ORION artifacts within its declared scope.

Expression is not authoritative for:

- the source;
- Human meaning or intention;
- semantic truth;
- interpretation;
- Evidence;
- importance or relevance;
- a preferred route;
- a decision;
- an action.

Because the certified Core establishes structure rather than semantic meaning,
Slice IV must not claim that it preserves a meaning established by ORION. It
preserves certified fields, relations, boundaries, provenance, and declared
absence. Meaning remains Human.

## 6. Expression Principles

The Expression Boundary is governed by these principles:

1. **Certified input only.** No expression begins before
   `at_slice_iii_certified`.
2. **Fidelity.** Every communicated statement resolves to certified input.
3. **No added authority.** Communicability does not create truth or meaning.
4. **No reinterpretation.** Expression may rephrase but may not change an
   identity, status, relation, order, boundary, or provenance claim.
5. **Visible absence.** Unknown, unavailable, excluded, and absent fields remain
   visible as such.
6. **Explicit scope.** A bounded expression states its scope and omissions.
7. **Determinism.** Equal certified inputs and equal declared Expression
   constraints produce equal output.
8. **Immutability.** Expression never mutates its certified inputs.
9. **Replayability.** The transformation from certified input to expression
   must be reproducible.
10. **External verifiability.** Fidelity must be verifiable outside the
    responsibility that creates the expression.
11. **Provenance continuity.** Expression preserves the complete cited lineage.
12. **Human authority.** Interpretation, acceptance, judgment, and action remain
    Human responsibilities.

No additional architectural principle is required beyond the certified Core
pattern and the already-established LYRA requirement of faithful language.

## 7. Relationship to LYRA

Slice IV is the architectural Expression responsibility.

LYRA is the canonical Human-language specialization within that responsibility.
It may faithfully translate certified fields into Human-readable language under
the existing LYRA authority boundary.

LYRA is not identical to all of Slice IV because Slice IV also defines:

- the certified input gate;
- provenance continuity;
- fidelity boundaries;
- external verifiability;
- the separation from Human interpretation and downstream action.

LYRA remains:

- non-authoritative;
- deterministic within declared inputs and language constraints;
- unable to choose routes or instruments;
- unable to infer semantics;
- unable to change certified artifacts;
- unable to replace or contradict ORION output.

The existing Human-to-ORION language role of LYRA remains unchanged. Slice IV
defines only the outward Expression boundary after the certified Core. It does
not redesign LYRA internals or add a second LYRA component.

## 8. Cross-Layer Pattern

Slice IV continues the established ORION pattern:

```text
Contract
        ↓
Construction
        ↓
External Conformance
        ↓
Certification
```

For Expression, the pattern means:

- a future Expression Contract must define fidelity, scope, provenance, and
  declared lossiness;
- future Expression construction must apply that contract without
  interpretation;
- external Expression Conformance must verify the output against the exact
  certified inputs without repair;
- future Slice IV Certification must verify determinism, replay, frozen
  responsibilities, and the closing boundary without adding behavior.

This document defines only the responsibility pattern. It creates no contract,
format, object, validator, certification artifact, proof, or work package.

## 9. Relationship to Other Boundaries

- **SIRIUS** remains outside Slice IV. It names the later position at which
  expressed orientation may enter a local access or action context. It receives
  no Expression or Core authority.
- **Runtime** remains outside this architecture definition. Runtime may not be
  designed or extended through Slice IV architecture.
- **Applications** may later present an accepted expression. Presentation does
  not gain authority to alter it.
- **NEXAHEDRON** remains the Human laboratory and presentation boundary. It may
  expose accepted expression but must not construct certified Core artifacts or
  reinterpret Expression as ORION authority.
- **Human** retains intention, interpretation, judgment, acceptance, and action.

Detailed boundaries are recorded in
[`SLICE_IV_BOUNDARIES.md`](SLICE_IV_BOUNDARIES.md).

## 10. Explicit Non-Goals

Slice IV architecture does not define or authorize:

- implementation;
- data structures or formats;
- APIs;
- Runtime behavior;
- LYRA internals;
- SIRIUS behavior;
- application or NEXAHEDRON behavior;
- semantic inference;
- interpretation;
- Evidence;
- relation or Navigation generation;
- Orientation Map construction;
- decision making;
- agent behavior;
- world models;
- visualization or presentation design;
- engineering work packages;
- proofs or certification artifacts.

## 11. Canonical Definition

Vertical Slice IV defines the certified boundary at which immutable Orientation
may become communicable without changing its authority, provenance,
deterministic structure, explicit boundaries, or Human ownership of meaning.
