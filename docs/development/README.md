# Development Index

This index separates current contributor guidance from historical phase records.
The official architecture baseline is
[`ORION_V1_ARCHITECTURE_FREEZE.md`](../architecture/ORION_V1_ARCHITECTURE_FREEZE.md).

## Current workflow

| Need | Document |
|---|---|
| prepare the workspace | [`WORKSPACE.md`](WORKSPACE.md) |
| route, develop and review work | [`DEVELOPMENT_WORKFLOW.md`](DEVELOPMENT_WORKFLOW.md) |
| understand the F1 freeze | [`ORION v1 Architecture Freeze`](../architecture/ORION_V1_ARCHITECTURE_FREEZE.md) |
| run canonical human-facing scenarios | [`Orientation Sessions`](../orientation_sessions/README.md) |
| explore the Phase 7 Reflection question | [`LUCY — Time for Reflection`](../architecture/lucy/LUCY_CONCEPT.md) |
| prepare a repository release | [`Release Strategy`](../releases/RELEASE_STRATEGY.md) |

## Completed phase records

| Phase | Scope | Record |
|---|---|---|
| 0 | recovered external Core baseline | [`PHASE_0_BASELINE_RECOVERY.md`](../architecture/baselines/PHASE_0_BASELINE_RECOVERY.md) |
| 1A | minimum deterministic execution | [`PHASE_1A_EXECUTION.md`](PHASE_1A_EXECUTION.md) |
| 1B | local Ollama reference adapter and closeout | [`PHASE_1B_OLLAMA.md`](PHASE_1B_OLLAMA.md), [`PHASE_1B_CLOSEOUT.md`](PHASE_1B_CLOSEOUT.md) |
| 2A | deterministic repository context | [`PHASE_2A_CONTEXT.md`](PHASE_2A_CONTEXT.md) |
| 2B | deterministic document selection | [`PHASE_2B_SELECTION.md`](PHASE_2B_SELECTION.md) |
| 2C | content-free Context Brief | [`PHASE_2C_CONTEXT_BRIEF.md`](PHASE_2C_CONTEXT_BRIEF.md) |
| 3A–3C | representation cartography and Transition Contracts | [`Representation Architecture`](../architecture/REPRESENTATION_ARCHITECTURE.md), [`Transformations`](../architecture/transformations/ORIENTATION_TRANSFORM_STACK.md) |
| 4A | deterministic Transformation Engine planning | [`PHASE_4A_TRANSFORMATION_ENGINE.md`](PHASE_4A_TRANSFORMATION_ENGINE.md), [`PHASE_4A_CLOSEOUT.md`](PHASE_4A_CLOSEOUT.md) |
| 5A | declarative Operator Registry | [`PHASE_5A_OPERATOR_REGISTRY.md`](PHASE_5A_OPERATOR_REGISTRY.md) |
| 6A | canonical LYRA language architecture | [`PHASE_6A_LYRA_LANGUAGE.md`](PHASE_6A_LYRA_LANGUAGE.md) |
| 6B | deterministic LYRA integration | [`PHASE_6B_LYRA_INTEGRATION.md`](PHASE_6B_LYRA_INTEGRATION.md) |
| 6C | documentation-backed Orientation Sessions | [`PHASE_6C_ORIENTATION_SESSIONS.md`](PHASE_6C_ORIENTATION_SESSIONS.md) |
| VI | first live public-contract Understand journey | [`PHASE_VI_FIRST_LIVE_ORIENTATION.md`](PHASE_VI_FIRST_LIVE_ORIENTATION.md) |
| VII | real-world UNDERSTAND corpus evaluation | [`Phase VII Evaluation`](../../evaluation/phase_vii/README.md) |
| F1 | ORION v1 Architecture Freeze | [`ORION_V1_ARCHITECTURE_FREEZE.md`](../architecture/ORION_V1_ARCHITECTURE_FREEZE.md) |

Phase records preserve the status and limitations at the time they were written.
When their future-tense language differs from current state, the frozen
architecture and this index are authoritative. A future phase may extend the
baseline but cannot silently reinterpret a completed phase.

Phase 7 is not listed as a completed implementation phase. Its LUCY documents
are conceptual research only and create no runtime or architectural authority.
