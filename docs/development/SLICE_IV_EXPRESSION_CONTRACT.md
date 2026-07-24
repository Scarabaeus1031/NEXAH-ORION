# Slice IV WP26 — Expression Contract

Status: Complete

Work package: WP26

Contract schema: `orion.expression-contract/0.1-alpha`

Contract version: `0.1-alpha`

Boundary: Expression Contract → `at_expression_contract` → STOP

## Responsibility

WP26 defines one immutable Expression Contract. It binds the exact certified
Slice III Orientation Map lineage to explicit declarations of communicative
scope, lossiness, and exclusions.

The contract defines what a future Expression may communicate. It constructs,
formats, communicates, validates, or certifies no Expression.

## Accepted certified inputs

Creation accepts only:

1. a passed immutable Vertical Slice III Certification Report;
2. the exact accepted Orientation Map Conformance Report named by it;
3. the exact immutable Orientation Map Object accepted by that report;
4. the exact immutable Constructed Orientation Map accepted by that report.

Every identity and SHA-256 reference must resolve to one certified lineage.
Missing, rejected, substituted, malformed, or inconsistent artifacts fail
before a contract exists.

## Immutable contract

The canonical contract records:

- deterministic contract identity and complete integrity digest;
- immutable schema, contract, and serialization versions;
- exact Slice III Certification identity and reference;
- exact Orientation Map Conformance identity and reference;
- exact Orientation Map identity and reference;
- exact Constructed Orientation Map identity and reference;
- Slice III Certification as the canonical provenance reference;
- canonically ordered declared communicative scope;
- canonically ordered declared lossiness;
- canonically ordered declared exclusions;
- `contract_defined` status;
- `expression_contract` responsibility;
- explicit `at_expression_contract` STOP.

The identity basis is canonical UTF-8 JSON containing every contract field
except the self-referential identity and integrity fields. The identifier uses
the first 24 hexadecimal characters of the basis SHA-256 digest. Integrity
preserves the full digest.

## Communicative scope

WP26 accepts only the architecture-authorized scope vocabulary:

- `canonical_order`;
- `certified_boundaries`;
- `declared_absence`;
- `orientation_map_entries`;
- `orientation_map_identity`;
- `provenance`;
- `structural_adjacency`.

Scope, lossiness, and exclusion declarations must be non-empty, unique, and
lexicographically ordered. The contract rejects rather than normalizes an
unordered, duplicate, malformed, or unsupported declaration.

These declarations authorize no Expression behavior. They are immutable inputs
to the later WP27 responsibility.

## Contract validation

The WP26 validator observes:

- strict contract shape;
- exact certified lineage;
- deterministic identity and integrity;
- exact artifact references;
- preservation of the WP26 STOP.

Validation does not perform External Expression Conformance. It validates the
contract itself and cannot construct, repair, normalize, complete, or certify
an Expression.

## Canonical serialization

Serialization uses canonical UTF-8 JSON:

- keys sorted lexicographically;
- compact separators;
- Unicode preserved;
- declarations retained in their already-canonical order;
- no implicit defaults or hidden fields.

Equal certified inputs and equal declarations produce byte-identical contract
bytes.

## Canonical proof

Run:

```bash
make slice-iv-expression-contract
```

The proof terminates at:

```text
Certified Slice III STOP
        ↓
Expression Contract
        ↓
Contract Validation
        ↓
Canonical Serialization
        ↓
at_expression_contract
        ↓
STOP
```

The proof verifies:

- source-fixture integrity;
- frozen WP12–WP25 source fingerprints;
- passed Slice III Certification;
- accepted Orientation Map Conformance;
- exact Map Object and Construction references;
- input immutability;
- deterministic identity and canonical serialization;
- byte-identical replay;
- provenance preservation;
- absence of WP27–WP30, LYRA, SIRIUS, Runtime, Gateway, and presentation
  execution.

Run the focused suite:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest \
  tests.test_expression_contract_alpha
```

## Explicit exclusions

The contract contains no:

- rendered text or generated language;
- prompts, models, providers, or templates;
- HTML, Markdown rendering, visualization, UI, or presentation;
- semantic interpretation, reasoning, recommendation, or action;
- Runtime or Gateway information;
- Expression Construction;
- External Expression Conformance;
- Expression Certification;
- Vertical Slice IV Certification;
- LYRA or SIRIUS behavior.

WP26 ends immediately after the immutable contract is validated and serialized
at `at_expression_contract`.
