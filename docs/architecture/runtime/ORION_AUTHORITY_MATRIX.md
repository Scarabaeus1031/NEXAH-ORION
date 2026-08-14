# ORION Version 1.1 — Authority Matrix

Status: Normative, frozen for Runtime API 1.0
Contract version: `1.0.0`

## 1. Purpose

This matrix assigns every Version 1.1 responsibility to exactly one owner.
Reading or transporting an artifact does not transfer its authority.

Legend:

- **O** — sole owner;
- **R** — may read, carry, or invoke only as specified;
- **—** — no responsibility or authority.

Each scoped row contains exactly one **O**.

## 2. Definitive matrix

| Scoped responsibility | Human Workspace | NEXAHEDRON | Gateway | Runtime | Core Invocation Adapter | Frozen ORION Core |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| Human intention, scope, continuation, and decision authority | **O** | R | R | — | — | R |
| Human confirmation of Working Material | **O** | R | R | — | — | R |
| Construction of immutable Confirmed Material wire artifact | R | **O** | R | R | R | R |
| Orientation Request construction from confirmed Human choices | R | **O** | R | R | R | R |
| Browser-facing interaction and graceful degradation | R | **O** | — | — | — | — |
| Same-origin browser proxy and per-client edge rate limit | — | **O** | R | R | — | — |
| HTTP transport, TLS termination contract, headers, body reading, and response publication | — | R | R | **O** | — | — |
| Service authentication and Runtime rate/concurrency admission | — | R | — | **O** | — | — |
| Transport-envelope schema and version validation | — | R | **O** | R | — | — |
| Confirmed Material wire validation and request-to-material matching | R | R | **O** | R | — | — |
| Clarification lineage closure validation | R | R | **O** | R | — | — |
| Deterministic Request Digest | — | R | **O** | R | — | — |
| Operational Execution ID | — | R | R | **O** | — | — |
| Mapping validated Confirmed Material to `ConfirmedMarkdownSource` | — | — | R | R | **O** | R |
| Frozen entry-point orchestration in the certified order | — | — | R | R | **O** | R |
| Deterministic Projection and Renderer execution | — | — | — | — | R | **O** |
| UNDERSTAND Inventory, Summary, and Statistics execution | — | — | — | — | R | **O** |
| Relations, Navigation, and Orientation Map execution | — | — | — | — | R | **O** |
| Expression Contract, Construction, and certified Expression execution | — | — | — | — | R | **O** |
| Core artifact validation and External Conformance | — | — | R | — | R | **O** |
| Core certification and certified STOPs | — | — | R | — | R | **O** |
| Core artifact identity, integrity, ordering, and canonical serialization | — | — | R | — | R | **O** |
| Source confirmation provenance | **O** | R | R | R | R | R |
| Core transformation and certification provenance | — | — | R | — | R | **O** |
| Manifest assembly from exact Core canonical bytes | — | — | **O** | R | R | R |
| Manifest transport-boundary verification | — | — | **O** | R | R | R |
| Deterministic Result Digest | — | R | **O** | R | — | — |
| Operational logging, metrics, retention, and deletion | — | — | R | **O** | — | — |
| Transport, authentication, rate, capacity, and timeout errors | — | R | R | **O** | — | — |
| Envelope, material, lineage, and manifest boundary errors | — | R | **O** | R | — | — |
| Adapter mapping and invocation-boundary errors | — | — | R | R | **O** | R |
| Deterministic Core rejection and failed Core conformance | — | — | R | R | R | **O** |
| Runtime readiness and startup fingerprint verification | — | — | R | **O** | R | R |
| Retry decision in the Human interaction | **O** | R | R | R | — | — |
| Runtime deployment, restart, upgrade, and rollback | — | — | — | **O** | — | — |
| Human-owned Orientation Record preservation | **O** | R | — | — | — | — |

## 3. Component boundaries

### 3.1 Human Workspace

Owns Human choices, confirmation, retry, Rest, and the Human-owned Orientation
Record. It never validates Core artifacts or performs ORION execution.

### 3.2 NEXAHEDRON

Owns the Human-facing integration, creation of transport artifacts from
explicit Human choices, the same-origin proxy, and graceful degradation. It
does not certify ORION results.

### 3.3 Gateway

Owns deterministic boundary admission and assembly:

- wire contracts;
- exact lineage;
- request/material identity;
- Request Digest;
- exact manifest assembly and boundary verification;
- Result Digest.

It does not perform Core conformance, certification, repair, or semantics.

### 3.4 Runtime

Owns operational execution conditions:

- HTTP;
- authentication;
- rate and resource limits;
- workers;
- timeout;
- readiness;
- logging;
- response publication;
- deployment and rollback.

It never creates or validates an ORION artifact.

### 3.5 Core Invocation Adapter

Owns only the mechanical mapping and ordered invocation of frozen callable
entry points. It does not own the behavior of those entry points or the
artifacts they produce.

### 3.6 Frozen ORION Core

Solely owns deterministic Orientation execution, Core artifact identity and
serialization, conformance, certification, provenance created by Core stages,
and all certified STOPs.

## 4. Non-transfer rules

- Transporting an artifact does not grant authority over it.
- Embedding an artifact does not make it a Runtime artifact.
- Checking a digest does not repeat Core certification.
- Invoking a callable does not transfer its responsibility to the Adapter.
- Presenting an ORION result does not transfer Human judgment to ORION.
- An operational success does not assert semantic truth.
- No error handler may repair a contract owned by another component.

## 5. Conflict rule

If an implementation would place two **O** assignments on one scoped
responsibility, it violates this contract and MUST stop before merge or
deployment.
