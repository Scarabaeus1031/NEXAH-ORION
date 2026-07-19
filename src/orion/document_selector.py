"""Deterministic document-path selection without repository access."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import PurePosixPath

from .contracts import OrientationRequest


class DocumentSelectionError(ValueError):
    """Base error for deterministic document selection."""


class UnknownDocumentScopeError(DocumentSelectionError):
    """Raised when a request contains a scope without an explicit rule."""


class EmptyDocumentSelectionError(DocumentSelectionError):
    """Raised when explicit rules produce no repository document paths."""


@dataclass(frozen=True, slots=True)
class DocumentSelectionRule:
    """One explicit mapping from a request scope to document paths."""

    rule_id: str
    scope: str
    document_paths: tuple[str, ...]

    def __post_init__(self) -> None:
        for field_name in ("rule_id", "scope"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} must be non-empty text")
        object.__setattr__(self, "rule_id", self.rule_id.strip())
        object.__setattr__(self, "scope", self.scope.strip())
        object.__setattr__(self, "document_paths", tuple(self.document_paths))


@dataclass(frozen=True, slots=True)
class SelectionResult:
    """Auditable path-only result produced before repository documents are read."""

    request_id: str
    selected_paths: tuple[str, ...]
    rule_id: str
    selection_provenance: tuple[str, ...]

    def __post_init__(self) -> None:
        selected_paths = tuple(self.selected_paths)
        provenance = tuple(self.selection_provenance)
        for field_name in ("request_id", "rule_id"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} must be non-empty text")
        if not selected_paths:
            raise EmptyDocumentSelectionError("document selection is empty")
        if tuple(sorted(set(selected_paths))) != selected_paths:
            raise ValueError("selected_paths must be unique and lexically ordered")
        if not provenance or any(
            not isinstance(item, str) or not item.strip()
            for item in provenance
        ):
            raise ValueError("selection provenance must contain non-empty text")
        object.__setattr__(self, "request_id", self.request_id.strip())
        object.__setattr__(self, "rule_id", self.rule_id.strip())
        object.__setattr__(self, "selected_paths", selected_paths)
        object.__setattr__(self, "selection_provenance", provenance)


DEFAULT_SELECTION_RULES = (
    DocumentSelectionRule(
        rule_id="scope-architecture/1",
        scope="architecture",
        document_paths=(
            "README.md",
            "docs/architecture/README.md",
            "docs/architecture/ORION_ARCHITECTURE.md",
            "docs/architecture/baselines/PHASE_0_BASELINE_RECOVERY.md",
            "docs/adr/README.md",
            "docs/adr/0001-orion-above-kernel.md",
            "docs/adr/0002-independent-repository-boundaries.md",
            "docs/adr/0003-structured-orientation-contracts.md",
            "docs/adr/0004-immutable-context-manifest.md",
            "docs/adr/0005-capability-based-reasoning-backends.md",
            "docs/adr/0006-human-approval-and-effect-classes.md",
            "docs/adr/0007-five-documentation-projections.md",
        ),
    ),
    DocumentSelectionRule(
        rule_id="scope-backend/1",
        scope="backend",
        document_paths=(
            "docs/development/PHASE_1A_EXECUTION.md",
            "docs/development/PHASE_1B_OLLAMA.md",
            "src/orion/backend.py",
            "src/orion/contracts.py",
            "src/orion/executor.py",
            "src/orion/fake_backend.py",
            "src/orion/ollama_backend.py",
            "tests/test_execution.py",
            "tests/test_ollama_backend.py",
        ),
    ),
    DocumentSelectionRule(
        rule_id="scope-validation/1",
        scope="validation",
        document_paths=(
            "docs/development/PHASE_1A_EXECUTION.md",
            "src/orion/contracts.py",
            "src/orion/validation.py",
            "tests/test_execution.py",
            "tests/test_ollama_backend.py",
        ),
    ),
)


@dataclass(frozen=True, slots=True)
class DocumentSelector:
    """Apply only explicit scope rules to request metadata."""

    rules: tuple[DocumentSelectionRule, ...] = DEFAULT_SELECTION_RULES
    rule_id: str = "explicit-scope-selection/1"

    def __post_init__(self) -> None:
        frozen_rules = tuple(self.rules)
        if not isinstance(self.rule_id, str) or not self.rule_id.strip():
            raise ValueError("rule_id must be non-empty text")
        scopes = [rule.scope for rule in frozen_rules]
        if len(set(scopes)) != len(scopes):
            raise ValueError("selection rule scopes must be unique")
        object.__setattr__(self, "rules", frozen_rules)
        object.__setattr__(self, "rule_id", self.rule_id.strip())

    def select(self, request: OrientationRequest) -> SelectionResult:
        rules_by_scope = {rule.scope: rule for rule in self.rules}
        requested_scopes = tuple(sorted(set(request.scope)))
        unknown_scopes = tuple(
            scope for scope in requested_scopes if scope not in rules_by_scope
        )
        if unknown_scopes:
            raise UnknownDocumentScopeError(
                f"no document selection rule for scope(s): {', '.join(unknown_scopes)}"
            )

        matched_rules = tuple(rules_by_scope[scope] for scope in requested_scopes)
        selected_paths = tuple(
            sorted(
                {
                    _normalize_selected_path(path)
                    for rule in matched_rules
                    for path in rule.document_paths
                }
            )
        )
        if not selected_paths:
            raise EmptyDocumentSelectionError(
                "document selection is empty for the requested scope"
            )

        provenance = (
            f"request_id:{request.request_id}",
            f"request_type:{request.request_type}",
            f"requested_by:{request.requested_by}",
            f"request_schema:{request.schema_version}",
            f"objective:{request.objective}",
            *(f"scope:{rule.scope};rule:{rule.rule_id}" for rule in matched_rules),
        )
        return SelectionResult(
            request_id=request.request_id,
            selected_paths=selected_paths,
            rule_id=self.rule_id,
            selection_provenance=provenance,
        )


def _normalize_selected_path(document_path: str) -> str:
    if not isinstance(document_path, str) or not document_path.strip():
        raise DocumentSelectionError(
            "selection rules must contain non-empty document paths"
        )
    value = document_path.strip()
    if "\\" in value:
        raise DocumentSelectionError(
            f"selection rule path must use POSIX separators: {value}"
        )
    path = PurePosixPath(value)
    if path.is_absolute() or value == "." or ".." in path.parts:
        raise DocumentSelectionError(
            f"selection rule path must be repository-relative: {value}"
        )
    return path.as_posix()
