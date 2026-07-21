# Repository Governance

NEXAH ORION is governed through explicit ownership, recorded decisions, compatibility review, and human approval.

## Authority

- NEXAH Core owns deterministic state, invariants, existing orientation contracts, and Kernel decisions.
- ORION owns request execution, context assembly, reasoning invocation, result validation, audit, and replay.
- Library owns curated knowledge, identity, editorial status, and guarded publication.
- Builder Hub owns operator-facing interaction and approval presentation.
- Models own no NEXAH domain authority.

## Decision levels

| Level | Example | Approval |
|---|---|---|
| repository-local | documentation layout, internal tool | ORION maintainers |
| architecture | module boundary, stable contract, authority | accepted ADR |
| cross-repository | Core/Library/Builder contract or version policy | affected repository owners |
| canonical or public effect | Kernel state, Library identity, public editorial change | governing external authority and human approval |

## Records

- Architecture decisions: `docs/adr/`
- Cross-repository rules: `docs/governance/`
- Release records: `docs/releases/` and Git tags
- Current architecture: `docs/architecture/`
- Local research and experiments: `.workspace/`, never authority by placement

Detailed governance is defined in [`docs/governance/CROSS_REPOSITORY_GOVERNANCE.md`](docs/governance/CROSS_REPOSITORY_GOVERNANCE.md).

## Frozen architecture baseline

[`ADR-0008`](docs/adr/0008-orion-v1-architecture-freeze.md) freezes the ORION v1
Architecture Baseline. Additive implementation work may proceed within its
extension points. A change to frozen terminology, authority, responsibility,
contracts, ownership, dependency direction, repository structure,
Architecture Plates or Orientation Sessions requires explicit Architecture
Review and an accepted ADR.
