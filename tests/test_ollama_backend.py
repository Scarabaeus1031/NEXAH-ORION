"""Unit tests for the local Ollama ReasoningBackend adapter."""

from __future__ import annotations

import json
import math
import unittest
from unittest.mock import patch
from urllib.error import URLError

from orion import (
    ContextEntry,
    ContextManifest,
    OrientationExecutor,
    OrientationRequest,
    ReasoningBackend,
)
from orion.contracts import ReasoningResult
from orion.ollama_backend import (
    OllamaBackend,
    ReasoningBackendError,
    ReasoningBackendResponseError,
    ReasoningBackendTimeoutError,
    ReasoningBackendUnavailableError,
)


class StubHTTPResponse:
    def __init__(self, payload: bytes) -> None:
        self.payload = payload

    def __enter__(self) -> "StubHTTPResponse":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        return None

    def read(self, size: int = -1) -> bytes:
        return self.payload if size < 0 else self.payload[:size]


def orientation_request() -> OrientationRequest:
    return OrientationRequest(
        request_id="req-ollama-unit",
        objective="Review the supplied architecture statement.",
        requested_by="unit-test",
        scope=("architecture",),
    )


def context_manifest(request: OrientationRequest) -> ContextManifest:
    return ContextManifest.create(
        request,
        (
            ContextEntry.create(
                entry_id="architecture-principle",
                owner="ORION",
                source_ref="docs/architecture/ORION_ARCHITECTURE.md",
                revision="phase-1b",
                content=(
                    "The model proposes. The Orchestrator validates. "
                    "The Kernel decides."
                ),
            ),
        ),
    )


def successful_provider_response() -> bytes:
    candidate = {
        "output": "The statement preserves separation of authority.",
        "claims": [
            {
                "claim_id": "claim-authority",
                "text": "The Kernel retains decision authority.",
                "evidence_refs": ["architecture-principle"],
            }
        ],
    }
    return json.dumps(
        {
            "model": "llama3.1:8b",
            "message": {"role": "assistant", "content": json.dumps(candidate)},
            "done": True,
            "provider_only_field": "must not escape",
        }
    ).encode("utf-8")


class OllamaBackendConfigurationTests(unittest.TestCase):
    def test_configuration_is_normalized(self) -> None:
        backend = OllamaBackend(
            model=" llama3.1:8b ",
            endpoint="http://localhost:11434/",
            timeout=7,
        )

        self.assertEqual(backend.model, "llama3.1:8b")
        self.assertEqual(backend.endpoint, "http://localhost:11434")
        self.assertEqual(backend.timeout, 7.0)
        self.assertEqual(backend.backend_id, "ollama/llama3.1:8b")
        self.assertIsInstance(backend, ReasoningBackend)

    def test_invalid_configuration_is_rejected(self) -> None:
        invalid_configurations = (
            {"model": ""},
            {"model": "llama3.1:8b", "timeout": 0},
            {"model": "llama3.1:8b", "timeout": math.inf},
            {"model": "llama3.1:8b", "endpoint": "http://example.com:11434"},
            {"model": "llama3.1:8b", "endpoint": "file:///tmp/ollama"},
            {
                "model": "llama3.1:8b",
                "endpoint": "http://127.0.0.1:11434/api",
            },
        )
        for configuration in invalid_configurations:
            with self.subTest(configuration=configuration):
                with self.assertRaises(ValueError):
                    OllamaBackend(**configuration)


