# NEXAH Proof of Architecture — POA-002

## Processor Equivalence

> **Status:** Planned experiment — design only
>
> **Prerequisite:** POA-001 has been implemented and has passed every success
> criterion in
> [`POA_001_MINIMAL_PROOF.md`](POA_001_MINIMAL_PROOF.md).
>
> **Architecture status:** Frozen reference
>
> **Scope:** Test only whether two independent implementations of the same
> POA-001 `COMPARE` capability produce semantically equivalent bounded Results.
>
> This document proposes an experiment layout only. It does not implement a
> Processor, create a fixture, extend OLS, alter POA-001, or define a reusable
> schema, contract, format, API, service, registry, network, package, deployment
> model, or architecture.

---

## 1. Question and hypothesis

Can two completely independent Processors execute the exact same POA-001 OLS
Expression and preserve the same semantic outcome and architectural boundaries
without sharing implementation code or state?

The hypothesis is:

> Two independent implementations of the same declared OLS capability can
> produce semantically equivalent Results without sharing implementation code.

POA-002 does not ask whether one implementation is faster, clearer, smaller, or
preferred. It asks only whether the frozen boundaries survive substitution of
the Processor.

---

## 2. Frozen experimental scope

POA-002 reuses the exact committed POA-001 artifacts:

- `request.json`;
- `observation.json`;
- `expression.json`.

It references those files directly and verifies their POA-001 checksums. It
does not copy, translate, normalize, repair, or extend them.

The reused semantic slice remains:

- operator: `COMPARE`;
- inputs: `record-a`, then `record-b`;
- field: `declared_value`;
- output meaning: the two declared values and their signed difference;
- preserved status: evidence and uncertainty;
- prohibited implications: preference, recommendation, and domain validity;
- outcomes: `complete` or visible `blocked`.

No field, operator, status, implication, or interpretation may be added.

---

## 3. Experimental path

```text
Reality
  ↓
Observation
  ↓
OLS Expression
    ├──────────────┐
    ↓              ↓
Processor A     Processor B
    ↓              ↓
Result A         Result B
    └──────┬───────┘
           ↓
Equivalence Review
           ↓
Representation
           ↓
Human
```

This is one fork and join inside the existing architecture:

- the fork supplies the same immutable OLS Expression and Observation to two
  Processors;
- the join reviews two independent Records;
- neither the fork nor the review changes OLS, the Processors, or the Results;
- the Representation remains a non-authoritative view for Human inspection.

---

## 4. One shared capability

Processor A and Processor B each implement only POA-001 `COMPARE`.

Each must:

- accept the exact same Observation and OLS Expression;
- validate the Request and Observation digests bound by the Expression;
- preserve source Record order;
- compare only `declared_value`;
- calculate the same signed difference;
- copy evidence without promotion;
- copy uncertainty and the Observation limitation without alteration;
- preserve the same prohibited implications;
- produce an independent `complete` or `blocked` Result;
- stop on every input that POA-001 declares unsupported or invalid.

Neither may:

- read the other Processor or Result;
- write to the other's working directory;
- select another input or comparison field;
- repair invalid input;
- infer evidence, uncertainty, preference, recommendation, validity, or
  causality;
- communicate through files, memory, environment state, process state, or
  network access;
- render the Representation or perform the Equivalence Review.

---

## 5. Processor independence

### 5.1 Development independence

To support the word “independent”:

1. the passing POA-001 Processor A, inputs, and required Result fields are
   frozen before Processor B begins;
2. Processor B is authored independently from the frozen artifact requirements,
   without inspecting Processor A source before Processor B is frozen;
3. neither implementation may copy, import, call, inspect, generate from, or
   wrap the other;
4. no local helper module may be shared;
5. each implementation is frozen by a different identity and SHA-256 digest
   before the two are compared;
6. each implementation's origin and freeze digest are recorded in the
   Equivalence Review.

Separate authors are preferred. If one developer must author both, the
experiment cannot claim complete development independence unless the two
implementations are produced in separated sessions from only the frozen
artifact requirements and are independently reviewed before comparison.

Different source digests alone are necessary but not sufficient: a copied
implementation with a cosmetic edit is not independent.

The internal algorithms may differ. Each implementation supplies a one-sentence
method summary before comparison so the difference can be inspected without
making either algorithm part of the semantic contract.

### 5.2 Runtime independence

Each Processor runs:

- as a separate local process;
- in a separate empty temporary working directory;
- with read-only access only to the same Observation and Expression;
- with no network;
- with no shared output path;
- with no inherited result or cache;
- once per invocation;
- with output captured only in its own candidate Result file.

Processor A completes or blocks before Result comparison begins. Processor B
does the same independently. The Equivalence Review reads both Results only
after both Processor invocations have ended.

### 5.3 Visible independence evidence

The final Human reviewer does not need to read source code. The Equivalence
Review must expose:

- distinct Processor identities;
- distinct source paths;
- distinct source digests;
- the predeclared one-sentence method summary for each implementation;
- separate working directories;
- the exact identical input digests received by each;
- a dependency check showing no import, call, or local helper shared between
  them;
- an authorship/independent-development statement;
- separate Result identities and digests;
- confirmation that neither Processor read the other's Result.

These facts establish the experiment's independence claim. They do not establish
that the implementations are generally independent outside this frozen slice.

---

## 6. Three kinds of equivalence

### 6.1 Byte equivalence

**Definition:** Result A and Result B are byte-equivalent only when their entire
stored byte sequences are identical.

Byte equivalence includes:

- field order;
- whitespace;
- line endings;
- number rendering;
- Result identity;
- Processor identity and digest;
- every other byte.

POA-002 does **not** require byte equivalence. It is normally expected to be
false because the independent Results must carry different Result and Processor
identities. Each Processor must still reproduce its own committed Result bytes
on replay.

### 6.2 Structural equivalence

**Definition:** Result A and Result B are structurally equivalent when both use
the same required POA-001 Result fields, types, nesting, cardinality, and
complete-versus-blocked shape, after treating the required independent Result
and Processor identity values as corresponding rather than equal.

Structural equivalence ignores:

- JSON object member order;
- insignificant whitespace;
- Result A versus Result B identity values;
- Processor A versus Processor B identity and digest values.

It does not ignore:

- a missing or additional semantic field;
- a type difference;
- source Record order;
- evidence or uncertainty cardinality;
- a `comparison` present in one blocked Result;
- a `reason` present in one complete Result.

Both Results must satisfy the same POA-001 shape. Structural equivalence is a
necessary comparison condition, but it does not by itself prove the hypothesis.

### 6.3 Semantic equivalence

**Definition:** Result A and Result B are semantically equivalent when every
meaning-bearing value and boundary required by the POA-001 Expression is the
same, despite visible implementation identity or byte-serialization
differences.

For a complete Result, both must have the same:

- `status`;
- Expression identity and digest;
- comparison field;
- ordered source Record identities;
- source values;
- signed difference;
- evidence references;
- uncertainty values and Observation limitation;
- prohibited implications.

For each negative replay, both must:

- reject or block the same unsupported or invalid condition;
- produce no complete comparison;
- preserve the same upstream lineage and boundary fields;
- avoid repair, invention, and continuation.

Blocked reason wording may differ, but the triggering condition, `blocked`
meaning, absent comparison, preserved statuses, and prohibited implications
must be the same.

### 6.4 Required level

POA-002 requires **semantic equivalence**.

Structural equivalence to the shared minimal POA-001 Result shape is required
as inspectable evidence. Byte equivalence between Processors is explicitly not
required. Byte stability remains required only when replaying each Processor
against its own committed Result.

---

## 7. Differences are classified, not erased

The Equivalence Review first records every Result difference. Only then may it
classify a difference as implementation-specific or semantic.

| Difference | Required classification |
| --- | --- |
| Result identity | Implementation-specific and required |
| Processor identity | Implementation-specific and required |
| Processor source digest | Implementation-specific and required |
| JSON member order or whitespace | Implementation-specific if both Results remain independently byte-stable |
| Blocked reason wording | Implementation-specific only when the same condition and boundary are preserved |
| Status | Semantic |
| Expression identity or digest | Semantic and lineage-bearing |
| Comparison field | Semantic |
| Source Record identity or order | Semantic |
| Source values or signed difference | Semantic |
| Evidence | Semantic and provenance-bearing |
| Uncertainty or limitation | Semantic and status-bearing |
| Prohibited implications | Semantic boundary |
| Continue versus block | Semantic and authority boundary |
| Additional unsupported claim | Semantic invention |

The Review must retain:

- both complete Result digests;
- a full path-by-path difference inventory;
- each difference's classification;
- the reason for that classification.

