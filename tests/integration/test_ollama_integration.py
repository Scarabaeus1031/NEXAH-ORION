"""Opt-in integration test against the local Ollama runtime."""

from __future__ import annotations

import os
import unittest

from orion.contracts import ContextEntry, OrientationRequest
from orion.executor import OrientationExecutor
from orion.ollama_backend import OllamaBackend


@unittest.skipUnless(
    os.environ.get("ORION_OLLAMA_INTEGRATION") == "1",
    "set ORION_OLLAMA_INTEGRATION=1 to use the local Ollama runtime",
)
class OllamaIntegrationTests(unittest.TestCase):
    def test_complete_orientation_execution(self) -> None:
        request = OrientationRequest(
            request_id="req-ollama-integration",
            objective="Identify who retains canonical decision authority.",
            requested_by="local-integration-test",
            scope=("phase-1b", "authority"),
        )
        context = ContextEntry.create(
            entry_id="architecture-principle",
            owner="ORION",
            source_ref="docs/architecture/ORION_ARCHITECTURE.md",
            revision="phase-1b",
            content=(
                "The model proposes. The Orchestrator validates. "
                "The Kernel decides."
            ),
        )
        backend = OllamaBackend(
            model=os.environ.get("ORION_OLLAMA_MODEL", "llama3.1:8b"),
            endpoint=os.environ.get(
                "ORION_OLLAMA_ENDPOINT", "http://127.0.0.1:11434"
            ),
            timeout=float(os.environ.get("ORION_OLLAMA_TIMEOUT", "180")),
        )

        response = OrientationExecutor(backend).execute(request, (context,))

        self.assertTrue(response.validated, response.validation.errors)
        self.assertEqual(response.backend_id, backend.backend_id)
        self.assertIsNotNone(response.candidate_output)
        self.assertTrue(response.claims)
        self.assertEqual(response.canonical_effects, ())
        for claim in response.claims:
            self.assertTrue(claim.evidence_refs)
            self.assertLessEqual(set(claim.evidence_refs), {"architecture-principle"})


if __name__ == "__main__":
    unittest.main()
