# ORION Version 1.1 — Gate 0 Replay Report

Status: **PASS**

## 1. Replay method

The Gate 0 supervisor started two independent worker processes. Each worker:

1. reconstructed the same canonical Confirmed Material from fixed proof data;
2. resolved the frozen Core callables independently;
3. executed the complete 31-stage Slice II–IV chain;
4. serialized every retained artifact with its frozen canonical serializer;
5. constructed and verified the complete 22-entry Artifact Manifest;
6. returned its canonical proof record to the supervisor.

The second worker did not consume artifacts, objects, temporary state, or
module state from the first worker.

## 2. Replay comparison

| Comparison | Result |
|---|---|
| Artifact count | identical |
| Artifact order | identical |
| Artifact references | identical |
| Canonical artifact bodies | byte-identical |
| Invocation call order | identical |
| Artifact Manifest | byte-identical |
| Deterministic Request Digest | identical |
| Deterministic Result Digest | identical |
| Expression artifacts | byte-identical |
| Terminal Slice IV certification | byte-identical |

Independent worker processes: `2`

Artifact count in each execution: `22`

## 3. Stable replay identities

| Identity | Initial execution | Independent replay |
|---|---|---|
| Request Digest | `sha256:4aa3941b6378280a265327ce2c42af7bd2f0526913480eda78b2f9c9c914c354` | same |
| Manifest reference | `sha256:e1a879bf9869be43e50519d25e066977fbcec6e612327afa3a103fb806f13a3c` | same |
| Result Digest | `sha256:430008906972034e65989614e11318bb2dd487a9d1d74884bf03189a598b8030` | same |
| Terminal certification reference | `sha256:6114accd7a4f662dcee593414b8253eeb7e3b2cc947b11392978a3f13b1eb82a` | same |
| Terminal STOP | `at_slice_iv_certified` | same |

## 4. Expression replay

The following Expression-layer artifacts were compared independently:

- Expression Contract
- Expression Artifact
- External Expression Conformance Report
- Expression Certification Report
- Vertical Slice IV Certification Report

All five canonical bodies and SHA-256 references were byte-identical.

## 5. Core immutability

Each worker hashed every Python source below `src/orion` before and after Core
execution. The before and after maps were identical in both processes.

No historical Runtime or Gateway module was loaded in either execution.

## 6. Existing certification replay

The canonical WP11, WP25, and WP30 proof programs were run after the Gate 0
replay. They independently confirmed:

- Slice II artifact and capability-proof replay;
- Slice III relations, navigation, Orientation Map, and certification replay;
- Slice IV Expression and terminal certification replay;
- frozen source fingerprints;
- terminal STOP preservation.

All three certification commands exited successfully.

## 7. Conclusion

The initial execution and independent replay produced identical deterministic
Core artifacts, identities, ordering, hashes, Expression outputs, manifest,
and terminal certification.
