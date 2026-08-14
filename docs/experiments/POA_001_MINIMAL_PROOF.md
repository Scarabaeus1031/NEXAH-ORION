# NEXAH Proof of Architecture — POA-001

> **Status:** Planned experiment — design only
>
> **Architecture status:** Frozen reference
>
> **Scope:** One offline, deterministic, replayable example of:
>
> `Reality → Observation → OLS → Processor → Record → Representation → Human`
>
> This document proposes an experiment layout only. It does not implement the
> proof, extend OLS, alter ORION, or define a reusable schema, contract, format,
> protocol, service, package, or architecture.

---

## 1. Question

Can one developer replay a complete orientation chain and inspect every
transition without a server, database, API, registry, network, AI model,
package, stream, or hidden state?

The Human request is exactly:

> Compare these two orientation records.

The proof compares one declared numeric value in each record. It makes no
domain, preference, recommendation, causality, or validity claim.

---

## 2. One capability

The Processor implements only **COMPARE**.

It accepts exactly:

- one valid POA-001 OLS Expression;
- one referenced Observation containing exactly two records;
- one declared numeric field shared by those records.

It produces exactly:

- `complete` with the two source values, their signed difference, preserved
  evidence references, and preserved uncertainty; or
- `blocked` with one visible reason.

It does not observe, select sources, infer meaning, recommend, approve, render,
write upstream artifacts, or continue automatically.

The SVG renderer is not an orientation Processor and has no orientation
capability. It projects an existing Result into one static Representation.

---

## 3. Visible chain

| Architecture term | Visible POA-001 evidence | What it establishes | What it does not establish |
| --- | --- | --- | --- |
| Reality | README statement that the two supplied records are the subject being compared | The formal chain has a named subject outside its claims | That software has direct or complete access to reality |
| Observation | `observation.json` | Exactly what values, evidence, and uncertainty were made available | Domain truth or independent validation |
| OLS | `expression.json` | `COMPARE`, its two inputs, preserved statuses, and prohibited implications | A new OLS syntax or full OLS conformance |
| Processor | `compare.py` plus its checksum | One bounded deterministic comparison implementation | A general OLS interpreter or ORION replacement |
| Record | `result.json` | Immutable comparison outcome, lineage, evidence, uncertainty, status, and boundary | Human judgment or scientific validity |
| Representation | `render_svg.py` and `result.svg` | One traceable static view of the Result | Authority over the Result |
| Human | `review.md` | A reviewer can answer the required questions and trace the SVG | Automated interpretation, approval, or decision |

Reality has no machine artifact because the frozen architecture places it
outside formal ownership. Its boundary is visible in the README and in the
Observation's explicit limitation.

---

## 4. Proposed repository layout

Use one flat directory:

```text
examples/poa-001/
├── README.md
├── request.json
├── observation.json
├── expression.json
├── compare.py
├── result.json
├── render_svg.py
├── result.svg
├── review.md
└── SHA256SUMS
```

A flat directory is smaller and easier to inspect than separate input, request,
processor, result, representation, and review directories. File roles remain
unambiguous at this scale.

The implementation must use only the Python standard library and ordinary
local filesystem reads. Replay output must go to a temporary directory and must
never overwrite the committed example.

`SHA256SUMS` is an integrity list, not a package format. The repository revision
preserves the checksum file itself.

---

## 5. Artifact inventory

| Artifact | Authority and purpose | Reads | May produce |
| --- | --- | --- | --- |
| `README.md` | Human-readable subject boundary and replay instructions | Nothing | Nothing |
| `request.json` | Preserves the exact Human question and selected Observation | Nothing | Nothing |
| `observation.json` | Immutable input artifact containing the two records | Nothing | Nothing |
| `expression.json` | Minimal OLS semantic slice for the requested comparison | Request and Observation identities/digests | Nothing |
| `compare.py` | The one bounded deterministic Processor | Observation and Expression | Candidate `result.json` bytes only |
| `result.json` | Immutable Orientation Result Record | References upstream identities/digests | Nothing |
| `render_svg.py` | Deterministic projection with no semantic authority | Result | Candidate `result.svg` bytes only |
| `result.svg` | Static Representation of the Result | References Result identity/digest | Nothing |
| `review.md` | Human inspection answers and trace table | All committed artifacts except source code is not required for the answers | Nothing |
| `SHA256SUMS` | Detects any change to the committed proof artifacts | All listed files | Nothing |

