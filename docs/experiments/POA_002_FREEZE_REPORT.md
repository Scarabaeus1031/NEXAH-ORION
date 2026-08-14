# NEXAH POA-002 Freeze Report

> **Status:** Experimentally complete; informative freeze record
>
> **Reviewed:** 2026-07-25
>
> **Scope:** The single frozen POA-002 Processor-equivalence experiment only

This report records the implementation, review, and successful replay of
`examples/poa-002/`. It does not alter POA-001, extend OLS, modify the frozen
architecture, establish a Processor abstraction, or begin POA-003.

## Experiment objective

POA-002 tests one hypothesis:

> Two independent implementations of the same declared OLS capability can
> produce semantically equivalent Results without sharing implementation code.

The experiment changes only the Processor implementation. It supplies the same
committed POA-001 Observation and OLS Expression to frozen Processor A and new
Processor B, preserves both independent Results, compares them only after both
executions end, renders the immutable Equivalence Review, and presents the
evidence to a Human.

## Review basis

Every POA-002 artifact was inspected against
`POA_002_PROCESSOR_EQUIVALENCE.md`, and the complete documented replay was
executed after the committed artifacts were generated.

The frozen experiment references retained their baseline bytes:

| Frozen reference | SHA-256 |
| --- | --- |
| `docs/experiments/POA_001_MINIMAL_PROOF.md` | `989d3f151b750c39ad2e95a3b3d403c3cc15f2c89c7935853d3c4d2aea6c4d5b` |
| `docs/experiments/POA_002_PROCESSOR_EQUIVALENCE.md` | `0a9ff9b8afd88ce3707cdae97c69570c327ada4367cb99d634818251a8f4f50b` |

All ten POA-001 artifacts also retained their recorded baseline digests. No
POA-001 file was modified.

## Implemented artifacts

The POA-002 directory contains exactly the nine artifacts required by the
frozen design:

| Artifact | Implemented responsibility |
| --- | --- |
| `README.md` | Defines scope, independence evidence, exact offline replay, expected outcome, and claim boundary |
| `processor-b.py` | Provides the second independent, single-file implementation of the frozen `COMPARE` capability |
| `result-b.json` | Preserves Processor B's immutable complete Result |
| `verify-equivalence.py` | Compares completed Results, frozen lineage, dependencies, differences, and STOP evidence without executing OLS |
| `equivalence-review.json` | Preserves the immutable path-by-path Equivalence Review and bounded verdict |
| `render-svg.py` | Projects only the immutable Equivalence Review |
| `equivalence.svg` | Provides the static, path-traceable Human Representation |
| `review.md` | Answers every frozen Human Review question without requiring source inspection |
| `SHA256SUMS` | Lists the integrity digests of the other eight POA-002 artifacts |

POA-002 copies no POA-001 input or Result. It reads the committed POA-001
artifacts directly.

## Replay procedure

Requirements are Python 3.11 or later, `shasum`, `cmp`, and a
POSIX-compatible shell. No network or external Python package is required.

The authoritative commands are the complete shell block under **Exact offline
replay commands** in `examples/poa-002/README.md`. To run that exact block from
the repository root:

```bash
awk 'BEGIN {inside=0} /^```bash$/ {inside=1; next} inside && /^```$/ {exit} inside {print}' \
  examples/poa-002/README.md | bash
```

The reviewed terminal outcome was:

```text
POA-002 PASS
```

Replay creates one temporary experiment directory, separate empty working
directories and output paths for the two Processors, and a clean inherited
environment for every Processor invocation. All candidates and negative
evidence remain temporary. No committed POA-001 or POA-002 artifact is
overwritten.

## Processor independence

| Independence condition | Evidence | Status |
| --- | --- | --- |
| Distinct implementation identity | `poa-001-compare` and `poa-002-compare-b` | PASS |
| Distinct source path | `../poa-001/compare.py` and `processor-b.py` | PASS |
| Distinct source digest | `05e122…b262` and `0b9d28…5a06` | PASS |
| Different internal method | Ordered subtraction versus identifier indexing followed by summing the second value with the negated first | PASS |
| No shared local import or helper | Static dependency inventory contains standard-library imports only and no local imports | PASS |
| No cross-reference | Neither source names, imports, calls, generates from, or wraps the other | PASS |
| Separate runtime state | Separate processes, empty working directories, clean environments, and output paths | PASS |
| No Result communication | Each Processor receives only the Observation and Expression as data arguments; comparison begins after both terminate | PASS |

