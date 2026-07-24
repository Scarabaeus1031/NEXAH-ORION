# ORION Version 1 Repository Cleanup Report

- Status: completed Phase VIII cleanup
- Scope: organization and public-boundary clarification only

## Runtime ownership classification

| Classification | Location | Finding |
|---|---|---|
| Public Contracts | `src/orion/public_contracts/` | correctly isolated; not Runtime behavior |
| Core Runtime | `src/orion/orientation_runtime/` | correctly contains only deterministic Understand execution |
| Gateway | `src/orion/gateway/gateway.py`, `translation.py` | correctly validates, translates and invokes; no orientation logic |
| Presentation | `src/orion/gateway/presentation.py` | correctly derives presentation from public outcomes |
| Evaluation | `evaluation/`, `scripts/phase_vi_*`, `scripts/phase_vii_*` | correctly outside production packages |
| Test | `tests/` | correctly isolated from production behavior |
| Research/Experimental/Historical | explicit legacy `src/orion/` modules, LYRA and Ollama slices | retained for reproducibility; removed from root public export |

No source move was necessary. Moving presentation out of the Gateway package
would add churn without improving its already explicit ownership.

## Changes made

- narrowed `orion.__all__` to frozen contracts, Runtime, Gateway boundary and
  presentation models;
- changed historical tests to import historical modules explicitly;
- normalized the implemented Understand operator and payload version to `1.0`;
- updated stale contract, source, schema and ownership status text;
- added a public-surface freeze test;
- removed the obsolete packaged `orion-demo` Phase 1A entry point while
  retaining its historical source components at explicit module paths;
- added the consolidated Version 1 reading and release documents.

## Intentionally retained

- historical phase records and earlier architecture freeze snapshots;
- draft transition/registry prototypes needed to reproduce earlier tests;
- the opt-in Ollama experiment;
- the repository development version until a release is explicitly authorized;
- unrelated pre-existing worktree changes in `CHANGELOG.md` and
  `scripts/check-boundaries`.

## Removed or moved

The obsolete Phase 1A `orion-demo` entry module was removed because it was a
packaged interface outside the Version 1 public lifecycle. No current production
behavior was relocated or deleted. The cleanup changes discoverability and
supported import boundaries, not architecture.
