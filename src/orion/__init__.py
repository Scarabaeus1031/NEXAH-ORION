"""Minimal, offline ORION execution boundary."""

from .backend import ReasoningBackend
from .contracts import (
    ContextEntry,
    ContextManifest,
    OrientationRequest,
    OrientationResponse,
    ProvenanceRef,
    ReasoningClaim,
    ReasoningResult,
    ValidationReport,
)
from .executor import OrientationExecutor
from .fake_backend import FakeBackend
from .ollama_backend import (
    OllamaBackend,
    ReasoningBackendError,
    ReasoningBackendResponseError,
    ReasoningBackendTimeoutError,
    ReasoningBackendUnavailableError,
)
from .validation import validate_execution

__all__ = [
    "ContextEntry",
    "ContextManifest",
    "FakeBackend",
    "OrientationExecutor",
    "OrientationRequest",
    "OrientationResponse",
    "OllamaBackend",
    "ProvenanceRef",
    "ReasoningBackend",
    "ReasoningBackendError",
    "ReasoningBackendResponseError",
    "ReasoningBackendTimeoutError",
    "ReasoningBackendUnavailableError",
    "ReasoningClaim",
    "ReasoningResult",
    "ValidationReport",
    "validate_execution",
]

__version__ = "0.3.0.dev0"
