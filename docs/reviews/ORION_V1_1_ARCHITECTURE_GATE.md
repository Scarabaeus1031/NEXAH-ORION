# ORION Version 1.1 — Architecture Readiness Gate

Status: Architecture review
Scope: Version 1.1 Public Runtime and Gateway Boundary
Reviewed proposal: `ORION_V1_1_IMPLEMENTATION_PLAN.md`
Core baseline: ORION Version 1, frozen
Implementation performed: No

## Overall readiness

**READY WITH CHANGES**

The proposed Version 1.1 architecture has the correct fundamental shape:

```text
NEXAHEDRON

↓

Gateway

↓

Runtime

↓

Core Invocation Adapter

↓

Frozen ORION Core
```

The plan preserves the decisive boundary: the Runtime transports and operates
requests; the frozen Core alone produces certified ORION artifacts. It also
correctly refuses to treat the historical Runtime and Gateway as substitutes
for the certified Slice II–IV execution chain.

The proposal is minimal in product scope and suitable for Version 1.1.
However, implementation must not begin beyond the frozen-execution audit until
the critical issues below are incorporated into the normative Runtime, API,
Gateway, and deployment specifications.

The required changes do not redesign ORION. They make the proposed boundary
precise enough to implement safely.

## Review by perspective

### 1. Determinism

The plan correctly requires equal accepted inputs to produce byte-identical
certified Core artifacts. It also correctly keeps operational failures outside
Core semantics.

Transport determinism is not yet fully defined. A success body containing a
new operational `execution_id` for every attempt cannot itself be
byte-identical on replay. Three identities must remain distinct:

1. the Human- or client-supplied contract request identity;
2. a deterministic digest of the accepted canonical request envelope;
3. a per-attempt operational correlation identity used only by transport,
   logs, and response headers.

Only the first two may appear in a canonical deterministic response body. A
random attempt identity must remain outside that body. Timestamps and other
attempt-specific data must also remain outside canonical artifacts and
canonical response bodies.

The proposed size and timeout limits are useful but do not yet prove bounded
execution. A valid CommonMark input can produce many elements, and structural
equality relations can grow quadratically. A request-size limit alone
therefore does not bound Core work, memory, or response size.

### 2. Certification

The plan preserves the frozen Core certification chain and terminal STOP at
`at_slice_iv_certified`.

The Gateway's proposed validation responsibility is currently too broad.
Statements such as verifying that the artifact set is “internally consistent”
could accidentally create a second certification authority. The ownership
must be exact:

- the Core owns artifact construction, conformance, certification, provenance,
  and certified STOPs;
- the Core Invocation Adapter invokes frozen entry points and collects their
  exact outputs without reinterpretation;
- the Gateway verifies transport-envelope validity, declared identities,
  integrity references, manifest completeness, frozen release fingerprint,
  and the presence of the expected terminal certification;
- the Runtime applies no ORION conformance or certification logic.

Runtime release evidence may certify packaging, routing, isolation, and
replay. It must not claim to re-certify the frozen Core.

### 3. Runtime isolation

The conceptual separation is strong. The plan assigns HTTP, authentication,
limits, logging, health, configuration, and deployment to the Runtime while
leaving deterministic Orientation behavior in the Core.

The isolation is not complete until Core execution occurs within an
operational boundary that can actually enforce termination. An in-process
Python timeout may return control without stopping the work that exceeded the
limit. The Runtime therefore needs a killable execution boundary, such as a
separate worker process with hard CPU and memory limits. This is operational
isolation, not a change to Core behavior.

The Core Invocation Adapter must remain mechanical. It may:

- translate the frozen transport binding into exact frozen Core inputs;
- invoke the documented frozen entry points in their certified order;
- collect exact outputs;
- expose exact identities and integrity references.

It must not repair inputs, infer missing artifacts, normalize Core outputs,
generate provenance, reinterpret a STOP, or reproduce Core algorithms.

### 4. Operational deployment

The proposed containerized Linux deployment, HTTPS reverse proxy, non-root
process, immutable release pin, environment configuration, health check,
restart policy, upgrade, and rollback form an appropriate minimal deployment.

Essential operational details remain to be made normative:

- hard CPU, memory, process, request, lineage, and response limits;
- kill-on-timeout behavior;
- startup failure on Core commit or fingerprint mismatch;
- readiness behavior during startup and shutdown;
- log retention, deletion, and field sanitization;
- credential rotation and revocation;
- compatible deployment and rollback order for Runtime and NEXAHEDRON;
- recovery of configuration and secrets without backing up Human payloads.

