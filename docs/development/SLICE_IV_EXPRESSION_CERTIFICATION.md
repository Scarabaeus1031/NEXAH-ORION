# Slice IV WP29 — Expression Certification

Status: Complete

Work package: WP29

Report schema: `orion.expression-certification/0.1-alpha`

Boundary: Expression Certification → `at_expression_certified` → STOP

## Responsibility

WP29 observes exactly one immutable WP28 External Expression Conformance
Report. If and only if that report is accepted and internally valid, WP29
records one immutable Expression Certification Report.

WP29 certifies only. It does not construct, validate, repair, interpret,
present, or execute any artifact.

## Accepted input

The certifier accepts exactly:

1. one immutable WP28 External Expression Conformance Report.

It does not accept or import the Expression Contract, Expression Artifact,
Slice III artifacts, or Orientation Map artifacts. Earlier work packages are
not reopened or reconstructed.

## Certification observations

WP29 requires:

- the exact WP28 report type;
- the frozen WP28 schema, responsibility, and STOP;
- a canonical and valid WP28 report identity;
- an accepted conformance decision;
- `valid = true`;
- no conformance errors;
- an exact accepted Expression reference;
- confirmed WP28 input immutability;
- complete canonical WP28 provenance.

Failure of any observation produces no Certification Report. WP29 does not
repair, normalize, rerun, or replace WP28.

## Immutable Certification Report

The canonical report records only:

- deterministic certification identity;
- deterministic certification integrity;
- certification schema and version;
- observed WP28 report identity;
- observed WP28 report integrity and canonical reference;
- observed accepted Expression reference;
- `certified` decision;
- WP28 provenance reference;
- `expression_certification` responsibility;
- explicit `at_expression_certified` STOP.

The report contains no Expression payload, Contract, Orientation Map, language,
presentation, semantic content, runtime state, or Vertical Slice IV
certification.

## Identity, integrity, and serialization

The certification basis is canonical UTF-8 JSON containing every report field
except the self-derived certification identity and integrity.

- `certification_integrity` is the lowercase SHA-256 hexadecimal digest of
  that basis;
- `certification_id` is
  `expression-certification-<first 24 digest characters>`;
- the observed WP28 integrity is the SHA-256 digest of the exact canonical
  WP28 report bytes;
- all artifact references use `sha256:<lowercase hexadecimal digest>`;
- equal accepted WP28 reports produce byte-identical Certification Reports.

The immutable report validates these invariants whenever it is constructed or
deserialized.

## Canonical proof

Run:

```bash
make slice-iv-expression-certification
```

The proof terminates at:

```text
Accepted WP28 Expression Conformance Report
        ↓
Expression Certification
        ↓
Canonical Certification Report
        ↓
at_expression_certified
        ↓
STOP
```

The proof verifies:

- the frozen WP28 implementation fingerprint;
- exact WP28 identity, integrity, and accepted Expression references;
- WP28 provenance continuity;
- input immutability;
- deterministic certification identity and integrity;
- canonical UTF-8 JSON serialization;
- byte-identical replay;
- absence of Contract reconstruction, Expression construction, conformance
  reruns, Vertical Slice IV certification, language generation, LYRA, SIRIUS,
  Runtime, Gateway, applications, presentation, and Human-facing reporting.

Run the focused suite:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest \
  tests.test_expression_certification_alpha
```

## Explicit exclusions

WP29 performs no:

- Contract, Expression, conformance, or earlier-artifact reconstruction;
- Expression construction or conformance validation;
- repair, normalization, completion, rewriting, or mutation;
- semantic interpretation, inference, reasoning, ranking, or recommendation;
- language generation or Human-facing reporting;
- presentation, HTML, Markdown, UI, graphics, or visualization;
- Vertical Slice IV Certification;
- LYRA, SIRIUS, Runtime, Gateway, application, or external-system behavior.

WP29 ends immediately after the immutable Certification Report is canonically
serialized at `at_expression_certified`.
