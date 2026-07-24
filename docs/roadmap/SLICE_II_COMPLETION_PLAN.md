# Slice II Completion Plan

- Status: canonical implementation plan
- Target: Slice II — Structure and Summary
- Governing roadmap: `docs/roadmap/ORION_VERTICAL_SLICES.md`
- Architecture status: frozen
- Calendar schedule: none

This plan records the work still required to change Slice II from **Next** to
**Complete**. It does not authorize Slice III work.

Status marks used throughout:

- **Complete** — implemented, tested and replayed successfully in the current
  repository.
- **Partial** — the accepted Alpha subset exists, but the complete Slice II
  responsibility does not.
- **Not started** — no executable Slice II implementation, focused test and
  proof exist.
- **Required** — work that must be completed before Slice II can close.

## 1. Current Status

### Audit basis

The current executable baseline was inspected against:

- `MARKDOWN_STRUCTURAL_REPRESENTATION_PROFILE_V1.md`;
- `MARKDOWN_STRUCTURAL_PROJECTION_SPECIFICATION_V1.md`;
- `ORION_VERTICAL_SLICES.md`;
- the Markdown Structural Renderer Alpha implementation;
- the external Conformance validator;
- UNDERSTAND Source Element Inventory Alpha;
- their focused tests, fixtures and proof scripts.

At the time of this audit, the two focused suites execute **26 tests
successfully** with:

```text
PYTHONPATH=src python3 -m unittest \
  tests.test_markdown_structural_renderer_alpha \
  tests.test_understand_source_element_inventory_alpha
```

The Renderer proof stops at `after_immutable_representation`; the Inventory
proof stops at `after_declared_source_element_inventory`. Both report
byte-identical replay.

These results establish a green Slice I baseline. They do not make Slice II
complete.

### Projection

**Complete**

- The canonical Projection specification covers the entire Profile v1 block
  vocabulary.
- Executable Projection exists for:
  - `document`;
  - `atx_heading`;
  - `paragraph`.
- The executable subset preserves canonical full-line locators, canonical
  ordinals, identity inputs and declared lossiness.
- Unsupported Alpha constructs fail instead of being silently converted.

**Partially complete**

- Projection execution is a deliberately bounded line-oriented Alpha
  implementation, not complete CommonMark `0.31.2` block execution.
- UTF-8, empty-document, ATX-heading and paragraph cases are executable.
- CommonMark container traversal and precedence are specified but not yet
  executable.

**Not started**

- Executable mapping for:
  - `block_quote`;
  - `ordered_list`;
  - `unordered_list`;
  - `list_item`;
  - `thematic_break`;
  - `fenced_code_block`;
  - `indented_code_block`;
  - `setext_heading`.
- A deterministic CommonMark `0.31.2` execution substrate capable of producing
  the specified nested block tree and exact source extents.
- Complete-vocabulary Projection replay.

### Renderer

**Complete**

- Deterministic rendering of the three Alpha element kinds.
- Immutable Representation and nested immutable elements.
- Deterministic element identities and Representation integrity.
- Explicit Projection, Renderer, profile, source and Human-confirmation
  provenance.

**Partially complete**

- The Renderer pipeline and serialization pattern are suitable for Slice II,
  but its accepted element vocabulary is still the Alpha tuple
  `document | atx_heading | paragraph`.

**Not started**

- Rendering of the eight remaining Profile v1 element kinds.
- `setext_heading.level` preservation.
- Complete-vocabulary immutable fixture and proof artifact.
- A reviewed Renderer version change that makes the new executable behavior
  explicit without changing the frozen profile identity.

### Structural Representation

**Complete**

- Immutable Representation envelope.
- Immutable element declarations.
- Source boundary, locator, ordinal, identity, integrity and provenance fields.
- `level` support for the existing `atx_heading` subset.

**Partially complete**

- The existing element shape can represent all no-property block kinds.
- Its validation currently permits only the Alpha element vocabulary.

**Not started**

- Acceptance of every Profile v1 element kind.
- Validation of `setext_heading.level` as integer `1` or `2`.
- Complete-vocabulary invariant tests.
- Complete-vocabulary canonical fixture.

No parent-element relation, semantic hierarchy or content field is required.
The frozen profile deliberately does not declare them.

### External Conformance

**Complete**