The service is stateless. Its backup requirement is therefore limited to
release manifests, image digests, configuration definitions, and recoverable
secret management. Request or result bodies must not be introduced as a
backup obligation.

### 5. Future maintainability

The versioned media type, immutable Core pin, explicit API version, stateless
request model, canonical serialization, and terminal artifact boundary are
good long-term extension points.

LYRA, SIRIUS, and future semantic layers must remain downstream consumers of
separately defined certified handoffs. They must not become hooks inside the
Core Invocation Adapter, Gateway validation, or Runtime response processing.

Version 1.1 should not add generic extension fields. A future API version can
define new envelopes without changing `/orientation/v1/requests` or the
Runtime/Core authority boundary.

## Critical issues

The following issues block implementation beyond the initial frozen-execution
audit.

### 1. The certified Core invocation path is not yet proven

The plan correctly identifies this as Stage 0, but its result is a prerequisite
for the rest of the architecture.

Before service implementation, the project must document and prove:

- every frozen callable entry point in the Slice II–IV chain;
- the exact ordered input artifact graph;
- the exact ordered output artifact graph;
- the terminal Slice IV certification artifact;
- the absence of mutations to frozen modules and artifacts;
- replay of all existing Core proofs through the same invocation path.

If the complete certified chain cannot be invoked without changing the frozen
Core, Version 1.1 must stop. The historical Runtime and Gateway are not an
acceptable fallback.

### 2. Canonical response identity conflicts with byte-identical replay

The proposed response includes `execution_id` while also requiring
byte-identical replay. This is ambiguous and can make the transport response
nondeterministic.

Before implementation, the API specification must define:

- contract request identity;
- deterministic canonical-request digest;
- deterministic result digest;
- operational attempt identity carried only in a response header and logs.

No random value, wall-clock timestamp, host identifier, or deployment
identifier may enter the canonical response body.

### 3. Resource exhaustion is not bounded by the current limits

The proposed two-megabyte request limit and wall-clock timeouts are
insufficient. Valid structural input can expand into a much larger element,
relation, navigation, map, and Expression artifact set.

Before implementation:

- adversarial but valid Profile v1 inputs must be measured;
- maximum accepted source size, element count, clarification depth, generated
  relation count, response size, CPU, and memory must be published;
- compressed request bodies must be rejected for Version 1.1;
- Core execution must run in a killable process with hard resource limits;
- timeout must terminate the worker rather than leave Core work running.

These limits are operational admission rules. They must not alter Core
algorithms or certified artifacts.

### 4. The transport binding to Confirmed Material is not frozen

NEXAHEDRON currently has an internal
`orion.confirmed-local-source/0.1-alpha` artifact. The current Gateway request
mapping and the proposed Runtime envelope do not yet share one frozen,
normative binding.

Before implementation, the public API specification must define:

- the exact accepted Confirmed Material schema and version;
- its canonical UTF-8 serialization;
- the mechanical mapping to frozen Core input artifacts;
- integrity verification at the boundary;
- the relationship between Orientation Object references and source content;
- rejection of unknown or additional material forms.

This does not require changing the Human Workspace. It requires freezing the
wire contract instead of deriving it implicitly from an internal Alpha type.

### 5. The output manifest is not sufficiently specified

The plan requires an artifact manifest but does not settle whether the
response carries complete canonical artifact bodies or only identities and
references.

A stateless public Runtime cannot return references that no authorized
downstream consumer can resolve. Conversely, returning the complete artifact
chain affects privacy, response size, and replay rules.

Before implementation, the API must define:

- which exact artifacts are returned;
- whether each entry is an embedded canonical body or a resolvable immutable
  reference;
- ordering and duplicate rules;
- identity and integrity verification;
- maximum response size;
- authorization and lifetime for any resolvable reference.

Version 1.1 should prefer a self-contained deterministic response unless a
pre-existing immutable artifact store is already authoritative. It must not
introduce a hidden storage system.

### 6. Clarification lineage needs one exact contract

Carried immutable lineage is the correct compatibility decision because it
preserves statelessness and avoids a hidden Runtime session. It is not yet
complete enough to implement.

The normative contract must require:

- the complete ordered chain of referenced requests and clarification results;
- canonical identities, schema versions, and integrity digests;
- exact resolution of every `clarification_of` reference;
- rejection of missing, reordered, duplicated, or unrelated lineage;
- a maximum lineage depth and total byte size;
- a new Human confirmation whenever the confirmed material changes.

