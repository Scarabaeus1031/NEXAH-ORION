# Markdown Structural Representation Profile v1

- Status: canonical profile specification
- Profile identifier: `orion.representation/markdown-structure`
- Profile version: `1.0.0`
- Qualified profile identity:
  `orion.representation/markdown-structure@1.0.0`
- Source grammar: CommonMark `0.31.2`
- Source media type: `text/markdown;charset=utf-8`
- Target domain: `orion.representation.markdown-block-structure`
- Architecture:
  [`ORION Structural Representation Architecture`](STRUCTURAL_REPRESENTATION_ARCHITECTURE.md)
- Implementation status: not implemented
- Public contract impact: none
- Runtime impact: none
- Gateway impact: none
- UNDERSTAND impact: none

## 1. Purpose

This document defines the first concrete profile governed by the frozen
Structural Representation Architecture.

It specifies one deterministic mapping from one exact, accepted Markdown source
boundary into one immutable ordered declaration of block-level source
structure.

The profile defines:

- the accepted Markdown source domain;
- the source grammar and grammar version;
- the complete Version 1 element vocabulary;
- the canonical source-locator model;
- deterministic element identity;
- canonical ordering;
- preservation and declared lossiness;
- deterministic rejection conditions;
- external conformance requirements;
- the guarantees available to UNDERSTAND.

This document defines a profile. It does not define an implementation, parser
library, Renderer API, schema, transport or Runtime behavior.

## 2. Normative language

The terms **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**,
**SHOULD**, **SHOULD NOT** and **MAY** are normative.

Where this profile references CommonMark `0.31.2`, the normative grammar is the
published specification at:

`https://spec.commonmark.org/0.31.2/`

No other CommonMark release, Markdown dialect or implementation-specific parse
behavior is interchangeable with that pinned grammar.

## 3. Profile identity

### 3.1 Immutable identity

The profile has the following immutable identity:

| Property | Normative value |
|---|---|
| Name | Markdown Structural Representation Profile v1 |
| Profile identifier | `orion.representation/markdown-structure` |
| Profile version | `1.0.0` |
| Qualified identity | `orion.representation/markdown-structure@1.0.0` |
| Source grammar | CommonMark `0.31.2` |
| Source media type | `text/markdown;charset=utf-8` |
| Target domain | `orion.representation.markdown-block-structure` |
| Source boundary | one whole, immutable Markdown document |
| Structural depth | block structure only |

The profile identifier, profile version, source grammar version, target domain,
element vocabulary, locator model, identity basis, ordering rules,
preservation rules and declared lossiness jointly define this profile.

Changing any of those properties creates a different profile version. An
implementation MUST NOT continue to use this qualified identity after making
such a change.

### 3.2 Compatibility policy

Conformance requires exact support for the qualified profile identity.

- A consumer supporting `1.0.0` MUST accept only artifacts that declare
  `1.0.0`.
- Unknown profile versions MUST fail deterministically.
- A profile version MUST NOT be inferred from its identifier, payload or
  element vocabulary.
- No implementation-specific extension may be emitted under this profile
  identity.
- A clarification that changes no normative behavior may correct the prose of
  this document without changing the profile identity.
- Any change to observable structural output, ordering, locators, identity,
  preservation, lossiness or failure behavior requires a new profile version.

## 4. Accepted source domain

An input belongs to this profile only when every requirement in this section is
satisfied.

### 4.1 Source authority and boundary

The input MUST already be:

- an immutable, Human-confirmed Orientation Object version;
- associated with one explicit source identity;
- associated with one explicit source revision;
- integrity-bound to the exact source bytes;
- bounded as the whole document.

The accepted boundary identifier is `whole`.

Partial documents, byte selections, line selections, concatenated documents,
transclusions and synthesized multi-source documents are not accepted.

The profile does not resolve, retrieve, select, repair or authorize the source.
Those actions, if any, occur before the Representation Boundary.

### 4.2 Encoding

The source MUST be a byte sequence that:

- decodes strictly as UTF-8;
- contains no UTF-8 byte-order mark;
- contains no null code point `U+0000`;
- contains no isolated surrogate value;
- requires no replacement character introduced by decoding.

