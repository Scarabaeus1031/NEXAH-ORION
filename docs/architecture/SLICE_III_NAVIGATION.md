# Vertical Slice III — Navigation Architecture

Status: Canonical architecture
Implementation status: Not started
Input boundary: Externally conformant immutable Structural Relation Set
Output boundary: Immutable Navigation Object; accepted only after External Navigation Conformance

## 1. Purpose

Navigation makes deterministic movement over accepted structural relations
possible.

It answers:

> From this exact structural position, which movements are explicitly
> available?

Navigation does not decide what a Human should inspect. It does not rank,
recommend, infer, interpret, or modify Relations.

## 2. Input

Navigation consumes exactly one externally conformant immutable Structural
Relation Set.

The Relation Set already contains:

- the complete ordered endpoint registry;
- validated relation declarations;
- relation identity, order, direction, and basis;
- Orientation Object, Representation, Inventory, and source lineage;
- integrity and provenance.

Navigation does not consume Markdown, source content, Projection, Renderer,
Representation, Inventory, Summary, or Statistics independently.

If Relation Conformance has not succeeded, no Navigation Object exists.

## 3. Navigation Object

Navigation produces one immutable Navigation Object.

Its envelope contains:

- navigation identity, version, and integrity;
- exact Structural Relation Set identity, version, and integrity;
- Orientation Object identity and version;
- Representation identity, version, and integrity;
- source identity, revision, integrity, and boundary;
- canonical origin;
- ordered immutable relation catalog copied without modification from the
  accepted Structural Relation Set;
- ordered address index;
- ordered transition declarations;
- ordered unavailable transition declarations;
- navigation policy identity and version;
- provenance;
- responsibility state;
- explicit STOP after Navigation.

The relation catalog preserves the exact relation identities, endpoints,
types, direction, basis, order, provenance, and integrity needed by a later
derived view. Navigation does not add to or reinterpret that catalog.

The object is a deterministic index of possible movement. It is not a user
session, history store, recommendation system, or route planner.

## 4. Canonical origin and entry points

### 4.1 Canonical origin

The canonical origin is the declared `document` element at ordinal `0`.

If that element is absent, duplicated, or unresolved, Navigation fails
deterministically.

### 4.2 Permitted entry points

A caller may address:

- the canonical document origin;
- one exact element identity;
- one exact canonical ordinal;
- one exact source locator;
- one exact relation identity;
- the source-boundary reference.

Identity and ordinal resolution return exactly one endpoint or fail.

Locator resolution returns the ordered set of all exact declared elements
whose locators equal the supplied locator. It does not guess among overlapping
or containing locators.

The source-boundary reference is inspectable provenance. It is not a document
element and cannot silently become a content location.

## 5. Traversal model

Navigation is expressed through immutable Navigation Steps.

A step contains:

- navigation identity and version;
- origin endpoint identity;
- current endpoint identity;
- action;
- relation identity when the action follows a relation;
- target endpoint identity;
- availability state;
- blocker when unavailable;
- canonical transition ordinal;
- relation-set lineage;
- provenance and integrity.

Executing or previewing a step does not mutate the Navigation Object or
Relation Set. A later caller may use the target as a new current endpoint.

Slice III defines no persistent cursor, session history, back stack, or Human
preference model.

## 6. Canonical navigation actions

Slice III permits exactly these actions:

| Action | Required basis | Result |
|---|---|---|
| `open_origin` | Canonical document endpoint | Resolve document root |
| `resolve_identity` | Exact endpoint identity | Resolve that endpoint |
| `resolve_ordinal` | Exact canonical ordinal | Resolve that element endpoint |
| `resolve_locator` | Exact declared locator | Return canonically ordered exact matches |
| `next` | `immediately_precedes` relation | Move to the adjacent canonical element |
| `previous` | `immediately_follows` relation | Move to the adjacent canonical element |
| `follow_relation` | Exact traversable relation identity | Move according to declared direction |
| `inspect_source_reference` | `source_reference` relation | Resolve the immutable source-boundary reference |
| `return_to_origin` | Canonical document endpoint | Resolve document root |

`follow_relation` applies to `same_element_kind`, `same_heading_level`, and
accepted `declared_cross_reference` edges as well as directed ordinal edges.