- External deterministic replay for the Alpha subset.
- Validation of source traceability, Orientation Object identity, profile and
  Renderer identity, canonical ordinals, element identity, locators,
  provenance, declared lossiness and Representation integrity.
- Tamper rejection for the existing subset.

**Partially complete**

- The validator architecture exists, but replay currently uses the bounded
  Renderer Alpha and therefore cannot validate the complete profile
  vocabulary.

**Not started**

- One-to-one declaration checks for each remaining block kind.
- Full nested depth-first pre-order replay.
- Complete CommonMark precedence and source-extent cases.
- Negative conformance for every unsupported, malformed or out-of-domain case
  required by the frozen profile.
- Complete-vocabulary Conformance proof.

### UNDERSTAND

**Complete**

- UNDERSTAND consumes only an immutable Structural Representation.
- Inventory preserves canonical order, element identities, locators,
  Representation lineage and source lineage.
- It does not read Markdown, execute Projection or Renderer, create structure
  or perform semantic processing.
- Inventory output is immutable and byte-identical on replay.

**Partially complete**

- Inventory behavior is structurally generic for no-property elements, but its
  heading validation recognizes only `atx_heading`.
- The only accepted input fixture contains the three Alpha kinds.

**Not started**

- Explicit acceptance and preservation of all remaining Profile v1 block
  kinds.
- `setext_heading.level` validation and preservation.
- Structural Summary.
- Structural Statistics.
- Focused negative boundary tests for Summary and Statistics.

### Proofs

**Complete**

- Bounded Renderer Alpha proof.
- Bounded Source Element Inventory Alpha proof.
- Byte-identical replay for both proofs.

**Not started**

- One bounded proof for each remaining block capability.
- One complete-vocabulary Representation and Inventory proof.
- Structural Summary proof.
- Structural Statistics proof.
- One end-to-end Slice II proof stopping after Structural Statistics.

### Tests

**Complete**

- 26 focused Slice I tests are green.
- Existing tests cover the Alpha subset's mapping, locators, identity,
  immutability, determinism, source-domain failures, external Conformance,
  UNDERSTAND isolation and proof replay.

**Not started**

- Positive, boundary, nesting, precedence, negative, tamper, replay and
  regression coverage for the eight remaining block kinds.
- Official CommonMark `0.31.2` example coverage for every applicable rule.
- Structural Summary and Structural Statistics tests.
- Complete Slice II proof replay.

### Documentation

**Complete**

- Frozen profile and Projection specifications.
- Slice I milestone documentation.
- Canonical vertical-slice roadmap.
- Capability roadmap.

**Partially complete**

- Existing implementation prose describes the bounded Alpha, not completed
  Slice II.

**Not started**

- Implementation decision record for the chosen deterministic CommonMark
  execution substrate and version pin.
- Per-capability implementation notes and proof commands.
- Summary and Statistics implementation notes.
- Final Slice II verification record and status transition.

## 2. Remaining Capability Matrix

The frozen Profile v1 vocabulary contains eleven element kinds. Three are
complete in the current executable subset; eight remain.

