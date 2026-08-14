# ORION Version 1.1 — Clarification Lineage Contract

Status: Normative, frozen for Runtime API 1.0
Schema: `orion.clarification-lineage/1.0`
Contract version: `1.0.0`

## 1. Decision

Runtime API 1.0 uses stateless carried clarification lineage.

The complete lineage required to resolve the current
`OrientationRequest.clarification_of` reference is carried in the request
envelope. Runtime stores no session and performs no lookup.

Version 1.1 does not generate Clarification Results. The certified Slice II–IV
chain produces structural and Expression artifacts only. This contract permits
an already existing frozen `orion.clarification-result/1.0` to be referenced
without discarding its provenance.

## 2. Exact lineage shape

The `lineage` object contains exactly:

```text
schema_version
requests
clarifications
```

`schema_version` MUST equal `orion.clarification-lineage/1.0`.

- `requests` is an ordered array of prior immutable
  `orion.orientation-request/1.0` contracts.
- `clarifications` is an ordered array of prior immutable
  `orion.clarification-result/1.0` contracts.
- the current Orientation Request remains the top-level `request` and is not
  duplicated in `lineage.requests`.

Unknown or duplicate fields are rejected.

## 3. Empty lineage

When the current request has no `clarification_of`:

- `requests` MUST be empty;
- `clarifications` MUST be empty.

Supplying unrelated history is invalid. Runtime API 1.0 is not a general
session-history transport.

## 4. Complete lineage

When the current request has `clarification_of`, the arrays MUST have equal
length `N`, where `1 <= N <= 8`.

For every zero-based index `i`:

- `clarifications[i].request_id == requests[i].request_id`;
- `clarifications[i].request_version == requests[i].request_version`;
- `clarifications[i].request_schema_version == requests[i].schema_version`;
- `clarifications[i].mode == requests[i].mode`;
- the Clarification Result is contract-valid;
- the originating Orientation Request is contract-valid.

For every index `i > 0`:

- `requests[i].clarification_of.result_id ==
  clarifications[i - 1].result_id`;
- `requests[i].clarification_of.result_version ==
  clarifications[i - 1].result_version`.

The current request MUST reference `clarifications[N - 1]` by exact result ID
and version.

This forms one alternating chain:

```text
request[0]
↓
clarification[0]
↓
request[1]
↓
clarification[1]
↓
...
↓
current request
```

No branch, merge, gap, or unreferenced item is permitted.

## 5. Ordering and uniqueness

The arrays are ordered oldest to newest.

These pairs MUST be unique within the complete envelope:

- `(request_id, request_version)`;
- `(result_id, result_version)`.

Ordering is determined only by exact references, not lexical ID order or
timestamps. Timestamps are not required and do not affect replay.

Every reference MUST resolve exactly once.

## 6. Human-controlled changes

Each follow-up request is validated from the beginning. Prior readiness does
not make a later request ready.

Retained Human-controlled values MUST remain exact unless the follow-up request
explicitly changes them. A change to:

- source content;
- source identity or version;
- Orientation Object identity or version;
- Human authority;
- intention;
- consequential scope;

requires a new exact request version. A source or Orientation Object change
also requires a new `orion.confirmed-material/1.0` confirmation matching the
current request.

Gateway MUST NOT infer a delta by comparing prose. It validates exact frozen
fields and references only.

## 7. Size limits

- maximum clarification depth: `8`;
- maximum prior requests: `8`;
- maximum prior Clarification Results: `8`;
- maximum canonical `lineage` object size: `1,000,000` bytes;
- lineage bytes count toward the total `2,000,000` byte request limit.

No truncation or pagination is permitted.

## 8. Canonical serialization and replay

The lineage object uses `ORION Canonical JSON 1.0`.

The complete lineage is included in the Deterministic Request Digest. Equal
current requests with unequal lineages therefore have unequal Request Digests.

Canonical replay requires:

- byte-identical prior request contracts;
- byte-identical Clarification Result contracts;
- identical array order;
- identical current request;
- identical Confirmed Material.

Runtime, Gateway, and Adapter store no hidden clarification state.

## 9. Validation authority

Gateway:

- validates the lineage schema;
- validates each frozen public contract with its existing validator;
- resolves exact references;
- checks ordering, uniqueness, closure, depth, and size;
- computes no clarification answer.

Runtime transports the validated envelope only. The Core Invocation Adapter
does not receive lineage as a structural algorithm input. The frozen Core is
unchanged.

## 10. Error conditions

Gateway returns `422` with category `lineage_validation` when:

- lineage is non-empty without `clarification_of`;
- lineage is empty with `clarification_of`;
- an array length differs;
- a contract is invalid or has an unsupported version;
- a request-to-result link differs;
- the current reference does not identify the final result;
- a reference is missing, duplicated, ambiguous, reordered, or unrelated;
- an identity-version pair repeats;
- depth or canonical lineage size exceeds its limit;
- current Confirmed Material no longer matches the current request.

HTTP `409` is not used by Runtime API 1.0 for missing or malformed lineage.
There is no Runtime-generated `clarification_required` outcome in Version 1.1.

The error response identifies only the failed contract identity and rule. It
does not copy Human content.

## 11. Failure boundary

Lineage validation completes before Core invocation. A failed lineage enters
no Core stage and produces no ORION artifact.

No component may discard `clarification_of`, replace an earlier result ID,
repair a chain, select a Human answer, or create a synthetic Clarification
Result.
