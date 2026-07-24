# Vertical Slice IV — Certification Path

- Status: Canonical certification plan
- Implementation status: Not started
- Scope: Expression Contract, Construction, External Conformance, Expression
  Certification, and Slice IV closeout

## 1. Purpose

This document defines the ordered gates by which a future Slice IV
implementation may progress from the certified ORION Core to the final
Expression boundary.

It defines gate responsibilities and pass conditions only. It does not design
proofs, records, schemas, objects, validators, source files, or implementation.

## 2. Entry Gate — Certified Slice III

Slice IV remains closed unless:

- Vertical Slice III Certification has passed;
- the exact Orientation Map Conformance Report named by that certification is
  available;
- the exact Orientation Map Object accepted by that report is available;
- the exact Constructed Orientation Map accepted by that report is available;
- every artifact belongs to one immutable certified lineage;
- the certified Core STOP remains intact.

Failure at entry produces no Expression work and triggers no reconstruction,
repair, retrieval, or fallback.

## 3. Gate Rules

Every Slice IV gate must:

- depend only on completed predecessor responsibilities;
- observe exact immutable artifacts and their lineage;
- preserve frozen authority and ownership;
- be deterministic and independently reviewable;
- fail closed;
- leave all predecessor artifacts unchanged;
- terminate at its declared STOP.

A gate must never:

- construct a predecessor's output;
- repair, normalize, complete, or replace a failed input;
- waive a missing dependency;
- conditionally admit the next stage;
- add content, meaning, or downstream behavior;
- reopen a certified Core responsibility.

## 4. Gate 1 — Expression Contract Gate

### Precondition

- the Certified Slice III Entry Gate has passed;
- WP26 has completed its one planning-defined responsibility;
- frozen Slice IV architecture remains unchanged.

### Gate Question

Is the future Expression responsibility bounded sufficiently for construction
and external conformance to remain separate, deterministic, faithful, and
non-authoritative?

### Required Conditions

- accepted certified inputs are bounded;
- fidelity is bounded;
- communicative scope and declared lossiness are bounded;
- provenance continuity and visible absence are required;
- determinism and replayability are required;
- Human meaning, interpretation, judgment, and action remain outside;
- construction, conformance, certification, SIRIUS, Runtime, and applications
  remain outside;
- no schema, object, format, or implementation has been smuggled into planning.

### Pass Consequence

WP27 may begin under the accepted Expression Contract responsibility.

### Failure Consequence

Construction remains blocked. The boundary returns for review without creating
Expression content.

### STOP

```text
Expression Contract Gate passed
        ↓
STOP
```

## 5. Gate 2 — Construction STOP

### Precondition

- the Expression Contract Gate has passed;
- WP27 has used only one exact certified lineage and explicit authorized
  communicative constraints.

### Gate Question

Has one candidate faithful Expression been constructed without claiming
conformance, certification, interpretation, or downstream authority?

### Required Conditions

- certified identities, status, order, provenance, boundaries, and absence are
  preserved;
- declared scope and lossiness are explicit;
- no input was mutated, repaired, completed, or reordered;
- no hidden input or undeclared determinant was used;
- the candidate remains unaccepted pending external conformance.

### Pass Consequence

The exact candidate and exact input lineage may enter WP28.

### Failure Consequence

External Conformance does not begin. No partial candidate is treated as
accepted.

### STOP

```text
Candidate Expression constructed
        ↓
STOP
```

## 6. Gate 3 — Expression Conformance Gate

### Precondition

- the Construction STOP has been reached;
- WP28 has received the exact contract, candidate, and certified lineage;
- conformance remains independent from construction.

### Gate Question

Does the supplied candidate faithfully satisfy its accepted Expression
Contract against the exact certified inputs?

### Required Conditions

- fidelity is evaluated against exact certified fields;
- identity, order, status, provenance, boundaries, scope, lossiness, and
  declared absence are evaluated;
- missing, malformed, inconsistent, or unrelated inputs reject;
- no repair, normalization, completion, replacement, or rephrasing occurs;
- acceptance creates no semantic or Human authority.

### Pass Consequence

The exact accepted candidate chain may enter WP29.

### Failure Consequence

Expression Certification remains blocked. The failed candidate is not modified
and cannot advance.

### STOP

```text
External Expression Conformance accepted or rejected
        ↓
STOP
```

