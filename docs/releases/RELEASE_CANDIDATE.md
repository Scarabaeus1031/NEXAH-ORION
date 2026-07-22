# ORION Publication Candidate

## Status

ORION remains `0.3.0-dev.0`. This is a prepared development publication
candidate, not a release or stable API declaration.

## Included capability

- provider-neutral reasoning boundary with unchanged FakeBackend baseline;
- local Ollama adapter behind the existing backend interface;
- deterministic selection, Context Manifest and Context Brief pipeline;
- Representation Graph, Transition Contracts and Transformation Engine;
- declarative Operator Registry with all T01–T15 operators non-executable;
- deterministic LYRA language boundary and canonical Orientation Sessions;
- frozen ORION v1 architecture and canonical SVG/PNG Architecture Plates.

## Explicit limits

- no executable transformation operators;
- no renderer execution;
- no generated target Representation;
- no autonomous inference, planning authority or Kernel mutation;
- no managed Ollama lifecycle;
- no LUCY runtime; and
- no production support promise.

## Verification

The local suite passes with 75 tests and one opt-in Ollama integration test
skipped. Architecture, responsibility-boundary and Plate checks pass. The
current clean publication candidate, including the approved licensing and
repository metadata, passes the complete development Release Gate in an
isolated workspace against the unchanged configured Core pin `9f79bb…`.
The ordinary connected workspace remains intentionally newer and therefore
stops at the exact revision comparison described in
`CORE_COMPATIBILITY_REPORT.md`.

## Publication gates

- publication of the prepared `NEXAH-ORION` repository and immutable baseline;
- publication of the existing clean immutable local ORION commits;
- owner decision on the existing Core pin;
- successful development Release Gate against that exact Core revision; and
- green public CI on the published commit.

No additional architecture or feature work is required for this candidate.

Software is licensed under Apache 2.0. Original documentation,
specifications, research, books and visual material are licensed under
CC BY 4.0 where applicable; `LICENSES.md` defines the boundary.
