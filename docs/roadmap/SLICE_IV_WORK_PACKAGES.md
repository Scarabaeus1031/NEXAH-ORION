# Vertical Slice IV — Work Packages

- Status: Canonical work-package plan
- Implementation status: Not started
- Scope: WP26–WP30
- Architecture status: Approved and frozen

## 1. Governing Rule

Every Slice IV work package has one owner, one responsibility, one dependency
boundary, and one STOP.

This document plans future work. It does not design or create Expression
objects, schemas, formats, proofs, validators, certification records, source
files, or implementation.

## 2. Package Sequence

| Package | Responsibility | Begins after | Ends at |
|---|---|---|---|
| WP26 | Expression Contract | Certified Slice III STOP | Contract Gate |
| WP27 | Expression Construction | WP26 accepted | Construction STOP |
| WP28 | External Expression Conformance | WP27 complete | Conformance Gate |
| WP29 | Expression Certification | WP28 accepted | Expression Certification Gate |
| WP30 | Vertical Slice IV Certification | WP29 complete | Slice IV STOP |

The sequence is mandatory. Later packages cannot compensate for an incomplete
earlier package.

## 3. WP26 — Expression Contract

### Objective

Establish the future contract responsibility that bounds how exact certified
Slice III information may become communicable.

### Owns

- permitted certified input boundary;
- fidelity obligation;
- declared communicative scope;
- provenance continuity obligation;
- visible absence obligation;
- declared lossiness obligation;
- deterministic and replayable construction constraints;
- separation from Human interpretation and downstream action.

### Reads

- frozen Slice IV architecture;
- certified Slice III entry boundary;
- certified Core authority and provenance guarantees.

### Accepted Inputs

- the four frozen Slice IV architecture documents;
- the certified Core Plate;
- the existing `at_slice_iii_certified` entry condition;
- the minimum certified input set already defined by architecture.

### Planned Output

An accepted Expression Contract responsibility sufficient to constrain future
construction and external conformance.

Its schema, object model, format, fields, API, and serialization are outside
this plan and must not be inferred from this description.

### Forbidden Inputs

- raw Markdown or source text;
- mutable Working Material;
- Projection or Renderer state;
- provider or model output;
- Runtime or application state;
- unvalidated or unrelated artifacts.

### Forbidden Outputs

- Expression content;
- constructed candidates;
- conformance decisions;
- certification results;
- LYRA, SIRIUS, Runtime, or application behavior.

### Authority Boundary

WP26 may bound faithful communicability. It may not grant Expression authority
over Core facts, semantics, Human meaning, interpretation, decisions, or
actions.

### Completion Conditions

WP26 is complete only when:

- its responsibility can be assigned without overlap;
- every permitted input is already authorized by frozen architecture;
- fidelity, scope, provenance, lossiness, absence, and determinism are bounded;
- forbidden inputs and outputs are explicit;
- construction and conformance can later be independently assigned;
- no format, schema, object, implementation, or downstream behavior has been
  introduced;
- all Core and Slice IV architecture remains unchanged.

### STOP

```text
Expression Contract accepted
        ↓
STOP
```

No Expression construction may occur inside WP26.

## 4. WP27 — Expression Construction

### Objective

Plan the future deterministic construction responsibility that applies the
accepted Expression Contract to one exact certified input lineage.

### Owns

- faithful transformation into communicable form;
- application of declared scope and lossiness;
- preservation of certified identity, order, status, provenance, boundaries,
  and absence;
- immutable candidate production.

### Reads

- accepted Expression Contract;
- passed Slice III Certification;
- exact accepted Orientation Map artifacts named by that certification;
- only those upstream certified fields explicitly required and referenced by
  the accepted lineage.

### Accepted Inputs

- the completed WP26 responsibility;
- one exact, internally consistent certified Slice III lineage;
- explicit communicative constraints authorized by the Expression Contract.

### Planned Output

One candidate faithful Expression awaiting independent conformance.

The candidate's concrete representation remains deliberately undefined here.

### Forbidden Inputs