| Block kind | Current status | Projection work | Renderer work | Representation support | External Conformance | UNDERSTAND support | Required tests | Required proof | Acceptance condition |
|---|---|---|---|---|---|---|---|---|---|
| `document` | Complete | Preserve current root and empty-document mapping | Preserve current root emission | Already accepted | Preserve root, whole-boundary and empty-document replay | Already inventories root first | Retain all current tests | Replay in every later proof | No regression; ordinal remains `0` |
| `atx_heading` | Complete | Preserve CommonMark ATX rule and level | Preserve level and identity | Already accepted with level `1..6` | Preserve locator, level and identity replay | Already preserves level | Retain boundary and UTF-8 tests | Replay in complete-vocabulary proof | No regression or identity drift for unchanged input |
| `paragraph` | Complete | Preserve remaining-paragraph and reference-definition behavior | Preserve paragraph declaration | Already accepted | Preserve extent and one-to-one replay | Already inventories paragraph | Retain multiline and rejection tests | Replay in complete-vocabulary proof | No unsupported block is coerced into a paragraph |
| `block_quote` | Not started | Execute CommonMark block quote containers, lazy continuation and recursive child traversal | Emit container in depth-first pre-order with exact extent | Add kind to accepted vocabulary | Replay one-to-one node, locator, ordinal and identity; reject marker-like non-quotes | Accept and preserve kind, identity, locator and ordinal | Single, multiline, lazy continuation, nested quote, quote containing supported blocks, marker-like paragraph, UTF-8, tamper and replay | One source containing quote and nested supported children, ending at immutable Inventory | Every recognized quote is declared exactly once; no hierarchy relation is invented |
| `ordered_list` | Not started | Execute ordered-list recognition, delimiter and indentation precedence as part of the atomic list family | Emit ordered-list container in canonical traversal | Add kind; no list metadata fields | Replay container extent, canonical order and identity | Accept and preserve container declaration | Start-number forms, `.` and `)`, indentation, interruption, nesting, false positives, UTF-8, tamper and replay | Atomic list-family proof containing an ordered list and its items | Every recognized ordered-list container and item are declared exactly once |
| `unordered_list` | Not started | Execute bullet-list recognition and precedence as part of the atomic list family | Emit unordered-list container in canonical traversal | Add kind; no marker field | Replay container extent, order and identity | Accept and preserve container declaration | `-`, `+`, `*`, interruption, indentation, nesting, thematic-break ambiguity, false positives, tamper and replay | Atomic list-family proof containing an unordered list and its items | Every recognized unordered-list container and item are declared exactly once |
| `list_item` | Not started | Execute list-item nodes, continuation, blank-item and nested-child traversal as part of the atomic list family | Emit each item immediately after its containing list position under depth-first pre-order | Add kind; no parent field | Replay item extent, ordinal and identity without asserting a hierarchy field | Accept and preserve item declaration | Empty/permitted item, multiline item, nested list, mixed list, lazy continuation, indentation, tamper and replay | Same atomic list-family proof | All items are emitted in canonical traversal; no parent relation is added |
| `thematic_break` | Not started | Execute CommonMark thematic-break precedence, including list and Setext ambiguities | Emit one leaf declaration with exact line locator | Add kind | Replay precedence, locator, ordinal and identity | Accept and preserve leaf | `*`, `-`, `_`, spaces, indentation, list ambiguity, Setext ambiguity, false positives, tamper and replay | One bounded thematic-break proof | Every recognized break maps once; no heading or list is misclassified |
| `fenced_code_block` | Not started | Execute backtick/tilde fences, indentation, matching close and valid open-to-EOF behavior | Emit one declaration covering opening through closing line or EOF | Add kind; do not add fence info or content | Replay exact extent and declared lossiness | Accept and preserve declaration only | Backtick, tilde, longer closer, info string, embedded fence, unclosed fence, indentation, invalid opener, UTF-8, tamper and replay | One bounded fenced-code proof including a valid unclosed fence case | Fence block is declared once; code content and fence metadata remain absent |
| `indented_code_block` | Not started | Execute four-column indentation, continuations, blank lines and interruption rules | Emit one declaration with exact complete extent | Add kind | Replay extent, ordering and identity | Accept and preserve declaration | Spaces, tabs as CommonMark columns, continuation, blank lines, paragraph interaction, list interaction, false positives, tamper and replay | One bounded indented-code proof | Every recognized indented block maps once with no content field |
| `setext_heading` | Not started | Execute Setext promotion and precedence against thematic breaks and paragraphs | Emit heading with level `1` or `2` and full content-to-underline extent | Add kind and level validation `1..2` | Replay type, level, locator, ordinal and identity | Accept and preserve type and level | `=` and `-`, multiline content, indentation, thematic-break ambiguity, reference definitions, false positives, UTF-8, tamper and replay | One bounded Setext proof plus precedence replay with thematic break | Correct type and level are stable and no paragraph duplicate remains |

### Atomic list-family rule

`ordered_list`, `unordered_list` and `list_item` are three declared element
kinds but one grammatically indivisible green implementation package.
CommonMark has no valid list container without a list item. Therefore:

- internal checkpoints may activate the three mappings sequentially;
- none of the three is declared complete independently;
- the work package becomes green only when both list container kinds and
  `list_item` pass Projection, Renderer, Representation, Conformance,
  UNDERSTAND, tests and the shared proof.

This is implementation sequencing, not a new architectural relation. The
Representation continues to omit parent-element hierarchy.

## 3. Structural Summary

Structural Summary is **not started**.

