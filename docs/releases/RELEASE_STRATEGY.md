# Release Strategy

## Independent releases

Core, ORION, Library, and Builder Hub release independently. An ORION tag never implies a coordinated ecosystem release unless a separate compatibility bundle explicitly pins all repositories.

## Release types

| Type | Purpose | Tag example |
|---|---|---|
| development | repository workshop and unstable contracts | no required tag; `VERSION` may contain prerelease |
| preview | bounded contributor testing | `v0.2.0-alpha.1` |
| candidate | release verification | `v0.2.0-rc.1` |
| stable repository release | supported ORION contract/runtime scope | `v0.2.0` |
| ecosystem compatibility bundle | known compatible independent releases | dated manifest, not a shared code version |

## Phase 1B release boundary

Phase 1B may release documentation, workshop tooling, the bounded offline
execution slice, and the local Ollama reference adapter. It must not claim:

- a stable or production ORION runtime;
- model independence demonstrated across multiple real providers;
- a public cross-repository contract;
- Core, Library, or Builder compatibility beyond pinned documentation;
- production readiness.

## Release inputs

- clean working tree;
- accepted ADRs for included architecture decisions;
- updated `VERSION` and `CHANGELOG.md`;
- passing `scripts/check-workspace`;
- passing `scripts/release-check`;
- compatibility matrix for every external contract used;
- release notes with limitations and postponed work;
- human approval by the ORION release owner.

## Release process

1. Open a release branch only when needed for stabilization.
2. Set the target version according to `VERSIONING.md`.
3. Freeze scope; unfinished work remains under `Unreleased`.
4. Run repository and compatibility checks.
5. Create release notes from the template.
6. Merge the reviewed release change.
7. Create an annotated Git tag matching `VERSION` without prerelease metadata mismatch.
8. Publish artifacts only from the tagged commit.
9. Record supported external revisions.
10. Begin the next development version in a separate change.

## Rollback

Git history and published tags are never rewritten. A bad release is deprecated and followed by a corrective release. External state effects follow the governing repository's own recovery policy.
