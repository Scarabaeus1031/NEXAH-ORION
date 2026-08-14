# NTO Calendar Reference-Space Review

- Status: Informative mathematical and architectural consistency review
- Scope: currently available repository and historical local materials
- Authority: none; this document does not modify OLS, ORION, the frozen
  architecture, or any Transition Contract
- Review date: 2026-07-25

## 1. Review question and result

This review asks whether the current NTO Calendar can be defined rigorously as
a Reference Space within the existing Orientation Language. It does not test
astronomical truth and does not assume that the calendar is physically correct.

**Recommendation: D. The NTO Calendar currently requires additional
mathematical definition before any of the other classifications can be
claimed.**

The available material supports a family resemblance to a cyclic calendar
representation and contains several visual and exploratory predecessors. It
does not provide an identifiable NTO specification with a coordinate domain,
epoch, units, mapping, boundary rules, inverse policy, fixtures, or executable
operator. The current repository itself lists NTO as excluded or deferred.

This finding is not a rejection of NTO. It is a boundary on what the available
evidence presently establishes.

## 2. Evidence boundary

### 2.1 Current repository

No file whose name or content defines an NTO Calendar was found in the current
repository. Explicit references to `NTO` occur only as exclusions:

- `docs/development/REPRESENTATION_ALPHA.md`
- `docs/development/RUNTIME_READINESS_ALPHA.md`
- `docs/roadmap/SLICE_III_ENGINEERING_PLAN.md`
- `docs/roadmap/SLICE_II_COMPLETION_PLAN.md`
- `docs/architecture/STRUCTURAL_REPRESENTATION_ARCHITECTURE.md`

The closest current architectural evidence is the draft calendar route:

- [`T13 — Stellar Projection → Calendar Projection`](../../architecture/transformations/contracts/T13.md)
- [`T14 — Dodecahedral Sky Map → Calendar Projection`](../../architecture/transformations/contracts/T14.md)
- [`T15 — Calendar Projection → Orientation Layer`](../../architecture/transformations/contracts/T15.md)
- [`Transition Contract Specification`](../../architecture/transformations/contracts/TRANSITION_CONTRACT_SPECIFICATION.md)
- [`Orientation Transform Stack`](../../architecture/transformations/ORIENTATION_TRANSFORM_STACK.md)

Those documents require explicit epochs, periods, directions, calendar
profiles, boundary conventions, source references, provenance, ambiguity, and
lossiness. They also state that no calendar profile is registered and that the
operators are unknown or candidates.

### 2.2 Historical, adjacent material

The following material was inspected as possible conceptual ancestry, not as
an authoritative NTO definition:

| Historical source identifier | SHA-256 | Evidence class |
| --- | --- | --- |
| `NEXAH-CODEX/SYSTEM_9_TESSAREC/Cosmic_Harmonic_Time/README.md` | `831c89207fa3d5018dd6e78c0ab75e657a94c6c48e4d5604034e53e1ed800d9d` | exploratory overview |
| `.../Cosmic_Calendar_Closure.md` | `32f943048b895c662cd824e01a107632fa38cf8e08d55e698c57be01cfb03c4b` | mathematical identity mixed with symbolic interpretation |
| `.../Möbius_Resonance_Timegeometry.md` | `f31c0bca41915006c75ffad479a41328e124ca704feec0d51c3981907306a5a3` | exploratory hypothesis |
| `NEXAH-CODEX/SYSTEM_X_NEXAH_GRAND_CODEX_URF/PLANETARY_FIELD_MODES/README.md` | `3fe12f6f42decd051f44061bcdd647c0cc9eb2bdea7a12686640686e9651d0ec` | symbolic research index |
| `.../calendar_mode_sun_centered.md` | `4f78114a26c35a1d1a530c8ebcb8911fb4ef177c51a85d28577efe3d5ca9bcbc` | calendar visualization proposal |
| `.../TimePearl_Field_Simulator.md` | `c38899fe7e32a80cb5f63ea2639de0dbe8e7659c5de831035d7c3b7dff48b161` | observer-centered visualization proposal |

