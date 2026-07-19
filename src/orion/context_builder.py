"""Deterministic, read-only repository context construction."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Iterable

from .contracts import ContextEntry, ContextManifest, OrientationRequest


class ContextDocumentError(ValueError):
    """Base error for repository document selection and loading."""


class ContextDocumentNotFoundError(ContextDocumentError):
    """Raised when an explicitly selected repository document does not exist."""


class InvalidContextDocumentPathError(ContextDocumentError):
    """Raised when a document path is not a safe repository-relative file path."""


@dataclass(frozen=True, slots=True)
class RepositoryContextProvider:
    """Load explicitly selected UTF-8 documents from one repository."""

    repository_root: Path
    source_id: str
    owner: str
    revision: str

    def __post_init__(self) -> None:
        root = Path(self.repository_root).expanduser().resolve()
        if not root.is_dir():
            raise ValueError("repository_root must be an existing directory")
        for field_name in ("source_id", "owner", "revision"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} must be non-empty text")
        object.__setattr__(self, "repository_root", root)
        object.__setattr__(self, "source_id", self.source_id.strip())
        object.__setattr__(self, "owner", self.owner.strip())
        object.__setattr__(self, "revision", self.revision.strip())

    def load(self, document_paths: Iterable[str]) -> tuple[ContextEntry, ...]:
        """Return one entry per unique path in reproducible lexical order."""

        normalized_paths = sorted(
            {_normalize_document_path(path) for path in document_paths}
        )
        if not normalized_paths:
            raise ContextDocumentError("at least one context document is required")
        return tuple(self._load_one(path) for path in normalized_paths)

    def _load_one(self, document_path: str) -> ContextEntry:
        candidate = (self.repository_root / document_path).resolve()
        try:
            candidate.relative_to(self.repository_root)
        except ValueError as error:
            raise InvalidContextDocumentPathError(
                f"context document escapes repository root: {document_path}"
            ) from error
        if not candidate.is_file():
            raise ContextDocumentNotFoundError(
                f"context document does not exist: {document_path}"
            )
        try:
            content = candidate.read_text(encoding="utf-8")
        except UnicodeDecodeError as error:
            raise ContextDocumentError(
                f"context document is not valid UTF-8: {document_path}"
            ) from error
        source_ref = f"{self.source_id}:{document_path}"
        return ContextEntry.create(
            entry_id=source_ref,
            owner=self.owner,
            source_ref=source_ref,
            revision=self.revision,
            content=content,
        )


@dataclass(frozen=True, slots=True)
class ContextBuilder:
    """Build an immutable manifest without invoking a reasoning backend."""

    provider: RepositoryContextProvider
    document_paths: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "document_paths", tuple(self.document_paths))

    def build(self, request: OrientationRequest) -> ContextManifest:
        entries = self.provider.load(self.document_paths)
        return ContextManifest.create(request, entries)


def _normalize_document_path(document_path: str) -> str:
    if not isinstance(document_path, str) or not document_path.strip():
        raise InvalidContextDocumentPathError(
            "context document path must be non-empty text"
        )
    value = document_path.strip()
    if "\\" in value:
        raise InvalidContextDocumentPathError(
            f"context document path must use POSIX separators: {value}"
        )
    path = PurePosixPath(value)
    if path.is_absolute() or value == "." or ".." in path.parts:
        raise InvalidContextDocumentPathError(
            f"context document path must be repository-relative: {value}"
        )
    return path.as_posix()
