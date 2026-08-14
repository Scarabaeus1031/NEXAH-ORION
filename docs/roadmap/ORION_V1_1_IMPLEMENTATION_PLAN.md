# ORION Version 1.1 — Public Runtime & Gateway Boundary

- Status: Implementation plan
- Target release: ORION Runtime `1.1.0`
- Public API version: `1.0`
- Frozen Core release: ORION `1.0.0`
- Frozen Core commit: `d34fbb2f99334534f4db89465a29f8bdb16d14d3`
- Frozen Core fingerprint:
  `6201362c094530a0a31fa3d80b46c9131011bb8c8d400183271b0da0eb423f8d`
- Implementation status: Not started
- Architecture status: ORION Version 1 Core remains frozen

## 1. Purpose

Version 1.1 exposes the frozen ORION Version 1 Core through a minimal,
versioned, deterministic execution boundary.

The Runtime is not the Core. It owns transport and operations around the Core.
It receives an exact confirmed input, invokes the frozen deterministic chain,
publishes only validated canonical artifacts, and stops at the certified
Version 1 boundary.

This plan authorizes no Core modification, new Orientation semantics, new
operator, LYRA or SIRIUS behavior, model call, evidence generation, Human
Report, recommendation, decision, or autonomous action.

Implementation may begin only through the ordered stages in this plan. A stage
that cannot preserve the Version 1 fingerprint stops closed.

## 2. Governing Baseline

Version 1.1 is governed by:

- [`ORION_V1_CERTIFIED_BASELINE.md`](../releases/ORION_V1_CERTIFIED_BASELINE.md);
- [`ORION_SYSTEM_PLATE.md`](../architecture/ORION_SYSTEM_PLATE.md);
- [`ORION_CORE_PLATE.md`](../architecture/ORION_CORE_PLATE.md);
- the frozen Version 1 public contracts under
  [`docs/architecture/contracts/`](../architecture/contracts/);
- the immutable Core implementation and certification proofs at the release
  commit and fingerprint recorded above.

The following distinction is normative:

```text
Certified ORION Core 1.0
        │
        │ immutable invocation only
        ▼
Core Invocation Adapter
        │
        ▼
Gateway 1.1
        │
        ▼
Runtime 1.1 HTTP boundary
        │
        ▼
Authorized consumer
```

Only the top component owns Orientation algorithms and certified artifacts.
The adapter, Gateway, and Runtime are Version 1.1 execution infrastructure.
They acquire no Core authority.

## 3. Non-Negotiable Compatibility Finding

The repository contains earlier `orientation_runtime` and `gateway` modules.
They produce the earlier Orientation Report contract flow. Their presence in
the repository and in the downstream fingerprint does not make them the
certified Slice II–IV Core execution chain.

Version 1.1 must not publish that historical path under the claim that it
executes the certified Core.

Before implementation proceeds, an independent test must prove that the
production invocation path executes, in canonical order, the frozen chain:

```text
Human-confirmed CommonMark
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
External Orientation Map Conformance
        ↓
Expression Contract
        ↓
Expression Construction
        ↓
External Expression Conformance
        ↓
Expression Certification
        ↓
Vertical Slice IV Certification
        ↓
at_slice_iv_certified
        ↓
STOP
```

The required Core Invocation Adapter is orchestration outside the frozen Core.
It may call existing frozen entry points in the certified order. It may not
reimplement, bypass, repair, normalize, substitute, or reinterpret any stage.

If the complete chain cannot be invoked without changing a frozen Core module,
Version 1.1 stops at this gate and records the limitation. The historical
Runtime is not an allowed fallback.

## 4. Architecture

### 4.1 Components

| Component | Owns | Must not own |
|---|---|---|
| Certified Core 1.0 | Frozen deterministic algorithms, artifacts, conformance, certifications, STOPs | HTTP, authentication, rate limiting, deployment, sessions |
| Core Invocation Adapter | Ordered invocation of exact frozen entry points and collection of their exact outputs | Core logic, semantic translation, artifact repair, alternate outputs |
| Gateway 1.1 | Envelope validation, lineage validation, version negotiation, invocation authorization, output-set validation | Core algorithms, Human presentation, evidence creation |
| Runtime 1.1 | HTTP, operational request identity, authentication, limits, timeout, logging, health, canonical transport serialization | Orientation meaning, UNDERSTAND logic, Expression construction, decisions |
| NEXAHEDRON proxy | Same-origin forwarding, service credential, boundary-failure presentation | Runtime execution, Core validation, report invention |

