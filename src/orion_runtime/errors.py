"""Stable Runtime boundary errors."""

from __future__ import annotations


class RuntimeBoundaryError(Exception):
    def __init__(
        self,
        *,
        status: int,
        category: str,
        code: str,
        retry: str = "never",
        detail_refs: tuple[str, ...] = (),
        retry_after: int | None = None,
    ) -> None:
        super().__init__(code)
        self.status = status
        self.category = category
        self.code = code
        self.retry = retry
        self.detail_refs = detail_refs
        self.retry_after = retry_after
