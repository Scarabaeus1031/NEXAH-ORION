# POA-002 Human Review

- Review status: **PASS**
- Review scope: committed POA-001 references and POA-002 artifacts
- Source-code reading required: **no**
- Preferred Processor: **none**
- Domain-validity claim: **none**

## Required answers

### Did both Processors receive the same Observation?

Yes. Both executions received the unchanged POA-001 `observation.json`.
`equivalence-review.json` records its SHA-256 as
`fe3f1c9e4339bd7d646814e1af101876573934539e40e01b4878852d29bd1d73`
for both Processor bindings.

### Did both receive the same OLS Expression?

Yes. Both complete Results reference `expression-001` with SHA-256
`cc57e561e0e209d4cca504f63d044bb012a740ac6479da71fd4dacc0247a9667`.
The Expression binds the same Human Request and Observation for both
executions.

### Where do the implementations differ?

Processor A is the frozen `../poa-001/compare.py`, identified as
`poa-001-compare`, with source SHA-256
`05e122b25d0cfb5f2ec05ec3d88ed9305013fb30f85ea77210380e885704b262`.
It validates the frozen shapes and lineage, then subtracts the first ordered
declared value from the second.

Processor B is `processor-b.py`, identified as `poa-002-compare-b`, with source
SHA-256
`0b9d285267ff511f4a6f5bc6e24d0d61684c52e8a24c7439f927e02035d05a06`.
It indexes validated records by identifier, resolves the declared order, and
sums the second value with the negated first.

Processor A was already committed and frozen. Processor B was authored anew in
a separate implementation task from the frozen POA-002 artifact requirements.
It does not copy, import, call, generate from, wrap, or communicate with
Processor A. The replay runs each in a separate empty working directory, with a
separate process and output path. This establishes implementation independence
for this experiment; it does not claim separate human authorship or general
independence.

### Where do the Results differ?

The parsed Results differ at exactly three paths:

| Path | Result A | Result B | Classification |
| --- | --- | --- | --- |
| `/id` | `result-001` | `result-002-b` | Implementation-specific and required |
| `/processor` | `poa-001-compare` | `poa-002-compare-b` | Implementation-specific and required |
| `/processor_sha256` | Processor A digest | Processor B digest | Implementation-specific and required |

The files are not byte-equivalent. The Equivalence Review retains both complete
file digests, byte sizes, and all 14 raw difference segments. No raw or parsed
difference was discarded before classification.

### Are those differences semantic or implementation-specific?

All three parsed differences are implementation-specific identity differences.
The status, Expression lineage, comparison field, source order, source values,
signed difference, evidence, uncertainty, limitation, prohibited implications,
and STOP behavior are equal. No semantic difference was found.

### Which architectural boundaries remained unchanged?

- Both Processors received the same frozen inputs.
- Both preserve exact Expression lineage.
- Both preserve evidence without promotion.
- Both preserve uncertainty and the Observation limitation.
- Both preserve all prohibited implications.
- Both block the same three unsupported or invalid conditions.
- Neither blocked Result contains a comparison.
- Neither Processor repairs input, invents a value, reads the other Result, or
  communicates with the other Processor.
- The verifier reads completed Results only and does not recalculate the signed
  difference.
- The renderer reads only the immutable Equivalence Review.
- The SVG and this review remain non-authoritative Human views.

## Required review checks

| Check | Visible evidence | Status |
| --- | --- | --- |
| Identical frozen inputs | `/inputs` contains matching Request, Observation, and Expression digests | PASS |
| Implementation independence | `/processors` contains distinct paths, identities, digests, work directories, method summaries, and dependency checks | PASS |
| Structural equivalence | `/structural_equivalence/equal` | PASS |
| Semantic equivalence | `/semantic_equivalence/equal` and all comparison rows | PASS |
| Evidence preservation | `/boundary_checks/evidence_preserved` | PASS |
| Uncertainty preservation | `/boundary_checks/uncertainty_and_limitation_preserved` | PASS |
| Prohibited-implication preservation | `/boundary_checks/prohibited_implications_preserved` | PASS |
| STOP equivalence | `/boundary_checks/stop_cases` and `/boundary_checks/stop_equivalence` | PASS |
| Complete difference visibility | `/differences`, including parsed and raw inventories | PASS |
| SVG-to-source traceability | SVG metadata and every visible group path resolve in the Review | PASS |

