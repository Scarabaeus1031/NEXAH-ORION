# NEXAH Orientation Infrastructure Architecture Review

> **Status:** Informative architecture review — no normative effect
>
> **Review date:** 2026-07-25
>
> **Baseline:** `MACHINE_READABLE_ORIENTATION_ARCHITECTURE.md`, released OLS
> 1.0 semantics, certified ORION Version 1 boundaries, and separately governed
> ORION Runtime API 1.0 evidence
>
> **Constraint:** This review does not amend OLS 1.0, reopen ORION Version 1, or
> establish a protocol, platform, service, schema, package, registry, media type,
> file extension, or scientific claim.

---

## 1. Executive finding

The repository supports a **bounded orientation interoperability
architecture**. It contains several of the responsibilities normally required
for infrastructure:

- released semantic contracts;
- a certified deterministic processor with explicit STOP boundaries;
- immutable requests, reports, manifests, artifacts, identities, and
  provenance;
- separation of semantics, execution, transport, representation, application,
  and Human authority;
- processor-like capability inventories and operational isolation;
- multiple producers, consumers, representations, and domain applications;
- validation and conformance practices.

It does **not** yet support the stronger claim that a general Orientation
Infrastructure has been implemented. Missing elements include a governed OLS
Abstract Expression Model, interchangeable carrier conformance, a
cross-processor capability contract, two independent conforming processors,
cross-system record interoperability, and demonstrated scientific value across
domains.

The term **Orientation Infrastructure** is therefore justified only as a
**provisional architecture hypothesis**:

> A set of separable semantic, artifact, processor, evidence, representation,
> transport, governance, and Human-interface contracts that permit bounded
> orientation work to be inspected, reproduced, substituted, and continued
> without transferring authority between layers.

This is narrower than a platform, operating system, universal protocol, or new
computing paradigm. It is broader than serialization only if independent
processors and applications can actually exchange governed artifacts without
semantic drift.

The recommended architecture is **artifact-centered, deployment-neutral, and
hybrid-capable**:

```text
domain source or Human question
  ↓
domain-owned observation / Human-owned intention
  ↓
immutable request and referenced source artifacts
  ↓
declared, bounded processor
  ↓
immutable result, evidence, provenance, and validation artifacts
  ↓
explicit representation mapping
  ↓
native representation
  ↓
Human Workspace
  ↓
Human interpretation, continuation, approval, decision, or stop
```

Files, local libraries, command-line tools, isolated workers, and services are
deployment choices. A processor contract must not require a network.

The smallest useful test does not require a platform. It requires a clearer
request/result envelope around the existing Stage 1 carrier experiment:

```text
immutable Orientation Request artifact
  → capability validation
  → one bounded local processor
  → immutable Orientation Result artifact
  → provenance-preserving SVG mapping
  → Human inspection
```

---

## 2. Review method and evidence classes

Repository evidence takes precedence over the hypothesis. This review labels
claims as follows:

| Label | Meaning |
| --- | --- |
| **Repository evidence** | A released, frozen, accepted, implemented, or documented repository artifact supports the statement in its declared scope |
| **Architectural inference** | Several existing responsibilities form a coherent pattern, but no governing document has adopted the combined model |
| **Analogy** | An established architecture category helps explain one aspect without establishing equivalence |
| **Proposal** | A testable next step requiring governance before normative use |
| **Unsupported** | The repository does not currently establish the claim |

Absence from the current repository is not proof that a design never existed.
Historical technical design, released specification, certified implementation,
and current repository integration remain separate statuses.

### 2.1 Evidence and authority table

| Evidence | Status and owner | Supports | Does not support |
| --- | --- | --- | --- |
| Released OLS 1.0 suite, summarized in [`OLS_1_0_REPOSITORY_ARCHITECTURE_EXTRACTION.md`](OLS_1_0_REPOSITORY_ARCHITECTURE_EXTRACTION.md) | Normative OLS semantic authority | Shared semantics, declarations, primitive contracts, profiles, semantic products, conformance and evolution | Transport, execution topology, storage, service interfaces, domain truth, or one normative serialization |
| [`MACHINE_READABLE_ORIENTATION_ARCHITECTURE.md`](MACHINE_READABLE_ORIENTATION_ARCHITECTURE.md) | Informative cross-repository analysis | Separation of semantics, abstract model, carriers, processors, records, mappings, media, packages and Workspaces | Adoption of any proposed contract |
| [`ORION_V1_ARCHITECTURE_FREEZE.md`](ORION_V1_ARCHITECTURE_FREEZE.md) and current release baseline | Frozen/certified ORION authority | One bounded deterministic processor, exact ownership, immutable artifacts, STOP conditions and Human boundary | Full OLS implementation or general processor model |
| [`ORIENTATION_REQUEST.md`](contracts/ORIENTATION_REQUEST.md) | Frozen ORION public contract | Human intention, scope, authority, exact object references, versioning and transport independence | A universal ecosystem request or a network endpoint |
| [`ORIENTATION_REPORT.md`](contracts/ORIENTATION_REPORT.md) | Frozen ORION public contract | Immutable result lineage, complete/partial/blocked status, evidence, uncertainty, validation and continuation | Domain truth, Human meaning, or one universal Orientation Record |
| [`ORION_AUTHORITY_MATRIX.md`](runtime/ORION_AUTHORITY_MATRIX.md) | Frozen Runtime API 1.0 responsibility evidence | Exact separation among Human Workspace, NEXAHEDRON, Gateway, Runtime, Adapter and frozen Core | Transfer of these exact deployment components to every processor |
| [`ORION_OPERATIONAL_BOUNDARY.md`](runtime/ORION_OPERATIONAL_BOUNDARY.md) | Frozen Runtime API 1.0 operational evidence, outside Core semantics | Isolated no-network workers, resource limits, startup identity checks and operational errors | A requirement that all processors be network services |
| [`ORIENTATION_TRANSFORM_STACK.md`](transformations/ORIENTATION_TRANSFORM_STACK.md) and transition contracts | Accepted ORION architecture in bounded scope | Explicit mappings, invariants, evidence, loss, blockers and prohibited implications | Executable mathematics for every transition or universal domain translation |
| Context, identity, artifact-manifest and confirmation contracts | Accepted or frozen within named ORION scopes | Immutable source selection, canonical identity, exact artifacts and replay boundaries | Scientific correctness or universal schemas |
| NEXAH IEEE, JANUS, Atlas, Library, Living Concepts and orientation records cited by the baseline analysis | Domain, research, curatorial and editorial evidence | Multiple domain owners, record types, validation methods, representations and consumers | Equivalence among domain meanings |
| Historical UDF design reviewed in the baseline | Concrete but unreleased historical design | A prior attempt at declarative scenes, players, controls, provenance and delivery | A current universal format or infrastructure layer |

