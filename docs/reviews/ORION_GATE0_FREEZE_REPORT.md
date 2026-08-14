# ORION Version 1.1 — Gate 0 Freeze Report

Status: Contract freeze complete
Decision: **READY FOR GATE 0**
Implementation performed: No
Deployment performed: No
Frozen ORION Core modified: No

## 1. Purpose

This report records the normative closure of the architectural blockers
identified by `ORION_V1_1_ARCHITECTURE_GATE.md`.

The contracts define what Gate 0 must verify. They do not claim that the
verification has already occurred.

## 2. Frozen contracts

### 2.1 Certified Slice II–IV Invocation Contract

Frozen in:
`docs/architecture/runtime/ORION_SLICE_EXECUTION_CONTRACT.md`

It fixes:

- the frozen Core commit and fingerprint;
- the only accepted inputs;
- the exact Confirmed Material mapping;
- 31 callable stages and their order;
- required intermediate outcomes;
- fixed Expression declarations;
- the terminal Slice IV Certification;
- failure, immutability, and replay requirements;
- exclusion of the historical Runtime and Gateway.

### 2.2 Identity Contract

Frozen in:
`docs/architecture/runtime/ORION_IDENTITY_CONTRACT.md`

It separates:

- Contract Request ID;
- Deterministic Request Digest;
- Deterministic Result Digest;
- Operational Execution ID.

It fixes canonical serialization, permitted locations, forbidden uses, retry,
replay, and error behavior.

### 2.3 Confirmed Material Contract

Frozen in:
`docs/architecture/runtime/ORION_CONFIRMED_MATERIAL_CONTRACT.md`

It fixes:

- wire schema `orion.confirmed-material/1.0`;
- exact fields and versions;
- CommonMark `0.31.2`;
- canonical UTF-8 representation;
- content integrity;
- the Core-compatible confirmation identity basis;
- exact mapping to `ConfirmedMarkdownSource`;
- input and post-projection bounds;
- deterministic rejection.

The internal NEXAHEDRON
`orion.confirmed-local-source/0.1-alpha` artifact is not the public wire
contract. No implicit Alpha compatibility remains.

### 2.4 Artifact Manifest Contract

Frozen in:
`docs/architecture/runtime/ORION_ARTIFACT_MANIFEST_CONTRACT.md`

It fixes:

- self-contained embedded artifacts;
- exactly 22 ordered entries;
- each frozen serializer;
- identity, integrity, reference, and terminal checks;
- response and manifest limits;
- authentication and privacy boundaries;
- rejection of partial or altered chains.

### 2.5 Clarification Lineage Contract

Frozen in:
`docs/architecture/runtime/ORION_CLARIFICATION_CONTRACT.md`

It fixes:

- stateless carried lineage;
- alternating request/result closure;
- canonical oldest-to-newest order;
- unique identity-version pairs;
- maximum depth `8`;
- maximum lineage size `1,000,000` bytes;
- Human reconfirmation after material changes;
- `422` for invalid lineage;
- no use of `409` for missing lineage;
- no Version 1.1 generation of Clarification Results.

### 2.6 Operational Boundary Contract

Frozen in:
`docs/architecture/runtime/ORION_OPERATIONAL_BOUNDARY.md`

It fixes:

- separate, killable worker processes;
- CPU, memory, process, file, temporary-storage, request, lineage, element,
  relation, manifest, and response limits;
- header, body, Core, and total timeouts;
- kill-on-timeout;
- startup commit, fingerprint, callable, serializer, and canary verification;
- readiness;
- logging and privacy retention;
- credential lifecycle;
- rate and concurrency limits;
- upgrade and compatible-pair rollback.

### 2.7 Authority Matrix

Frozen in:
`docs/architecture/runtime/ORION_AUTHORITY_MATRIX.md`

It assigns every scoped responsibility to exactly one owner across:

- Human Workspace;
- NEXAHEDRON;
- Gateway;
- Runtime;
- Core Invocation Adapter;
- frozen ORION Core.

It resolves prior ambiguity between transport validation and Core conformance
or certification.

## 3. Architecture issues closed

The contract freeze closes these architecture questions:

- which frozen execution path Runtime 1.1 must invoke;
- which identifier is deterministic and which is operational;
- which Confirmed Material format crosses the wire;
- how Alpha confirmation identity is replaced without changing Core;
- which artifacts a successful response contains;
- whether artifacts are embedded or externally resolved;
- how clarification remains stateless;
- which limits make public execution bounded;
- how timed-out work is prevented from publishing;
- which component owns each form of validation, execution, identity, error,
  artifact, and certification;
- how NEXAHEDRON remains usable when Runtime is unavailable;
- how deployment and rollback preserve consumer compatibility.

No open architectural choice is delegated to implementation.

## 4. Issues remaining

The remaining issues are verification gates, not unresolved architecture.

### 4.1 Frozen invocation proof

Gate 0 must prove that every callable named by the Slice Execution Contract can
execute the complete sequence on accepted, non-fixture Confirmed Material
without modifying the frozen Core.

### 4.2 Canonical serializer proof

Gate 0 must prove that every one of the 22 manifest bodies:

- has an available frozen canonical serializer;
- survives exact reconstruction where a frozen reconstruction contract exists;
- reproduces the declared SHA-256 and byte length;
- resolves all earlier artifact references.

### 4.3 Replay proof

Two fresh isolated invocations of one canonical envelope must produce:

- byte-identical Core artifacts;
- byte-identical ordered manifest;
- byte-identical terminal Slice IV Certification;
- equal Request and Result Digests;
- potentially different Operational Execution IDs without affecting those
  bytes.

### 4.4 Bound verification

Gate 0 must exercise accepted and adversarial Profile v1 inputs at each
published limit and demonstrate:

- deterministic rejection above a limit;
- no partial publication;
- worker termination at CPU, memory, and wall-time boundaries;
- maximum response enforcement;
- no surviving worker after timeout.

The published limits are frozen. A failure to enforce them blocks
implementation rather than authorizing an undocumented substitute.

### 4.5 NEXAHEDRON compatibility proof

Gate 0 must confirm that NEXAHEDRON can mechanically produce
`orion.confirmed-material/1.0` and the API envelope from explicit Human
confirmation.

This will require a later implementation update because the existing internal
Alpha confirmation digest is intentionally not wire-compatible. That work must
follow this contract; it is not a remaining architectural decision.

### 4.6 Graceful-degradation proof

Before public activation, tests must show that Runtime absence, rejection,
timeout, version mismatch, and certification failure never mutate or remove:

- Working Material;
- Reflection;
- Rest;
- the Human-owned Orientation Record.

## 5. Gate 0 entry criteria

Gate 0 may begin because:

- [x] the invocation sequence is explicit;
- [x] accepted inputs and outputs are explicit;
- [x] identifiers and canonical digests are explicit;
- [x] material mapping and integrity are explicit;
- [x] manifest contents and ordering are explicit;
- [x] clarification lineage and errors are explicit;
- [x] operational limits and isolation are explicit;
- [x] ownership contains no unresolved overlap;
- [x] the frozen Core remains unchanged;
- [x] no Runtime implementation has begun.

## 6. Gate 0 exit criteria

Gate 0 passes only when:

- [ ] the complete frozen invocation succeeds;
- [ ] all existing Slice II–IV proofs remain green;
- [ ] all 22 manifest artifacts verify;
- [ ] independent replay is byte-identical;
- [ ] Core commit and fingerprint remain exact;
- [ ] operational bounds are enforceable without Core changes;
- [ ] the timeout worker is demonstrably killable;
- [ ] Confirmed Material v1 mapping is exact;
- [ ] clarification closure is independently reproducible;
- [ ] no historical Runtime or Gateway path is used;
- [ ] no LYRA, SIRIUS, semantic, or AI behavior is introduced.

Only after these conditions pass may the status advance to
`READY FOR IMPLEMENTATION`.

## 7. Final decision

**READY FOR GATE 0**

The Version 1.1 contracts are now normatively specified. Gate 0 may officially
begin as a bounded verification of the frozen invocation, canonical artifacts,
replay, operational limits, and NEXAHEDRON transport compatibility.

Runtime implementation and deployment remain prohibited until Gate 0 passes.
