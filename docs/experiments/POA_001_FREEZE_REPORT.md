# NEXAH POA-001 Freeze Report

> **Status:** Experimentally complete; informative freeze record
>
> **Reviewed:** 2026-07-25
>
> **Scope:** The single frozen POA-001 experimental slice only

This report records the review and successful replay of the implementation in
`examples/poa-001/`. It does not alter the frozen architecture, extend OLS, or
add a Processor contract.

## Experiment objective

POA-001 asks whether one developer can replay and inspect one complete chain:

```text
Reality
  ↓
Observation
  ↓
OLS
  ↓
Processor
  ↓
Record
  ↓
Representation
  ↓
Human
```

The implemented slice compares the declared numeric value of two supplied
orientation records. It must operate offline, preserve evidence and
uncertainty, expose lineage, stop on unsupported or invalid input, and render
the immutable Result without giving the Representation semantic authority.

## Review basis

Every file under `examples/poa-001/` was inspected against
`POA_001_MINIMAL_PROOF.md`, and the complete replay procedure was executed.
No inconsistency requiring an implementation change was found.

The frozen experiment documents retained the same bytes across the POA-001
implementation and freeze review:

| Frozen reference | SHA-256 |
| --- | --- |
| `docs/experiments/POA_001_MINIMAL_PROOF.md` | `989d3f151b750c39ad2e95a3b3d403c3cc15f2c89c7935853d3c4d2aea6c4d5b` |
| `docs/experiments/POA_002_PROCESSOR_EQUIVALENCE.md` | `0a9ff9b8afd88ce3707cdae97c69570c327ada4367cb99d634818251a8f4f50b` |

The implemented renderer is named `render-svg.py`. This follows the later,
explicit POA-001 implementation instruction; its responsibility remains the
one assigned to `render_svg.py` in the frozen design.

## Implemented artifacts

The implementation contains exactly the ten artifacts required by the frozen
design:

| Artifact | Implemented responsibility |
| --- | --- |
| `README.md` | Defines the external subject boundary, constraints, exact offline replay, expected outcomes, and scope of the claim |
| `request.json` | Preserves the exact Human question and selected Observation |
| `observation.json` | Preserves the two supplied records, evidence, uncertainty, and limitation |
| `expression.json` | Declares the bounded `COMPARE` operation and binds the exact Request and Observation |
| `compare.py` | Provides the single isolated deterministic implementation of `COMPARE` |
| `result.json` | Preserves the complete immutable Result, lineage, evidence, uncertainty, limitation, and prohibited implications |
| `render-svg.py` | Deterministically projects only the supplied immutable Result |
| `result.svg` | Provides the static, path-traceable Representation |
| `review.md` | Records the Human-readable answers and trace table |
| `SHA256SUMS` | Lists the integrity digests of the other nine committed artifacts |

There is no package, shared utility, reusable framework, registry, service,
database, API, or Processor abstraction in the example.

## Replay procedure

Requirements are Python 3.11 or later, `shasum`, `cmp`, and a
POSIX-compatible shell. No network or external Python package is required.

The authoritative commands are the complete shell block under **Exact offline
replay commands** in `examples/poa-001/README.md`. To execute that exact block
from the repository root without copying it, the reviewed replay used:

```bash
awk 'BEGIN {inside=0} /^```bash$/ {inside=1; next} inside && /^```$/ {exit} inside {print}' \
  examples/poa-001/README.md | bash
```

The procedure first verifies committed checksums, creates a directory with
`mktemp -d`, writes every generated candidate and negative Result there,
compares candidate bytes with committed evidence, performs lineage and
boundary checks, and verifies committed checksums again. It does not overwrite
the committed Request, Observation, Expression, Processor, Result,
Representation, review, or checksum list.

Expected terminal outcome:

```text
POA-001 PASS
```

## Positive result

The positive execution completed with the exact declared values `2` and `5`
and signed difference `3`. It retained:

- evidence `supplied-record-a` and `supplied-record-b`;
- uncertainty `none-declared` for both records;
- the limitation that the supplied values are not independently validated;
- the prohibited implications `preference`, `recommendation`, and
  `domain-validity`.

The candidate Result matched committed `result.json` byte for byte. The
candidate SVG generated from that Result matched committed `result.svg` byte
for byte.

## Negative result summary

| Required case | Exit | Result | Reason | Review |
| --- | ---: | --- | --- | --- |
| Unsupported operator | `2` | `blocked` | `unsupported_operator` | PASS |
| Changed Observation with stale digest | `2` | `blocked` | `observation_digest_mismatch` | PASS |
| Invalid required input shape | `2` | `blocked` | `invalid_required_input_shape` | PASS |

Every blocked Result omitted `comparison` and retained the original evidence,
uncertainty, limitation, and prohibited implications. No case invented a
replacement value, selected a different input, repaired invalid input, or
continued silently.

## Deterministic replay status

| Check | Status |
| --- | --- |
| Two independent Processor runs produced identical Result bytes | PASS |
| Candidate Result matched the committed Result bytes | PASS |
| Two independent renderer runs produced identical SVG bytes | PASS |
| Candidate SVG matched the committed SVG bytes | PASS |
| A Processor identity change changed the Result while preserving comparison semantics and preserved fields | PASS |
| A Representation-only edit left the Result unchanged | PASS |

