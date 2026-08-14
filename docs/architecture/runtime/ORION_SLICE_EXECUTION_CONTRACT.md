# ORION Version 1.1 — Certified Slice II–IV Invocation Contract

Status: Normative, frozen for Runtime API 1.0
Contract version: `1.0.0`
Frozen Core commit: `d34fbb2f99334534f4db89465a29f8bdb16d14d3`
Frozen Core fingerprint:
`6201362c094530a0a31fa3d80b46c9131011bb8c8d400183271b0da0eb423f8d`

## 1. Purpose

This contract defines the only permitted Version 1.1 invocation of the frozen
ORION Version 1 Core. It does not add an ORION capability. It makes the
certified Slice II–IV sequence callable through a mechanical boundary.

The historical `orion.orientation_runtime` and `orion.gateway` modules are not
this invocation contract and SHALL NOT be used as substitutes or fallbacks.

Normative terms `MUST`, `MUST NOT`, `SHALL`, `SHALL NOT`, and `MAY` are to be
interpreted as requirements.

## 2. Accepted invocation input

One invocation accepts exactly:

1. one validated `orion.confirmed-material/1.0` transport artifact;
2. one valid frozen `orion.orientation-request/1.0`;
3. one valid clarification lineage as defined by
   `ORION_CLARIFICATION_CONTRACT.md`;
4. an empty Evidence collection;
5. the fixed Expression declarations in Section 7.

The Core input derived from Confirmed Material is exactly one
`ConfirmedMarkdownSource`. No other source profile is accepted by Runtime API
1.0.

The Orientation Request and clarification lineage establish request authority
and provenance at the Gateway boundary. They SHALL NOT be interpreted as input
to structural algorithms that do not accept those contracts.

## 3. Preconditions

Before invocation, the Core Invocation Adapter MUST verify:

- the checked-out Core commit equals the commit stated above;
- the canonical Core fingerprint equals the fingerprint stated above;
- every module and callable listed in Section 5 is present;
- the transport input passed Gateway validation;
- the Confirmed Material maps exactly to a valid `ConfirmedMarkdownSource`;
- the request identifies the same Orientation Object and version;
- Evidence is empty;
- no prior partial artifact exists for the invocation.

Failure of any precondition terminates before Core execution. No artifact is
published.

## 4. Source mapping

The Adapter SHALL call `ConfirmedMarkdownSource.create` with this exact
mapping:

| Frozen Core parameter | Confirmed Material field |
|---|---|
| `orientation_object_id` | `orientation_object_id` |
| `orientation_object_version` | `orientation_object_version` |
| `source_id` | `source.entry_id` |
| `source_owner` | `source.source_owner` |
| `source_ref` | `source.source_ref` |
| `content` | `source.content` |
| `confirmed_by` | `confirmation.confirmed_by` |
| `confirmed_revision` | `confirmation.confirmed_revision` |

The constructed object MUST reproduce:

- `source_revision == source.source_version`;
- `content_sha256 == source.integrity_sha256`;
- `confirmation_id == confirmation.confirmation_id`;
- CommonMark version `0.31.2`;
- boundary `whole`;
- the frozen Confirmed Markdown Source schema.

Any mismatch terminates the invocation as invalid input.

## 5. Frozen callable entry points

Only the following Core callables are normative entry points for Version 1.1:

| Stage | Module | Callable |
|---:|---|---|
| 1 | `markdown_structural_renderer_alpha` | `ConfirmedMarkdownSource.create` |
| 2 | `markdown_structural_renderer_alpha` | `MarkdownStructuralRendererAlpha.project` |
| 3 | `markdown_structural_renderer_alpha` | `MarkdownStructuralRendererAlpha.render` |
| 4 | `markdown_structural_renderer_alpha` | `validate_markdown_structural_representation` |
| 5 | `understand_source_element_inventory_alpha` | `inventory_declared_source_elements` |
| 6 | `understand_structural_summary_alpha` | `summarize_declared_structure` |
| 7 | `understand_structural_summary_alpha` | `validate_structural_summary` |
| 8 | `understand_structural_statistics_alpha` | `measure_declared_structure` |
| 9 | `understand_structural_statistics_alpha` | `validate_structural_statistics` |
| 10 | `sequential_relations_alpha` | `generate_sequential_relations` |
| 11 | `sequential_relations_alpha` | `validate_sequential_relation_set` |
| 12 | `structural_equality_relations_alpha` | `generate_structural_equality_relations` |
| 13 | `structural_equality_relations_alpha` | `validate_structural_equality_relation_set` |
| 14 | `declared_cross_references_alpha` | `generate_declared_reference_relations` |
| 15 | `declared_cross_references_alpha` | `validate_declared_reference_relation_set` |
| 16 | `relation_conformance_alpha` | `validate_relation_conformance` |
| 17 | `relations_certification_alpha` | `certify_relations` |
| 18 | `navigation_object_alpha` | `create_navigation_object` |
| 19 | `navigation_construction_alpha` | `construct_navigation` |
| 20 | `navigation_conformance_alpha` | `validate_navigation_conformance` |
| 21 | `navigation_certification_alpha` | `certify_navigation` |
| 22 | `orientation_map_object_alpha` | `create_orientation_map_object` |
| 23 | `orientation_map_construction_alpha` | `construct_orientation_map` |
| 24 | `orientation_map_conformance_alpha` | `validate_orientation_map_conformance` |
| 25 | `slice_iii_certification_alpha` | `certify_slice_iii` |
| 26 | `expression_contract_alpha` | `create_expression_contract` |
| 27 | `expression_contract_alpha` | `validate_expression_contract` |
| 28 | `expression_construction_alpha` | `construct_expression` |
| 29 | `expression_conformance_alpha` | `validate_expression_conformance` |
| 30 | `expression_certification_alpha` | `certify_expression` |
| 31 | `slice_iv_certification_alpha` | `certify_slice_iv` |