It must be implemented as one immutable internal UNDERSTAND diagnostic derived
only from the accepted immutable Source Element Inventory.

### Required fields

The Summary must contain:

- diagnostic identity and version;
- operator identity and version;
- input Inventory integrity or deterministic input reference;
- Orientation Object identity and version;
- Representation identity, version and integrity;
- source identity, revision, integrity and boundary;
- total declared element count;
- ordered sequence of declared element kinds;
- declared heading levels, associated only with their exact element identities
  or ordinals;
- first canonical ordinal;
- final canonical ordinal;
- source-boundary identifier;
- declared block-kind coverage:
  - kinds declared in this Inventory;
  - kinds absent from this Inventory;
  - complete frozen Profile v1 vocabulary used as the comparison basis;
- responsibility state;
- explicit `STOP` value after Structural Summary.

### Required implementation tasks

1. Define the immutable internal Summary diagnostic without creating a public
   contract.
2. Accept only the immutable Inventory diagnostic.
3. Validate Inventory lineage and canonical order before derivation.
4. Copy identity and lineage fields without modification.
5. Derive every Summary value only from Inventory fields and frozen profile
   constants.
6. Serialize with the existing canonical JSON rules.
7. Reject invalid Inventory rather than repair it.
8. Keep the module outside Runtime, Gateway and the public import surface.

### Required proofs

- A focused proof consumes one immutable complete-vocabulary Inventory.
- A second execution over the same Inventory produces byte-identical Summary
  bytes.
- Every Summary field is independently recomputed from the Inventory by the
  test.
- The proof records that raw Markdown, Projection, Renderer, Runtime and
  Gateway were not accessed.
- The proof stops at `after_structural_summary`.

### Determinism and immutability

- Equal Inventory bytes must yield equal Summary bytes.
- Summary identity, if present, must use only the immutable input reference,
  diagnostic version and responsibility identity.
- All sequences must preserve canonical Inventory order.
- The diagnostic and every nested value must be immutable.
- No locale, clock, random value, environment value or unordered iteration may
  affect output.

### Traceability

Every Summary must resolve exactly to:

- one Source Element Inventory;
- one immutable Structural Representation;
- one source identity and revision;
- one Orientation Object identity and version.

### Explicit exclusions

The Summary must not contain:

- raw source or excerpts;
- subject, topic or content summaries;
- inferred sections;
- inferred hierarchy or containment;
- importance or ranking;
- relations;
- entities, concepts, claims or Evidence;
- uncertainty estimates;
- navigation;
- LYRA text.

### Summary acceptance

Structural Summary is complete only when its focused suite, negative boundary
suite, deterministic replay and proof all pass against a complete-vocabulary
Inventory while every earlier proof remains byte-identical.

## 4. Structural Statistics

Structural Statistics is **not started**.

It must be one immutable internal UNDERSTAND diagnostic derived only from the
accepted Inventory. It must not parse Markdown or consume the Representation
directly.

### Required statistics

