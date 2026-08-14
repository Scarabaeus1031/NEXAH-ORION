# NEXAH Architecture Distilled

> **Status:** Informative editorial consolidation
>
> **Purpose:** Compress and stabilize the architecture already documented in
> [`OLS_1_0_REPOSITORY_ARCHITECTURE_EXTRACTION.md`](OLS_1_0_REPOSITORY_ARCHITECTURE_EXTRACTION.md),
> [`MACHINE_READABLE_ORIENTATION_ARCHITECTURE.md`](MACHINE_READABLE_ORIENTATION_ARCHITECTURE.md),
> and
> [`ORIENTATION_INFRASTRUCTURE_ARCHITECTURE_REVIEW.md`](ORIENTATION_INFRASTRUCTURE_ARCHITECTURE_REVIEW.md).
>
> This document introduces no new architecture and has no normative effect.
> Released OLS semantics, certified ORION boundaries, domain authority, and
> Human authority remain unchanged.

---

## 1. Distillation finding

The three source documents describe one essential architecture:

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

Reality is outside formal ownership. The downward path means “is made available
through a bounded, recorded transition,” not “is captured completely” or “passes
authority to the next layer.”

Everything else in the source documents serves one of five purposes:

1. defines one of these boundaries more precisely;
2. implements or transports something across a boundary;
3. preserves evidence about a boundary crossing;
4. explains the architecture;
5. explores an unadopted possibility.

The system does not require a universal format, graph, record, API, service
topology, package, registry, platform, or infrastructure layer to remain
coherent.

---

## 2. Part 1 — Core principles

These ten principles are the smallest set that preserves the repeated
architectural rules of all three source documents.

1. **Reality remains outside the formal system and is approached only through situated observation.**
2. **Domains own their sources, evidence criteria, and claims of scientific or factual validity.**
3. **OLS owns orientation semantics but not execution, domain truth, or Human meaning.**
4. **Processors act only within declared boundaries and stop visibly when those boundaries are not met.**
5. **Identity, provenance, evidence, uncertainty, status, and correction history remain inspectable.**
6. **Difference, disagreement, missing information, and unsupported claims must not be silently erased.**
7. **Representations declare their source and loss and never become authority over what they represent.**
8. **Encoding, storage, transport, invocation, and presentation do not transfer semantic or decision authority.**
9. **Every claim is limited to its declared scope and validation.**
10. **The Human owns intention, interpretation, continuation, approval, and consequential decision.**

### Why these are fundamental

Principles 1–3 locate semantic and domain authority. Principles 4 and 9 bound
software claims. Principles 5–7 preserve accountability through change and
representation. Principle 8 prevents technical convenience from changing
meaning. Principle 10 preserves the established Human boundary.

Provider independence, composability, extensibility, deterministic replay,
security, versioning, accessibility, and openness remain important, but they
are applications of these principles within particular specifications or
implementations rather than additional system-wide principles.

---

## 3. Part 2 — Essential architecture

### 3.1 Minimal diagram

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

### 3.2 Why each term remains

| Term | Why indispensable | Boundary preserved |
| --- | --- | --- |
| Reality | Prevents the formal system from equating its data or models with the subject itself | Representation is not reality |
| Observation | Makes selection, framing, measurement, testimony, provenance, and uncertainty explicit before semantic processing | Source acts and evidence remain domain-owned |
| OLS | Supplies the shared semantics and prohibited implications of orientation | Meaning remains separate from execution |
| Processor | Names bounded behavior without prescribing a library, process, service, provider, or runtime | Implementation claims remain scoped |
| Record | Preserves accountable identity, state, evidence, provenance, uncertainty, validation, and history | Processing does not disappear into transient output |
| Representation | Makes source-to-view transformation and loss visible | A view does not become its source |
| Human | Preserves intention, interpretation, continuation, approval, and decision outside autonomous processing | Software does not acquire consequential authority |

### 3.3 Why other layers can be removed from the core diagram

