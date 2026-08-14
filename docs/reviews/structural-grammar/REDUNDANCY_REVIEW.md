# Structural Vocabulary Redundancy Review

- Status: Informative consolidation review
- Rule: consolidate roles, not legitimate domain distinctions
- OLS changes proposed: none

## 1. Summary

Most apparent duplication comes from three causes:

1. domain terms naming a specialization of an existing OLS concept;
2. visual metaphors used as if they were architecture components;
3. related but non-equivalent responsibilities being used interchangeably.

The appropriate correction is usually documentation discipline, not removal
from historical or domain research.

## 2. Consolidate under existing roles

| Current terms | Shared structural role | Recommended canonical wording |
| --- | --- | --- |
| OPU, runtime engine, processing machine, interpreter, orchestrator | bounded execution of a declared capability | **Processor**; use ORION or Kernel only for their owned scopes |
| lens, aperture, filter, viewpoint, frame of view | construction/selection condition affecting what is represented | **perspective** plus explicit constraint, boundary, or mapping where applicable |
| map, landscape, diagram, field view | structured inspectable form | **representation**, followed by its domain-specific type |
| atlas, gallery, collection of maps | collection or navigation arrangement of representations | representation collection; retain **Atlas** as a product/title |
| journey, route, path, corridor | ordered relation through positions/states, sometimes selected under constraint | use **path** for the ordered relation and **route** only for a selected navigation result |
| gate, aperture, threshold, switch | conditions around admissibility or classification | express through **constraint**, derived **boundary**, **threshold**, or **transition**; retain domain term only when its rule is defined |
| code, JSON, YAML, RDF, DSL | concrete encoding of expressions or records | **carrier** in architecture discussions |
| SVG, GLB, Markdown, audio, plot, poster | perceptible output form | **representation** or native media |
| result, report, manifest, review, episode | accountable preserved artifact classes | bounded **Record classes**, never one universal Record |
| engine, application, workspace, website | implementation or Human-use locations | name the owned capability or interface; do not treat as semantic layers |

`Processor` and `carrier` are architectural compression terms already supported
by the distilled architecture. They are not new OLS primitives.

## 3. Preserve important distinctions

These pairs overlap but must not be merged:

| Terms | Why distinct |
| --- | --- |
| observer / perspective / position | role, viewing condition, and location/focus are different declarations |
| context / Reference Space / domain | context bounds interpretation; Reference Space is a composite; domain owns subject rules and validity |
| Coordinate System / Reference Space | a coordinate method can change while referents and valid comparisons remain; changing valid comparisons changes more than coordinates |
| observation / evidence | captured material does not automatically support a claim |
| provenance / evidence / uncertainty | origin, support, and unresolved knowledge are independent responsibilities |
| transition / transformation | transition is declared state change; transformation is an operation changing form or state |
| projection / representation / rendering | mapping rule, resulting structured form, and perceptual realization are separate |
| relation / causality | relation alone never establishes mechanism |
| validation / approval | criteria-bounded test and governed Human status change are different |
| orientation / interpretation / meaning | OLS orientation is bounded situated understanding; Human interpretation and meaning remain outside autonomous authority |
| result / representation | a representation may present a result but must not recalculate or own it |
| identity / equality / equivalence | same subject, same structure, and preserved semantics are different claims |

## 4. Partially overlapping research terms

| Research vocabulary | Existing expression | Recommendation |
| --- | --- | --- |
| Reference Frame | context + perspective + scale + position + representation type, with origin/direction where domain-required | keep as domain shorthand; do not elevate |
| Orientation Layer | normalized representation with source references and declared loss | keep as named representation target, not universal layer |
| topology | representation + relation + neighborhood rules | keep as mathematical domain term |
| geometry | representation + coordinate/reference basis + relations/distances | keep as mathematical domain term |
| regime | state or classified structure under an explicit rule | keep as domain vocabulary |
| field | domain representation/model with declared coordinates and relations | keep as domain vocabulary |
| DERIS | post-transition path/segment classification with time, evidence, and uncertainty | research vocabulary only |
| HYDRA | time-dependent observation/representation mapping profile | research vocabulary only |
| NTO | proposed calendar reference configuration/profile | incomplete research profile |
| JANUS | policy of preserving declared complementary perspectives | principle, not operator or primitive |
| bridge | relation/transformation across a derived boundary | retain only with endpoints, mapping, and loss stated |

## 5. Graph redundancy

The repository uses:

- relation graphs;
- representation graphs;
- transition graphs;
- navigation graphs;
- provenance graphs;
- execution plans;
- knowledge or Library views;
- diagrams that merely look graph-like.

They must not be merged into a universal graph. Their node identities, edge
semantics, owners, and authority differ. The common grammar operates over
stable references and typed relations without requiring one canonical graph.

## 6. Sequence redundancy

Several sequences are explanatory projections of the same responsibility
boundaries:

```text
Reality → Observation → OLS → Processor → Record → Representation → Human
```

```text
OBSERVE → REPRESENT → COMPARE → ORIENT → EXPLAIN
```

```text
source → mapping → target representation → review
```

They should not be concatenated into one longer mandatory pipeline:

- the first is a responsibility architecture;
- the second is the universal OLS semantic example;
- the third is a representation-mapping pattern.

Documentation should state which level a sequence describes.

## 7. Recommended smallest vocabulary

For structural analysis use:

- source or semantic product reference;
- declaration;
- operator application;
- result or blocker;
- identity;
- evidence;
- provenance;
- uncertainty;
- status;
- preserved invariant and declared loss;
- representation;
- Human.

Add context, perspective, scale, position, relation, constraint, boundary,
coordinate, or transformation only when the concrete claim depends on them.

## 8. Removal recommendations

Remove from future architectural claims, while preserving historical sources:

- OPU as a new peer module beside OLS or ORION;
- universal Orientation Machine;
- universal observer axis;
- universal gate/corridor geometry;
- universal graph or universal record;
- astronomical marker names as infrastructure responsibilities;
- claims that lens, projection, or representation creates truth or meaning;
- claims that a visual recurrence is evidence of mathematical equivalence.

No file, historical name, or research image needs deletion. The recommendation
concerns canonical vocabulary and responsibility assignment.