Decoding with replacement, guessing an encoding or transcoding from another
encoding is forbidden.

Other Unicode scalar values accepted by CommonMark `0.31.2` remain accepted.
Unicode normalization MUST NOT be applied.

### 4.3 Newlines

The only accepted line ending is line feed `U+000A`, represented by the single
byte `0A`.

- Carriage return `U+000D` is not accepted.
- CRLF input is not accepted.
- Mixed line-ending input is not accepted.
- No newline normalization occurs inside this profile.
- A terminal line feed is optional.
- The presence or absence of a terminal line feed is part of source integrity.

An external producer MAY normalize line endings before Human confirmation.
Once confirmed, normalization would create different source bytes and therefore
a different source revision.

### 4.4 Markdown grammar

The source MUST be interpreted exclusively according to CommonMark `0.31.2`.

This profile does not enable:

- GitHub Flavored Markdown;
- tables;
- task-list semantics;
- strikethrough;
- footnotes;
- definition lists;
- mathematical extensions;
- directives;
- custom containers;
- wiki links;
- implementation-specific Markdown extensions.

Text that resembles an extension but remains valid CommonMark is processed
solely according to its CommonMark interpretation. No extension intent is
inferred.

### 4.5 Front matter

YAML, TOML, JSON and other front-matter conventions have no special status.

Delimiter-like text at the beginning of a document is interpreted as ordinary
CommonMark source. It MUST NOT be declared as `front_matter`, metadata or a
hidden document property.

### 4.6 Raw HTML

CommonMark raw HTML blocks are excluded from the accepted Version 1 source
domain.

If the CommonMark `0.31.2` parse contains an HTML block, processing MUST fail
deterministically with an unsupported-source-domain outcome. It MUST NOT:

- remove the HTML;
- reinterpret it as text;
- sanitize it;
- render it;
- emit a partial Structural Representation.

Raw HTML appearing only inside block content is not independently inspected by
this block-only profile unless CommonMark classifies it as an HTML block.
Inline structure is outside the Version 1 declaration as specified in
Section 5.

### 4.7 Empty documents

An empty byte sequence is accepted.

Its declaration contains exactly one element:

- the `document` root;
- ordinal `0`;
- the zero-width document locator defined in Section 6.

An empty document contains no inferred paragraph, blank-line element or
placeholder.

### 4.8 Source-domain rejection

Processing MUST stop without producing a Representation when:

- the immutable source identity, revision, integrity or whole-document boundary
  is absent;
- strict UTF-8 decoding fails;
- a byte-order mark is present;
- `U+0000` is present;
- `U+000D` is present;
- another Markdown grammar or extension mode is requested;
- a CommonMark HTML block is present;
- the exact grammar version cannot be established;
- the source boundary is not `whole`.

No source-domain failure may be converted into a successful but lossy
Representation.

## 5. Version 1 element vocabulary

Version 1 declares block-level structure only. The vocabulary in this section
is complete and closed.

### 5.1 Declared element kinds

| Element kind | CommonMark construct | Required profile property |
|---|---|---|
| `document` | document root | none |
| `block_quote` | block quote | none |
| `ordered_list` | ordered list container | none |
| `unordered_list` | bullet list container | none |
| `list_item` | list item | none |
| `atx_heading` | ATX heading | `level`, integer `1` through `6` |
| `setext_heading` | Setext heading | `level`, integer `1` or `2` |
| `paragraph` | paragraph | none |
| `thematic_break` | thematic break | none |
| `fenced_code_block` | fenced code block | none |
| `indented_code_block` | indented code block | none |

Every declared element MUST contain the architectural fields required by the
Structural Representation Architecture:

- stable element identity;
- element kind;
- accepted parent source-boundary reference;
- canonical source locator;
- declared ordinal.

Only `atx_heading` and `setext_heading` add a profile-required structural
property. No other element-specific property is emitted by Version 1.

### 5.2 Containers and descendants

The following are container elements:

