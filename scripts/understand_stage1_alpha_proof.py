#!/usr/bin/env python3
"""Run the cross-repository UNDERSTAND Stage 1 Binding Alpha proof."""

from __future__ import annotations

from dataclasses import asdict
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any

from orion.gateway.translation import construct_orientation_request
from orion.readiness_alpha import prove_runtime_readiness
from orion.understand_stage1_alpha import bind_understand_stage1


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_NEXAHEDRON_ROOT = ROOT.parent / "NEXAHEDRON"


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _run_nexahedron_proof(root: Path, script: str) -> dict[str, Any]:
    environment = os.environ.copy()
    environment["ORION_SOURCE_PATH"] = str(ROOT / "src")
    result = subprocess.run(
        [
            "node",
            "--no-warnings",
            "--experimental-strip-types",
            script,
        ],
        cwd=root,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(
            result.stderr.strip() or f"NEXAHEDRON proof failed: {script}"
        )
    return json.loads(result.stdout)


def main() -> int:
    nexahedron_root = Path(
        os.environ.get("NEXAHEDRON_ROOT", DEFAULT_NEXAHEDRON_ROOT)
    ).resolve()
    try:
        handoff = _run_nexahedron_proof(
            nexahedron_root,
            "scripts/representation-alpha-handoff.mjs",
        )
        request_proof = _run_nexahedron_proof(
            nexahedron_root,
            "scripts/representation-referenced-request.mjs",
        )
        representation = handoff["representation"]
        request = construct_orientation_request(request_proof["request"])
        readiness = prove_runtime_readiness(request)
        binding = bind_understand_stage1(
            request,
            readiness,
            representation,
        )
    except (
        KeyError,
        OSError,
        TypeError,
        ValueError,
        RuntimeError,
        json.JSONDecodeError,
    ) as error:
        print(f"[UNDERSTAND Stage 1 Binding Alpha] {error}", file=sys.stderr)
        return 1

    proof = {
        "binding": asdict(binding),
        "diagnostic_kind": "internal_understand_stage1_binding",
        "input_hashes": {
            "representation_sha256": representation["representation_sha256"],
            "request_sha256": sha256(
                _canonical_bytes(asdict(request))
            ).hexdigest(),
            "runtime_readiness_proof_sha256":
                "dd8547f2e4b110e992ebb99079dd7d39a73f8da98e814b0dd9a1d347fc07eaf1",
        },
        "semantic_processing": "none",
        "stages_completed": ["understand/1"],
        "stop": "before_understand/2",
    }
    print(
        json.dumps(
            proof,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
