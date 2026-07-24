# Markdown Structural Projection Specification v1

- Status: canonical Projection specification
- Projection identifier: `orion.projection/markdown-structure`
- Projection version: `1.0.0`
- Qualified Projection identity:
  `orion.projection/markdown-structure@1.0.0`
- Source grammar: CommonMark `0.31.2`
- Source media type: `text/markdown;charset=utf-8`
- Accepted source boundary: `whole`
- Target profile:
  `orion.representation/markdown-structure@1.0.0`
- Target domain: `orion.representation.markdown-block-structure`
- Governing profile:
  [`Markdown Structural Representation Profile v1`](MARKDOWN_STRUCTURAL_REPRESENTATION_PROFILE_V1.md)
- Implementation status: not implemented
- Public contract impact: none
- Runtime impact: none
- Gateway impact: none
- UNDERSTAND impact: none

## 1. Purpose and scope

This document defines the deterministic mapping from one accepted
CommonMark `0.31.2` whole-document source into the structural declaration
required by the frozen Markdown Structural Representation Profile v1.

The Projection is the normative mapping rule. It defines:

- which CommonMark block constructs become declared elements;
- when each declared element exists;
- which required structural properties survive;
- how source locators are derived;
- how containers affect traversal;
- how canonical order and ordinals are assigned;
- which mapped values enter deterministic element identity;
- which structural distinctions are preserved;
- which information is intentionally omitted;
- when no valid mapping can exist;
- the complete structural decision set handed to the Renderer.

The Projection does not execute these rules.

It does not:

- select or resolve a source;
- parse source bytes at Runtime;
- invoke a parser;
- create a Representation;
- generate element identities;
- calculate Representation integrity;
- serialize output;
- perform external conformance;
- execute UNDERSTAND;
- infer meaning.

A conforming Markdown Structural Renderer executes this Projection exactly. It
adds no source-domain, element, property, locator, ordering, containment,
identity-basis, preservation or lossiness decision.

## 2. Normative language and authority

The terms **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**,
**SHOULD**, **SHOULD NOT** and **MAY** are normative.

This specification is subordinate to the frozen Markdown Structural
Representation Profile v1. It specializes that profile without changing it.

The following frozen values are authoritative:

| Property | Normative value |
|---|---|
| Source grammar | CommonMark `0.31.2` |
| Source media type | `text/markdown;charset=utf-8` |
| Source boundary | `whole` |
| Target profile | `orion.representation/markdown-structure@1.0.0` |
| Target domain | `orion.representation.markdown-block-structure` |
| Structural depth | block structure only |

If this specification and the governing profile appear to conflict, the
governing profile prevails and the Projection cannot conform until the
conflict is resolved through governance.

No implementation-specific parse behavior, Markdown extension or alternate
grammar may supplement the mapping.

## 3. Projection input

The Projection applies only to one source that already satisfies the complete
accepted source domain of the governing profile.

The mapping context contains exactly:

- qualified Projection identity;
- qualified target-profile identity;
- Orientation Object identity and version;
- source identity and source revision;
- exact source integrity reference;
- accepted boundary identifier `whole`;
- exact accepted UTF-8 source bytes;
- source grammar identity CommonMark `0.31.2`;
- target domain;
- the declared lossiness fixed by the target profile.

These values are inputs to the mapping. The Projection does not create, repair
or reinterpret them.

The source bytes remain authoritative. Any intermediate parse form is only a
means of applying the mapping and has no independent identity or authority.

## 4. General mapping rule

The Projection maps the CommonMark `0.31.2` block structure into one closed,
ordered declaration.

For every supported CommonMark block node:

1. determine the corresponding Version 1 element kind from Section 5;
2. retain only the profile-required structural properties;
3. bind the element to source boundary `whole`;
4. derive the canonical locator from Section 7;
5. place the element in the canonical traversal from Section 8;
6. assign its contiguous canonical ordinal;
7. expose the values required by the identity basis in Section 9.

The mapping is one-to-one:

- every supported CommonMark block node produces exactly one declared element;
- every declared non-document element corresponds to exactly one supported
  CommonMark block node;
- the CommonMark document root produces exactly one `document` element;
- no omitted inline or non-element construct produces a declaration;
- no declaration is merged with another declaration;
- no supported block node is split into multiple declarations.

