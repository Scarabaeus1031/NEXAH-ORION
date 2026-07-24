# Slice IV WP28 — External Expression Conformance

Status: Complete

Work package: WP28

Report schema: `orion.expression-conformance/0.1-alpha`

Boundary: External Expression Conformance →
`after_expression_conformance` → STOP

## Responsibility

WP28 observes one immutable WP26 Expression Contract and one immutable WP27
Expression Artifact. It determines whether the supplied Artifact conforms
exactly to its originating Contract and the frozen WP27 construction
guarantees.

WP28 creates only an immutable `accepted` or `rejected` Conformance Report. It
constructs, repairs, normalizes, completes, certifies, communicates, or
interprets nothing.

## Accepted inputs

The validator accepts exactly:

1. immutable WP26 Expression Contract;
2. immutable WP27 Expression Artifact.

It imports no Slice III artifact type and receives no Slice III artifact.
Certified Slice III lineage is verified only through the immutable identities
and references already bound by WP26 and preserved by WP27.

## External observations

WP28 verifies:

- exact Contract type, schema, version, status, responsibility, and STOP;
- exact Artifact type, schema, identity, integrity, construction state,
  responsibility, and STOP;
- exact Contract identity, integrity, canonical reference, schema version,
  contract version, and status preserved by the Artifact;
- exact Slice III Certification, Orientation Map Conformance, Orientation Map,
  and Constructed Orientation Map references preserved by the Artifact;
- exact provenance continuity;
- exact communicative scope;
- exact declared lossiness;
- exact declared exclusions;
- canonical declaration order and duplicate absence;
- canonical Contract and Artifact serialization;
- absence of unexpected payload or authority fields;
- complete input immutability.

Unknown, missing, changed, duplicated, malformed, inconsistent, or unexpected
content produces a deterministic rejected report. The validator does not repair
the supplied artifacts.

## Immutable Conformance Report

The canonical report records:

- deterministic report identity;
- immutable report schema version;
- observed Contract identity, integrity, and canonical reference;
- observed Expression identity, integrity, and canonical reference;
- `accepted` or `rejected` decision;
- deterministic ordered checks and errors;
- accepted Expression reference only when every check passes;
- input-immutability observation;
- `external_expression_conformance` responsibility;
- explicit `after_expression_conformance` STOP.

The report contains validation results only. It contains no Expression payload,
Human-facing report, generated language, interpretation, presentation, or
certification status.

## Determinism and serialization

The report identity basis is canonical UTF-8 JSON containing every report field
except its self-referential identifier.

The identifier uses the first 24 hexadecimal characters of the basis SHA-256
digest.

Equal canonical Contract and Artifact bytes produce a byte-identical
Conformance Report.

## Canonical proof

Run:

```bash
make slice-iv-expression-conformance
```

The proof terminates at:

```text
Expression Contract
        +
Expression Artifact
        ↓
External Observation
        ↓
Conformance Validation
        ↓
Canonical Conformance Report
        ↓
after_expression_conformance
        ↓
STOP
```

The proof verifies:

- frozen WP26 and WP27 source fingerprints;
- exact Contract and Artifact authority references;
- exact provenance continuity;
- immutable inputs;
- deterministic accepted decision;
- canonical report serialization;
- byte-identical replay;
- absence of construction, certification, language generation, LYRA, SIRIUS,
  Runtime, Gateway, presentation, and Human-report behavior.

Run the focused suite:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest \
  tests.test_expression_conformance_alpha
```

## Explicit exclusions

WP28 performs no:

- Contract or Expression construction;
- repair, reconstruction, normalization, completion, or rewriting;
- Slice III artifact access or Orientation Map reconstruction;
- semantic interpretation, inference, reasoning, ranking, or recommendation;
- language generation or Human-facing reporting;
- presentation, HTML, Markdown rendering, UI, or visualization;
- Expression Certification or Vertical Slice IV Certification;
- LYRA, SIRIUS, Runtime, Gateway, application, or external-system behavior.

WP28 ends immediately after the immutable report is canonically serialized at
`after_expression_conformance`.
