# Independent Structural Grammar

- Status: Informative structural review
- Method: derived from non-visual repository evidence
- Normative effect: none
- OLS effect: none
- Architecture effect: none
- Review date: 2026-07-25

## 1. Evidence boundary

This grammar was reconstructed before consulting the visual corpus. The
derivation used:

- the released OLS vocabulary, declarations, operators, products, and grammar
  as inventoried in
  [`OLS_1_0_REPOSITORY_ARCHITECTURE_EXTRACTION.md`](../../architecture/OLS_1_0_REPOSITORY_ARCHITECTURE_EXTRACTION.md);
- ORION object, relation, navigation, map, expression, transformation, and
  authority boundaries in
  [`ORION_V1_ARCHITECTURE_FREEZE.md`](../../architecture/ORION_V1_ARCHITECTURE_FREEZE.md),
  [`SLICE_III_RELATIONS.md`](../../architecture/SLICE_III_RELATIONS.md),
  [`SLICE_III_NAVIGATION.md`](../../architecture/SLICE_III_NAVIGATION.md), and
  [`SLICE_IV_EXPRESSION_ARCHITECTURE.md`](../../architecture/SLICE_IV_EXPRESSION_ARCHITECTURE.md);
- Transition Contracts `T01–T15` and their
  [`Transition Contract Specification`](../../architecture/transformations/contracts/TRANSITION_CONTRACT_SPECIFICATION.md);
- the
  [`Markdown Structural Representation Profile`](../../architecture/MARKDOWN_STRUCTURAL_REPRESENTATION_PROFILE_V1.md)
  and
  [`Projection`](../../architecture/MARKDOWN_STRUCTURAL_PROJECTION_SPECIFICATION_V1.md);
- executable ORION contracts and deterministic construction code under
  `src/orion/`;
- [POA-001](../../experiments/POA_001_MINIMAL_PROOF.md),
  [POA-002](../../experiments/POA_002_PROCESSOR_EQUIVALENCE.md), and
  [POA-003](../../experiments/POA_003_REPRESENTATION_INDEPENDENCE.md)
  specifications and freeze reports;
- repository ownership, provenance, validation, STOP, and representation
  boundaries.

Posters, diagrams, colors, astronomical labels, symbolic names, and historical
metaphors were excluded from this derivation.

## 2. Structural finding

Multiple independent repository areas repeatedly instantiate the same smallest
form:

```text
applicable declarations
        +
identified input reference(s)
        +
bounded operator application
        ↓
resulting semantic product OR explicit blocker
        +
preserved status and trace
```

This is not a new primitive. It is the carrier-independent shape already
proposed by the OLS Abstract Expression Model:

- declaration;
- semantic product or source reference;
- primitive operator application;
- condition;
- evidence, provenance, uncertainty, and status attachment;
- result or blocker reference.

The same shape appears in code as immutable inputs, explicit contracts,
deterministic construction or planning, immutable outputs, validation, lineage,
and failure without repair.

## 3. Minimal grammar

The notation below is review notation, not a new OLS syntax.

```text
construction ::=
    declaration*
    input-reference+
    operator-application
    outcome
    attachment*

operator-application ::=
    operator
    required-basis
    required-parameter*
    condition*

outcome ::=
    semantic-product
  | explicit-blocker

attachment ::=
    identity
  | time
  | evidence
  | provenance
  | uncertainty
  | status
  | authority-scope
  | preserved-invariant
  | declared-loss
```

The operator contract decides which declarations, parameters, and attachments
are mandatory. The `*` notation does not authorize omission where an existing
contract requires a value.

Stable references connect constructions:

```text
construction₁.outcome
        ↓ reference
construction₂.input
```

A valid chain is therefore an ordered acyclic set of bounded constructions,
unless an activated profile explicitly defines iteration or recurrence.

## 4. Semantic specialization

The released universal OLS chain is one specialization:

```text
source
  ↓ OBSERVE
observation
  ↓ REPRESENT
representation
  ↓ COMPARE
comparison finding
  ↓ ORIENT
orientation finding
  ↓ EXPLAIN
explanation
```

Profile operators `SELECT`, `TRANSFORM`, `VALIDATE`, `RECORD`, and `APPROVE`
specialize the same structural form with different owners, inputs, outputs, and
prohibited implications.

The grammar does not imply that every chain uses every operator. For example:

- Markdown structural projection uses an explicit mapping but performs no
  semantic interpretation;
- Navigation follows declared relations but performs no recommendation;
- Validation changes validation status but not empirical truth;
- Representation changes inspectable form but not source authority;
- Approval changes governed status but not evidence.

