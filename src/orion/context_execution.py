"""Execution composition for request-owned repository context."""

from __future__ import annotations

from dataclasses import dataclass

from .backend import ReasoningBackend
from .context_builder import ContextBuilder
from .contracts import OrientationRequest, OrientationResponse, response_id_for
from .validation import validate_execution


@dataclass(frozen=True, slots=True)
class ContextualOrientationExecutor:
    """Build context, invoke one injected backend, then validate its proposal."""

    backend: ReasoningBackend
    context_builder: ContextBuilder

    def execute(self, request: OrientationRequest) -> OrientationResponse:
        context = self.context_builder.build(request)
        result = self.backend.reason(request, context)
        validation = validate_execution(
            request,
            context,
            result,
            expected_backend_id=self.backend.backend_id,
        )
        return OrientationResponse(
            response_id=response_id_for(result, validation),
            request_id=request.request_id,
            manifest_id=context.manifest_id,
            backend_id=result.backend_id,
            backend_result_id=result.result_id,
            validated=validation.valid,
            candidate_output=result.output if validation.valid else None,
            claims=result.claims if validation.valid else (),
            provenance=context.provenance,
            validation=validation,
        )