- raw Markdown or source text;
- mutable Workspace material;
- unrelated, missing, rejected, or unreferenced artifacts;
- hidden prompts, provider output, external retrieval, or mutable state;
- SIRIUS, Runtime, application, or user-profile state.

### Forbidden Outputs

- semantic interpretation;
- inferred or enriched Core information;
- repaired certified artifacts;
- ranking, recommendations, decisions, or actions;
- a conformance or certification claim.

### Authority Boundary

WP27 may change communicative form only. It cannot change what the certified
Core established, what it left absent, or who owns meaning.

### Completion Conditions

WP27 is complete only when:

- construction depends only on accepted inputs and explicit constraints;
- the candidate preserves the exact certified lineage;
- scope and lossiness remain explicit;
- absence, unknowns, exclusions, and boundaries remain visible;
- no certified input is mutated, reordered, repaired, or completed;
- equal canonical inputs and equal declared constraints are required to yield
  equal canonical output;
- the candidate makes no claim of conformance or certification;
- WP26 and the certified Core remain unchanged.

### STOP

```text
Candidate faithful Expression constructed
        ↓
STOP
```

No external conformance occurs inside WP27.

## 5. WP28 — External Expression Conformance

### Objective

Plan the independent observation of whether the exact candidate Expression
satisfies the accepted Expression Contract against the exact certified input
lineage.

### Owns

- external fidelity evaluation;
- contract-bound acceptance or rejection;
- deterministic observation of scope, provenance, lossiness, absence, and
  lineage preservation;
- fail-closed handling of malformed or inconsistent inputs.

### Reads

- accepted Expression Contract;
- exact candidate Expression;
- exact certified Slice III lineage used by construction.

### Accepted Inputs

- completed WP26 responsibility;
- completed WP27 candidate;
- the exact immutable certified artifacts referenced by both.

### Planned Output

One external conformance decision for the supplied candidate.

The decision's artifact form and schema remain outside this plan.

### Forbidden Inputs

- raw source or mutable Working Material;
- unrelated certified lineages;
- replacement candidates;
- Runtime, SIRIUS, application, or Human decision state.

### Forbidden Outputs

- constructed or rewritten Expression;
- repaired, normalized, completed, or rephrased content;
- new provenance or substituted references;
- semantic approval;
- certification status.

### Authority Boundary

WP28 may state only whether the supplied candidate conforms to the accepted
contract. It cannot create conformity by changing the candidate.

### Completion Conditions

WP28 is complete only when:

- evaluation is outside the construction responsibility;
- the exact candidate and its exact certified lineage are observed;
- accepted and rejected outcomes are deterministic;
- malformed, missing, inconsistent, or unreferenced inputs fail closed;
- no repair, normalization, completion, mutation, or reinterpretation occurs;
- conformance does not claim semantic truth or Human meaning;
- WP26, WP27, and the certified Core remain unchanged.

### STOP

```text
External Expression Conformance decided
        ↓
STOP
```

No Expression certification occurs inside WP28.

## 6. WP29 — Expression Certification

### Objective

Plan certification of the complete Expression responsibility after external
conformance has accepted the exact candidate.

### Owns

- certification of deterministic replay across WP26–WP28;
- certification of immutable inputs and outputs;
- certification of provenance continuity and frozen responsibilities;
- certification that Expression added no authority or interpretation;
- the Expression Layer certification boundary.

### Reads

- accepted Expression Contract;
- exact candidate Expression;
- accepted External Expression Conformance result;
- exact certified Slice III lineage;
- completed WP26–WP28 review and verification results.

### Accepted Inputs

- completed WP26 through WP28 in order;
- an accepted conformance result for the exact candidate;
- unchanged certified Core dependencies.

### Planned Output

An Expression Layer certification decision.

The certification artifact, fields, proof form, and identifiers are not
designed by this plan.

### Forbidden Inputs

- rejected or uncertified candidate chains;
- missing or substituted lineage;
- downstream SIRIUS, Runtime, application, or Human action state.

### Forbidden Outputs

- new or modified Expression content;
- a repaired conformance result;
- reconstructed Core artifacts;
- vertical-slice closeout;
- downstream authorization.

