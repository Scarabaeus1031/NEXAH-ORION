# ORION Version 1.1 — Runtime Release Audit

Audit date: 2026-07-24

Audit role: Independent technical auditor

Audited state: Runtime Stage 1, reported as `READY FOR INTEGRATION`

## Executive finding

The Runtime executes the certified Slice II–IV chain deterministically on the
tested inputs. The frozen Core remained unchanged, the 22-artifact manifest was
reproduced, the terminal STOP was reached, all focused tests passed, and the
full regression remained green.

Those results establish the valid happy path. They do not establish release
compliance. The Runtime presently violates mandatory requirements in the
Operational Boundary, Artifact Manifest Contract, Execution Contract, and
startup release binding. Two violations were reproduced directly:

- the worker can transmit UDP data after its network-denial function has run;
- the Runtime becomes ready when the mandatory startup canary is disabled.

The Runtime is therefore not acceptable for NEXAHEDRON integration in its
current state.

Final classification: **ACCEPT WITH CONDITIONS**

Integration may begin only after the blocking conditions in
`ORION_RUNTIME_RELEASE_DECISION.md` are resolved and independently replayed.

## Scope and method

The audit examined:

- all seven frozen Version 1.1 contracts;
- the frozen Authority Matrix;
- every file under `src/orion_runtime`;
- the Dockerfile, systemd unit, environment example, and deployment guide;
- Runtime tests and the Stage 1 proof;
- Slice II, Slice III, and Slice IV certification proofs;
- release fingerprint and Git state;
- HTTP behavior through local loopback;
- worker network behavior through an adversarial local UDP receiver;
- static type-checking output.

No Runtime, Core, deployment, or contract file was modified.

## Confirmed strengths

### Frozen Core boundary

- No tracked file under `src/orion` differs.
- The repository HEAD remains
  `d34fbb2f99334534f4db89465a29f8bdb16d14d3`.
- The existing Core fingerprint reproduces as
  `6201362c094530a0a31fa3d80b46c9131011bb8c8d400183271b0da0eb423f8d`.
- The Adapter imports frozen callable entry points directly and does not call
  the historical Runtime or Gateway.

### Deterministic execution

- The Adapter follows the frozen 31-stage order.
- Fixed Expression declarations match the Execution Contract.
- Evidence remains empty.
- Declared cross-reference declarations remain empty.
- Core serializers produce the 22 artifacts in the required order.
- Request and Result Digests exclude operational identifiers.
- The Operational Execution ID does not enter the canonical success body.
- No timestamp, random value, process identifier, temporary filename, locale,
  or host identifier enters deterministic output.

### Gateway admission

- Duplicate JSON keys, floats, constants, BOM input, and invalid UTF-8 are
  rejected.
- Confirmed Material integrity, source version, confirmation identity, and
  request-to-material matching are checked.
- Empty clarification lineage is checked.
- A valid one-level clarification lineage was independently constructed and
  executed through the terminal Slice IV STOP.
- Unknown top-level fields and non-empty Evidence are rejected.

### HTTP and privacy

- The success path uses the declared media type and version headers.
- Service credentials do not enter Core input or output.
- Request and artifact bodies are not included in application logs.
- Cache prevention and `nosniff` are present on Runtime JSON responses.
- The authenticated success response contains no Operational Execution ID in
  its body.

## Blocking findings

### R-01 — Release identity is asserted, not verified

Severity: Critical

Evidence:

- `src/orion_runtime/release.py` accepts `ORION_CORE_COMMIT` as the current
  commit without reading repository state.
- The Dockerfile excludes `.git` and sets that environment variable to the
  expected value.
- The reproduced fingerprint covers 21 historical Core/public-contract files,
  but does not cover the Slice II–IV modules invoked by the Adapter and does
  not cover the Runtime implementation.
- No Runtime release manifest, immutable image digest binding, supported
  Gateway version, or verification-evidence binding exists.

Consequences:

A container built from modified Slice II–IV or Runtime source can report the
expected commit and pass the existing fingerprint check. This violates
Execution Contract Section 3 and Operational Boundary Sections 7 and 12.

### R-02 — Mandatory startup verification is optional

Severity: Critical

Evidence:

`ORION_STARTUP_CANARY=false` bypasses both required canary executions. An
independent audit invocation produced:

```text
{"ready": true, "errors": []}
```

Consequences:

The service can publish readiness without replaying the complete isolated Core
chain. This violates Operational Boundary Section 7.

### R-03 — Worker network isolation is not effective

Severity: Critical

Evidence:

