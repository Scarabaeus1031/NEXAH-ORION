# UNDERSTAND Declared Representation Inventory Alpha

- Status: implemented proof
- Canonical stage: `understand/2`
- Responsibility: `declared_representation_inventory`
- Responsibility state: `completed`
- Canonical Stage 2 completed: no
- Semantic processing: none
- Public contract impact: none
- Runtime behavior impact: none
- Stop boundary: `before_source_structure_inventory`

## Purpose

This milestone proves one bounded responsibility inside canonical UNDERSTAND
Stage 2:

> Determine which exact Representations have already been explicitly declared
> for the bound Orientation Object.

The executable proof is:

```text
Completed understand/1 binding
→ inventory exactly the declared Representation
→ immutable internal inventory diagnostic
→ STOP before source-structure inventory
```

It does not claim that `understand/2` is complete.

## Metadata-only inventory

The inventory preserves exactly:

- Representation ID, version and schema;
- Projection ID and version;
- Renderer ID and version;
- declared target domain;
- declared media type;
- fragment reference;
- declared lossiness;
- original request ordering.

No Representation is selected, ranked, compared, normalized, repaired, merged
or substituted. “Available” means only explicitly referenced, identity-resolved
and supplied to this bounded proof.

## Payload boundary

The inventory never opens the Representation payload. The declared media type
is read from the existing Projection profile as `source_media_type`; no payload
field is needed.

A runtime guard fails immediately if the inventory asks for `payload`. Static
guards also exclude content, source-structure, graph, semantic, Evidence,
Library, report and Continuation dependencies.

## Internal diagnostic

The immutable internal diagnostic contains only:

- diagnostic version;
- request and operator identity;
- Orientation Object identity;
- canonical stage `understand/2`;
- responsibility `declared_representation_inventory`;
- ordered Representation count;
- ordered declared Representation metadata;
- responsibility completion state;
- stop boundary.

It contains no payload, document structure, concepts, entities, graph
structure, findings, Evidence, confidence, summaries, interpretations, report
fields or Continuation data. It is absent from the public ORION exports and is
not a Runtime outcome.

## Run the proof

The accepted NEXAHEDRON checkout must be available beside this repository, or
its root must be supplied through `NEXAHEDRON_ROOT`.

```bash
PYTHONPATH=src \
  python3 scripts/understand_representation_inventory_alpha_proof.py
```

The canonical output is deterministic:

```text
SHA-256
54469b52ac2fb4b3fc1d72b8da9b2d4b731b3023158151a1b75281e11fba3b2b
```

Run the focused guard suite:

```bash
PYTHONPATH=src python3 -m unittest discover \
  -s tests -p 'test_understand_representation_inventory_alpha.py'
```

## Preserved earlier proofs

This milestone does not alter:

- Representation Alpha;
- adapter-free Representation handoff;
- Representation-referenced Orientation Request assembly;
- Runtime Readiness Validation Alpha;
- UNDERSTAND Stage 1 Binding Alpha;
- Runtime, Gateway or public-contract behavior.

The accepted immediate predecessor remains:

```text
UNDERSTAND Stage 1
b3d845ea91ae4bd0af295ff9237a13189f86e27114c769ca7d6ac431ab1b1723
```

## Stop boundary

The milestone ends after exactly one declared Representation is inventoried.
Source-structure inventory and every later UNDERSTAND responsibility remain
unimplemented by this proof.