No artifact may rewrite another artifact. Generation writes new candidate bytes
to a temporary replay directory. Byte comparison determines whether the
candidate matches the committed proof.

---

## 6. Minimal fields and their justification

The JSON shapes below are example-local and non-normative. They are not schemas
and must not be reused as an implied ecosystem contract.

### 6.1 `request.json`

| Field | Why it exists | Why nothing more is needed |
| --- | --- | --- |
| `id` | Gives the Human Request a stable local reference | Exact version is supplied by its digest |
| `question` | Preserves the Human's wording without rewriting it as an answer | No audience, preference, or expected answer is needed |
| `observation_ref` | Names the selected immutable input | The proof has exactly one Observation |

Illustrative shape:

```json
{
  "id": "request-001",
  "question": "Compare these two orientation records.",
  "observation_ref": "observation-001"
}
```

### 6.2 `observation.json`

| Field | Why it exists | Why nothing more is needed |
| --- | --- | --- |
| `id` | Gives the Observation a stable local reference | Exact version is supplied by its digest |
| `subject` | States what was observed without claiming that the record is reality | One sentence is sufficient for this proof |
| `field` | Declares the only value that may be compared | Prevents the Processor from choosing a field |
| `records` | Contains exactly the two identified values | No general Record model is needed |
| `evidence` in each record | Preserves the declared basis of each value | The proof does not rank or validate evidence |
| `uncertainty` in each record | Makes unknown or absent uncertainty visible | No probability model is required |
| `limitation` | States that the Observation is supplied input, not established truth | Prevents software-validity overclaiming |

Illustrative content:

```json
{
  "id": "observation-001",
  "subject": "Two supplied orientation records",
  "field": "declared_value",
  "records": [
    {
      "id": "record-a",
      "declared_value": 2,
      "evidence": "supplied-record-a",
      "uncertainty": "none-declared"
    },
    {
      "id": "record-b",
      "declared_value": 5,
      "evidence": "supplied-record-b",
      "uncertainty": "none-declared"
    }
  ],
  "limitation": "The supplied values are not independently validated."
}
```

### 6.3 `expression.json`

| Field | Why it exists | Why nothing more is needed |
| --- | --- | --- |
| `id` | Gives the Expression a stable local reference | Exact version is supplied by its digest |
| `request_ref` and `request_sha256` | Binds the semantic operation to the exact Human Request | Prevents silent substitution of intention |
| `observation_ref` and `observation_sha256` | Binds the operation to the exact Observation bytes | Makes an Observation change invalidate downstream work |
| `operator` | Declares `COMPARE`, the Processor's only capability | No operator registry is needed |
| `inputs` | Orders the two source Record identities | Prevents hidden source selection |
| `field` | Names the declared value being compared | Prevents hidden comparison criteria |
| `preserve` | Requires evidence and uncertainty to survive | No additional status set is used |
| `prohibited_implications` | Preserves the existing OLS boundary | The proof needs only the implications at risk in this comparison |

Illustrative shape:

```json
{
  "id": "expression-001",
  "request_ref": "request-001",
  "request_sha256": "<exact-request-digest>",
  "observation_ref": "observation-001",
  "observation_sha256": "<exact-observation-digest>",
  "operator": "COMPARE",
  "inputs": ["record-a", "record-b"],
  "field": "declared_value",
  "preserve": ["evidence", "uncertainty"],
  "prohibited_implications": [
    "preference",
    "recommendation",
    "domain-validity"
  ]
}
```

This is an informative carrier example for an existing OLS operator. It does
not add an OLS primitive or claim that these field names are OLS syntax.

### 6.4 `result.json`