- `document`;
- `block_quote`;
- `ordered_list`;
- `unordered_list`;
- `list_item`.

All other Version 1 kinds are leaf block elements.

Nested block elements are declared independently. A child remains traceable to
the same accepted source boundary as its ancestor. Version 1 does not emit a
parent-element identifier or a separate hierarchy edge.

Containment is reflected only by:

- canonical depth-first ordering;
- source locators;
- element kinds;
- the CommonMark parse from which the declaration was produced.

Consumers MUST NOT treat overlapping locators as an independently declared
relationship.

### 5.3 CommonMark constructs not emitted as elements

The following CommonMark constructs do not become Version 1 declared elements:

- blank lines;
- link reference definitions;
- text;
- code spans;
- emphasis;
- strong emphasis;
- links;
- images;
- autolinks;
- hard line breaks;
- soft line breaks;
- entity and numeric character references;
- backslash escapes;
- inline raw HTML.

Their omission is declared lossiness. Their source bytes remain covered by
source integrity and may lie inside a declared block locator.

No omitted construct may be silently promoted to a new element kind.

### 5.4 Unsupported element kinds

The following element kinds MUST NOT appear:

- `table`;
- `table_row`;
- `table_cell`;
- `task`;
- `task_item`;
- `strikethrough`;
- `footnote`;
- `definition_list`;
- `math`;
- `directive`;
- `front_matter`;
- `html_block`;
- any custom or implementation-specific kind;
- any inline element kind.

An output containing an element kind outside Section 5.1 is non-conforming.

## 6. Canonical source-locator model

### 6.1 Locator coordinates

Every element uses one canonical locator containing:

- `start_byte`: zero-based inclusive UTF-8 byte offset;
- `end_byte`: zero-based exclusive UTF-8 byte offset;
- `start_line`: one-based inclusive physical source line;
- `end_line`: one-based inclusive physical source line.

Byte offsets always refer to the exact accepted source bytes before any parse
operation. They never refer to Unicode code points, UTF-16 code units, rendered
text, decoded entities or normalized text.

Line numbers are derived from the exact accepted LF bytes:

- line `1` begins at byte offset `0`;
- every `0A` terminates the current physical line;
- the byte after a non-terminal `0A` begins the next physical line;
- a terminal `0A` does not create an additional physical line;
- the empty source has one conventional zero-width document line numbered `1`.

Column positions are not part of this profile.

### 6.2 Document locator

The `document` element locator is:

- `start_byte = 0`;
- `end_byte = source byte length`;
- `start_line = 1`;
- `end_line = the final physical source line`, or `1` for an empty source.

### 6.3 Block-element locator

A non-document block locator covers the complete physical source lines on which
the CommonMark block exists.

Its byte range:

- begins at the first byte of its first physical line;
- ends immediately after the terminating `0A` of its final physical line when
  that line has a line ending;
- otherwise ends at end of source.

Consequences:

- block markers and indentation on covered lines are included;
- line endings inside the block range are included;
- container and descendant locators may be equal;
- nested block locators may overlap;
- bytes preceding or following the block on another physical line are excluded;
- a locator never points outside the accepted whole-document boundary.

CommonMark block start and end lines are determined by the pinned grammar.
No implementation-specific source-span convention may replace this rule.

### 6.4 Locator validity

For every element:

- `0 <= start_byte <= end_byte <= source byte length`;
- `start_line <= end_line`;
- the byte and line coordinates MUST describe the same physical-line interval;
- all non-document elements MUST have a non-zero byte range;
- all non-document locators MUST be contained by the `document` locator;
- the declared locator MUST reproduce identically from identical accepted
  source bytes.

A locator is a trace-back coordinate. It is not an excerpt and does not copy
source authority into the Representation.

## 7. Deterministic element identity

### 7.1 Identity basis

Every element identity is determined exclusively by this canonical identity
basis:

1. qualified profile identity;
2. Orientation Object identity and version;
3. source identity and source revision;
4. accepted boundary identifier `whole`;
5. element kind;
6. required profile properties, in canonical property-name order;
7. canonical locator;
8. canonical ordinal.

