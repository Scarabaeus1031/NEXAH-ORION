# UNDERSTAND Stage 1 Binding Alpha

- Status: implemented proof
- Operator: `orion.orientation-operator/understand@1.0`
- Stage: `understand/1`
- Completion state: `completed`
- Semantic processing: none
- Public contract impact: none
- Runtime behavior impact: none
- Stop boundary: `before_understand/2`

## Purpose

This milestone proves one permanent Version 1 invariant:

> UNDERSTAND Stage 1 is semantically free. It establishes only immutable
> identity, version binding and integrity lineage. It performs no
> interpretation of the Orientation Object.

The executable proof is:

```text
Ready OrientationRequest 1.0
        +
Referenced immutable Representation
→ verify exact declared references
→ bind UNDERSTAND operator identity and version
→ immutable internal binding diagnostic
→ STOP before understand/2
```

## Bound responsibility

Stage 1 reads only declared metadata:

- request ID and version;
- Orientation Object ID and version;
- Representation ID and version;
- source owner, reference and revision;
- exact integrity method, value, coverage and verification state;
- existing UNDERSTAND operator ID and version.

“Identify” means resolving the declared identity. It does not mean discovering,
classifying or interpreting what the material represents.

The binding fails deterministically when any declared reference differs.
Nothing is normalized, repaired, inferred, substituted or merged.

## Content boundary

Stage 1 never reads the Representation `content` field. It consumes only the
already-conformant artifact's identity and integrity metadata. It does not
deserialize the payload into another Representation model and does not replay
the Renderer.

The upstream Representation Alpha proof remains responsible for Representation
conformance. Stage 1 preserves that artifact; it does not transform or
reinterpret it.

## Internal diagnostic

The frozen internal diagnostic records only:

- request identity;
- operator identity;
- Orientation Object identity;
- Representation identity;
- source identity and revision;
- integrity reference;
- `stage_id: understand/1`;
- `completion_state: completed`;
- `stop: before_understand/2`.

It contains no findings, concepts, entities, summaries, Evidence, confidence,
conclusions, report status or Continuation data. It has no public
`schema_version`, is absent from the root ORION exports and is not a Runtime
outcome.

## Run the proof

The accepted NEXAHEDRON checkout must be available beside this repository, or
its root must be supplied through `NEXAHEDRON_ROOT`.

```bash
PYTHONPATH=src python3 scripts/understand_stage1_alpha_proof.py
```

The canonical output is deterministic:

```text
SHA-256
b3d845ea91ae4bd0af295ff9237a13189f86e27114c769ca7d6ac431ab1b1723
```

Run the focused guard suite:

```bash
PYTHONPATH=src python3 -m unittest discover \
  -s tests -p 'test_understand_stage1_alpha.py'
```

## Guarded exclusions

The proof and tests prevent:

- `understand/2` or any later stage;
- Representation content inspection or transformation;
- reasoning, tokenization, classification or inference;
- Evidence or Library access;
- graph traversal;
- report or result identity creation;
- Continuation generation;
- Gateway, LYRA, LUCY, SIRIUS, browser or UI interaction;
- persistence or transport.

## Preserved earlier proofs

This milestone does not alter:

- Representation Alpha;
- adapter-free Representation handoff;
- Representation-referenced Orientation Request assembly;
- public request validation;
- Runtime Readiness Validation Alpha;
- Runtime, Gateway or public-contract behavior.

The Runtime Readiness Alpha diagnostic remains:

```text
dd8547f2e4b110e992ebb99079dd7d39a73f8da98e814b0dd9a1d347fc07eaf1
```

## Stop boundary

The milestone ends after the exact identity binding is recorded.
`understand/2`, Representation inventory and all semantic processing remain
unimplemented by this proof.
