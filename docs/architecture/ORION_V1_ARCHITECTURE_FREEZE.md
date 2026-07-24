# ORION v1 Architecture Freeze

> Historical F1 freeze record. Its accepted boundary remains decision evidence;
> current Version 1 status and inventory are defined by the
> [Phase VIII Architecture Audit](../releases/ORION_V1_ARCHITECTURE_AUDIT.md).

- Baseline ID: `orion-architecture-v1`
- Status: Frozen
- Freeze phase: F1
- Freeze date: 2026-07-19
- Repository version: `0.3.0-dev.0`
- Governing decision: [`ADR-0008`](../adr/0008-orion-v1-architecture-freeze.md)
- Release status: development baseline; no tag or public release

## 1. Baseline statement

Phases 0 through 6C are complete. ORION is architecture-complete and
interaction-complete for its first bounded human-facing, deterministic and
provider-independent architecture. “Complete” means that responsibilities,
authority, dependency direction, contracts, planning and language boundaries
are coherent and executable where declared. It does not mean that
transformations, Renderers, mathematical Operators or production integrations
exist.

This document is the official baseline reference. Future work extends it. A
change that redefines a frozen item requires explicit Architecture Review and an
accepted ADR.

## 2. Canonical architecture

```text
Human
  ↕ canonical language
LYRA                         translation and faithful explanation only
  ↕ existing runtime inputs and exact reports
ORION                        orchestration, context, validation and navigation
  ↕ published external boundaries only
NEXAH Core / Library         independent deterministic and knowledge authorities

Reasoning Backend → ORION  replaceable proposal source; never an authority
Builder Hub → ORION        independent application boundary; not vendored
LUCY                         reserved future Reflection Boundary; no current path
```

Two deterministic flows coexist without collapsing responsibility:

### Reasoning flow

```text
OrientationRequest
→ DocumentSelector
→ RepositoryContextProvider
→ ContextBuilder
→ ContextManifest
→ ContextBriefBuilder
→ ContextBrief
→ ReasoningBackend
→ ReasoningResult
→ Validation
→ OrientationResponse
```

Selection chooses explicit paths. The Provider reads those paths. The Builder is
the sole `ContextManifest` creator. The Brief is an immutable, content-free
projection. A Reasoning Backend returns only provider-neutral, untrusted results.
Validation remains independent.

### Representation-navigation flow

```text
HumanLanguageRequest
→ LYRA translation
→ OrientationObject + RepresentationTarget
→ TransformationEngine
→ TransformationPlan + TransformationReport
→ LYRA explanation
→ Human
```

The Transformation Engine navigates only registered graph edges, verifies
Transition Contracts and reports provenance, evidence, invariants and blockers.
It performs no transformation mathematics, Operator execution or rendering.
LYRA retains the exact report and never plans or validates.

## 3. Frozen authority and responsibility matrix

| Layer | Owns | Must never own |
|---|---|---|
| NEXAH Core | deterministic objects, relations, invariants and canonical decisions | model reasoning or ORION runs |
| ORION | request lifecycle, deterministic context, backend boundary, result validation, route planning, reports and audit metadata | Kernel truth, Library identity, human approval or UI authority |
| Reasoning Backend | provider translation and provider-neutral proposals | validation, canonical truth, Kernel or Library writes |
| Transformation Engine | deterministic graph navigation and contract verification | mathematics, Operator selection/execution, rendering, inference or persistence |
| Operator Registry | immutable capability declarations for T01–T15 | selection, loading, execution or invented mathematics |
| LYRA | canonical vocabulary translation and faithful report explanation | reasoning, planning, routing, validation, contracts, Operators, Renderers or providers |
| NEXAH Library | independent curated knowledge and editorial authority | ORION navigation or Kernel invariants |
| Builder Hub | independent operator-facing interaction | model, ORION, Kernel or Library authority |
| Human | intention, delegated authority and required approval | replaceable automation behavior |
| LUCY | nothing in this baseline | every current ORION responsibility; future boundary only |

