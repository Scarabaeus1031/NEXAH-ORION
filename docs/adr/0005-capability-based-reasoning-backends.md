# ADR-0005: Capability-based Reasoning Backends

- Status: Accepted
- Date: 2026-07-19
- Decision owner: ORION Architecture
- Affected repositories: nexah-orion
- Supersedes: none
- Superseded by: none

## Context

Local and cloud model runtimes differ in structured output, tools, context, multimodality, reproducibility, streaming, errors, and cancellation despite superficial API compatibility.

## Decision

ORION selects Reasoning Backends through declared capabilities and policy. Applications must not branch on provider classes or model names.

## Ownership and authority

ORION owns the Reasoning Backend port and routing policy. Each adapter owns provider translation only. Existing `nexah/backends/` remains the Core's Representation Backend boundary.

## Consequences

- Provider-specific behavior stays in adapters.
- Unknown capabilities fail visibly.
- Backend equality is established through conformance and semantic acceptance, not endpoint shape.

## Alternatives considered

Treating all OpenAI-compatible endpoints as equivalent was rejected because compatibility is partial and behavior remains model-dependent.

## Compatibility and migration

Backend interfaces and adapters are postponed until structured request and result ownership is approved.

## Verification

Future routing depends on capability requirements and policies; provider imports remain within adapter directories.

## References

- [`../architecture/evidence/NEXAH_REASONING_ARCHITECTURE_REVIEW.md`](../architecture/evidence/NEXAH_REASONING_ARCHITECTURE_REVIEW.md)
