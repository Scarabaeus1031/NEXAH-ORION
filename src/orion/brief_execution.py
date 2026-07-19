"""Phase 2C execution composition with deterministic ContextBrief input."""

from __future__ import annotations

from dataclasses import dataclass, field

from .brief_backend import ContextBriefReasoningBackend
from .context_brief import ContextBriefBuilder
from .context_builder import ContextBuilder, RepositoryContextProvider
from .contracts import OrientationRequest, OrientationResponse, response_id_for
from .document_selector import DocumentSelector, SelectionResult
from .validation import validate_execution


@dataclass(frozen=True, slots=True)
class ContextBriefOrientationExecutor:
    """Select, load, build, brief, reason, and validate without shared ownership."""

    backend: ContextBriefReasoningBackend
    selector: DocumentSelector
    context_provider: RepositoryContextProvider
    brief_builder: ContextBriefBuilder = field(default_factory=ContextBriefBuilder)

    def select(self, request: OrientationRequest) -> SelectionResult:
        return self.selector.select(request)

    def execute(self, request: OrientationRequest) -> OrientationResponse:
        selection = self.select(request)
        manifest = ContextBuilder(
            provider=self.context_provider,
            document_paths=selection.selected_paths,
        ).build(request)
        brief = self.brief_builder.build(manifest)
        result = self.backend.reason(request, brief)
        validation = validate_execution(
            request,
            manifest,
            result,
            expected_backend_id=self.backend.backend_id,
        )
        return OrientationResponse(
            response_id=response_id_for(result, validation),
            request_id=request.request_id,
            manifest_id=manifest.manifest_id,
            backend_id=result.backend_id,
            backend_result_id=result.result_id,
            validated=validation.valid,
            candidate_output=result.output if validation.valid else None,
            claims=result.claims if validation.valid else (),
            provenance=manifest.provenance,
            validation=validation,
        )
