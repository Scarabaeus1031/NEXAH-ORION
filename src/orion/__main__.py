"""Run the complete Phase 1A slice without network access."""

from __future__ import annotations

import json

from .contracts import ContextEntry, OrientationRequest
from .executor import OrientationExecutor
from .fake_backend import FakeBackend


def main() -> int:
    request = OrientationRequest(
        request_id="demo-request-001",
        objective="Prove one complete ORION execution",
        requested_by="local-contributor",
        scope=("phase-1a", "offline"),
    )
    context = ContextEntry.create(
        entry_id="architecture-principle",
        owner="nexah-orion",
        source_ref="docs/architecture/ORION_ARCHITECTURE.md",
        revision="working-tree",
        content="The model proposes. The Orchestrator validates. The Kernel decides.",
    )
    response = OrientationExecutor(FakeBackend()).execute(request, (context,))
    print(json.dumps(response.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if response.validated else 1


if __name__ == "__main__":
    raise SystemExit(main())