### 4.2 Data flow

```text
Human-confirmed NEXAHEDRON session
        ↓
Confirmed Material + Orientation Request 1.0
        ↓
NEXAHEDRON /api/orientation
        ↓
Authenticated Runtime request
        ↓
Gateway envelope and lineage validation
        ↓
Core Invocation Adapter
        ↓
Frozen Core 1.0
        ↓
Exact certified artifacts
        ↓
Gateway output-set validation
        ↓
Canonical Runtime response
        ↓
NEXAHEDRON boundary presentation
        ↓
STOP
```

NEXAHEDRON sends only material explicitly confirmed by the Human. Runtime and
Gateway do not retrieve source material and do not create Evidence.

### 4.3 Authority boundary

- Human authority remains the source of intention, scope, confirmation, and
  any decision to submit or resubmit.
- NEXAHEDRON owns interaction and the same-origin proxy only.
- Runtime owns operational execution conditions only.
- Gateway owns acceptance of the transport envelope and exact lineage only.
- Core owns every deterministic Orientation artifact and certification.
- No component may silently complete data owned by another authority.

## 5. Runtime Boundary

### 5.1 Accepted inputs

The Runtime accepts one canonical transport envelope containing:

1. API version `1.0`;
2. one frozen `orion.orientation-request/1.0`;
3. one existing immutable NEXAHEDRON Confirmed Material artifact;
4. an optional ordered clarification lineage;
5. an `evidence` array that must be empty in Runtime 1.1;
6. no executable effects.

Confirmed Material must contain the exact Human-confirmed UTF-8 material,
source identity, version, confirmation identity, and integrity digest already
defined by NEXAHEDRON. It is an existing boundary artifact, not a new ORION
semantic contract.

The Runtime rejects:

- mutable working material;
- unconfirmed material;
- a request whose Orientation Object does not identify the supplied Confirmed
  Material;
- unsupported source profiles;
- non-empty evidence input;
- unknown contract or API versions;
- effects other than `none`;
- credentials or provider configuration inside the body.

### 5.2 Produced outputs

A successful execution returns a Runtime envelope containing:

- API version;
- Runtime version;
- operational execution identifier;
- exact Orientation Request identity and version;
- exact Core version, commit, and canonical fingerprint;
- terminal STOP;
- an ordered manifest of exact certified artifact identities, schema versions,
  integrity values, and canonical bodies;
- the exact terminal Vertical Slice IV Certification reference;
- no Human-facing interpretation.

The Runtime envelope is transport structure. It does not replace or modify any
inner certified artifact.

### 5.3 Immutability

The Runtime treats every submitted and produced artifact as immutable. It may
allocate an operational execution identifier and timestamps for logs, but
neither may become an input to Core identity, ordering, serialization, or
certification.

Equal canonical accepted inputs must produce byte-identical Core artifacts.
Transport headers and operational log timestamps are outside that deterministic
artifact comparison.

## 6. Public API Version 1

The normative API specification will be created as
`docs/api/ORION_PUBLIC_API_V1.md`.

### 6.1 Endpoint

```text
POST /orientation/v1/requests
```

Required request headers:

```text
Authorization: Bearer <service credential>
Content-Type: application/vnd.orion.runtime+json;version=1.0
Accept: application/vnd.orion.runtime+json;version=1.0
ORION-API-Version: 1.0
```

Optional request header:

```text
ORION-Execution-ID: <caller-generated correlation identifier>
```

The Runtime validates but never uses a caller-supplied operational identifier
as a Core identity input. If absent, the Runtime creates one.

Required response headers:

```text
Content-Type: application/vnd.orion.runtime+json;version=1.0
ORION-API-Version: 1.0
ORION-Runtime-Version: 1.1.0
ORION-Core-Version: 1.0.0
ORION-Core-Fingerprint: 6201362c094530a0a31fa3d80b46c9131011bb8c8d400183271b0da0eb423f8d
ORION-Execution-ID: <operational identifier>
Cache-Control: no-store
```

