# ADR-0004: Immutable Context Manifest

- Status: Accepted
- Date: 2026-07-19
- Decision owner: ORION Architecture
- Affected repositories: nexah-orion, NEXAH Core, NEXAH Library
- Supersedes: none
- Superseded by: none

## Context

Model outputs cannot be inspected or replayed if the selected context, source revisions, omissions, and transformations are unknown.

## Decision

Every reasoning run uses an immutable Context Manifest that records source identities, versions, selected segments or objects, transformations, retrieval decisions, omissions, and digests.

## Ownership and authority

ORION owns the manifest and context assembly record. Source identity and content authority remain with Core, Library, or the declared source owner.

## Consequences

- Prompt caching is an optimization, not the reproducibility record.
- Context summaries retain source references and declared loss.
- Changed context produces a new manifest rather than rewriting the old one.

## Alternatives considered

Storing only final prompts was rejected because prompts cannot reconstruct retrieval decisions or source authority.

## Compatibility and migration

Manifest schema implementation is postponed until the cross-repository source references are owned and versioned.

## Verification

Every future model run must reference one immutable manifest before it can be considered replayable.

## References

- [`../architecture/ORION_ARCHITECTURE.md`](../architecture/ORION_ARCHITECTURE.md)