### 2.2 Evidence threshold for the infrastructure term

The term becomes more than a hypothesis only when all of the following have
evidence:

1. one governed semantic baseline and one carrier-independent expression model;
2. at least two independently implemented processors with capability
   declarations;
3. at least two independently implemented consumers;
4. immutable request/result exchange across implementation boundaries;
5. visible compatibility, partial-result, STOP, provenance, uncertainty and
   loss behavior;
6. offline replay of at least one complete chain;
7. measurable value in more than one domain;
8. no transfer of semantic, scientific, or Human authority through transport.

The repository is strong on items 4–5 inside ORION, partial on 1 and 6, and has
not yet demonstrated 2, 3, or 7 at ecosystem scale.

---

## 3. Definitions and terminology assessment

### 3.1 Architectural category analogies

| Category | Useful analogy | Limit |
| --- | --- | --- |
| Protocol stack | Separate semantic, carrier, processing, representation and transport concerns | No shared wire protocol or negotiated network stack is established |
| Intermediate-representation ecosystem | A carrier-independent expression can feed multiple processors and targets | OLS is richer than an execution IR and includes Human and authority boundaries |
| Service-oriented architecture | Capabilities can be invoked behind stable contracts | Deployment may remain local; operator names are not service boundaries |
| Event-driven architecture | Observations, corrections and retractions may form append-only streams | Most orientation work is artifact- and request-centered, not necessarily event-driven |
| Data infrastructure | Identity, provenance, immutable artifacts, schemas and validation are central | Orientation includes semantic operations, representation loss and Human interpretation |
| Compiler/toolchain architecture | Source semantics, intermediate model, processors, diagnostics and target representations are separable | Orientation is not compilation; results may be partial, uncertain, nondeterministic and Human-interpreted |
| Scientific workflow infrastructure | Frozen inputs, methods, outputs, provenance and replay are first-class | Software replay cannot establish empirical or clinical validity |
| Knowledge-representation infrastructure | Shared identifiers, relations, evidence and graph views support exchange | OLS is not established as a universal ontology or canonical knowledge graph |

No single analogy is sufficient. The closest composite is a scientific
artifact workflow with language and toolchain characteristics.

### 3.2 OLS statement assessment

| Statement | Classification | Finding |
| --- | --- | --- |
| “OLS owns meaning.” | **Narrowed / directly supported** | OLS owns released orientation semantics, not all domain meaning, Human meaning, or truth |
| “OLS is an Orientation Intermediate Representation.” | **Useful analogy, incomplete** | A future OLS Abstract Expression Model could act as a semantic IR; OLS 1.0 itself is a specification suite, not an IR artifact |
| “OLS is a shared protocol language.” | **Misleading now** | OLS can govern meanings exchanged through protocols, but it defines no transport, endpoint, negotiation or wire protocol |
| “OLS is a domain-independent orientation language.” | **Directly supported with boundary** | Universal concepts and operators are domain-independent; profiles and domain validation remain owned by their domains |
| “OLS is infrastructure.” | **Rejected literally** | A language specification may be a foundation of infrastructure, but it does not execute, store, transport, discover or render |

Required distinctions:

```text
OLS semantic specification
  ≠ proposed OLS Abstract Expression Model
  ≠ concrete carrier
  ≠ processor input/output contract
  ≠ durable record
  ≠ service/API contract
```

### 3.3 Terminology

| Term | Current recommendation | Reason |
| --- | --- | --- |
| Language | **Use** for OLS | Released semantic specification exists |
| Specification | **Use** for governed contracts in their scopes | Repository already distinguishes normative and informative documents |
| Architecture | **Use** | Responsibilities and boundaries are documented |
| Infrastructure | **Use only as a provisional architecture hypothesis** | Components exist, but independent ecosystem interoperability is not demonstrated |
| Stack | **Use carefully as a diagrammatic analogy** | Planes cross layers and storage/transport remain orthogonal |
| Protocol | **Avoid for the whole architecture** | No universal interaction or wire protocol exists |
| Framework | **Use only for the existing NEXAH Framework** | It names an implementation/governance scope, not the whole ecosystem |
| Ecosystem | **Use** | Multiple repositories, owners, applications and artifacts exist |
| Runtime | **Use only for an execution environment** | ORION Runtime is separately owned and does not define semantics |
| Platform | **Defer** | No integrated developer/user product with stable cross-processor APIs exists |
| Orientation Computing | **Defer** | A research programme may test it; current evidence does not establish a distinct computing model |
| Orientation Operating System | **Reject** | Misstates resource, process and authority ownership |
| Orientation Web | **Reject now** | No federated protocol, discovery system or trust model exists |

---

## 4. Reality–observation–orientation boundary

### 4.1 Corrected sequence

Reality is outside the formal architecture. The system has access only to
interactions, measurements, testimony, documents, selections and records.