The mapping MUST NOT depend on the textual content, apparent subject, semantic
importance or Human intention expressed inside a block.

## 5. Element mapping rules

The element vocabulary is closed. Only the mappings in this section are valid.

### 5.1 `document`

#### Source construct

The single CommonMark document root for the accepted whole-document source.

#### Existence

- Exactly one `document` element always exists.
- It exists for both empty and non-empty accepted sources.

#### Non-existence

The `document` element never has a valid absence. If one document root cannot
be established, no valid mapping exists.

#### Required structural properties

No profile-specific property is added.

The element:

- references boundary `whole`;
- uses the document locator from Section 7.2;
- is first;
- has ordinal `0`.

### 5.2 `block_quote`

#### Source construct

One block quote container recognized under CommonMark `0.31.2`, including its
continuation lines and any lazily continued block content assigned to that
container by the grammar.

#### Existence

One `block_quote` element exists for each CommonMark block quote container
node.

Nested block quotes produce distinct elements.

#### Non-existence

No `block_quote` exists merely because:

- a `>` character appears inside code, inline code or ordinary text;
- an escaped `>` is present;
- source content discusses or quotes a block-quote marker;
- a line is not assigned to a block quote container by CommonMark.

#### Required structural properties

No profile-specific property is added.

Block quote marker count, marker spacing and nesting depth are not emitted as
properties.

### 5.3 `ordered_list`

#### Source construct

One ordered list container recognized under CommonMark `0.31.2`.

The CommonMark rules determine:

- where the list begins and ends;
- which adjacent items belong to the same list;
- whether a change of delimiter separates lists;
- which nested list belongs to which containing block.

#### Existence

One `ordered_list` element exists for each CommonMark ordered list container
node.

#### Non-existence

No `ordered_list` exists when numeral-like text is not recognized as an
ordered list marker by CommonMark.

Separate CommonMark list containers MUST NOT be merged because they appear
visually adjacent or use the same marker style.

#### Required structural properties

No profile-specific property is added.

Starting number, delimiter character, marker width and list tightness are not
emitted.

### 5.4 `unordered_list`

#### Source construct

One bullet list container recognized under CommonMark `0.31.2`.

The CommonMark rules determine:

- where the list begins and ends;
- which adjacent items belong to the same list;
- whether a change of bullet marker separates lists;
- which nested list belongs to which containing block.

#### Existence

One `unordered_list` element exists for each CommonMark bullet list container
node.

#### Non-existence

No `unordered_list` exists when bullet-like text is parsed as:

- a thematic break;
- ordinary paragraph content;
- code;
- another CommonMark construct.

Separate CommonMark list containers MUST NOT be merged.

#### Required structural properties

No profile-specific property is added.

Bullet marker character, marker width and list tightness are not emitted.

### 5.5 `list_item`

#### Source construct

One list item node belonging to a CommonMark ordered or bullet list container.

#### Existence

One `list_item` element exists for each CommonMark list item node, including an
empty item when CommonMark recognizes one.

Nested list items produce distinct elements in their respective list
containers.

#### Non-existence

No `list_item` exists for:

- a marker-like sequence not recognized as a list item;
- a paragraph contained by an item;
- a continuation line without its own CommonMark list-item node;
- a task marker interpreted only as ordinary inline content.

#### Required structural properties

No profile-specific property is added.

The item marker, ordinal number, checkbox-like content and indentation width
are not emitted as properties.

### 5.6 `atx_heading`

#### Source construct

One ATX heading recognized under CommonMark `0.31.2`.

#### Existence

One `atx_heading` element exists for each CommonMark ATX heading node.

#### Non-existence

No `atx_heading` exists when a hash sequence is parsed as:

- paragraph content;
- code;
- an escaped character sequence;
- another CommonMark construct.

#### Required structural properties

The required property is:

- `level`: the integer number of opening ATX marker characters recognized by
  CommonMark, from `1` through `6`.

Optional closing markers, marker spacing and inline heading content are not
emitted.

### 5.7 `setext_heading`

#### Source construct

One Setext heading recognized under CommonMark `0.31.2`.

#### Existence

One `setext_heading` element exists for each CommonMark Setext heading node.

#### Non-existence

No `setext_heading` exists when an underline-like line is parsed as:

- a thematic break;
- paragraph content;
- code;
- another CommonMark construct.

#### Required structural properties

The required property is:

- `level = 1` when CommonMark recognizes the `=` underline form;
- `level = 2` when CommonMark recognizes the `-` underline form.

Underline length, indentation and inline heading content are not emitted.

### 5.8 `paragraph`

#### Source construct

One paragraph block remaining after application of the CommonMark `0.31.2`
block rules, including CommonMark treatment of link reference definitions.

#### Existence

One `paragraph` element exists for each CommonMark paragraph node that remains
in the block structure.

#### Non-existence

No `paragraph` exists for:

- a source region entirely consumed as one or more link reference definitions;
- a blank line;
- content assigned to another leaf block;
- inline content as a separate unit;
- an empty placeholder invented for a container.

When link reference definition lines precede content that remains a paragraph,
only the physical lines belonging to the remaining paragraph determine the
paragraph locator.

#### Required structural properties

No profile-specific property is added.

Text, inline structure, reference resolution and visible rendering are not
emitted.

### 5.9 `thematic_break`

#### Source construct

One thematic break recognized under CommonMark `0.31.2` after application of
the grammar's precedence rules.

#### Existence

One `thematic_break` element exists for each CommonMark thematic break node.

#### Non-existence

No `thematic_break` exists when the same or similar marker sequence is parsed
as:

- a Setext heading underline;
- a list marker;
- paragraph content;
- code;
- another CommonMark construct.

#### Required structural properties

No profile-specific property is added.

Marker character, marker count and intervening whitespace are not emitted.

### 5.10 `fenced_code_block`

#### Source construct

One fenced code block recognized under CommonMark `0.31.2`.

An unclosed code fence extending to end of document remains a valid fenced code
block when CommonMark recognizes it as such.

#### Existence

One `fenced_code_block` element exists for each CommonMark fenced code block
node.

#### Non-existence

No `fenced_code_block` exists when a fence-like sequence is parsed as:

- inline code;
- paragraph content;
- an indented code block;
- another CommonMark construct.

#### Required structural properties

No profile-specific property is added.

Fence character, fence length, indentation, closing-fence presence, info
string and code content are not emitted.

### 5.11 `indented_code_block`

#### Source construct

One indented code block recognized under CommonMark `0.31.2`.

#### Existence

One `indented_code_block` element exists for each CommonMark indented code
block node.

#### Non-existence

No `indented_code_block` exists when indentation belongs to:

- continuation content in a list item or block quote;
- a paragraph;
- a fenced code block;
- another CommonMark construct.

#### Required structural properties

No profile-specific property is added.

Indentation width, blank-line detail and code content are not emitted.

## 6. Container rules

### 6.1 Container set

The Projection recognizes these CommonMark block containers:

- document root → `document`;
- block quote container → `block_quote`;
- ordered list container → `ordered_list`;
- bullet list container → `unordered_list`;
- list item container → `list_item`.

Container status is used only to:

- determine which CommonMark block nodes exist;
- determine each node's source extent;
- perform canonical depth-first pre-order traversal.

### 6.2 No emitted semantic hierarchy

The Projection MUST NOT emit:

- parent-element identity;
- child-element identity;
- depth;
- path;
- ancestry;
- descendant count;
- containment edge;
- semantic section;
- inferred relationship.

Every declared element references the same accepted parent source boundary:
`whole`.

The CommonMark container tree governs mapping order but does not become an
independent Representation relationship model.

### 6.3 Nested containers

Nested containers remain separate mapped elements.

For any container:

1. map the container itself;
2. visit its direct CommonMark block children in source order;
3. for a child container, map that child and then visit its descendants;
4. return to the next sibling only after completing the child subtree.

Equal or overlapping locators are permitted. They do not authorize a consumer
to reconstruct or assert hierarchy beyond the profile.

### 6.4 Empty containers

When CommonMark recognizes an empty block quote or empty list item, the
container element exists even if it has no emitted descendant leaf block.

The Projection MUST NOT invent a paragraph or placeholder child.

### 6.5 List containment

An ordered or unordered list element precedes all of its mapped list items in
canonical traversal.

Each list item precedes all mapped block descendants assigned to that item.

The Projection does not emit:

- a reference from item to list;
- a reference from nested list to item;
- an ordered-list item number;
- a task-state interpretation.

## 7. Locator derivation

### 7.1 Physical-line table

Locators are derived from the exact accepted UTF-8 source bytes.