| Removed as a core layer | Derived from |
| --- | --- |
| Domain / Reality Interface | The boundary between Reality and Observation |
| Measurement, testimony, evidence class, and domain validation | Observation, with domain ownership |
| Abstract Expression Model | A structured realization of OLS semantics |
| Carrier, JSON, YAML, RDF, DSL, and canonical serialization | Encoding choices for OLS expressions or Records |
| Processor Capability, plan, execution, runtime, worker, gateway, and service | Contracts or deployment forms of Processor |
| Request, result, report, manifest, episode, validation record, and continuation record | Bounded kinds of Record |
| Provenance, evidence, uncertainty, correction, retraction, signature, and hash | Properties or supporting records of Observation and Record |
| Orientation Graph | A Record, plan, or Representation depending on its declared purpose |
| Representation Mapping Contract and Transition Contract | The governed transition from Record or OLS source to Representation |
| SVG, GLB, Markdown, audio, tables, animation, and UDF-style scenes | Kinds of Representation |
| Renderer, player, and native media | Means by which a Representation becomes perceptible |
| Workspace, application, and NEXAHEDRON | The interface through which a Human inspects and continues |
| Files, APIs, streams, queues, packages, and content-addressed stores | Transport or storage choices crossing the diagram |
| Semantic, execution, evidence, representation, transport, governance, and Human planes | Review perspectives over the same responsibilities |
| Infrastructure, platform, ecosystem, stack, protocol, and computing model | Explanatory or speculative descriptions, not additional responsibilities |

Governance remains necessary, but it is expressed by the named owner of each
responsibility rather than by adding a governance layer to the processing
sequence.

---

## 4. Part 3 — Responsibility compression

| Responsibility | Canonical owner | Derived responsibilities |
| --- | --- | --- |
| Subject outside formalization | No software owner | Reality boundary; prohibited claims of completeness |
| Observation and domain validity | Source, instrument, evidence, or domain owner | Measurement; testimony; acquisition; evidence class; calibration; domain validation |
| Orientation semantics | OLS governance | Concepts; declarations; profiles; primitive operators; semantic products; grammar; semantic conformance |
| Bounded processing | Named processor owner | Capability declaration; planning; execution; deterministic or nondeterministic behavior; STOP; operational isolation; ORION correspondence |
| Accountable preservation | Named Record-class owner | Requests; results; reports; manifests; evidence references; validation records; provenance; uncertainty; status; supersession; continuation |
| Representation | Source, mapping, media, and renderer owners within their separate scopes | Mapping; transition; graph view; SVG; GLB; Markdown; audio; animation; rendering; playback |
| Human authority | Human | Intention; scope choice; confirmation; interpretation; reflection; continuation; approval; decision |

### Compression rules

- **Carrier** is the collective term for JSON, YAML, RDF, DSLs, or other
  encodings; the architecture does not promote one encoding into a layer.
- **Representation** is the collective term for SVG, GLB, Markdown, audio,
  animation, tables, graphs, and other Human- or machine-perceivable views.
- **Processor** covers libraries, command-line tools, workers, isolated
  processes, browser workers, embedded implementations, and services.
- **Record** covers bounded immutable or superseding requests, results, reports,
  manifests, evidence, validation, provenance, and continuation artifacts.
- **Human** covers the authority boundary; Workspace and application describe
  where that authority is exercised, not a separate authority.

---

## 5. Part 4 — Vocabulary reduction

### 5.1 Core vocabulary

Use these terms in the permanent architecture overview:

| Term | Minimal meaning |
| --- | --- |
| Reality | The subject outside formal ownership |
| Observation | A situated, provenance-bearing claim or record about a source interaction |
| OLS | The authority for orientation semantics |
| Processor | A bounded implementation acting within declared scope |
| Record | An accountable, identity-bearing preservation of input, process, result, evidence, or history |
| Representation | A source-linked and potentially lossy view |
| Human | The owner of intention, interpretation, continuation, approval, and decision |

The plain qualifiers **authority**, **boundary**, **evidence**, **provenance**,
**uncertainty**, **status**, **loss**, and **STOP** remain necessary wherever
the corresponding condition exists. They are not additional layers.

### 5.2 Supporting vocabulary

Use only inside the specification or contract that needs it:

- reference, identity, version, scope, context, perspective, scale, boundary;
- declaration, primitive, profile, operator, semantic product, derivation,
  transition, conformance;
- request, result, report, manifest, validation, continuation, supersession;
- capability, determinism, canonicalization, replay, compatibility;
- carrier, mapping, native media, renderer, player, package, transport;
- application, Workspace, NEXAHEDRON, ORION, Kernel, LYRA;
- domain translation, analogy, equivalence, invariant, prohibited implication.

These terms clarify one core responsibility but should not appear in the
minimal diagram unless the document is specifically about them.

### 5.3 Historical vocabulary

Retain only in historical or archaeological discussions:

- the older general Orientation Grammar;
- LYRA as “The Language of Orientation”;
- UDF, UBF, and USF;
- `.nxa`, `.xva`, and `.scarab`;
- historical CORTEX or container terminology;
- superseded names for engine, runtime, gateway, or representation roles.

