# ORION Version 1.1 — Operational Boundary Contract

Status: Normative, frozen for Runtime API 1.0
Runtime version: `1.1.0`
Contract version: `1.0.0`

## 1. Purpose

This contract defines the operational conditions under which the frozen ORION
Core may be invoked publicly. These limits govern admission, isolation, and
publication. They do not change Core semantics or artifacts.

## 2. Process boundary

The HTTP Runtime and Core execution MUST be separate processes.

Each accepted request receives a fresh or reset isolated Core worker that:

- processes one invocation at a time;
- has no outbound network access;
- runs as a non-root identity;
- uses a read-only application and Core filesystem;
- receives only the validated canonical input;
- can write only to bounded ephemeral memory or temporary storage;
- is terminated after success, failure, or timeout;
- cannot publish directly to the network.

Only the parent Runtime may return an HTTP response.

## 3. Fixed limits

### 3.1 HTTP admission

| Limit | Value |
|---|---:|
| Request body | `2,000,000` bytes |
| Request headers combined | `32,768` bytes |
| Header count | `50` |
| Content encoding | `identity` only |
| Header-read timeout | `5` seconds |
| Body-read timeout | `10` seconds |
| Total request wall time | `30` seconds |

Chunked input MAY be accepted only when the accumulated decoded body remains
within the body limit. Compressed input is rejected.

### 3.2 Confirmed Material and lineage

| Limit | Value |
|---|---:|
| Confirmed UTF-8 content | `262,144` bytes |
| Physical lines | `8,192` |
| Clarification depth | `8` |
| Canonical lineage | `1,000,000` bytes |

### 3.3 Core result

| Limit | Value |
|---|---:|
| Declared elements including document | `128` |
| Final Relation Objects | `16,384` |
| Manifest entries | exactly `22` |
| Canonical manifest | `16,000,000` bytes |
| Complete canonical success response | `16,777,216` bytes |

### 3.4 Worker resources

| Limit | Value |
|---|---:|
| Core wall time | `15` seconds |
| Core CPU time | `15` seconds |
| Worker address-space memory | `512 MiB` |
| Worker temporary storage | `64 MiB` |
| Worker open file descriptors | `64` |
| Concurrent workers per service credential | `2` |
| Runtime container memory | `1,536 MiB` |
| Runtime container process limit | `32` |

Limits are measured per invocation unless stated otherwise.

## 4. Kill-on-timeout

At the Core wall-time limit, Runtime MUST:

1. stop accepting worker output;
2. terminate the worker;
3. forcibly kill it if it remains alive one second later;
4. discard every partial artifact and temporary byte;
5. return `504` with `Retry-After`;
6. keep no completion callback capable of publishing later.

An application-language exception or cooperative cancellation alone is
insufficient.

CPU, memory, process, file, or temporary-storage exhaustion also terminates the
worker and publishes no partial result.

## 5. Admission and limit errors

| Condition | HTTP status | Stable code |
|---|---:|---|
| HTTP body exceeds limit | `413` | `request_body_too_large` |
| Headers exceed limit | `431` | `request_headers_too_large` |
| Unsupported compression | `415` | `content_encoding_unsupported` |
| Material, lineage, element, relation, manifest, or response profile exceeds a deterministic published bound | `422` | `operational_profile_exceeded` |
| Rate or concurrency limit reached | `429` | `capacity_limited` |
| Worker exceeds wall or CPU time | `504` | `core_timeout` |
| Worker becomes unavailable before invocation | `503` | `core_worker_unavailable` |
| Worker fails unexpectedly | `500` | `core_worker_failed` |

Errors do not modify or truncate the input.

## 6. Rate limits

Runtime enforces:

- `30` POST attempts per service credential per rolling minute;
- burst capacity `5`;
- `2` concurrent Core workers per service credential;
- `60` health requests per source IP per minute.