```text
reality or subject matter
  ↓  interaction under a domain method
signal, testimony, document, event, or other source material
  ↓  selection + framing + observer/instrument + provenance
observation claim or measurement record
  ↓  domain validation and evidence-status assignment
OLS-governed semantic expression about the observation
  ↓  bounded processing
derived records and representations
  ↓
Human inspection and interpretation
```

No arrow grants direct access to reality. Every formal chain begins after a
source interaction and must preserve the conditions under which it occurred.

### 4.2 Boundary distinctions

| Concern | Owner | What it may assert | What it may not assert |
| --- | --- | --- | --- |
| Reality / subject matter | Outside software ownership | Nothing through software alone | That a model or record is the subject itself |
| Measurement | Domain instrument/method owner | A quantity was produced under a stated calibration, unit and method | That the quantity is correctly interpreted |
| Sensor observation | Domain acquisition system and source owner | A device emitted a reading/event at a stated time and configuration | Human testimony, causal explanation, or general truth |
| Human testimony | Human/source authority plus recorder | A person stated or reported something under stated conditions | Instrumental measurement or independently validated fact |
| Primary observation | Domain observer/acquisition owner | A direct observation claim linked to source interaction | Freedom from selection, framing, error or uncertainty |
| Derived observation | Named derivation owner | A result was computed from identified prior observations | Primary status or independent evidence |
| OLS expression | OLS-governed author/processor | Concepts, relations, status and operator products conform to declared semantics | That the source event occurred or is scientifically valid |
| Validation | Contract or domain validator | Declared criteria passed or failed in a stated scope | Universal truth or Human approval |
| Interpretation | Domain expert or Human | A meaning or judgment under stated authority | Silent promotion into source evidence |

### 4.3 Observation is not one thing

“Observation” spans at least four responsibilities:

1. the domain event or act of observing;
2. the immutable input/evidence record describing that act;
3. the OLS semantic product created by `OBSERVE`;
4. an ORION or application-specific inspection stage.

These may be linked but must not be collapsed. Observation therefore does not
belong wholly inside or outside OLS:

- the source act, instrument, testimony and scientific acceptance are
  domain-owned;
- OLS owns the semantics and prohibited implications of an observation product;
- a carrier encodes it;
- a bounded record preserves its occurrence claim and provenance;
- a validator checks only its declared criteria.

Uncertainty first enters no later than source acquisition and selection. It may
also be introduced by parsing, mapping, inference, processing and rendering.
Evidence status should be assigned by the authority responsible for the
evidence class, never inferred merely from successful OLS conformance.

---

## 5. Minimal infrastructure layers

Layers are retained only where they have a distinct input, output, authority or
failure boundary.

| Layer | Owner | Input | Output | Authority | Validation | Failure mode | Prohibited implication | Required? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Domain / Reality Interface | Domain source, instrument, researcher or Human | Interaction with subject/source | Signal, testimony, document or event | Acquisition method and source identity | Calibration, collection protocol, source review | Unavailable, biased, corrupted, uncalibrated | Direct or complete access to reality | Required as an external boundary |
| Observation and Evidence | Domain/evidence owner | Source material and method | Observation/evidence record | Occurrence claim, evidence class and uncertainty | Domain criteria and provenance checks | Unsupported, disputed, missing provenance | OLS conformance equals empirical validity | Required when claims depend on evidence |
| OLS Semantics | OLS governance | Declared concepts and products | Meaning and legal semantic composition | Orientation semantics only | OLS conformance | Undefined, incompatible, prohibited implication | Domain truth, execution or decision | Required for an OLS claim |
| Abstract Expression | Future OLS governance | OLS semantic construction | Carrier-independent expression | Structural realization of released semantics | Model invariants and semantic mapping | Unmapped or lossy construction | New semantics by convenience | Proposed, not currently available |
| Carrier | Carrier-profile owner | Abstract expression or bounded record | Bytes/text | Encoding only | Parse/schema/canonicalization tests | Invalid, ambiguous, unsupported version | Carrier is the semantic model | Optional choice; some carrier is operationally necessary |
| Processor Capability | Processor owner under ecosystem contract | Processor declaration | Supported subset and limits | Capability claim only | Declaration/conformance fixtures | Missing, incompatible, false claim | Permission, trust or scientific authority | Required for substitution; proposed generally |
| Execution | Implementation/runtime owner | Validated inputs and capability match | Attempt outcome and operational trace | Bounded computation | Unit, conformance, isolation and resource tests | Invalid, blocked, timeout, exhausted, internal failure | Operational success is semantic/scientific success | Required when processing occurs |
| Bounded Records | Record-class owner | Request, process product or result | Immutable/superseding record | Named record responsibility | Contract and lineage validation | Invalid, partial, blocked, superseded, withdrawn | One universal record or final truth | Required where accountability/replay is claimed |
| Provenance and Validation | Source, processor, validator and governance owners | Identities, artifacts, criteria | Lineage and scoped validation results | Derivation and test claims | Digest, method and criteria checks | Gap, mismatch, unknown, invalid | Signature/hash/test equals truth | Required for accountable claims |
| Representation Mapping | Mapping/profile owner | Semantic/record source | Mapping record and target parameters | Declared transformation, invariants and loss | Mapping fixtures and source/output trace | Unsupported, lossy, invalid, inaccessible | Representation becomes source authority | Optional unless a new representation is produced |
| Native Media | External standard/profile owner | Mapping output | SVG, GLB, Markdown, audio, table or other artifact | Media structure only | Native validator | Invalid or unsupported media | Native rendering conveys complete semantics | Optional |
| Renderer / Player | Implementation owner | Native media and capability policy | Observed display/audio/interaction | Rendering behavior | Renderer tests and bounded environment | Unsupported, nondeterministic, unsafe | Rendered perception is deterministic truth | Optional |
| Workspace / Application | Application owner | Records and representations | Interaction, inspection and continuation | Presentation and application workflow | UX, accessibility and domain tests | Misleading, inaccessible, stale, unavailable | Application owns OLS/domain truth | Optional but required for Human-facing use |
| Human Interpretation and Decision | Human | Presented sources, records, evidence and context | Interpretation, continuation, approval, decision or stop | Consequential meaning and decision | Human/domain governance | Misunderstanding, disagreement, deferral | Autonomous system owns Human authority | Required for consequential closure; outside autonomous processing |