| Field | Why it exists | Why nothing more is needed |
| --- | --- | --- |
| `id` | Gives the Result a stable local reference | Exact version is supplied by its digest |
| `status` | Distinguishes `complete` from `blocked` | The proof has no asynchronous lifecycle |
| `expression_ref` and `expression_sha256` | Identifies the exact semantic input | Request and Observation are already bound by the Expression |
| `processor` and `processor_sha256` | Identifies the exact implementation | No provider, service, runtime, or registry exists |
| `comparison` | Preserves source IDs, source values, field, and signed difference | This is the Processor's entire output capability |
| `evidence` | Copies the two source evidence references without promotion | No evidence validation is performed |
| `uncertainty` | Copies source uncertainty and the Observation limitation | No uncertainty is inferred |
| `prohibited_implications` | Carries the Expression boundary into the Result | Prevents the output from implying more than comparison |

For a blocked Result, `comparison` is absent and one `reason` replaces it. A
blocked Result retains the same lineage, evidence, uncertainty, and prohibited
implications.

No timestamp is included because it would break byte-for-byte replay and adds
nothing to this timeless local example.

### 6.5 `result.svg`

The SVG contains only:

- a title naming the Result;
- one box for `record-a`;
- one box for `record-b`;
- one arrow labeled with the signed difference;
- one uncertainty/limitation line;
- one footer naming the Processor and Result digest.

Every visible group has:

- a stable SVG `id`;
- a `data-result-path` pointing to the exact `result.json` field represented.

The SVG also contains the Result ID and Result SHA-256 in metadata. It contains
no script, animation, external resource, interaction, inference, or hidden
semantic field.

---

## 7. Transition inspection

| Transition | Required visible check | Failure |
| --- | --- | --- |
| Reality → Observation | README names the external subject boundary; Observation states its limitation | Observation is presented as reality or validated truth |
| Human Request → Observation | Request names the exact Observation selected by the Human | Processor selects or replaces the input |
| Observation → OLS | Expression contains the exact Observation digest, ordered Record IDs, field, preserved statuses, and prohibited implications | Any source or comparison criterion is implicit |
| OLS → Processor | Processor rejects every operator except `COMPARE` and every unsupported shape | Unsupported input is guessed, repaired, or accepted |
| Processor → Record | Result binds exact Expression and Processor digests and has `complete` or `blocked` status | Output lacks lineage or hides a stop |
| Record → Representation | SVG metadata binds the Result digest and each element names one Result path | A visible element has no source path |
| Representation → Human | Review answers the five required questions using artifacts and trace paths | Reviewer must read Python source to understand the outcome |

The Human Request appears before Observation selection in the interaction, while
the frozen seven-term architecture begins at Reality and Observation. POA-001
shows both without adding the Request as a new architectural layer.

---

## 8. Replay procedure to be implemented

The future README should require only locally available `python3`, `shasum`, and
`cmp` or their documented platform equivalents.

Replay performs these steps:

1. verify `SHA256SUMS`;
2. create an empty temporary directory;
3. run `compare.py` with the committed Expression and Observation;
4. compare candidate Result bytes with committed `result.json`;
5. run `render_svg.py` with the candidate Result;
6. compare candidate SVG bytes with committed `result.svg`;
7. verify that every SVG `data-result-path` resolves in the Result;
8. display the paths to `review.md` and `result.svg`;
9. delete or leave the temporary replay directory outside the proof.

The committed artifacts are read-only inputs to replay. The programs must use
stable key ordering, whitespace, number rendering, line endings, SVG element
ordering, and no current time or environment-dependent values.

### Required negative replays

Only three negative cases are necessary:

| Change | Expected outcome |
| --- | --- |
| Unsupported operator in a temporary Expression | Processor emits or reports visible `blocked`; it does not compare |
| Observation bytes changed without updating the Expression digest | Processor stops before comparison |
| Result bytes changed without regenerating the SVG | Renderer/trace verification detects the Result-digest mismatch |

Negative cases are temporary mutations made during replay. They are not
additional committed fixtures.

---

## 9. Change-isolation proof

| Changed artifact | Must remain unchanged | Immediate expected change | Downstream consequence after explicit replay |
| --- | --- | --- | --- |
| `result.svg` only | Request, Observation, Expression, Processor, Result | SVG digest only | Replay restores or rejects the untraceable Representation; Result never changes |
| `compare.py` only | Request, Observation, Expression | Candidate Result or Processor digest | Representation changes only when the separate downstream renderer is run |
| `observation.json` | Nothing downstream is presumed valid | Observation digest | Expression binding must change, then Result and SVG must be regenerated |