Processor A was already committed and frozen. Processor B was authored anew in
a separate implementation task from the frozen POA-002 artifact requirements.
This establishes implementation independence for this experiment. It does not
claim separate human authorship or general independence outside this slice.

## Positive results

Processor A independently reproduced committed POA-001 `result.json`.
Processor B independently reproduced committed `result-b.json`.

Both complete Results preserve:

- Expression identity `expression-001` and digest
  `cc57e561e0e209d4cca504f63d044bb012a740ac6479da71fd4dacc0247a9667`;
- comparison field `declared_value`;
- ordered sources `record-a`, then `record-b`;
- declared source values `2` and `5`;
- signed difference `3`;
- evidence `supplied-record-a` and `supplied-record-b`;
- uncertainty `none-declared` for both records;
- the limitation that the supplied values are not independently validated;
- prohibited implications `preference`, `recommendation`, and
  `domain-validity`.

No additional Result field or unsupported claim was introduced.

## Equivalence status

| Level | Definition applied | Result |
| --- | --- | --- |
| Byte equivalence | Entire stored byte sequences are identical | **False, expected, and not required** |
| Structural equivalence | Required fields, types, nesting, cardinality, and complete shape correspond | **PASS** |
| Semantic equivalence | Every meaning-bearing value and frozen boundary is equal | **PASS** |

Each Processor remains byte-stable against its own committed Result. POA-002
does not normalize the independent Results to make their bytes equal.

## Difference inventory

The complete Results have different whole-file digests and sizes. The Review
retains all 14 raw byte-difference segments, including byte ranges and segment
digests.

Parsed comparison found exactly three different paths:

| Path | Classification | Reason |
| --- | --- | --- |
| `/id` | Implementation-specific and required | Independent Results retain distinct identities |
| `/processor` | Implementation-specific and required | Each Result identifies its producing implementation |
| `/processor_sha256` | Implementation-specific and required | Each Result binds different source bytes |

No semantic path differs. The Review records zero differences discarded before
classification.

## Negative result summary

| Required case | Processor A | Processor B | Equivalent boundary |
| --- | --- | --- | --- |
| Unsupported operator | Exit `2`, `blocked`, `unsupported_operator` | Exit `2`, `blocked`, `operator_not_implemented` | PASS |
| Changed Observation with stale digest | Exit `2`, `blocked`, `observation_digest_mismatch` | Exit `2`, `blocked`, `input_digest_conflict` | PASS |
| Invalid required input shape | Exit `2`, `blocked`, `invalid_required_input_shape` | Exit `2`, `blocked`, `required_expression_shape_invalid` | PASS |

Different reason wording remains visible and is classified as
implementation-specific. Every blocked Result omits `comparison`, preserves
the same Expression lineage, evidence, uncertainty, limitation, and prohibited
implications, and records the triggering failure. Neither Processor repairs
input, invents a value, or continues silently.

## Deterministic replay status

| Check | Status |
| --- | --- |
| Two Processor A runs produced identical bytes | PASS |
| Processor A candidate matched committed Result A | PASS |
| Two Processor B runs produced identical bytes | PASS |
| Processor B candidate matched committed Result B | PASS |
| Two Equivalence Review runs produced identical bytes | PASS |
| Candidate Review matched the committed Review | PASS |
| Two SVG renderer runs produced identical bytes | PASS |
| Candidate SVG matched the committed SVG | PASS |
| Result A and Result B remained visibly byte-distinct | PASS |
| Representation-only mutation left both Results and Review unchanged | PASS |

## Checksum and lineage status

POA-001 `SHA256SUMS` and POA-002 `SHA256SUMS` passed before and after the
complete replay.

