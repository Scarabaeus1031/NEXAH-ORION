# Phase 4A — Transformation Engine

## Status

- Repository version: `0.3.0-dev.0`
- Runtime scope: deterministic orchestration only
- Operators: not implemented
- Renderers: not implemented
- LLM, networking, persistence, Kernel mutation: not used

## Purpose

The Transformation Engine proves that ORION can navigate the registered
Representation Graph, bind every selected edge to its Transition Contract, and
produce an inspectable plan and report without performing a transformation.

```text
OrientationObject
        ↓
explicit RepresentationGraph
        ↓
deterministic path enumeration
        ↓
TransitionContract verification
        ↓
TransformationPlan
        ↓
validation and blockers
        ↓
TransformationReport
```

`produced_representation` is always `None` in Phase 4A.

## Components

### Contract and graph registry

[`src/orion/transformation_contracts.py`](../../src/orion/transformation_contracts.py)
contains immutable runtime planning records for:

- `GraphEdge`;
- `RepresentationGraph`;
- `TransitionContract`;
- `TransitionContractRegistry`;
- the explicit `T01–T15` graph and contract catalog.

The catalog is a provider-independent planning projection of the Phase 3C
documentation. It contains no callable operator and no renderer instance.

### Engine and reports

[`src/orion/transformation_engine.py`](../../src/orion/transformation_engine.py)
contains:

- `RepresentationRef` and `RepresentationTarget`;
- `OrientationObject`;
- `TransformationEngine`;
- `TransformationPlan` and `PlannedTransition`;
- `TransformationProvenanceStep`;
- `TransformationValidation`, `TransformationIssue`, and
  `TransformationReport`.

All records are immutable.

## Deterministic navigation

The engine uses only registered directed edges. It enumerates simple paths, so a
representation cannot be visited twice in one route. Paths are ordered by:

1. edge count;
2. transition-ID tuple.

The first route is the selected shortest path. Remaining routes are retained as
`alternative_paths`. This is a deterministic tie-break, not evidence ranking or
semantic inference.

No missing edge is inferred. Unknown representation names and unsupported
directions produce `UnsupportedPath`.

## Contract verification

For every edge on the selected path the engine verifies:

- a contract with the same transition ID exists;
- source and target endpoints match the graph;
- declared source/target representation versions are compatible when a contract
  constrains them;
- every invariant active on the input Orientation Object is declared preserved;
- evidence and contract version are copied into plan provenance;
- a verified operator reference exists;
- a compatible renderer reference exists.

The Phase 3C catalog contains only `unknown` and `candidate` operators and no
renderers. Default plans therefore terminate as `blocked`, normally with
`MissingOperator` and `MissingRenderer` for each selected edge. This is the
intended Phase 4A result.

## Invariants and provenance

Every input carries:

- Orientation Object ID and version;
- current Representation ID, type, version, and coordinate profile;
- source references;
- source provenance;
- optional epoch and known constants.

The engine never mutates these values. It builds an ordered provenance step for
each planned edge. `epoch` and `known_constants` become active invariants only
when present on the input. The four unconditional invariants are:

```text
identity
provenance
orientation_object_id
source_references
```

An edge that does not declare an active invariant produces
`InvariantViolation` and blocks the report.

## Failure model

Issues are immutable provider-neutral records containing:

- issue kind;
- transition ID where applicable;
- evidence level;
- deterministic reason.

Supported Phase 4A kinds are:

| Kind | Meaning |
| --- | --- |
| `UnsupportedPath` | no directed registered route exists |
| `MissingContract` | graph edge exists but its contract is absent |
| `ContractIncompatible` | endpoints or declared versions do not match |
| `InvariantViolation` | the contract does not preserve an active invariant |
| `MissingOperator` | no verified operator reference is registered |
| `MissingRenderer` | no renderer reference is registered |

The engine stops at the planning boundary. It does not dynamically import,
approximate, or call an operator or renderer.

## Example

```python
from orion import (
    OrientationObject,
    RepresentationRef,
    RepresentationTarget,
    TransformationEngine,
)

source = OrientationObject(
    orientation_object_id="orientation-1",
    orientation_object_version="orientation/1",
    representation=RepresentationRef(
        representation_id="observation-1",
        representation_type="Observation",
        representation_version="observation/1",
        coordinate_profile="observation-profile/1",
    ),
    source_references=("source:observation-1",),
    provenance=("source:observation-1@revision-1",),
)

report = TransformationEngine().execute(
    source,
    RepresentationTarget("Stellar Projection"),
)

print(report.plan.transition_ids)
print(report.status)  # blocked: operators and renderers are intentionally absent
```

## Tests

[`tests/test_transformation_engine.py`](../../tests/test_transformation_engine.py)
covers:

- deterministic shortest-path selection;
- multiple routes;
- invariant preservation and violations;
- provenance and evidence chains;
- endpoint and representation-version compatibility;
- unsupported paths and missing contracts;
- missing operator and renderer reports;
- immutability and absence of a produced representation.

Run:

```bash
make test
```

The Ollama integration is unrelated and remains opt-in. The engine does not call
an LLM or manage any external runtime.

## Out of scope

- mathematical or geometric operators;
- numerical approximation;
- rendering and UI;
- LLM reasoning;
- Kernel mutation;
- persistence;
- execution of planned transitions;
- scientific validation of the representation system.