Malformed or unresolved lineage is invalid input and should use `422`.
`409` should be reserved, if retained, for a valid Core outcome that explicitly
requires Human clarification. It must not mean both “missing contract data”
and “valid clarification required.”

Replay uses the full canonical envelope, including lineage. The Runtime must
store none of it as session state.

### 7. Operational rollout and graceful degradation are not yet closed

NEXAHEDRON will normally place one service credential behind a same-origin
proxy. A Runtime limit applied only per credential allows one abusive public
client to consume the quota for every visitor. The minimum safe arrangement is:

- per-client rate limiting at the NEXAHEDRON edge;
- a global credential and concurrency limit at the Runtime;
- no Runtime credential in the browser.

Deployment and rollback must also be compatibility-aware:

1. deploy a Runtime compatible with the currently deployed NEXAHEDRON;
2. verify health, fingerprint, API version, and a deterministic canary;
3. activate the new NEXAHEDRON Gateway path;
4. retain the previous compatible pair for rollback.

Rolling back only the Runtime after deploying a newer incompatible consumer
can create an outage.

Release acceptance must prove that Runtime absence, timeout, authentication
failure, version mismatch, and certification failure:

- never erase or mutate the Human-owned Workspace state;
- never prevent Reflection, Rest, or access to the Orientation Record;
- never trigger an automatic retry that changes Human intent;
- provide a clear recoverable failure at the ORION boundary.

## Recommended improvements

These improvements are ordered by importance. They should be incorporated
while closing the critical issues, but they do not expand Version 1.1.

### 1. Publish one responsibility table in every normative document

Use identical language for Core, Core Invocation Adapter, Gateway, Runtime,
NEXAHEDRON proxy, and Human Workspace. In particular, replace broad uses of
“validation” with the exact object being validated.

### 2. Make startup fail closed

The Runtime must refuse readiness when the configured Core commit,
fingerprint, API version, or required frozen entry point differs from the
release manifest. A running process with the wrong Core must not return a
healthy status.

### 3. Define `/health` as readiness

One endpoint is sufficient for Version 1.1. It should:

- perform no Core execution;
- expose no secrets or Human data;
- report the Runtime version, API version, and expected Core fingerprint;
- return non-success until startup verification is complete;
- use `Cache-Control: no-store`.

Process liveness can remain an orchestrator concern.

### 4. Harden the small HTTP surface

For Version 1.1:

- accept only the declared content type and `Content-Encoding: identity`;
- reject unknown top-level fields;
- disable cross-origin browser access to the Runtime origin;
- expose the API through the NEXAHEDRON same-origin proxy;
- add `Cache-Control: no-store` to request results;
- add `X-Content-Type-Options: nosniff`;
- never forward arbitrary client headers to the Core;
- never log authorization values or request bodies.

### 5. Define credential lifecycle

Document creation, storage, overlap rotation, revocation, and emergency
replacement of the NEXAHEDRON service credential. Comparison must not leak the
credential through timing, errors, or logs.

### 6. Define privacy retention explicitly

Operational logs should contain only bounded metadata and should have a
declared retention and deletion period. User-controlled request identifiers
must not become unbounded metric labels. Human source content, fragments, and
certified artifact bodies must not enter logs, traces, or error reports.

### 7. Separate HTTP errors from Core outcomes

Transport rejection, operational failure, and valid Core outcomes must have
different stable error codes. HTTP status is not an ORION semantic result.
Every error body should identify its authority as Runtime, Gateway, or Core
without reproducing sensitive input.

### 8. Publish a compatibility matrix

The Runtime release manifest should bind:

- Runtime version;
- public API version;
- container image digest;
- Core commit and fingerprint;
- supported NEXAHEDRON Gateway version;
- verification evidence.

This is a Runtime release attestation, not a new Core certification.

### 9. Make rollback verification symmetrical with deployment

Upgrade and rollback should both verify the exact image digest, Core
fingerprint, health response, deterministic canary, and NEXAHEDRON compatibility
before traffic is accepted.

### 10. Preserve a deliberately narrow future boundary

Future consumers should receive frozen artifact references or a separately
certified handoff. The Runtime must not contain provider adapters, semantic
hooks, presentation rules, or generic extension payloads.

## API assessment

The single execution endpoint and single health endpoint are minimal and
appropriate:

```text
POST /orientation/v1/requests
GET  /health
```

The path is versionable and can remain stable when a future `/orientation/v2`
is introduced. Version negotiation must be strict: an unsupported version is
rejected rather than approximated.

The execution endpoint remains stateless only if:

- every required artifact and clarification ancestor is carried by the
  request;
