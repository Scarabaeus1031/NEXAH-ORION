"""Single-invocation isolated Core worker."""

from __future__ import annotations

from dataclasses import asdict
import sys

from .adapter import invoke_frozen_core
from .canonical import canonical_bytes, parse_json_bytes
from .errors import RuntimeBoundaryError
from .isolation import install_worker_network_isolation


def main() -> int:
    try:
        envelope = parse_json_bytes(sys.stdin.buffer.read())
        if not isinstance(envelope, dict):
            raise ValueError("worker envelope must be an object")
        install_worker_network_isolation()
        result = invoke_frozen_core(envelope)
        output = {"ok": True, "result": asdict(result)}
    except RuntimeBoundaryError as exc:
        output = {
            "ok": False,
            "error": {
                "status": exc.status,
                "category": exc.category,
                "code": exc.code,
                "retry": exc.retry,
                "detail_refs": list(exc.detail_refs),
            },
        }
    except Exception:
        output = {
            "ok": False,
            "error": {
                "status": 500,
                "category": "core_invocation",
                "code": "core_worker_failed",
                "retry": "manual_review",
                "detail_refs": [],
            },
        }
    sys.stdout.buffer.write(canonical_bytes(output))
    sys.stdout.buffer.write(b"\n")
    return 0 if output["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
