# ORION Tests

This directory owns Phase 1A contract and execution tests, Phase 1B Ollama adapter
tests, Phase 2A context-builder tests, Phase 2B document-selection tests, Phase 2C
Context Brief tests, Phase 4A Transformation Engine planning tests, Phase 5A
Operator Registry boundary tests, Phase 6B deterministic LYRA round-trip tests,
and opt-in local integration tests. Core tests remain in the NEXAH Core
repository; ORION tests do not duplicate Core authority.

The Phase F1 baseline treats these tests as architecture conformance evidence.
New extension tests may add coverage but must not silently redefine frozen
responsibilities or terminology.
