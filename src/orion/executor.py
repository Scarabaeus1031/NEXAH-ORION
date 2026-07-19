"""Thin executor for one complete ORION request."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .backend import ReasoningBackend
from .contracts import (
    ContextEntry,
    ContextManifest,
    OrientationRequest,
    OrientationResponse,
    response_id_for,
)
from .validation import validate_execution


@dataclass(frozen=True, slots=True)
class OrientationExecutor:
    """Coordinates the flow without absorbing backend or validation ownership."""

    backend: ReasoningBackend

    def execute(
        self,
        request: OrientationRequest,
        context_entries: Iterable[ContextEntry],
    ) -> OrientationResponse:
        context = ContextManifest.create(request, context_entries)
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

