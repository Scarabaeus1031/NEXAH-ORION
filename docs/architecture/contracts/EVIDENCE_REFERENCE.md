# Evidence Reference

- Status: Canonical public specification; runtime implementation pending
- Contract ID: `orion.evidence-reference`
- Contract version: `1.0`
- Scope: public identity, provenance and traceability of evidence used by ORION
- Effects: none

## 1. Purpose

An Evidence Reference lets a consumer trace a report finding to the material,
authority, version and derivation that support, counter, contextualize or limit
it.

It is a reference contract, not the evidence content itself. It does not grant
access, editorial status or canonical authority.

Evidence behavior is governed by
[`ORION_ORIENTATION_POLICIES.md`](../operators/ORION_ORIENTATION_POLICIES.md).
This specification defines only the stable public reference.

### Suite position

This is chapter 3 of the public contract suite. Evidence References are
versioned traceability records used by Orientation Reports; they are not a
separate orientation outcome. It inherits the canonical vocabulary in
[`ORIENTATION_REQUEST.md`](ORIENTATION_REQUEST.md#65-canonical-suite-vocabulary).
Read next:
[`ORIENTATION_REPORT.md`](ORIENTATION_REPORT.md).

## 2. Scope

This specification defines:

- evidence identity and version;
- source provenance;
- authority and editorial status;
- evidence class and relationship;
- derivation trace;
- validation and integrity;
- report traceability;
- compatibility behavior.

It does not define retrieval, storage, ranking, inference or Library mutation.

## 3. Normative language

The terms **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT** and **MAY** are
normative. Examples use illustrative field notation only.

## 4. Authority boundaries

- The source owner owns source identity and source version.
- The Library or declared editorial owner owns editorial status.
- ORION owns the relationship between an Evidence Reference and its report
  findings.
- A derivation owner owns the declared derivation rule and version.
- LYRA MAY explain evidence fields but MUST NOT promote or reinterpret them.
- A consumer MUST NOT infer authority from inclusion in a report.
- Providers, prompts, orchestration, transport, internal plans and reasoning
  strategies MUST NOT appear in an Evidence Reference.

## 5. Common envelope

| Field | Required | Rule |
|---|---:|---|
| `schema_version` | yes | supported `orion.evidence-reference/<major>.<minor>` |
| `evidence_id` | yes | stable evidence identity |
| `evidence_version` | yes | exact version of this reference record |
| `source` | yes | Source Reference |
| `authority` | yes | Authority Declaration |
| `evidence_class` | yes | `observed`, `derived`, `proposed` or `unknown` |
| `relationship` | yes | `supports`, `counters`, `contextualizes` or `limits` |
| `provenance` | yes | ordered, possibly empty Provenance Step list |
| `validation` | yes | Evidence Validation |
| `traceability` | yes | one or more report or finding targets |
| `access_status` | yes | `available`, `restricted`, `unavailable` or `unknown` |

## 6. Identity and source

### 6.1 Source Reference

| Field | Required | Rule |
|---|---:|---|
| `source_id` | yes | stable source identity within `identity_domain` |
| `source_version` | yes | exact version or explicit `unknown` |
| `identity_domain` | yes | domain that owns source identity |
| `source_owner` | yes | authoritative owner or explicit `unknown` |
| `source_ref` | yes | traceable external or canonical reference |
| `fragment_ref` | no | stable fragment, passage, row, field or region reference |
| `integrity_ref` | no | Integrity Reference for content verification |

`evidence_id` identifies the evidence record. `source_id` identifies the source.
They MUST NOT be treated as the same identity.

### 6.2 Integrity Reference

An Integrity Reference contains:

- `method` — declared integrity method;
- `value` — method-specific integrity value;
- `coverage` — exact source or fragment covered;
- `verified` — `true`, `false` or `unknown`.

No integrity method is implied when `integrity_ref` is absent.

## 7. Authority Declaration

| Field | Required | Rule |
|---|---:|---|
| `authority_owner` | yes | owner of the declared evidence status or explicit `unknown` |
| `authority_domain` | yes | domain in which the declaration applies |
| `editorial_status` | yes | `draft`, `reviewed`, `published`, `withdrawn`, `unclassified` or `unknown` |
| `authority_version` | yes | exact declaration version or explicit `unknown` |
| `declared_at` | no | source-owned temporal reference |

Editorial status MUST NOT be inferred from source format, popularity, location
or inclusion in an Orientation Report.

## 8. Evidence class

| Class | Meaning | Required provenance |
|---|---|---|
| `observed` | directly present in the cited source or approved Representation | source and fragment sufficient for inspection |
| `derived` | produced by a declared deterministic rule from cited inputs | complete ordered derivation steps and input evidence refs |
| `proposed` | non-authoritative interpretation or hypothesis | source refs, proposal origin and explicit proposed status |
| `unknown` | evidence relationship cannot be established | gaps and failed validation or access reason |

Evidence class is not editorial authority, truth status or confidence.

## 9. Evidence relationship

`relationship` describes how the evidence relates to each traceability target:

- `supports` — contributes positive support;
- `counters` — contradicts or weakens the target;
- `contextualizes` — establishes relevant context without directly supporting;
- `limits` — defines a boundary, omission or known limitation.

One Evidence Reference has one relationship in version `1.0`. The same source
used in another relationship requires a distinct Evidence Reference identity.

## 10. Provenance

Each Provenance Step contains:

| Field | Required | Rule |
|---|---:|---|
| `step_id` | yes | unique within this Evidence Reference |
| `step_kind` | yes | `source`, `representation`, `transition`, `derivation` or `proposal` |
| `input_refs` | yes | ordered, possibly empty source, Representation or Evidence refs |
| `output_ref` | yes | exact output of the step |
| `owner` | yes | owner of the step declaration |
| `contract_id` | no | governing contract when applicable |
| `contract_version` | no | required when `contract_id` is present |
| `lossiness` | yes | `none`, declared loss items, or `unknown` |

Provenance steps MUST be ordered from source toward the referenced evidence
record. A missing step MUST be declared as a provenance gap; it MUST NOT be
silently bridged.

## 11. Validation

Evidence Validation contains:

| Field | Required | Rule |
|---|---:|---|
| `status` | yes | `valid`, `invalid` or `unverified` |
| `checks` | yes | ordered, possibly empty check identifiers |
| `issues` | yes | ordered, possibly empty issue identifiers |
| `validated_against` | yes | contract and policy versions |

`valid` requires completed declared checks and no validation errors. `invalid`
evidence MAY remain in a report only when visibly marked and relevant to a
blocker, conflict or audit trail. `unverified` MUST NOT be presented as valid.

### 11.1 Transition evidence levels

An Evidence Reference MAY include:

- `evidence_level`;
- `evidence_scale_id`;
- `evidence_scale_version`.

These fields are valid only when an authoritative Evidence or Transition
Contract supplies the scale. `E0–E4` MUST NOT be invented as a general report
confidence score.

## 12. Traceability

`traceability` is a non-empty ordered list. Each target contains:

| Field | Required | Rule |
|---|---:|---|
| `report_id` | yes | exact Orientation Report identity |
| `report_version` | yes | exact report version |
| `target_path` | yes | stable public path to a finding, issue or mode-payload field |
| `finding_id` | no | stable finding identity when one exists |

Every substantive public finding MUST have at least one Evidence Reference or
be explicitly classified `unknown` with an evidence gap.

## 13. Versioning

`schema_version` uses:

```text
orion.evidence-reference/<major>.<minor>
```

A major change alters evidence classes, relationship meaning, identity,
authority, provenance or validation semantics. A minor change may add optional
metadata that cannot promote authority or evidence status.

`schema_version` versions this contract language. `evidence_version` versions
an immutable Evidence Reference. They are never interchangeable.

## 14. Canonical invariants

1. Evidence identity and source identity remain distinct.
2. Source owner and editorial authority remain explicit.
3. Evidence class and relationship remain explicit.
4. Provenance is ordered and gaps remain visible.
5. Derived evidence names its inputs and governing rule.
6. Proposed evidence never becomes observed through repetition or presentation.
7. Counterevidence remains first-class evidence.
8. Validation status is never inferred from inclusion in a report.
9. Traceability reaches exact report fields.
10. No Evidence Reference grants access or mutation authority.
11. `evidence_id + evidence_version` identifies one immutable Evidence
    Reference, including its provenance and authority declarations.

## 15. Examples

### 15.1 Observed supporting evidence

```yaml
schema_version: orion.evidence-reference/1.0
evidence_id: evidence-paper-claim-01
evidence_version: "1"
source:
  source_id: paper-01
  source_version: "3"
  identity_domain: library.publications
  source_owner: author-team-01
  source_ref: source-paper-01-section-4
  fragment_ref: section-4.paragraph-2
authority:
  authority_owner: library-editorial
  authority_domain: library.publications
  editorial_status: published
  authority_version: "7"
evidence_class: observed
relationship: supports
provenance:
  - step_id: source-step-01
    step_kind: source
    input_refs: []
    output_ref: source-paper-01-section-4-paragraph-2
    owner: author-team-01
    lossiness: none
validation:
  status: valid
  checks: [source_resolved, version_resolved, fragment_resolved]
  issues: []
  validated_against: [orion.evidence-reference/1.0]
traceability:
  - report_id: report-understand-01
    report_version: "1"
    target_path: mode_payload.claims_and_support[0]
    finding_id: finding-claim-01
access_status: available
```

### 15.2 Derived evidence with declared loss

```yaml
schema_version: orion.evidence-reference/1.0
evidence_id: evidence-derived-01
evidence_version: "1"
source:
  source_id: representation-observation-01
  source_version: "1"
  identity_domain: nexah.representations
  source_owner: nexah
  source_ref: representation-observation-01
authority:
  authority_owner: transition-contract-owner
  authority_domain: orion.transitions
  editorial_status: reviewed
  authority_version: "1"
evidence_class: derived
relationship: contextualizes
provenance:
  - step_id: transition-step-01
    step_kind: transition
    input_refs: [representation-observation-01]
    output_ref: representation-calendar-projection-01
    owner: orion
    contract_id: T13
    contract_version: 0.1-draft
    lossiness: [spatial_detail]
validation:
  status: unverified
  checks: [identity_binding]
  issues: [missing_executable_operator]
  validated_against: [T13@0.1-draft]
traceability:
  - report_id: report-understand-01
    report_version: "1"
    target_path: issues[0]
access_status: available
```

## 16. Future compatibility

- Unknown major versions are rejected visibly.
- Optional metadata may be ignored only when evidence identity, class,
  relationship, authority, validation and traceability remain unchanged.
- New evidence classes or relationships require a major version unless a
  compatibility profile proves existing consumers can preserve meaning.
- Adapters MUST NOT collapse `counters`, `contextualizes` or `limits` into
  `supports`.
- Missing authority, version or provenance remains `unknown`; it is never filled
  by adaptation.
- Evidence references from future runtimes remain conformant only when every
  canonical invariant is preserved.
- Compatibility is suite-wide; adaptation MUST preserve every referenced
  contract identity, version and invariant.