| Statistic | Source field | Deterministic derivation rule | Proof requirement | Acceptance criteria | Non-goal |
|---|---|---|---|---|---|
| Total ordered elements | `ordered_element_count` and `elements` | Require equality; emit the exact count | Recompute from tuple length | Count equals both sources | No estimate of document complexity |
| Count by element kind | `elements[].element_kind` | Count exact profile kinds; emit in frozen Profile v1 vocabulary order | Independently recount every kind | Sum equals total elements | No ranking or importance |
| Heading-level distribution | heading `element_kind` and `level` | Count ATX levels `1..6` and Setext levels `1..2` separately; retain zero counts deterministically | Recompute from exact heading entries | Every heading contributes once | No inferred outline |
| Declared container-kind count | `elements[].element_kind` | Count entries whose kind is in the profile-declared container set: `document`, `block_quote`, `ordered_list`, `unordered_list`, `list_item` | Compare with explicit frozen set | Exact integer equals independent replay | No containment relation |
| Declared leaf-kind count | `elements[].element_kind` | Count all Profile v1 kinds outside the declared container set | Compare with exact complement set | Container plus leaf counts equal total | No semantic leaf concept |
| Byte span per element | `locator.start_byte`, `locator.end_byte` | `end_byte - start_byte` | Recompute for every element identity | Non-negative and exact | No payload extraction |
| Physical-line span per element | locator byte width and line endpoints | `0` for a zero-width locator; otherwise `end_line - start_line + 1` | Recompute for every element identity | Exact non-negative integer | No logical-line interpretation |
| First canonical ordinal | `elements[0].ordinal` | Require and emit `0` | Replay from Inventory | Exactly `0` | No first-important element |
| Final canonical ordinal | `elements[-1].ordinal` | Emit `ordered_element_count - 1` after validation | Replay from count and final entry | Exact equality | No endpoint meaning |
| Document byte boundary | document locator | Emit document `start_byte`, `end_byte` and width | Recompute from root | Root begins at `0`; width is exact | No source content |
| Declared non-document byte coverage | non-document locator intervals and document locator | Compute the union length of half-open byte intervals clipped only by prior validation; emit covered bytes, total document bytes and uncovered bytes | Independent interval-union replay, including overlap | Covered plus uncovered equals total; overlapping containers are not double-counted | No relation from overlap; no percentage required |
| Declared non-document line coverage | non-document locator line intervals and document locator | Compute the union of inclusive physical-line intervals; empty document yields zero covered and zero available physical lines | Independent interval-union replay | Counts are exact and bounded by document lines | No logical sections |
| Declared block-kind coverage | element kinds and frozen vocabulary | Emit present-kind count and absent-kind count | Recompute from exact set membership | Present plus absent equals eleven kinds | No source completeness claim |
| Nesting-depth availability | no current Inventory source field | Emit `unavailable` because Profile v1 declares no parent-element hierarchy or depth | Prove no alternate field is consulted | Always unavailable for this profile | Never infer from locator overlap, order, kind or reparsing |

### Required implementation tasks

1. Define one immutable internal Statistics diagnostic.
2. Accept exactly one immutable Inventory.
3. Validate the Inventory before calculating any statistic.
4. Implement each derivation as an exact pure function over declared fields.
5. Use integers and explicit availability states; do not introduce
   floating-point coverage.
6. Preserve all input identity and lineage references.
7. Canonically serialize all mappings in fixed profile order.
8. Reject unknown kinds, invalid levels, invalid locators and broken ordinals.
9. Keep Statistics outside Runtime, Gateway and the public import surface.

### Required proof

The proof must include:

- all eleven Profile v1 block kinds across one accepted complete-vocabulary
  Inventory;
- overlapping container and descendant locators to prove interval union does
  not double-count;
- blank physical lines to prove uncovered boundary reporting;
- UTF-8 content represented only through byte locators;
- an empty-document replay;
- independently recomputed expected values;
- byte-identical repeated output;
- explicit `nesting_depth = unavailable`;
- `STOP` at `after_structural_statistics`.

### Statistics acceptance

Structural Statistics is complete only when:

- every listed statistic exists;
- every value is independently reproducible from Inventory fields alone;
- all results are immutable and byte-identical on replay;
- coverage never treats locator overlap as hierarchy;
- unavailable nesting depth remains explicit;
- no raw source, semantic or relation field is present;
- the focused proof and all regressions pass.

## 5. Test Matrix

Legend:

- **✓** — exists and passes for the current capability.
- **△** — a shared Slice I mechanism exists, but capability-specific coverage
  remains required.
- **□** — required and not present.
- **—** — not applicable to the bounded capability.

| Capability | Unit | Integration | Negative | Immutability | Determinism | Conformance | Proof replay | Regression |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `document` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `atx_heading` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `paragraph` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| CommonMark `0.31.2` execution substrate | □ | □ | □ | — | □ | □ | □ | ✓ |
| `block_quote` | □ | □ | □ | △ | □ | □ | □ | ✓ |
| ordered-list family | □ | □ | □ | △ | □ | □ | □ | ✓ |
| unordered-list family | □ | □ | □ | △ | □ | □ | □ | ✓ |
| `list_item` within list family | □ | □ | □ | △ | □ | □ | □ | ✓ |
| `thematic_break` | □ | □ | □ | △ | □ | □ | □ | ✓ |
| `fenced_code_block` | □ | □ | □ | △ | □ | □ | □ | ✓ |
| `indented_code_block` | □ | □ | □ | △ | □ | □ | □ | ✓ |
| `setext_heading` | □ | □ | □ | △ | □ | □ | □ | ✓ |
| Complete-vocabulary Representation | □ | □ | □ | □ | □ | □ | □ | ✓ |
| Complete-vocabulary Inventory | □ | □ | □ | □ | □ | □ | □ | ✓ |
| Structural Summary | □ | □ | □ | □ | □ | □ | □ | ✓ |
| Structural Statistics | □ | □ | □ | □ | □ | □ | □ | ✓ |
| Full Slice II vertical proof | — | □ | □ | □ | □ | □ | □ | ✓ |

