# Versioning

ORION uses Semantic Versioning for repository releases:

```text
MAJOR.MINOR.PATCH[-PRERELEASE]
```

## Meaning

| Change | Version |
|---|---|
| incompatible public contract, persisted record, authority or effect change | MAJOR |
| backward-compatible capability or contract addition | MINOR |
| backward-compatible fix or documentation correction affecting no contract meaning | PATCH |
| work not yet declared stable | prerelease suffix |

The initial development line is `0.y.z`. During `0.x`, breaking changes are still explicitly identified and require ADRs; the zero major version is not permission for silent incompatibility.

## Independently versioned items

Repository version and schema versions are separate:

- ORION repository release: `VERSION` and Git tag;
- each public schema: its own `schema_version`;
- ADRs: immutable sequence number, not release version;
- Architecture Baseline: status and release reference;
- compatibility bundle: dated manifest with exact repository revisions;
- prompt/renderer assets: versioned only when that implementation phase begins.

## Current version

`0.3.0-dev.0` means the Phase 1B local Ollama reference adapter exists alongside
the Phase 1A offline execution slice. Its Python contracts remain internal and
unstable; no public cross-repository contract or stable ORION runtime is released.
Python package metadata represents the same version as `0.3.0.dev0`, the PEP 440
spelling of the repository prerelease.

## Version source

The root `VERSION` file is the single repository-version source. Release automation may read it but must not invent or update it implicitly.
