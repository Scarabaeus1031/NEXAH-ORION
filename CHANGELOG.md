# Changelog

All notable changes to the ORION repository are recorded here.

The format follows Keep a Changelog principles. Versions follow the policy in [`docs/releases/VERSIONING.md`](docs/releases/VERSIONING.md).

## [Unreleased]

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
