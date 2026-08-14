# NTO Calendar Dependency Graph

- Status: Informative dependency review
- Subject: incomplete NTO Calendar candidate
- Architectural effect: none

## 1. Dependency graph

```text
Frozen OLS semantics
  ├── context / perspective / scale
  ├── representation / position / relation / difference
  ├── constraint / derived boundary
  └── identity / evidence / uncertainty / provenance
                    │
                    ▼
        NTO Reference-Space declaration
        (currently incomplete)
          ├── coordinate profile
          ├── object and marker bindings
          ├── ordering and neighborhood
          ├── boundary rules
          ├── mappings and lossiness
          └── validation fixtures
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
Existing Calendar          Representation
Transition Contracts       / visual renderer
T13 / T14 / T15            (non-authoritative)
        │
        ▼
ORION planning and future bounded execution
(generic; no NTO-specific semantic authority)

Optional astronomical source profile
  ├── measured or computed states
  ├── epoch / frame / units / precision
  └── evidence / uncertainty
        │
        └──────► marker-coordinate bindings only

Historical symbolic and visual material
        └──────► research provenance only
                 (does not define the profile)
```

## 2. Precise dependency table

| NTO part | Depends on OLS | Depends on ORION | Depends on existing coordinate abstractions | Depends on astronomy | Independent of astronomy |
| --- | --- | --- | --- | --- | --- |
| Reference-Space declaration | yes, existing composite semantics | no | yes | no | yes |
| Coordinate tuple/domain | only for typed expression | no | yes | no, unless deliberately defined from ephemerides | yes |
| Ordering/neighborhood | relation/difference/constraint | no | yes | no | yes |
| Epoch/period values | time, evidence, provenance | no | yes | only if sourced from astronomical dynamics | possible with abstract values |
| Marker identifiers | object/identity/reference | no | yes | no | yes |
| Marker labels | representation metadata | no | no | no | yes |
| Marker coordinates | observation/evidence/uncertainty | no | yes | optional source dependency | yes with abstract fixtures |
| Forward/reverse mapping | representation/transition/provenance/loss | no | yes | optional | yes |
| Transition planning | declared contract semantics | yes, current generic planner | yes | no | yes |
| Mathematical execution | declared capability semantics | future bounded processor only | yes | optional by binding | yes |
| Validation fixtures | evidence/uncertainty/prohibited implications | generic validation boundary | yes | only for astronomical claim fixtures | yes |
| Calendar visual | representation/provenance | no renderer currently | reads coordinates only | no | yes |
| Astronomical interpretation | evidence/context/perspective | no | only if it asserts coordinates | yes | no |
| Symbolic interpretation | context/perspective/provenance | no | no | no physical dependency | yes |

## 3. Ownership and non-dependencies

### OLS owns

- the existing semantic vocabulary used to declare the profile;
- identity, evidence, uncertainty, provenance, representation, relation, and
  transformation boundaries;
- no NTO constants or astronomical truth.

### The NTO profile would own

- its domain, coordinate tuple, epoch, periods, direction, ordering,
  neighborhood, boundaries, mappings, ambiguity, and lossiness;
- its versioned marker bindings and conformance fixtures;
- no ORION behavior and no OLS primitive.

### ORION owns

- generic planning over registered representations and contracts;
- deterministic blocker reporting in the current baseline;
- only a future explicitly approved bounded execution, if implemented;
- no NTO-specific constants, marker meanings, or astronomical assumptions.

### Astronomical sources would own

- any measured or computed celestial state;
- frame, epoch, units, precision, model version, provenance, and uncertainty;
- no calendar semantics by default.

### Representations own

- visual or textual presentation of an already declared Result;
- no coordinate generation, semantic mapping, or evidential authority.

## 4. Independence tests

### 4.1 Marker substitution

Replace all celestial labels with `marker-01`, `marker-02`, and so forth.
Coordinate validation and transformations must remain unchanged unless the
profile explicitly consumes astronomical source values.

### 4.2 Processor substitution

Two conforming processors given the same profile, parameters, and source
coordinates must preserve the same declared semantic outcome. ORION must not
special-case the profile name.

### 4.3 Representation substitution

Replace a spiral, table, or diagram with another renderer. Coordinates,
relations, boundaries, and Results must remain unchanged.

### 4.4 Reference-space substitution

Replace NTO with another declared calendar profile. ORION's generic planning
boundary must remain intact; only profile bindings and compatible routes may
change.

## 5. Hidden-coupling failures

The profile is not interchangeable if any of these occurs:

- a marker's name silently selects a numeric constant;
- the renderer computes calendar positions;
- visual proximity defines neighborhood;
- ORION contains branches keyed to `NTO`;
- a missing epoch or boundary convention receives a default;
- the astronomical interpretation changes coordinate validity;
- normalization discards the source profile or uncertainty;
- a historical symbolic relation is treated as a measured relation.

## 6. Current dependency conclusion

The intended clean architecture is achievable without new primitives:

```text
NTO depends on existing OLS semantics.
ORION may depend on a declared NTO profile at invocation time.
ORION architecture does not depend on NTO.
Astronomical interpretation is an optional, separately evidenced binding.
Visual illustration depends on NTO Results, never the reverse.
```

At present, the middle artifact — the declared NTO profile — is missing.
Consequently the graph describes required ownership and separation, not an
implemented dependency chain.
