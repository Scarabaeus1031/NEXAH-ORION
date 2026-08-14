# POA-001 Human Review

- Review status: **PASS**
- Review scope: committed POA-001 artifacts
- Source-code reading required: **no**
- Domain-validity claim: **none**
- Recommendation or approval: **none**

## Required answers

### What was observed?

The immutable Observation contains two supplied orientation Records:

- `record-a` declares `declared_value` `2`, with evidence
  `supplied-record-a` and uncertainty `none-declared`;
- `record-b` declares `declared_value` `5`, with evidence
  `supplied-record-b` and uncertainty `none-declared`.

The Observation states that these supplied values were not independently
validated.

### What did the Processor actually do?

The OLS Expression requested only `COMPARE` over `declared_value`, ordered
`record-a` before `record-b`, and required evidence and uncertainty to be
preserved. The Processor copied both source values and calculated the signed
difference as second value minus first value.

It did not select sources, repair input, infer evidence, validate the domain,
recommend, approve, or continue.

### What changed?

The declared value changed from `2` in `record-a` to `5` in `record-b`. The
signed difference is `3`.

### What remains uncertain?

Both source Records declare uncertainty as `none-declared`. That does not mean
there is no uncertainty. The preserved limitation states that the supplied
values were not independently validated.

### Where did this graphical element come from?

Every visible SVG group has a `data-result-path`. The table below traces each
group from the static SVG to the immutable Result, OLS Expression, and
Observation.

## Trace table

| SVG group | Result path | Expression path | Observation path | Status |
| --- | --- | --- | --- | --- |
| `result-title` | `/id` | `/id` via `expression_ref` | `/id` via `observation_ref` | PASS |
| `record-a` | `/comparison/sources/0` | `/inputs/0`, `/field` | `/records/0` | PASS |
| `record-a-evidence` | `/evidence/0` | `/preserve/0` | `/records/0/evidence` | PASS |
| `record-b` | `/comparison/sources/1` | `/inputs/1`, `/field` | `/records/1` | PASS |
| `record-b-evidence` | `/evidence/1` | `/preserve/0` | `/records/1/evidence` | PASS |
| `signed-difference` | `/comparison/signed_difference` | `/operator`, `/field`, `/inputs` | `/records/0/declared_value`, `/records/1/declared_value` | PASS |
| `uncertainty` | `/uncertainty` | `/preserve/1` | `/records/0/uncertainty`, `/records/1/uncertainty`, `/limitation` | PASS |
| `prohibited-implications` | `/prohibited_implications` | `/prohibited_implications` | Not derived from Observation | PASS |
| `processor-footer` | `/processor` | Result's `/expression_sha256` binds the Expression | Expression's `/observation_sha256` binds the Observation | PASS |

## Boundary checks

| Check | Evidence | Status |
| --- | --- | --- |
| Same Human Request | Expression contains the exact Request reference and SHA-256 | PASS |
| Same Observation | Expression contains the exact Observation reference and SHA-256 | PASS |
| One capability | Expression declares only `COMPARE`; Processor blocks another operator | PASS |
| Evidence preserved | Result values equal both Observation evidence values | PASS |
| Uncertainty preserved | Result values equal both Observation uncertainty values | PASS |
| Limitation preserved | Result limitation equals Observation limitation | PASS |
| Prohibited implications preserved | Result list equals Expression list | PASS |
| No silent repair | Invalid required shape returns `blocked` with no comparison | PASS |
| No invention | Every Result value is copied from input or is the declared signed difference | PASS |
| Representation non-authority | Renderer reads Result only; SVG cannot modify Result | PASS |
| Human authority | Review records inspection only; it makes no approval or decision | PASS |

## Immutable lineage

| Artifact | SHA-256 |
| --- | --- |
| `request.json` | `d847553992b746790bc7f55dd8b58f06631c5f1e31fd0e8d60b6425f9fd7d52a` |
| `observation.json` | `fe3f1c9e4339bd7d646814e1af101876573934539e40e01b4878852d29bd1d73` |
| `expression.json` | `cc57e561e0e209d4cca504f63d044bb012a740ac6479da71fd4dacc0247a9667` |
| `compare.py` | `05e122b25d0cfb5f2ec05ec3d88ed9305013fb30f85ea77210380e885704b262` |
| `result.json` | `6d565b327ed812f7b4e3b2239298e07715bdf3ac077d759d48263ce1279bb6b3` |
| `render-svg.py` | `721e8f083760d128f9418c86f0a314f1ed17edd631cc1137030307d9921f4447` |
| `result.svg` | `857d4aa28e531445a6e884eff1ab913d3821de88a975135c3d26fbad530effeb` |

## Review conclusion

The committed POA-001 example passes the frozen Human inspection questions for
this one minimal comparison. This review makes no broader architectural claim.
