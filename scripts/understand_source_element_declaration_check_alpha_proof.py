#!/usr/bin/env python3
"""Run the UNDERSTAND source-element declaration check Alpha proof."""

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
    DeclaredRepresentationInventoryDiagnostic,
    DeclaredRepresentationInventoryEntry,
)
from orion.understand_source_boundary_inventory_alpha import (
    DeclaredSourceBoundaryEntry,
    DeclaredSourceBoundaryInventoryDiagnostic,
)
from orion.understand_source_element_declaration_check_alpha import (
    check_declared_source_element_declaration,
)
from orion.understand_stage1_alpha import UnderstandStage1BindingDiagnostic


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_NEXAHEDRON_ROOT = ROOT.parent / "NEXAHEDRON"
STAGE1_PROOF_SHA256 = (
    "b3d845ea91ae4bd0af295ff9237a13189f86e27114c769ca7d6ac431ab1b1723"
)
REPRESENTATION_INVENTORY_PROOF_SHA256 = (
    "54469b52ac2fb4b3fc1d72b8da9b2d4b731b3023158151a1b75281e11fba3b2b"
)
BOUNDARY_INVENTORY_PROOF_SHA256 = (
    "9b639edffc15bec1d5d6acd83658f845c8e01c31227fdae20a277c2d39f3dbe1"
)
REQUEST_PROOF_SHA256 = (
    "06135ecd0c212605840a7fd31e8cc2492494a58a11af89eeb8b335d43635167d"
)


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


def _representation_inventory(
    value: dict[str, Any],
) -> DeclaredRepresentationInventoryDiagnostic:
    entries = tuple(
        DeclaredRepresentationInventoryEntry(
            **{
                **entry,
                "declared_lossiness": tuple(entry["declared_lossiness"]),
            }
        )
        for entry in value["representations"]
    )
    return DeclaredRepresentationInventoryDiagnostic(
        **{**value, "representations": entries}
    )


def _boundary_inventory(
    value: dict[str, Any],
) -> DeclaredSourceBoundaryInventoryDiagnostic:
    boundaries = tuple(
        DeclaredSourceBoundaryEntry(**boundary)
        for boundary in value["boundaries"]
    )
    return DeclaredSourceBoundaryInventoryDiagnostic(
        **{**value, "boundaries": boundaries}
    )


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

        representation_proof, representation_stdout = _run(
            [
                sys.executable,
                "scripts/understand_representation_inventory_alpha_proof.py",
            ],
            cwd=ROOT,
            environment=environment,
        )
        representation_hash = sha256(
            representation_stdout.encode("utf-8")
        ).hexdigest()
        if representation_hash != REPRESENTATION_INVENTORY_PROOF_SHA256:
            raise ValueError("Representation Inventory proof hash mismatch")
        representation_inventory = _representation_inventory(
            representation_proof["inventory"]
        )

        boundary_proof, boundary_stdout = _run(
            [
                sys.executable,
                "scripts/understand_source_boundary_inventory_alpha_proof.py",
            ],
            cwd=ROOT,
            environment=environment,
        )
        boundary_hash = sha256(boundary_stdout.encode("utf-8")).hexdigest()
        if boundary_hash != BOUNDARY_INVENTORY_PROOF_SHA256:
            raise ValueError("Source Boundary Inventory proof hash mismatch")
        boundary_inventory = _boundary_inventory(
            boundary_proof["boundary_inventory"]
        )

        request_proof, request_stdout = _run(
            [
                "node",
                "--no-warnings",
                "--experimental-strip-types",
                "scripts/representation-referenced-request.mjs",
            ],
            cwd=nexahedron_root,
            environment=environment,
        )
        request_hash = sha256(request_stdout.encode("utf-8")).hexdigest()
        if request_hash != REQUEST_PROOF_SHA256:
            raise ValueError("Representation-referenced request proof hash mismatch")
        request = construct_orientation_request(request_proof["request"])
        declaration = check_declared_source_element_declaration(
            request,
            stage1,
            representation_inventory,
            boundary_inventory,
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
            f"[UNDERSTAND Source Element Declaration Check Alpha] {error}",
            file=sys.stderr,
        )
        return 1

    proof = {
        "canonical_stage_completed": False,
        "declaration": asdict(declaration),
        "diagnostic_kind": "internal_declared_source_element_declaration_check",
        "input_hashes": {
            "boundary_inventory_proof_sha256": boundary_hash,
            "representation_inventory_proof_sha256": representation_hash,
            "request_proof_sha256": request_hash,
            "stage1_proof_sha256": stage1_hash,
        },
        "element_inventory_created": False,
        "filesystem_accessed": False,
        "parser_invoked": False,
        "payload_accessed": False,
        "semantic_processing": "none",
        "structural_discovery": "none",
        "stop": "before_declared_source_element_inventory",
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