Before mapping block extents, the source boundary defines one deterministic
physical-line table:

1. byte offset `0` begins line `1`;
2. every accepted `0A` byte terminates the current line;
3. the byte after a non-terminal `0A` begins the next line;
4. a terminal `0A` remains part of its line and creates no additional line;
5. an empty source has one conventional zero-width line numbered `1`.

Each physical line has:

- one one-based line number;
- one zero-based inclusive start byte;
- one zero-based exclusive end byte;
- an end byte that includes its terminating `0A` when present.

No code-point, character, UTF-16 or display-column coordinate participates.

### 7.2 Document locator

The `document` locator is always:

- `start_byte = 0`;
- `end_byte = exact source byte length`;
- `start_line = 1`;
- `end_line = final physical line number`, or `1` for the empty source.

### 7.3 General non-document locator

For every supported non-document CommonMark block node:

1. identify the first physical line assigned to that node by the pinned block
   grammar;
2. identify the last physical line assigned to that node by the pinned block
   grammar;
3. set `start_line` to the first assigned line number;
4. set `end_line` to the last assigned line number;
5. set `start_byte` to the first assigned line's start byte;
6. set `end_byte` to the last assigned line's end byte.

The locator therefore spans complete physical lines.

It includes:

- container markers on those lines;
- indentation on those lines;
- block delimiters on those lines;
- internal blank lines assigned to the node;
- terminating line feeds belonging to covered lines.

It excludes:

- physical lines before the node begins;
- physical lines after the node ends;
- trailing separator lines not assigned to the node by CommonMark.

### 7.4 Element-specific block extents

The following rules make the first and last assigned lines explicit:

| Element kind | First assigned line | Last assigned line |
|---|---|---|
| `block_quote` | line on which the CommonMark block quote container begins | final line, including a lazy continuation line, assigned to that same container |
| `ordered_list` | line on which the first item of that CommonMark ordered list begins | final line assigned to the final item in that same list container |
| `unordered_list` | line on which the first item of that CommonMark bullet list begins | final line assigned to the final item in that same list container |
| `list_item` | line containing the item's recognized CommonMark list marker | final line assigned to that same item |
| `atx_heading` | line containing the recognized ATX heading | the same line |
| `setext_heading` | first paragraph-content line promoted into the Setext heading | recognized Setext underline line |
| `paragraph` | first line belonging to the remaining CommonMark paragraph | final line belonging to that paragraph |
| `thematic_break` | line containing the recognized thematic break | the same line |
| `fenced_code_block` | line containing the recognized opening fence | recognized closing-fence line, or final source line when no closing fence exists |
| `indented_code_block` | first line assigned to the indented code block | final line assigned to that code block |

Blank lines internal to a list, item, block quote or code block are included
only when CommonMark assigns them within that node's extent.

Link reference definition lines that produce no declared block element do not
independently receive locators. A reference-definition-only line MUST NOT
extend a remaining paragraph locator.

### 7.5 Nested block locators

For nested blocks, each locator is derived independently from the physical
lines assigned to its own CommonMark node.

Because locators cover whole physical lines:

- a container and descendant may have identical locators;
- siblings may have distinct or adjacent locators;
- ancestor and descendant ranges may overlap;
- overlap does not add a parent-child field.

### 7.6 Locator rejection

No valid mapping exists if:

- a supported block node has no determinable first or last physical line;
- a non-document locator is zero-width;
- byte and line coordinates disagree;
- a locator falls outside the `document` locator;
- the locator cannot be reproduced from identical source bytes and grammar;
- an implementation would need a source-position convention contrary to this
  section.

## 8. Canonical ordering

### 8.1 Traversal algorithm

The Projection defines this normative traversal:

1. begin at the single CommonMark document root;
2. emit `document`;
3. visit each direct block child in CommonMark source order;
4. emit the mapped element for the child;
5. if the child is a supported container, recursively visit its direct block
   children in source order;
6. complete the child's subtree before visiting its next sibling;
7. ignore omitted inline and non-element constructs for emission and ordinal
   purposes;
8. stop with failure upon an unsupported HTML block or unmappable block node.

This is depth-first pre-order traversal of the supported CommonMark block tree.

### 8.2 Ordinals

Ordinal assignment follows emission order:

