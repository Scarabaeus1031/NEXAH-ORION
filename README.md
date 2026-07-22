# NEXAH-ORION

ORION is the model-independent reasoning and orchestration repository above the frozen NEXAH Kernel.

This repository contains the frozen ORION v1 Architecture Baseline established
after Phases 0–6C. It includes the deterministic reasoning boundary, context
pipeline, Representation Architecture, Transformation Engine, declarative
Operator Registry, LYRA language boundary and canonical Orientation Sessions.
`FakeBackend` remains the offline reasoning baseline; `OllamaBackend` is the
first real implementation of the frozen provider-neutral port.

The governing rule is:

> The model proposes. The Orchestrator validates. The Kernel decides.

## Start here

| I want to… | Read |
|---|---|
| understand the ecosystem's highest governance baseline | [NEXAH Ecosystem Constitution v1.0](https://github.com/Scarabaeus1031/NEXAH/blob/main/GOVERNANCE/ECOSYSTEM_CONSTITUTION.md) |
| understand the architecture | [`docs/architecture/ORION_ARCHITECTURE.md`](docs/architecture/ORION_ARCHITECTURE.md) |
| inspect the official ORION v1 freeze | [`docs/architecture/ORION_V1_ARCHITECTURE_FREEZE.md`](docs/architecture/ORION_V1_ARCHITECTURE_FREEZE.md) |
| read the F1 architecture review | [`docs/architecture/ORION_V1_ARCHITECTURE_REVIEW.md`](docs/architecture/ORION_V1_ARCHITECTURE_REVIEW.md) |
| understand representation and rendering | [`docs/architecture/REPRESENTATION_ARCHITECTURE.md`](docs/architecture/REPRESENTATION_ARCHITECTURE.md) |
| navigate the Orientation Transform Stack | [`docs/architecture/transformations/ORIENTATION_TRANSFORM_STACK.md`](docs/architecture/transformations/ORIENTATION_TRANSFORM_STACK.md) |
| inspect the versioned transformation contracts | [`docs/architecture/transformations/contracts/TRANSITION_CONTRACT_SPECIFICATION.md`](docs/architecture/transformations/contracts/TRANSITION_CONTRACT_SPECIFICATION.md) |
| understand the operator capability inventory | [`docs/architecture/operators/OPERATOR_ARCHITECTURE.md`](docs/architecture/operators/OPERATOR_ARCHITECTURE.md) |
| understand LYRA's human-language boundary | [`docs/architecture/lyra/LYRA_ARCHITECTURE.md`](docs/architecture/lyra/LYRA_ARCHITECTURE.md) |
| explore why LUCY may exist | [`docs/architecture/lucy/LUCY_CONCEPT.md`](docs/architecture/lucy/LUCY_CONCEPT.md) |
| inspect the LUCY Concept Freeze | [`docs/architecture/lucy/LUCY_CONCEPT_REVIEW.md`](docs/architecture/lucy/LUCY_CONCEPT_REVIEW.md) |
| walk through the first NEXAH Alpha experience | [`docs/experience/FIRST_USER_JOURNEY.md`](docs/experience/FIRST_USER_JOURNEY.md) |
| browse the canonical Architecture Plates | [`docs/architecture/plates/README.md`](docs/architecture/plates/README.md) |
| inspect the recovered Core baseline | [`docs/architecture/baselines/PHASE_0_BASELINE_RECOVERY.md`](docs/architecture/baselines/PHASE_0_BASELINE_RECOVERY.md) |
| prepare my local workspace | [`docs/development/WORKSPACE.md`](docs/development/WORKSPACE.md) |
| browse completed development phases | [`docs/development/README.md`](docs/development/README.md) |
| understand where work belongs | [`docs/governance/OWNERSHIP.md`](docs/governance/OWNERSHIP.md) |
| contribute a change | [`CONTRIBUTING.md`](CONTRIBUTING.md) |
| inspect the publication candidate | [`docs/releases/RELEASE_CANDIDATE.md`](docs/releases/RELEASE_CANDIDATE.md) |
| inspect the exact Core mismatch | [`docs/releases/CORE_COMPATIBILITY_REPORT.md`](docs/releases/CORE_COMPATIBILITY_REPORT.md) |
| propose an architecture decision | [`docs/adr/README.md`](docs/adr/README.md) |
| prepare a release | [`docs/releases/RELEASE_STRATEGY.md`](docs/releases/RELEASE_STRATEGY.md) |
| inspect publication readiness | [`docs/releases/PUBLICATION_BASELINE.md`](docs/releases/PUBLICATION_BASELINE.md) |
| inspect the first execution slice | [`docs/development/PHASE_1A_EXECUTION.md`](docs/development/PHASE_1A_EXECUTION.md) |
| run the local Ollama backend | [`docs/development/PHASE_1B_OLLAMA.md`](docs/development/PHASE_1B_OLLAMA.md) |
| verify the executable baseline | [`docs/development/PHASE_1B_CLOSEOUT.md`](docs/development/PHASE_1B_CLOSEOUT.md) |
| build deterministic repository context | [`docs/development/PHASE_2A_CONTEXT.md`](docs/development/PHASE_2A_CONTEXT.md) |
| derive repository documents from request scope | [`docs/development/PHASE_2B_SELECTION.md`](docs/development/PHASE_2B_SELECTION.md) |
| derive a deterministic content-free context brief | [`docs/development/PHASE_2C_CONTEXT_BRIEF.md`](docs/development/PHASE_2C_CONTEXT_BRIEF.md) |
| plan deterministic representation transitions | [`docs/development/PHASE_4A_TRANSFORMATION_ENGINE.md`](docs/development/PHASE_4A_TRANSFORMATION_ENGINE.md) |
| inspect the Phase 5A operator placeholders | [`docs/development/PHASE_5A_OPERATOR_REGISTRY.md`](docs/development/PHASE_5A_OPERATOR_REGISTRY.md) |
| understand the Phase 6A language model | [`docs/development/PHASE_6A_LYRA_LANGUAGE.md`](docs/development/PHASE_6A_LYRA_LANGUAGE.md) |
| run the Phase 6B Human → ORION → Human boundary | [`docs/development/PHASE_6B_LYRA_INTEGRATION.md`](docs/development/PHASE_6B_LYRA_INTEGRATION.md) |
| execute canonical Phase 6C Orientation Sessions | [`docs/orientation_sessions/README.md`](docs/orientation_sessions/README.md) |

