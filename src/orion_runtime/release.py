"""Verification of the immutable ORION Version 1 release."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path

from .canonical import canonical_bytes
from .constants import (
    API_VERSION,
    CORE_COMMIT,
    CORE_FINGERPRINT,
    RELEASE_MANIFEST_PATH,
    RELEASE_MANIFEST_SCHEMA,
    RUNTIME_VERSION,
)


ROOT = Path(__file__).resolve().parents[2]


def fingerprint_paths() -> tuple[Path, ...]:
    fixed = (
        ROOT / "VERSION",
        ROOT / "workspace.yaml",
        ROOT / "evaluation/phase_vii/corpus.json",
        ROOT / "docs/architecture/operators/ORION_ORIENTATION_POLICIES.md",
        ROOT / "docs/architecture/operators/ORION_ORIENTATION_OPERATORS.md",
    )
    discovered = tuple(
        path
        for pattern in (
            "docs/architecture/contracts/*.md",
            "src/orion/public_contracts/**/*.py",
            "src/orion/orientation_runtime/**/*.py",
            "src/orion/gateway/**/*.py",
        )
        for path in ROOT.glob(pattern)
        if path.is_file()
    )
    return tuple(
        sorted(
            (*fixed, *discovered),
            key=lambda path: path.relative_to(ROOT).as_posix(),
        )
    )


def current_fingerprint() -> str:
    lines = []
    for path in fingerprint_paths():
        relative = path.relative_to(ROOT).as_posix()
        lines.append(f"{sha256(path.read_bytes()).hexdigest()}  {relative}")
    manifest = "\n".join(lines) + "\n"
    return sha256(manifest.encode("utf-8")).hexdigest()


def repository_commit() -> str | None:
    """Read repository evidence when present; never accept an environment assertion."""
    head = ROOT / ".git" / "HEAD"
    if not head.exists():
        return None
    value = head.read_text(encoding="utf-8").strip()
    if value.startswith("ref: "):
        ref = ROOT / ".git" / value[5:]
        if ref.exists():
            return ref.read_text(encoding="utf-8").strip()
        packed = ROOT / ".git" / "packed-refs"
        if packed.exists():
            suffix = value[5:]
            for line in packed.read_text(encoding="utf-8").splitlines():
                if line and not line.startswith("#") and line.endswith(f" {suffix}"):
                    return line.split(" ", 1)[0]
    return value


def verify_runtime_release_manifest() -> tuple[bool, tuple[str, ...]]:
    errors: list[str] = []
    path = ROOT / RELEASE_MANIFEST_PATH
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False, ("runtime_release_manifest_unreadable",)
    expected_fields = {
        "schema_version",
        "runtime_version",
        "api_version",
        "core_commit",
        "core_fingerprint",
        "supported_gateway_version",
        "files",
        "release_id",
    }
    if not isinstance(value, dict) or set(value) != expected_fields:
        return False, ("runtime_release_manifest_shape",)
    if value["schema_version"] != RELEASE_MANIFEST_SCHEMA:
        errors.append("runtime_release_manifest_schema")
    if value["runtime_version"] != RUNTIME_VERSION or value["api_version"] != API_VERSION:
        errors.append("runtime_release_manifest_version")
    if value["core_commit"] != CORE_COMMIT:
        errors.append("runtime_release_manifest_core_commit")
    if value["core_fingerprint"] != CORE_FINGERPRINT:
        errors.append("runtime_release_manifest_core_fingerprint")
    files = value["files"]
    if not isinstance(files, list) or not files:
        errors.append("runtime_release_manifest_files")
    else:
        names: list[str] = []
        for entry in files:
            if (
                not isinstance(entry, dict)
                or set(entry) != {"path", "sha256", "bytes"}
                or not isinstance(entry["path"], str)
                or entry["path"].startswith("/")
                or ".." in Path(entry["path"]).parts
                or not isinstance(entry["sha256"], str)
                or not isinstance(entry["bytes"], int)
            ):
                errors.append("runtime_release_manifest_entry")
                continue
            names.append(entry["path"])
            target = ROOT / entry["path"]
            try:
                content = target.read_bytes()
            except OSError:
                errors.append(f"runtime_release_file_missing:{entry['path']}")
                continue
            if len(content) != entry["bytes"] or sha256(content).hexdigest() != entry["sha256"]:
                errors.append(f"runtime_release_file_mismatch:{entry['path']}")
        if names != sorted(names) or len(names) != len(set(names)):
            errors.append("runtime_release_manifest_order")
    basis = dict(value)
    release_id = basis.pop("release_id")
    if release_id != f"sha256:{sha256(canonical_bytes(basis)).hexdigest()}":
        errors.append("runtime_release_identity_mismatch")
    return not errors, tuple(errors)


def verify_release() -> tuple[bool, tuple[str, ...]]:
    errors: list[str] = []
    commit = repository_commit()
    if commit is not None and commit != CORE_COMMIT:
        errors.append("core_commit_mismatch")
    if current_fingerprint() != CORE_FINGERPRINT:
        errors.append("core_fingerprint_mismatch")
    errors.extend(verify_runtime_release_manifest()[1])
    return not errors, tuple(errors)