### Required test classes

Every remaining block capability must add:

- valid single-element cases;
- valid multi-element cases;
- applicable nested-container cases;
- grammar-precedence cases;
- exact physical-line and UTF-8 byte locators;
- canonical depth-first pre-order and contiguous ordinals;
- deterministic element identity;
- immutable output;
- byte-identical replay;
- tamper rejection;
- false-positive and unsupported-input rejection;
- external Conformance replay;
- UNDERSTAND identity, locator and order preservation;
- proof script replay;
- all prior capability regressions.

The complete suite must additionally enforce by static and runtime checks that
UNDERSTAND Summary and Statistics cannot:

- access files or raw Markdown;
- import or execute Projection or Renderer;
- import Runtime, Gateway or public outcome contracts;
- create relations or semantic fields.

## 6. Proof Matrix

| Proof | Purpose | Input | Expected immutable artifacts | Expected STOP | Success condition |
|---|---|---|---|---|---|
| Slice I baseline replay | Freeze the starting point | Existing confirmed Alpha source and immutable fixture | Existing Representation and Inventory | Existing two Slice I STOP values | Current bytes and all 26 tests remain unchanged |
| Block quote proof | Prove first container mapping | Confirmed Markdown with quote, lazy continuation and supported descendants | Representation; Conformance result; Inventory | `after_declared_source_element_inventory` | Quote and descendants map once in canonical order |
| List-family proof | Prove both list containers and items atomically | Confirmed Markdown with ordered, unordered, nested and multiline items | Representation; Conformance result; Inventory | `after_declared_source_element_inventory` | Both container kinds and every item are exact and reproducible |
| Thematic-break proof | Prove precedence-sensitive leaf mapping | Confirmed Markdown covering recognized break and ambiguity boundaries | Representation; Conformance result; Inventory | `after_declared_source_element_inventory` | Break is neither list nor Setext heading in the accepted case |
| Fenced-code proof | Prove fenced extent mapping | Confirmed Markdown with closed and valid unclosed fences | Representation; Conformance result; Inventory | `after_declared_source_element_inventory` | Exact opening-to-close/EOF locators; no content emitted |
| Indented-code proof | Prove indentation mapping | Confirmed Markdown with continuation, blank and interruption cases | Representation; Conformance result; Inventory | `after_declared_source_element_inventory` | Exact block extents and no paragraph coercion |
| Setext-heading proof | Prove heading promotion and level | Confirmed Markdown with both levels and thematic-break boundary | Representation; Conformance result; Inventory | `after_declared_source_element_inventory` | Level and extent are exact; no duplicate paragraph |
| Empty-document complete-profile proof | Preserve the profile's empty boundary | Empty confirmed Markdown | Root-only Representation; Conformance; root-only Inventory | `after_declared_source_element_inventory` | Zero-width root remains the sole declaration |
| Complete-vocabulary proof | Prove all Profile v1 kinds together | One confirmed CommonMark document containing every kind | Complete Representation; Conformance result; complete Inventory | `after_declared_source_element_inventory` | Eleven kinds are accepted; order, identity, locators and lineage replay |
| Structural Summary proof | Prove bounded structural synopsis | Complete immutable Inventory | Immutable Summary | `after_structural_summary` | Every field recomputes from Inventory; bytes repeat |
| Structural Statistics proof | Prove bounded measurements | Complete immutable Inventory plus empty Inventory case | Immutable Statistics | `after_structural_statistics` | Every statistic recomputes exactly; depth is unavailable |
| Full Slice II proof | Prove the complete vertical slice | Human-confirmed complete-vocabulary Markdown | Projection mapping; Representation; Conformance; Inventory; Summary; Statistics | `after_structural_statistics` | All artifacts are immutable, traceable, byte-identical and downstream work is absent |
| Negative boundary proof | Prove what Slice II does not do | Tampered artifacts and prohibited/unsupported source cases | Deterministic rejection diagnostic only | Failure before invalid artifact, or Slice II STOP for valid source | No repair, partial acceptance, relation, semantic field or downstream execution |