The SVG renderer was also reviewed structurally: it reads one supplied Result,
contains no comparison calculation, and writes only its candidate SVG to
standard output. It does not read the Observation, Request, Expression, or
Processor.

## Checksum status

`shasum -a 256 -c SHA256SUMS` passed before and after replay for all nine listed
artifacts. `SHA256SUMS` is excluded from its own list and is preserved by the
repository revision.

The lineage checks also passed:

- Expression to exact Request and Observation bytes;
- Result to exact Expression and Processor bytes;
- SVG metadata to exact Result bytes;
- every `data-result-path` in the SVG to a resolvable Result field.

## Human Review status

`review.md` answers, without requiring source-code inspection:

- what was observed;
- what the Processor did;
- what changed;
- what remains uncertain;
- where each visible SVG element came from.

It identifies the comparison, the preserved evidence and limitation, the
prohibited implications, and the Result paths used by the Representation.
Human Review status: **PASS**.

## Repository boundary verification

| Boundary | Verification |
| --- | --- |
| Frozen architecture references | Their recorded content digests did not change during implementation or this review |
| POA-002 | Remains a design document only; no `examples/poa-002/` or Processor B exists |
| Reusable framework | None appeared |
| Shared Processor abstraction | None appeared |
| `compare.py` | Remains one isolated, single-file, standard-library-only `COMPARE` implementation |
| `render-svg.py` | Reads only the immutable Result and does not recalculate or reinterpret the comparison |
| Generated artifacts | Replay candidates and negative Results are written only to a temporary directory; committed POA artifacts remain under `examples/poa-001/` |
| Repository architecture checks | Architecture consistency, frozen/responsibility boundaries, and all architecture plate checks passed |

The complete repository test command reported only the three known categories
of repository-wide exception assessed below. Excluding the affected Phase VII
corpus and sandbox-bound HTTP modules, 538 tests passed. The 15 HTTP runtime
tests passed when executed in an environment permitted to bind localhost.

## Remaining repository-wide exceptions

| Exception | Observed state | Does it affect POA-001? | Fix now? | Ownership |
| --- | --- | --- | --- | --- |
| Root README digest mismatch | `evaluation/phase_vii/corpus.json` expects `10cb10a979bede22f50c902a85b5d9aec8e2589852d2add6f747bd7654c82317`; current `README.md` is `f979e9f79ad86304da12a81bb511166fdf3015540d88a71b7b9c11b8ba6f28c4` | No. POA-001 neither reads nor binds the root README | No. Resolving whether to accept the changed README and refresh its corpus evidence, or restore it, is unrelated to freezing this experiment | Phase VII evaluation-corpus maintenance, outside the POA experiment |
| Connected Core revision mismatch | `workspace.yaml` pins `9f79bb06210402c40c9ef7d9937ca00d86c092b1`; the connected Core is at `57fdd7ea21944aba19ed2bc3c2a9254b8b20da8c` | No. POA-001 is self-contained and invokes no connected Core | No. Checking out, reconnecting, or approving a Core revision is a separate workspace-governance action | Connected-workspace and Core pin management, outside the POA experiment |
| Localhost sandbox permission note | The sandbox denied local socket binding in four HTTP runtime tests; all 15 runtime tests passed when localhost binding was permitted | No. POA-001 opens no socket and requires no network or server | No repository change. Record the execution-environment restriction when running those runtime tests | Runtime test environment, outside the POA experiment |

None of these exceptions changes POA-001 input, execution, output, lineage,
checksums, or Human Review. They are therefore not POA-001 freeze blockers.

## Limitations of the experiment

POA-001 contains one Observation shape, one Expression, one Processor
implementation, one `COMPARE` capability, one Result shape, and one static SVG
projection. It demonstrates deterministic behavior only for these committed
artifacts and required negative cases.

It does not test other OLS vocabulary or operators, general conformance,
independent Processor implementations, alternative Representations, multiple
domains, distributed execution, interoperability, performance, services,
registries, networks, APIs, databases, packages, streaming, or AI integration.
The supplied values also remain supplied observations rather than independently
validated facts.

## Repository status recommendation

- Recommended commit message:
  `experiments: freeze POA-001 minimal proof`
- Optional annotated tag after an isolated freeze commit:
  `poa-001-freeze`
- Readiness for POA-002: **yes, as a future separate experiment**. POA-001 has
  passed its frozen criteria, and the remaining repository-wide exceptions do
  not block the Processor-equivalence claim. POA-002 should begin only from an
  intentional repository state after the POA-001 implementation and this
  report are committed together.

No tag or commit is created by this report, and no POA-002 implementation has
begun.

## Final conclusion

POA-001 passes the success criteria of this single frozen experimental slice:
its positive and negative behavior is deterministic and inspectable, its
evidence and boundaries are preserved, its committed artifacts verify, and a
Human can trace the static Representation back to the immutable Result.

POA-001 validates only this single frozen experimental slice.

- It does not establish general OLS validity.
- It does not establish Processor conformance in general.
- It does not establish Representation independence.
- It does not establish multi-Processor equivalence.

Those remain future architectural claims.
