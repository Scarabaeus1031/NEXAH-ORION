# ORION Version 1.1 — Artifact Manifest Contract

Status: Normative, frozen for Runtime API 1.0
Schema: `orion.runtime-artifact-manifest/1.0`
Contract version: `1.0.0`

## 1. Purpose

The Artifact Manifest makes one successful frozen Core execution
self-contained, ordered, integrity-verifiable, and replayable.

Runtime and Gateway MUST NOT invent, repair, omit, rename, or reorder Core
artifacts.

## 2. Representation choice

Runtime API 1.0 returns embedded canonical artifact bodies. It does not return
unresolvable storage references and does not introduce an artifact store.

Each body remains a frozen Core artifact. Embedding it in the transport
envelope grants no new Runtime authority over it.

## 3. Manifest schema

The manifest object contains exactly:

```text
schema_version
artifact_count
artifacts
terminal_artifact_ref
```

`schema_version` MUST equal `orion.runtime-artifact-manifest/1.0`.

Each `artifacts` entry contains exactly:

```text
ordinal
artifact_kind
artifact_version
artifact_ref
canonical_byte_length
body
```

Rules:

- `ordinal` is a zero-based contiguous integer;
- `artifact_kind` is the exact value in Section 4;
- `artifact_version` is the artifact's frozen schema or diagnostic version;
- `artifact_ref` is `sha256:<digest>` of the exact frozen canonical bytes;
- `canonical_byte_length` is the byte length of those bytes;
- `body` is the parsed JSON value represented by those exact canonical bytes.

Unknown manifest or entry fields are rejected.

## 4. Canonical artifact order

The manifest MUST contain exactly these 22 entries:

| Ordinal | `artifact_kind` | Frozen canonical serializer |
|---:|---|---|
| 0 | `structural_representation` | `canonical_representation_bytes` |
| 1 | `source_element_inventory` | `canonical_inventory_bytes` |
| 2 | `structural_summary` | `canonical_structural_summary_bytes` |
| 3 | `structural_statistics` | `canonical_structural_statistics_bytes` |
| 4 | `sequential_relation_set` | `canonical_sequential_relation_set_bytes` |
| 5 | `structural_equality_relation_set` | `canonical_structural_equality_relation_set_bytes` |
| 6 | `declared_reference_relation_set` | `canonical_declared_reference_relation_set_bytes` |
| 7 | `relation_conformance` | `canonical_relation_conformance_report_bytes` |
| 8 | `relations_certification` | `canonical_relations_certification_report_bytes` |
| 9 | `navigation_object` | `canonical_navigation_object_bytes` |
| 10 | `constructed_navigation` | `canonical_constructed_navigation_bytes` |
| 11 | `navigation_conformance` | `canonical_navigation_conformance_report_bytes` |
| 12 | `navigation_certification` | `canonical_navigation_certification_report_bytes` |
| 13 | `orientation_map_object` | `canonical_orientation_map_object_bytes` |
| 14 | `constructed_orientation_map` | `canonical_constructed_orientation_map_bytes` |
| 15 | `orientation_map_conformance` | `canonical_orientation_map_conformance_report_bytes` |
| 16 | `slice_iii_certification` | `canonical_slice_iii_certification_report_bytes` |
| 17 | `expression_contract` | `canonical_expression_contract_bytes` |
| 18 | `expression_artifact` | `canonical_expression_artifact_bytes` |
| 19 | `expression_conformance` | `canonical_expression_conformance_report_bytes` |
| 20 | `expression_certification` | `canonical_expression_certification_report_bytes` |
| 21 | `slice_iv_certification` | `canonical_slice_iv_certification_report_bytes` |

Projection Mapping and intermediate validation diagnostics are required during
execution but are not public manifest artifacts because they have no frozen
public canonical artifact contract. Their successful completion is evidenced
by the accepted conformance and certification chain.

## 5. Identity and integrity verification

For every entry, Gateway MUST:

1. validate the body using its frozen artifact type;
2. serialize it with the listed frozen serializer;
3. compare the exact length to `canonical_byte_length`;
4. compare SHA-256 to `artifact_ref`;
5. verify all native identity and integrity fields through the frozen type;
6. verify references to earlier entries resolve exactly;
7. verify no later entry is referenced by an earlier construction stage unless
   the frozen contract explicitly permits it.

The Manifest's `terminal_artifact_ref` MUST equal entry 21's `artifact_ref`.
The success response's `terminal_certification_ref` MUST equal the same value.

## 6. Manifest canonicalization

The manifest is serialized with `ORION Canonical JSON 1.0`. Embedded bodies
MUST reproduce their frozen canonical bytes when passed through their frozen
serializers.

The manifest itself does not replace native artifact identities. Its SHA-256
reference binds ordered transport assembly only.

## 7. Limits

- exactly `22` entries;
- maximum complete canonical manifest size: `16,000,000` bytes;
- maximum complete canonical success response size: `16,777,216` bytes;
- no individual artifact may exceed the manifest-size limit;
- no duplicate `artifact_ref` is permitted unless two distinct frozen stages
  genuinely produce byte-identical artifacts; Runtime 1.1 expects none.

If a successfully computed Core chain exceeds a limit, the worker output is
discarded and the Runtime returns an operational output-limit error. It MUST
NOT truncate, paginate, compress, or partially publish the manifest.

## 8. Authorization and privacy

The manifest is returned only to the authenticated service consumer that
submitted the request. Runtime API 1.0 provides no anonymous artifact endpoint,
reference resolver, or later retrieval endpoint.

The Runtime MUST NOT persist manifest bodies after response completion. Bodies
MUST NOT enter logs, traces, metrics, crash reports, or health responses.

NEXAHEDRON may preserve the result only within its existing Human-owned
Orientation Record boundary. This contract grants no public-distribution
authority.

## 9. Failure rules

A success response is forbidden when:

- any required entry is missing or additional;
- ordering or ordinals differ;
- a body cannot be reproduced by its frozen serializer;
- a digest, byte length, native identity, integrity value, reference, decision,
  or STOP differs;
- terminal certification is not `certified`;
- terminal STOP is not `at_slice_iv_certified`;
- a limit is exceeded.

Gateway reports one deterministic output-validation failure and publishes no
manifest.
