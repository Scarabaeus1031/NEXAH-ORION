# NTO Calendar Formal Specification — Completion Profile

- Status: Incomplete candidate; informative requirements skeleton
- Conformance status: not conforming and not executable
- Architectural effect: none
- OLS effect: none
- ORION effect: none

## 1. Purpose

This document records the minimum declarations needed to evaluate an NTO
Calendar as a reusable Reference Space using existing OLS concepts. It does not
fill unknown values, register a profile, authorize a transformation, or assert
astronomical meaning.

`unknown` is intentional. Replacing it with an inferred default would make the
specification appear more complete than the evidence.

## 2. Reference Space

NTO is to be declared through the existing composite responsibility:

| Component | Required NTO declaration | Current value |
| --- | --- | --- |
| context | intended domain and valid scope | `unknown` |
| representation | calendar representation type and version | `unknown` |
| perspective | construction/reading condition | `unknown` |
| scale | temporal, phase, discrete index, or product scale | `unknown` |
| position | meaning of a location in the calendar | `unknown` |
| relation | valid order, adjacency, recurrence, and mapping relations | `unknown` |
| difference | basis for comparing two coordinates | `unknown` |
| constraint | admissible coordinates and transformations | `unknown` |
| boundary | derived wrap, interval, discontinuity, and ambiguity rules | `unknown` |

No new `Reference Space` primitive is proposed.

## 3. Coordinate System

### 3.1 Required declarations

```text
profile_id: unknown
profile_version: unknown
domain D: unknown
coordinate_set C: unknown
coordinate_tuple: unknown
coordinate_types: unknown
units: unknown
epoch t0: unknown
direction: unknown
precision: unknown
cycle_count_status: unknown
```

If the intended system is a single cycle, a possible existing contract shape is
a cyclic coordinate `τ ∈ [0,1)` derived from an explicitly supplied source
coordinate, epoch, and period. This is already the candidate form in `T15`; it
is not evidence that NTO actually uses that form.

If NTO combines several cycles, it must declare either:

- a product coordinate with one component per cycle; or
- a documented reduction from the product to another coordinate.

The reduction must expose collisions and loss. A picture of several overlaid
cycles is not a mapping definition.

### 3.2 Order

Exactly one or more of the following must be declared:

- linear order;
- cyclic order relative to an origin and direction;
- component-wise partial order;
- no meaningful global order.

The specification must define equality at wrap boundaries and tie behavior.

### 3.3 Neighborhood

The profile must declare whether neighborhood means:

- immediate predecessor/successor;
- cyclic adjacency;
- distance below a threshold under a declared metric;
- graph adjacency through declared relations; or
- not applicable.

Renderer proximity must not silently define semantic neighborhood.

### 3.4 Boundary conditions

Required:

```text
interval closure: unknown
wrap/modulo rule: unknown
cycle boundary: unknown
timezone: unknown or explicitly not applicable
date-boundary convention: unknown or explicitly not applicable
intercalation/leap rule: unknown or explicitly not applicable
out-of-range behavior: deterministic rejection required
ambiguous-boundary behavior: unknown
```

## 4. Objects and markers

Objects are identified subjects within the declared representation. Named
markers such as Earth, Moon, Sun, Jupiter, Titan, Pluto, Sedna, Eris, or Hydra
must be represented as ordinary object identifiers with optional labels.

Each marker requires:

```text
object_id
object_version
label
role
coordinate source
source epoch, if temporal
units
evidence references
uncertainty
```

No celestial name supplies a coordinate or physical necessity by itself.

## 5. Coordinate Mapping

### 5.1 Forward mapping

The profile must define a versioned partial function:

```text
encode_profile : S ⇀ C
```

where `S` is a declared source coordinate domain and `C` is the NTO coordinate
set. Its required parameters, valid domain, units, epoch, direction, precision,
and failure conditions must be explicit.

If `S` is a phase coordinate and the profile uses the `T13` candidate, all of
`θ`, `t0`, `P`, direction, units, calendar profile, and boundary rules are
mandatory. The formula may not be adopted by implication.

### 5.2 Reverse mapping