Historical evidence may explain lineage. It does not establish current
architecture or reserve a name.

### 5.4 Experimental vocabulary

Keep explicitly labeled as proposed, candidate, or informative:

- OLS Abstract Expression Model;
- OLS carrier profile;
- Processor Capability Contract;
- shared Record envelope;
- Orientation Graph as a cross-system view;
- Representation Mapping Contract;
- orientation package profile;
- Orientation Infrastructure;
- Orientation Computing;
- federation, discovery, and processor registry.

### 5.5 Recommended future vocabulary

Future overview documentation should begin with only:

> Reality, Observation, OLS, Processor, Record, Representation, Human.

It should add a supporting term only when a concrete specification, contract,
or boundary requires it. It should not use “infrastructure,” “platform,”
“protocol,” “stack,” “operating system,” “web,” or “computing” as synonyms for
the architecture.

---

## 6. Part 5 — Document consolidation

The classifications below apply to top-level sections. “Canonical” means the
best location among these three informative documents; it does not override a
released OLS specification, certified ORION baseline, accepted ADR, or
domain-owned specification.

### 6.1 OLS repository architecture extraction

| Section | Classification | Recommendation |
| --- | --- | --- |
| 0. Archaeological method and evidence status | Canonical | Keep as the method for the extraction |
| 1. High-level overview | Canonical | Keep as the informative introduction to released OLS |
| 2. Design principles | Duplicate | Replace architecture-wide repetition with a link to this distilled review; retain OLS-specific qualifications |
| 3. Vocabulary | Canonical | Keep as detailed OLS vocabulary navigation |
| 4. Grammar | Canonical | Keep; grammar belongs with the OLS extraction |
| 5. Primitive concepts | Canonical | Keep; do not repeat in general architecture |
| 6. Operators | Canonical | Keep OLS and non-OLS distinctions here |
| 7. Orientation records | Better moved elsewhere | Retain OLS `OP-RECORD` findings here; move general Record architecture to the machine-readable analysis |
| 8. Reference spaces | Canonical | Keep the detailed terminology archaeology here |
| 9. Relationship to ORION | Canonical | Keep the detailed correspondence and non-equivalence |
| 10. Relationship to NEXAHEDRON and ecosystem | Duplicate | Reduce to authority references; use the distilled responsibility table for overview |
| 11. External standards and models | Better moved elsewhere | Keep only OLS conceptual comparisons; carrier/media comparisons belong in the machine-readable analysis |
| 12. Repository map | Canonical | Keep as the archaeological navigation layer |
| 13. Missing components | Historical reference only | Preserve as a dated extraction gap list; do not treat it as a current roadmap |
| 14. Consolidated findings | Duplicate | Replace future overview use with this distilled review |
| Canonical extraction statement | Canonical | Keep as the extraction's own status boundary |

### 6.2 Machine-readable orientation architecture

| Section | Classification | Recommendation |
| --- | --- | --- |
| 1. Executive summary | Duplicate | Use this distilled review for the stable overview; retain the original as analysis context |
| 2. Method, evidence labels, and authority | Canonical | Keep the detailed evidence method and supplied-source status |
| 3. Existing assets and evidence | Canonical | Keep as the cross-repository evidence ledger |
| 4. Architectural problem | Duplicate | Compress to the seven-term architecture in future overview use |
| 5. Proposed layer model | Duplicate | Supersede editorially with the minimal diagram; retain for detailed derivation |
| 6. Responsibility matrix | Duplicate | Use this document's compressed responsibility table for overview; retain detailed distinctions as reference |
| 7. OLS Abstract Expression Model | Canonical | Keep as the analysis of this experimental requirement |
| 8. Concrete syntax and DSL options | Canonical | Keep carrier comparison outside the permanent overview |
| 9. Orientation Record architecture | Canonical | Keep the detailed bounded-record analysis |
| 10. Orientation Graph options | Canonical | Keep as the explicit rejection of a universal graph |
| 11. Processor contract | Canonical | Keep detailed capability and ORION-boundary analysis |
| 12. Representation Mapping Layer | Canonical | Keep detailed mapping responsibilities; call it a contract, not a core layer, in future prose |
| 13. UDF assessment | Historical reference only | Preserve as recovered technical lineage |
| 14. Historical format recommendation | Historical reference only | Preserve the bounded hypotheses and rejections; do not place names in overview architecture |
| 15. glTF / GLB integration | Better moved elsewhere | Future media-profile documentation, if adopted; otherwise retain as analysis |
| 16. Animation and audiovisual architecture | Better moved elsewhere | Future representation-profile documentation, if adopted |
| 17. Package and container architecture | Historical reference only | Retain as optional packaging analysis, not core architecture |
| 18. Security model | Better moved elsewhere | Security belongs with each parser, processor, package, renderer, and deployment contract |
| 19. Provenance, hashes, and signatures | Duplicate | Provenance is core Record responsibility; technical signing detail belongs with identity/package contracts |
| 20. Streaming and performance | Better moved elsewhere | Transport or runtime documentation only when required |
| 21. Domain translation contract | Canonical | Keep as the detailed safeguard against false cross-domain equivalence |
| 22. Repository ownership map | Canonical | Keep until governance adopts or rejects the proposed homes |
| 23. ADR and RFC recommendations | Historical reference only | Preserve as analysis history; maintain active decisions in ADR/RFC indexes |
| 24. Staged roadmap | Historical reference only | Move active work to roadmap documents; do not use as architecture |
| 25. Risks and rejected alternatives | Canonical | Keep detailed rejection evidence; summarize in “Things We Should Not Build (Yet)” |
| 26. Conclusions changed by added sources | Historical reference only | Preserve the archaeology correction |
| 27. Missing evidence | Historical reference only | Preserve as a dated gap assessment |
| 28. Open questions | Better moved elsewhere | Move still-active questions to the owning specification or decision record |
| 29. Explicit decision answers | Duplicate | Use this distilled review for stable architectural answers |
| 30. Architectural conclusion | Duplicate | Replace future overview use with the one-page architecture below |