Transport and governance are not additional serial stages. They cross all
layers and are clearer as planes.

---

## 6. Infrastructure planes

The plane view improves the architecture because several concerns apply across
the entire chain rather than occurring once.

| Plane | Contains | Why distinct | Risk if collapsed |
| --- | --- | --- | --- |
| Semantic | OLS concepts, declarations, profiles, operators and products | Governs meaning independently of bytes and deployment | Implementations silently redefine semantics |
| Execution | Capabilities, plans, processing, resources, STOP and operational outcomes | Governs what a processor does under limits | Network/runtime success is confused with valid orientation |
| Evidence | Sources, observations, provenance, uncertainty, validation, corrections and retractions | Tracks why a claim may be considered and how it changes | Derived claims overwrite or impersonate evidence |
| Representation | Mappings, projections, media, renderers and loss | Governs how sources become perceivable forms | Attractive outputs become authoritative |
| Transport | Files, APIs, streams, queues and content-addressed exchange | Moves artifacts without changing their meaning | API or package semantics leak into source contracts |
| Governance | Ownership, versions, compatibility, conformance, signatures, certification and approval | Determines who may define and attest what | Technical components acquire authority by implementation |
| Human | Question, intention, confirmation, interpretation, reflection, continuation and decision | Preserves the non-automated authority boundary | “Human in the loop” becomes a decorative final click |

Planes are not a second implementation hierarchy. They are review lenses. An
Orientation Result, for example, has semantic fields, execution status,
evidence lineage, representation references, transport encodings, governed
versions and a Human-use boundary.

---

## 7. Processor deployment model

### 7.1 Processor contract versus deployment

A processor is a bounded implementation that accepts declared input classes,
performs declared behavior, and emits declared outcomes under a capability and
authority contract. It may be deployed as:

| Deployment | Legitimate use | Principal concern |
| --- | --- | --- |
| Local library | Embedded deterministic processing and tests | Dependency/version isolation |
| Command-line tool | Git, batch, offline and scientific workflows | Stable exit/outcome and artifact discipline |
| Deterministic worker | Isolated bounded execution | Resource and environment identity |
| Isolated process | Untrusted inputs or renderer/parser separation | IPC and lifecycle complexity |
| Network service | Shared capacity and remote application access | Authentication, latency, availability and authority confusion |
| Event consumer | Continuous observation streams | Ordering, correction, replay and back-pressure |
| Browser worker | Local inspection or bounded rendering | browser variability and capability sandboxing |
| Embedded system | Sensor-adjacent, low-resource work | constrained profiles and intermittent connectivity |

Several profiles can share one processor contract. Conformance must describe
semantic and artifact behavior separately from HTTP, queue, CLI or library
bindings.

### 7.2 Are operators services?

No. `OBSERVE`, `REPRESENT`, `COMPARE`, `ORIENT`, and `EXPLAIN` are semantic
responsibilities, not deployment units. “Observe Service” or “Compare Service”
is legitimate only when an independently owned, independently scalable and
cohesive capability has:

- a stable input/output contract;
- a distinct security and resource boundary;
- a real independent consumer;
- observable value from separate deployment;
- no hidden shared transaction or semantic state.

Creating one service per operator would introduce:

- five or more version-negotiation boundaries;
- latency and partial-failure paths between semantic stages;
- fragmented provenance and canonicalization;
- pressure to serialize internal intermediate state;
- duplicated authorization and observability;
- ambiguous ownership of STOP and correction.

The default should be a coarse bounded processor that may internally execute
several operators. `Validate`, `Translate`, and `Render` may be separate
components because their authorities and security surfaces differ, not because
their names sound like verbs.

---

## 8. Request/result architecture

### 8.1 General contract

```text
Orientation Request
  → capability and compatibility validation
  → accepted processing attempt
  → Orientation Result | Blocker | Unsupported | Invalid | Operational Error
```

This is an architectural pattern, not a new universal schema. Existing frozen
ORION contracts remain unchanged.

| Concern | Request | Processor declaration | Result | Separate record |
| --- | --- | --- | --- | --- |
| Identity/version | Request lineage | Processor/version/profile | Result lineage and request reference | Registry only if later justified |
| Human intention | Exact Human-owned statement/reference | Must not redefine | Exact preserved reference | Approval/decision record remains separate |
| Scope and constraints | Included, excluded, unresolved | Supported bounds | Applied scope and deviations | Clarification lineage when needed |
| Input | Immutable expression/record/artifact references or bounded inline content | Accepted classes/carriers | Exact consumed identities | Source and evidence records |
| Capabilities | Requirements only | Supported semantics, determinism, resources, outputs, STOP | Actual matched capability/version | Certification report |
| Evidence policy | Requested policy/reference | Supported policy | Evidence used, missing and disputed | Evidence records remain separately owned |
| Status | No predicted answer | Declared possible outcomes | Complete, partial, blocked or other contract outcome | Runtime error when no valid semantic result exists |
| Provenance | Source references | Processor identity/dependencies | Derivation links and digests | Detailed provenance/manifest may be separate |
| Validation | Requested criteria | Available validators | Scoped validation result refs | Domain validation and approval stay separate |
| Continuation | Prior lineage and allowed Human scope | Supported continuation mechanism | Options, blockers and STOP reason | Human selection is a later request/decision |

