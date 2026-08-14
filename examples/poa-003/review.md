# POA-003 Human Review

- Review status: **PASS**
- Review structure: **A–B–C relational inspection**
- Representation A: committed POA-001 static SVG
- Representation B: committed POA-003 Markdown table
- C: Human Review
- Source-code reading required: **no**
- Domain-validity claim: **none**
- Recommendation, approval, or decision: **none**

## A — Static SVG

The SVG makes the two Records spatially distinct and connects them with an
arrow labeled with the signed difference. Evidence is placed with each Record.
Uncertainty, the limitation, prohibited implications, Processor identity, and
the exact Result digest remain visible.

The spatial placement and arrow are presentation choices. They are not
additional facts in the Result. JSON types, full nesting, status, Expression
lineage, and the Processor source digest are not directly visible; the exact
Result digest provides the trace back to those fields.

## B — Markdown table

The Markdown Representation exposes every frozen leaf path as a JSON literal.
This makes strings, numbers, complete lineage, uncertainty, evidence, and
prohibited implications explicit.

The table flattens JSON nesting. It does not reproduce the SVG's spatial
relation, panels, emphasis, or arrow. It declares those losses and states that
the immutable Result remains the semantic source.

## C — Relational review

C does not merge A and B into a new Result. It compares both Representations
with their common immutable source.

### Did A and B read the same Result?

Yes. Both bind Result `result-001` with SHA-256
`6d565b327ed812f7b4e3b2239298e07715bdf3ac077d759d48263ce1279bb6b3`.
The verifier rejects a stale or different digest.

### What does each Representation show?

A shows two spatial source panels, their evidence, a directional difference,
uncertainty, the limitation, prohibited implications, and lineage.

B shows every frozen Result leaf as a typed path-value row, followed by its
declared mapping loss and authority boundary.

### Which values came directly from the Result?

| Meaning | Result path | A | B |
| --- | --- | --- | --- |
| Result identity | `/id` | visible | visible |
| Compared field | `/comparison/field` | visible in both source panels | visible as a row |
| First source and value | `/comparison/sources/0` | visible | visible as leaf rows |
| Second source and value | `/comparison/sources/1` | visible | visible as leaf rows |
| Signed difference | `/comparison/signed_difference` | visible on arrow | visible as a row |
| Evidence | `/evidence` | visible beside sources | visible as rows |
| Uncertainty and limitation | `/uncertainty` | visible as boundary text | visible as rows |
| Prohibited implications | `/prohibited_implications` | visible as boundary text | visible as rows |
| Processor identity | `/processor` | visible in footer | visible as a row |

No displayed semantic value lacks a Result path.

### What does each Representation emphasize?

A emphasizes relation and direction through position and an arrow. B
emphasizes completeness, type, and lineage through explicit paths and JSON
literals. These are representational differences, not Result differences.

### What does each Representation omit or make less explicit?

A makes four lineage fields reachable through the bound Result rather than
directly visible and does not expose full JSON types or nesting.

B omits the SVG's spatial grammar and flattens nesting. Both losses remain
recorded in `representation-review.json`; no difference was normalized away.

### Did evidence and boundaries survive?

| Required concern | A | B | Review |
| --- | --- | --- | --- |
| Comparison meaning | PASS | PASS | PASS |
| Evidence | PASS | PASS | PASS |
| Uncertainty | PASS | PASS | PASS |
| Limitation | PASS | PASS | PASS |
| Prohibited implications | PASS | PASS | PASS |
| Processor lineage | PASS | PASS | PASS |
| Exact Result binding | PASS | PASS | PASS |
| Non-authoritative status | PASS | PASS | PASS |

### Did either Representation invent meaning?

No semantic invention was found. The SVG's arrow and spatial placement are
classified as presentational additions, not evidence or new Result fields.
The table contains exactly the frozen leaf paths and values.

### Can either Representation change or replace the Result?

No. Both renderers read the Result and write candidates to separate paths.
The verifier reads completed artifacts only. Replay confirms the Result and
all POA-001 checksums before and after execution.

### Where is each visible element traced?

The SVG embeds `data-result-path` attributes and exact Result lineage. The
Markdown table names the Result path on every semantic row. The deterministic
Review inventories both sets of paths, media digests, differences, and losses.

### What remains Human interpretation?

Whether the arrow is easier to understand than the table, whether one form is
preferable for a particular person, and what significance the comparison has
remain Human judgments. POA-003 makes no preference, recommendation, approval,
decision, or domain-validity claim.

## Negative-case review

| Invalid Representation | Required outcome | Observed |
| --- | --- | --- |
| Stale Result digest | block, no repair | PASS |
| Invented signed difference | block, no repair | PASS |
| Missing uncertainty/limitation | block, no repair | PASS |
| Missing evidence | block, no repair | PASS |
| Missing prohibited implication | block, no repair | PASS |
| Claimed semantic authority | block, no repair | PASS |
| Missing trace path | block, no repair | PASS |

## Review conclusion

For the single immutable POA-001 Result, A and B preserve the frozen required
meaning and boundary conditions while exposing materially different media,
structures, emphasis, visibility, and mapping loss. This Human Review accepts
the bounded POA-003 finding only. It does not establish general Representation
conformance or identical Human interpretation.
