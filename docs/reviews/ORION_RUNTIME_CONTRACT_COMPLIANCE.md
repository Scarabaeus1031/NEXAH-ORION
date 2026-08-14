# ORION Version 1.1 — Runtime Contract Compliance

Audit date: 2026-07-24

## Compliance scale

- **Conformant** — every audited normative requirement is implemented and
  evidenced.
- **Partially conformant** — the principal contract is implemented but one or
  more normative requirements are absent or unproven.
- **Nonconformant** — a mandatory requirement is contradicted by implementation
  or reproduced behavior.

## Summary matrix

| Frozen contract | Status | Principal reason |
|---|---|---|
| Slice Execution Contract | Partially conformant | ordered execution passes; actual release precondition and post-projection admission do not |
| Identity Contract | Conformant on audited paths | identifier authorities and digest bases remain separated |
| Confirmed Material Contract | Partially conformant | schema and integrity pass; published profile-error code and admission timing differ |
| Artifact Manifest Contract | Nonconformant | cross-entry reference graph is not verified |
| Clarification Lineage Contract | Partially conformant | implementation and one-level audit pass; complete boundary suite is absent |
| Operational Boundary | Nonconformant | network isolation, startup verification, lifecycle, and limits fail mandatory rules |
| Authority Matrix | Partially conformant | Core semantics remain separated; Gateway and Runtime do not fully discharge assigned duties |

## 1. Certified Slice II–IV Invocation Contract

### Conformant

- Confirmed Material maps to `ConfirmedMarkdownSource` using the frozen fields.
- Source revision, content digest, and confirmation identity are compared.
- The 31 frozen callables are invoked in declared order.
- Required conformance and validation stages execute before downstream stages.
- Evidence is empty.
- declared cross-reference declarations are empty.
- fixed Expression declarations match exactly.
- no historical Runtime, historical Gateway, LYRA, or SIRIUS path is called.
- input canonical bytes are checked for mutation.
- the terminal Slice IV STOP is reached.
- independent replay is byte-identical.

### Deviations

- The actual checked-out commit is not verified in the container; an
  environment assertion substitutes for repository evidence.
- The frozen fingerprint does not cover the invoked Slice II–IV modules.
- the 128-element post-projection limit is checked only after the complete
  chain.
- certification decisions are mostly relied upon through downstream
  constructors rather than checked explicitly at each Adapter boundary.

Status: **Partially conformant**

## 2. Identity Contract

### Conformant

- Contract Request ID is preserved in the success body.
- Request Digest uses exactly API version, request, Confirmed Material,
  lineage, and Evidence.
- Result Digest uses the declared basis.
- Operational Execution ID is absent from Core input, artifacts, both
  deterministic digests, and the canonical success body.
- caller IDs are syntax-bounded;
- absent IDs receive a lowercase UUIDv4;
- retry attempts may use different operational IDs without changing result
  identity.

### Observation

An invalid caller-provided execution ID is rejected but the rejection receives
a newly generated operational ID. This remains within the permitted
operational authority.

Status: **Conformant on audited paths**

## 3. Confirmed Material Contract

### Conformant

- exact top-level, source, and confirmation fields;
- schema, media type, CommonMark version, and whole boundary;
- strict UTF-8 content, BOM/NUL/CR rejection;
- content byte and line limits;
- SHA-256 source integrity and source-version binding;
- confirmation revision range and deterministic confirmation ID;
- exact request/material source identity binding;
- no repair, dereference, or semantic interpretation.

### Deviations

- source content profile excess is returned as `contract_invalid` rather than
  the Operational Boundary's stable `operational_profile_exceeded`;
- post-projection element and relation admission is delayed until after the
  full Core chain.

Status: **Partially conformant**

## 4. Artifact Manifest Contract

### Conformant

- exact manifest and entry fields;
- exact count of 22;
- contiguous ordinals and canonical artifact kinds;
- frozen canonical reserialization;
- byte length and SHA-256 verification;
- duplicate reference rejection;
- terminal artifact reference;
- manifest-size limit;
- terminal decision and STOP.

### Deviations

The verifier processes each artifact independently. It does not:

- resolve every reference to the exact earlier manifest entry;
- reject references to later entries where not explicitly permitted;
- recompute the complete cross-layer reference graph.

Those are explicit mandatory steps in Artifact Manifest Contract Section 5.

Status: **Nonconformant**

## 5. Clarification Lineage Contract

### Conformant

- exact lineage shape and schema;
- empty lineage when no clarification reference exists;
- equal request/result cardinality;
- maximum depth and canonical size;
- prior request and Clarification Result validation;
- exact pairwise lineage, final reference, ordering, and uniqueness;
- no Runtime storage or lookup;
- lineage enters Request Digest but not structural Core input.

An independent valid one-level lineage reached the terminal Slice IV STOP.

### Evidence gaps

Repository tests do not cover:

- any valid non-empty lineage;
- maximum depth;
- maximum lineage size;
- reordered, branched, duplicated, or incomplete lineage;
- changed material across a follow-up;
- replay equality for a non-empty lineage.

Status: **Partially conformant pending complete boundary evidence**

## 6. Operational Boundary Contract

### Conformant

- parent HTTP process and child Core worker are separate;
- one fresh child is created per invocation;
- wall timeout terminates the process group and escalates to SIGKILL;
- CPU, address-space on Linux, file-size, and open-file limits are attempted;
- canonical worker input and bounded worker output;
- authentication and per-credential worker concurrency;
- rolling and burst limits;
- health rate limiting;
- content-free logs on inspected paths;
- no artifact persistence;
- success requires a complete terminal manifest.

### Deviations

- worker outbound network access is possible;
- mandatory startup canary can be disabled;
- actual Runtime/Core release identity is not proven;
- Runtime release-manifest verification is absent;
- total request wall time is not implemented as one deadline;
- CPU timeout status can differ from the required `504`;
- temporary storage is not bounded per invocation;
- shutdown does not track and kill active workers explicitly;
- post-projection operational limits are checked late;
- health does not revalidate release identity after startup;
- Runtime container/image compatibility data are not bound;
- monitoring and 30-day deletion controls are documentation only.

Status: **Nonconformant**

## 7. Authority Matrix

### Preserved authorities

- Frozen Core remains the only owner of structural algorithms, conformance,
  certification, artifact identity, and Core provenance.
- Adapter remains mechanical.
- Runtime does not produce semantic artifacts.
- Human request and confirmation authority are transported rather than
  reinterpreted.
- Operational identities remain Runtime-owned.

### Incomplete assigned duties

- Gateway does not perform complete manifest graph verification.
- Runtime does not perform the frozen release/readiness verification assigned
  to it.
- Runtime does not enforce the complete operational isolation and lifecycle
  boundary assigned to it.

Status: **Partially conformant**

## Error-contract observations

The declared stable error surface is not completely uniform:

- profile-limit failures can use `contract_invalid`;
- CPU exhaustion can become `core_worker_failed`;
- unsupported HTTP methods return inherited HTML rather than the Runtime error
  envelope.

These responses are operational, not Core outcomes, but their inconsistency
matters to a deterministic Gateway consumer.

## Compliance conclusion

The implementation complies with the frozen deterministic execution path but
does not comply with the complete public Runtime boundary. No Core or
architectural change is required to close the observed gaps; the existing
frozen contracts already specify the required behavior.