NEXAHEDRON's same-origin edge MUST also enforce a per-client limit before using
the shared Runtime credential. Runtime rate-limit state is operational and
never enters Core identity or replay.

## 7. Startup verification

Before readiness, Runtime MUST:

1. verify the configured Runtime release manifest;
2. verify Core commit
   `d34fbb2f99334534f4db89465a29f8bdb16d14d3`;
3. reproduce Core fingerprint
   `6201362c094530a0a31fa3d80b46c9131011bb8c8d400183271b0da0eb423f8d`;
4. resolve every callable in the Slice Execution Contract;
5. verify all required canonical serializers;
6. run one packaged, content-free or non-sensitive deterministic canary twice
   in isolated workers;
7. verify byte-identical manifest and terminal certification;
8. verify the terminal STOP `at_slice_iv_certified`.

Any failure leaves the process not ready. Runtime MUST NOT substitute another
Core version.

## 8. Readiness

`GET /health` is the Version 1.1 readiness endpoint.

It returns `200` only when:

- startup verification passed;
- the configured worker boundary can accept work;
- shutdown has not begun;
- Core commit and fingerprint remain verified.

Otherwise it returns `503`.

The body contains only:

```text
status
runtime_version
api_version
core_version
core_fingerprint
```

Health performs no Orientation, contains no Human data, and uses
`Cache-Control: no-store`.

## 9. Logging and privacy

Runtime logs only:

- Operational Execution ID;
- authorized service-consumer identity;
- API and Runtime versions;
- Core fingerprint;
- request byte count;
- stage boundary;
- status and stable error code;
- bounded duration and resource measurements.

It MUST NOT log:

- Authorization values;
- request or response bodies;
- Confirmed Material content;
- Human annotations;
- artifact bodies;
- clarification issues or retained context;
- source references when they contain Human-controlled data.

Operational logs have a maximum retention of `30` days and MUST be deletable.
Metrics MUST use bounded labels; Human- or caller-provided identifiers MUST NOT
be metric labels.

## 10. Credentials

POST requires a service credential. The browser never receives it.

The operational contract requires:

- secret storage outside image and repository;
- comparison without observable value disclosure;
- immediate revocation;
- rotation with at most `24` hours of two-key overlap;
- no credential in URLs, bodies, logs, metrics, or Core inputs.

Runtime accepts no Human cookie and creates no Human account.

## 11. Shutdown and restart

On shutdown Runtime:

1. becomes not ready;
2. stops accepting new POST requests;
3. allows an active worker no more than its existing deadline;
4. kills remaining workers;
5. publishes no partial result;
6. exits cleanly.

Restart creates no recovery obligation because Runtime holds no session or
artifact state.

## 12. Release, upgrade, and rollback

Every deployable release binds:

- Runtime version;
- API version;
- immutable container image digest;
- frozen Core commit and fingerprint;
- supported NEXAHEDRON Gateway version;
- verification evidence.

Upgrade order:

1. deploy a Runtime compatible with the current NEXAHEDRON;
2. pass readiness and deterministic canary;
3. verify an authenticated boundary request;
4. deploy or activate the compatible NEXAHEDRON integration;
5. perform a production smoke test.

Rollback MUST restore a previously verified compatible Runtime/NEXAHEDRON
pair. Runtime-only rollback is forbidden when the deployed consumer is
incompatible.

The previous image and configuration manifest remain available until
acceptance. No Human payload backup is created.

## 13. Monitoring

Minimum operational monitoring covers:

- readiness status;
- request count by bounded status class;
- rejection count by stable error code;
- worker timeout, memory termination, and unexpected failure;
- rate and concurrency saturation;
- response-size distribution;
- restart count;
- Core fingerprint mismatch.

Monitoring does not inspect source content or artifact meaning.

## 14. Publication boundary

Only a complete, verified manifest ending at `at_slice_iv_certified` may be
published as success.

Runtime never publishes after timeout, never publishes from a killed worker,
and never publishes a partial chain.
