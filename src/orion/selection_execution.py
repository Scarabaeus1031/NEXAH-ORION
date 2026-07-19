"""Execution composition for deterministic request-based document selection."""

from __future__ import annotations

from dataclasses import dataclass

from .backend import ReasoningBackend
from .context_builder import ContextBuilder, RepositoryContextProvider
from .context_execution import ContextualOrientationExecutor
from .contracts import OrientationRequest, OrientationResponse
from .document_selector import DocumentSelector, SelectionResult


@dataclass(frozen=True, slots=True)
class SelectingOrientationExecutor:
    """Select paths, delegate manifest creation, then execute one request."""

    backend: ReasoningBackend
    selector: DocumentSelector
    context_provider: RepositoryContextProvider

    def select(self, request: OrientationRequest) -> SelectionResult:
        return self.selector.select(request)

    def execute(self, request: OrientationRequest) -> OrientationResponse:
        selection = self.select(request)
        context_builder = ContextBuilder(
            provider=self.context_provider,
            document_paths=selection.selected_paths,
        )
        return ContextualOrientationExecutor(
            backend=self.backend,
            context_builder=context_builder,
        ).execute(request)
