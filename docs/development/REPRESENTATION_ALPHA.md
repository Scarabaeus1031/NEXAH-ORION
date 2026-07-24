# ORION Representation Alpha

- Status: implemented
- Profile: exact Human-confirmed local text
- Projection: `orion.projection/exact-text@0.1-alpha`
- Renderer: `orion.renderer/exact-text@0.1-alpha`
- Public contract impact: none
- Effects: none

## Purpose

This implementation proves one bounded capability:

```text
confirmed, pre-resolved local text
→ deterministic exact-text Projection
→ versioned Renderer
→ immutable Representation
→ external conformance validation
```

It implements the first executable part of the accepted ORION Representation
Architecture. It does not perform Orientation and does not change the frozen
Version 1 Runtime, Gateway, public contracts or validators.

## Implemented profile

The source fixture is exact UTF-8 text owned and confirmed by a Human. The
source is already resolved before it enters the Renderer boundary. Its source
version is the SHA-256 digest of the exact UTF-8 content.

The exact-text Projection:

- selects the declared whole-text fragment;
- preserves the exact text and media type;
- adds no concepts, labels, classification or meaning;
- declares `none` as lossiness.

The Renderer is a pure in-process function. It performs no file I/O, retrieval,
reasoning, Evidence classification, Orientation or report binding.

The resulting Representation records:

- Orientation Object identity and version;
- exact source identity, version and content digest;
- fragment identity;
- Projection identity and version;
- Renderer identity and version;
- exact payload and payload integrity;
- ordered Human-confirmation and deterministic-projection provenance;
- declared lossiness;
- content-addressed Representation identity and version.

External conformance reruns the Renderer and verifies exact equality, source
trace-back, payload integrity, identity preservation, Renderer and Projection
identity, lossiness, and the absence of Evidence or report-binding semantics.

## Run the proof

From the repository root:

```bash
python3 scripts/representation_alpha_proof.py
```

The command prints the resolved source identity, complete immutable
Representation and every conformance check. It exits non-zero when conformance
fails.

The isolated tests run through the existing repository command:

```bash
./scripts/test
```

## Ownership

- The Human owns the fixture content and confirmation.
- The source is pre-resolved; ORION does not claim source or Library authority.
- ORION owns the exact-text Projection, Renderer and Representation.
- Conformance is external to the Renderer.
- No output is Evidence.

The module is intentionally absent from the root `orion` public exports. It is
an internal Alpha implementation profile, not a Version 1 public contract.

## Deferred

The Alpha does not implement:

- NEXAHEDRON transport or live Workspace integration;
- Library resolution, ingestion or editorial authority;
- Source Evidence or Evidence Binding;
- Orientation, Orientation Reports or Continuations;
- LYRA;
- PDF, URL or Markdown parsing;
- semantic retrieval, search, embeddings or LLM providers;
- NTO, Projection mathematics or alternative reference frames;
- a general Renderer framework, SDK or ecosystem.

No deferred capability is simulated by this proof.
