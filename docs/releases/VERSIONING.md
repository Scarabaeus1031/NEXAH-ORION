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

`1.0.0` is the immutable release of the certified baseline recorded in
`ORION_V1_CERTIFIED_BASELINE.md`. Its scope ends at
`at_slice_iv_certified`. Runtime, Gateway, LYRA execution, SIRIUS,
applications, Human Reports, presentation, reasoning, semantic interpretation,
and decision making remain outside the certified release.

Historical development versions and phase documents retain their recorded
version identifiers. They do not redefine the current repository release.

## Version source

The root `VERSION` file is the single repository-version source. Release automation may read it but must not invent or update it implicitly.
