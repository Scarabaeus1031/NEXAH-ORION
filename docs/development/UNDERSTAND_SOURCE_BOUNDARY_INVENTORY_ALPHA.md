# UNDERSTAND Declared Source Boundary Inventory Alpha

- Status: implemented proof
- Canonical stage: `understand/2`
- Responsibility: `declared_source_boundary_inventory`
- Responsibility state: `completed`
- Canonical Stage 2 completed: no
- Semantic processing: none
- Public contract impact: none
- Runtime behavior impact: none
- Stop boundary: `before_declared_source_element_inventory`

## Purpose

This milestone proves one bounded responsibility inside canonical UNDERSTAND
Stage 2:

> Determine which explicit source boundary has already been declared for each
> inventoried Representation.

The executable proof is:

```text
Completed understand/1 binding
→ completed declared Representation inventory
→ preserve the exact declared fragment boundary
→ immutable internal boundary diagnostic
→ STOP before declared source-element inventory
```

It does not claim that `understand/2` is complete.

## Metadata-only boundary

The exact accepted predecessor is the Declared Representation Inventory Alpha.
The boundary proof combines only its ordered Representation identity and
declared fragment reference with the already-bound request, source, revision and
integrity lineage.

The current Alpha profile preserves exactly one boundary:

```text
fragment_ref = whole
```

It does not determine whether additional source elements exist. It never
selects, compares, merges, normalizes, repairs or creates boundaries.

## Content boundary

The implementation accepts no Representation or source-content input. It does
not reopen the Projection or Representation. It performs no filesystem access,
source resolution, parsing, structural discovery or semantic processing.

Static and executable guards exclude content access, Context Manifest and
Context Brief use, Library authority, Gateway and LYRA participation, Evidence,
report construction and downstream UNDERSTAND responsibilities.

## Internal diagnostic

The immutable internal diagnostic contains only:

- diagnostic, request, operator and Orientation Object identity;
- exact predecessor responsibility and stop boundary;
- canonical stage `understand/2`;
- responsibility `declared_source_boundary_inventory`;
- ordered boundary count;
- Representation, source, fragment and integrity lineage;
- responsibility state `completed`;
- canonical Stage 2 state `incomplete`;
- stop boundary.

It contains no source elements, excerpts, content lengths, hierarchy, graph
elements, concepts, entities, findings, Evidence, confidence, summaries,
interpretations, Runtime outcome, report fields or Continuation data. It is not
exported from the public ORION surface.

## Run the proof

The accepted NEXAHEDRON checkout must be available beside this repository, or
its root must be supplied through `NEXAHEDRON_ROOT`.

```bash
PYTHONPATH=src \
  python3 scripts/understand_source_boundary_inventory_alpha_proof.py
```

The canonical output is deterministic:

```text
SHA-256
9b639edffc15bec1d5d6acd83658f845c8e01c31227fdae20a277c2d39f3dbe1
```

Run the focused guard suite:

```bash
PYTHONPATH=src python3 -m unittest discover \
  -s tests -p 'test_understand_source_boundary_inventory_alpha.py'
```

## Preserved earlier proofs

The executable proof verifies the frozen hashes of:

- Representation-referenced Orientation Request Alpha;
- UNDERSTAND Stage 1 Binding Alpha;
- UNDERSTAND Declared Representation Inventory Alpha.

It does not modify Representation Alpha, the adapter-free handoff, Runtime
Readiness, Runtime, Gateway or the Version 1 public contracts.

## Stop boundary

The milestone ends after exactly one already-declared source boundary is
inventoried. Declared Source Element Inventory and every later UNDERSTAND
responsibility remain unimplemented.
