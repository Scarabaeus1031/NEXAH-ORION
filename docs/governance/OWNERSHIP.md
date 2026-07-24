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
| NEXAH-ORION | the certified deterministic chain from Structural Representation through UNDERSTAND, Relations, Navigation, Orientation Map and Expression certification | Runtime, Gateway, LYRA execution, SIRIUS, applications, Human Reports, presentation, semantic interpretation, decision making, Library identity and Human authority |
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
| `docs/architecture/contracts/` | earlier frozen public contract specifications | retained; outside the certified Version 1 Core baseline |
| `schemas/` | optional machine-readable transport encodings of the public contracts | reserved; no transport encoding approved |
| `src/orion/` certified Slice II–IV modules | certified Structural Representation, UNDERSTAND, Relations, Navigation, Orientation Map and Expression responsibilities | active; certified Version 1 implementation |
| `src/orion/public_contracts/` | earlier executable contract models and canonical fixtures | retained; outside the certified Version 1 Core baseline |
| `src/orion/orientation_runtime/` | earlier minimal Runtime proof | retained; outside the certified Version 1 Core baseline |
| `src/orion/gateway/` | earlier Gateway and presentation proof | retained; outside the certified Version 1 Core baseline |
| `src/orion/` other phase modules | historical internal conformance slices and experiments | retained; not exported as Version 1 public APIs |
| `evaluation/` | reproducible evaluation corpus, traces and reviews | active; no runtime authority |
| `tests/` | ORION-owned contract and execution verification | active |
| `tools/` | maintained ORION repository tools | reserved |
| `scripts/` | repository workshop automation | active |
| `.workspace/` | local, untracked research, experiments, runs and sibling repositories | local only |

## ORION component ownership

| Component | Owner | Sole responsibility | Explicit non-responsibility |
|---|---|---|---|
| Structural Representation | ORION Representation boundary | deterministically materialize the accepted source structure with identity, ordering, locators, provenance, integrity and declared lossiness | semantic interpretation, source repair, Runtime or presentation |
| External Representation Conformance | ORION conformance boundary | observe and validate an immutable Structural Representation | construction, repair, mutation or interpretation |
| UNDERSTAND Inventory | ORION structural inventory boundary | inventory only already-declared immutable source elements | parsing, discovery, inference, summary or statistics |
| Structural Summary | ORION structural summary boundary | deterministically describe organization already present in the Representation | semantics, source access or statistical aggregation |
| Structural Statistics | ORION structural statistics boundary | deterministically derive certified structural measures | semantics, ranking or recommendation |
| Relations | ORION Relations boundary | create only the certified structural and explicitly declared relations | semantic inference, graph authority, navigation or mutation |
| Navigation | ORION Navigation boundary | construct deterministic movement over certified Relations | relation creation, ranking, recommendation or path inference |
| Orientation Map | ORION Orientation Map boundary | construct the immutable derived structural map from certified Navigation | storage, visualization, geometry, interpretation or presentation |
| Expression | ORION Expression boundary | bind and construct only the certified, bounded Expression artifact and certify its conformance | generated language, presentation, Human Reports, Runtime or LYRA execution |
| Slice certifications | ORION certification boundary | observe accepted predecessor certifications and freeze their deterministic boundary | reconstruction, validation, repair, execution or new authority |

The following rows describe earlier architecture slices retained for historical
reproducibility. They do not enlarge the certified Version 1 baseline.

| Component | Owner | Sole responsibility | Explicit non-responsibility |
|---|---|---|---|
| Public Contract Suite | earlier ORION contract boundary | define and validate the earlier frozen public language | certified Version 1 Core authority, Runtime behavior, transport, presentation policy |
| `OrientationRuntime` | earlier ORION Runtime proof | execute the earlier bounded Understand workflow | certified Version 1 Core authority, gateway translation, presentation, transport, providers or persistence |
| `OrientationGateway` | earlier ORION Gateway proof | translate inputs and map the earlier bounded presentation result | certified Version 1 Core authority, orientation, evidence selection, reasoning |
| Presentation mapping | earlier ORION presentation proof | derive fields from the earlier public contract result | certified Version 1 Core authority, modifying contracts or inventing findings |
| Evaluation harness | ORION Evaluation boundary | run reproducible historical sessions and record observations | production behavior, certified contract authority, architecture authority |
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

These explicit module paths remain internal and do not enlarge the supported
Version 1 public interface.

## Architecture maintenance mode

The frozen scope is defined in
[`ORION_V1_ARCHITECTURE_FREEZE.md`](../architecture/ORION_V1_ARCHITECTURE_FREEZE.md).
Additive work must preserve this ownership map. Changing an owner, sole
responsibility, explicit non-responsibility or repository boundary is an
architecture change and requires an accepted ADR before implementation.

## Ownership test

A change belongs in ORION only if all are true:

1. It concerns an authority explicitly assigned to ORION by the certified
   Version 1 baseline or a separately governed future boundary.
2. It does not redefine an existing Core, OLS, Library, or Builder authority.
3. Its persistent data and effects are governed by ORION.
4. Its compatibility can be reviewed without editing an external repository implicitly.

If any answer is no or unknown, route the work to the owning repository or open a cross-repository decision.

## Current human ownership placeholders

Individual names and teams are intentionally not invented. `.github/CODEOWNERS` uses the repository maintainer fallback until explicit owner handles are confirmed. Replacing placeholders requires a governance PR, not code changes.
