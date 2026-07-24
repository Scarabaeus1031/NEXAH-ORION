# Slice IV WP30 — Vertical Slice IV Certification

Status: Complete

Work package: WP30

Report schema: `orion.slice-iv-certification/0.1-alpha`

Boundary: Vertical Slice IV Certification → `at_slice_iv_certified` → STOP

## Responsibility

WP30 observes exactly one immutable WP29 Expression Certification Report and
records one immutable Vertical Slice IV Certification Report.

WP30 certifies and closes Vertical Slice IV only. It does not construct,
perform conformance, repair, interpret, present, or execute any artifact.

## Accepted input

The certifier accepts exactly:

1. one immutable WP29 Expression Certification Report.

It does not accept or import the Expression Contract, Expression Artifact,
External Expression Conformance Report, Slice III artifacts, or Orientation
Map artifacts. Earlier work packages are not reopened or reconstructed.

The frozen WP29 decision is `certified`. This is the accepted Expression
Certification state required by WP30.

## Certification observations

WP30 requires:

- the exact WP29 report type;
- the frozen WP29 schema, responsibility, and STOP;
- a canonical and valid WP29 certification identity;
- valid deterministic WP29 certification integrity;
- the `certified` WP29 decision;
- complete canonical WP29 provenance.

Failure of any observation produces no Slice IV Certification Report. WP30
does not repair, normalize, rerun, or replace WP29.

## Immutable Certification Report

The canonical report records only:

- deterministic Slice IV certification identity;
- deterministic Slice IV certification integrity;
- certification schema and version;
- observed WP29 certification identity;
- observed WP29 certification integrity;
- `certified` decision;
- canonical WP29 provenance reference;
- `vertical_slice_iv_certification` responsibility;
- explicit `at_slice_iv_certified` STOP.

The report contains no Expression payload, Contract, Conformance Report,
Orientation Map, language, presentation, semantic content, or runtime state.

## Identity, integrity, and serialization

The certification basis is canonical UTF-8 JSON containing every report field
except the self-derived Slice IV certification identity and integrity.

- `certification_integrity` is the lowercase SHA-256 hexadecimal digest of
  that basis;
- `certification_id` is
  `slice-iv-certification-<first 24 digest characters>`;
- `expression_certification_integrity` preserves the exact integrity declared
  by WP29;
- `provenance_ref` is the SHA-256 reference of the exact canonical WP29 report
  bytes;
- equal certified WP29 reports produce byte-identical Slice IV Certification
  Reports.

The immutable report validates these invariants whenever it is constructed or
deserialized.

## Frozen implementation baseline

The canonical WP30 proof verifies the implementation fingerprints of:

- WP26 — Expression Contract;
- WP27 — Expression Construction;
- WP28 — External Expression Conformance;
- WP29 — Expression Certification.

Fingerprint verification belongs to the repository proof. The WP30
Certification Report remains limited to its single WP29 input and does not
embed or reopen preceding implementation artifacts.

## Canonical proof

Run:

```bash
make slice-iv-certification
```

The proof terminates at:

```text
WP26 Expression Contract
        ↓
WP27 Expression Construction
        ↓
WP28 External Expression Conformance
        ↓
WP29 Expression Certification
        ↓
WP30 Vertical Slice IV Certification
        ↓
at_slice_iv_certified
        ↓
STOP
```

The proof verifies:

- frozen WP26–WP29 implementation fingerprints;
- exact WP29 identity and integrity preservation;
- exact WP29 canonical provenance;
- WP29 input immutability;
- deterministic Slice IV certification identity and integrity;
- canonical UTF-8 JSON serialization;
- byte-identical replay;
- absence of prior-stage reconstruction, Runtime, Gateway, LYRA, SIRIUS,
  applications, presentation, language generation, and semantic
  interpretation.

Run the focused suite:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest \
  tests.test_slice_iv_certification_alpha
```

## Explicit exclusions

WP30 performs no:

- Contract, Expression, Conformance, or WP29 reconstruction;
- construction, conformance, repair, normalization, rewriting, or mutation;
- semantic interpretation, inference, reasoning, ranking, or recommendation;
- language generation or Human-facing reporting;
- presentation, HTML, Markdown, UI, graphics, or visualization;
- LYRA, SIRIUS, Runtime, Gateway, application, or external-system behavior.

WP30 ends immediately after the immutable Certification Report is canonically
serialized at `at_slice_iv_certified`.
