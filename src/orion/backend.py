"""Replaceable ReasoningBackend port."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from .contracts import ContextManifest, OrientationRequest, ReasoningResult


@runtime_checkable
class ReasoningBackend(Protocol):
    """Minimal inference boundary owned by ORION."""

    @property
    def backend_id(self) -> str:
        """Stable runtime identifier used for validation and audit."""

    def reason(
        self,
        request: OrientationRequest,
        context: ContextManifest,
    ) -> ReasoningResult:
        """Return an untrusted candidate result for later validation."""