### 6.2 Request envelope

The API specification must define this transport shape without redefining any
contained artifact:

```text
api_version
request
confirmed_material
lineage
  requests
  clarifications
evidence
```

`lineage.requests` and `lineage.clarifications` are ordered immutable public
contracts used only when `request.clarification_of` is present. `evidence` must
be an empty array in Version 1.1.

Unknown top-level fields are rejected. Unknown fields inside frozen contracts
follow their existing compatibility rules.

### 6.3 Success response

The API specification must define:

```text
api_version
runtime_version
execution_id
request_ref
core_release
  version
  commit
  fingerprint
status
terminal_stop
artifact_manifest
terminal_certification_ref
```

`status` describes execution completion only. It does not assert meaning,
correctness of Human interpretation, evidence sufficiency, or a recommended
action.

### 6.4 Operational error response

Failures before or around Core execution use a separate operational error
envelope:

```text
api_version
runtime_version
execution_id
error
  category
  code
  retry
  detail_refs
```

Permitted categories are limited to:

- `transport`;
- `authentication`;
- `rate_limit`;
- `version`;
- `request_validation`;
- `lineage_validation`;
- `timeout`;
- `runtime_unavailable`;
- `core_invocation`;
- `output_validation`.

Operational errors contain no stack trace, filesystem path, secret, source
payload, internal exception text, or inferred explanation. A frozen Core
failure artifact remains a Core artifact and must not be rewritten as an
operational error.

### 6.5 HTTP status codes

| Status | Meaning | Retry rule |
|---:|---|---|
| `200` | Complete validated execution reached `at_slice_iv_certified` | No automatic retry required |
| `400` | Malformed JSON or malformed transport envelope | Retry only after caller correction |
| `401` | Missing or invalid service credential | Do not retry without credential correction |
| `406` | Requested response media type is unsupported | Retry with supported `Accept` |
| `409` | Clarification lineage is required but not supplied as an exact immutable chain | Retry only after Human-controlled clarification and exact lineage inclusion |
| `413` | Body exceeds the published limit | Do not retry unchanged |
| `415` | Unsupported request media type | Retry with the Version 1 media type |
| `422` | Contained contract, confirmation, identity, integrity, or lineage is invalid | Retry only after correcting the invalid input |
| `429` | Rate limit exceeded | Retry only after `Retry-After` |
| `500` | Runtime could not safely publish a validated output | Retry only when response declares `safe` |
| `503` | Runtime or frozen Core dependency is unavailable | Retry after `Retry-After` |
| `504` | Published execution timeout reached before a validated terminal artifact | Same immutable request may be retried after the declared interval |

No redirect is permitted for `POST /orientation/v1/requests`.

### 6.6 Timeout and body limits

The initial public deployment uses:

- maximum request body: `2,000,000` bytes;
- request-header timeout: `5` seconds;
- body-read timeout: `10` seconds;
- Core execution timeout: `15` seconds;
- total request timeout: `30` seconds.

Timeout terminates publication, not the deterministic rules. A partial artifact
set is never returned as complete. The implementation must ensure that timed
out work cannot later publish to the completed response.

### 6.7 Rate limits

The initial deployment uses:

- `30` accepted POST attempts per service credential per minute;
- burst capacity of `5`;
- maximum `2` concurrent Core executions per credential;
- `60` health requests per source IP per minute.

Rate-limit state is operational only. It must not alter Core output or artifact
identity. A rejected request never enters the Core.

### 6.8 Retry behavior

The API is side-effect free. Retrying the same immutable accepted envelope is
safe at the Core boundary and must reproduce the same certified artifacts.

Clients must not retry `400`, `401`, `406`, `409`, `413`, `415`, or `422`
without the correction named above. Clients may retry `429`, `503`, and `504`
only after `Retry-After`. A `500` response is retried only when its error
envelope declares `retry: safe`.

The Runtime does not retry Core execution internally after an unknown failure.

### 6.9 Health endpoint

```text
GET /health
```

