# NEXAH POA-003 Freeze Report

> **Status:** Experimentally complete; informative freeze record
>
> **Reviewed:** 2026-07-25
>
> **Scope:** The single frozen POA-003 Representation-independence experiment
> only

This report records the implementation, review, and successful replay of
`examples/poa-003/`. It does not modify POA-001 or POA-002, extend OLS,
introduce OPU, formalize A–B–C or D–E notation, or establish a general
Representation framework.

## Experiment objective

POA-003 tests one hypothesis:

> Two different Representations of the same immutable Result can preserve the
> same source trace, evidence, uncertainty, limitations, prohibited
> implications, and non-authoritative boundary without changing the Result.

The experiment holds the committed POA-001 Result fixed. It compares:

- A — the committed POA-001 static SVG;
- B — a new deterministic Markdown table;
- C — a Human relational review of A and B against their common Result.

Only the Representation form changes. No Processor is executed.

## Review basis

The experimental claim follows the explicit final finding of
`POA_002_PROCESSOR_EQUIVALENCE.md`, which names Representation independence as
the next unproven architectural claim.

The frozen predecessor designs retained their recorded bytes:

| Frozen reference | SHA-256 |
| --- | --- |
| `docs/experiments/POA_001_MINIMAL_PROOF.md` | `989d3f151b750c39ad2e95a3b3d403c3cc15f2c89c7935853d3c4d2aea6c4d5b` |
| `docs/experiments/POA_002_PROCESSOR_EQUIVALENCE.md` | `0a9ff9b8afd88ce3707cdae97c69570c327ada4367cb99d634818251a8f4f50b` |
| `docs/experiments/POA_003_REPRESENTATION_INDEPENDENCE.md` | `7c9079e2fcf7aba81f018e8df89c7ab3dd64774a10574810587ee43c387caa70` |

All ten POA-001 artifacts and all nine POA-002 artifacts retained their
recorded baseline digests. POA-003 modified none of them.

## Implemented artifacts

The POA-003 directory contains exactly seven artifacts:

| Artifact | Implemented responsibility |
| --- | --- |
| `README.md` | Scope, artifact responsibilities, exact offline replay, negative tests, and bounded claim |
| `render-markdown.py` | Isolated standard-library-only deterministic renderer for Representation B |
| `result-table.md` | Committed non-authoritative Markdown Representation |
| `verify-representations.py` | Bounded completed-artifact verifier; it does not render, execute OLS, invoke a Processor, or repair input |
| `representation-review.json` | Immutable comparison of source binding, preserved meaning, differences, and mapping loss |
| `review.md` | Human A–B–C relational review requiring no source-code inspection |
| `SHA256SUMS` | Integrity digests for the other six artifacts |

Representation A remains the committed
`examples/poa-001/result.svg`; POA-003 neither copies nor modifies it.

## Replay procedure

Requirements are Python 3.11 or later, `shasum`, `cmp`, and a
POSIX-compatible shell. No network or external Python package is required.

The authoritative commands are the complete shell block under **Exact offline
replay commands** in `examples/poa-003/README.md`. From the repository root,
the exact replay command is:

```bash
awk 'BEGIN {inside=0} /^```bash$/ {inside=1; next} inside && /^```$/ {exit} inside {print}' \
  examples/poa-003/README.md | bash
```

The reviewed outcome was:

```text
Representation A deterministic replay: PASS
Representation B deterministic replay: PASS
Committed Representation comparison: PASS
Representation Review deterministic replay: PASS
stale Result digest blocked: PASS
invented value blocked: PASS
missing uncertainty blocked: PASS
missing evidence blocked: PASS
missing prohibited implication blocked: PASS
authority claim blocked: PASS
missing trace path blocked: PASS
checksum verification: PASS
POA-003 PASS
```

Replay writes all generated candidates and negative evidence below one
temporary directory. It does not overwrite committed evidence.

## Positive result

Both Representations bind:

- Result identity `result-001`;
- Result SHA-256
  `6d565b327ed812f7b4e3b2239298e07715bdf3ac077d759d48263ce1279bb6b3`.

Both preserve:

