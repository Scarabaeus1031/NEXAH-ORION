# ORION Publication Baseline

## Status

**Development publication candidate — not yet releasable.**

ORION remains `0.3.0-dev.0`. The F1 freeze stabilizes the ORION v1 architecture
but does not declare a stable public API, executable Transformation Stack or
production runtime.

## Candidate inputs

| Input | Required state | Current state |
|---|---|---|
| ORION source | clean, immutable commit | local baseline is committed through `f16adc9…`; no public remote exists |
| NEXAH Core | exact revision in `workspace.yaml` | configured `9f79bb06210402c40c9ef7d9937ca00d86c092b1`; connected clean checkout is on a newer local Operations series |
| Library | explicit canonical Registry reference | remains external to ORION and currently canonical in `NEXAH/LIBRARY` |
| Builder Hub | only when consumed | not part of this publication candidate |
| Runtime | optional external Ollama for integration only | never managed by ORION |

## Core mismatch

The Release Gate is correct to stop. ORION was frozen against NEXAH Core commit
`9f79bb06210402c40c9ef7d9937ca00d86c092b1`. The connected NEXAH checkout has
advanced beyond that revision and contains publication/governance work. A newer
Framework commit is not automatically a compatible Core baseline.

The first valid path has now been verified; the owner still chooses which
baseline to publish:

1. adopt the successful clean verification against the existing pinned Core;
   or
2. approve a new cross-repository compatibility record and update the pin.

Operations must not choose the second action without the Framework and ORION
owners. The Release Gate must not be weakened or taught to ignore a dirty or
different checkout.

## Publication blockers

- repository-wide license requires owner approval;
- public repository identity and remote require owner/GitHub action;
- owner must adopt the verified existing Core pin or request qualification of a
  newer revision; and
- public CI must pass on the published immutable commit.

The local consolidation blocker is closed. ORION `0a9c031…` passed the full
development Release Gate in an isolated clean workspace against the unchanged
Core pin `9f79bb…`; follow-up `f16adc9…` records that evidence and changes no
runtime source.

## Verification commands

```sh
make test
./scripts/check-workspace
./scripts/release-check --development
```

The opt-in Ollama integration is not required for the architecture baseline and
must never start or stop the external runtime.