A request may reference immutable OLS expressions rather than contain them.
References must bind exact version, integrity and access expectations. Human
intention is preserved as an authority-scoped statement; it is neither a
prediction nor semantic truth.

Deterministic processors declare frozen dependencies and replay level.
Nondeterministic processors declare source of nondeterminism, seed/model/provider
identity where available, repeatability limits and result status. Asynchronous
execution adds an attempt/status resource but must not mutate an issued result.
Event streams append observations and corrections; they do not replace request
identity or silently rewrite source records.

### 8.2 Non-normative minimal example

The following illustrates an envelope for the prototype only. Field names are
not reserved.

```json
{
  "kind": "orientation-request-example",
  "version": "proposal-0",
  "request_id": "req-local-001",
  "human_intention": {
    "statement": "Inspect the declared difference between two source records.",
    "authority_ref": "human-session-local"
  },
  "scope": {
    "include": ["difference", "evidence", "uncertainty"],
    "exclude": ["recommendation", "action"],
    "unresolved": []
  },
  "input_refs": [
    {
      "id": "record-a",
      "version": "1",
      "path": "inputs/record-a.json",
      "sha256": "<example-digest-a>"
    },
    {
      "id": "record-b",
      "version": "1",
      "path": "inputs/record-b.json",
      "sha256": "<example-digest-b>"
    }
  ],
  "processor_requirements": {
    "operation": "bounded-comparison",
    "offline": true,
    "deterministic_result": true,
    "required_output": "orientation-result-example"
  },
  "effects": "none"
}
```

```json
{
  "kind": "orientation-result-example",
  "version": "proposal-0",
  "result_id": "result-local-001",
  "request_ref": "req-local-001",
  "status": "partial",
  "processor": {
    "id": "local-comparison-prototype",
    "version": "0",
    "capability_match": "accepted"
  },
  "findings": [
    {
      "status": "supported-within-inputs",
      "statement": "The records declare different boundary values.",
      "evidence_refs": ["record-a", "record-b"]
    }
  ],
  "uncertainties": [
    "No domain validator established whether the boundary values are accurate."
  ],
  "prohibited_implications": [
    "preference",
    "recommendation",
    "domain-validity"
  ],
  "representation_refs": ["difference-view.svg"],
  "continuation": {
    "status": "human-selection-required"
  }
}
```

The example deliberately keeps validation, approval and source evidence as
references rather than pretending that one result owns them.

---

## 9. Artifact-first, API-first, and hybrid modes

| Criterion | Artifact-first | API-first | Hybrid: API references/returns immutable artifacts |
| --- | --- | --- | --- |
| Reproducibility | Strong when inputs/outputs are frozen | Weak unless every body and dependency is retained | Strong if identities and bytes are durable |
| Offline operation | Native | Usually poor | Supported when the same processor has local binding |
| Scientific audit | Git/digest friendly | Requires capture infrastructure | Strong with artifact manifests and attempt records |
| Deterministic replay | Natural | Possible but environment-sensitive | Strong when execution profile is frozen |
| Streaming | Awkward for live/large inputs | Natural | Natural transport with artifact checkpoints |
| Security | Small offline surface | Authentication/network exposure | More components, but bounded artifact intake is possible |
| Caching | Content-addressed | Often endpoint/key specific | Content identity can govern cache safely |
| Versioning | Visible files and schemas | API and server version coupling | Artifact and API versions remain separate |
| Long-term preservation | Strong | Poor if service disappears | Strong if APIs are dispensable |
| Git workflows | Native | Indirect | Native for artifacts |
| Distributed operation | Transfer is explicit | Natural | Natural without making service state authoritative |
| Human inspection | Direct | Requires client tooling | Direct artifacts plus convenient client |
| Low-resource/embedded | Good with narrow files/tools | Network may be unavailable | Local profile remains possible |

**Recommendation:** NEXAH should be **deployment-neutral but
artifact-centered**, with a hybrid interaction profile where remote invocation
is useful. “Hybrid” is supported as a mode, not a mandate that every deployment
provide an API.

The durable contract is:

```text
immutable input identities
  → declared processor identity and capability
  → immutable result identities
```

An API returns status, identities and links or bounded inline artifacts. It
does not become the sole location of orientation knowledge.

---

## 10. Distributed and federated considerations

Multiple independent processors could interoperate without one central runtime
if they share governed artifact and capability contracts. This remains a
proposal until independent implementations exist.

| Question | Minimal answer | Deferred production concern |
| --- | --- | --- |
| Processor identity | Stable owner-scoped ID, version and artifact digest | Global naming and legal identity |
| Capability discovery | Signed or digest-bound declaration obtained directly, from a package, or by configuration | Search, ranking and availability registry |
| OLS release mismatch | Exact supported releases; stop on incompatible major semantics | Automated translation among releases |
| Profile negotiation | Request requirements intersect declared support; missing required capability stops | Rich preference/optimization negotiation |
| Cross-system records | Stable URI/owner ID plus exact version and digest | Global resolver |
| Chained provenance | Each result references exact inputs, processor and prior result | Cross-organizational privacy and retention |
| Partial-result composition | Preserve each status and prohibited implication; do not upgrade completeness | General composition algebra |
| Malicious processors | Isolation, allowlists, independent validation and no authority transfer | Reputation and revocation network |
| Trust versus authority | Trust policy decides whose claim is accepted; semantic authority remains with the named owner | Federated trust governance |
| Caching | Key by input, processor, capability, dependency and result-profile identities | Distributed invalidation |
| Offline operation | Capability manifests and artifacts may be preloaded | Synchronization after reconnection |

A central registry is **not required** for the first architecture. It may later
be useful as an optional directory, but it would be neither semantic authority
nor a single point through which local processing must pass. A production
network protocol is unjustified until two real processors need remote
interoperation.

---

## 11. Scientific-usefulness assessment

