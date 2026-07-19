# ADR-0001: ORION operates above the Kernel

- Status: Accepted
- Date: 2026-07-19
- Decision owner: ORION Architecture
- Affected repositories: NEXAH Core, nexah-orion
- Supersedes: none
- Superseded by: none

## Context

The frozen NEXAH Core owns deterministic objects, relations, invariants, evidence boundaries, and canonical decisions. Model reasoning must be replaceable without changing that authority.

## Decision

ORION is a separate orchestration architecture above the Kernel. Models propose. ORION validates. The Kernel decides. Neither a model nor ORION may directly mutate canonical Kernel state.

## Ownership and authority

- Core owns deterministic truth within NEXAH and Kernel commands.
- ORION owns request execution, context, reasoning invocation, validation, audit, and replay.
- Models own no NEXAH domain authority.

## Consequences

- The Core has no dependency on ORION or provider SDKs.
- ORION integrates through published Core contracts or ports.
- Missing Core capability becomes a proposal to the Core owner, not an ORION workaround.

## Alternatives considered

Embedding model reasoning inside the Core was rejected because it would couple canonical authority to replaceable inference behavior.

## Compatibility and migration

The frozen Core remains unchanged. ORION begins as a new repository.

## Verification

Dependency and ownership checks must show no Core-to-ORION dependency and no direct model-to-Kernel mutation path.

## References

- [`../architecture/ORION_ARCHITECTURE.md`](../architecture/ORION_ARCHITECTURE.md)
- [`../architecture/baselines/PHASE_0_BASELINE_RECOVERY.md`](../architecture/baselines/PHASE_0_BASELINE_RECOVERY.md)