Dependency direction remains inward toward owned ports and outward through
adapters. NEXAH Core has no dependency on ORION. Provider-specific objects never
cross a Reasoning Backend boundary. LYRA depends on existing ORION models but the
Transformation Engine does not depend on LYRA.

## 4. Canonical terminology

The following terms and casing are frozen for normative prose. Python symbols
are language bindings of the same concepts, not synonyms.

| Canonical term | Python binding where present | Frozen meaning |
|---|---|---|
| Orientation Object | `OrientationObject` | immutable identity-bearing object being represented |
| Representation | `RepresentationRef` | one identified projection of an Orientation Object |
| Representation Target | `RepresentationTarget` | requested registered destination Representation |
| Source Representation | Transition Contract field | declared input role of one transition |
| Target Representation | Transition Contract field | declared output role of one transition; not the request object |
| Representation Graph | `RepresentationGraph` | explicit T01–T15 connectivity; no inferred edges |
| Transition Contract | `TransitionContract` | versioned permission and constraint record for one graph edge |
| Transformation Engine | `TransformationEngine` | deterministic route planner and contract verifier |
| Transformation Plan | `TransformationPlan` | selected path, alternatives, evidence and provenance plan |
| Transformation Report | `TransformationReport` | authoritative navigation result, validation and issues |
| Operator Registry | `OperatorRegistry` | declarative, non-executing Operator capability inventory |
| Reasoning Backend | `ReasoningBackend` | provider-neutral proposal port |
| Context Manifest | `ContextManifest` | immutable record of exactly what context was loaded |
| Context Brief | `ContextBrief` | immutable content-free presentation metadata derived from a manifest |
| LYRA | `orion.lyra` / `Lyra*` | non-authoritative human-language boundary |
| Orientation Session | documentation plus conformance case | versioned reproducible Human → ORION → Human scenario |
| Kernel | external NEXAH Core authority | deterministic decision boundary; not part of ORION |

“Orientation Engine”, “Reasoning Engine” and provider model names are not
substitutes for Transformation Engine. Historical evidence may preserve earlier
wording, but new normative documents use this table.

Representation Target and Target Representation are deliberately distinct: the
first is an existing runtime request model; the second is an output field inside
one Transition Contract. They must not be used interchangeably.

## 5. Frozen architecture principles

The principles frozen from the accepted architecture are:

1. Structure First.
2. Observe Before Naming.
3. Evidence Before Interpretation.
4. One Kernel, Many Representations.
5. Separation of Authority.
6. Break Down → Bridge → Build.
7. Preserve Difference and Provenance.
8. Stable Core, Replaceable Components.
9. Multiple Representations, Explicit Translation.
10. Human-Governed Impact.
11. Preserve and Share Deliberately.
12. Learn Through Feedback Without Rewriting History.

These principles constrain extensions; they are not executable algorithms.

## 6. Frozen repository and documentation structure

| Path | Frozen role |
|---|---|
| `src/orion/` | ORION-owned runtime and internal contracts |
| `src/orion/lyra/` | translation and explanation only |
| `docs/architecture/` | normative current architecture and bounded specializations |
| `docs/adr/` | immutable accepted decision history |
| `docs/development/` | phase history, reproduction and contributor guidance |
| `docs/governance/` | ownership, compatibility and cross-repository rules |
| `docs/orientation_sessions/` | canonical executable interaction documentation |
| `docs/architecture/plates/src/` | canonical editable SVG Plate sources |
| `docs/architecture/plates/*.png` | generated documentation artifacts; never edited directly |
| `tests/` | ORION-owned conformance and regression verification |
| `scripts/` | repository checks and workshop automation |
| `.workspace/` | ignored local research, experiments, runs and sibling repositories |

Documentation authority is: accepted ADRs, this freeze baseline and the current
architecture, specialized architecture documents, then generated visual
companions. Evidence and historical phase documents explain evolution but do not
override current normative documents.

Architecture Plates obey one path only:

```text
canonical SVG → generated PNG → embedding Markdown → governing ADR
```

A material change requires all affected elements to be reviewed together.

## 7. Current capabilities

- immutable provider-neutral Phase 1 request, result, validation and provenance
  contracts;
