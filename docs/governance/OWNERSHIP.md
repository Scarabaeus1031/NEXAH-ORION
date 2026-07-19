# Ownership Map

Ownership is defined by responsibility and authority, not by convenience or import direction.

## Repository ownership

| Repository | Owns | Does not own |
|---|---|---|
| NEXAH Core | OLS authority, deterministic contracts, Kernel behavior, existing evidence and validation | model reasoning, ORION runs, Library editorial authority, Builder UI |
| NEXAH ORION | request lifecycle, context assembly, model invocation boundary, result validation, run audit and replay | Kernel truth, OLS semantics, Library identity, human approval, application UI |
| NEXAH Library | Registry identity, Works, Editions, reader journeys, knowledge contracts and guarded editorial execution | ORION routing, Kernel invariants, Builder UI |
| Builder Hub | operator-facing request, inspection, diff and approval interaction | model or Kernel authority, Library identity |

## ORION directory ownership

| Path | Responsibility | Current status |
|---|---|---|
| `docs/architecture/` | current architecture and recovered baselines | active |
| `docs/adr/` | immutable decision history | active |
| `docs/governance/` | ownership and cross-repository rules | active |
| `docs/releases/` | release, version and compatibility policy | active |
| `docs/development/` | contributor and workspace process | active |
| `schemas/` | future ORION-owned public cross-repository contracts | reserved; no public contracts approved |
| `src/orion/` | internal contracts, backend port, validation, execution and local Ollama adapter | active |
| `tests/` | ORION-owned contract and execution verification | active |
| `tools/` | maintained ORION repository tools | reserved |
| `scripts/` | repository workshop automation | active |
| `.workspace/` | local, untracked research, experiments, runs and sibling repositories | local only |

## Ownership test

A change belongs in ORION only if all are true:

1. It concerns ORION's request, run, context, reasoning, validation, audit, or replay responsibility.
2. It does not redefine an existing Core, OLS, Library, or Builder authority.
3. Its persistent data and effects are governed by ORION.
4. Its compatibility can be reviewed without editing an external repository implicitly.

If any answer is no or unknown, route the work to the owning repository or open a cross-repository decision.

## Current human ownership placeholders

Individual names and teams are intentionally not invented. `.github/CODEOWNERS` uses the repository maintainer fallback until explicit owner handles are confirmed. Replacing placeholders requires a governance PR, not code changes.
