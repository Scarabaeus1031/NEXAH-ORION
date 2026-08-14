# NEXAH Proof of Architecture — POA-003
# Representation Independence

> **Status:** Frozen experiment design
>
> **Scope:** One immutable POA-001 Result, two different Representations, and
> one Human relational review

## Purpose

POA-001 demonstrated one complete frozen chain. POA-002 demonstrated, for that
same slice, that the Processor boundary does not depend on one implementation.
POA-002 identifies Representation independence as the next unproven
architectural claim.

POA-003 tests only this hypothesis:

> Two different Representations of the same immutable Result can preserve the
> same source trace, evidence, uncertainty, limitations, prohibited
> implications, and non-authoritative boundary without changing the Result.

POA-003 does not extend OLS, define an Orientation Processing Unit, formalize an
observer-axis notation, or introduce another architectural layer.

## Normative references

POA-003 treats the following committed artifacts as frozen inputs:

- `docs/experiments/POA_001_MINIMAL_PROOF.md`;
- `docs/experiments/POA_002_PROCESSOR_EQUIVALENCE.md`;
- `examples/poa-001/result.json`;
- `examples/poa-001/result.svg`;
- `examples/poa-001/render-svg.py`.

POA-003 must not modify any of them.

## Experimental architecture

```text
                 one immutable Result
                    /           \
                   /             \
                  ▼               ▼
     Representation A       Representation B
       static SVG           Markdown table
                  \               /
                   \             /
                    ▼           ▼
                 relational review
                         ▼
                       Human
```

The Result is the only semantic source. Neither Representation may read the
Request, Observation, OLS Expression, Processor source, another
Representation, or the Human Review.

## A–B–C review structure

The Human Review uses a triptych only as an explanatory arrangement:

- **A** — the committed POA-001 static SVG;
- **B** — a deterministic Markdown table generated independently from the same
  Result;
- **C** — the Human relational review of A and B against the Result.

C is not a third semantic source, a synthesis Result, or an autonomous
interpreter. It records what A and B preserve, emphasize, omit, or make easier
to inspect.

The letters A, B, and C are review labels only. Any D–E observer-axis notation
remains outside this experiment because no frozen OLS or POA contract defines
it. Existing OLS concepts such as observer, perspective, position, and context
remain sufficient.

## Frozen variable and changed variable

| Concern | POA-003 treatment |
| --- | --- |
| Result | Fixed: committed `examples/poa-001/result.json` |
| OLS meaning | Fixed by the Result and frozen POA-001 lineage |
| Processor | Not executed and not varied |
| Representation A | Committed POA-001 SVG |
| Representation B | New deterministic Markdown table |
| Human Review | Compares both Representations with the Result |

Only the Representation form changes.

## Representation requirements

Each Representation must:

1. bind the exact Result identity and SHA-256 digest;
2. display the two declared sources and their values;
3. display the comparison field and signed difference;
4. preserve both evidence values;
5. preserve both uncertainty declarations and the limitation;
6. preserve every prohibited implication;
7. retain Processor identity as lineage;
8. expose that it is non-authoritative;
9. add no recommendation, preference, approval, validation, or domain claim;
10. be inspectable without reading renderer source.

The Representations need not have identical bytes, structure, ordering,
layout, emphasis, or visual grammar.

## Representation loss

Different forms necessarily expose different affordances and losses.

POA-003 does not normalize those differences away. The Representation Review
must record at least:

- fields visible in each Representation;
- Result fields reachable only through the bound Result digest;
- ordering or type information made more or less explicit;
- spatial relationships introduced by the SVG;
- visual relationships absent from the table;
- tabular explicitness absent from the SVG;
- any ambiguity introduced by either mapping.

A mapping loss is acceptable only when it is visible in the Review and does
not alter the required preserved meaning.

## Independence

Representation A and Representation B:

- use different media;
- use different renderer implementations;
- do not import or call one another;
- do not share a utility module;
- do not communicate;
- receive only the same immutable Result;
- write only to separate candidate paths during replay.

Representation B must not be produced by parsing or translating
Representation A.

## Representation Review

One deterministic verifier inspects the completed Result and both completed
Representations. It does not render, execute OLS, invoke a Processor, repair
input, or infer missing values.

The Review records:

- Result identity and digest;
- Representation identities and digests;
- source binding;
- required semantic preservation;
- visible mapping differences;
- disclosed loss;
- prohibited additions;
- non-authoritative status;
- a bounded pass or blocked verdict.

The verifier is evidence for this experiment only. It is not a general
Representation validator or reusable conformance framework.

## Human Review

Without reading source code, a reviewer must be able to answer:

1. Did A and B read the same Result?
2. What does each Representation show?
3. Which values came directly from the Result?
4. What does each Representation emphasize?
5. What does each Representation omit or make less explicit?
6. Did evidence, uncertainty, limitations, and prohibited implications survive?
7. Did either Representation invent meaning?
8. Can either Representation change or replace the Result?
9. Where is each visible element traced?
10. What remains a Human interpretation?

The Human may accept or reject the experimental finding. The Human does not
alter the Result.

## Determinism and immutability

Replay must:

- verify the committed POA-001 checksums before use;
- generate every candidate in a temporary directory;
- run Representation B twice and require byte identity;
- compare Representation A with a fresh run of its frozen renderer;
- compare both fresh candidates with their committed artifacts;
- run the Representation Review twice and require byte identity;
- verify POA-003 checksums;
- leave every committed artifact unchanged.

Byte equivalence between A and B is neither expected nor meaningful.

## Required negative cases

The verifier must block and preserve a diagnostic when:

1. a Representation is bound to a stale or different Result digest;
2. a Representation invents or changes a comparison value;
3. uncertainty or the limitation is omitted or changed;
4. evidence is omitted or changed;
5. a prohibited implication is omitted;
6. a Representation claims recommendation, approval, validation, or semantic
   authority;
7. a required trace path is absent.

No invalid Representation may be repaired or completed by the verifier.

## Success criteria

POA-003 succeeds only if:

- both Representations bind the same immutable Result;
- both preserve the required meaning and boundaries;
- the Representations are structurally and byte-wise different;
- implementation and media differences remain inspectable;
- mapping loss is explicitly recorded;
- neither Representation affects the Result;
- deterministic replay succeeds;
- committed checksums verify;
- all required negative cases block;
- Human Review answers every required question without source inspection.

## Explicit non-goals

POA-003 does not prove:

- general Representation conformance;
- arbitrary media equivalence;
- semantic equivalence of all visualizations;
- general OLS validity;
- Processor conformance;
- domain validity or truth;
- observer theory;
- a formal A–B–C or D–E grammar;
- OPU, runtime, transport, API, service, registry, network, database, package,
  streaming, AI, interaction, animation, or deployment behavior;
- that one Representation is preferable;
- that Human interpretations are identical.

## Required artifacts

Implementation is confined to `examples/poa-003/` and contains:

- `README.md`;
- `render-markdown.py`;
- `result-table.md`;
- `verify-representations.py`;
- `representation-review.json`;
- `review.md`;
- `SHA256SUMS`.

After successful implementation and replay,
`docs/experiments/POA_003_FREEZE_REPORT.md` records the bounded evidence.

## Why this is enough

POA-001 held one Processor and one Representation fixed. POA-002 varied only
the Processor and thereby tested implementation independence for one declared
capability. POA-003 now holds the immutable Result fixed and varies only the
Representation form. If the SVG and Markdown table preserve the same required
meaning and boundaries while exposing their different mappings and losses,
the experiment provides bounded evidence that a Result is not owned by one
presentation. The next architectural claim remains unproven: a declared
runtime can admit and invoke the same frozen work without acquiring semantic
authority. POA-003 does not design or test that runtime claim.
