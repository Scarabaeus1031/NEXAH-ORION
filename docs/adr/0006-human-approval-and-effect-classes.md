# ADR-0006: Human approval and effect classes

- Status: Accepted
- Date: 2026-07-19
- Decision owner: Cross-Repository Architecture
- Affected repositories: nexah-orion, NEXAH Core, NEXAH Library, Builder Hub
- Supersedes: none
- Superseded by: none

## Context

Read-only orientation, draft generation, canonical mutation, and public external effects carry different authority and risk.

## Decision

Every ORION request declares an effect class. Human approval and the owning external authority are required according to that class. Model output never counts as approval.

## Ownership and authority

- Builder Hub may present and capture approval but cannot invent authority.
- ORION enforces run policy and approval stops.
- Kernel or Library validates and performs its own governed effect.
- Human principals retain responsibility for delegated actions.

## Consequences

Read-only operations can remain low-friction. Draft, canonical, public, or external changes require progressively stronger review and explicit commands.

## Alternatives considered

A single generic tool-call permission was rejected because it collapses different effect and authority boundaries.

## Compatibility and migration

The exact effect taxonomy is postponed until request contracts and external command ports are designed.

## Verification

No future effect-bearing path may bypass a declared effect class, required approval, or the target repository's own validator.

## References

- [`../governance/CROSS_REPOSITORY_GOVERNANCE.md`](../governance/CROSS_REPOSITORY_GOVERNANCE.md)