## Negative result evidence

| Case | Processor A | Processor B | Equivalent boundary |
| --- | --- | --- | --- |
| Unsupported operator | `blocked`: `unsupported_operator` | `blocked`: `operator_not_implemented` | PASS |
| Changed Observation with stale digest | `blocked`: `observation_digest_mismatch` | `blocked`: `input_digest_conflict` | PASS |
| Invalid required input shape | `blocked`: `invalid_required_input_shape` | `blocked`: `required_expression_shape_invalid` | PASS |

The reason wording remains visibly different. In every case, both Results
preserve the same evidence, uncertainty, limitation, prohibited implications,
and Expression lineage; both omit `comparison`.

## Representation trace

| SVG group | Equivalence Review path | Upstream source |
| --- | --- | --- |
| `review-title`, `canvas` | `/id` | Equivalence Review identity |
| `shared-inputs` | `/inputs` | Frozen POA-001 Request, Observation, and Expression |
| `processor_a`, `processor_b` | `/processors/processor_a`, `/processors/processor_b` | Both Processor identities and source digests |
| `result-identities` | `/results` | Result A and Result B |
| `equivalence-levels` | `/semantic_equivalence/equal` | Required equivalence verdict |
| `semantic-row-1` through `semantic-row-13` | `/semantic_equivalence/comparisons/0` through `/semantic_equivalence/comparisons/12` | Explicit A/B semantic values |
| `difference-1` through `difference-3` | `/differences/parsed/0` through `/differences/parsed/2` | Complete parsed difference inventory |
| `boundary-1` through `boundary-7` | Corresponding `/boundary_checks` fields | Evidence, uncertainty, prohibited implications, invention, STOP, repair, and communication checks |
| `stop-case-1` through `stop-case-3` | `/boundary_checks/stop_cases/0` through `/boundary_checks/stop_cases/2` | Both blocked Results for each negative case |
| `verdict` | `/verdict` | Final bounded verdict and Review digest |

`equivalence.svg` metadata binds `equivalence-review-001` and the exact
Equivalence Review SHA-256. Every visible SVG group has a stable `id` and a
resolvable `data-equivalence-review-path`.

## Immutable lineage

| Artifact | SHA-256 |
| --- | --- |
| POA-001 `request.json` | `d847553992b746790bc7f55dd8b58f06631c5f1e31fd0e8d60b6425f9fd7d52a` |
| POA-001 `observation.json` | `fe3f1c9e4339bd7d646814e1af101876573934539e40e01b4878852d29bd1d73` |
| POA-001 `expression.json` | `cc57e561e0e209d4cca504f63d044bb012a740ac6479da71fd4dacc0247a9667` |
| Processor A | `05e122b25d0cfb5f2ec05ec3d88ed9305013fb30f85ea77210380e885704b262` |
| Result A | `6d565b327ed812f7b4e3b2239298e07715bdf3ac077d759d48263ce1279bb6b3` |
| Processor B | `0b9d285267ff511f4a6f5bc6e24d0d61684c52e8a24c7439f927e02035d05a06` |
| Result B | `b29336fdc35d0af1b49a232ab97a1e50c3d4c396d7ebf9ed07a9595958c7a990` |
| Equivalence Review | `4ce5632714309df241858be5989b05e9907deee7e0b3cb91bf13d094062affb6` |
| Renderer | `ca5915874782c705b7a9977412eaefe8b080cb243e2cc8ff3a6e067a72435b51` |
| SVG | `2d53abddfd560a8e630a216f7a83b602f7e80077ed2c7fc2de7267bdc929057e` |

## Review conclusion

POA-002 demonstrates semantic equivalence between these two independent
implementations for this one frozen `COMPARE` experiment. It does not establish
general Processor conformance, equivalence for other OLS operators,
Representation independence, distributed execution, general interoperability,
or domain validity.
