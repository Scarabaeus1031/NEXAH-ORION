# ORION Version 1.1 — Gate 0 Execution Proof

Status: **PASS WITH LIMITATIONS**

## 1. Purpose

This proof establishes that the frozen ORION Version 1 Core can be invoked
through the frozen Version 1.1 execution contracts without using the historical
Runtime or Gateway and without modifying any Core module.

The verification harness is:

`scripts/orion_gate0_execution_proof.py`

It is a test-only supervisor and worker. It is not the Runtime, Gateway,
Core Invocation Adapter, or production code.

## 2. Frozen baseline

| Property | Verified value |
|---|---|
| Frozen Core commit | `d34fbb2f99334534f4db89465a29f8bdb16d14d3` |
| Frozen Core fingerprint | `6201362c094530a0a31fa3d80b46c9131011bb8c8d400183271b0da0eb423f8d` |
| Invocation contract | `1.0.0` |
| Confirmed Material schema | `orion.confirmed-material/1.0` |
| Terminal schema | `orion.slice-iv-certification/0.1-alpha` |
| Terminal STOP | `at_slice_iv_certified` |

The canonical fingerprint was reproduced independently with
`scripts/orion-v1-fingerprint`.

## 3. Canonical proof input

The harness constructed one canonical Confirmed Material artifact containing a
bounded CommonMark 0.31.2 document, one matching frozen Orientation Request,
an empty clarification lineage, and no Evidence.

The Confirmed Material was mapped to `ConfirmedMarkdownSource.create` exactly
as defined by the frozen execution contract. The resulting source revision,
content SHA-256, confirmation identity, CommonMark version, and whole-document
boundary were checked before Core execution.

Deterministic Request Digest:

`sha256:4aa3941b6378280a265327ce2c42af7bd2f0526913480eda78b2f9c9c914c354`

No Operational Execution ID entered the canonical input, Core artifacts,
manifest, or deterministic result identity.

## 4. Invocation result

All 31 frozen callable stages were resolved and invoked in normative order:

1. Confirmed Markdown Source creation
2. Markdown Projection
3. Structural Rendering
4. Representation Conformance
5. Source Element Inventory
6. Structural Summary
7. Summary validation
8. Structural Statistics
9. Statistics validation
10. Sequential Relations
11. Sequential Relation validation
12. Structural Equality Relations
13. Structural Equality validation
14. Declared Reference Relations
15. Declared Reference validation
16. External Relation Conformance
17. Relations Certification
18. Navigation Object
19. Navigation Construction
20. External Navigation Conformance
21. Navigation Certification
22. Orientation Map Object
23. Orientation Map Construction
24. External Orientation Map Conformance
25. Slice III Certification
26. Expression Contract
27. Expression Contract validation
28. Expression Construction
29. External Expression Conformance
30. Expression Certification
31. Slice IV Certification

Every validation, conformance decision, and certification succeeded before its
dependent stage ran.

| Result | Value |
|---|---:|
| Frozen callable stages invoked | `31` |
| Manifest artifacts | `22` |
| Structural elements | `5` |
| Final relation objects | `15` |
| Manifest canonical bytes | `112723` |
| Manifest reference | `sha256:e1a879bf9869be43e50519d25e066977fbcec6e612327afa3a103fb806f13a3c` |
| Deterministic Result Digest | `sha256:430008906972034e65989614e11318bb2dd487a9d1d74884bf03189a598b8030` |
| Terminal certification ID | `slice-iv-certification-8dd9ff1cd10e414d2cdea7cf` |
| Terminal certification reference | `sha256:6114accd7a4f662dcee593414b8253eeb7e3b2cc947b11392978a3f13b1eb82a` |
| Terminal STOP | `at_slice_iv_certified` |

## 5. Boundary verification

The harness verified that:

- no file under `src/orion` changed during either execution;
- neither `orion.gateway` nor `orion.orientation_runtime` was loaded;
- no historical Runtime, Gateway, shortcut, or compatibility layer executed;
- the fixed Expression declarations were supplied exactly as frozen;
- declared cross-reference input was the required empty tuple;
- canonical serializers from the frozen artifact modules were used;
- the terminal certification was produced by the frozen Slice IV callable;
- all proof input and output measurements were within the frozen operational
  profile.

The existing Slice II, Slice III, and Slice IV certification proofs were also
replayed successfully with:

```text
make slice-ii-certification slice-iii-certification slice-iv-certification
```

WP11, WP25, and WP30 each reported successful certification and
byte-identical replay.

## 6. Contract verification

| Contract | Gate 0 verification |
|---|---|
| Slice Execution Contract | All 31 entry points executed in order; terminal Slice IV certification reached |
| Identity Contract | Request and Result digests were deterministic; no operational identity entered deterministic artifacts |
| Confirmed Material Contract | Canonical input, integrity, mapping, and bounds verified |
| Artifact Manifest Contract | Exact 22-entry order, canonical bytes, references, and manifest integrity verified |
| Clarification Contract | Empty lineage accepted and canonically represented; non-empty lineage was not applicable to this proof |
| Operational Boundary | Accepted-input limits and supervisor timeout were checked; production resource isolation remains unimplemented |
| Authority Matrix | Harness performed only Core invocation and verification; no transport, Gateway, Runtime, or Human authority was assumed |

## 7. Non-blocking harness correction

An initial pre-proof run reached the terminal Core artifact and then stopped
while assembling the verification manifest because the harness looked only for
a generic `schema_version` field. The frozen Navigation Object and Orientation
Map Object expose their frozen versions as `navigation_schema_version` and
`orientation_map_schema_version`.

The correction changed only the test harness's explicit version-field mapping.
No Core source, contract, artifact, serializer, or execution behavior changed.
Both recorded proof executions were performed after that correction.

## 8. Limitation

Gate 0 proves Core executability and deterministic replay. It does not prove
the production Runtime mechanisms that do not yet exist: non-root sandboxing,
read-only filesystems, disabled network access, hard CPU and address-space
limits, bounded temporary storage and file descriptors, forced worker
termination, HTTP admission, rate limiting, or readiness orchestration.

These are mandatory implementation constraints in the frozen Operational
Boundary Contract. They are not frozen Core defects and require no Core
change.

## 9. Conclusion

The frozen ORION Core is directly executable through the Version 1.1
invocation contract. It reaches the certified Slice IV STOP, emits the complete
manifest vocabulary, preserves deterministic identities and provenance, and
replays byte-identically without the historical Runtime or Gateway.

Runtime implementation may begin subject to the operational limitation stated
above.