The endpoint is unauthenticated and returns only:

```text
status
runtime_version
api_version
core_version
core_fingerprint
```

It returns `200` only when the Runtime has loaded the exact pinned Core,
verified its fingerprint, and can accept work. Otherwise it returns `503`.
Health performs no Orientation and returns no environment details.

## 7. Gateway Boundary

Gateway 1.1 owns five operations, in order:

1. validate transport envelope structure and version;
2. validate Confirmed Material and exact request-to-material identity;
3. validate optional clarification lineage;
4. invoke the Core Invocation Adapter once;
5. validate that the returned artifact set is complete, ordered, internally
   consistent, and terminal at `at_slice_iv_certified`.

Gateway must not:

- inspect text for meaning;
- create or select Evidence;
- infer missing fields;
- generate a Human Report;
- call the historical Runtime as a fallback;
- repair invalid Core artifacts;
- reorder artifacts;
- omit a failed certification;
- publish an incomplete chain as successful.

## 8. Clarification Compatibility Decision

### 8.1 Decision

Version 1.1 uses **stateless carried lineage**.

A follow-up Orientation Request preserves its frozen
`clarification_of.result_id` and `result_version`. Its Runtime envelope also
carries the exact ordered prior Orientation Request and Clarification Result
contracts needed to resolve that reference.

Gateway 1.1 validates one combined contract set containing:

- all supplied prior requests;
- all supplied prior Clarification Results;
- the current follow-up request;
- the current Core outcomes.

No contract field is removed or rewritten. No prior identifier is replaced.
The Runtime stores no hidden session state and does not retrieve lineage from a
database.

### 8.2 Validation rules

- The lineage is empty when `clarification_of` is absent.
- When `clarification_of` is present, the referenced exact Clarification Result
  and its originating exact Orientation Request must be present.
- The complete supplied chain must have unique identity-version pairs.
- Every clarification reference must resolve.
- Request versions must remain distinct and ordered.
- Human-provided changes must remain attributable to the follow-up request.
- Unreferenced, duplicate, reordered, altered, or incomplete lineage fails
  closed.

### 8.3 Compatibility rationale

This decision changes the Version 1.1 Gateway invocation context, not any
Version 1 public contract and not Core behavior. It preserves the existing
`clarification_of` requirement and makes the information needed by frozen
cross-contract validation explicit at the transport boundary.

If implementation proves that the Gateway cannot include carried lineage
without modifying frozen Core validation, Version 1.1 publishes clarification
as a known one-step limitation:

- the first Clarification Result may be returned;
- follow-up execution is rejected with `409`;
- NEXAHEDRON preserves the Human's work;
- no provenance reference is discarded;
- no bypass is permitted.

## 9. Authentication and Trust

The initial deployment is publicly documented but POST access is
service-to-service:

- NEXAHEDRON holds one rotatable Runtime credential as a Cloudflare secret;
- the browser never receives the credential or the Runtime origin URL;
- `/api/orientation` is the sole browser-facing proxy;
- Runtime accepts no cookies and creates no Human account;
- credentials identify the authorized consumer, not the Human;
- credential identity never enters Core artifacts.

Anonymous public POST access is outside Version 1.1. Adding consumers requires
credential issuance and rate-limit configuration only; it does not change
Orientation semantics.

## 10. Logging and Monitoring

Runtime logs only operational metadata:

- execution identifier;
- authorized consumer identifier;
- API and Runtime version;
- Core fingerprint;
- HTTP status;
- request and response byte counts;
- duration;
- terminal STOP or operational error code.

Runtime does not log:

- source text;
- Human annotations;
- request body;
- certified artifact bodies;
- authorization values;
- stack traces in public responses.

Monitoring covers availability, latency, error counts, rate-limit rejection,
timeout, fingerprint mismatch, and restart count. Monitoring must not inspect
or classify Orientation content.

## 11. Packaging

The canonical packaging target is one OCI/Docker image owned by the ORION
repository.

Requirements:

- Python `3.10+`, with one exact minor version pinned for the release image;
- immutable ORION source at the recorded release commit;
- build-time and startup verification of the canonical Core fingerprint;
- base image pinned by digest;
- dependency versions pinned;
- non-root process;
- read-only root filesystem where supported;
- no interactive startup;
- environment-only configuration;
- stdout/stderr structured operational logs;
- `SIGTERM` graceful shutdown;
- health check against `/health`;
- no database, queue, model, provider, browser, or source-retrieval dependency.

Required environment variables:

```text
ORION_RUNTIME_HOST
ORION_RUNTIME_PORT
ORION_RUNTIME_PUBLIC_URL
ORION_RUNTIME_AUTH_SECRET
ORION_RUNTIME_LOG_LEVEL
ORION_RUNTIME_REQUEST_TIMEOUT_SECONDS
ORION_RUNTIME_RATE_LIMIT_PER_MINUTE
ORION_EXPECTED_CORE_VERSION
ORION_EXPECTED_CORE_COMMIT
ORION_EXPECTED_CORE_FINGERPRINT
```

Secrets must not appear in the image, repository, build arguments, logs, or
health response.

Two builds from the same release input must produce the same application
manifest and the same embedded Core manifest. Container registry metadata that
cannot be made byte-identical must remain outside the Core reproducibility
claim and be documented.

## 12. Minimal Deployment

The minimal production target is:

```text
Cloudflare
  HTTPS + DNS + edge limits
        ↓
runtime.nexahedron.com
        ↓
TLS reverse proxy or managed container ingress
        ↓
one ORION Runtime 1.1 container
        ↓
frozen ORION Core 1.0
```

System requirements:

- Linux container host or managed container service;
- one CPU allocation;
- at least `512 MiB` memory;
- outbound network access disabled unless required for operational monitoring;
- persistent storage not required;
- automatic restart on process failure;
- immutable image deployment by digest;
- HTTPS at the public ingress;
- Runtime origin restricted to Cloudflare or the selected trusted ingress
  where the platform supports it.

The current shared OVH static webhosting is not a Runtime target. The current
NEXAHEDRON JavaScript Worker does not embed the Python service.

### 12.1 Installation

1. provision the container host;
2. install or select the pinned container runtime;
3. configure secrets and non-secret environment values;
4. pull the immutable image by digest;
5. verify embedded Core release metadata;
6. start one instance;
7. verify `/health`;
8. attach `runtime.nexahedron.com`;
9. verify TLS and authenticated POST from a controlled client;
10. keep NEXAHEDRON disconnected until the release gate passes.

### 12.2 Upgrade

1. build and verify a new Runtime image;
2. preserve the frozen Core fingerprint unless a separately governed Core
   release exists;
3. deploy the new image beside the current instance;
4. run health and deterministic replay;
5. switch traffic only after verification;
6. retain the previous digest for rollback.

### 12.3 Rollback

Rollback selects the previously verified image digest and restores its exact
environment configuration. It does not rebuild the image, modify Core
artifacts, or replay partial requests. NEXAHEDRON presents Gateway unavailable
during any interval in which no healthy Runtime exists.

## 13. NEXAHEDRON Integration

NEXAHEDRON integration begins only after the deployed Runtime passes its release
gate.

Required changes are limited to:

1. extend the existing transport envelope with Confirmed Material and carried
   clarification lineage;
2. update the same-origin `/api/orientation` proxy to the Runtime 1.0 media
   type and required version headers;
3. store the Runtime service credential as a Cloudflare secret;
4. set:

   ```text
   ORION_GATEWAY_URL=https://runtime.nexahedron.com/orientation/v1/requests
   ```

5. accept only the documented Runtime 1.0 response envelope;
6. present operational failures through the existing boundary-failure surface;
7. expose certified artifact identity, status, provenance, and STOP without
   inventing a Human Report or explanation;
8. preserve the current Workspace, confirmation, Rest, and Human authority
   behavior unchanged.

The current NEXAHEDRON consumer expects the earlier Orientation Report envelope.
That envelope must not be treated as proof of certified Slice II–IV execution.
The consumer adapter must be updated to the Runtime 1.0 envelope before public
activation. This is an integration change, not a Core change and not a new
Human interaction.

