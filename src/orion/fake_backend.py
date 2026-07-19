"""Deterministic offline backend used only to prove the execution boundary."""

from __future__ import annotations

from .contracts import (
    ContextManifest,
    OrientationRequest,
    ReasoningClaim,
    ReasoningResult,
    result_id_for,
)


class FakeBackend:
    """A replaceable backend with no network, SDK, model, or hidden state."""

    @property
    def backend_id(self) -> str:
        return "fake-backend/0.1"

    def reason(
        self,
        request: OrientationRequest,
        context: ContextManifest,
    ) -> ReasoningResult:
        evidence_refs = tuple(entry.entry_id for entry in context.entries)
        output = (
            f"Fake execution completed for '{request.objective}' "
            f"with {len(context.entries)} provenance-bound context item(s)."
        )
        claim = ReasoningClaim(
            claim_id="claim-execution-boundary",
            text="The request traversed the complete offline ORION boundary.",
            evidence_refs=evidence_refs,
        )
        return ReasoningResult(
            result_id=result_id_for(
                request_id=request.request_id,
                manifest_id=context.manifest_id,
                backend_id=self.backend_id,
            ),
            request_id=request.request_id,
            manifest_id=context.manifest_id,
            backend_id=self.backend_id,
            output=output,
            claims=(claim,),
        )