No other input may affect identity.

In particular, identity MUST NOT depend on:

- memory location;
- parser-internal node identity;
- filesystem path unless that path is already the authoritative source
  identity;
- execution time;
- locale;
- operating system;
- provider;
- Runtime state;
- traversal implementation;
- semantic content classification;
- rendered HTML;
- a random value.

### 7.2 Identity equality

Within this profile, two declared element identities are equal if and only if
their complete canonical identity bases are equal.

Every element identity MUST:

- be unique within one Structural Representation;
- be reproducible by an independent conforming implementation;
- be covered by Representation integrity;
- remain unchanged across repeated executions with identical inputs.

The concrete serialization envelope may encode the identity without changing
its canonical basis. Encoding must not add identity authority.

### 7.3 Stability after edits

Element identity is stable only for the exact source identity and source
revision from which it was declared.

After any source-byte edit:

- source integrity changes;
- source revision changes;
- no element identity is required to survive;
- apparent textual or structural similarity does not establish identity
  continuity.

Cross-revision element matching is not part of this profile.

### 7.4 Stability within one Representation version

Within one accepted Representation version:

- ordinals are immutable;
- locators are immutable;
- element kinds and required properties are immutable;
- element identities are immutable;
- reordering or replacing any declaration produces a different Representation
  integrity value and version.

## 8. Canonical ordering

### 8.1 Traversal

Elements are ordered by depth-first pre-order traversal of the CommonMark
`0.31.2` block parse.

The rules are:

1. `document` is first and has ordinal `0`.
2. A container is emitted before any of its descendants.
3. Children of a container are visited in source order.
4. Each child subtree is completed before the next sibling is visited.
5. Only element kinds in Section 5.1 are emitted.
6. Omitted inline constructs do not receive ordinals.
7. Ordinals are contiguous integers from `0` through
   `declared element count - 1`.

### 8.2 Block ordering

Block ordering follows the block structure produced by CommonMark `0.31.2`.
It is never sorted by:

- element kind;
- heading level;
- locator length;
- identity;
- visual importance;
- semantic relevance.

### 8.3 Nested structures

For nested lists, block quotes and list items, canonical depth-first pre-order
is authoritative even when multiple elements share the same line interval.

The ordinal disambiguates elements that otherwise share kind-compatible
coordinates. The ordinal does not claim semantic priority.

### 8.4 Inline ordering

Version 1 emits no inline elements. Therefore it defines no inline-element
ordinal sequence.

Inline parsing performed as part of CommonMark conformance MUST NOT alter the
Version 1 block declaration, except where CommonMark itself determines the
validity or extent of a block construct.

## 9. Preservation

A conforming Representation MUST preserve:

- Orientation Object identity and version;
- source identity and source revision;
- exact source integrity reference;
- whole-document source-boundary identity;
- qualified profile identity;
- CommonMark grammar identity and version;
- Structural Projection identity and version;
- Structural Renderer identity and version;
- Representation identity, version and integrity;
- complete Projection and Renderer provenance;
- every Version 1 block element recognized by the pinned grammar;
- each declared element kind;
- heading level for declared headings;
- canonical block order;
- canonical ordinals;
- canonical source locators;
- deterministic element identities;
- the declared lossiness of Section 10.

The Representation MUST preserve traceability to the exact source. It is not
required to embed or reproduce the source bytes.

## 10. Declared lossiness

This profile intentionally does not preserve the following as Structural
Representation fields:

- raw Markdown source bytes or excerpts;
- parent-element identifiers and explicit hierarchy edges;
- inline element declarations;
- blank-line declarations;
- link reference definition declarations;
- link destinations and titles;
- image destinations and titles;
- visible inline text values;
- code-span values;
- fenced-code info strings;
- fenced-code fence character or fence length;
- ordered-list starting numbers;
- list delimiter characters;
- bullet marker characters;
- list tightness;
- optional closing ATX heading markers;
- original delimiter choice for emphasis or strong emphasis;
- backslash escape form;
- entity-reference form and decoded value;
- non-structural whitespace distinctions;
- comments;
- front-matter interpretation;
- extension-specific structure;
- parser-specific metadata;
- rendering hints;
- editor state;
- selections, cursor position or annotations;
- HTML output;
- semantic relationships;
- concepts, entities, claims, Evidence roles, importance, relevance or
  confidence.