Lineage verification passed for:

- the frozen Request, Observation, Expression, Processor A, and Result A
  digests;
- both Processors' binding to the same Request, Observation, and Expression;
- each Result's exact Processor source digest;
- both independent Result identities and whole-file digests;
- the Equivalence Review's references to all compared artifacts;
- SVG metadata binding the exact Equivalence Review identity and digest;
- every visible SVG group's resolvable
  `data-equivalence-review-path`.

## Verifier and Representation boundaries

`verify-equivalence.py` reads completed Results and frozen artifacts only after
both Processor processes terminate. It compares the signed-difference values;
it does not calculate a replacement signed difference, execute OLS, repair a
Result, merge Results, rank Processors, or erase differences.

`render-svg.py` reads only the immutable Equivalence Review. It contains no
Observation, Expression, Result, or signed-difference calculation. Visual
inspection confirmed that the committed SVG exposes the shared inputs,
Processor and Result identities, semantic rows, identity differences,
boundaries, STOP evidence, and verdict without text collisions. The SVG
remains non-authoritative.

## Human Review status

`review.md` answers without Processor source inspection:

- whether both Processors received the same Observation and Expression;
- where the implementations differ;
- where the Results differ;
- whether each difference is semantic or implementation-specific;
- which architectural boundaries remained unchanged.

All ten required Human Review checks pass: identical inputs, implementation
independence, structural equivalence, semantic equivalence, evidence,
uncertainty, prohibited implications, STOP equivalence, difference visibility,
and source traceability. No Processor preference is stated.

Human Review status: **PASS**.

## Repository boundary verification

| Boundary | Verification |
| --- | --- |
| POA-001 | All ten baseline artifact digests are unchanged |
| Frozen experiment references | POA-001 and POA-002 design digests are unchanged |
| Frozen architecture | Baseline architecture digests are unchanged |
| New files | Exactly nine implementation artifacts under `examples/poa-002/` and this required Freeze Report |
| Reusable infrastructure | None introduced |
| Processor abstraction | None introduced |
| Shared utility library | None introduced |
| Processor B | One isolated standard-library-only file implementing only the frozen `COMPARE` slice |
| Generated evidence | Candidate artifacts remain in temporary paths |
| POA-003 | Not begun and not proposed |

Architecture consistency, frozen/responsibility boundary, and all architecture
plate checks passed.

The repository-wide suite ran 554 tests. It retained the same unrelated
exceptions already documented by the POA-001 freeze: one Phase VII corpus
setup error from the changed root README digest and four localhost HTTP-test
permission errors in the restricted sandbox; one test was skipped. The
connected Core also remains at
`57fdd7ea21944aba19ed2bc3c2a9254b8b20da8c` rather than the workspace pin
`9f79bb06210402c40c9ef7d9937ca00d86c092b1`. These conditions do not affect
POA-002, which reads no root README, invokes no connected Core, and opens no
network socket.

## Limitations of the experiment

POA-002 compares exactly two implementations of one frozen `COMPARE`
Expression over one supplied Observation and three required STOP cases. Its
development-independence evidence is artifact-, dependency-, method-, and
runtime-based; it does not claim separate human authorship. The supplied
values remain observations and are not independently validated domain facts.

The single static SVG demonstrates only this Review projection. No claim is
made for another Representation, operator, domain, Processor, transport, or
execution environment.

## Validated by POA-002

- Semantic equivalence of these two independent Processor implementations for
  this single frozen experiment.

## Not validated

- General Processor conformance.
- Arbitrary OLS operators.
- Representation independence beyond this experiment.
- Distributed execution.
- Interoperability in general.
- Domain validity.

## Final conclusion

POA-002 passes every frozen success criterion for this single experiment. Two
distinct, isolated, standard-library-only Processor implementations reproduce
their own immutable Results, preserve the same semantic outcome and authority
boundaries, expose every implementation-specific difference, and stop
equivalently on all required negative inputs.

This is evidence only for semantic equivalence between these two
implementations of this one frozen `COMPARE` slice. It establishes none of the
claims listed under **Not validated**.
