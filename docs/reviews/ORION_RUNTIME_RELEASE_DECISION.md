# ORION Version 1.1 — Runtime Release Decision

Decision date: 2026-07-24

## Decision

**ACCEPT WITH CONDITIONS**

This is not permission to integrate the Runtime in its present state.
NEXAHEDRON integration may begin only after all integration-blocking conditions
below are resolved and independently verified.

## Basis

The Runtime demonstrates:

- exact frozen Slice II–IV execution on accepted material;
- byte-identical replay;
- correct 22-artifact ordering on the tested chain;
- terminal Slice IV certification;
- stable Request and Result Digests;
- no change to the frozen Core;
- green focused and full regression tests.

The Runtime does not yet demonstrate:

- trustworthy deployed release identity;
- mandatory startup verification;
- actual no-network worker isolation;
- complete manifest reference verification;
- complete operational lifecycle and limit enforcement.

The failed properties are mandatory frozen-contract requirements, not optional
hardening or future architecture.

## Integration-blocking conditions

### C-01 — Prove the actual release

Readiness must verify the actual deployed Runtime and complete invoked Core
against an immutable release binding. A configured environment value must not
stand in for observed source identity. The binding must include the Runtime
release data required by Operational Boundary Section 12.

Acceptance evidence:

- modified Runtime or invoked Core source causes readiness failure;
- a mismatched release commit causes readiness failure;
- the exact accepted deployment artifact reports its immutable identity.

### C-02 — Make startup verification mandatory

No releasable configuration may become ready without the two isolated,
byte-identical canary executions required by the Operational Boundary.

Acceptance evidence:

- attempted canary disablement leaves readiness false;
- canary failure leaves readiness false;
- both successful manifests and terminal certifications match exactly.

### C-03 — Enforce worker network isolation

The worker must have no outbound network authority.

Acceptance evidence must reject at least:

- TCP connect;
- UDP send/sendto;
- DNS resolution;
- subprocess networking;
- inherited network descriptors;
- connection to the parent Runtime and reverse proxy.

### C-04 — Complete Gateway manifest verification

Gateway must independently resolve every frozen cross-artifact reference
against the exact earlier manifest entry and reject forbidden forward,
missing, duplicate, or altered references.

Acceptance evidence:

- a valid manifest passes;
- each corrupted reference class fails before success publication;
- no worker-produced repair or normalization is accepted.

### C-05 — Complete the operational lifecycle

The frozen behavior must be demonstrated for:

- one total request deadline;
- CPU and wall timeout status;
- aggregate per-invocation temporary storage;
- active-worker shutdown and forced termination;
- post-projection element/relation admission;
- no late publication after timeout or shutdown.

### C-06 — Close the HTTP boundary

The deployed boundary must deterministically reject ambiguous critical headers,
unsupported methods, pre-authentication resource exhaustion, and profile-limit
errors using the frozen error authority and stable codes.

## Conditions before public deployment

After integration blockers pass:

1. build and inspect the Docker image on target Linux;
2. use immutable base and image identities;
3. verify non-root, read-only, memory, CPU, process, file, temporary-storage,
   and network controls;
4. verify reverse-proxy HTTPS and admission policy;
5. verify credential creation, rotation, revocation, and non-disclosure;
6. verify log retention and deletion;
7. execute authenticated replay, restart, upgrade, and rollback tests;
8. bind the compatible NEXAHEDRON Gateway version;
9. run the full regression and every frozen proof against the release artifact.

## Non-blocking maintenance condition

The 29 current static type-check errors should be resolved before the Runtime
is declared a stable maintained public service. They do not independently
invalidate the demonstrated Core result, but leaving them at the contract
boundary increases regression risk.

## What is not required

This decision requires no:

- Core modification;
- architectural redesign;
- semantic extension;
- additional endpoint;
- LYRA or SIRIUS work;
- NEXAHEDRON interaction redesign;
- Version 2 capability.

Every blocking condition follows directly from an already frozen Version 1.1
contract.

## Final statement

The Runtime is functionally executable but not yet operationally compliant.
It may be accepted as a conditional release candidate, not as an integration
dependency in its current state.

**ACCEPT WITH CONDITIONS**