The profile must separately declare:

```text
decode_profile : C ⇀ S
```

or, if several source coordinates map to one NTO coordinate:

```text
decode_profile : C ⇀ P(S)
```

Round-trip claims are limited to the declared preserved fields. A missing
absolute cycle count usually prevents recovery of absolute chronology.

### 5.3 Mapping invariants

Every approved mapping must preserve:

- object identity by reference;
- source representation identity;
- declared cyclic or other order;
- epoch when applicable;
- direction;
- units or explicit conversion;
- source evidence and provenance;
- uncertainty and ambiguity;
- declared lossiness.

## 6. Allowed Transformations

This profile introduces no new transition. It may only bind to an existing,
approved contract whose source and target types match.

| Existing route | Current relevance | Current execution status |
| --- | --- | --- |
| `T13` Stellar Projection → Calendar Projection | possible phase-to-calendar route | draft candidate; blocked |
| `T14` Dodecahedral Sky Map → Calendar Projection | possible address-to-calendar route | operator unknown; blocked |
| `T15` Calendar Projection → Orientation Layer | possible cycle normalization | target profile incomplete; blocked |

An NTO binding must declare:

```text
transition_contract_id
transition_contract_version
binding_id
binding_version
source_profile_id
target_profile_id
required_parameters
preserved_invariants
declared_lossiness
ambiguity policy
failure conditions
evidence fixtures
```

No renderer is an allowed semantic transformation. A reverse route is a
separate declared transformation and is not assumed from the forward route.

## 7. Valid Queries

The following queries are valid only after their required declarations exist:

| Query | Required declarations |
| --- | --- |
| Is coordinate `c` valid? | domain and validity predicate |
| Where does source position `s` map? | forward mapping and parameters |
| Which source positions may correspond to `c`? | reverse/set-valued mapping |
| Does `c1` precede `c2`? | order, origin, direction, and cycle context |
| Are `c1` and `c2` neighbors? | neighborhood rule |
| What is the interval or difference? | difference basis, units, boundary rule |
| Which objects occupy or reference `c`? | object-coordinate relations and version |
| What recurs with a declared period? | period, tolerance, and cycle-count policy |
| Convert NTO to another representation | approved transition binding |
| Trace this coordinate to evidence | complete provenance chain |

Invalid until separately specified:

- prediction of astronomical events;
- causal inference;
- physical equivalence;
- universal resonance claims;
- use of visual proximity as metric;
- interpretation of marker labels as measured dynamics.

## 8. Constraints

1. All coordinates, profiles, mappings, and source artifacts are versioned.
2. No hidden epoch, timezone, phase origin, direction, or wrap default is
   allowed.
3. Unknown parameters block transformation.
4. Named astronomical markers remain labels unless a versioned astronomical
   source binding is declared.
5. Representation never becomes authority for source dynamics.
6. Aggregation, ambiguity, uncertainty, and loss remain visible.
7. Every target retains source identity and provenance.
8. ORION may plan or execute only declared capabilities and does not acquire
   NTO-specific semantic authority.
9. NTO must remain replaceable by another declared coordinate framework.
10. Visual layout does not define coordinates, relations, or neighborhoods.

## 9. Required conformance fixtures

A minimal fixture set must include:

- one ordinary forward mapping;
- lower and upper boundary cases;
- exact wrap case;
- immediately before and after wrap;
- invalid coordinate;
- missing required parameter;
- ambiguous reverse mapping;
- repeated coordinate in different cycle counts;
- abstract-marker substitution;
- unit conversion or incompatible-unit rejection;
- provenance and uncertainty preservation;
- round-trip test restricted to preserved fields.

Expected outputs must be immutable and digest-bound. No fixture set is currently
available.

## 10. Completion criteria

This document can support classification as a reusable coordinate-system
specification only when Sections 3–9 contain no unresolved required value and
the fixtures replay deterministically.

Classification as a reusable Reference Space profile additionally requires the
context, perspective, scale, relation, difference, constraint, boundary,
provenance, uncertainty, and loss declarations in Section 2.

Until then the profile remains incomplete and must fail closed.
