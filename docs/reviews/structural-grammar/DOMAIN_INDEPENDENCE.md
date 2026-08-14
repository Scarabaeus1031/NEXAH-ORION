# Structural Grammar — Domain Independence

- Status: Informative falsification review
- Dependency: [`STRUCTURAL_GRAMMAR.md`](STRUCTURAL_GRAMMAR.md)
- Visual evidence used in derivation: none

## 1. Test

The candidate grammar is domain-independent only if it remains useful after
removing:

- astronomy and named celestial bodies;
- music, harmony, rhythm, and resonance labels;
- colors and symbolic icons;
- NTO, HYDRA, DERIS, Scarabaeus, JANUS, and other project-specific names;
- assumed Euclidean coordinates or a preferred visual layout.

The test asks whether independent domains can still declare inputs, reference
conditions, bounded operations, outcomes or blockers, and preserved trace.

## 2. Domain instantiations

### 2.1 Geometry and coordinate systems

```text
declarations:
  domain, coordinate profile, units, origin, direction, boundary conditions
input:
  identified point or geometric object
application:
  declared coordinate transformation or projection
outcome:
  target coordinate/representation or singularity blocker
trace:
  source identity, parameters, invariants, uncertainty, loss
```

This uses the optional reference configuration. No astronomy is required.

### 2.2 Graph representations

```text
declarations:
  node and relation vocabulary, direction, admissible endpoint set
input:
  immutable endpoint and relation declarations
application:
  exact relation construction or traversal
outcome:
  relation/navigation step or unavailable transition
trace:
  derivation basis, endpoint identities, order, lineage
```

No numerical coordinate system is required. This falsifies the hypothesis that
coordinates are universal to the grammar.

### 2.3 Observation and measurement

```text
declarations:
  observer/instrument, context, units, calibration, time, sampling rule
input:
  identified source interaction
application:
  OBSERVE and, if needed, REPRESENT
outcome:
  observation/measurement representation or invalid-input blocker
trace:
  provenance, evidence status, uncertainty, calibration reference
```

Changing the observation map changes the representation without necessarily
changing the underlying subject. No HYDRA name is required to express this.

### 2.4 Navigation

```text
declarations:
  exact current position, relation vocabulary, direction, constraints
input:
  conformant relation set
application:
  resolve or follow one declared relation
outcome:
  available movement or explicit unavailable movement
trace:
  origin, relation identity, target, blocker, provenance
```

No geographic or astronomical map is required.

### 2.5 Software architecture

```text
declarations:
  component identity, owner, interface, authority scope, accepted schema
input:
  versioned request or artifact
application:
  one declared capability
outcome:
  result or stable boundary error
trace:
  versions, dependency identity, validation, provenance
```

Here “position” is generally unnecessary. The grammar survives through scope,
identity, relations, and authority rather than spatial metaphor.

### 2.6 Scientific visualization

```text
declarations:
  source record, target representation type, mapping profile, renderer version
input:
  immutable result
application:
  representation mapping
outcome:
  SVG, table, plot, or blocked rendering
trace:
  source digest, preserved fields, derived fields, omissions, loss
```

The representation is not allowed to recalculate the scientific result.

### 2.7 Document structure

```text
declarations:
  CommonMark version, source boundary, target structural profile
input:
  exact UTF-8 source bytes and source identity
application:
  deterministic block projection
outcome:
  ordered structural declaration or no valid mapping
trace:
  locators, canonical order, identity basis, declared lossiness
```

This is a particularly strong non-metaphorical instance because the repository
defines both the source grammar and exact projection behavior.

## 3. Substitution tests

| Substitution | Result |
| --- | --- |
| celestial names → opaque IDs | grammar unchanged |
| musical labels → numeric or opaque relation labels | grammar unchanged |
| colors → textual statuses | grammar unchanged |
| Euclidean points → graph endpoints | grammar unchanged |
| visual arrows → typed directed relations | grammar unchanged |
| map → ordered Markdown block inventory | grammar unchanged |
| OPU → named bounded Processor capability | grammar unchanged |
| DERIS → declared post-transition path segment | grammar unchanged |
| HYDRA → versioned observation-map profile | grammar unchanged |
| NTO → any declared calendar or coordinate profile | grammar unchanged |

The substitutions remove branding and metaphor without removing the structural
roles.

## 4. Failure tests

The following stronger candidates do not survive domain substitution:

| Candidate universal structure | Counterexample |
| --- | --- |
| every orientation uses coordinates | structural relations and authority scopes use exact references without coordinates |
| every orientation is a projection | approval, validation, and relation construction are not projections |
| every process follows a linear pipeline | OLS profiles permit branching, blocking, optional operators, and referenced graph-shaped dependencies |
| every transition is continuous | Markdown and graph transitions are discrete |
| every transition has an inverse | contracts explicitly allow partial, unknown, or no invertibility |
| every system has an observer axis | software contracts and deterministic structural mappings do not require one |
| every boundary is geometric | authority, schema, evidence, source, and STOP boundaries are non-geometric |
| every view is complementary to another | many representations have no declared counterpart or equivalence relation |

Therefore the repository supports a domain-independent orientation grammar but
not a universal mathematical geometry.

## 5. Independence from named research concepts

### DERIS

An outgoing post-crossing segment can be represented with existing state,
transition, time, path, position, relation, evidence, and uncertainty concepts.
DERIS is not required by the grammar.

### HYDRA

A changing observation map is a transformation or representation mapping with
parameters, time, provenance, and loss. HYDRA is not required by the grammar.

### NTO

A complete NTO proposal would instantiate the optional reference
configuration and coordinate-system specialization. NTO is not required by the
grammar and currently remains incomplete.

### Astronomical and musical semantics

They may supply domain objects, parameters, evidence, and labels. They do not
own the grammar and cannot establish its invariants by analogy.

## 6. Domain-independence conclusion

The grammar survives all required removals because its core is relational and
contractual, not visual or domain-specific:

```text
declared conditions
  + referenced input
  + bounded application
  → result or blocker
  + preserved trace
```

Domain independence is supported. Mathematical universality is not.
