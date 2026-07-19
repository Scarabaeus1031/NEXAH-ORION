# ADR-0002: Independent repository boundaries

- Status: Accepted
- Date: 2026-07-19
- Decision owner: Cross-Repository Architecture
- Affected repositories: NEXAH Core, nexah-orion, NEXAH Library, Builder Hub
- Supersedes: none
- Superseded by: none

## Context

Core, ORION, Library, and Builder Hub have different authority, lifecycle, data, and release responsibilities.

## Decision

They remain independent repositories. The frozen NEXAH repository stays intact. ORION is new. Library and Builder Hub retain independent ownership. Cross-repository interaction occurs through versioned contracts.

## Ownership and authority

Each repository owns its code, persistent records, releases, and public contracts. No repository grants itself authority over another repository by importing or copying its types.

## Consequences

- Releases and versions are independent.
- Local working copies are coordinated through `workspace.yaml`.
- Cross-repository changes require all affected owners.
- Physical Library extraction from the frozen monorepo is a separate postponed migration.

## Alternatives considered

A single monorepo and a shared undifferentiated `/core /orion /lyra /library` layout were rejected because they collapse distinct authority and release boundaries.

## Compatibility and migration

The Core baseline is pinned by commit. Library and Builder remotes remain pending until their authoritative repository identities are confirmed.

## Verification

No sibling repository is tracked inside ORION. The manifest records exact external revisions or explicit `pending` state.

## References

- [`../governance/CROSS_REPOSITORY_GOVERNANCE.md`](../governance/CROSS_REPOSITORY_GOVERNANCE.md)
