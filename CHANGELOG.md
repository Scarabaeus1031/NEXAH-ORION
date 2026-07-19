# Changelog

All notable changes to the ORION repository are recorded here.

The format follows Keep a Changelog principles. Versions follow the policy in [`docs/releases/VERSIONING.md`](docs/releases/VERSIONING.md).

## [Unreleased]

### Added

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
  documentation levels, identity preservation, and Lyra ownership boundaries.
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
