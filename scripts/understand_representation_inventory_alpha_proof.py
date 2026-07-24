#!/usr/bin/env python3
"""Run the UNDERSTAND Declared Representation Inventory Alpha proof."""

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
from orion.understand_representation_inventory_alpha import (
    inventory_declared_representation,
)
from orion.understand_stage1_alpha import UnderstandStage1BindingDiagnostic


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_NEXAHEDRON_ROOT = ROOT.parent / "NEXAHEDRON"
STAGE1_PROOF_SHA256 = (
    "b3d845ea91ae4bd0af295ff9237a13189f86e27114c769ca7d6ac431ab1b1723"
)


class _PayloadAccessGuard(dict[str, Any]):
    """Fail if the inventory attempts to open the Representation payload."""

    def get(self, key: str, default: object = None) -> object:
        if key == "payload":
            raise RuntimeError("Representation payload access is forbidden")
        return super().get(key, default)


def _run(
    command: list[str],
    *,
    cwd: Path,
    environment: dict[str, str],
) -> tuple[dict[str, Any], str]:
    result = subprocess.run(
        command,
        cwd=cwd,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"proof failed: {command[-1]}")
    return json.loads(result.stdout), result.stdout


def _run_nexahedron(
    root: Path,
    script: str,
    environment: dict[str, str],
) -> dict[str, Any]:
    value, _ = _run(
        [
            "node",
            "--no-warnings",
            "--experimental-strip-types",
            script,
        ],
        cwd=root,
        environment=environment,
    )
    return value


def main() -> int:
    nexahedron_root = Path(
        os.environ.get("NEXAHEDRON_ROOT", DEFAULT_NEXAHEDRON_ROOT)
    ).resolve()
    environment = os.environ.copy()
    environment["ORION_SOURCE_PATH"] = str(ROOT / "src")
    environment["PYTHONPATH"] = str(ROOT / "src")
    try:
        stage1_proof, stage1_stdout = _run(
            [sys.executable, "scripts/understand_stage1_alpha_proof.py"],
            cwd=ROOT,
            environment=environment,
        )
        stage1_hash = sha256(stage1_stdout.encode("utf-8")).hexdigest()
        if stage1_hash != STAGE1_PROOF_SHA256:
            raise ValueError("UNDERSTAND Stage 1 proof hash mismatch")
        stage1 = UnderstandStage1BindingDiagnostic(**stage1_proof["binding"])

        handoff = _run_nexahedron(
            nexahedron_root,
            "scripts/representation-alpha-handoff.mjs",
            environment,
        )
        request_proof = _run_nexahedron(
            nexahedron_root,
            "scripts/representation-referenced-request.mjs",
            environment,
        )
        request = construct_orientation_request(request_proof["request"])
        representation = _PayloadAccessGuard(handoff["representation"])
        inventory = inventory_declared_representation(
            request,
            stage1,
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
        print(
            f"[UNDERSTAND Declared Representation Inventory Alpha] {error}",
            file=sys.stderr,
        )
        return 1

    proof = {
        "diagnostic_kind": "internal_declared_representation_inventory",
        "input_hashes": {
            "representation_sha256":
                handoff["representation"]["representation_sha256"],
            "request_proof_sha256":
                "06135ecd0c212605840a7fd31e8cc2492494a58a11af89eeb8b335d43635167d",
            "stage1_proof_sha256": stage1_hash,
        },
        "inventory": asdict(inventory),
        "payload_accessed": False,
        "semantic_processing": "none",
        "source_structure_inspected": False,
        "stage_completed": False,
        "stop": "before_source_structure_inventory",
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