Deployment of this integration requires a new NEXAHEDRON Worker version. It
does not require an OVH upload, nameserver change, new public domain, or Miso
action. The existing `nexahedron.com` domains remain attached to the Worker.

## 14. Verification

### 14.1 Frozen Core verification

- reproduce the canonical Core fingerprint before packaging;
- run every Version 1 proof and certification test;
- compare every frozen source and canonical document with the Version 1 release
  commit;
- prove that Runtime packaging modifies no frozen file;
- prove the production adapter imports and invokes only approved frozen entry
  points;
- prove the historical Runtime is absent from the production execution path.

### 14.2 Runtime verification

- canonical request parsing;
- strict media-type and version negotiation;
- body, header, timeout, concurrency, and rate limits;
- authentication acceptance and rejection;
- no payload logging;
- deterministic output for identical accepted input;
- complete artifact manifest and terminal STOP;
- no partial success;
- graceful shutdown;
- restart recovery;
- health failure on fingerprint mismatch.

### 14.3 Gateway verification

- exact request-to-Confirmed-Material identity;
- invalid confirmation and integrity rejection;
- unsupported CommonMark input rejection;
- artifact ordering;
- complete certification chain;
- output validation without repair;
- historical Runtime fallback impossible;
- empty evidence boundary enforced.

### 14.4 Clarification verification

- first clarification result remains exact;
- follow-up carries exact prior request and result;
- valid carried lineage resolves;
- missing, altered, duplicate, or mismatched lineage fails closed;
- repeated replay is byte-identical;
- no server session is required.

### 14.5 NEXAHEDRON end-to-end verification

- Human confirmation remains mandatory;
- only confirmed material crosses the boundary;
- service credential remains server-side;
- complete request reaches the public Runtime;
- complete certified response returns through the same-origin proxy;
- provenance and Core fingerprint remain visible;
- Gateway unavailable, timeout, version mismatch, and contract rejection remain
  distinct;
- browser retry does not duplicate effects;
- no Workspace state changes automatically;
- production smoke test passes on desktop and mobile.

## 15. Required Documentation

Implementation must create these five normative documents before deployment:

| Document | Canonical path | Responsibility |
|---|---|---|
| Runtime boundary | `docs/architecture/ORION_RUNTIME_BOUNDARY.md` | Runtime/Core separation, authority, inputs, outputs, exclusions |
| Runtime deployment | `docs/deployment/ORION_RUNTIME_DEPLOYMENT.md` | Build, configuration, install, health, upgrade, rollback |
| Public API | `docs/api/ORION_PUBLIC_API_V1.md` | Normative HTTP and envelope contract |
| Gateway decisions | `docs/architecture/ORION_GATEWAY_DECISIONS.md` | Invocation, lineage, validation, no-fallback decisions |
| Runtime release plan | `docs/releases/ORION_RUNTIME_RELEASE_PLAN.md` | Freeze, verification, publication, rollback, downstream activation |

These documents describe Version 1.1 only. They must not edit, supersede, or
reinterpret the Version 1 certified baseline.

## 16. Known Limitations

Version 1.1 intentionally:

- accepts only the frozen Version 1 CommonMark source domain;
- supports only the frozen deterministic Core chain;
- accepts no non-empty Evidence collection;
- performs no Library retrieval;
- performs no semantic interpretation;
- produces no Human Report or generated language;
- provides no LYRA, SIRIUS, recommendation, decision, or action;
- persists no session or Orientation material;
- has no anonymous POST access;
- has no multi-region availability guarantee;
- exposes no streaming, batch, search, webhook, or asynchronous API;
- returns no partial artifact chain as success.

The Clarification follow-up path remains a declared limitation if carried
lineage cannot be added solely at the Gateway boundary.

## 17. Remaining Owner Actions

Repository implementation cannot complete:

1. selection and funding of the Linux/container host;
2. creation of the production container registry/repository;
3. production secret generation and custody;
4. creation of `runtime.nexahedron.com` after the service is healthy;
5. production ingress and TLS ownership;
6. approval of published rate limits and operational retention;
7. final deployment authorization;
8. production smoke-test acceptance.

These are owner or Operations actions, not Core implementation.

## 18. Estimated Implementation Order

The order is dependency-based, not calendar-based.

