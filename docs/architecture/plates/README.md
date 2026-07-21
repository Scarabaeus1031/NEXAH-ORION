# Canonical Architecture Plates

Architecture Plates are generated artifacts and visual companions to the
authoritative Markdown architecture. SVG files are the canonical editable
sources. PNG files are generated for repository documentation and must never be
edited directly. Each plate documents exactly one stable concept. A plate cannot
introduce a transition, operator, invariant, authority or lifecycle state that
is absent from its source document.

If a Plate changes:

1. Edit the SVG source.
2. Regenerate the PNG.
3. Review both the Markdown and the Plate.

Plate 08 and its embedding in the LYRA architecture were reviewed against the
Phase 6B executable boundary. Its flow remains descriptive: LYRA translates;
ORION retains planning authority.

## Canonical collection

| Plate | File | Concept | Authoritative document | Caption | Source |
|---:|---|---|---|---|---|
| 01 | [`01_system_perspective.png`](01_system_perspective.png) | System Perspective | [`ORION_ARCHITECTURE.md`](../ORION_ARCHITECTURE.md) | NEXAH defines the Orientation Space, ORION navigates it, and LYRA makes it accessible to human language. | deterministic SVG |
| 02 | [`02_orientation_workflow.png`](02_orientation_workflow.png) | Orientation Workflow | [`ORION_ARCHITECTURE.md`](../ORION_ARCHITECTURE.md) | Orientation moves from observation through differentiation and connection toward a preserved, shareable result. | deterministic SVG |
| 03 | [`03_representation_architecture.png`](03_representation_architecture.png) | Representation Architecture | [`REPRESENTATION_ARCHITECTURE.md`](../REPRESENTATION_ARCHITECTURE.md) | One Orientation Object may have many immutable representations without changing its identity. | deterministic SVG |
| 04 | [`04_representation_graph.png`](04_representation_graph.png) | Representation Graph | [`REPRESENTATION_GRAPH.md`](../transformations/REPRESENTATION_GRAPH.md) | The Representation Graph contains only the fifteen explicitly registered T01–T15 transitions. | deterministic SVG |
| 05 | [`05_transition_contract_anatomy.png`](05_transition_contract_anatomy.png) | Transition Contract | [`TRANSITION_CONTRACT_SPECIFICATION.md`](../transformations/contracts/TRANSITION_CONTRACT_SPECIFICATION.md) | Every registered graph edge has an inspectable contract declaring inputs, invariants, evidence and loss. | deterministic SVG |
| 06 | [`06_transformation_engine.png`](06_transformation_engine.png) | Transformation Engine | [`PHASE_4A_TRANSFORMATION_ENGINE.md`](../../development/PHASE_4A_TRANSFORMATION_ENGINE.md) | The Transformation Engine plans registered routes and reports blockers without executing transformations. | deterministic SVG |
| 07 | [`07_operator_registry.png`](07_operator_registry.png) | Operator Registry | [`OPERATOR_ARCHITECTURE.md`](../operators/OPERATOR_ARCHITECTURE.md) | The Operator Registry inventories known capabilities without selecting, loading or executing them. | deterministic SVG |
| 08 | [`08_lyra_language_layer.png`](08_lyra_language_layer.png) | LYRA Language Layer | [`LYRA_ARCHITECTURE.md`](../lyra/LYRA_ARCHITECTURE.md) | LYRA translates between human language and ORION without changing deterministic decisions. | deterministic SVG |
| 09 | [`09_documentation_projections.png`](09_documentation_projections.png) | Documentation Projections | [`ADR-0007`](../../adr/0007-five-documentation-projections.md) | Poster, Map, Blueprint, Specification and Atlas are coordinated views of one architecture release. | deterministic SVG |
| 10 | [`10_evidence_inference_boundary.png`](10_evidence_inference_boundary.png) | Evidence/Inference Boundary | [`ORION_ARCHITECTURE.md`](../ORION_ARCHITECTURE.md) | NEXAH supports expressive representations while keeping inference bounded by evidence. | deterministic SVG |

All ten entries are canonical companions for repository version
`0.3.0-dev.0`. “Canonical” applies to their documentation role, not to any
mathematical or scientific claim.

Phase F1 reviewed all ten SVG → PNG pairs against their authoritative Markdown
and ADRs. No Plate required a content change. The collection is frozen as part
of [`orion-architecture-v1`](../ORION_V1_ARCHITECTURE_FREEZE.md); a future
material change follows ADR-0008 review rules.

## Authority and review rules

1. Markdown and accepted ADRs remain authoritative.
2. Every plate has one primary concept and one authoritative source document.
3. A material source-document change requires review of its plate in the same
   change set.
4. A plate never upgrades `unknown` or `candidate` evidence, implies execution,
   or fills an undocumented edge.
5. Temporary roadmaps, phase next steps and speculative mathematics do not
   belong in canonical plates.
6. Replaced variants are retired rather than kept as parallel canonical views.
7. LUCY remains a reserved boundary until a separate architecture decision
   defines it.

## Sources and rendering

The canonical editable sources for all ten plates live in [`src/`](src/).
Regenerate every PNG with:

```bash
./scripts/generate-architecture-plates
```

`rsvg-convert` is a documentation build tool, not an ORION runtime dependency.
The generator reads SVG files and writes PNG files only; it never rewrites a
canonical SVG source.

Historical candidates are intentionally not stored in this directory. They are
evidence of visual evolution, not competing specifications.