These sources contain cyclic, spiral, phase, observer, Möbius, solar, planetary,
prime, and symbolic constructions. They do not identify themselves as the NTO
Calendar and cannot be silently combined into one specification.

### 2.3 Evidence classification

| Material | Present evidence | Not established |
| --- | --- | --- |
| Mathematical definitions | isolated equations, cyclic and spiral candidates, one correct integer identity | one coherent NTO domain, mapping, metric, topology, or calendar algebra |
| Implementation | visual assets and descriptions of intended simulations | an NTO encoder, decoder, validator, fixtures, or deterministic replay |
| Exploratory hypotheses | harmonic, phase, Möbius, prime, and observer-centered interpretations | tested necessity, uniqueness, or interoperability |
| Astronomical interpretation | named celestial markers and proposed cycles | physical accuracy, causal relevance, required astronomical dynamics |
| Speculative interpretation | symbolic correspondences and resonance readings | scientific validation |
| Visual illustration | calendar spirals, phase maps, and observer views | semantic authority or mathematical completeness |

## 3. Mathematical consistency

The assessment below distinguishes absence from contradiction. Most failures
are missing definitions, not demonstrated inconsistencies.

| Requirement | Current status | Required definition |
| --- | --- | --- |
| Coordinate domain | missing | exact set of valid coordinates and their types |
| Coordinate mapping | missing | deterministic mapping from a declared source coordinate to NTO and its domain |
| Ordering | partial idea only | linear, cyclic, partial, or product ordering and tie behavior |
| Continuity | undefined | topology or explicit declaration that the system is discrete |
| Neighborhood | undefined | predecessor/successor, adjacency, metric ball, or other rule |
| Reproducible transformations | absent | versioned forward mapping, parameters, fixtures, and failure rules |
| Boundary conditions | absent | epoch, wrap, interval closure, leap/intercalation, timezone, and discontinuity policy |
| Invertibility | unknown | injective region, cycle-count requirements, ambiguity set, and inverse failure behavior |
| Units | missing | time, phase, index, angular, or dimensionless unit per coordinate |
| Epoch | missing | origin and reference convention |
| Period/cycle | proposed but not registered | exact period values, provenance, precision, and update policy |
| Marker semantics | ambiguous | label, coordinate anchor, observed body, or computed state |

The current material therefore cannot yet be tested for internal consistency as
one system. A diagram can be internally legible while the mapping that produces
its positions remains undefined.

### 3.1 Minimal consistency conditions

A future NTO declaration would be mathematically reviewable only when it
provides:

1. a non-empty domain `D`;
2. a coordinate set `C` with units and validity predicates;
3. an epoch and every required period or index range;
4. a deterministic partial mapping `encode: D → C`;
5. an explicitly partial or set-valued inverse where information is lost;
6. order and neighborhood relations;
7. wrap and all other boundary rules;
8. versioned examples covering ordinary, boundary, ambiguous, and invalid
   cases;
9. round-trip expectations restricted to the fields actually preserved.

None of these conditions requires a new OLS primitive.

## 4. OLS consistency

The current OLS extraction states that `Reference Space` is an architecture
composite rather than a released universal primitive. Its responsibility is
distributed across context, representation, perspective, scale, position,
relation, difference, constraint, and a derived boundary.

NTO can therefore be expressed using existing concepts:

| Requested NTO notion | Existing OLS expression |
| --- | --- |
| Reference Space | declared context + representation + perspective + scale + position + relation + constraint/boundary basis |
| Coordinate System | position represented under an explicit representation type and scale |
| Coordinates | typed represented positions; no implication of physical location |
| Objects | identified subjects or named marker objects |
| Relations | order, adjacency, recurrence, mapping, or source association, each declared separately |
| Observation | sourced input with evidence and uncertainty |
| Representation | the calendar form made inspectable |
| Orientation | a declared reading or construction over those references |

Terms such as “cosmic lock,” “TimePearl,” “harmonic cathedral,” or a celestial
name may remain titles, labels, or domain vocabulary. They are not needed to
express the reference-space contract and should not become redundant OLS
primitives.

### 4.1 OLS compatibility finding