| Claimed benefit | Required architecture | Smallest demonstration | Success criterion | Failure condition / overclaim risk |
| --- | --- | --- | --- | --- |
| Reproducible evidence-to-representation path | Immutable sources, processor/mapping identity, provenance and validation | One frozen dataset to result and SVG, replayed independently | Same declared replay level and complete trace | Same picture is mistaken for same science |
| Representation independence | Semantic/record source separated from mapping and media | One source rendered as table and SVG | Both preserve declared invariants and expose different loss | “Multiple views” hide incompatible assumptions |
| Transparent uncertainty and loss | Typed uncertainty plus mapping loss contract | Render known, unknown and disputed states | Human can locate source uncertainty and representation loss | Visual convention implies confidence not present in source |
| Cross-domain structural comparison | Domain translation contracts and analogy/equivalence labels | Compare one IEEE topology with one non-power topology | Shared structure and prohibited implications are explicit | Structural similarity is promoted to causal/domain equivalence |
| Processor substitution | Capability contract and conformance fixtures | Two processors consume the same immutable request | Comparable status, identity and diagnostics within claimed subset | Outputs differ without visible capability/version cause |
| Reusable validation | Separation of carrier, semantic, processor and domain validators | Run each validator independently on one artifact chain | Each reports only its scope | Passing schema validation is called scientific validity |
| Machine-assisted review | Evidence-linked candidate records and Human Workspace | AI proposes findings; deterministic checks and Human review follow | Reviewer traces every claim and rejects/edits without source loss | Automation bias or hidden unsupported claims |
| Traceable AI outputs | Model/provider identity, inputs, candidate status and validation records | One extraction task with cited source spans | Every accepted field has source trace and reviewer status | Fluent explanation launders uncertain extraction |
| Durable scientific records | Immutable/superseding records and content identity | Correct one observation without deleting the old version | Both versions and derivation impact remain inspectable | Immutability blocks legitimate correction or violates privacy |
| Multiple representations from one source | Mapping contracts and native media | Table, SVG and narrative from one result record | Each links to the same source and declares loss | Presentation becomes a competing source of truth |
| Explicit observation/inference/decision separation | Status model and Human authority boundary | One workflow containing all three | UI and records never merge statuses | Extra bureaucracy with no change in reviewer behavior |

Scientific value is not established by architecture elegance. The hypothesis
fails scientifically if these demonstrations add cost without improving
traceability, error detection, reproducibility, substitution or Human review.

---

## 12. Domain case studies

### 12.1 IEEE power-system analysis

```text
versioned IEEE case + solver configuration
  → measured or simulated bus/branch observations
  → domain-owned quantities, units, topology and evidence status
  → bounded power-system processor
  → immutable result/validation records
  → geometry or network mapping
  → table + SVG/network view
  → engineer inspection and decision
```

Generic components: identity, request scope, processor declaration, immutable
lineage, status, uncertainty, mapping loss, representation references and
Human authority.

Domain-owned components: electrical quantities, per-unit conventions, solver
method, contingency model, physical validity, tolerances and engineering
approval. A generic orientation layer may preserve these but cannot validate
them.

### 12.2 Biological or medical observation

```text
sample, image, assay, instrument output, or clinical testimony
  → acquisition/observation record with consent and method
  → domain terminology and uncertainty
  → bounded extraction/comparison processor
  → candidate findings and validation references
  → annotated image/table/explanation
  → qualified Human review and clinical/research decision
```

Generic components: source identity, provenance gaps, candidate status,
processor limits, evidence links, corrections and representation trace.

Domain-owned components: consent, privacy, specimen/patient identity, clinical
meaning, diagnostic thresholds, bias assessment, biological validity and
medical decision. An OLS-conforming expression cannot become a diagnosis.

### 12.3 AI-supported research review

```text
Human question + frozen paper corpus
  → source-selection/context manifest
  → evidence excerpts and candidate OLS expressions
  → AI proposing processor
  → deterministic citation/schema/status checks
  → bounded review record
  → evidence matrix + narrative projection
  → Human scholarly interpretation and decision
```

Generic components: immutable request, corpus identity, candidate status,
capability declaration, evidence references, validation, uncertainty and
supersession.

Domain-owned components: methodological quality, disciplinary standards,
interpretation, novelty, consensus and publication decision. Citation presence
does not validate the cited claim.

### 12.4 Cultural, historical, or Atlas interpretation

```text
Work, Edition, archive item, testimony, or curated collection
  → source/occurrence and curatorial record
  → perspective- and context-declared semantic expression
  → bounded relation/navigation processor
  → parallel interpretation records
  → Atlas map, timeline, image or reading path
  → Human interpretation and editorial decision
```

Generic components: stable references, provenance, multiple perspectives,
disagreement preservation, mappings, representation loss and continuation.

Domain-owned components: Work/Edition identity, cultural context, source
criticism, community authority, rights, curatorial framing and editorial
publication. Parallel interpretations must not be averaged into false
consensus.

Across all four cases, shared structure supports interoperability of records
and review—not equivalence of power flow, biology, scholarship and culture.

---

## 13. AI participation boundary

An AI model may participate as a **bounded proposing processor**. It may:

- extract candidate observations from identified sources;
- propose candidate semantic expressions;
- compare declared structures;
- propose explanations;
- identify possible gaps and continuations.

It may not become:

- OLS semantic authority;
- source or domain evidence authority;
- deterministic validator merely because it is repeatable;
- ORION Core or Kernel authority;
- Human approval or decision authority.

The governing rule remains:

> The model proposes. The Orchestrator validates. The Kernel decides.

For the broader architecture:

| Role | Responsibility |
| --- | --- |
| Model | Produces explicitly untrusted or candidate outputs under a declared model/provider/version context |
| Orchestrator | Selects inputs, enforces contracts, validates boundaries, preserves provenance and stops on unsupported conditions |
| Kernel | Makes only the canonical decisions assigned to its frozen deterministic authority |
| ORION | Executes and certifies only its bounded structural scope; it is not replaced by model fluency |
| Domain validator | Tests domain-specific claims under an owned method |
| Human | Owns intention, interpretation, continuation, approval and consequential decision |

