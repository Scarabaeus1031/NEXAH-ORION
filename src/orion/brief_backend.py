"""Provider-neutral reasoning port for content-free ContextBrief input."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from .context_brief import ContextBrief
from .contracts import OrientationRequest, ReasoningResult


@runtime_checkable
class ContextBriefReasoningBackend(Protocol):
    """Additive Phase 2C port; the frozen Phase 1 backend remains unchanged."""

    @property
    def backend_id(self) -> str:
        """Stable runtime identifier used for validation and audit."""

    def reason(
        self,
        request: OrientationRequest,
        context: ContextBrief,
    ) -> ReasoningResult:
        """Return an untrusted result bound to the brief's source manifest."""
