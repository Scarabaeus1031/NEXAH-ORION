# ORION Version 1 Release Notes

- Repository version: `1.0.0`
- Release status: immutable certified baseline
- Final certified STOP: `at_slice_iv_certified`

## What ORION Version 1 is

ORION Version 1 is the certified deterministic Orientation Core within the
NEXAH ecosystem. It accepts already-confirmed, immutable structural material
and proves one bounded chain through Structural Representation, UNDERSTAND,
Relations, Navigation, Orientation Map, and Expression.

Every stage owns one explicit responsibility, preserves provenance and
immutability, serializes canonically, and stops at its declared boundary.

## Certified capabilities

- deterministic Markdown Structural Representation for the frozen Version 1
  profile;
- external Representation conformance;
- UNDERSTAND inventory of already-declared structural elements;
- deterministic Structural Summary and Structural Statistics;
- immutable structural and declared Relations;
- external Relation conformance and Relations certification;
- immutable Navigation construction, conformance, and certification;
- deterministic Orientation Map construction and conformance;
- Vertical Slice III certification;
- immutable Expression Contract and deterministic Expression Construction;
- external Expression conformance and Expression certification;
- Vertical Slice IV certification.

The canonical responsibility inventory is
[`ORION_V1_CERTIFIED_BASELINE.md`](ORION_V1_CERTIFIED_BASELINE.md).

## Explicit exclusions

Version 1 does not certify or execute:

- Runtime;
- Gateway;
- LYRA;
- SIRIUS;
- applications;
- Human Reports;
- presentation;
- reasoning;
- semantic interpretation;
- decision making.

Earlier repository work concerning these responsibilities remains historical,
experimental, or separately governed. Its presence does not broaden the
certified release.

## Deterministic guarantees

For the certified chain, Version 1 guarantees:

- immutable artifacts;
- canonical UTF-8 JSON serialization;
- stable deterministic identities and SHA-256 integrity;
- complete provenance continuity;
- byte-identical proof replay for equal accepted inputs;
- external conformance before certification;
- no mutation of certified predecessor artifacts;
- explicit STOP boundaries.

## Compatibility

Downstream repositories must pin the exact immutable ORION release commit and
the canonical-content fingerprint published for that commit. They must
regenerate derived contracts or artifacts and rerun their complete verification
before publication.

No compatible consumer acquires ORION authority by consuming a certified
artifact. Human meaning and judgment remain outside ORION.

## Canonical downstream fingerprint

The Version 1 downstream-compatibility fingerprint is:

`6201362c094530a0a31fa3d80b46c9131011bb8c8d400183271b0da0eb423f8d`

It is the SHA-256 of the sorted per-file SHA-256 manifest defined by
`scripts/orion-v1-fingerprint`. The fingerprint covers the established
cross-repository contract surface: `VERSION`, `workspace.yaml`, the Phase VII
corpus manifest, the frozen Orientation policies and operators, the earlier
public-contract specifications and their executable contract, Runtime and
Gateway bindings. Certified Slice II–IV artifacts retain their own frozen
internal fingerprints and proof chains.

Run `./scripts/orion-v1-fingerprint` from any clean checkout of the release
commit. The output must match the value above.
