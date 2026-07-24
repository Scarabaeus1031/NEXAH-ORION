# UNDERSTAND Declared Source Element Declaration Check Alpha

- Status: implemented proof
- Canonical stage: `understand/2`
- Responsibility: `declared_source_element_declaration_check`
- Declaration state: `not_declared`
- Responsibility state: `completed`
- Canonical Stage 2 completed: no
- Structural discovery: none
- Semantic processing: none
- Public contract impact: none
- Runtime behavior impact: none
- Stop boundary: `before_declared_source_element_inventory`

## Purpose

This milestone proves one bounded responsibility inside canonical UNDERSTAND
Stage 2:

> Determine whether the current bound Representation profile authoritatively
> declares source elements within the accepted source boundary.

The executable proof is:

```text
Completed understand/1 binding
→ completed declared Representation inventory
→ completed declared source-boundary inventory
→ inspect the accepted Representation profile identity
→ declaration state: not_declared
→ immutable internal diagnostic
→ STOP before declared source-element inventory
```

It does not claim that the source contains no elements. It establishes only
that the accepted Exact-Text Alpha profile declares none.

## Metadata-only profile check

The check accepts only immutable predecessor diagnostics and the immutable
Orientation Request. It recognizes exactly:

```text
orion.representation/exact-text/0.1-alpha
```

including its accepted Projection, Renderer, target domain, media type and
lossiness metadata. An unknown or altered profile fails deterministically.
Nothing is guessed, normalized or repaired.

The implementation does not receive or reopen a Representation, Projection
payload or source. It performs no parsing, filesystem access, structural
discovery, semantic processing or external resolution.

## Internal diagnostic

The immutable diagnostic contains only:

- diagnostic, request, operator and Orientation Object identity;
- Representation identity;
- exact predecessor responsibility and stop;
- canonical stage and responsibility;
- exact Representation schema as the declaration basis;
- declaration state `not_declared`;
- responsibility state `completed`;
- canonical Stage 2 state `incomplete`;
- stop boundary.

It contains no elements, element count, source structure, payload excerpt,
content length, findings, concepts, entities, Evidence, Runtime outcome, report
or Continuation data. It is not exported from the public ORION surface.

## Run the proof

The accepted NEXAHEDRON checkout must be available beside this repository, or
its root must be supplied through `NEXAHEDRON_ROOT`.

```bash
PYTHONPATH=src \
  python3 scripts/understand_source_element_declaration_check_alpha_proof.py
```

The canonical output is deterministic:

```text
SHA-256
740808f29d4b40b3f55c12472be52db4f93c4d615621b255da810055feebb4d7
```

Run the focused guard suite:

```bash
PYTHONPATH=src python3 -m unittest discover \
  -s tests -p 'test_understand_source_element_declaration_check_alpha.py'
```

## Preserved earlier proofs

The proof verifies the frozen hashes of:

- Representation-referenced Orientation Request Alpha;
- UNDERSTAND Stage 1 Binding Alpha;
- UNDERSTAND Declared Representation Inventory Alpha;
- UNDERSTAND Declared Source Boundary Inventory Alpha.

It does not modify Representation Alpha, handoff, Runtime Readiness, Runtime,
Gateway or Version 1 public contracts.

## Stop boundary

The milestone ends after declaration availability is determined as
`not_declared`. Declared Source Element Inventory, structural discovery,
UNDERSTAND Stage 3 and every later responsibility remain unimplemented.