This interprets “changing the Processor changes only the Result” at the
Processor transition: the Processor cannot write the Observation, Expression,
or Representation. A full downstream replay may then produce a new
Representation of the new Result, as the frozen chain requires.

Changing the SVG cannot change the Result because the renderer and SVG have no
write path to it.

---

## 10. Human validation

`review.md` is completed from the committed artifacts, not from Python source.
It contains exactly:

### Required answers

| Question | Required answer source |
| --- | --- |
| What was observed? | Observation subject, two Record IDs and values, evidence, uncertainty, and limitation |
| What did the Processor actually do? | Expression operator/field and Result comparison |
| What changed? | Result's signed difference from `record-a` to `record-b` |
| What remains uncertain? | Preserved uncertainty plus the Observation limitation |
| Where did this graphical element come from? | SVG ID → Result path → Expression input → Observation Record |

### Required trace table

| SVG element | Result path | Expression path | Observation path |
| --- | --- | --- | --- |
| Title | Result ID | Expression reference | Observation reference |
| Record A box | First comparison source/value | First input | First Record |
| Record B box | Second comparison source/value | Second input | Second Record |
| Difference arrow | Signed difference and field | Operator and field | Both declared values |
| Uncertainty line | Uncertainty | Preserved statuses | Both uncertainties and limitation |
| Footer | Processor identity and Result digest | Expression digest | Observation digest through Expression |

The reviewer records `pass` or `fail` for each answer and trace. No approval,
preference, recommendation, or action is requested.

---

## 11. Success criteria

POA-001 passes only when all of the following are true:

1. a second developer replays the proof completely offline from documented
   commands;
2. checksum verification covers every committed proof artifact except
   `SHA256SUMS`, whose bytes are fixed by the repository revision;
3. replay never overwrites a committed artifact;
4. candidate Result and SVG bytes exactly match their committed counterparts;
5. every transition in Section 7 has a visible artifact check;
6. every visible SVG element resolves to a Result path and ultimately to one or
   both source Records;
7. the three negative replays stop or fail exactly as declared;
8. editing only the SVG leaves Result bytes and digest unchanged;
9. changing the Processor cannot write or alter Request, Observation,
   Expression, or SVG;
10. changing Observation bytes invalidates every downstream digest binding;
11. the Human reviewer answers all five questions without reading source code;
12. the proof makes no domain-validity, recommendation, approval, full-OLS,
   full-ORION, interoperability, or platform claim.

Any unmet item makes the experiment incomplete or failed. There is no partial
architecture certification.

---

## 12. Explicit non-deliverables

POA-001 does not create:

- a normative OLS expression model or carrier;
- a reusable request, result, or Record schema;
- a general Processor contract or capability registry;
- a second Processor or Processor substitution test;
- an API, service, server, database, queue, stream, or network path;
- a package or new file extension;
- an AI, provider, model, prompt, or orchestration path;
- an interactive, animated, audio, 3D, or domain-specific Representation;
- domain evidence validation;
- a change to OLS, ORION, NEXAHEDRON, or any frozen architecture document.

Only after this design is separately approved should implementation files under
`examples/poa-001/` be created.

---

## Why this is enough

POA-001 is sufficient because it makes every irreducible responsibility visible
once: an external subject is bounded by an Observation; an existing OLS
operator gives that Observation semantic intent; one deterministic Processor
acts within one declared capability; one immutable Result preserves lineage,
evidence, uncertainty, status, and prohibited implications; one static
Representation remains traceable and non-authoritative; and one Human can
inspect the entire path. Replay, checksum, negative, trace, and change-isolation
checks test the boundaries without adding infrastructure that the architecture
does not require.

The first architectural claim left unproven is **Processor interchangeability**:
POA-001 uses only one implementation, so it cannot show that a second independent
Processor can consume the same OLS Expression and produce a semantically
equivalent bounded Result while preserving the same authority and STOP
boundaries.