Every proof must:

- expose exact input and artifact identities;
- expose source, Projection, Renderer and Representation versions;
- expose integrity and provenance;
- execute twice and compare canonical bytes;
- record the expected STOP;
- fail non-zero when any required check is false;
- be callable from a clean checkout using documented commands.

## 7. Definition of Done

Slice II transitions from **Next** to **Complete** only when every statement
below is true:

- [ ] Every Profile v1 block kind is executable:
  `document`, `block_quote`, `ordered_list`, `unordered_list`, `list_item`,
  `atx_heading`, `setext_heading`, `paragraph`, `thematic_break`,
  `fenced_code_block`, `indented_code_block`.
- [ ] Identical accepted CommonMark `0.31.2` source produces byte-identical
  Projection output.
- [ ] Every recognized supported block node is declared exactly once.
- [ ] Canonical depth-first pre-order and contiguous ordinals are externally
  replayed.
- [ ] Canonical byte and line locators pass all positive, boundary, nesting and
  precedence cases.
- [ ] Deterministic element identities and Representation integrity replay
  exactly.
- [ ] Immutable Structural Representation accepts the complete vocabulary and
  no other vocabulary.
- [ ] `setext_heading.level` is preserved and validated as `1` or `2`.
- [ ] External Conformance validates every supported kind and rejects every
  invalid, tampered, unsupported or out-of-domain artifact.
- [ ] UNDERSTAND inventories every supported kind without source access,
  Projection execution, Renderer execution or structural discovery.
- [ ] Complete-vocabulary Inventory preserves identity, locator, ordinal,
  source and Representation lineage.
- [ ] Structural Summary contains every required field and only permitted
  structural information.
- [ ] Structural Summary is immutable and byte-identical on replay.
- [ ] Structural Statistics contains every required statistic and only
  permitted derivations.
- [ ] Structural Statistics is immutable and byte-identical on replay.
- [ ] Nesting depth is explicitly unavailable for Profile v1.
- [ ] No relation is inferred from locator overlap, traversal order or element
  kind.
- [ ] Every capability-specific proof succeeds.
- [ ] Complete-vocabulary proof succeeds.
- [ ] Summary and Statistics proofs succeed.
- [ ] Full Slice II proof succeeds and stops after Structural Statistics.
- [ ] Negative boundary proof succeeds.
- [ ] All Slice I proof artifacts and tests remain green.
- [ ] The full repository verification suite is green.
- [ ] Implementation documentation records exact commands, versions,
  limitations and STOP boundaries.
- [ ] No Runtime, Gateway, public API or architecture file changed.
- [ ] The canonical roadmap status is updated only after all preceding checks
  are demonstrably true.

Failure of any one item leaves Slice II at **Next** or **In progress**. There is
no partial-completion waiver.

## 8. Explicit Non-Goals

Slice II must not implement:

- structural relations;
- inferred relations;
- declared-relation processing;
- navigation primitives;
- Orientation Map;
- entity recognition;
- concept detection;
- claim detection;
- Evidence or Evidence Binding;
- reasoning;
- semantic interpretation;
- content summarization;
- source excerpts;
- semantic hierarchy;
- parent or child relations;
- hierarchy reconstruction from locator overlap;
- LYRA;
- SIRIUS;
- LUCY;
- NTO;
- additional Operators or Modes;
- Runtime changes or execution;
- Gateway changes or invocation;
- public contract changes;
- transport;
- persistence;
- Library participation;
- browser workflow;
- public application or nexahedron.com implementation.

Slice II describes and measures declared structure. It does not orient,
interpret, navigate or communicate that structure.

## 9. Recommended Execution Order

Each work package must finish with:

```text
Capability
        ↓
Implementation
        ↓
Tests
        ↓
Proof
        ↓
Documentation
        ↓
Green
```

No later package begins while the active package is red.

### WP0 — Freeze the executable baseline

**Bounded capability:** reproducible Slice I baseline.

- Record the two focused test and proof commands.
- Capture hashes of the accepted Alpha fixtures and proof outputs.
- Verify the 26 focused tests and both existing proof replays.
- Add no behavior.

**Green condition:** an independent clean checkout reproduces the accepted
Slice I bytes and STOP boundaries.