### Stage 0 — Frozen execution audit

- enumerate the exact certified callable entry points;
- reproduce every Version 1 proof;
- prove the complete chain can be orchestrated without a Core edit;
- record the unchanged fingerprint;
- STOP if this cannot be proven.

### Stage 1 — Normative boundary documents

- create `ORION_RUNTIME_BOUNDARY.md`;
- create `ORION_GATEWAY_DECISIONS.md`;
- freeze Runtime/Core ownership and the carried-lineage decision;
- STOP before code.

### Stage 2 — Public API specification

- create `ORION_PUBLIC_API_V1.md`;
- freeze media type, envelopes, statuses, limits, retries, and health;
- validate against existing frozen contracts and Confirmed Material;
- STOP before transport implementation.

### Stage 3 — Core Invocation Adapter

- implement only ordered invocation of frozen entry points;
- verify complete artifact collection and terminal STOP;
- prove no historical Runtime fallback;
- run all Core proofs;
- STOP before HTTP.

### Stage 4 — Gateway 1.1

- implement envelope, confirmation, identity, lineage, and output-set
  validation;
- implement carried clarification lineage;
- prove deterministic invocation and failure closure;
- STOP before network deployment.

### Stage 5 — Runtime HTTP service

- implement HTTP, authentication, limits, timeout, logging, health, shutdown,
  and canonical transport serialization;
- run focused and full regression suites;
- STOP before packaging.

### Stage 6 — Reproducible packaging

- create the pinned OCI image;
- create `ORION_RUNTIME_DEPLOYMENT.md`;
- verify image and embedded Core manifests;
- STOP before production.

### Stage 7 — Runtime release candidate

- deploy to a non-production ingress;
- execute deterministic replay, failure injection, restart, upgrade, and
  rollback tests;
- create `ORION_RUNTIME_RELEASE_PLAN.md`;
- freeze the verified image digest;
- STOP before NEXAHEDRON activation.

### Stage 8 — NEXAHEDRON integration

- update the internal consumer envelope and same-origin proxy;
- configure a non-production Runtime URL and credential;
- run boundary, clarification, provenance, and end-to-end tests;
- redeploy the NEXAHEDRON Worker only after all tests pass;
- STOP before production Runtime traffic.

### Stage 9 — Production activation

- deploy the frozen Runtime image;
- verify health, TLS, authentication, and fingerprint;
- set the production NEXAHEDRON Runtime URL and secret;
- deploy the verified NEXAHEDRON Worker version;
- run production smoke tests;
- publish Version 1.1 status;
- STOP.

## 19. Definition of Done

ORION Runtime Version 1.1 is complete only when:

- [ ] the frozen Core commit and fingerprint remain unchanged;
- [ ] every Version 1 proof and certification replay passes;
- [ ] the production path invokes the complete certified Slice II–IV chain;
- [ ] the historical Runtime is not substituted for the certified Core;
- [ ] the Core Invocation Adapter contains orchestration only;
- [ ] the public API is versioned and externally documented;
- [ ] authentication, limits, timeouts, logging, health, restart, upgrade, and
      rollback are verified;
- [ ] equal accepted inputs produce byte-identical certified Core artifacts;
- [ ] clarification lineage is preserved exactly or its follow-up limitation is
      explicitly enforced;
- [ ] no Evidence is generated or accepted in Version 1.1;
- [ ] no semantic interpretation, Human Report, LYRA, SIRIUS, model, decision,
      or action exists;
- [ ] the Runtime image is immutable and deployed by digest;
- [ ] NEXAHEDRON integration passes end to end;
- [ ] NEXAHEDRON keeps its Workspace and Human authority unchanged;
- [ ] production smoke tests pass;
- [ ] the execution stops at `at_slice_iv_certified`;
- [ ] the five required normative documents are complete;
- [ ] all remaining external actions have named owners.

## 20. Closing Statement

ORION Version 1.1 makes the frozen Version 1 Core executable without making the
Runtime part of the Core.

The Runtime transports, limits, invokes, observes, and publishes. The Core
alone constructs and certifies deterministic Orientation artifacts. Human
meaning, judgment, and action remain outside both.
