# ADR-0008: Freeze the ORION v1 architecture baseline

- Status: Accepted
- Date: 2026-07-19
- Decision owner: ORION Architecture
- Affected repositories: nexah-orion; informative boundary references to NEXAH Core, NEXAH Library, and Builder Hub
- Supersedes: none
- Superseded by: none

## Context

Phases 0 through 6C established repository recovery, the reasoning boundary,
deterministic context, representation architecture, transition contracts,
deterministic graph navigation, the declarative Operator Registry, LYRA, and
executable Orientation Sessions. The repository is architecture-complete and
interaction-complete for this bounded scope. Beginning a Reflection Boundary
without first fixing the authority and ownership baseline would allow later work
to redefine ORION implicitly.

## Decision

The architecture documented by
[`ORION_V1_ARCHITECTURE_FREEZE.md`](../architecture/ORION_V1_ARCHITECTURE_FREEZE.md)
is the first official ORION Architecture Baseline. Its principles,
responsibilities, authority boundaries, dependency direction, internal
contracts, ownership, repository and documentation structure, Architecture
Plates, and Orientation Sessions are frozen.

Future work extends this baseline. A change to a frozen item requires explicit
Architecture Review and an accepted ADR that identifies the affected authority,
compatibility and migration consequences.

Operator and Renderer implementations, transformation execution, mathematical
models, additional provider adapters, and a future Reflection Boundary remain
intentionally unfrozen. Their implementation must conform to the baseline and
does not receive authority by being an extension.

## Ownership and authority

- NEXAH Core remains the external deterministic and canonical authority.
- ORION owns context, provider-neutral reasoning orchestration, validation,
  deterministic representation-route planning, reports and audit metadata.
- LYRA translates canonical language and reports without planning, validation or
  execution authority.
- Reasoning Backends propose provider-neutral results and own no domain truth.
- NEXAH Library and Builder Hub remain independent repositories.
- LUCY is only a reserved future Reflection Boundary and owns no current runtime
  path or ORION authority.

## Consequences

### Positive

- One baseline now governs architecture, implementation boundaries, visuals,
  sessions and contributor workflow.
- Extension work can be reviewed against stable responsibilities.
- Architecture drift becomes an explicit decision rather than an incidental
  code or documentation edit.

### Costs and constraints

- Even internal architectural renaming requires review when it changes a frozen
  term, responsibility or dependency.
- Architecture Plates and their authoritative Markdown must change together.
- An extension cannot bypass missing Operators, Renderers, evidence or external
  repository authority.

## Alternatives considered

Leaving the repository in continuous architecture exploration was rejected
because Phase 6C already proved the intended interaction boundary. Declaring a
stable public runtime release was rejected because transformation execution,
public cross-repository contracts and multi-provider production conformance do
not exist.

## Compatibility and migration

This decision changes no API, schema, runtime behavior or repository version.
The repository remains `0.3.0-dev.0` with no release tag. Future extensions must
state whether they are additive or whether they require an ADR that supersedes a
frozen decision.

## Verification

The freeze requires unit tests, boundary checks, workspace checks, architecture
consistency, Architecture Plate reproducibility, Markdown links, syntax and
imports, and the development release gate to pass. Frozen Phase 1 files retain
their recorded SHA-256 checksums.

## References

- [`../architecture/ORION_ARCHITECTURE.md`](../architecture/ORION_ARCHITECTURE.md)
- [`../architecture/ORION_V1_ARCHITECTURE_FREEZE.md`](../architecture/ORION_V1_ARCHITECTURE_FREEZE.md)
- [`../governance/OWNERSHIP.md`](../governance/OWNERSHIP.md)
- [`../orientation_sessions/README.md`](../orientation_sessions/README.md)
