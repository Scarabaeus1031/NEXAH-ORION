# Runtime Readiness Validation Alpha

- Status: implemented proof
- Decision: `ready`
- Diagnostic version: `0.1-alpha`
- Public contract impact: none
- Runtime behavior impact: none
- Stop boundary: before processing

## Purpose

This milestone answers one question:

> Can the existing ORION Runtime deterministically establish that one validated
> `OrientationRequest 1.0` is ready to enter processing without beginning
> Orientation?

The executable proof is:

```text
Validated OrientationRequest 1.0
→ existing Runtime-owned readiness checks
→ internal ready diagnostic
→ STOP before processing
```

## Validation, readiness and Orientation

These responsibilities remain separate:

- **Contract validation** determines whether the request conforms to the frozen
  public request contract.
- **Readiness validation** determines whether the existing Runtime may begin
  processing that valid request.
- **Orientation** applies an Orientation Operator after readiness.

Only readiness is demonstrated here. The diagnostic is not a public contract,
Runtime result or additional readiness state.

## Existing readiness conditions

The proof exercises the readiness branches already present in
`OrientationRuntime._orient`:

1. public request validation succeeds;
2. the current Runtime supports the requested `understand` mode;
3. the existing clarification rules find no unresolved identity, access, Scope
   or Depth issue;
4. the declared source access state permits processing.

No additional readiness policy was introduced.

## Stop mechanism

No Runtime extraction was necessary. An internal Alpha probe subclasses the
existing Runtime and places a sentinel at `_report_id`, the first operation
after the current readiness branches.

Reaching that sentinel proves that the unchanged Runtime path passed all
existing readiness decisions. The sentinel prevents report identity creation,
Evidence handling, blocked-report generation and every later result path.

The production `OrientationRuntime`, its public interface and its execution
semantics remain unchanged.

## Cross-repository lineage

The proof executes the accepted NEXAHEDRON artifacts:

```text
Working Material
→ Confirmed Material
→ immutable Representation
→ Representation-referenced OrientationRequest 1.0
```

It then verifies exactly one request and one Representation, including:

- Orientation Object identity and version;
- Representation identity and version;
- source owner, source reference and source revision;
- whole-content SHA-256 integrity;
- request identity and version.

Only after those checks does the internal readiness probe run.

## Run the proof

The accepted NEXAHEDRON checkout must be available beside this repository, or
its root must be supplied through `NEXAHEDRON_ROOT`.

```bash
PYTHONPATH=src python3 scripts/runtime_readiness_alpha_proof.py
```

The canonical diagnostic output is deterministic:

```text
SHA-256
dd8547f2e4b110e992ebb99079dd7d39a73f8da98e814b0dd9a1d347fc07eaf1
```

Run the focused guard suite:

```bash
PYTHONPATH=src python3 -m unittest discover \
  -s tests -p 'test_runtime_readiness_alpha.py'
```

## Guarded boundaries

Tests explicitly prevent:

- Orientation result execution;
- complete or blocked report generation;
- Evidence handling or Evidence Binding;
- Continuation generation;
- Gateway or presentation invocation;
- transport, browser or UI behavior;
- publication of the diagnostic through the root ORION API.

## Intentionally unimplemented

The milestone does not implement or modify:

- Orientation execution;
- Runtime or Gateway behavior;
- reports or blocked reports;
- Evidence or Evidence Binding;
- Library resolution;
- Continuations;
- clarification behavior;
- LYRA;
- NTO or additional Projection mathematics;
- persistence, transport, deployment or UI behavior.

The proof stops immediately after the existing Runtime classifies the request
as ready.