- `document` receives ordinal `0`;
- each subsequent emitted element receives the next integer;
- ordinals are contiguous;
- no omitted construct reserves an ordinal;
- no post-processing reorder is permitted.

### 8.3 Normative purpose

Ordering is normative because it:

- makes identical source produce identical declarations;
- disambiguates elements with equal kinds and equal line ranges;
- supplies one identity input;
- permits external replay and conformance;
- preserves source sequence without assigning semantic priority.

The declaration MUST NOT be reordered by kind, locator size, heading level,
identity, presentation preference, importance or relevance.

## 9. Deterministic identity inputs

The Projection does not generate or encode element identities.

For every mapped element it supplies these Projection-derived identity inputs:

1. element kind;
2. required profile properties in canonical property-name order;
3. canonical locator:
   - `start_byte`;
   - `end_byte`;
   - `start_line`;
   - `end_line`;
4. canonical ordinal;
5. accepted parent source-boundary reference `whole`.

The complete identity basis additionally binds the frozen context supplied to
the Projection:

1. qualified target-profile identity;
2. Orientation Object identity and version;
3. source identity and source revision.

The Renderer MUST use exactly this combined basis when generating a
deterministic element identity.

No hashing algorithm, string encoding or serialization is defined here.
Whatever identity encoding is used, equality remains equality of the complete
canonical basis.

No parser node identifier, container path, semantic label, source excerpt,
execution detail or hidden value may enter identity.

## 10. Preservation

The Projection MUST preserve unchanged:

- Orientation Object identity and version;
- source identity and source revision;
- source integrity reference;
- source boundary `whole`;
- CommonMark grammar identity and version;
- Projection identity and version;
- target-profile identity and version;
- target domain;
- the distinction between every element kind in Section 5;
- ATX heading level;
- Setext heading level;
- the existence of every supported CommonMark block node;
- source order through canonical traversal;
- exact physical-line traceability through canonical locators;
- canonical ordinal assignment;
- the deterministic identity inputs;
- target-profile declared lossiness.

The Projection MUST preserve syntactic distinctions even when their visible
rendering could appear similar.

In particular:

- ATX and Setext headings remain different element kinds;
- ordered and unordered lists remain different element kinds;
- fenced and indented code blocks remain different element kinds;
- nested containers remain distinct mapped elements;
- thematic breaks are not converted into separators of another kind.

Preservation does not transfer source, semantic, Evidence, editorial or Human
authority to the Projection.

## 11. Declared lossiness

The Projection adopts exactly the declared lossiness of the frozen target
profile.

It intentionally omits from the mapped declaration:

- raw source bytes and excerpts;
- parent-element identifiers and hierarchy edges;
- inline elements and inline values;
- blank-line elements;
- link reference definition elements;
- source spelling and delimiter details not preserved by the target profile;
- list numbering, marker and tightness details;
- code fence and info-string details;
- non-structural whitespace distinctions;
- parser metadata;
- rendering and editor state;
- all semantic, conceptual, evidential and inferential information.

The complete normative lossiness list remains Section 10 of the governing
profile. This specification does not narrow, extend or reinterpret that list.

An omitted value MUST NOT be restored through inference, parser convenience or
Renderer-specific metadata.

An unsupported construct is not declared lossiness when the profile requires
deterministic failure.

## 12. Deterministic failure

Because Projection defines rules but performs no execution, this section
defines conditions under which application of the Projection has no valid
result.

Application MUST fail without a partial structural mapping when:

### 12.1 Input and profile failure

- the source does not satisfy the governing profile's accepted source domain;
- the source boundary is not `whole`;
- source identity, revision or integrity is absent or inconsistent;
- the CommonMark grammar is not exactly `0.31.2`;
- an alternate Markdown extension mode is active;
- Projection identity or version is unknown;
- target-profile identity or version is unknown or mismatched.

### 12.2 Grammar and vocabulary failure

- the source cannot be mapped according to CommonMark `0.31.2`;
- the CommonMark block structure contains an HTML block;
- a CommonMark block node cannot map one-to-one to Section 5;
- mapping would require an element kind outside the frozen vocabulary;
- a supported block node would be omitted;
- a declaration would lack a corresponding supported block node;
- an ATX heading level is outside `1` through `6`;
- a Setext heading level is outside `1` or `2`.

### 12.3 Locator and ordering failure

