# ADR-0003: Structured Orientation contracts

- Status: Accepted
- Date: 2026-07-19
- Decision owner: ORION Architecture
- Affected repositories: nexah-orion and future consumers
- Supersedes: none
- Superseded by: none

## Context

Plain prompt strings cannot express authority, scope, evidence, effects, budgets, or compatibility reliably. Prompts also vary by model and runtime.

## Decision

Stable ORION boundaries use versioned structured Orientation Requests and Results. Prompt and message text are derived renderer artifacts, not product contracts.

## Ownership and authority

ORION owns its request/run contracts. External Core, Library, and Builder contracts remain owned by their producing repositories.

## Consequences

- Request types can include Review, Navigation, Comparison, Atlas, and Builder requests after separate approval.
- Contracts carry scope, evidence policy, effects, budgets, and output schema.
- Provider-specific fields remain inside adapters.

## Alternatives considered

A universal `generate(prompt)` interface was rejected because it hides incompatible semantics and leaks provider behavior into applications.

## Compatibility and migration

No schemas are implemented in Phase 1. Contract form and serialization remain subject to a later ADR after ownership inventory.

## Verification

Future public flows begin from a versioned request object, and provider SDK types do not cross ORION's public boundary.

## References

- [`../architecture/ORION_ARCHITECTURE.md`](../architecture/ORION_ARCHITECTURE.md)