This lossiness is fixed for profile `1.0.0`. An implementation MUST NOT preserve
an omitted property as a profile-defined authoritative field.

Source integrity and locators allow a permitted external reviewer to inspect
the authoritative source. That traceability does not make omitted information
part of the structural declaration.

## 11. Malformed and unsupported input

### 11.1 CommonMark validity

CommonMark defines every accepted character sequence as a document. Therefore
constructs such as unmatched delimiters, unclosed emphasis and an unclosed
fenced code block are not automatically malformed.

They MUST be treated exactly as CommonMark `0.31.2` specifies. A Renderer MUST
NOT repair author intent.

### 11.2 Deterministic failures

Processing MUST fail before a Representation is accepted when:

- any source-domain rule in Section 4 fails;
- CommonMark `0.31.2` behavior cannot be reproduced;
- the parse contains an excluded HTML block;
- the emitted element vocabulary is not closed under Section 5.1;
- a required heading level is unavailable or invalid;
- a canonical locator cannot be established;
- canonical ordering cannot be established;
- an element identity cannot be reproduced from the identity basis;
- provenance or integrity is incomplete;
- any partial declaration would otherwise be emitted.

### 11.3 No silent repair

The Projection and Renderer MUST NOT:

- rewrite invalid UTF-8;
- remove a BOM;
- normalize newlines;
- normalize Unicode;
- add a terminal newline;
- reinterpret another Markdown dialect;
- promote extension syntax;
- repair list indentation;
- close delimiters;
- balance fences;
- remove unsupported HTML;
- omit a failing element and continue.

Failure produces no conforming Structural Representation.

## 12. External conformance

Conformance validation is external to the Structural Renderer.

Before a Representation is accepted, an external validator MUST verify all of
the following.

### 12.1 Identity and version

- profile identifier and version exactly match Section 3;
- source grammar is exactly CommonMark `0.31.2`;
- target domain exactly matches Section 3;
- Orientation Object identity and version are present and unchanged;
- source identity, revision and integrity reference are present and unchanged;
- Projection and Renderer identities and versions are explicit;
- Representation identity, version and integrity are internally consistent.

### 12.2 Source domain

- source bytes satisfy Section 4;
- the boundary is exactly `whole`;
- source integrity matches the exact bytes;
- no excluded HTML block exists;
- no normalization or repair was applied.

### 12.3 Structural declaration

- exactly one `document` element exists;
- the document has ordinal `0`;
- an empty document contains no other element;
- every kind belongs to Section 5.1;
- heading properties satisfy Section 5.1;
- no omitted or unsupported kind is present;
- every recognized Version 1 block is declared exactly once;
- no undeclared block is invented;
- ordinals are contiguous and canonical;
- declaration order follows Section 8.

### 12.4 Locators

- every locator satisfies Section 6;
- document bounds equal the whole source boundary;
- byte and line coordinates agree;
- every non-document locator lies inside the document;
- every locator resolves to the physical lines occupied by the declared
  CommonMark block;
- repeated validation produces identical locators.

### 12.5 Element identity

- every element identity is unique within the Representation;
- every identity uses only the basis in Section 7;
- equal bases yield equal identities;
- unequal bases do not share an identity within the Representation;
- repeated validation reproduces every identity.

### 12.6 Provenance, lossiness and integrity

- provenance traces the exact source through the named Projection and Renderer;
- no provenance step claims semantic, Evidence, Library, Human or UNDERSTAND
  authority;
- declared lossiness exactly matches Section 10;
- the complete ordered declaration is covered by Representation integrity;
- replay from identical accepted inputs produces a byte-identical canonical
  Representation serialization.

### 12.7 Rejection

The external validator MUST reject:

- an unknown profile or grammar version;
- a partial declaration;
- a declaration with unverifiable source bytes;
- any ordering, locator, identity, provenance, integrity or lossiness mismatch;
- any representation containing semantic, Evidence or inferred structural
  claims outside this profile.

