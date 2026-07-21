# Ownership Map

This map derives from the adopted
[NEXAH Ecosystem Constitution v1.0](https://github.com/Scarabaeus1031/NEXAH/blob/main/GOVERNANCE/ECOSYSTEM_CONSTITUTION.md).
The Constitution defines the Houses and their authority. This document assigns
concrete ORION repository and component responsibilities within those
boundaries; it does not repeat or amend constitutional principles.

Ownership is defined by responsibility and authority, not by convenience or import direction.

## Repository ownership

| Repository | Owns | Does not own |
|---|---|---|
| NEXAH Framework / OLS / Kernel | framework definitions, OLS authority, deterministic contracts, Kernel behavior, existing evidence and validation | model reasoning, ORION runs, Library editorial authority, Builder UI |
| NEXAH-ORION | request lifecycle, context selection and assembly, model invocation boundary, result validation, representation-route planning, contract verification, run audit and replay | Kernel truth, OLS semantics, mathematical transformation operators not yet approved, renderer authority not yet implemented, Library identity, human approval, application UI |
| Library House (currently canonical in `NEXAH/LIBRARY`) | Registry identity, Works, Editions, reader journeys, knowledge contracts and guarded editorial execution | ORION routing, Kernel invariants, Builder UI |
| Builder Hub | operator-facing request, inspection, diff and approval interaction | model or Kernel authority, Library identity |

## ORION directory ownership

| Path | Responsibility | Current status |
|---|---|---|
| `docs/architecture/` | current architecture and recovered baselines | active |
| `docs/architecture/plates/` | canonical SVG sources and generated PNG companions to authoritative Markdown and ADRs | active; PNG is never edited directly and plates cannot change architecture independently |
| `docs/adr/` | immutable decision history | active |
| `docs/governance/` | ownership and cross-repository rules | active |
| `docs/releases/` | release, version and compatibility policy | active |
| `docs/development/` | contributor and workspace process | active |
| `schemas/` | future ORION-owned public cross-repository contracts | reserved; no public contracts approved |
| `src/orion/` | internal contracts, context pipeline, backend ports/adapters, validation, explicit representation graph, declarative operator inventory, transformation planning, blocker reports and LYRA language boundary | active; transformation operator implementations and renderers absent |
| `tests/` | ORION-owned contract and execution verification | active |
| `tools/` | maintained ORION repository tools | reserved |
| `scripts/` | repository workshop automation | active |
| `.workspace/` | local, untracked research, experiments, runs and sibling repositories | local only |

## ORION component ownership

| Component | Owner | Sole responsibility | Explicit non-responsibility |
|---|---|---|---|
| `DocumentSelector` | ORION selection layer | map explicit request scopes to ordered repository-relative paths | file I/O, discovery, ranking, manifests |
| `RepositoryContextProvider` | ORION context-source boundary | load only explicitly selected repository documents read-only | selection, hashing policy, backend calls |
| `ContextBuilder` | ORION context-integrity layer | create the Phase 2 `ContextManifest` from loaded documents | document selection, reasoning, validation |
| `ContextBriefBuilder` | ORION presentation-metadata layer | derive an immutable content-free `ContextBrief` | content access, prompts, summarization, backend calls |
| Reasoning backend ports and adapters | ORION reasoning boundary | return provider-neutral untrusted `ReasoningResult` objects | Validation, Kernel or Library mutation |
| Validation | ORION validation boundary | validate backend results against the original `ContextManifest` | canonical Kernel decisions |
| Representation Graph registry | ORION representation-planning boundary | enumerate only registered `T01–T15` edges | infer transitions or execute operators |
| Transition Contract registry | ORION representation-planning boundary | expose the normalized planning metadata of `T01–T15` | upgrade evidence or provide algorithms |
| Operator Registry | ORION capability-inventory boundary | expose immutable operator identity, lifecycle, compatibility, evidence and ownership metadata | select, rank, load or execute operators; provide mathematics |
| `TransformationEngine` | ORION navigation layer | plan deterministic routes and report provenance, evidence, compatibility and blockers | mathematics, operators, rendering, target production, persistence, LLM calls, Kernel mutation |
| LYRA language boundary | ORION human-language layer | deterministically map canonical requests to existing planning inputs and faithfully explain the exact structured report | reasoning, planning, routing, validation, contracts, operators, renderers, providers, Kernel truth |
| `LyraOrientationExecutor` | ORION composition layer | sequence translation, unchanged Engine planning and explanation through dependency injection | language inference, planning policy, validation changes, operator or renderer execution |
| Transition operator implementations | unassigned until separately approved | none in the current baseline | all Phase 5A registry entries are non-executable |
| Renderers | future ORION Representation boundary | none in the current baseline | not executable in the frozen baseline; never LYRA authority |

## Architecture maintenance mode

The frozen scope is defined in
[`ORION_V1_ARCHITECTURE_FREEZE.md`](../architecture/ORION_V1_ARCHITECTURE_FREEZE.md).
Additive work must preserve this ownership map. Changing an owner, sole
responsibility, explicit non-responsibility or repository boundary is an
architecture change and requires an accepted ADR before implementation.

## Ownership test

A change belongs in ORION only if all are true:

1. It concerns ORION's request, run, context, reasoning, validation, audit, or replay responsibility.
2. It does not redefine an existing Core, OLS, Library, or Builder authority.
3. Its persistent data and effects are governed by ORION.
4. Its compatibility can be reviewed without editing an external repository implicitly.

If any answer is no or unknown, route the work to the owning repository or open a cross-repository decision.

## Current human ownership placeholders

Individual names and teams are intentionally not invented. `.github/CODEOWNERS` uses the repository maintainer fallback until explicit owner handles are confirmed. Replacing placeholders requires a governance PR, not code changes.