## Repository boundary

```text
NEXAH Framework / OLS / Kernel   definitions, semantics and deterministic contracts
NEXAH-ORION                      deterministic navigation, reports, validation and LYRA
Library House                    Works, Editions and editorial identity
Builder Hub                      independent operator-facing application
```

The NEXAH Framework and Builder Hub are not vendored into this repository. The
canonical Library Registry currently lives under `NEXAH/LIBRARY`; the
constitutional Library House does not by itself require an independent
repository. Local working copies and reserved workspace entries are described
by [`workspace.yaml`](workspace.yaml).

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

Reserved Library and Builder Hub workspace entries remain unavailable until an
authoritative repository identity and baseline are separately approved. Those
entries do not establish new constitutional authority.

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
| Library identity, records or editorial execution | the Library House; currently `NEXAH/LIBRARY`, never ORION |
| Builder UI and operator interaction | Builder Hub, never here |

## Repository status

Under the adopted Ecosystem Constitution, ORION is the House that navigates.
This repository therefore owns deterministic navigation, reports, validation
and the LYRA language boundary; it does not own Experience presentation,
Library identity or Human interpretation, Reflection and decision.

The Phase 7A LUCY Concept Freeze remains a non-normative boundary record. LUCY
is not an ORION component or constitutional House. The Human remains the one
who reflects and decides.

The F1 ORION Architecture Baseline remains frozen, architecture-complete and
interaction-complete for its scope. Core architecture stays in maintenance mode:
a change to frozen terminology, responsibilities, authority, contracts,
dependency direction or structure requires explicit Architecture Review and an
accepted ADR.

The Phase 6C Orientation Sessions remain the executable Human → LYRA → ORION
→ LYRA → Human conformance baseline. LYRA does not reason, plan, route,
validate, render, execute, call a provider, or upgrade evidence. LUCY remains
outside the execution path. Phase 7 asks what human Reflection means before any
future architecture is considered.

Architecture Plates follow a source/artifact rule: SVG files under
`docs/architecture/plates/src/` are canonical and editable; PNG files are
generated documentation artifacts and are never edited directly.

The Operator Registry remains the current transformation capability
baseline: all T01–T15 entries are non-executable and deterministic routing is
unchanged. Ollama remains an externally managed runtime; ORION never starts or
stops it. Run all isolated tests with `make test`; the `llama3.1:8b` integration
remains opt-in through `make integration`.

No registered transition is currently executable. ORION can navigate documented
representation routes, attach declarative operator metadata and produce
Transformation Plans and blocker reports, but it never generates a
Representation Target; `produced_representation` remains `None`.

The repository remains `0.3.0-dev.0`. The F1 freeze is an architecture baseline,
not a public release, stable semantic-version tag or production-readiness claim.
Its current publication blockers and exact Core-pin mismatch are recorded in
[`docs/releases/PUBLICATION_BASELINE.md`](docs/releases/PUBLICATION_BASELINE.md).

The public repository identity is
[`Scarabaeus1031/NEXAH-ORION`](https://github.com/Scarabaeus1031/NEXAH-ORION).
It publishes the independent ORION development baseline; public release tags
and stable API claims remain governed separately. The verified Core pin is
unchanged.

Original software is licensed under the [Apache License 2.0](LICENSE).
Original documentation, specifications, research, books and visual material
are licensed under [CC BY 4.0](LICENSE-DOCS.md) where applicable. Third-party
and source-derived material retains its stated terms. See the complete
[Licensing Scope](LICENSES.md).

Community participation follows the canonical
[`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md); security reports follow
[`SECURITY.md`](SECURITY.md).