Only an accepted outcome opens the next gate.

## 7. Gate 4 — Expression Certification Gate

### Precondition

- the Expression Conformance Gate has accepted the exact candidate;
- WP26–WP28 are complete and unchanged;
- the certified Core lineage still resolves exactly.

### Gate Question

Is the complete Expression responsibility deterministic, immutable,
provenance-preserving, replayable, externally conformant, and confined to its
frozen authority?

### Required Conditions

- the contract, candidate, and conformance result form one exact lineage;
- repeated execution under equal canonical inputs and constraints is required
  to be byte-identical;
- all predecessor artifacts remain immutable;
- no semantic inference, interpretation, repair, or hidden determinant exists;
- Expression does not claim Core, Human, SIRIUS, Runtime, or application
  authority;
- WP29 adds no content and performs no construction or conformance repair.

### Pass Consequence

The certified Expression Layer becomes an immutable dependency of WP30.

### Failure Consequence

Vertical Slice IV cannot close. No downstream boundary may begin.

### STOP

```text
Expression Layer certified
        ↓
STOP
```

## 8. Gate 5 — Vertical Slice IV Certification Gate

### Precondition

- the Expression Certification Gate has passed;
- all WP26–WP29 responsibilities completed in order;
- the original certified Core baseline remains unchanged.

### Gate Question

Is the complete transition from `at_slice_iii_certified` through faithful,
externally conformant Expression finished, reproducible, and stopped at the
approved Slice IV boundary?

### Required Conditions

- every predecessor gate passed without waiver or alternate path;
- one exact certified Core lineage resolves through the complete Slice IV
  chain;
- Core and Slice III certifications remain valid and unchanged;
- authority, fidelity, provenance, determinism, immutability, explicit scope,
  declared lossiness, visible absence, and STOP boundaries are preserved;
- WP30 introduces no content, validation, repair, or new capability;
- SIRIUS, Runtime, applications, NEXAHEDRON behavior, and Human action have not
  executed.

### Pass Consequence

Vertical Slice IV is certified complete and becomes a frozen boundary.

### Failure Consequence

Slice IV remains uncertified. Nothing downstream may treat it as complete.

### STOP

```text
Vertical Slice IV certified
        ↓
STOP
```

## 9. Complete Certification Path

```text
Certified Slice III STOP
        ↓
Expression Contract Gate
        ↓
STOP
        ↓
Expression Construction
        ↓
STOP
        ↓
External Expression Conformance Gate
        ↓
STOP
        ↓
Expression Certification Gate
        ↓
STOP
        ↓
Vertical Slice IV Certification Gate
        ↓
Vertical Slice IV STOP
```

The intermediate STOPs are mandatory control boundaries. They do not authorize
the next stage unless the corresponding gate has passed.

## 10. Certification Separation

| Stage | Decides | Does not decide |
|---|---|---|
| Contract Gate | Whether Expression is sufficiently bounded | Whether any candidate is faithful |
| Construction STOP | Whether candidate construction has ended | Whether the candidate conforms |
| Conformance Gate | Whether the exact candidate satisfies the contract | Whether the layer or slice is certified |
| Expression Certification Gate | Whether the Expression responsibility is reproducible and frozen | Whether the full Core-to-Slice-IV transition is closed |
| Slice IV Certification Gate | Whether the complete vertical slice is certified and stopped | Any downstream behavior |

This separation prevents self-validation, self-certification, and authority
overlap.

## 11. Failure Discipline

Any failure:

- identifies the failed stage;
- leaves every accepted predecessor immutable;
- produces no partial certification;
- does not fall back to another producer or path;
- does not trigger repair, completion, reinterpretation, or downstream work;
- returns control to the owner of the failed responsibility.

Certification cannot convert an architectural ambiguity into an implementation
choice. Ambiguity stops the work for review.

## 12. Future Boundary

The final Slice IV gate ends before:

```text
SIRIUS
        ↓
Runtime
        ↓
Applications
        ↓
NEXAHEDRON presentation
        ↓
Human interpretation and action
```

These boundaries receive no behavior, work package, certification gate, or
implementation plan from this document.

## 13. Certification Closing Rule

Vertical Slice IV becomes certified only through the ordered completion of
Contract, Construction, External Conformance, Expression Certification, and
Vertical Slice Certification. Certification observes completed
responsibilities; it never creates them.