No normalization may discard a difference before it is recorded. A semantic
comparison may exclude only the explicitly listed implementation identities
and byte-presentation differences.

---

## 8. Proposed repository layout

POA-002 should remain a second flat example beside POA-001:

```text
examples/
├── poa-001/
│   ├── request.json
│   ├── observation.json
│   ├── expression.json
│   ├── compare.py
│   └── result.json
└── poa-002/
    ├── README.md
    ├── processor-b.py
    ├── result-b.json
    ├── verify-equivalence.py
    ├── equivalence-review.json
    ├── render-svg.py
    ├── equivalence.svg
    ├── review.md
    └── SHA256SUMS
```

The shortened POA-001 listing shows only the reused artifacts. Its `compare.py`
is Processor A and its `result.json` is Result A. POA-001 remains unchanged and
retains its other files.

POA-002 introduces no copied Request, Observation, or Expression. Relative
paths and exact POA-001 digests bind both Processors to the same inputs.

The two Processor files implement the same single capability. The verifier and
renderer are not orientation Processors:

- `verify-equivalence.py` validates and compares two completed Result Records;
- `render-svg.py` creates one static view of the Equivalence Review.

The implementation should use only the Python standard library and local
filesystem reads. No file under `examples/poa-002/` is created by this design
document.

---

## 9. Artifact responsibilities

| Artifact | Reads | May produce | Must never do |
| --- | --- | --- | --- |
| `README.md` | Frozen POA-001 and POA-002 design references | Nothing | Redefine the experiment |
| POA-001 `compare.py` | POA-001 Observation and Expression | Candidate Result A only | Read Processor/Result B or shared state |
| `processor-b.py` | POA-001 Observation and Expression | Candidate Result B only | Read POA-001 Processor/Result A or shared state |
| POA-001 `result.json` | References Expression and Processor A digests | Nothing | Represent Processor B |
| `result-b.json` | References Expression and Processor B digests | Nothing | Represent Processor A |
| `verify-equivalence.py` | Both Processors' identities, both Results, and frozen POA-001 inputs | Candidate Equivalence Review only | Repair or rewrite either Result |
| `equivalence-review.json` | References every compared artifact | Nothing | Become an OLS, domain, or Human authority |
| `render-svg.py` | Equivalence Review | Candidate static SVG only | Re-evaluate the comparison or equivalence |
| `equivalence.svg` | References Equivalence Review digest and paths | Nothing | Replace either Result or the Review |
| `review.md` | Inputs, Results, Equivalence Review, and SVG | Human pass/fail answers only | Require source-code reading |
| `SHA256SUMS` | Every committed POA-002 artifact except itself | Nothing | Act as a package or trust claim |

Every generated candidate is written to a fresh temporary directory. Replay
never overwrites committed artifacts.

---

## 10. Independent Result Records

Result A and Result B reuse exactly the minimal POA-001 Result fields. No
POA-002-only field is added to either Result.

They must differ in:

- `id`;
- `processor`;
- `processor_sha256`;
- whole-file digest.

They may differ in:

- JSON member order and whitespace;
- blocked reason wording within the limits in Section 6.3.

They must not differ in any other meaning-bearing field.

Each Result is independently replayable against its own Processor. Neither
Result refers to, supersedes, validates, or ranks the other.

---

## 11. One Equivalence Review

`equivalence-review.json` is an example-local immutable review artifact. It is
not a new general Record type or reusable contract.

### 11.1 Minimal fields

| Field | Why it exists |
| --- | --- |
| `id` | Gives this one Review a stable local reference |
| `inputs` | Proves both Processors received the same Request, Observation, and Expression identities and digests |
| `processors` | Preserves both independent implementation identities, source digests, and independence checks |
| `results` | Preserves both Result identities and digests without merging them |
| `byte_equivalence` | Records the exact-byte comparison and expected visible differences |
| `structural_equivalence` | Records shared fields, types, shapes, and all structural differences |
| `semantic_equivalence` | Records every required semantic path and its A/B values |
| `differences` | Retains the complete path-by-path difference inventory and classification |
| `boundary_checks` | Records evidence, uncertainty, prohibited implications, invention, and STOP comparisons |
| `verdict` | States `pass` only when every required semantic and boundary check passes |

The exact file shape remains local to POA-002. The implementation may not add
scores, tolerances, preferences, rankings, confidence, or inferred equivalence.

### 11.2 Semantic comparison table

The Review must show these rows without hiding equal values:

| Compared concern | Result A | Result B | Required relation |
| --- | --- | --- | --- |
| Input Request digest | Exact value | Exact value | Equal to POA-001 |
| Input Observation digest | Exact value | Exact value | Equal to POA-001 |
| Input Expression digest | Exact value | Exact value | Equal to POA-001 |
| Result status | Exact value | Exact value | Equal |
| Comparison field | Exact value | Exact value | Equal |
| Ordered source IDs | Exact values | Exact values | Equal and same order |
| Source values | Exact values | Exact values | Equal |
| Signed difference | Exact value | Exact value | Equal |
| Evidence | Exact values | Exact values | Equal to Observation |
| Uncertainty and limitation | Exact values | Exact values | Equal to Observation |
| Prohibited implications | Exact values | Exact values | Equal to Expression |
| Invented information | Listed additions or none | Listed additions or none | None |
| STOP behavior | Outcome per negative replay | Outcome per negative replay | Same boundary |

Processor and Result identities appear in the Review but are not required to be
equal.

---

## 12. Equivalence Review procedure

The future replay performs:

1. verify that POA-001 passed and that its Request, Observation, and Expression
   match their frozen digests;
2. verify POA-002 checksums;
3. create separate empty temporary directories for Processor A and Processor B;
4. invoke each Processor separately with read-only access to the same POA-001
   Observation and Expression;
5. byte-compare each candidate Result with its own committed Result;
6. confirm distinct Processor identities, source paths, source digests,
   working directories, and Result identities;
7. confirm no shared local dependency, import, output, cache, or communication
   path;
8. inventory every raw byte and parsed-path difference between the Results;
9. verify both Results against the same minimal POA-001 Result shape;
10. compare every semantic and boundary row in Section 11.2;
11. run both Processors independently against the same temporary negative
    inputs;
12. produce a candidate Equivalence Review;
13. byte-compare it with the committed `equivalence-review.json`;
14. render a candidate static SVG from the Review;
15. byte-compare it with the committed `equivalence.svg`;
16. present the Review, SVG, and `review.md` to the Human.

The verifier performs equality and trace checks only. It does not execute OLS,
recalculate the signed difference, repair a Result, choose a preferred
Processor, or replace Human review.

---

## 13. Required STOP comparison

The same three temporary negative cases from POA-001 are supplied independently
to both Processors:

| Negative case | Processor A must | Processor B must | Equivalent boundary |
| --- | --- | --- | --- |
| Unsupported operator | Block before comparison | Block before comparison | Neither silently accepts unsupported capability |
| Observation changed without Expression digest update | Stop before comparison | Stop before comparison | Neither repairs or ignores broken lineage |
| Invalid required input shape | Block without inventing a value | Block without inventing a value | Neither fills missing information |

The Processors need not use identical bytes or wording for a blocked outcome.
They must preserve the same semantic boundary: no complete comparison, no
invented data, no altered evidence or uncertainty, no changed prohibited
implications, and no continuation.

If one continues while the other blocks, semantic equivalence fails.

---

## 14. Failure conditions

| Failure | Why POA-002 fails |
| --- | --- |
| Processor A silently accepts unsupported input | Its declared capability boundary is not preserved |
| Processor B silently repairs invalid input | It changes input meaning and hides a required STOP |
| Either Processor invents information | The Result no longer derives only from the shared Observation and Expression |
| Prohibited implications differ | OLS semantic boundaries depend on implementation |
| Uncertainty changes | One implementation has promoted, removed, or invented status |
| Evidence changes | Provenance and evidential meaning depend on implementation |
| One Processor continues while the other blocks | STOP behavior is not interchangeable |
| Comparison field, source order, source values, or signed difference changes | The semantic outcome differs |
| Any other semantic meaning changes | The Processor implementation has changed the frozen semantic outcome, so the hypothesis is false |
| One Result omits required lineage | Equivalence cannot be inspected |
| A raw difference is discarded before classification | Implementation-specific and semantic differences cannot be audited |
| Processors share code, helpers, state, cache, or outputs | The experiment no longer tests independent implementations |
| Verifier repairs, recalculates, merges, or prefers a Result | The Review has become a third semantic Processor |
| Human must read source code to understand the result | Implementation differences are not exposed through artifacts |

One failure is sufficient to reject the hypothesis for POA-002.

---

## 15. Static Representation

`equivalence.svg` is one static, non-interactive view of the Equivalence Review.
It contains only:

- the shared Request, Observation, and Expression digests;
- Processor A identity leading to Result A identity;
- Processor B identity leading to Result B identity;
- the semantic comparison rows;
- every non-semantic difference classification;
- evidence, uncertainty, prohibited-implication, and STOP checks;
- the final `pass` or `fail` verdict;
- the Equivalence Review identity and digest.

Every visible SVG group has a stable `id` and one
`data-equivalence-review-path` pointing to the exact Review field represented.
The SVG contains no script, animation, external resource, interaction,
normalization, hidden comparison, or semantic authority.

The renderer reads only the Equivalence Review. Changing the SVG cannot change
the Review or either Result.

---

## 16. Human review

The Human reviews the frozen inputs, both Results, the Equivalence Review, and
the SVG. Source-code reading is not required.

`review.md` must answer:

| Question | Visible answer source |
| --- | --- |
| Did both Processors receive the same Observation? | Input digests in both Results and the Equivalence Review |
| Did both receive the same OLS Expression? | Expression identity/digest in both Results and the Equivalence Review |
| Where do the implementations differ? | Processor identities, source digests, independence checks, and difference inventory |
| Where do the Results differ? | Complete path-by-path difference table |
| Are those differences semantic or implementation-specific? | Classification and reason for every difference |
| Which architectural boundaries remained unchanged? | Evidence, uncertainty, prohibited implications, lineage, STOP, Representation, and Human-authority checks |

The reviewer records `pass` or `fail` for:

- identical frozen inputs;
- implementation independence;
- structural equivalence;
- semantic equivalence;
- evidence preservation;
- uncertainty preservation;
- prohibited-implication preservation;
- STOP equivalence;
- complete difference visibility;
- SVG-to-Review-to-Result-to-source traceability.

No preference between Processors is requested or permitted.

---

## 17. Success criteria

POA-002 passes only when:

1. POA-001 has already passed;
2. Processor A and Processor B are independently implemented and have distinct
   identities, source paths, source digests, and isolated execution state;
3. both receive the exact same immutable Request, Observation, and Expression;
4. both implement only the same declared `COMPARE` capability;
5. each independently reproduces its own committed Result bytes;
6. both Results conform structurally to the same minimal POA-001 Result shape;
7. the Equivalence Review records every raw and parsed difference before
   classification;
8. every meaning-bearing field is semantically equivalent;
9. evidence, uncertainty, limitation, and prohibited implications are
   unchanged;
10. all required negative cases preserve equivalent STOP behavior;
11. no Processor repairs input, invents information, communicates, or continues
    beyond its boundary;
12. implementation-specific differences remain visible;
13. byte equivalence is reported but is not required;
14. the static SVG traces every claim to the Equivalence Review, both Results,
    and the shared inputs;
15. a second developer replays the entire experiment offline;
16. the Human answers every review question without reading Processor source;
17. no claim extends beyond this one semantic slice and these two
    implementations.

There is no majority rule, tolerance, score, or partial pass. Both Processors
must preserve every required semantic and authority boundary.

---

## 18. Explicit non-goals

POA-002 does not attempt to prove:

- byte identity between independent Processors;
- full OLS Processor conformance;
- equivalence for another OLS operator or semantic slice;
- distributed execution;
- network interoperability;
- APIs or services;
- Processor discovery;
- a Processor registry;
- multiple domains or domain validity;
- AI integration;
- performance or optimization;
- scalability;
- package, streaming, database, or deployment behavior;
- multiple Representation forms;
- general equivalence of all implementations;
- preference for Processor A or Processor B.

It creates no implementation until this design is separately approved. It does
not modify POA-001 or any frozen architecture reference.

---

## Why this is enough

Processor Equivalence is the next architectural claim after POA-001 because
POA-001 can show only that one implementation realizes the frozen chain.
POA-002 changes exactly one variable—the Processor implementation—while holding
the Request, Observation, OLS Expression, semantic capability, evidence,
uncertainty, prohibited implications, STOP conditions, review method,
Representation boundary, and Human authority fixed. If two independently
authored and isolated implementations produce semantically equivalent bounded
Results, the architecture has its first evidence that its boundaries do not
depend on one codebase.

The next unproven architectural claim would be **Representation independence**:
POA-001 and POA-002 still use one static SVG form, so they do not show that two
different Representations of the same immutable Result can preserve the same
source trace, evidence, uncertainty, loss, and non-authoritative boundary
without changing the Result.
