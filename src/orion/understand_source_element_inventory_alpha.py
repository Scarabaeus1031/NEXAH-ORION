"""Declared Source Element Inventory inside UNDERSTAND Stage 2.

This internal Alpha consumes one already-existing immutable Structural
Representation. It preserves its declared element order, identities, locators
and profile properties without opening source material, executing Projection or
Rendering, or creating structure.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json

from orion.markdown_structural_renderer_alpha import (
    ALPHA_ELEMENT_KINDS,
    COMMONMARK_GRAMMAR,
    COMMONMARK_VERSION,
    MARKDOWN_STRUCTURAL_PROFILE_ID,
    MARKDOWN_STRUCTURAL_PROFILE_VERSION,
    MARKDOWN_STRUCTURAL_PROJECTION_ID,
    MARKDOWN_STRUCTURAL_PROJECTION_VERSION,
    MARKDOWN_STRUCTURAL_RENDERER_ID,
    MARKDOWN_STRUCTURAL_RENDERER_VERSION,
    MARKDOWN_STRUCTURAL_REPRESENTATION_SCHEMA,
    MARKDOWN_TARGET_DOMAIN,
    WHOLE_BOUNDARY,
    ImmutableMarkdownStructuralRepresentation,
    SourceLocator,
)


INVENTORY_DIAGNOSTIC_VERSION = "0.1-alpha"
CANONICAL_STAGE = "understand/2"
OPERATOR_ID = "orion.orientation-operator/understand"
OPERATOR_VERSION = "1.0"
RESPONSIBILITY = "declared_source_element_inventory"
INPUT_BOUNDARY = "immutable_structural_representation"
STOP_AFTER_ELEMENT_INVENTORY = "after_declared_source_element_inventory"


@dataclass(frozen=True, slots=True)
class DeclaredSourceElementInventoryEntry:
    """One exact declared element in canonical Representation order."""

    element_id: str
    element_kind: str
    boundary_ref: str
    locator: SourceLocator
    ordinal: int
    level: int | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.element_id, str) or not self.element_id:
            raise ValueError("element_id must be exact non-empty text")
        if not isinstance(self.element_kind, str) or not self.element_kind:
            raise ValueError("element_kind must be exact non-empty text")
        if self.element_kind not in ALPHA_ELEMENT_KINDS:
            raise ValueError("element kind is outside the accepted Renderer scope")
        if self.boundary_ref != WHOLE_BOUNDARY:
            raise ValueError("inventory element must preserve boundary 'whole'")
        if not isinstance(self.locator, SourceLocator):
            raise TypeError("inventory locator must be SourceLocator")
        self.locator.__post_init__()
        if type(self.ordinal) is not int or self.ordinal < 0:
            raise ValueError("inventory ordinal must be a non-negative integer")
        if self.element_kind == "atx_heading":
            if type(self.level) is not int or not 1 <= self.level <= 6:
                raise ValueError("inventory ATX heading level must be 1 through 6")
        elif self.element_kind == "setext_heading":
            if type(self.level) is not int or not 1 <= self.level <= 2:
                raise ValueError("inventory Setext heading level must be 1 or 2")
        elif self.level is not None:
            raise ValueError("only declared headings may carry level")


@dataclass(frozen=True, slots=True)
class DeclaredSourceElementInventoryDiagnostic:
    """Internal deterministic inventory; never a public Runtime outcome."""

    diagnostic_version: str
    canonical_stage: str
    operator_id: str
    operator_version: str
    responsibility: str
    input_boundary: str
    orientation_object_id: str
    orientation_object_version: str
    representation_id: str
    representation_version: str
    representation_schema: str
    representation_integrity: str
    profile_id: str
    profile_version: str
    source_id: str
    source_owner: str
    source_ref: str
    source_revision: str
    source_integrity: str
    source_boundary: str
    ordered_element_count: int
    elements: tuple[DeclaredSourceElementInventoryEntry, ...]
    responsibility_state: str
    canonical_stage_state: str
    stop: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "elements", tuple(self.elements))
        for field_name in (
            "diagnostic_version",
            "canonical_stage",
            "operator_id",
            "operator_version",
            "responsibility",
            "input_boundary",
            "orientation_object_id",
            "orientation_object_version",
            "representation_id",
            "representation_version",
            "representation_schema",
            "representation_integrity",
            "profile_id",
            "profile_version",
            "source_id",
            "source_owner",
            "source_ref",
            "source_revision",
            "source_integrity",
            "source_boundary",
            "responsibility_state",
            "canonical_stage_state",
            "stop",
        ):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value:
                raise ValueError(f"{field_name} must be exact non-empty text")
        if (
            type(self.ordered_element_count) is not int
            or self.ordered_element_count < 1
            or self.ordered_element_count != len(self.elements)
        ):
            raise ValueError("ordered element count does not match inventory")
        for element in self.elements:
            if not isinstance(element, DeclaredSourceElementInventoryEntry):
                raise TypeError("inventory elements must be exact inventory entries")
            element.__post_init__()
        if tuple(element.ordinal for element in self.elements) != tuple(
            range(len(self.elements))
        ):
            raise ValueError("inventory ordinals must remain canonical")
        if self.elements[0].element_kind != "document":
            raise ValueError("inventory must preserve the document root first")


def _require_frozen_structural_profile(
    representation: ImmutableMarkdownStructuralRepresentation,
) -> None:
    if representation.schema_version != MARKDOWN_STRUCTURAL_REPRESENTATION_SCHEMA:
        raise ValueError("unknown Structural Representation schema")
    if (
        representation.profile_id != MARKDOWN_STRUCTURAL_PROFILE_ID
        or representation.profile_version != MARKDOWN_STRUCTURAL_PROFILE_VERSION
    ):
        raise ValueError("unknown Structural Representation profile")
    if representation.target_domain != MARKDOWN_TARGET_DOMAIN:
        raise ValueError("unknown Structural Representation target domain")
    if (
        representation.projection.projection_id
        != MARKDOWN_STRUCTURAL_PROJECTION_ID
        or representation.projection.projection_version
        != MARKDOWN_STRUCTURAL_PROJECTION_VERSION
    ):
        raise ValueError("unknown Structural Projection")
    if (
        representation.projection.source_grammar != COMMONMARK_GRAMMAR
        or representation.projection.source_grammar_version != COMMONMARK_VERSION
    ):
        raise ValueError("unknown Structural Representation grammar")
    if (
        representation.renderer_id != MARKDOWN_STRUCTURAL_RENDERER_ID
        or representation.renderer_version != MARKDOWN_STRUCTURAL_RENDERER_VERSION
    ):
        raise ValueError("unknown Structural Renderer")
    if representation.boundary_ref != WHOLE_BOUNDARY:
        raise ValueError("unknown Structural Representation boundary")


def inventory_declared_source_elements(
    representation: ImmutableMarkdownStructuralRepresentation,
) -> DeclaredSourceElementInventoryDiagnostic:
    """Inventory only already-declared immutable source elements."""

    if not isinstance(representation, ImmutableMarkdownStructuralRepresentation):
        raise TypeError(
            "source element inventory requires an immutable Structural Representation"
        )
    representation.__post_init__()
    _require_frozen_structural_profile(representation)

    entries = tuple(
        DeclaredSourceElementInventoryEntry(
            element_id=element.element_id,
            element_kind=element.element_kind,
            boundary_ref=element.boundary_ref,
            locator=element.locator,
            ordinal=element.ordinal,
            level=element.level,
        )
        for element in representation.elements
    )
    diagnostic = DeclaredSourceElementInventoryDiagnostic(
        diagnostic_version=INVENTORY_DIAGNOSTIC_VERSION,
        canonical_stage=CANONICAL_STAGE,
        operator_id=OPERATOR_ID,
        operator_version=OPERATOR_VERSION,
        responsibility=RESPONSIBILITY,
        input_boundary=INPUT_BOUNDARY,
        orientation_object_id=representation.orientation_object_id,
        orientation_object_version=representation.orientation_object_version,
        representation_id=representation.representation_id,
        representation_version=representation.representation_version,
        representation_schema=representation.schema_version,
        representation_integrity=representation.representation_sha256,
        profile_id=representation.profile_id,
        profile_version=representation.profile_version,
        source_id=representation.source.entry_id,
        source_owner=representation.source.owner,
        source_ref=representation.source.source_ref,
        source_revision=representation.source.revision,
        source_integrity=representation.source.content_sha256,
        source_boundary=representation.boundary_ref,
        ordered_element_count=len(entries),
        elements=entries,
        responsibility_state="completed",
        canonical_stage_state="incomplete",
        stop=STOP_AFTER_ELEMENT_INVENTORY,
    )
    diagnostic.__post_init__()
    return diagnostic


def inventory_as_dict(
    inventory: DeclaredSourceElementInventoryDiagnostic,
) -> dict[str, object]:
    """Return the deterministic internal proof shape."""

    inventory.__post_init__()
    return asdict(inventory)


def canonical_inventory_bytes(
    inventory: DeclaredSourceElementInventoryDiagnostic,
) -> bytes:
    """Return stable bytes for repeatability verification."""

    return json.dumps(
        inventory_as_dict(inventory),
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


__all__: tuple[str, ...] = ()
