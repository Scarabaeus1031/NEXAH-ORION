# ORION Publication Baseline

> Historical F1 publication record. Current readiness is governed by the
> [ORION Version 1 RC1 Recommendation](ORION_V1_RC1_RECOMMENDATION.md).

## Status

**Development publication candidate — locally publication-ready.**

ORION remains `0.3.0-dev.0`. The F1 freeze stabilizes the ORION v1 architecture
but does not declare a stable public API, executable Transformation Stack or
production runtime.

## Candidate inputs

| Input | Required state | Current state |
|---|---|---|
| ORION source | clean, immutable commit | current clean commit contains the approved license and public repository identity; pre-license baseline was `18d8a454842c8f25301ca4d3118f7ad903de55a2` |
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

## Publication gates

- Apache 2.0 for software and CC BY 4.0 for original documentation and visual
  material are recorded in `LICENSE`, `LICENSE-DOCS.md` and `LICENSES.md`;
- public repository identity is
  `https://github.com/Scarabaeus1031/NEXAH-ORION`;
- owner must adopt the verified existing Core pin or request qualification of a
  newer revision; and
- public CI must pass on the published immutable commit.

The local consolidation and licensing blockers are closed. The current clean
publication candidate passed the full development Release Gate in an isolated
workspace against the unchanged Core pin `9f79bb…`. Its executable baseline
entered at `0a9c031…`; subsequent publication commits change no runtime source.

## Verification commands

```sh
make test
./scripts/check-workspace
./scripts/release-check --development
```

The opt-in Ollama integration is not required for the architecture baseline and
must never start or stop the external runtime.