- comparison field `declared_value`;
- ordered source values `record-a = 2` and `record-b = 5`;
- signed difference `3`;
- evidence `supplied-record-a` and `supplied-record-b`;
- uncertainty `none-declared` for both source Records;
- limitation `The supplied values are not independently validated.`;
- prohibited implications `preference`, `recommendation`, and
  `domain-validity`;
- Processor identity `poa-001-compare`;
- the Result's non-authoritative Representation boundary.

Neither Representation recommends, approves, validates the domain, changes the
Result, invokes the Processor, or becomes a new semantic source.

## Representation differences

The experiment intentionally preserves differences:

| Concern | Representation A | Representation B | Classification |
| --- | --- | --- | --- |
| Media | SVG | Markdown | Representation-specific |
| Structure | Spatial groups, panels, and arrow | Ordered path-value rows | Representation-specific |
| Value visibility | Selected semantic groups | Every frozen leaf path | Disclosed mapping difference |
| Type visibility | JSON types not directly visible | JSON literals preserve string/number distinction | Disclosed mapping difference |
| Lineage visibility | Four fields require following exact Result binding | All lineage leaf paths visible | Disclosed mapping loss |
| Spatial relation | Present | Not reproduced | Disclosed media difference |

No difference was discarded or normalized away. The SVG's spatial placement
and arrow are classified as presentational additions, not new evidence or
Result fields.

## Negative result summary

| Required invalid case | Verifier result | Repair attempted | Status |
| --- | --- | --- | --- |
| Stale Result digest | `representation_b_stale_result_digest` | No | PASS |
| Invented signed difference | `representation_b_changed_or_invented_value` | No | PASS |
| Missing uncertainty/limitation | `representation_b_changed_or_missing_uncertainty` | No | PASS |
| Missing evidence | `representation_b_changed_or_missing_evidence` | No | PASS |
| Missing prohibited implication | `representation_b_missing_prohibited_implication` | No | PASS |
| Claimed semantic authority | `representation_b_claims_authority` | No | PASS |
| Missing required trace path | `representation_b_missing_required_trace_path` | No | PASS |

Every case exits with status `2`, emits an immutable blocked Review candidate,
and records `repair_attempted: false`.

## Deterministic replay status

| Check | Status |
| --- | --- |
| Two frozen SVG renderer runs produced identical bytes | PASS |
| Fresh SVG matched committed Representation A | PASS |
| Two Markdown renderer runs produced identical bytes | PASS |
| Fresh Markdown matched committed Representation B | PASS |
| A and B remained byte-distinct | PASS |
| A and B remained media- and structure-distinct | PASS |
| Two Representation Review runs produced identical bytes | PASS |
| Fresh Review matched committed Review | PASS |
| POA-001 checksums passed before and after replay | PASS |
| POA-003 checksums passed before and after replay | PASS |

## Checksum status

`examples/poa-003/SHA256SUMS` verifies all six other POA-003 artifacts.
The committed Representation digests are:

| Representation | SHA-256 |
| --- | --- |
| A — `examples/poa-001/result.svg` | `857d4aa28e531445a6e884eff1ab913d3821de88a975135c3d26fbad530effeb` |
| B — `examples/poa-003/result-table.md` | `b2739204f3d764b9754d305c37ee91cf2583163883b156b586914f6e2da0187e` |

Checksum verification status: **PASS**.

## Human Review status

`examples/poa-003/review.md` answers without source-code inspection:

- whether A and B read the same Result;
- what each Representation shows;
- which values came from the Result;
- what each form emphasizes;
- what each form omits or makes less explicit;
- whether evidence, uncertainty, limitations, and prohibited implications
  survived;
- whether either Representation invented meaning;
- whether either Representation can change the Result;
- where visible elements are traced;
- what remains Human interpretation.

C is explicitly a Human relational review, not a third Result, autonomous
interpretation, or new OLS construct. Human Review status: **PASS**.

## Repository boundary verification

