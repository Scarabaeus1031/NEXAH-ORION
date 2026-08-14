# ORION Version 1.1 — Identity Contract

Status: Normative, frozen for Runtime API 1.0
Contract version: `1.0.0`

## 1. Purpose

This contract separates contract identity, deterministic transport identity,
deterministic result identity, and operational correlation. No identifier may
serve more than one of these authorities.

## 2. Canonical serialization

Digests defined here use `ORION Canonical JSON 1.0`:

- UTF-8 without BOM;
- JSON object keys sorted lexicographically by Unicode code point;
- array order preserved;
- no insignificant whitespace;
- strings encoded as JSON strings;
- integers encoded in base 10 without leading zeroes;
- only objects, arrays, strings, integers, booleans, and `null`;
- floating-point numbers forbidden;
- duplicate object keys forbidden;
- invalid UTF-8 and non-canonical input rejected.

SHA-256 is applied to the resulting bytes and rendered as 64 lowercase
hexadecimal characters.

## 3. Contract Request ID

### Definition

The Contract Request ID is the `request_id` already owned by the immutable
`orion.orientation-request/1.0` contract.

### Authority

The Human Workspace originates it through the existing request-creation
boundary. NEXAHEDRON transports it unchanged. Runtime components do not
generate, replace, normalize, or reinterpret it.

### Permitted locations

- contained Orientation Request;
- success response `request_id`;
- deterministic error detail reference when safe;
- provenance references inside frozen contracts that already permit it.

### Forbidden uses

It MUST NOT:

- identify an HTTP attempt;
- serve as a content digest;
- prove byte equality;
- become a log or metric cardinality source without bounded sanitization;
- be changed on retry of the same immutable contract.

Two different immutable request versions MUST have distinct frozen contract
identities according to the existing public contract rules.

## 4. Deterministic Request Digest

### Definition

`request_digest` is:

```text
sha256:<SHA-256 of canonical request-digest basis>
```

The request-digest basis contains exactly:

```text
api_version
request
confirmed_material
lineage
evidence
```

It excludes authentication, HTTP headers, Runtime version, Core version,
operational execution identity, timestamps, host data, and rate-limit state.

### Authority

The Gateway computes it after structural validation and before Core
invocation. It does not alter the contained contracts.

### Permitted locations

- canonical success response;
- canonical operational error response after a complete valid body is parsed;
- Artifact Manifest provenance;
- deterministic replay records.

### Properties

Equal accepted canonical envelopes produce equal Request Digests. Any byte-
significant change to a contained contract, material, lineage entry, or
Evidence array produces a different digest.

## 5. Deterministic Result Digest

### Definition

`result_digest` is:

```text
sha256:<SHA-256 of canonical result-digest basis>
```

The result-digest basis contains exactly:

```text
api_version
request_digest
core_release
status
terminal_stop
artifact_manifest
terminal_certification_ref
```

The Artifact Manifest is the canonical manifest defined by
`ORION_ARTIFACT_MANIFEST_CONTRACT.md`.

### Authority

The Gateway computes the Result Digest after the frozen Core has produced a
complete terminal chain and after manifest boundary verification.

### Permitted locations

- canonical success response;
- deterministic replay evidence;
- NEXAHEDRON's immutable ORION result reference.

### Forbidden inputs

Operational execution IDs, timestamps, retry counts, deployment identities,
HTTP headers, and logs MUST NOT enter the Result Digest.

## 6. Operational Execution ID

### Definition

`ORION-Execution-ID` is an opaque, per-attempt correlation identifier. It is
either:

- a caller-supplied value matching `^[A-Za-z0-9][A-Za-z0-9._:-]{0,63}$`; or
- a Runtime-generated UUID version 4 in lowercase canonical form.

The Runtime MUST generate a new value when no valid caller value is supplied.
An invalid supplied value is rejected with `400`.

### Authority

Runtime owns this identifier. It identifies one HTTP attempt, not one ORION
request or result.

### Permitted locations

- request header `ORION-Execution-ID`;
- response header `ORION-Execution-ID`;
- operational logs and traces;
- operational error response body.

### Forbidden locations and uses

It MUST NOT appear in:

- a frozen Core input;
- a Core artifact;
- the canonical success response body;
- Request Digest or Result Digest;
- certification, provenance, or artifact identity.

A retry MAY use a new Operational Execution ID while preserving the same
Request Digest and Result Digest.

## 7. Identifier matrix

| Identifier | Owner | Deterministic | Canonical success body | HTTP header | Core input | Logs |
|---|---|---:|---:|---:|---:|---:|
| Contract Request ID | Human Workspace | Per frozen contract | Yes | No | Only where existing contract requires | Sanitized |
| Request Digest | Gateway | Yes | Yes | MAY | No | Yes |
| Result Digest | Gateway | Yes | Yes | MAY | No | Yes |
| Operational Execution ID | Runtime | No | No | Yes | Never | Yes |

## 8. Retry and replay

- Same immutable envelope, new attempt: same Request Digest.
- Same accepted envelope and frozen Core: same Result Digest.
- Same attempt: one Operational Execution ID.
- New attempt: Operational Execution ID may differ.
- A changed Human request or changed Confirmed Material is not a retry; it is a
  new deterministic request.

## 9. Errors

Before a complete body is parsed, no Request Digest exists. The error response
MUST omit it.

After the accepted envelope is canonicalized, errors MAY carry the Request
Digest. No Result Digest exists unless the complete certified result and
manifest were produced.

No component may manufacture a missing digest from partial data.