The canonical serializer associated with every produced artifact SHALL be the
serializer in that artifact's frozen module. Generic reserialization is not a
replacement.

## 6. Required execution order and outputs

The Adapter MUST execute the stages above in numeric order. It MUST retain the
following exact outputs:

| Stage | Required output |
|---:|---|
| 1 | Confirmed Markdown Source |
| 2 | Projection Mapping |
| 3 | Immutable Structural Representation |
| 4 | accepted Representation Conformance |
| 5 | Source Element Inventory |
| 6 | Structural Summary |
| 7 | valid Structural Summary validation |
| 8 | Structural Statistics |
| 9 | valid Structural Statistics validation |
| 10 | Sequential Relation Set |
| 11 | valid Sequential Relation Set validation |
| 12 | Structural Equality Relation Set |
| 13 | valid Structural Equality validation |
| 14 | Declared Reference Relation Set |
| 15 | valid Declared Reference validation |
| 16 | accepted Relation Conformance Report |
| 17 | passed Relations Certification Report |
| 18 | Navigation Object |
| 19 | Constructed Navigation Object |
| 20 | accepted Navigation Conformance Report |
| 21 | passed Navigation Certification Report |
| 22 | Orientation Map Object |
| 23 | Constructed Orientation Map |
| 24 | accepted Orientation Map Conformance Report |
| 25 | passed Slice III Certification Report |
| 26 | Expression Contract |
| 27 | valid Expression Contract validation |
| 28 | Expression Artifact |
| 29 | accepted Expression Conformance Report |
| 30 | certified Expression Certification Report |
| 31 | certified Slice IV Certification Report |

Runtime 1.1 supplies no declared cross references. Stage 14 MUST therefore use
`declarations=()`. This is not an inference that no references exist; it is the
bounded capability of the accepted Profile v1 source.

All validation and conformance outputs MUST be successful before the next
stage begins. Failure stops the sequence. No later stage may execute.

## 7. Fixed Expression declarations

Runtime 1.1 MUST pass these exact, canonically ordered tuples to
`create_expression_contract`:

```text
communicative_scope:
  canonical_order
  orientation_map_entries
  orientation_map_identity
  provenance
  structural_adjacency

declared_lossiness:
  human_interpretation
  semantic_meaning
  visual_layout

declared_exclusions:
  actions
  generated_language
  recommendations
  semantic_reasoning
```

They are invocation constants, not caller options.

## 8. Certified terminal artifact

Successful execution ends with exactly one `SliceIVCertificationReport` whose:

- schema is `orion.slice-iv-certification/0.1-alpha`;
- decision is `certified`;
- responsibility is `vertical_slice_iv_certification`;
- STOP is `at_slice_iv_certified`;
- observed Expression Certification identity and integrity match stage 30;
- provenance reference equals the SHA-256 reference to the canonical stage 30
  artifact.

The terminal artifact is necessary but not sufficient for publication. The
complete Artifact Manifest Contract MUST also pass Gateway boundary checks.

No stage after `at_slice_iv_certified` exists in Version 1.1.

## 9. Immutability and failure

The Adapter SHALL snapshot canonical input bytes before execution and verify
that the corresponding input bytes are unchanged after execution.

It MUST NOT:

- edit an input or output;
- repair an invalid artifact;
- skip a validation or certification stage;
- synthesize a successful result;
- substitute proof fixtures for caller input;
- call LYRA, SIRIUS, the historical Runtime, or the historical Gateway;
- return a partial chain as success.

On failure, artifacts created in the isolated worker are discarded as one
unit. They are not published individually.

## 10. Replay requirements

For one accepted canonical invocation envelope:

1. execute the complete sequence twice in fresh isolated workers;
2. serialize every required artifact with its frozen canonical serializer;
3. compare corresponding bytes;
4. compare the ordered manifest bytes;
5. compare the terminal certification bytes.

Replay passes only if every comparison is byte-identical and both executions
stop at `at_slice_iv_certified`.

Operational execution IDs, timestamps, log records, worker IDs, host IDs, and
HTTP headers are excluded from Core replay and MUST NOT enter any Core input.

## 11. Gate condition

This contract is frozen as a specification. Gate 0 remains responsible for
proving that the listed entry points can execute the complete sequence against
non-fixture accepted Confirmed Material without changing the frozen Core.

If that proof fails, implementation SHALL NOT proceed.