### 6.3 Orientation infrastructure architecture review

| Section | Classification | Recommendation |
| --- | --- | --- |
| 1. Executive finding | Duplicate | Use this distilled review for the permanent overview |
| 2. Review method and evidence classes | Duplicate | Reference the machine-readable evidence method |
| 3. Definitions and terminology assessment | Canonical | Keep the detailed rejection and qualification of infrastructure terminology |
| 4. Reality–observation–orientation boundary | Canonical | Keep as the detailed source of the first two terms in the minimal diagram |
| 5. Minimal infrastructure layers | Duplicate | Supersede editorially with the seven-term diagram |
| 6. Infrastructure planes | Duplicate | Retain only as an optional review lens over the same core responsibilities |
| 7. Processor deployment model | Canonical | Keep the deployment-neutral processor analysis |
| 8. Request/result architecture | Better moved elsewhere | Detailed contracts belong with bounded Record/processor specifications if adopted |
| 9. Artifact/API/hybrid modes | Canonical | Keep the artifact-centered, deployment-neutral decision |
| 10. Distributed and federated considerations | Historical reference only | Retain as deferred analysis only |
| 11. Scientific-usefulness assessment | Canonical | Keep the measurable benefit and failure tests |
| 12. Domain case studies | Historical reference only | Retain as examples, not architecture |
| 13. AI participation boundary | Canonical | Keep until the same boundary is canonical elsewhere |
| 14. Failure and falsification analysis | Canonical | Keep as the strongest test against unnecessary abstraction |
| 15. Minimal prototype recommendation | Better moved elsewhere | Move active implementation work to an experiment record |
| 16. ADR and RFC implications | Historical reference only | Track live decisions in their indexes |
| 17. Accepted, narrowed, deferred, rejected claims | Duplicate | Consolidated by this review |
| 18. Final decision table | Canonical | Keep as the detailed disposition of the infrastructure hypothesis |
| 19. Final recommendation | Duplicate | Use this distilled review for the stable overview |

### 6.4 Minimum future documentation structure

The smallest sustainable structure is:

1. **This document** as the permanent informative architectural overview.
2. **Released OLS specifications** as the authority for orientation semantics.
3. **Certified ORION architecture and contracts** as the authority for ORION's
   bounded implementation.
4. **Owner-specific domain, Record, representation, security, and operational
   specifications** only where an implemented responsibility requires them.

The three source reviews should remain available as dated evidence and
reasoning records, but they need not all remain in the primary reading path:

- OLS extraction: detailed semantic archaeology and repository navigation;
- machine-readable architecture: detailed design-option and historical-format
  analysis;
- infrastructure review: falsification and terminology decision record.

Do not merge normative OLS or certified ORION material into an informative
overview. Consolidate navigation, not authority.

---

## 7. Part 6 — What actually remains to build?

Only one bounded experiment is necessary to validate the unimplemented bridge
described by the three documents.