The validator MUST NOT repair a failing Representation.

## 13. UNDERSTAND contract

After successful external conformance, UNDERSTAND may assume:

- the Representation is immutable;
- the qualified profile identity is exact;
- the source grammar is CommonMark `0.31.2`;
- the source boundary is the whole confirmed document;
- source identity, revision and integrity are complete;
- the element vocabulary is closed and profile-valid;
- every element has one stable identity;
- every element has one valid canonical locator;
- every element has one contiguous canonical ordinal;
- ordering is canonical depth-first pre-order;
- heading level is valid when present;
- provenance is complete;
- declared lossiness is explicit and exact;
- repeated execution from identical inputs is byte-identical.

UNDERSTAND may inventory only the declarations that exist.

UNDERSTAND MUST NOT:

- inspect or parse raw Markdown;
- execute the Projection or Renderer;
- create, repair or infer elements;
- infer inline structure from block content;
- reconstruct parent-element hierarchy;
- reinterpret omitted constructs;
- infer source intent from extension-like syntax;
- treat heading level or block kind as semantic importance;
- create Evidence;
- assign confidence;
- infer concepts, entities, claims or relationships;
- supplement lossiness with hidden source analysis.

The profile establishes syntactic block structure only. It does not establish
meaning.

## 14. Out of scope

This profile does not define or authorize:

- semantic interpretation;
- inline Structural Representation;
- AST optimization;
- parent-element hierarchy;
- relationship inference;
- entity recognition;
- concept identification;
- claims;
- Evidence;
- Source Evidence;
- Evidence Binding;
- confidence;
- reasoning;
- summarization;
- classification;
- relevance ranking;
- raw-source retrieval;
- Library resolution;
- search indexing;
- embeddings;
- HTML generation;
- Markdown rendering;
- browser behavior;
- editor behavior;
- syntax highlighting;
- presentation layout;
- Runtime execution;
- Gateway behavior;
- UNDERSTAND execution;
- report generation;
- continuations;
- LYRA;
- LUCY;
- transport;
- persistence.

## 15. Canonical invariants

1. The profile identity is immutable.
2. CommonMark `0.31.2` is the only accepted grammar.
3. The whole confirmed Markdown document is the only accepted boundary.
4. Exact UTF-8 source bytes remain authoritative.
5. No newline or Unicode normalization occurs.
6. Version 1 declares block structure only.
7. The Version 1 element vocabulary is closed.
8. Every declared element traces to canonical source coordinates.
9. Every declared element has a deterministic identity.
10. Declaration order is canonical depth-first pre-order.
11. The complete declaration is immutable and integrity-bound.
12. Lossiness is explicit and fixed.
13. Raw HTML blocks fail deterministically.
14. Extension semantics are never inferred.
15. No malformed or unsupported input is silently repaired.
16. Conformance remains external to the Renderer.
17. Structural authority remains syntactic and source-bound.
18. Structural authority is not semantic, Evidence, editorial or Human
    authority.
19. UNDERSTAND inventories declarations and never creates them.
20. No Version 1 public contract is changed by this profile.

## 16. Acceptance criteria

This profile is complete when an independent reviewer can derive, without a new
system-level architectural decision:

- one Markdown Structural Projection for the exact accepted source domain;
- one deterministic Markdown Structural Renderer;
- one immutable Markdown Structural Representation;
- one external Conformance Validator;
- one reproducible proof for a non-empty document;
- one reproducible proof for an empty document;
- deterministic rejection proofs for every source-domain failure;
- byte-identical repeated output for identical accepted inputs.

The resulting implementation must demonstrate:

```text
Human-confirmed whole Markdown source
        ↓
Markdown Structural Projection
        ↓
Deterministic Markdown Structural Renderer
        ↓
Immutable Markdown Structural Representation
        ↓
External Conformance
        ↓
STOP
```

No Orientation, Evidence, report, continuation, LYRA output or UNDERSTAND
execution is required or authorized by this profile.