### Authority Boundary

WP29 certifies the Expression responsibility only. It neither re-executes a
Core responsibility nor certifies the complete Slice IV transition.

### Completion Conditions

WP29 is complete only when:

- WP26–WP28 responsibilities are verified as distinct and unchanged;
- the accepted chain is deterministically replayable;
- immutable inputs, candidate, and conformance result are preserved;
- certified provenance resolves to one exact Slice III lineage;
- no interpretation, enrichment, repair, or hidden determinant is present;
- the Expression Layer can become a frozen dependency of WP30;
- no slice closeout or downstream execution has occurred.

### STOP

```text
Expression Layer certified
        ↓
STOP
```

Vertical Slice IV remains open until WP30.

## 7. WP30 — Vertical Slice IV Certification

### Objective

Plan the final certification and closeout of the complete Vertical Slice IV
transition.

### Owns

- ordered verification of WP26–WP29 completion;
- verification that the certified Core baseline remains unchanged;
- verification of the transition from `at_slice_iii_certified` through the
  certified Expression Layer;
- final Slice IV boundary certification;
- explicit downstream STOP.

### Reads

- frozen Core certification baseline;
- exact certified Slice III entry lineage;
- completed and certified Expression Layer;
- package and gate completion status for WP26–WP29.

### Accepted Inputs

- passed Expression Certification Gate;
- unchanged Slice III certification and exact Map lineage;
- complete ordered Slice IV package record.

### Planned Output

A Vertical Slice IV certification decision and final Slice IV STOP.

No concrete certification artifact is designed here.

### Forbidden Inputs

- incomplete or conditionally accepted work packages;
- failed conformance;
- altered Core artifacts;
- SIRIUS, Runtime, application, or Human action state.

### Forbidden Outputs

- Expression content or repair;
- new Core capability;
- SIRIUS behavior;
- Runtime execution;
- application behavior;
- Human interpretation or action.

### Authority Boundary

WP30 may certify completion of the Slice IV boundary only. It cannot authorize
or implement any responsibility beyond that boundary.

### Completion Conditions

WP30 is complete only when:

- WP26–WP29 have passed their STOPs in order;
- the Expression Layer certification remains valid;
- the complete chain resolves to the original certified Slice III lineage;
- Core artifacts and prior certifications remain unchanged;
- determinism, immutability, provenance, scope, lossiness, visible absence, and
  responsibility separation are verified across the slice;
- no fallback or alternate path exists;
- no downstream capability has executed;
- the final Slice IV STOP is explicit.

### STOP

```text
Vertical Slice IV certified
        ↓
STOP
```

SIRIUS, Runtime, applications, NEXAHEDRON presentation, and Human action remain
outside the work-package plan.

## 8. Cross-Package Responsibility Matrix

| Package | Owns | Reads | Certifies | Never owns |
|---|---|---|---|---|
| WP26 | Expression Contract boundary | Frozen architecture and Core entry requirements | Nothing | Content, validation, certification |
| WP27 | Expression construction | Contract and certified lineage | Nothing | Conformance, interpretation, certification |
| WP28 | External conformance | Contract, candidate, certified lineage | Nothing; it decides conformance | Construction, repair, certification |
| WP29 | Expression Layer certification | Completed WP26–WP28 chain | Expression Layer | Content, conformance construction, slice closeout |
| WP30 | Slice IV certification | Certified Core and Expression Layer | Full Slice IV boundary | Expression behavior or downstream execution |

## 9. Package-Level Non-Goals

No package may introduce:

- semantic reasoning or interpretation;
- AI or provider behavior;
- LYRA internals;
- Evidence, claims, entities, concepts, or knowledge graphs;
- relation, Navigation, or Orientation Map behavior;
- visualization or presentation design;
- SIRIUS;
- Runtime;
- applications or NEXAHEDRON workflow;
- transport, persistence, or sessions;
- later-slice planning.

## 10. Work-Package Closing Rule

A work package is complete only when its single responsibility is bounded,
independently reviewable, and stopped before the next responsibility. No later
package may absorb unfinished work from an earlier package.
