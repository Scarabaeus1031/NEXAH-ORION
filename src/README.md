# ORION Runtime Source

`orion/` contains the Phase 1A executable architecture slice, the Phase 1B local
Ollama adapter, the Phase 2A deterministic repository context builder, the Phase
2B document selector, the Phase 2C content-free Context Brief, the Phase 4A
Transformation Engine, the Phase 5A declarative Operator Registry, and the Phase
6B deterministic LYRA language boundary. Its
internal contracts, explicit representation graph, selection and context
components, backend ports, adapters, validators, plans, reports, language
projections, and executors are ORION-owned.

Only versioned scope-to-path rules, explicit read-only document loading, and
deterministic content-free brief projection are authorized for context in this
phase. The Engine may plan registered representation transitions, copy operator
metadata and report blockers, but may not select or execute operators or
renderers. No prompt renderer, additional provider, semantic retrieval pipeline,
persistence layer, or Kernel command is authorized.

`orion/lyra/` owns translation and explanation only. The ORION-owned
`lyra_execution.py` composition delegates planning to the unchanged
Transformation Engine and returns the exact report alongside its explanation.

This responsibility layout is frozen by the
[`ORION v1 Architecture Baseline`](../docs/architecture/ORION_V1_ARCHITECTURE_FREEZE.md).
Operator, Renderer and Reflection extensions may not change it without explicit
Architecture Review and an accepted ADR.