Recommended chain:

```text
Human question
  → immutable Orientation Request
  → AI proposes candidate records
  → deterministic contract/citation validator checks
  → bounded processor or domain validator records outcomes
  → Human inspects evidence, uncertainty and rejected claims
  → Human decides, continues, or stops
```

Deterministic validation may establish shape, identity, citation presence,
allowed status transitions or exact computations. It cannot generally establish
the truth of an AI-generated interpretation.

---

## 14. Failure and falsification analysis

| Risk | Boundary or mitigation | Experimental test | Rejection criterion |
| --- | --- | --- | --- |
| “Orientation” is too broad | Require a bounded responsibility and prohibited implications for every contract | Implement one narrow comparison, not a universal workflow | If useful contracts cannot be narrower than generic “input/process/output” |
| OLS becomes an abstract universal vocabulary with little operational value | Keep released primitives fixed; test only explicit mappings | Two implementations exchange one subset | If the abstract model adds no interoperability or catches no drift |
| Domains cannot agree on evidence or semantics | Keep domain profiles and validators owner-scoped | Cross-domain case uses analogy labels and separate evidence policies | If infrastructure requires a universal evidence ranking |
| Abstract model becomes another ontology layer | Minimize nodes to carrier-independent OLS requirements | Round-trip one carrier without inventing concepts | If it duplicates an ontology/record model without semantic preservation value |
| Carrier mappings drift | Canonical fixtures, semantic equivalence tests and visible unsupported fields | Independent parse/serialize comparison | If incompatible mappings can both claim conformance |
| Processors become incompatible | Exact capability declarations and STOP | Substitute a second processor | If negotiation cannot explain output/status differences |
| Provenance is too expensive | Tiered profiles; require only what supports the claim | Measure artifact size and review time | If provenance costs exceed benefit without detecting or explaining errors |
| Human workflow rejects complexity | Progressive disclosure; machine details remain inspectable, not constantly displayed | Usability test with domain reviewers | If users cannot complete work or understand status better than baseline |
| Existing standards solve the useful parts | Reuse JSON, SVG, glTF, PROV/RO-Crate/BagIt candidates and native tools | Standards-gap analysis before each new contract | Reject new format/protocol when no unique semantic responsibility remains |
| Infrastructure becomes bureaucracy | Gate each new record by demonstrated consumer and failure it prevents | Compare task time/error rate with and without envelope | If records are produced but never inspected, exchanged or used |
| API decomposition destroys reproducibility | Keep immutable artifacts canonical and APIs dispensable | Replay offline from captured artifacts | Reject API-only design if replay depends on vanished server state |
| Representation independence hides domain assumptions | Mapping contract names units, frames, invariants, loss and authority | Produce two representations and audit differences | If mappings cannot expose assumptions needed for domain interpretation |
| Semantic claims cannot be independently validated | Separate semantic conformance from domain validation | Adversarial valid-but-false example | Reject wording that calls semantic validation truth |
| One architecture is forced across incompatible cases | Core envelope stays small; domain records remain independent | Apply prototype to two unlike domains | If common fields become a large optional superset or erase domain controls |
| Distributed design adds fragility | Local deterministic execution is the baseline; federation is optional | Run identical artifact workflow offline and remotely | Reject mandatory networking if no material distributed requirement exists |
| Human authority becomes ceremonial | Require exact intention preservation and explicit continuation/approval record | Test disagreement and stop paths | Reject workflow if automation can silently continue or promote status |

Falsification is successful when a candidate layer, plane, record or service can
be removed without losing an owned responsibility, measurable property or
necessary boundary. Such a component should be removed.

---

## 15. Minimal prototype recommendation

### 15.1 Relationship to the existing Stage 1

The baseline Stage 1 tests:

```text
JSON carrier
  → parser
  → abstract model
  → validator
  → canonical round trip
```

That is necessary but insufficient to test infrastructure. It tests a carrier
and abstract-model hypothesis, not processor substitution, request/result
accountability or Human inspection.

The infrastructure prototype should **extend the experiment**, not change the
released architecture:

```text
immutable request artifact
  → local capability check
  → Stage 1 parse/validate/abstract-model path
  → one bounded compare-or-represent operation
  → immutable complete/partial/blocked result artifact
  → mapping record
  → static SVG
  → Human inspection checklist
```

### 15.2 Required prototype properties

- no network, database, queue, registry, package extension or new media type;
- one local command or library entry point;
- ordinary files in a Git-diffable directory;
- exact input, processor, result and SVG digests;
- one capability declaration;
- one compatible request, one unsupported request and one blocked result;
- evidence, uncertainty, prohibited implications and mapping loss;
- no recommendation, authorization, domain truth or autonomous continuation;
- independent replay on a clean environment;
- Human review that can trace one SVG element back to source evidence.

### 15.3 Success and stop criteria

The hypothesis gains evidence if:

1. request/result envelopes clarify responsibility beyond the carrier alone;
2. replay reproduces the declared result level;
3. unsupported capability stops visibly;
4. source-to-SVG trace is inspectable;
5. replacing the SVG mapping does not change the result record;
6. a second processor can later consume the same request without contract
   reinterpretation.

Stop or narrow the work if:

- the envelope merely repeats existing ORION contracts without a second use;
- the abstract model requires new OLS semantics;
- domain-specific fields dominate the common contract;
- provenance cannot be used during review;
- the SVG is treated as evidence rather than a representation;
- a service, package or registry becomes necessary only to make the diagram
  look infrastructural.

The immediate change is therefore **a clearer experimental request/result
envelope around Stage 1**, not a platform and not a change to ORION Version 1.

