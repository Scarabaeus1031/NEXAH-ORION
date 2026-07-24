# Vertical Slice IV — Expression Boundaries

Status: Canonical architecture
Implementation status: Not started
Scope: Authority and exclusion boundaries

## 1. Core-to-Expression Boundary

The certified Core ends at:

```text
Vertical Slice III Certification
        ↓
at_slice_iii_certified
        ↓
STOP
```

Slice IV begins on the other side of that STOP. The transition is read-only.

The certified Core passes no implicit context. Every Slice IV input must be an
exact immutable artifact named by the passed certification lineage.

## 2. Minimum Authority Boundary

The passed Vertical Slice III Certification Report is the entry authority. It
does not contain all communicable content, so the exact accepted Orientation
Map Object, Constructed Orientation Map, and Orientation Map Conformance Report
must accompany it.

The certification establishes acceptance. The Map artifacts provide the
certified content. Their immutable references establish that both belong to the
same chain.

Missing, rejected, inconsistent, or unreferenced artifacts do not cross the
boundary.

## 3. Fidelity Boundary

Expression may change communicative form. It may not change certified
substance.

It must preserve:

- identity;
- version;
- status;
- canonical order;
- relation kind and direction;
- endpoint identity;
- structural adjacency;
- provenance;
- integrity references;
- explicit boundaries;
- declared absence and unavailability;
- declared scope and lossiness.

If a communicative choice cannot preserve these properties, no conforming
expression exists for that choice.

## 4. Interpretation Boundary

Expression is not interpretation.

Expression may state:

- what the certified artifact declares;
- how its declared elements are ordered;
- which exact Relations exist;
- which information is unavailable or excluded;
- where provenance resolves.

Expression may not state:

- what the source means;
- why a Relation matters;
- which element is more important;
- what should be believed;
- which route should be chosen;
- what action should follow.

Those statements require authority that Slice IV does not possess.

## 5. Mutation Boundary

Slice IV may never:

- modify a certified artifact;
- replace an identity or reference;
- reorder certified entries;
- add or remove Relations;
- create Navigation;
- construct or complete an Orientation Map;
- repair missing lineage;
- normalize a rejected artifact;
- infer unavailable information;
- overwrite provenance;
- conceal a certified boundary.

A failed Expression attempt leaves every input unchanged.

## 6. System Boundaries

### LYRA

LYRA is inside the Expression Boundary only when it performs faithful
Human-language expression of certified information. It remains outside Core
authority and outside Human meaning.

### SIRIUS

SIRIUS begins after expression, at a later local access or action-context
boundary. Slice IV does not define its mechanics, authority, or execution.

### Runtime

Runtime is not an input, owner, or output of this Slice IV architecture.
Nothing in these documents authorizes Runtime execution or redesign.

### Applications

Applications may later present a conformant expression. They may choose
presentation form only within the accepted expression; they may not rewrite its
certified substance.

### NEXAHEDRON

NEXAHEDRON remains the Human laboratory and presentation boundary. It does not
receive authority over Core construction or Expression fidelity.

### Human

The Human remains outside the software authority chain and owns:

- intention;
- meaning;
- interpretation;
- judgment;
- acceptance;
- continuation;
- action.

## 7. Forbidden Capabilities

Slice IV excludes:

- semantic inference;
- semantic enrichment;
- source interpretation;
- Evidence generation;
- claims or reasoning;
- knowledge graphs;
- LLM authority;
- relation generation;
- Navigation generation or execution;
- Orientation Map construction;
- route computation;
- ranking or recommendation;
- decision making;
- agent behavior;
- world models;
- Runtime execution;
- graphical design or visualization assessment;
- persistence or application state.

## 8. Future Separation

```text
Certified Core
        ↓
Expression Boundary
        ↓
Faithful communicability
        ↓
Slice IV boundary
════════════════════════════════════
Outside Slice IV
════════════════════════════════════
SIRIUS
Runtime integration
Applications
NEXAHEDRON presentation
Human interpretation and action
```

This diagram assigns boundaries only. It does not define future behavior or
implementation order.

## 9. Boundary Invariant

> Nothing becomes more authoritative merely because it becomes easier to
> communicate.
