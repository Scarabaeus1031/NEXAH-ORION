"""Deterministic Version 1.1 Gateway boundary."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from .canonical import canonical_bytes, digest_ref
from .constants import (
    API_VERSION,
    CORE_COMMIT,
    CORE_FINGERPRINT,
    CORE_VERSION,
    MAX_RESPONSE_BYTES,
    RUNTIME_VERSION,
    TERMINAL_STOP,
)
from .contracts import validate_envelope
from .errors import RuntimeBoundaryError
from .manifest import verify_manifest
from .process import WorkerProcess


@dataclass(frozen=True, slots=True)
class GatewayResult:
    body: dict[str, Any]
    request_digest: str
    result_digest: str


class Gateway:
    def __init__(self, worker: WorkerProcess | None = None) -> None:
        self.worker = worker or WorkerProcess()

    def execute(
        self,
        value: object,
        *,
        worker_timeout: float | None = None,
    ) -> GatewayResult:
        envelope, request, request_digest = validate_envelope(value)
        worker_result = self.worker.execute(envelope, timeout=worker_timeout)
        manifest = verify_manifest(worker_result.get("artifact_manifest"))
        terminal_ref = worker_result.get("terminal_certification_ref")
        if (
            terminal_ref != manifest["terminal_artifact_ref"]
            or worker_result.get("terminal_stop") != TERMINAL_STOP
        ):
            raise RuntimeBoundaryError(
                status=500,
                category="output_validation",
                code="artifact_manifest_invalid",
                retry="manual_review",
                detail_refs=("worker_terminal_mismatch",),
            )
        core_release = {
            "version": CORE_VERSION,
            "commit": CORE_COMMIT,
            "fingerprint": CORE_FINGERPRINT,
        }
        result_basis = {
            "api_version": API_VERSION,
            "request_digest": request_digest,
            "core_release": core_release,
            "status": "complete",
            "terminal_stop": TERMINAL_STOP,
            "artifact_manifest": manifest,
            "terminal_certification_ref": terminal_ref,
        }
        result_digest = digest_ref(canonical_bytes(result_basis))
        body = {
            "api_version": API_VERSION,
            "runtime_version": RUNTIME_VERSION,
            "request_id": request.request_id,
            "request_digest": request_digest,
            "result_digest": result_digest,
            "core_release": core_release,
            "status": "complete",
            "terminal_stop": TERMINAL_STOP,
            "artifact_manifest": manifest,
            "terminal_certification_ref": terminal_ref,
        }
        if len(canonical_bytes(body)) > MAX_RESPONSE_BYTES:
            raise RuntimeBoundaryError(
                status=422,
                category="output_validation",
                code="operational_profile_exceeded",
                detail_refs=("success_response_size",),
            )
        return GatewayResult(body, request_digest, result_digest)

    def shutdown(self) -> None:
        self.worker.shutdown()