---

## 16. ADR and RFC implications

No production RFC should be opened merely to reserve the term Orientation
Infrastructure.

| Order | Decision artifact | Question | Gate |
| --- | --- | --- | --- |
| 1 | Informative experiment plan | Can Stage 1 plus request/result and SVG trace demonstrate measurable value? | No normative effect |
| 2 | ADR: use of “Orientation Infrastructure” | Is the term retained as a provisional architecture category, narrowed, or retired? | Prototype evidence reviewed |
| 3 | RFC: OLS Abstract Expression Model | What minimal carrier-independent structure realizes released semantics? | OLS governance approval |
| 4 | RFC: processor capability contract | Which capabilities, determinism levels, outputs and STOPs are interoperable? | Two processor candidates |
| 5 | ADR/RFC: bounded request/result envelope | Which fields are genuinely common without replacing owner-specific records? | Two distinct domain or processor uses |
| 6 | RFC: representation mapping contract | How are source, invariants, loss, renderer and output linked? | Two mappings and an independent consumer |
| 7 | Optional federation research note | Is discovery needed beyond direct configuration and artifact exchange? | Concrete remote interoperability requirement |

Do not create a central registry, universal API, service taxonomy or
infrastructure certification programme before these gates.

---

## 17. Accepted, narrowed, deferred, and rejected claims

### 17.1 Accepted

- The repository contains a coherent architecture spanning semantics, bounded
  processing, accountable artifacts, representations and Human inspection.
- Reality remains outside formal ownership.
- Storage and transport are orthogonal to semantic and record contracts.
- Processors may share a contract across local and remote deployments.
- Immutable records can connect processor stages when identity, status,
  provenance and compatibility remain explicit.
- Human interpretation and consequential decision remain outside autonomous
  processing.

### 17.2 Narrowed

- “OLS owns meaning” means released orientation semantics, not domain or Human
  meaning.
- OLS is IR-like only through a future Abstract Expression Model.
- Orientation Infrastructure is a provisional interoperability architecture,
  not an implemented universal system.
- NEXAHEDRON participates as the Human Workspace and application boundary, not
  semantic or scientific authority.
- Hybrid architecture means artifact-centered contracts with optional APIs,
  not mandatory network services.

### 17.3 Deferred

- Orientation Computing as a distinct research or engineering discipline;
- a general processor capability specification;
- cross-processor request/result interoperability;
- federation, discovery and optional registries;
- infrastructure conformance or certification;
- package and streaming profiles;
- platform terminology.

### 17.4 Rejected

- OLS itself is infrastructure;
- OLS operators should each become services;
- the architecture should be API-first;
- observation is wholly owned by OLS;
- a central registry is initially required;
- AI may act as semantic, scientific, Kernel or Human authority;
- Orientation Protocol, Orientation Operating System or Orientation Web as
  current architecture names;
- infrastructure validity implies scientific validity.

---

## 18. Final decision table

An `X` identifies the decision. “Narrowed” means a limited form survives.

| Hypothesis | Supported | Narrowed | Deferred | Rejected | Reason |
| --- | :---: | :---: | :---: | :---: | --- |
| OLS is infrastructure |  |  |  | X | OLS is semantic specification and a possible foundation, not execution/storage/transport infrastructure |
| OLS is an intermediate representation |  | X |  |  | A future Abstract Expression Model may serve an IR-like role; OLS 1.0 itself is not an IR artifact |
| Orientation Infrastructure is a valid architecture term |  | X |  |  | Valid provisionally for the bounded interoperability hypothesis; implementation evidence is incomplete |
| Processors should expose service interfaces |  | X |  |  | Some deployments may expose services, but the processor contract remains deployment-neutral |
| OLS operators should become services |  |  |  | X | Semantic primitives are not deployment boundaries |
| The architecture should be API-first |  |  |  | X | It weakens offline replay, preservation and artifact authority |
| The architecture should be artifact-first |  | X |  |  | Artifacts are the durable center, but live/remote profiles may use APIs or streams |
| The architecture should be hybrid |  | X |  |  | Hybrid operation is useful, but the architecture remains deployment-neutral and does not require an API |
| Observation belongs inside OLS |  | X |  |  | OLS owns observation-product semantics; source acquisition and validity remain domain-owned |
| Observation is a separate domain-owned boundary |  | X |  |  | The source act and evidence are domain-owned, while OLS governs semantic expression |
| Orientation Records can connect processors | X |  |  |  | Bounded immutable records can preserve identities, statuses and lineage without becoming universal |
| A central processor registry is required |  |  |  | X | Direct configuration and artifact-bound declarations suffice for the prototype |
| AI can act as semantic authority |  |  |  | X | Models propose and cannot own OLS, domain, Kernel or Human authority |
| AI can act as a bounded proposing processor | X |  |  |  | Supported when outputs are candidate, traceable, validated and Human-governed |
| NEXAHEDRON is part of the infrastructure |  | X |  |  | It is the Human Workspace/application boundary, not a mandatory semantic or execution component |
| Human interpretation and decision remain outside autonomous processing | X |  |  |  | Directly supported by OLS and ORION authority boundaries |

---

## 19. Final recommendation

Retain **Orientation Infrastructure** as the name of an **informative,
falsifiable architecture hypothesis**, with this required qualifier:

> It denotes interoperable boundaries among orientation semantics, immutable
> artifacts, bounded processors, evidence, representations and Human
> Workspaces. It does not denote a platform, network, operating system,
> universal service architecture, or source of scientific or Human authority.

Do not adopt **Orientation Computing** yet. That term requires evidence of a
distinct, reusable operational method with measurable value beyond good
software architecture and scientific provenance practice.

The project starts correctly by building one small offline artifact chain,
measuring whether its request/result boundary improves accountability and
replay, and being willing to retire the infrastructure term if it does not.
