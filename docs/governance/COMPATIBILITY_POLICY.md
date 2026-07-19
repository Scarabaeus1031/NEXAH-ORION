# Compatibility Policy

## Compatibility surfaces

ORION tracks compatibility independently for:

- NEXAH Core contracts and baseline revision;
- Library query/read contracts;
- Builder Hub request/result contracts;
- Reasoning backend capabilities;
- persisted ORION Run Records and Context Manifests;
- command proposal schemas.

Compatibility in one surface does not imply compatibility in another.

## Classification

| Level | Meaning |
|---|---|
| Exact | identical schema and declared behavior |
| Backward compatible | new producer works with supported existing consumers |
| Forward tolerable | old consumer safely ignores or rejects a new optional feature |
| Adapter required | explicit version adapter preserves meaning and boundaries |
| Incompatible | migration or coordinated major release required |
| Unknown | not tested; must not be claimed compatible |

## Matrix location

Release candidates record tested combinations in `docs/releases/compatibility/`. The template is [`docs/templates/compatibility-matrix.yaml`](../templates/compatibility-matrix.yaml).

The development manifest `workspace.yaml` pins the current Core baseline but is not a substitute for a release compatibility matrix.

## Deprecation

- Deprecation requires an accepted ADR.
- The replacement and migration path must exist before the warning period begins.
- A deprecated public contract remains supported for at least one minor release unless security or authority integrity requires faster removal.
- Removal is a major-version change.

## Failure behavior

Unknown or incompatible versions fail visibly. ORION must not silently coerce identifiers, evidence roles, authority, or effect classes to make a request appear compatible.