- deterministic `FakeBackend` and loopback-only Ollama reference adapter;
- deterministic explicit repository document selection and read-only loading;
- reproducible `ContextManifest` and content-free `ContextBrief`;
- explicit Representation Graph and versioned T01–T15 Transition Contracts;
- deterministic shortest-route and alternative-route planning;
- invariant, compatibility, evidence and provenance reporting;
- immutable non-executable Operator Registry;
- deterministic canonical LYRA planning-language mappings and faithful report
  explanations;
- thirteen canonical Orientation Sessions backed by executable conformance tests;
- reproducible Architecture Plate generation and drift detection.

The architecture is provider-independent because provider types and lifecycle
remain behind the Reasoning Backend port. Only one real provider adapter is
currently implemented; multi-provider production equivalence is not claimed.

## 8. Known limitations

- No registered transformation has an executable Operator.
- No Renderer is implemented or executable.
- `TransformationReport.produced_representation` remains `None`.
- Transition mathematics and datasets remain unknown or candidate evidence.
- Repository context uses explicit rules only; no semantic retrieval exists.
- LYRA supports a deliberately bounded deterministic language, not open natural
  language or AI interpretation.
- Ollama is an externally managed local runtime and is never started or stopped
  by ORION.
- NEXAH Core, NEXAH Library and Builder Hub are not vendored.
- No stable public cross-repository API, production release or stable semantic
  version tag exists.
- LUCY is neither specified as runtime nor implemented.

## 9. Intentionally unfrozen extension points

The following may be designed later without reopening the baseline if they obey
its ownership and authority:

- Operator implementations;
- Renderer implementations;
- transformation execution;
- mathematical models and verification datasets;
- additional Reasoning Backend adapters;
- future retrieval strategies;
- the separate future LUCY Reflection Boundary.

An extension that changes a frozen term, responsibility, contract, dependency or
authority is not merely an extension and requires a superseding ADR.

## 10. Architecture review summary

| Reviewed surface | Result |
|---|---|
| README and current-phase statement | aligned to F1 and maintenance mode |
| Architecture overview and specializations | same authority model; historical roadmap explicitly marked |
| ADR-0001 through ADR-0008 | accepted, indexed and mutually compatible |
| Development guides | Phase 0–6C history retained; F1 index added |
| Repository and component ownership | complete; LYRA and composition ownership explicit |
| Architecture Plates | ten SVG sources and ten reproducible PNG artifacts synchronized |
| Orientation Sessions | thirteen indexed scenarios with one-to-one conformance coverage |
| Runtime tests | deterministic boundaries and documented scenarios covered |
| Repository hygiene | no tracked secrets, model weights, caches, run artifacts or machine-specific paths |
| Release and version documentation | development baseline retained at `0.3.0-dev.0` |
| Changelog | F1 freeze and review recorded under Unreleased |

Resolved documentation drift was limited to obsolete “Proposed”, Phase 1B
current-state and pre-implementation roadmap wording. No runtime, API, schema,
planning behavior or authority changed during F1.

## 11. Verification status

The F1 baseline requires and records:

| Verification | Result |
|---|---|
| Unit and documentation-backed tests | passed; 75 tests, 1 opt-in Ollama integration skip |
| Frozen Phase file checksums | passed |
| Boundary checks | passed |
| Workspace checks | passed |
| Architecture consistency | passed for T01–T15 |
| Architecture Plate checks | passed for 10 SVG/PNG pairs |
| Markdown link checks | passed |
| Python syntax and import checks | passed |
| Development release gate | passed |
| Repository hygiene | passed |
| Repository version | unchanged at `0.3.0-dev.0` |

The skipped Ollama integration is not a failure: the runtime is externally
managed and integration remains opt-in. No production release gate, tag, public
release or push is part of F1.

## 12. Repository health and transition

The repository is suitable as the first stable architecture baseline. Core
architecture enters maintenance mode: corrections and extensions continue, but
redefinition requires explicit review.

The next separate architectural phase may define LUCY as a Reflection Boundary.
It must build on this baseline and may not change deterministic planning,
Transition Contracts, validation, Kernel authority or LYRA's non-authoritative
role merely by being added above them.