The worker replaces `socket.connect`, `connect_ex`, `create_connection`, and
`getaddrinfo`. It does not block datagram `sendto`, inherited descriptors,
subprocess-based networking, or other native networking paths.

After `_disable_network()` ran, an independent child sent
`worker-egress` over UDP and the audit receiver obtained all 13 bytes.

Consequences:

The worker does not satisfy the mandatory no-outbound-network process
boundary. The documented internal Docker network restricts external routing
but does not isolate the worker from the parent Runtime or other members of the
internal network. The systemd unit supplies no worker-specific network
isolation.

### R-04 — Manifest reference graph is not verified

Severity: High

Evidence:

`verify_manifest` validates each artifact independently. Its native verifier
receives only one artifact body and ordinal. It has no prior-entry context and
therefore cannot verify that references to earlier manifest entries resolve
exactly or that forbidden forward references are absent.

Consequences:

Artifact Manifest Contract Section 5, steps 6 and 7, are not implemented.
Frozen reserialization is valuable but is not equivalent to verifying the
manifest's cross-artifact graph.

### R-05 — Operational lifecycle limits are incomplete

Severity: High

The following mandatory behaviors are absent or incomplete:

- no single 30-second total request deadline exists;
- CPU-limit termination can surface as `500 core_worker_failed` rather than
  the required `504 core_timeout`;
- `RLIMIT_FSIZE` limits one file, not aggregate worker temporary storage;
- the Docker tmpfs is shared by concurrent workers rather than bounded per
  invocation;
- the systemd temporary directory has no 64 MiB aggregate bound;
- shutdown does not track, drain, or explicitly terminate active workers;
- readiness does not re-check that commit and fingerprint remain verified.

The idle-process SIGTERM test does not exercise shutdown during an active Core
invocation.

### R-06 — Post-projection admission occurs after the full chain

Severity: High

The element and relation profile checks execute after Relations, Navigation,
Orientation Map, and Expression have completed. The Confirmed Material
Contract defines these as post-projection admission bounds.

Consequences:

An input already known to exceed the profile can consume the most expensive
parts of the pipeline before rejection. This increases denial-of-service
exposure and does not honor the specified admission boundary.

### R-07 — HTTP edge behavior is not fully closed

Severity: Medium

- unsupported methods use the inherited `http.server` HTML `501` response;
- that response exposes the Runtime server banner and does not use the
  canonical error envelope;
- duplicate security-sensitive headers are not explicitly rejected;
- pre-authentication HTTP threads are unbounded;
- invalid credentials have no source-level admission limit;
- material and lineage profile excesses use `contract_invalid`, not the stable
  `operational_profile_exceeded` code required by the Operational Boundary.

The audited `PUT` response was HTML with status `501` and a
`Server: ORION-Runtime/1.1` header.

### R-08 — Release verification coverage is insufficient

Severity: Medium

The focused suite contains ten tests, but it does not cover:

- non-empty clarification lineage;
- manifest cross-reference corruption;
- UDP or native network attempts;
- mandatory-canary enforcement;
- actual source-to-release binding;
- active-worker shutdown;
- CPU-limit status mapping;
- aggregate temporary-storage exhaustion;
- duplicate HTTP headers;
- total request deadline;
- target-Linux memory and filesystem enforcement.

The independent audit successfully exercised a one-level lineage, but this is
not repository regression coverage.

### R-09 — Static maintenance signal is red

Severity: Low

`mypy src/orion_runtime --no-incremental` reports 29 errors. This does not
invalidate deterministic runtime execution, but it weakens future maintenance
confidence at the exact boundary responsible for contract parsing and
manifest verification.

## Independent verification results

| Verification | Result |
|---|---|
| Focused Runtime tests | 10 passed |
| Full repository tests | 556 passed, 1 skipped |
| Runtime Stage 1 proof | passed |
| Slice II certification | passed |
| Slice III certification | passed |
| Slice IV certification | passed |
| Valid one-level clarification execution | passed |
| Frozen Core tracked changes | none |
| Worker UDP isolation challenge | failed |
| Mandatory startup-canary challenge | failed |
| Static type check | 29 errors |
| Docker build and target-Linux smoke test | not available |

## Release assessment

The implementation proves that the Core can be called correctly. It does not
yet prove that the Core can be called safely through the frozen public
operational boundary.

The distinction is decisive:

- deterministic Core execution: demonstrated;
- Runtime contract compliance: incomplete;
- safe NEXAHEDRON integration: blocked pending conditions;
- public deployment: not approved.