**Compatible in principle, incomplete in fact.** Existing OLS vocabulary is
sufficient to describe a rigorously declared NTO profile. The missing work is
domain mathematics and evidence, not language expansion.

## 5. ORION compatibility

ORION's current Transformation Engine can navigate registered representation
edges, verify planning metadata, and report blockers. It does not execute
mathematical transformation operators or renderers. The calendar contracts are
documentation-only drafts.

The preferred dependency direction is supported:

```text
declared NTO profile
        │
        ▼
existing representation and transition contracts
        │
        ▼
ORION planning / future bounded processor
```

ORION should not import astronomical constants, special marker meanings, or
NTO-specific control flow. A future processor may consume an NTO profile only
through declared coordinates, objects, relations, transformations, constraints,
evidence, and provenance.

### 5.1 Hidden assumptions that must be removed from the ORION boundary

- celestial names determine numeric values without a versioned mapping;
- a visual angle or spiral radius is automatically a time coordinate;
- phase establishes absolute chronology without epoch and cycle count;
- a renderer's layout supplies adjacency or distance;
- named planets imply required physical dynamics;
- timezone, date boundary, direction, intercalation, or wrap defaults are
  universal;
- distinct cycles can be combined without a declared product or reduction rule;
- normalization preserves domain meaning.

### 5.2 ORION compatibility finding

ORION requires no architectural change to treat NTO as an interchangeable
profile in principle. It would require a registered profile, approved
transition contracts or bindings, executable operators if transformations are
to run, validators, and fixtures. Those are profile and implementation work,
not changes to ORION's semantic authority.

## 6. Astronomical neutrality test

Replace every celestial name with stable abstract identifiers:

```text
Earth → marker-01
Moon → marker-02
Sun → marker-03
Jupiter → marker-04
Titan → marker-05
Pluto → marker-06
Sedna → marker-07
Eris → marker-08
Hydra → marker-09
```

If the mapping, ordering, neighborhoods, boundaries, and valid queries still
work, the names function as labels. If a transformation needs ephemerides,
orbital periods, or measured states, that dependency must be declared as an
astronomical source profile with epoch, units, precision, and provenance.

The available material does not yet provide enough formal mapping to run this
substitution test. Nothing currently demonstrates that the names are
mathematically necessary.

## 7. Hidden assumptions and missing definitions

The blocking omissions are:

- normative NTO source document and version;
- coordinate tuple and valid domain;
- base chronology or source coordinate;
- epoch and direction;
- periods, units, precision, and cycle-count policy;
- linear/cyclic/product order;
- neighborhood and distance, if any;
- marker-to-coordinate mapping;
- multiple-cycle combination rule;
- discontinuity, wrap, leap, timezone, and date-boundary rules;
- ambiguity and aggregation policy;
- forward and inverse transformation definitions;
- representation lossiness;
- immutable examples and expected outputs;
- validation rules and deterministic failure cases;
- provenance binding to observations or astronomical data, where used.

## 8. Maturity assessment

| Dimension | Maturity |
| --- | --- |
| Visual exploration | present in adjacent historical material |
| Domain vocabulary | exploratory and non-canonical |
| Mathematical profile | not yet defined |
| OLS expressibility | sufficient in principle |
| ORION planning compatibility | sufficient in principle |
| Executable transformation | absent |
| Reproducible validation | absent |
| Astronomical validity | outside this review and not established |

## 9. Final recommendation

**D. The NTO Calendar currently requires additional mathematical definition
before any of the above can be claimed.**

Option A would overstate the evidence because the available visuals are
historical calendar-adjacent materials, not an identified NTO artifact set.
Option B would require a complete coordinate-system contract. Option C would
additionally require the surrounding Reference Space declarations, provenance,
constraints, and versioned evidence. Neither exists today.

The smallest valid next step is not an OLS change or an ORION dependency. It is
to fill the unresolved declarations in
[`NTO_FORMAL_SPEC.md`](NTO_FORMAL_SPEC.md), attach boundary fixtures, and test
the profile using abstract marker IDs before adding any astronomical
interpretation.