- no server-side session is created;
- retries do not depend on a previous process instance;
- idempotency means deterministic recomputation, not stored response lookup.

Request identifiers alone do not preserve provenance. Provenance is preserved
by the complete canonical input artifact graph, its identities and integrity
digests, the frozen Core release identity, and the exact certified output
chain.

Subject to the critical corrections above, no additional Version 1 endpoint is
needed.

## Clarification lineage decision

**Accept carried immutable lineage, with changes.**

This is the only proposed approach that preserves all three required
properties:

- the Runtime remains stateless;
- the frozen Core contract is not changed;
- a clarification chain can be independently reconstructed and replayed.

The lineage is part of the canonical request. Equal complete lineages and equal
confirmed material must produce equal certified Core artifacts.

The Runtime must not look up, append, repair, summarize, or retain lineage.
NEXAHEDRON remains responsible for Human-controlled inclusion of the prior
immutable artifacts. The Gateway verifies exact reference closure before Core
invocation.

If the frozen Core cannot accept the closed lineage through its existing
contracts, Version 1.1 must publish clarification as an explicit unsupported
Runtime limitation. It must not simulate the cycle or discard the prior
identifier.

## Deployment assessment

The simplest suitable production model remains:

```text
Public HTTPS

↓

Reverse proxy

↓

Stateless ORION Runtime container

↓

Killable Core worker process
```

The container image must bind the immutable Runtime release and frozen Core
release. Configuration comes from environment or mounted secrets; no
interactive setup is permitted.

The deployment does not require a database, session store, message queue,
artifact repair service, or content backup. It does require bounded resources,
restart supervision, readiness, structured metadata-only logs, monitoring,
and a tested image-level rollback.

## NEXAHEDRON integration assessment

The Human Workspace can remain independent of Runtime availability because
ORION begins only after explicit Human confirmation. That independence must be
treated as a release invariant, not merely a user-interface preference.

The integration is acceptable when:

- confirmed material remains Human-owned before submission;
- the service credential remains server-side;
- the Workspace sends one versioned canonical envelope;
- a failed submission leaves the Orientation Record intact;
- retry requires an explicit Human action;
- the user can continue locally or Rest without ORION;
- returned artifacts remain visibly attributed to ORION and do not acquire
  Human authority.

No Workspace redesign is necessary.

## Things intentionally left out

The following do not belong to Version 1.1:

- LYRA;
- SIRIUS;
- semantic interpretation or reasoning;
- LLM or model-provider integration;
- evidence discovery, retrieval, or generation;
- recommendations, decisions, or autonomous actions;
- anonymous public execution;
- developer-token and multi-tenant authorization systems;
- persistent Runtime sessions;
- an idempotency database or response cache;
- asynchronous jobs, queues, webhooks, streaming, or batch execution;
- a public artifact repository introduced solely for this API;
- additional source profiles or generalized media ingestion;
- Human Reports and presentation generation;
- plugin systems or provider adapters;
- multi-region orchestration and advanced autoscaling;
- a generalized API extension mechanism;
- any change to frozen Core semantics, algorithms, proofs, or certification.

These omissions keep Version 1.1 small enough to certify operationally and do
not prevent a future versioned API or downstream certified handoff.

## Gate conditions

The architecture gate becomes fully green only when the proposed plan and its
normative documents record:

- [ ] a proven callable frozen Slice II–IV execution chain;
- [ ] distinct contract, deterministic, and operational identities;
- [ ] exact Confirmed Material transport binding;
- [ ] exact response artifact and manifest contract;
- [ ] closed, bounded clarification lineage;
- [ ] non-overlapping Core, Adapter, Gateway, and Runtime validation authority;
- [ ] hard source, element, relation, lineage, response, CPU, and memory limits;
- [ ] kill-on-timeout worker isolation;
- [ ] privacy, credential, readiness, rollout, and rollback rules;
- [ ] graceful-degradation acceptance criteria for NEXAHEDRON.

## Final verdict

**Would implementation begin today?**

Not the Runtime service itself.

The frozen-execution audit and the normative specification corrections should
begin today. They are architecture-closing work, not feature development.

Runtime, Gateway, or NEXAHEDRON integration code should begin only after all
critical issues and gate conditions above are resolved. At that point, the
architecture is sufficiently complete, coherent, minimal, isolated, and safe
to implement without redesigning ORION.

The final gate verdict is therefore:

**READY WITH CHANGES — begin Gate 0 verification now; begin implementation
after the blocking contracts and operational bounds are frozen.**