| Work | Why necessary | Why it cannot yet be removed | Measurable success criterion |
| --- | --- | --- | --- |
| One small machine-readable OLS expression slice | Tests whether released semantics can survive a structured machine form without becoming a new semantic source | OLS has no adopted carrier-independent machine expression model or concrete carrier | One positive and several negative fixtures parse, validate, round-trip, and preserve the selected OLS meanings and prohibited implications |
| One declared local Processor over that slice | Tests the separation between semantics and bounded execution without requiring a service | ORION is a certified bounded processor but is not established as a full OLS processor or general reference implementation | The Processor accepts only its declared subset and emits visible unsupported or blocked outcomes for everything else |
| One immutable request-to-result Record chain | Tests identity, provenance, evidence, uncertainty, status, and STOP across processing | Existing bounded Records demonstrate the pattern, but cross-boundary exchange has not been validated for the proposed slice | Exact request, input, Processor, result, and supersession references reproduce the same declared result level without hidden state |
| One provenance-preserving static Representation | Tests that a result can become inspectable without transferring authority to the view | Representation mapping is well documented but not demonstrated for the proposed OLS slice | Every represented claim traces to its source Record; declared loss remains visible; changing the view does not change the result |
| One independent replay and Human trace test | Tests whether the chain improves inspection rather than adding documentation overhead | A single implementation run cannot establish interchange or practical accountability | A clean implementation reproduces the declared artifacts, and a Human reviewer can trace a selected representation element to source, evidence, uncertainty, and Processor status |

These items form one experiment, not five products. They require no platform,
network, registry, package format, custom extension, production API, or change
to OLS 1.0 or ORION Version 1.

---

## 8. Part 7 — Things We Should Not Build (Yet)

The existing reviews reject or defer the following:

- a universal orientation protocol;
- an Orientation Infrastructure platform;
- an Orientation Operating System, Orientation Web, or general Orientation
  Computing claim;
- a mandatory API or API-first architecture;
- a mandatory network service or distributed deployment;
- one service or microservice per OLS operator;
- a central mandatory Processor registry;
- one universal Orientation Graph;
- one universal Orientation Record;
- one universal OLS file format or mandatory DSL;
- a universal RDF or knowledge-graph authority;
- a mandatory package or container;
- a broad revived UDF container/runtime/media format;
- UBF or USF as reserved formats;
- `.nxa`, `.xva`, or `.scarab` as established file formats;
- a new format where an existing carrier or representation standard suffices;
- a claim that ORION is the full OLS interpreter or reference implementation;
- normative OLS schemas owned by ORION;
- one architecture forced across all domain evidence and validation methods;
- automatic promotion of analogy into equivalence;
- executable scripts, shaders, network access, or filesystem access enabled by
  default in representations;
- AI as OLS, scientific, Kernel, approval, or Human decision authority;
- a representation treated as evidence or truth merely because it is valid,
  deterministic, signed, attractive, or reproducible;
- production federation, streaming, discovery, trust, or negotiation protocols
  without a demonstrated interoperability requirement.

“Yet” means that a concrete need and governing owner would be required before
reconsideration. It does not imply that every item should eventually be built.

---

## 9. Part 8 — One-page architecture

NEXAH preserves a disciplined path from situated observation to Human
orientation. OLS defines the semantics used along that path; bounded Processors
may produce accountable Records; Representations make those Records
inspectable without replacing their sources. Domain validity remains with
domain authorities, and intention, interpretation, continuation, approval, and
decision remain with the Human.

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

1. Reality remains outside the formal system and is approached only through situated observation.
2. Domains own their sources, evidence criteria, and claims of scientific or factual validity.
3. OLS owns orientation semantics but not execution, domain truth, or Human meaning.
4. Processors act only within declared boundaries and stop visibly when those boundaries are not met.
5. Identity, provenance, evidence, uncertainty, status, and correction history remain inspectable.
6. Difference, disagreement, missing information, and unsupported claims must not be silently erased.
7. Representations declare their source and loss and never become authority over what they represent.
8. Encoding, storage, transport, invocation, and presentation do not transfer semantic or decision authority.
9. Every claim is limited to its declared scope and validation.
10. The Human owns intention, interpretation, continuation, approval, and consequential decision.

| Responsibility | Owner | Boundary |
| --- | --- | --- |
| Reality | No software owner | The subject is not the model |
| Observation | Source or domain owner | Evidence and validity remain situated |
| Semantics | OLS governance | Meaning is separate from execution |
| Processing | Named Processor owner | Behavior is bounded and may STOP |
| Preservation | Named Record owner | Identity, evidence, uncertainty, and history remain visible |
| Representation | Source, mapping, and representation owners | A view never replaces its source |
| Interpretation and decision | Human | Consequential authority remains Human |
