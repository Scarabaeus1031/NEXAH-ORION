# Cross-Repository Governance

## Principle

No repository may grant itself authority over another repository's contract or canonical state.

## Change classes

| Class | Examples | Required record |
|---|---|---|
| Internal | documentation layout, private helper | local PR |
| Public-compatible | additive optional field, new read-only capability | local ADR or compatibility note as defined by owner |
| Cross-repository | request schema, Core port, Library query contract | ADR plus acknowledgments from affected owners |
| Breaking | removed field, changed invariant, changed authority | major version decision in every affected contract owner |
| Effect-bearing | Kernel command, Library publication, external write | effect policy, human approval and external owner decision |

## Proposal workflow

```text
need identified
→ owning repository named
→ ADR proposed in contract-owning repository
→ consumer impact recorded
→ affected owners acknowledge
→ contract version and migration window agreed
→ implementation proceeds independently per repository
→ compatibility matrix updated
→ release order executed
```

## Contract ownership

- The producer of a public contract normally owns its schema and version.
- Consumers own adapters to that contract unless a separate shared-contract repository is explicitly approved.
- ORION does not copy external types and then treat the copies as authoritative.
- A shared schema repository is not created until duplication and release pressure demonstrate the need.

## Required cross-repository record

Every cross-repository change records:

- contract owner;
- producer and consumers;
- previous and next versions;
- compatibility classification;
- rollout and rollback order;
- minimum supported revisions;
- deprecation date when applicable;
- approval from affected owners.

Use [`docs/templates/cross-repository-change.md`](../templates/cross-repository-change.md).

## Release order

Default order for an additive contract change:

1. contract owner publishes compatible producer behavior;
2. consumers add support while retaining the previous version;
3. compatibility is verified across pinned revisions;
4. defaults may move only after all required consumers are ready;
5. removal occurs only in a later major version.

Effect-bearing changes additionally require the human authority of the affected system.

## Frozen Core rule

The pinned NEXAH Core baseline is read-only. If ORION discovers a missing Core capability, the first output is a proposal to the Core owner. ORION must not patch, vendor, monkey-patch, or reinterpret the frozen Core to proceed.