## 5. Optional reference configuration

Some constructions need positions, comparisons, coordinates, or navigation.
For those cases the repository repeatedly assembles an optional reference
configuration:

```text
reference-configuration ::=
    context
    perspective
    representation-type
    [scale]
    [position]
    relation*
    [difference-basis]
    constraint*
    [derived-boundary-rule]
```

This is the existing OLS mapping for the architecture term `Reference Space`.
It is not a new universal primitive.

A Coordinate System is a further specialization:

```text
coordinate-system ::=
    reference-configuration
    coordinate-domain
    coordinate-rule
    unit*
    [origin]
    [direction]
    [ordering]
    [neighborhood]
    [boundary-condition]
```

Coordinates are optional. Graph relations, source locators, ownership scopes,
and exact references instantiate the grammar without numerical coordinates.

## 6. Necessary invariants

The evidence supports these cross-domain invariants:

1. Inputs and outputs remain distinguishable.
2. Identity is preserved or versioned explicitly.
3. An operation is bounded by a declared owner, basis, and capability.
4. Missing required declarations or capability produce an explicit blocker.
5. Provenance remains resolvable to exact inputs.
6. Evidence and uncertainty are not silently promoted.
7. Preserved, derived, hidden, aggregated, and lost information remain
   distinguishable where representation or transformation occurs.
8. Relations do not imply cause, preference, or authority.
9. Representation does not become source reality or semantic authority.
10. Human interpretation and consequential decision remain outside autonomous
    structural processing.

Not every invariant is mathematical. Together they form the repository's
orientation grammar rather than a universal geometry.

## 7. Independent recurring realizations

| Repository area | Declarations and inputs | Application | Outcome | Trace/boundary |
| --- | --- | --- | --- | --- |
| OLS universal grammar | context, perspective, representation type, source products | primitive operator | semantic product | evidence, provenance, uncertainty, prohibited implications |
| Transition Contract | source/target types, coordinates, parameters, preconditions | declared transformation | target or failure | invariants, loss, evidence, validation |
| Markdown Projection | CommonMark version, whole-source boundary, target profile | deterministic block mapping | structural declaration or no valid mapping | source identity, ordering, lossiness |
| ORION Relations | certified inventory and exact relation basis | deterministic relation construction | relation set or rejection | endpoint identity, lineage, conformance |
| ORION Navigation | conformant relation set and exact current position | declared traversal action | navigation step or unavailable transition | direction, relation identity, blocker, provenance |
| Transformation Engine | immutable Orientation Object, graph, contracts, target | route planning | plan/report or blocker | alternatives, evidence chain, invariants, source provenance |
| POA-001 | Observation, Request, OLS Expression | bounded `COMPARE` processor | immutable Result or blocked Result | evidence, uncertainty, lineage, prohibited implications |
| POA-002 | same source and expression, two processor identities | independent execution and review | equivalent or non-equivalent Results | all differences retained; STOP compared |
| POA-003 | one immutable Result | two independent mapping/rendering paths | two representations plus review | source trace, loss, non-authoritative boundary |

The recurrence is structural rather than lexical: these areas use different
record types and responsibilities but preserve the same input–application–
outcome–trace form.

## 8. What was not found

The non-visual evidence does **not** establish a shared:

- metric;
- manifold;
- topology;
- coordinate dimension;
- reference direction;
- dynamical law;
- phase space;
- projection family;
- observer axis;
- gate geometry;
- cyclic time model;
- astronomical or musical correspondence.

Those structures occur only in particular domains or candidate
representations. Promoting any of them into the minimal grammar would exclude
valid graph, Markdown, governance, and software-contract realizations.

## 9. Minimality test

Removing any core part breaks independently implemented behavior:

| Removed part | Failure |
| --- | --- |
| declarations | context, basis, units, profiles, or authority become implicit |
| input references | identity and lineage cannot be verified |
| bounded operator application | change or inference has no accountable owner or capability |
| result/blocker distinction | unsupported input can be silently accepted or repaired |
| status and trace | evidence, uncertainty, loss, and provenance disappear across a transition |

Coordinates, graphs, records, renderers, and Human interfaces can be removed
from the universal form because they are specializations or downstream
realizations.

## 10. Relationship to OLS

**Outcome A: the recurring structure is already completely described by OLS.**

The grammar is a compression of existing OLS concepts, declarations,
operators, profile composition, semantic products, attachments, and blocker
rules. ORION and the POAs provide implementation evidence for bounded subsets;
they do not reveal a missing OLS abstraction.

No OLS extension and no new primitive are recommended.
