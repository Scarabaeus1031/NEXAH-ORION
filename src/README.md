# ORION Runtime Source

`orion/` contains the Phase 1A executable architecture slice and the Phase 1B
local Ollama adapter. Its internal contracts, backend port, adapters, validator,
and executor are ORION-owned.

Only the Ollama provider adapter is authorized in this phase. No additional
provider, retrieval pipeline, persistence layer, or Kernel command is authorized.
