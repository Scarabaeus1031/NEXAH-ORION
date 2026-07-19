# ORION Runtime Source

`orion/` contains the Phase 1A executable architecture slice, the Phase 1B local
Ollama adapter, the Phase 2A deterministic repository context builder, the Phase
2B document selector, the Phase 2C content-free Context Brief, and the Phase 4A
Transformation Engine. Its internal contracts, explicit representation graph,
selection and context components, backend ports, adapters, validators, plans,
reports, and executors are ORION-owned.

Only versioned scope-to-path rules, explicit read-only document loading, and
deterministic content-free brief projection are authorized for context in this
phase. Phase 4A may plan registered representation transitions and report their
blockers, but may not execute operators or renderers. No prompt renderer,
additional provider, semantic retrieval pipeline, persistence layer, or Kernel
command is authorized.