For symmetric relations, the target is the opposite endpoint. For directed
relations, traversal is allowed only in the declared direction unless a
separate inverse relation exists.

## 7. Unavailable navigation

Unavailable movement is explicit, not omitted ambiguously.

An unavailable transition declaration contains:

- attempted action;
- current endpoint;
- required relation type;
- availability state `unavailable`;
- deterministic blocker code;
- relation-set reference.

Canonical blocker codes are:

| Blocker | Meaning |
|---|---|
| `endpoint_not_declared` | Requested identity or ordinal does not resolve |
| `locator_not_declared` | No element has the exact locator |
| `relation_not_declared` | Required relation does not exist |
| `direction_not_declared` | Relation exists but not in the requested direction |
| `hierarchy_not_declared` | Parent, child, enter, or leave action has no declared hierarchy |
| `cross_reference_not_declared` | No accepted cross-reference relation exists |
| `source_boundary_only` | Action requires an element but current endpoint is the source boundary |

Unavailable declarations do not create fallback edges.

For the Markdown Structural Representation Profile v1, these actions are
always unavailable:

- enter container;
- leave container;
- move to parent;
- move to child;
- move to sibling.

They remain visible as unavailable only where the Orientation Map needs to
explain the boundary. They are not part of the executable action vocabulary.

## 8. Deterministic ordering

The address index preserves Relation Set endpoint order.

Available transitions are ordered by:

1. source endpoint canonical ordinal;
2. action order from Section 6;
3. relation canonical ordinal;
4. target endpoint canonical ordinal;
5. target endpoint identity;
6. transition identity.

Source-boundary transitions sort after element transitions.

Unavailable transitions are ordered by:

1. current endpoint canonical ordinal;
2. attempted action;
3. blocker code.

Identical Relation Set bytes produce identical Navigation Object bytes.

## 9. Stable identity

Navigation identity is derived only from:

- navigation policy identity and version;
- Structural Relation Set identity, version, and integrity;
- canonical origin identity;
- ordered address index;
- ordered available and unavailable transition declarations.

Navigation Step identity is derived only from:

- Navigation Object identity and version;
- origin and current endpoint identities;
- action;
- exact relation identity when applicable;
- target endpoint identity;
- availability and blocker state.

No clock, random value, locale, interface state, Human profile, or prior
interaction affects identity.

## 10. Navigation boundaries

Navigation may:

- resolve exact declared references;
- expose accepted relation traversal;
- preserve direction;
- return deterministic ordered matches;
- expose unavailable movement explicitly.

Navigation must never:

- add, remove, reverse, merge, or relabel a relation;
- create a relation from a requested movement;
- infer hierarchy from locators or order;
- rank paths or choose a preferred route;
- recommend a next step;
- search source content;
- interpret endpoint meaning;
- persist a Human's path;
- mutate an Orientation Map.

## 11. Provenance

Every available step resolves through:

```text
Navigation Step
        ↓
Navigation transition declaration
        ↓
Validated relation identity and basis
        ↓
Immutable endpoint declaration
        ↓
Inventory and Representation lineage
        ↓
Confirmed source identity and revision
```

Every unavailable step resolves to the exact missing declaration and blocker.

## 12. External navigation conformance

An external validator verifies:

- exact Relation Set identity and integrity;
- canonical origin;
- endpoint and relation resolution;
- action-to-relation compatibility;
- direction preservation;
- transition identity and order;
- exact locator-match behavior;
- unavailable blocker correctness;
- deterministic replay;
- absence of recommendation, ranking, semantic, and session fields.

Validation does not execute navigation on behalf of the Human and does not
repair missing transitions.

## 13. Acceptance conditions

Navigation architecture is implementable only if:

- the input is one externally conformant immutable Relation Set;
- every available step cites one exact accepted relation or canonical origin;
- every target resolves to the immutable endpoint registry;
- direction and inverse behavior are explicit;
- canonical entry points resolve deterministically;
- hierarchical actions remain unavailable for Profile v1;
- identical input bytes produce identical Navigation Object bytes;
- Relations remains byte-identical and unmodified;
- no route selection, recommendation, semantic interpretation, or persistence
  occurs.
