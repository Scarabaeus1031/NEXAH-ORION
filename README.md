# NEXAH ORION

ORION is the model-independent reasoning and orchestration repository above the frozen NEXAH Kernel.

This repository contains the development workshop, the Phase 1A deterministic execution slice, and the Phase 1B local Ollama reference backend. `FakeBackend` remains the offline baseline; `OllamaBackend` is the first real implementation of the same provider-neutral port.

The governing rule is:

> The model proposes. The Orchestrator validates. The Kernel decides.

## Start here

| I want to… | Read |
|---|---|
| understand the architecture | [`docs/architecture/ORION_ARCHITECTURE.md`](docs/architecture/ORION_ARCHITECTURE.md) |
| inspect the recovered Core baseline | [`docs/architecture/baselines/PHASE_0_BASELINE_RECOVERY.md`](docs/architecture/baselines/PHASE_0_BASELINE_RECOVERY.md) |
| prepare my local workspace | [`docs/development/WORKSPACE.md`](docs/development/WORKSPACE.md) |
| understand where work belongs | [`docs/governance/OWNERSHIP.md`](docs/governance/OWNERSHIP.md) |
| contribute a change | [`CONTRIBUTING.md`](CONTRIBUTING.md) |
| propose an architecture decision | [`docs/adr/README.md`](docs/adr/README.md) |
| prepare a release | [`docs/releases/RELEASE_STRATEGY.md`](docs/releases/RELEASE_STRATEGY.md) |
| inspect the first execution slice | [`docs/development/PHASE_1A_EXECUTION.md`](docs/development/PHASE_1A_EXECUTION.md) |
| run the local Ollama backend | [`docs/development/PHASE_1B_OLLAMA.md`](docs/development/PHASE_1B_OLLAMA.md) |
| verify the executable baseline | [`docs/development/PHASE_1B_CLOSEOUT.md`](docs/development/PHASE_1B_CLOSEOUT.md) |

## Repository boundary

```text
NEXAH Core       deterministic authority; frozen external repository
NEXAH ORION      requests, runs, context, reasoning, validation, audit
NEXAH Library    independent knowledge and editorial authority
Builder Hub      independent operator-facing application
```

Core, Library, and Builder Hub are not vendored into this repository. Local working copies live under the ignored `.workspace/` directory and are described by [`workspace.yaml`](workspace.yaml).

## First setup

```bash
./scripts/bootstrap-workspace
./scripts/check-workspace
./scripts/test
```

To connect the already available frozen Core clone:

```bash
./scripts/bootstrap-workspace \
  --core-path /absolute/path/to/NEXAH
```

Alternatively, clone the pinned Core revision:

```bash
./scripts/bootstrap-workspace --clone-core
```

Library and Builder Hub are deliberately not cloned until their authoritative remotes and baseline revisions are recorded in `workspace.yaml`.

## Where work belongs

| Work | Destination |
|---|---|
| accepted ORION architecture | `docs/architecture/` and an ADR when ownership or contracts change |
| proposed architecture decision | `docs/adr/` |
| cross-repository rules | `docs/governance/` |
| release and compatibility policy | `docs/releases/` |
| Phase 1A internal contracts and runtime | `src/orion/` |
| public cross-repository contracts | `schemas/` only after separate approval |
| ORION-owned verification | `tests/` beside the owned behavior |
| local research | `.workspace/research/` |
| local experiments | `.workspace/experiments/` |
| local run artifacts | `.workspace/runs/` |
| release candidates and review bundles | `.workspace/releases/` |
| NEXAH semantic or deterministic Core changes | the NEXAH Core repository, never here |
| Library records or editorial execution | the independent Library repository, never here |
| Builder UI and operator interaction | Builder Hub, never here |

## Current phase

Phase 1B adds one provider adapter only: local Ollama. Ollama remains an externally
managed runtime; ORION never starts or stops it. Run the offline baseline with
`make demo`, all isolated tests with `make test`, and the opt-in `llama3.1:8b`
integration with `make integration`. Other providers, retrieval, persistence,
Kernel calls, and application integration remain postponed.

The repository development version is recorded in [`VERSION`](VERSION). No version number implies production readiness.
