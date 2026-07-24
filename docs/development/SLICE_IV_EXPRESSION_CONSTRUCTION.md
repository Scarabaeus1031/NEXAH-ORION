# Slice IV WP27 — Expression Construction

Status: Complete

Work package: WP27

Artifact schema: `orion.expression-artifact/0.1-alpha`

Boundary: Expression Construction → `after_expression_construction` → STOP

## Responsibility

WP27 constructs one immutable Expression Artifact exclusively from one valid
WP26 Expression Contract.

It materializes the authority and references already present in the contract.
It does not reopen the bound Slice III artifacts, copy Orientation Map content,
generate language, interpret information, validate External Conformance,
certify Expression, or present anything.

## Accepted input

Construction accepts exactly one input:

- immutable WP26 Expression Contract at `at_expression_contract`.

The constructor imports no Slice III artifact type. It cannot receive,
revalidate, reconstruct, or repair the Slice III Certification, Orientation
Map Conformance, Orientation Map Object, or Constructed Orientation Map already
bound by the contract.

## Immutable Expression Artifact

The canonical artifact records:

- deterministic Expression identity and complete integrity digest;
- immutable artifact and serialization versions;
- exact Expression Contract identity, integrity, reference, schema version,
  contract version, and status;
- exact Slice III Certification reference preserved by the contract;
- exact Orientation Map Conformance reference;
- exact Orientation Map identity and reference;
- exact Constructed Orientation Map identity and reference;
- unchanged provenance reference;
- unchanged communicative scope;
- unchanged declared lossiness;
- unchanged declared exclusions;
- atomic canonical order `0`;
- `constructed_unvalidated` state;
- `expression_construction` responsibility;
- `externally_conformant: false`;
- explicit `after_expression_construction` STOP.

The artifact contains references and declarations only. It contains no
rendered or Human-facing Expression content.

## Deterministic construction

The identity basis is canonical UTF-8 JSON containing every artifact field
except the self-referential Expression identity and integrity fields.

The identifier uses the first 24 hexadecimal characters of the basis SHA-256
digest. Integrity preserves the complete digest.

Equal canonical Expression Contract bytes always produce equal canonical
Expression Artifact bytes.

Construction preserves the existing canonical order of communicative scope,
lossiness, and exclusions. It does not normalize or reorder declarations.

## Construction validation

WP27 construction validates only its own immutable invariants:

- exact WP26 Contract shape and STOP;
- strict artifact field set;
- deterministic identity and integrity;
- exact Contract reference;
- exact preservation of scope, lossiness, exclusions, and provenance;
- canonical declaration order;
- canonical serialization round-trip;
- `constructed_unvalidated` state;
- absence of an External Conformance claim.

This is not External Expression Conformance. WP27 cannot accept, reject,
repair, complete, or certify the Expression Artifact.

## Canonical proof

Run:

```bash
make slice-iv-expression-construction
```

The proof terminates at:

```text
at_expression_contract
        ↓
Expression Construction
        ↓
Construction Validation
        ↓
Canonical Serialization
        ↓
after_expression_construction
        ↓
STOP
```

The proof verifies:

- the frozen WP26 source fingerprint;
- WP26 Contract immutability;
- strict artifact round-trip;
- deterministic identity and canonical serialization;
- byte-identical replay;
- exact Contract identity and integrity;
- exact scope, lossiness, exclusions, and provenance;
- absence of External Conformance, certification, generated language, LYRA,
  SIRIUS, Runtime, Gateway, presentation, rendering, graphics, and reports.

Run the focused suite:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest \
  tests.test_expression_construction_alpha
```

## Explicit exclusions

WP27 performs no:

- Human-language generation;
- prompts, provider calls, or LLM behavior;
- semantic interpretation, inference, reasoning, ranking, or recommendation;
- relation, orientation, order, authority, or provenance creation;
- input repair or mutation;
- HTML, Markdown rendering, UI structure, graphics, reports, or presentation;
- External Expression Conformance;
- Expression Certification;
- Vertical Slice IV Certification;
- LYRA, SIRIUS, Runtime, Gateway, or application behavior.

WP27 ends immediately after the immutable artifact is structurally valid,
canonically serialized, and stopped at `after_expression_construction`.
