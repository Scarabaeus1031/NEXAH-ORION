# Changelog

All notable changes to the ORION repository are recorded here.

The format follows Keep a Changelog principles. Versions follow the policy in [`docs/releases/VERSIONING.md`](docs/releases/VERSIONING.md).

## [Unreleased]

### Added

- NEXAH Alpha First User Journey specifying the complete five-minute experience
  from a blank browser through question, orientation, evidence, human Reflection
  and a pressure-free departure without extending the frozen architecture.
- Phase 7A LUCY Concept Review confirming that Reflection remains human-owned,
  non-authoritative and outside the ORION Architecture Baseline, with explicit
  unresolved questions and bounded recommendations for future exploration.
- Phase 7 non-normative LUCY concept exploration defining Reflection from a
  human perspective, its relationship to ORION and LYRA, and its strict absence
  of planning, validation, evidence, provenance, contract or Kernel authority.
- Reflection Manifest, conceptual boundary diagram, open-question register and
  future human-centered research directions without runtime or implementation.
- Phase F1 official ORION v1 Architecture Freeze report, canonical terminology,
  frozen/unfrozen scope, repository-health record and accepted ADR-0008.
- Development and Architecture index entries making the frozen baseline the
  authoritative current reference while retaining completed phase history.
- Phase 6C canonical Orientation Sessions covering navigation, faithful
  explanation, blocked routes, missing capabilities, unknown and ambiguous
  requests, unsupported vocabulary, report comparison, inspection, validation
  and alternatives.
- Documentation-backed Phase 6C conformance tests that execute every indexed
  session and preserve status, evidence, provenance, validation, alternatives,
  blockers and report identity.
- Phase 6B deterministic LYRA runtime boundary with canonical vocabulary,
  explicit source-to-target translation, provider-neutral clarification and
  unsupported-language failures, faithful `TransformationReport` explanation,
  and an ORION-owned Human → ORION → Human composition root.
- Phase 6B tests preserving status, evidence, provenance, blockers,
  alternatives, validation and exact report identity across the round trip.
- Canonical ten-plate Architecture Plate collection covering system perspective,
  workflow, representations, graph, contracts, planning, operator inventory,
  LYRA, documentation projections and the evidence/inference boundary.
- Canonical editable SVG sources and generated PNG documentation artifacts for
  all ten plates, with repository checks that forbid source loss and direct
  raster-only maintenance.
- Phase 6A LYRA architecture establishing the canonical human-facing Orientation
  Vocabulary, the bidirectional translation model, authority boundaries,
  conversation principles, examples, and the reserved LUCY reflection boundary
  without parser, prompts, LLM integration, or runtime changes.
- Phase 6A development documentation distinguishing existing ORION input and
  report models from future language translation contracts.
- Phase 5A immutable, versioned Operator Registry with one non-executable
  placeholder for every T01–T15 transition, exact Phase 3C status/evidence
  continuity, compatibility and ownership metadata, deterministic lookup, and
  additive Transformation Plan reporting without selection or execution.
- Phase 5A operator architecture, development guide, boundary checks, and tests
  for lifecycle, coverage, immutability, compatibility and Engine integration.
- Phase 4A immutable Transformation Engine with explicit `T01–T15` graph and
  contract registries, deterministic shortest-path and alternative-route
  planning, provenance/evidence propagation, invariant and compatibility checks,
  and provider-neutral blocker reports without operator or renderer execution.
- Phase 4A tests and development documentation covering supported and missing
  paths, contracts, operators, renderers, versions, provenance, evidence, and
  invariants.
- Phase 3C provider-independent `TransitionContract` specification and one
  versioned draft contract for every registered graph edge `T01–T15`, including
  explicit input/output profiles, coordinates, units, epochs, parameters,
  invariant and loss declarations, evidence/dataset gaps, renderer compatibility,
  validation rules, and deterministic failure conditions.
- Phase 3B Orientation Transform Stack with a branched Representation Graph,
  ten-state Representation Matrix, fifteen Transition Cards, invariant mapping,
  candidate operators, and prioritized missing evidence.
- Phase 3A provider-independent Representation and Rendering Architecture,
  formalizing Orientation Objects, immutable projections, renderer families,
  documentation levels, identity preservation, and LYRA ownership boundaries.
- Immutable, content-free `ContextBrief` contract and deterministic
  `ContextBriefBuilder` preserving manifest order, hashes, revisions, lengths,
  and provenance.
- Additive brief-capable backend port and execution composition without changing
  the frozen Phase 1 backend interface.
- Phase 2C integrity, equality, immutability, provenance, and execution tests plus
  context-brief architecture documentation.
- Deterministic request-scope document selection with versioned explicit rules,
  immutable selection results, and auditable rule provenance.
- Selection-aware execution composition that delegates manifest creation to the
  unchanged Phase 2A Context Builder.
- Phase 2B tests and documentation for unknown scopes, empty selections,
  ordering, duplicate elimination, path-only results, and rule provenance.
- Deterministic, read-only repository context provider using explicit document
  selection only.
- Context builder and contextual execution composition ahead of the existing
  reasoning backend boundary.
- Unit coverage and Phase 2A documentation for ordering, duplicate prevention,
  missing documents, path containment, immutability, and provenance.

### Changed

- Consolidated obsolete proposed, pre-implementation roadmap and Phase 1B
  current-state wording without changing runtime behavior, contracts or APIs.
- Declared core architecture in maintenance mode: future redefinition requires
  explicit Architecture Review and an accepted ADR.

## [0.3.0-dev.0] - 2026-07-19

### Added

- First real `ReasoningBackend` reference implementation for local Ollama.
- Strict loopback-only HTTP transport using the Python standard library.
- Configurable model, endpoint, and timeout.
- Unit, configuration, timeout, malformed-response, validation-boundary, and
  opt-in local integration tests for `llama3.1:8b`.
- Phase 1B closeout record and hardened repository ignore policy.

### Changed

- Declared Ollama an externally managed runtime; unreachable services now fail
  with a provider-neutral backend error and never trigger lifecycle management.

## [0.2.0-dev.0] - 2026-07-19

### Added

- First complete offline ORION execution slice.
- Immutable request, context, result, validation, response, and provenance contracts.
- Replaceable backend port with a deterministic `FakeBackend`.
- Acceptance tests for the valid path, backend replacement, provenance integrity,
  immutability, and rejected backend output.

## [0.1.0-dev.0] - 2026-07-19

### Added

- Initial architecture review.
- Stable ORION architecture baseline.
- Phase 0 NEXAH Core baseline recovery map.
