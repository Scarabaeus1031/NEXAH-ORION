#!/usr/bin/env python3
"""Generate the immutable Runtime release-state manifest."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from orion_runtime.canonical import canonical_bytes  # noqa: E402
from orion_runtime.constants import (  # noqa: E402
    API_VERSION,
    CORE_COMMIT,
    CORE_FINGERPRINT,
    RELEASE_MANIFEST_PATH,
    RELEASE_MANIFEST_SCHEMA,
    RUNTIME_VERSION,
)


def normative_paths() -> tuple[Path, ...]:
    fixed = (
        ROOT / "VERSION",
        ROOT / "workspace.yaml",
        ROOT / "pyproject.toml",
        ROOT / ".dockerignore",
        ROOT / "evaluation/phase_vii/corpus.json",
        ROOT / "Dockerfile",
        ROOT / "deploy/orion-runtime.service",
        ROOT / "deploy/nginx-orion-runtime.conf",
        ROOT / "deploy/runtime.env.example",
    )
    discovered = tuple(
        path
        for pattern in (
            "docs/architecture/contracts/*.md",
            "docs/architecture/operators/*.md",
            "docs/architecture/runtime/*.md",
            "src/orion/**/*.py",
            "src/orion_runtime/**/*.py",
        )
        for path in ROOT.glob(pattern)
        if path.is_file() and "__pycache__" not in path.parts
    )
    return tuple(
        sorted(
            set((*fixed, *discovered)),
            key=lambda path: path.relative_to(ROOT).as_posix(),
        )
    )


def main() -> int:
    files = []
    for path in normative_paths():
        content = path.read_bytes()
        files.append(
            {
                "path": path.relative_to(ROOT).as_posix(),
                "sha256": sha256(content).hexdigest(),
                "bytes": len(content),
            }
        )
    basis = {
        "schema_version": RELEASE_MANIFEST_SCHEMA,
        "runtime_version": RUNTIME_VERSION,
        "api_version": API_VERSION,
        "core_commit": CORE_COMMIT,
        "core_fingerprint": CORE_FINGERPRINT,
        "supported_gateway_version": "nexahedron-gateway/1.0",
        "files": files,
    }
    value = dict(basis)
    value["release_id"] = f"sha256:{sha256(canonical_bytes(basis)).hexdigest()}"
    destination = ROOT / RELEASE_MANIFEST_PATH
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(destination)
    print(value["release_id"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