| Boundary | Verification |
| --- | --- |
| POA-001 | All ten baseline artifact digests unchanged |
| POA-002 | All nine implementation artifacts and its frozen design unchanged |
| OLS and frozen architecture | Not modified |
| New implementation files | Exactly seven artifacts under `examples/poa-003/` |
| Reusable infrastructure | None introduced |
| Representation abstraction | None introduced |
| Shared utility library | None introduced |
| Processor | Not invoked, copied, changed, or abstracted |
| Representation A | Replayed only through its frozen renderer |
| Representation B | One isolated single-file renderer reading only the Result |
| Verifier | Experiment-local completed-artifact check only |
| A–B–C | Review labels only |
| D–E observer axis | Not formalized or implemented |
| OPU | Not introduced |
| Generated evidence | Temporary paths only |

Architecture consistency checks passed for all 15 graph edges and frozen
registries. Frozen/responsibility boundary checks passed. All ten canonical
architecture SVG sources and ten generated Plate digests passed.

## Remaining repository-wide exceptions

| Exception | Observed state | Does it affect POA-003? | Fix now? | Ownership |
| --- | --- | --- | --- | --- |
| Root README digest mismatch | Phase VII corpus expects `10cb10a979bede22f50c902a85b5d9aec8e2589852d2add6f747bd7654c82317`; current `README.md` is `f979e9f79ad86304da12a81bb511166fdf3015540d88a71b7b9c11b8ba6f28c4` | No. POA-003 reads only the POA-001 Result and two Representations | No | Phase VII evaluation-corpus maintenance |
| Connected Core revision mismatch | `workspace.yaml` pins `9f79bb06210402c40c9ef7d9937ca00d86c092b1`; connected Core is `57fdd7ea21944aba19ed2bc3c2a9254b8b20da8c` | No. POA-003 invokes no connected Core | No | Connected-workspace and Core pin governance |
| Localhost sandbox permission note | Restricted execution denied `127.0.0.1` binding in HTTP runtime tests | No. POA-003 opens no socket and requires no server or network | No repository change | Runtime test environment |

The repository suite reproduced the root README corpus mismatch and localhost
permission restriction already recorded by the predecessor Freeze Reports.
The first repository check attempted with Apple's Python 3.9 also failed its
known version boundary; rerunning with the bundled Python 3.12 made the
architecture checks pass and isolated only the exceptions above. None changes
the POA-003 Result, Representations, Review, replay, or checksums.

## Limitations of the experiment

POA-003 examines exactly one Result and two static Representations. One
Representation predates the experiment and the other is a deterministic
Markdown table. The verifier knows only this frozen Result shape and this
pair's declared mappings.

The experiment does not determine which medium is clearer, whether different
Humans interpret the forms identically, or whether either form is valid for a
domain decision. The source values remain supplied observations and are not
independently validated facts.

The A–B–C arrangement is a Human-review device. It does not establish a
universal triptych grammar. D–E observer-axis notation remains visual research
and is neither required nor rejected by this experiment.

## Validated by POA-003

- Representation independence of the committed SVG and Markdown table for the
  single immutable POA-001 `result-001`.
- Preservation of the frozen required meaning, source binding, evidence,
  uncertainty, limitation, prohibited implications, and non-authoritative
  boundary across those two forms.
- Inspectability of their media-specific differences and mapping losses.

## Not validated

- General Representation conformance.
- Arbitrary media or visualization equivalence.
- Identical Human interpretation.
- General OLS validity.
- General Processor conformance.
- Runtime semantic neutrality.
- Observer theory or formal A–B–C/D–E semantics.
- OPU.
- Domain validity, truth, recommendation, approval, or decision.
- APIs, services, registries, networks, databases, packages, streaming,
  distributed execution, AI integration, interaction, animation, deployment,
  performance, or scalability.

## Repository status recommendation

- Recommended commit message:
  `experiments: freeze POA-003 representation independence`
- Optional annotated tag after an isolated freeze commit:
  `poa-003-freeze`
- POA-003 status: **experimentally complete for this frozen slice**.
- No next POA is designed, implemented, or proposed by this report.

## Final conclusion

POA-003 passes every frozen success criterion for its single experimental
slice. It demonstrates that the committed SVG and Markdown table can present
the same immutable Result while preserving the required meaning and boundaries
and exposing rather than erasing their different structures and losses.

This does not establish general Representation independence, general OLS
validity, Processor conformance, Runtime neutrality, observer theory, OPU, or
domain truth. It establishes only one concrete piece of implementation
evidence: `result-001` is not semantically owned by either of these two
presentation forms.
