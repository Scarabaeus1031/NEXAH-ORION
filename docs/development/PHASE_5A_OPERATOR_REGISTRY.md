# Phase 5A: Operator Registry

## Purpose

Phase 5A adds the missing declarative layer between Transition Contracts and
transformation planning. The registry makes known and unknown capabilities
inspectable without executing an operator or overstating evidence.

The repository remains `0.3.0-dev.0`.

## Scope

Implemented:

- immutable `OperatorStatus`, `OperatorReference`, `OperatorSpecification` and
  `OperatorRegistry` records;
- deterministic exact-ID and transition lookup;
- one non-executable placeholder for each T01–T15;
- explicit contract-version and representation-version compatibility queries;
- additive Transformation Plan metadata and improved `MissingOperator` reasons;
- consistency, boundary and unit tests.

Not implemented: mathematics, geometry, operator implementations, selection,
ranking, execution, persistence, renderers, provider loading, plugin discovery,
dynamic imports, Kernel mutation, scientific validation or Builder Hub work.

## Runtime boundary

```text
Orientation Object
        ↓
Representation Graph navigation
        ↓
Transition Contract lookup
        ↓
Operator Registry metadata lookup
        ↓
TransformationPlan + MissingOperator
```

Registry lookup does not change route calculation. If exactly one declaration
matches a transition, its ID, version, status and owner are copied to the plan.
Zero entries are reported. Multiple entries are reported without choosing among
them. Every Phase 5A entry is non-executable, so the report remains blocked and
`produced_representation` remains `None`.

## Registry schema

`OperatorSpecification` contains the fields required by the architecture:

| Group | Fields |
|---|---|
| Identity | `operator_id`, `operator_name`, `operator_version` |
| Maturity | `status`, `evidence_level`, `executable` |
| Capability | `implemented_transition_ids`, parameters, invariants, lossiness |
| Compatibility | supported contract and representation versions |
| Dependencies | provider and renderer dependency identifiers |
| Governance | `owner`, `notes` |

Compatibility values are declarations, not runtime probes. The registry never
crawls modules or the filesystem.

## Initial entries

| Transition | Operator ID | Status | Evidence | Executable |
|---|---|---|---|---|
| T01 | `orion.operator.placeholder/T01` | `unknown` | E1 | false |
| T02 | `orion.operator.placeholder/T02` | `unknown` | E0 | false |
| T03 | `orion.operator.placeholder/T03` | `candidate` | E0–E1 | false |
| T04 | `orion.operator.placeholder/T04` | `unknown` | E0 | false |
| T05 | `orion.operator.placeholder/T05` | `unknown` | E0 | false |
| T06 | `orion.operator.placeholder/T06` | `candidate` | E0–E1 | false |
| T07 | `orion.operator.placeholder/T07` | `candidate` | E1 | false |
| T08 | `orion.operator.placeholder/T08` | `unknown` | E0 | false |
| T09 | `orion.operator.placeholder/T09` | `candidate` | E1 | false |
| T10 | `orion.operator.placeholder/T10` | `candidate` | E1 | false |
| T11 | `orion.operator.placeholder/T11` | `unknown` | E0 | false |
| T12 | `orion.operator.placeholder/T12` | `candidate` | E0–E1 | false |
| T13 | `orion.operator.placeholder/T13` | `candidate` | E0–E1 | false |
| T14 | `orion.operator.placeholder/T14` | `unknown` | E0 | false |
| T15 | `orion.operator.placeholder/T15` | `candidate` | E1 | false |

## Example inspection

```python
from orion import DEFAULT_OPERATOR_REGISTRY

entries = DEFAULT_OPERATOR_REGISTRY.for_transition("T13")
entry = entries[0]
assert entry.status.value == "candidate"
assert entry.supports_contract("T13", "0.1-draft")
assert entry.executable is False
```

This is metadata inspection only. There is deliberately no `execute`, `load`,
`select` or `rank` method.

## Verification

```bash
make test
./scripts/check-workspace
./scripts/check-architecture-consistency
./scripts/check-boundaries
```

The tests cover immutability, lookup, T01–T15 coverage, lifecycle values,
contract compatibility, exact unknown/candidate continuity, Engine metadata,
missing declarations and the no-execution invariant.

## Future phases

Future work may separately establish operator specifications, evidence review,
implementation ports, conformance tests and controlled execution. None is
implicitly authorized by the presence of a placeholder. Lifecycle promotion,
owner assignment or executable capability requires explicit architectural and
validation evidence.