### WP1 — Deterministic CommonMark execution substrate

**Bounded capability:** execute the frozen CommonMark `0.31.2` block grammar
without changing Projection meaning.

- Select and pin a conforming execution implementation, or complete the local
  implementation.
- Keep parser internals private to Projection execution.
- Prove exact block-node kind, source extent and child traversal against the
  applicable CommonMark `0.31.2` examples.
- Ensure parser metadata never crosses into Representation.
- Preserve current Alpha output for unchanged Alpha inputs.

**Green condition:** grammar execution is deterministic, pinned, externally
tested and introduces no new Representation field or architectural decision.

### WP2 — `block_quote`

**Bounded capability:** first Profile v1 container.

- Implement Projection, Renderer, Representation acceptance, Conformance and
  UNDERSTAND support.
- Add the full focused test class.
- Add and replay the block quote proof.
- Document exact supported rule boundaries.

**Green condition:** all quote tests and proof pass with every prior test green.

### WP3 — Atomic list family

**Bounded capability:** ordered lists, unordered lists and list items.

- Implement all three declared kinds as one grammar-complete package.
- Cover canonical recursive traversal without emitting parent relations.
- Add list-family Conformance, Inventory, tests and proof.

**Green condition:** both list container kinds and all items are green
together; no incomplete list mapping is accepted.

### WP4 — `thematic_break`

**Bounded capability:** precedence-sensitive thematic break.

- Implement the complete rule.
- Add list and Setext ambiguity tests.
- Add Conformance and proof replay.

**Green condition:** every accepted break and rejection boundary is
deterministic and all prior packages remain green.

### WP5 — `fenced_code_block`

**Bounded capability:** closed and valid open-to-EOF fenced blocks.

- Implement exact extent mapping without emitting content or fence metadata.
- Add closed, nested-marker, info-string and unclosed cases.
- Complete Conformance, Inventory and proof.

**Green condition:** the focused proof and all negative cases pass.

### WP6 — `indented_code_block`

**Bounded capability:** CommonMark indented code blocks.

- Implement column-sensitive recognition and extent.
- Test spaces, tabs, blank lines, interruption and list interactions.
- Complete Conformance, Inventory and proof.

**Green condition:** no paragraph/list coercion occurs and replay is exact.

### WP7 — `setext_heading`

**Bounded capability:** Setext heading type, level and extent.

- Implement both levels.
- Extend Representation and Inventory level validation.
- Complete precedence tests, Conformance and proof.

**Green condition:** both levels and every ambiguity boundary pass with no
duplicate paragraph declaration.

### WP8 — Complete-vocabulary Representation and Inventory

**Bounded capability:** all Profile v1 kinds in one immutable path.

- Create the complete canonical fixture.
- Run full ordering, locator, identity, provenance and integrity validation.
- Run the empty-document and complete-vocabulary proofs.
- Confirm all per-capability fixtures remain valid.

**Green condition:** one source containing the full vocabulary reaches an
immutable complete Inventory with byte-identical replay.

### WP9 — Structural Summary

**Bounded capability:** deterministic structural synopsis.

- Implement only the fields in Section 3.
- Add isolation, immutability, traceability and deterministic replay tests.
- Add the focused Summary proof and documentation.

**Green condition:** every output field independently recomputes from Inventory
and the proof stops after Summary.

### WP10 — Structural Statistics

**Bounded capability:** deterministic structural measurements.

- Implement only the statistics in Section 4.
- Add exact derivation, interval-union, empty-document, unavailable-depth and
  negative tests.
- Add the focused Statistics proof and documentation.

**Green condition:** every statistic independently recomputes from Inventory
and the proof stops after Statistics.

### WP11 — Slice II closure

**Bounded capability:** complete Slice II vertical proof.

- Execute the full Test Matrix.
- Execute every capability and negative proof.
- Execute the complete vertical proof twice and compare every artifact.
- Run full repository verification and architecture-boundary checks.
- Produce the final verification record.
- Update status to **Complete** only after every Definition-of-Done item passes.

**Green condition:** the complete path reproducibly stops after Structural
Statistics; every earlier milestone remains green; Slice III code does not
exist.

## 10. Canonical Closing Statement

> A vertical slice is complete only when every declared capability is
> implemented, externally verified, reproducible, fully tested and stopped at
> its defined boundary.
