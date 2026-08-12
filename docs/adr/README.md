# Architecture Decision Records

ADRs preserve why a decision exists, who owns it, and what it constrains. They are immutable historical records after acceptance.

## Status lifecycle

```text
Draft → Proposed → Accepted
                 ↘ Rejected
Accepted → Superseded
```

- **Draft**: local preparation; not ready for decision.
- **Proposed**: complete proposal under review; implementation must wait.
- **Accepted**: governing decision.
- **Rejected**: reviewed and not adopted; retained for history.
- **Superseded**: replaced by a later accepted ADR; retained and linked.

## Index

| ADR | Title | Status |
|---|---|---|
| [0001](0001-orion-above-kernel.md) | ORION operates above the Kernel | Accepted |
| [0002](0002-independent-repository-boundaries.md) | Independent repository boundaries | Accepted |
| [0003](0003-structured-orientation-contracts.md) | Structured Orientation contracts | Accepted |
| [0004](0004-immutable-context-manifest.md) | Immutable Context Manifest | Accepted |
| [0005](0005-capability-based-reasoning-backends.md) | Capability-based Reasoning Backends | Accepted |
| [0006](0006-human-approval-and-effect-classes.md) | Human approval and effect classes | Accepted |
| [0007](0007-five-documentation-projections.md) | Five documentation projections | Accepted |
| [0008](0008-orion-v1-architecture-freeze.md) | Freeze the ORION v1 architecture baseline | Accepted |
| [0009](0009-orion-master-architecture-adoption.md) | Adopt the reconciled ORION Master Architecture partition | Accepted |

## Creating an ADR

```bash
./scripts/new-adr "Short decision title"
```

The script creates the next numbered file from [`0000-template.md`](0000-template.md). Complete every section, set the status to `Proposed`, and open a review.

## Acceptance rules

An ADR is accepted only when:

- the decision owner is named;
- alternatives and consequences are explicit;
- affected repositories and contracts are listed;
- all affected repository owners acknowledge cross-repository changes;
- implementation and migration timing are separated from the decision;
- the index is updated.

Do not edit the decision of an accepted ADR. Correct typographical errors only when meaning is unchanged. Use a new ADR to alter or supersede it.