- a first or last assigned physical line cannot be established;
- a locator cannot satisfy Section 7;
- byte and line coordinates do not agree;
- traversal cannot satisfy Section 8;
- ordinals are not contiguous;
- repeated mapping of identical input would change order, locator, kind or
  property values.

### 12.4 Preservation and authority failure

- a required distinction from Section 10 would be lost or altered;
- target-profile lossiness cannot be declared exactly;
- mapping would require source repair or normalization;
- mapping would require semantic interpretation;
- mapping would require retrieval or external state;
- any partial declaration would otherwise be returned.

The Projection MUST NOT define recovery, fallback or best-effort output.

## 13. Output contract to the Renderer

The Projection hands the Renderer one complete deterministic structural mapping
decision set for the accepted source.

The decision set contains:

### 13.1 Bound context

- Projection identifier and version;
- target-profile identifier and version;
- target domain;
- CommonMark grammar identity and version;
- Orientation Object identity and version;
- source identity and source revision;
- exact source integrity reference;
- accepted source-boundary reference `whole`;
- target-profile declared lossiness.

### 13.2 Ordered mapped elements

For each mapped element, in canonical order:

- element kind;
- `level` only for `atx_heading` or `setext_heading`;
- parent source-boundary reference `whole`;
- canonical locator:
  - `start_byte`;
  - `end_byte`;
  - `start_line`;
  - `end_line`;
- canonical ordinal;
- the complete Projection-derived identity inputs from Section 9.

No source excerpt, parser node, hierarchy edge, inline value, semantic label or
Evidence property is handed to the Renderer as a structural decision.

### 13.3 Renderer responsibility

The Renderer:

- executes this Projection for the exact accepted input;
- generates element identities from the prescribed basis;
- places the ordered declaration inside the immutable Representation envelope;
- records its own explicit identity, version and provenance;
- binds Representation identity, version and integrity;
- emits no Representation when the Projection has no valid result.

The Renderer MUST NOT:

- choose another mapping;
- add or remove an element;
- change a kind or heading level;
- alter a locator or ordinal;
- add containment;
- add structural metadata excluded by the profile;
- reinterpret lossiness;
- repair source;
- apply semantic judgment.

The Renderer is the deterministic executor of the Projection, not a second
source of structural rules.

## 14. Projection invariants

1. Projection defines mapping and performs no execution.
2. The accepted grammar is exactly CommonMark `0.31.2`.
3. The accepted source boundary is exactly `whole`.
4. The mapping vocabulary is closed.
5. Every supported block node maps exactly once.
6. Every non-document declaration originates from one supported block node.
7. Exactly one `document` element always exists.
8. Container structure governs traversal but is not emitted as semantic
   hierarchy.
9. Every element references the same parent source boundary.
10. Locators cover complete physical source lines.
11. Ordering is depth-first pre-order.
12. Ordinals are contiguous and begin with `document` at `0`.
13. Only heading level survives as an element-specific property.
14. Element identity uses only the frozen canonical basis.
15. Preservation is exact and profile-bounded.
16. Lossiness is exactly the lossiness of the target profile.
17. Unsupported or indeterminate mapping fails.
18. Partial mapping is forbidden.
19. Renderer execution adds no structural decision.
20. Projection establishes syntax, never meaning.

## 15. Acceptance criteria

This specification is complete when two independent conforming implementations
given the same accepted CommonMark source and the same frozen context derive
identical:

- supported element count;
- element kinds;
- heading levels;
- parent source-boundary references;
- byte locators;
- line locators;
- depth-first pre-order;
- contiguous ordinals;
- identity bases;
- preservation result;
- declared lossiness;
- deterministic failure result.

An independent reviewer MUST be able to determine, without a new architectural
decision:

- whether each CommonMark block produces an element;
- which element kind it produces;
- which structural property it retains;
- which physical lines its locator covers;
- where it appears in the declaration;
- which values form its identity basis;
- when mapping must stop.

The defined execution boundary is:

```text
Accepted Human-confirmed CommonMark source
        ↓
Markdown Structural Projection Specification v1
        ↓
Complete deterministic structural mapping
        ↓
Markdown Structural Renderer
        ↓
Immutable Markdown Structural Representation
```

This specification stops at the mapping contract. It defines no parser
internals, serialization, Runtime behavior, Gateway behavior, UNDERSTAND
execution, Evidence, Orientation, report, continuation or language output.