class OllamaBackendUnitTests(unittest.TestCase):
    def setUp(self) -> None:
        self.request = orientation_request()
        self.context = context_manifest(self.request)
        self.backend = OllamaBackend(model="llama3.1:8b", timeout=4)

    @patch("orion.ollama_backend._open_local")
    def test_provider_response_is_mapped_to_neutral_result(self, mock_open) -> None:
        mock_open.return_value = StubHTTPResponse(successful_provider_response())

        result = self.backend.reason(self.request, self.context)

        self.assertIsInstance(result, ReasoningResult)
        self.assertEqual(result.backend_id, "ollama/llama3.1:8b")
        self.assertEqual(result.request_id, self.request.request_id)
        self.assertEqual(result.manifest_id, self.context.manifest_id)
        self.assertEqual(result.claims[0].evidence_refs, ("architecture-principle",))
        self.assertFalse(hasattr(result, "provider_only_field"))

        transport_request = mock_open.call_args.args[0]
        payload = json.loads(transport_request.data.decode("utf-8"))
        self.assertEqual(transport_request.full_url, "http://127.0.0.1:11434/api/chat")
        self.assertEqual(mock_open.call_args.kwargs["timeout"], 4.0)
        self.assertEqual(payload["model"], "llama3.1:8b")
        self.assertFalse(payload["stream"])
        self.assertEqual(
            payload["format"]["properties"]["claims"]["items"]["properties"]
            ["evidence_refs"]["items"]["enum"],
            ["architecture-principle"],
        )

    @patch("orion.ollama_backend._open_local", side_effect=TimeoutError)
    def test_timeout_is_translated_to_neutral_error(self, mock_open) -> None:
        with self.assertRaises(ReasoningBackendTimeoutError):
            self.backend.reason(self.request, self.context)

        self.assertEqual(mock_open.call_args.kwargs["timeout"], 4.0)

    @patch(
        "orion.ollama_backend._open_local",
        side_effect=URLError(ConnectionRefusedError()),
    )
    def test_unreachable_runtime_fails_with_neutral_backend_error(
        self,
        mock_open,
    ) -> None:
        with self.assertRaises(ReasoningBackendUnavailableError) as raised:
            self.backend.reason(self.request, self.context)

        self.assertIsInstance(raised.exception, ReasoningBackendError)
        self.assertEqual(
            str(raised.exception),
            "local reasoning runtime is not reachable",
        )
        mock_open.assert_called_once()

    def test_malformed_provider_responses_are_rejected(self) -> None:
        malformed_responses = (
            b"not-json",
            json.dumps({"done": True}).encode("utf-8"),
            json.dumps(
                {
                    "model": "llama3.1:8b",
                    "done": True,
                    "message": {"role": "assistant", "content": "not-json"},
                }
            ).encode("utf-8"),
            json.dumps(
                {
                    "model": "llama3.1:8b",
                    "done": True,
                    "message": {
                        "role": "assistant",
                        "content": json.dumps({"output": "text", "claims": []}),
                    }
                }
            ).encode("utf-8"),
        )
        for response in malformed_responses:
            with self.subTest(response=response):
                with patch(
                    "orion.ollama_backend._open_local",
                    return_value=StubHTTPResponse(response),
                ):
                    with self.assertRaises(ReasoningBackendResponseError):
                        self.backend.reason(self.request, self.context)

    @patch("orion.ollama_backend._open_local")
    def test_backend_cannot_bypass_independent_validation(self, mock_open) -> None:
        candidate = {
            "output": "Unsupported candidate.",
            "claims": [
                {
                    "claim_id": "claim-unknown",
                    "text": "This claim cites missing evidence.",
                    "evidence_refs": ["missing-context"],
                }
            ],
        }
        mock_open.return_value = StubHTTPResponse(
            json.dumps(
                {
                    "model": "llama3.1:8b",
                    "done": True,
                    "message": {
                        "role": "assistant",
                        "content": json.dumps(candidate),
                    },
                }
            ).encode("utf-8")
        )

        response = OrientationExecutor(self.backend).execute(
            self.request,
            self.context.entries,
        )

        self.assertFalse(response.validated)
        self.assertIsNone(response.candidate_output)
        self.assertEqual(response.claims, ())
        self.assertIn("claim_evidence_unknown", response.validation.errors[0])


if __name__ == "__main__":
    unittest.main()
