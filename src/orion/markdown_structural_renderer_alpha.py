"""Deterministic reference implementation of the Markdown structural profile.

This internal Alpha executes the complete Slice II structural block vocabulary:

    confirmed CommonMark 0.31.2 whole document
      -> deterministic block Projection
      -> document | block_quote | ordered_list | unordered_list
         | list_item | atx_heading | setext_heading | paragraph
         | thematic_break | fenced_code_block | indented_code_block declarations
      -> immutable Structural Representation
      -> external conformance validation

The Renderer rejects every later block construct. It performs no Orientation,
Evidence work, UNDERSTAND execution, Runtime or Gateway interaction. Parser
tokens remain private Projection execution details.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
import re
from typing import Any, Mapping

from .contracts import ProvenanceRef
from .representation_alpha import (
    RepresentationConformance,
    RepresentationProvenanceStep,
)


CONFIRMED_MARKDOWN_SOURCE_SCHEMA = "orion.confirmed-markdown-source/0.1-alpha"
MARKDOWN_STRUCTURAL_REPRESENTATION_SCHEMA = (
    "orion.representation/markdown-structure/1.0.0"
)
MARKDOWN_STRUCTURAL_PROFILE_ID = "orion.representation/markdown-structure"
MARKDOWN_STRUCTURAL_PROFILE_VERSION = "1.0.0"
MARKDOWN_STRUCTURAL_PROJECTION_ID = "orion.projection/markdown-structure"
MARKDOWN_STRUCTURAL_PROJECTION_VERSION = "1.0.0"
MARKDOWN_STRUCTURAL_RENDERER_ID = "orion.renderer/markdown-structure"
MARKDOWN_STRUCTURAL_RENDERER_VERSION = "0.3-alpha"
COMMONMARK_GRAMMAR = "CommonMark"
COMMONMARK_VERSION = "0.31.2"
MARKDOWN_MEDIA_TYPE = "text/markdown;charset=utf-8"
MARKDOWN_TARGET_DOMAIN = "orion.representation.markdown-block-structure"
WHOLE_BOUNDARY = "whole"
ALPHA_ELEMENT_KINDS = (
    "document",
    "block_quote",
    "ordered_list",
    "unordered_list",
    "list_item",
    "atx_heading",
    "setext_heading",
    "paragraph",
    "thematic_break",
    "fenced_code_block",
    "indented_code_block",
)

# These labels encode the omissions already frozen in profile Section 10. They
# are implementation metadata, not a second lossiness policy.
MARKDOWN_STRUCTURAL_LOSSINESS = (
    "raw_source_not_embedded",
    "parent_element_hierarchy_not_declared",
    "inline_elements_not_declared",
    "blank_lines_not_declared",
    "link_reference_definitions_not_declared",
    "source_spelling_details_not_declared",
    "list_details_not_declared",
    "code_fence_details_not_declared",
    "parser_metadata_not_declared",
    "rendering_and_editor_state_not_declared",
    "semantic_and_evidence_information_not_declared",
)

_ATX_HEADING = re.compile(r"^ {0,3}(#{1,6})(?:[ \t]+|$)")
_BLOCK_QUOTE = re.compile(r"^ {0,3}>[ \t]?")
_LIST_MARKER = re.compile(
    r"^(?P<indent> {0,3})(?:(?P<number>\d{1,9})(?P<delimiter>[.)])|"
    r"(?P<bullet>[-+*]))(?P<spacing>[ \t]+|$)"
)
_SETEXT_UNDERLINE = re.compile(r"^ {0,3}(?:=+|-+)[ \t]*$")
_FENCED_CODE = re.compile(
    r"^ {0,3}(?P<fence>`{3,}|~{3,})(?P<suffix>.*)$"
)
_LINK_REFERENCE_DEFINITION = re.compile(r"^ {0,3}\[[^]]+\]:")


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _digest(value: Any) -> str:
    return sha256(_canonical_bytes(value)).hexdigest()


def _content_digest(content: str) -> str:
    return sha256(content.encode("utf-8")).hexdigest()


def _require_text(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be non-empty text")


def _require_digest(value: str, field_name: str) -> None:
    if not isinstance(value, str) or len(value) != 64 or any(
        character not in "0123456789abcdef" for character in value
    ):
        raise ValueError(f"{field_name} must be a lowercase SHA-256 digest")


def _validate_markdown_source_content(content: str) -> bytes:
    if not isinstance(content, str):
        raise TypeError("content must be text")
    if content.startswith("\ufeff"):
        raise ValueError("UTF-8 BOM is outside the Markdown profile")
    if "\x00" in content:
        raise ValueError("U+0000 is outside the Markdown profile")
    if "\r" in content:
        raise ValueError("only LF line endings belong to the Markdown profile")
    if any(0xD800 <= ord(character) <= 0xDFFF for character in content):
        raise ValueError("isolated surrogate is outside the Markdown profile")
    try:
        return content.encode("utf-8", errors="strict")
    except UnicodeEncodeError as exc:
        raise ValueError("content must encode strictly as UTF-8") from exc


def _confirmation_identity_basis(
    *,
    orientation_object_id: str,
    orientation_object_version: str,
    source_id: str,
    source_revision: str,
    confirmed_by: str,
    confirmed_revision: int,
    boundary_ref: str,
) -> dict[str, object]:
    return {
        "orientation_object_id": orientation_object_id,
        "orientation_object_version": orientation_object_version,
        "source_id": source_id,
        "source_revision": source_revision,
        "confirmed_by": confirmed_by,
        "confirmed_revision": confirmed_revision,
        "boundary_ref": boundary_ref,
    }


@dataclass(frozen=True, slots=True)
class ConfirmedMarkdownSource:
    """Human-confirmed, pre-resolved whole Markdown source."""

    orientation_object_id: str
    orientation_object_version: str
    source_id: str
    source_owner: str
    source_ref: str
    source_revision: str
    content: str
    content_sha256: str
    confirmed_by: str
    confirmed_revision: int
    confirmation_id: str
    boundary_ref: str = WHOLE_BOUNDARY
    media_type: str = MARKDOWN_MEDIA_TYPE
    grammar: str = COMMONMARK_GRAMMAR
    grammar_version: str = COMMONMARK_VERSION
    schema_version: str = CONFIRMED_MARKDOWN_SOURCE_SCHEMA

    @classmethod
    def create(
        cls,
        *,
        orientation_object_id: str,
        orientation_object_version: str,
        source_id: str,
        source_owner: str,
        source_ref: str,
        content: str,
        confirmed_by: str,
        confirmed_revision: int,
    ) -> "ConfirmedMarkdownSource":
        content_sha256 = _content_digest(content)
        source_revision = f"sha256:{content_sha256}"
        confirmation_sha256 = _digest(
            _confirmation_identity_basis(
                orientation_object_id=orientation_object_id,
                orientation_object_version=orientation_object_version,
                source_id=source_id,
                source_revision=source_revision,
                confirmed_by=confirmed_by,
                confirmed_revision=confirmed_revision,
                boundary_ref=WHOLE_BOUNDARY,
            )
        )
        return cls(
            orientation_object_id=orientation_object_id,
            orientation_object_version=orientation_object_version,
            source_id=source_id,
            source_owner=source_owner,
            source_ref=source_ref,
            source_revision=source_revision,
            content=content,
            content_sha256=content_sha256,
            confirmed_by=confirmed_by,
            confirmed_revision=confirmed_revision,
            confirmation_id=f"confirmation-{confirmation_sha256[:16]}",
        )

    def __post_init__(self) -> None:
        for field_name in (
            "orientation_object_id",
            "orientation_object_version",
            "source_id",
            "source_owner",
            "source_ref",
            "source_revision",
            "confirmed_by",
            "confirmation_id",
            "boundary_ref",
            "media_type",
            "grammar",
            "grammar_version",
            "schema_version",
        ):
            _require_text(getattr(self, field_name), field_name)
        if type(self.confirmed_revision) is not int or self.confirmed_revision < 1:
            raise ValueError("confirmed_revision must be a positive integer")
        _validate_markdown_source_content(self.content)
        _require_digest(self.content_sha256, "content_sha256")
        if self.content_sha256 != _content_digest(self.content):
            raise ValueError("confirmed Markdown content digest mismatch")
        if self.source_revision != f"sha256:{self.content_sha256}":
            raise ValueError("source revision must identify the exact UTF-8 bytes")
        if self.boundary_ref != WHOLE_BOUNDARY:
            raise ValueError("the Markdown profile accepts only boundary 'whole'")
        if self.media_type != MARKDOWN_MEDIA_TYPE:
            raise ValueError("unsupported Markdown source media type")
        if self.grammar != COMMONMARK_GRAMMAR:
            raise ValueError("unsupported Markdown grammar")
        if self.grammar_version != COMMONMARK_VERSION:
            raise ValueError("unsupported CommonMark grammar version")
        if self.schema_version != CONFIRMED_MARKDOWN_SOURCE_SCHEMA:
            raise ValueError("unsupported confirmed Markdown source schema")
        expected_confirmation = _digest(
            _confirmation_identity_basis(
                orientation_object_id=self.orientation_object_id,
                orientation_object_version=self.orientation_object_version,
                source_id=self.source_id,
                source_revision=self.source_revision,
                confirmed_by=self.confirmed_by,
                confirmed_revision=self.confirmed_revision,
                boundary_ref=self.boundary_ref,
            )
        )
        if self.confirmation_id != f"confirmation-{expected_confirmation[:16]}":
            raise ValueError("confirmation identity does not match the source")

    def provenance(self) -> ProvenanceRef:
        return ProvenanceRef(
            entry_id=self.source_id,
            owner=self.source_owner,
            source_ref=self.source_ref,
            revision=self.source_revision,
            content_sha256=self.content_sha256,
        )


@dataclass(frozen=True, slots=True)
class MarkdownStructuralProjection:
    """Frozen mapping identity executed by the reference Renderer."""

    projection_id: str = MARKDOWN_STRUCTURAL_PROJECTION_ID
    projection_version: str = MARKDOWN_STRUCTURAL_PROJECTION_VERSION
    profile_id: str = MARKDOWN_STRUCTURAL_PROFILE_ID
    profile_version: str = MARKDOWN_STRUCTURAL_PROFILE_VERSION
    source_media_type: str = MARKDOWN_MEDIA_TYPE
    source_grammar: str = COMMONMARK_GRAMMAR
    source_grammar_version: str = COMMONMARK_VERSION
    source_boundary: str = WHOLE_BOUNDARY
    target_domain: str = MARKDOWN_TARGET_DOMAIN
    declared_lossiness: tuple[str, ...] = MARKDOWN_STRUCTURAL_LOSSINESS

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "declared_lossiness",
            tuple(self.declared_lossiness),
        )
        if self.projection_id != MARKDOWN_STRUCTURAL_PROJECTION_ID:
            raise ValueError("unsupported Markdown Structural Projection")
        if self.projection_version != MARKDOWN_STRUCTURAL_PROJECTION_VERSION:
            raise ValueError("unsupported Markdown Structural Projection version")
        if self.profile_id != MARKDOWN_STRUCTURAL_PROFILE_ID:
            raise ValueError("unsupported Markdown Structural profile")
        if self.profile_version != MARKDOWN_STRUCTURAL_PROFILE_VERSION:
            raise ValueError("unsupported Markdown Structural profile version")
        if self.source_media_type != MARKDOWN_MEDIA_TYPE:
            raise ValueError("Projection source media type mismatch")
        if self.source_grammar != COMMONMARK_GRAMMAR:
            raise ValueError("Projection source grammar mismatch")
        if self.source_grammar_version != COMMONMARK_VERSION:
            raise ValueError("Projection source grammar version mismatch")
        if self.source_boundary != WHOLE_BOUNDARY:
            raise ValueError("Projection accepts only boundary 'whole'")
        if self.target_domain != MARKDOWN_TARGET_DOMAIN:
            raise ValueError("Projection target domain mismatch")
        if self.declared_lossiness != MARKDOWN_STRUCTURAL_LOSSINESS:
            raise ValueError("Projection lossiness differs from the frozen profile")


@dataclass(frozen=True, slots=True)
class SourceLocator:
    """Canonical full-physical-line source locator."""

    start_byte: int
    end_byte: int
    start_line: int
    end_line: int

    def __post_init__(self) -> None:
        for field_name in ("start_byte", "end_byte", "start_line", "end_line"):
            if type(getattr(self, field_name)) is not int:
                raise TypeError(f"{field_name} must be an integer")
        if self.start_byte < 0 or self.end_byte < self.start_byte:
            raise ValueError("invalid byte locator")
        if self.start_line < 1 or self.end_line < self.start_line:
            raise ValueError("invalid line locator")


@dataclass(frozen=True, slots=True)
class ProjectedBlock:
    """One immutable result of executing the frozen Projection mapping."""

    element_kind: str
    boundary_ref: str
    locator: SourceLocator
    ordinal: int
    level: int | None = None

    def __post_init__(self) -> None:
        if self.element_kind not in ALPHA_ELEMENT_KINDS:
            raise ValueError("element kind is outside the Renderer Alpha")
        if self.boundary_ref != WHOLE_BOUNDARY:
            raise ValueError("projected block must reference boundary 'whole'")
        if not isinstance(self.locator, SourceLocator):
            raise TypeError("locator must be SourceLocator")
        self.locator.__post_init__()
        if type(self.ordinal) is not int or self.ordinal < 0:
            raise ValueError("ordinal must be a non-negative integer")
        if self.element_kind == "atx_heading":
            if type(self.level) is not int or not 1 <= self.level <= 6:
                raise ValueError("ATX heading level must be an integer from 1 to 6")
        elif self.element_kind == "setext_heading":
            if type(self.level) is not int or not 1 <= self.level <= 2:
                raise ValueError(
                    "Setext heading level must be an integer from 1 to 2"
                )
        elif self.level is not None:
            raise ValueError("only declared headings may carry level")

    def identity_properties(self) -> dict[str, int]:
        if self.level is None:
            return {}
        return {"level": self.level}


@dataclass(frozen=True, slots=True)
class MarkdownProjectionMapping:
    """Complete deterministic mapping handed to the Renderer."""

    source_id: str
    source_revision: str
    boundary_ref: str
    blocks: tuple[ProjectedBlock, ...]
    declared_lossiness: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "blocks", tuple(self.blocks))
        object.__setattr__(
            self,
            "declared_lossiness",
            tuple(self.declared_lossiness),
        )
        _require_text(self.source_id, "source_id")
        _require_text(self.source_revision, "source_revision")
        if self.boundary_ref != WHOLE_BOUNDARY:
            raise ValueError("mapping boundary must be 'whole'")
        if not self.blocks:
            raise ValueError("mapping requires the document root")
        for block in self.blocks:
            if not isinstance(block, ProjectedBlock):
                raise TypeError("mapping blocks must be ProjectedBlock")
            block.__post_init__()
        if tuple(block.ordinal for block in self.blocks) != tuple(
            range(len(self.blocks))
        ):
            raise ValueError("mapping ordinals must be contiguous")
        if self.blocks[0].element_kind != "document":
            raise ValueError("mapping must begin with document")
        if self.declared_lossiness != MARKDOWN_STRUCTURAL_LOSSINESS:
            raise ValueError("mapping lossiness differs from the frozen profile")


@dataclass(frozen=True, slots=True)
class DeclaredStructuralElement:
    """One immutable source-element declaration."""

    element_id: str
    element_kind: str
    boundary_ref: str
    locator: SourceLocator
    ordinal: int
    level: int | None = None

    def __post_init__(self) -> None:
        _require_text(self.element_id, "element_id")
        ProjectedBlock(
            element_kind=self.element_kind,
            boundary_ref=self.boundary_ref,
            locator=self.locator,
            ordinal=self.ordinal,
            level=self.level,
        )


@dataclass(frozen=True, slots=True)
class ImmutableMarkdownStructuralRepresentation:
    """Immutable structural declaration emitted by the Renderer Alpha."""

    representation_id: str
    representation_version: str
    representation_sha256: str
    orientation_object_id: str
    orientation_object_version: str
    source: ProvenanceRef
    boundary_ref: str
    profile_id: str
    profile_version: str
    target_domain: str
    projection: MarkdownStructuralProjection
    renderer_id: str
    renderer_version: str
    elements: tuple[DeclaredStructuralElement, ...]
    provenance: tuple[RepresentationProvenanceStep, ...]
    declared_lossiness: tuple[str, ...]
    schema_version: str = MARKDOWN_STRUCTURAL_REPRESENTATION_SCHEMA

    def __post_init__(self) -> None:
        object.__setattr__(self, "elements", tuple(self.elements))
        object.__setattr__(self, "provenance", tuple(self.provenance))
        object.__setattr__(
            self,
            "declared_lossiness",
            tuple(self.declared_lossiness),
        )
        for field_name in (
            "representation_id",
            "representation_version",
            "orientation_object_id",
            "orientation_object_version",
            "boundary_ref",
            "profile_id",
            "profile_version",
            "target_domain",
            "renderer_id",
            "renderer_version",
            "schema_version",
        ):
            _require_text(getattr(self, field_name), field_name)
        _require_digest(self.representation_sha256, "representation_sha256")
        if self.representation_version != f"sha256:{self.representation_sha256}":
            raise ValueError("Representation version must identify its integrity")
        if self.schema_version != MARKDOWN_STRUCTURAL_REPRESENTATION_SCHEMA:
            raise ValueError("unsupported Markdown Structural Representation")
        if self.boundary_ref != WHOLE_BOUNDARY:
            raise ValueError("Representation boundary must be 'whole'")
        if self.profile_id != MARKDOWN_STRUCTURAL_PROFILE_ID:
            raise ValueError("Representation profile mismatch")
        if self.profile_version != MARKDOWN_STRUCTURAL_PROFILE_VERSION:
            raise ValueError("Representation profile version mismatch")
        if self.target_domain != MARKDOWN_TARGET_DOMAIN:
            raise ValueError("Representation target domain mismatch")
        if not isinstance(self.source, ProvenanceRef):
            raise TypeError("source must be ProvenanceRef")
        self.source.__post_init__()
        if not isinstance(self.projection, MarkdownStructuralProjection):
            raise TypeError("projection must be MarkdownStructuralProjection")
        self.projection.__post_init__()
        if self.renderer_id != MARKDOWN_STRUCTURAL_RENDERER_ID:
            raise ValueError("Representation Renderer mismatch")
        _require_text(self.renderer_version, "renderer_version")
        if not self.elements:
            raise ValueError("Representation requires the document root")
        for element in self.elements:
            if not isinstance(element, DeclaredStructuralElement):
                raise TypeError("elements must be DeclaredStructuralElement")
            element.__post_init__()
        if tuple(element.ordinal for element in self.elements) != tuple(
            range(len(self.elements))
        ):
            raise ValueError("Representation ordinals must be contiguous")
        if self.elements[0].element_kind != "document":
            raise ValueError("Representation must begin with document")
        for step in self.provenance:
            if not isinstance(step, RepresentationProvenanceStep):
                raise TypeError("invalid Representation provenance step")
            step.__post_init__()
        if tuple(step.sequence for step in self.provenance) != tuple(
            range(1, len(self.provenance) + 1)
        ):
            raise ValueError("Representation provenance must be contiguous")
        if self.declared_lossiness != MARKDOWN_STRUCTURAL_LOSSINESS:
            raise ValueError("Representation lossiness differs from the profile")


@dataclass(frozen=True, slots=True)
class _PhysicalLine:
    number: int
    start_byte: int
    end_byte: int
    body: str


def _physical_lines(content: str) -> tuple[_PhysicalLine, ...]:
    if not content:
        return ()
    output: list[_PhysicalLine] = []
    byte_offset = 0
    for number, line in enumerate(content.splitlines(keepends=True), start=1):
        line_bytes = line.encode("utf-8")
        body = line[:-1] if line.endswith("\n") else line
        output.append(
            _PhysicalLine(
                number=number,
                start_byte=byte_offset,
                end_byte=byte_offset + len(line_bytes),
                body=body,
            )
        )
        byte_offset += len(line_bytes)
    return tuple(output)


def _line_locator(first: _PhysicalLine, last: _PhysicalLine) -> SourceLocator:
    return SourceLocator(
        start_byte=first.start_byte,
        end_byte=last.end_byte,
        start_line=first.number,
        end_line=last.number,
    )


@dataclass(frozen=True, slots=True)
class _ViewLine:
    source_index: int
    body: str


@dataclass(frozen=True, slots=True)
class _BlockNode:
    element_kind: str
    start_source_index: int
    end_source_index: int
    children: tuple["_BlockNode", ...] = ()
    level: int | None = None


@dataclass(frozen=True, slots=True)
class _ListMarker:
    element_kind: str
    signature: str
    indent: int
    content_indent: int
    content: str
    start_number: int | None = None


def _thematic_break(body: str) -> bool:
    if len(body) - len(body.lstrip(" ")) > 3:
        return False
    candidate = body.lstrip(" ")
    compact = candidate.replace(" ", "").replace("\t", "")
    return (
        len(compact) >= 3
        and compact[0] in "*-_"
        and set(compact) == {compact[0]}
    )


def _list_marker(body: str) -> _ListMarker | None:
    match = _LIST_MARKER.match(body)
    if match is None:
        return None
    indent = len(match.group("indent"))
    marker_end = match.start("spacing")
    spacing = match.group("spacing")
    spacing_width = len(spacing.expandtabs(4)) if spacing else 1
    if spacing_width > 4:
        spacing_width = 1
    content_indent = marker_end + spacing_width
    content = body[match.end() :]
    if len(spacing) > spacing_width:
        content = spacing[spacing_width:] + content
    if match.group("number") is not None:
        return _ListMarker(
            element_kind="ordered_list",
            signature=f"ordered:{match.group('delimiter')}",
            indent=indent,
            content_indent=content_indent,
            content=content,
            start_number=int(match.group("number")),
        )
    return _ListMarker(
        element_kind="unordered_list",
        signature=f"unordered:{match.group('bullet')}",
        indent=indent,
        content_indent=content_indent,
        content=content,
    )


def _indent_columns(body: str) -> int:
    columns = 0
    for character in body:
        if character == " ":
            columns += 1
        elif character == "\t":
            columns += 4 - (columns % 4)
        else:
            break
    return columns


def _fence_open(body: str) -> tuple[str, int] | None:
    match = _FENCED_CODE.match(body)
    if match is None:
        return None
    fence = match.group("fence")
    suffix = match.group("suffix")
    if fence[0] == "`" and "`" in suffix:
        return None
    return fence[0], len(fence)


def _fence_close(body: str, character: str, minimum_length: int) -> bool:
    stripped = body.lstrip(" ")
    if len(body) - len(stripped) > 3:
        return False
    marker_length = len(stripped) - len(stripped.lstrip(character))
    return (
        marker_length >= minimum_length
        and not stripped[marker_length:].strip(" \t")
    )


def _unsupported_block(body: str) -> str | None:
    if body.lstrip(" ").startswith("<") and len(body) - len(body.lstrip(" ")) <= 3:
        return "html_block"
    return None


def _starts_new_block(body: str) -> bool:
    return bool(
        _ATX_HEADING.match(body)
        or _BLOCK_QUOTE.match(body)
        or _list_marker(body)
        or _thematic_break(body)
        or _fence_open(body)
        or _indent_columns(body) >= 4
        or _unsupported_block(body)
    )


def _interrupts_paragraph(body: str) -> bool:
    marker = _list_marker(body)
    list_interrupts = (
        marker is not None
        and bool(marker.content.strip(" \t"))
        and (
            marker.element_kind == "unordered_list"
            or marker.start_number == 1
        )
    )
    return bool(
        _ATX_HEADING.match(body)
        or _BLOCK_QUOTE.match(body)
        or _thematic_break(body)
        or _fence_open(body)
        or _unsupported_block(body)
        or list_interrupts
    )


def _strip_item_continuation(body: str, content_indent: int) -> str:
    if not body.strip(" \t"):
        return ""
    expanded = body.expandtabs(4)
    leading = len(expanded) - len(expanded.lstrip(" "))
    if leading >= content_indent:
        return expanded[content_indent:]
    return body


def _parse_list(
    lines: tuple[_ViewLine, ...],
    start: int,
    marker: _ListMarker,
) -> tuple[_BlockNode, int]:
    list_children: list[_BlockNode] = []
    cursor = start
    list_end_source_index = lines[start].source_index

    while cursor < len(lines):
        active = _list_marker(lines[cursor].body)
        if (
            active is None
            or active.signature != marker.signature
            or active.indent != marker.indent
        ):
            break

        item_start = cursor
        item_view: list[_ViewLine] = [
            _ViewLine(lines[cursor].source_index, active.content)
        ]
        cursor += 1
        while cursor < len(lines):
            candidate = lines[cursor]
            candidate_marker = (
                None
                if _thematic_break(candidate.body)
                else _list_marker(candidate.body)
            )
            if (
                candidate_marker is not None
                and candidate_marker.indent == marker.indent
            ):
                break
            if not candidate.body.strip(" \t"):
                item_view.append(_ViewLine(candidate.source_index, ""))
                cursor += 1
                continue
            leading = len(candidate.body) - len(candidate.body.lstrip(" "))
            if leading > marker.indent:
                item_view.append(
                    _ViewLine(
                        candidate.source_index,
                        _strip_item_continuation(
                            candidate.body,
                            active.content_indent,
                        ),
                    )
                )
                cursor += 1
                continue
            if _starts_new_block(candidate.body):
                break
            item_view.append(candidate)
            cursor += 1

        item_end_source_index = (
            item_view[-1].source_index
            if item_view
            else lines[item_start].source_index
        )
        list_end_source_index = max(list_end_source_index, item_end_source_index)
        item_children = _parse_blocks(tuple(item_view))
        list_children.append(
            _BlockNode(
                element_kind="list_item",
                start_source_index=lines[item_start].source_index,
                end_source_index=item_end_source_index,
                children=item_children,
            )
        )

        next_marker = (
            (
                None
                if _thematic_break(lines[cursor].body)
                else _list_marker(lines[cursor].body)
            )
            if cursor < len(lines)
            else None
        )
        if (
            next_marker is None
            or next_marker.signature != marker.signature
            or next_marker.indent != marker.indent
        ):
            break

    return (
        _BlockNode(
            element_kind=marker.element_kind,
            start_source_index=lines[start].source_index,
            end_source_index=list_end_source_index,
            children=tuple(list_children),
        ),
        cursor,
    )


def _parse_block_quote(
    lines: tuple[_ViewLine, ...],
    start: int,
) -> tuple[_BlockNode, int]:
    cursor = start
    quote_view: list[_ViewLine] = []
    while cursor < len(lines):
        line = lines[cursor]
        marker = _BLOCK_QUOTE.match(line.body)
        if marker is not None:
            quote_view.append(
                _ViewLine(line.source_index, line.body[marker.end() :])
            )
            cursor += 1
            continue
        if (
            line.body.strip(" \t")
            and quote_view
            and quote_view[-1].body.strip(" \t")
            and not _interrupts_paragraph(line.body)
        ):
            quote_view.append(line)
            cursor += 1
            continue
        break

    return (
        _BlockNode(
            element_kind="block_quote",
            start_source_index=lines[start].source_index,
            end_source_index=quote_view[-1].source_index,
            children=_parse_blocks(tuple(quote_view)),
        ),
        cursor,
    )


def _parse_fenced_code_block(
    lines: tuple[_ViewLine, ...],
    start: int,
    fence: tuple[str, int],
) -> tuple[_BlockNode, int]:
    character, minimum_length = fence
    cursor = start + 1
    end = len(lines) - 1
    while cursor < len(lines):
        if _fence_close(lines[cursor].body, character, minimum_length):
            end = cursor
            cursor += 1
            break
        cursor += 1
    return (
        _BlockNode(
            element_kind="fenced_code_block",
            start_source_index=lines[start].source_index,
            end_source_index=lines[end].source_index,
        ),
        cursor,
    )


def _parse_indented_code_block(
    lines: tuple[_ViewLine, ...],
    start: int,
) -> tuple[_BlockNode, int]:
    cursor = start
    final_content = start
    while cursor < len(lines):
        body = lines[cursor].body
        if not body.strip(" \t"):
            cursor += 1
            continue
        if _indent_columns(body) < 4:
            break
        final_content = cursor
        cursor += 1
    return (
        _BlockNode(
            element_kind="indented_code_block",
            start_source_index=lines[start].source_index,
            end_source_index=lines[final_content].source_index,
        ),
        cursor,
    )


def _parse_blocks(lines: tuple[_ViewLine, ...]) -> tuple[_BlockNode, ...]:
    nodes: list[_BlockNode] = []
    cursor = 0
    while cursor < len(lines):
        line = lines[cursor]
        if not line.body.strip(" \t"):
            cursor += 1
            continue

        unsupported = _unsupported_block(line.body)
        if unsupported is not None:
            raise ValueError(
                f"CommonMark block is outside Renderer Alpha scope: {unsupported}"
            )

        fence = _fence_open(line.body)
        if fence is not None:
            node, cursor = _parse_fenced_code_block(lines, cursor, fence)
            nodes.append(node)
            continue

        if _indent_columns(line.body) >= 4:
            node, cursor = _parse_indented_code_block(lines, cursor)
            nodes.append(node)
            continue

        quote = _BLOCK_QUOTE.match(line.body)
        if quote is not None:
            node, cursor = _parse_block_quote(lines, cursor)
            nodes.append(node)
            continue

        heading = _ATX_HEADING.match(line.body)
        if heading is not None:
            nodes.append(
                _BlockNode(
                    element_kind="atx_heading",
                    start_source_index=line.source_index,
                    end_source_index=line.source_index,
                    level=len(heading.group(1)),
                )
            )
            cursor += 1
            continue

        if _thematic_break(line.body):
            nodes.append(
                _BlockNode(
                    element_kind="thematic_break",
                    start_source_index=line.source_index,
                    end_source_index=line.source_index,
                )
            )
            cursor += 1
            continue

        marker = _list_marker(line.body)
        if marker is not None:
            node, cursor = _parse_list(lines, cursor, marker)
            nodes.append(node)
            continue

        if _LINK_REFERENCE_DEFINITION.match(line.body):
            cursor += 1
            continue

        paragraph_start = cursor
        setext_level: int | None = None
        setext_end: int | None = None
        cursor += 1
        while cursor < len(lines):
            candidate = lines[cursor]
            underline = _SETEXT_UNDERLINE.match(candidate.body)
            if underline is not None:
                marker = candidate.body.lstrip(" ")[0]
                setext_level = 1 if marker == "=" else 2
                setext_end = cursor
                cursor += 1
                break
            if (
                not candidate.body.strip(" \t")
                or _interrupts_paragraph(candidate.body)
            ):
                break
            cursor += 1
        if setext_level is not None and setext_end is not None:
            nodes.append(
                _BlockNode(
                    element_kind="setext_heading",
                    start_source_index=lines[paragraph_start].source_index,
                    end_source_index=lines[setext_end].source_index,
                    level=setext_level,
                )
            )
        else:
            nodes.append(
                _BlockNode(
                    element_kind="paragraph",
                    start_source_index=lines[paragraph_start].source_index,
                    end_source_index=lines[cursor - 1].source_index,
                )
            )
    return tuple(nodes)


def _emit_nodes(
    nodes: tuple[_BlockNode, ...],
    physical_lines: tuple[_PhysicalLine, ...],
    projected: list[ProjectedBlock],
) -> None:
    for node in nodes:
        projected.append(
            ProjectedBlock(
                element_kind=node.element_kind,
                boundary_ref=WHOLE_BOUNDARY,
                locator=_line_locator(
                    physical_lines[node.start_source_index],
                    physical_lines[node.end_source_index],
                ),
                ordinal=len(projected),
                level=node.level,
            )
        )
        _emit_nodes(node.children, physical_lines, projected)


def _project_alpha_blocks(
    source: ConfirmedMarkdownSource,
    projection: MarkdownStructuralProjection,
) -> MarkdownProjectionMapping:
    """Execute the frozen Projection for the supported Slice II block kinds."""

    source.__post_init__()
    projection.__post_init__()
    source_bytes = _validate_markdown_source_content(source.content)
    lines = _physical_lines(source.content)
    final_line = lines[-1].number if lines else 1
    projected: list[ProjectedBlock] = [
        ProjectedBlock(
            element_kind="document",
            boundary_ref=WHOLE_BOUNDARY,
            locator=SourceLocator(
                start_byte=0,
                end_byte=len(source_bytes),
                start_line=1,
                end_line=final_line,
            ),
            ordinal=0,
        )
    ]

    view = tuple(
        _ViewLine(source_index=index, body=line.body)
        for index, line in enumerate(lines)
    )
    _emit_nodes(_parse_blocks(view), lines, projected)

    return MarkdownProjectionMapping(
        source_id=source.source_id,
        source_revision=source.source_revision,
        boundary_ref=source.boundary_ref,
        blocks=tuple(projected),
        declared_lossiness=projection.declared_lossiness,
    )


def _element_identity_basis(
    *,
    source: ConfirmedMarkdownSource,
    projection: MarkdownStructuralProjection,
    block: ProjectedBlock,
) -> dict[str, object]:
    return {
        "qualified_profile_identity": (
            f"{projection.profile_id}@{projection.profile_version}"
        ),
        "orientation_object_id": source.orientation_object_id,
        "orientation_object_version": source.orientation_object_version,
        "source_id": source.source_id,
        "source_revision": source.source_revision,
        "boundary_ref": block.boundary_ref,
        "element_kind": block.element_kind,
        "properties": block.identity_properties(),
        "locator": asdict(block.locator),
        "ordinal": block.ordinal,
    }


def _element_id(
    *,
    source: ConfirmedMarkdownSource,
    projection: MarkdownStructuralProjection,
    block: ProjectedBlock,
) -> str:
    return f"element-{_digest(_element_identity_basis(source=source, projection=projection, block=block))[:24]}"


@dataclass(frozen=True, slots=True)
class MarkdownStructuralRendererAlpha:
    """Read-only deterministic executor of the frozen Projection."""

    renderer_id: str = MARKDOWN_STRUCTURAL_RENDERER_ID
    renderer_version: str = MARKDOWN_STRUCTURAL_RENDERER_VERSION
    projection: MarkdownStructuralProjection = MarkdownStructuralProjection()

    def __post_init__(self) -> None:
        if self.renderer_id != MARKDOWN_STRUCTURAL_RENDERER_ID:
            raise ValueError("unsupported Markdown Structural Renderer")
        _require_text(self.renderer_version, "renderer_version")
        if not isinstance(self.projection, MarkdownStructuralProjection):
            raise TypeError("projection must be MarkdownStructuralProjection")
        self.projection.__post_init__()

    def project(self, source: ConfirmedMarkdownSource) -> MarkdownProjectionMapping:
        """Execute only the mapping decisions frozen by the Projection."""

        return _project_alpha_blocks(source, self.projection)

    def render(
        self,
        source: ConfirmedMarkdownSource,
    ) -> ImmutableMarkdownStructuralRepresentation:
        """Create one immutable declaration without semantic processing."""

        mapping = self.project(source)
        elements = tuple(
            DeclaredStructuralElement(
                element_id=_element_id(
                    source=source,
                    projection=self.projection,
                    block=block,
                ),
                element_kind=block.element_kind,
                boundary_ref=block.boundary_ref,
                locator=block.locator,
                ordinal=block.ordinal,
                level=block.level,
            )
            for block in mapping.blocks
        )
        representation_id = self._representation_id(source)
        provenance = (
            RepresentationProvenanceStep(
                sequence=1,
                step_id=source.confirmation_id,
                step_kind="human_confirmation",
                owner=source.confirmed_by,
                input_refs=(
                    f"{source.source_id}@{source.source_revision}",
                    (
                        f"{source.orientation_object_id}"
                        f"@{source.orientation_object_version}"
                    ),
                ),
                output_ref=f"confirmed:{source.source_id}@{source.source_revision}",
                declared_lossiness=("none",),
            ),
            RepresentationProvenanceStep(
                sequence=2,
                step_id=(
                    f"{self.projection.projection_id}"
                    f"@{self.projection.projection_version}"
                ),
                step_kind="deterministic_projection",
                owner="ORION Representation Boundary",
                input_refs=(
                    f"confirmed:{source.source_id}@{source.source_revision}",
                    (
                        f"{self.projection.profile_id}"
                        f"@{self.projection.profile_version}"
                    ),
                ),
                output_ref=f"mapping:{representation_id}",
                declared_lossiness=self.projection.declared_lossiness,
            ),
            RepresentationProvenanceStep(
                sequence=3,
                step_id=f"{self.renderer_id}@{self.renderer_version}",
                step_kind="deterministic_rendering",
                owner="ORION Representation Boundary",
                input_refs=(f"mapping:{representation_id}",),
                output_ref=representation_id,
                declared_lossiness=self.projection.declared_lossiness,
            ),
        )
        representation_basis = {
            "schema_version": MARKDOWN_STRUCTURAL_REPRESENTATION_SCHEMA,
            "representation_id": representation_id,
            "orientation_object_id": source.orientation_object_id,
            "orientation_object_version": source.orientation_object_version,
            "source": asdict(source.provenance()),
            "boundary_ref": source.boundary_ref,
            "profile_id": self.projection.profile_id,
            "profile_version": self.projection.profile_version,
            "target_domain": self.projection.target_domain,
            "projection": asdict(self.projection),
            "renderer_id": self.renderer_id,
            "renderer_version": self.renderer_version,
            "elements": [asdict(element) for element in elements],
            "provenance": [asdict(step) for step in provenance],
            "declared_lossiness": self.projection.declared_lossiness,
        }
        representation_sha256 = _digest(representation_basis)
        return ImmutableMarkdownStructuralRepresentation(
            representation_id=representation_id,
            representation_version=f"sha256:{representation_sha256}",
            representation_sha256=representation_sha256,
            orientation_object_id=source.orientation_object_id,
            orientation_object_version=source.orientation_object_version,
            source=source.provenance(),
            boundary_ref=source.boundary_ref,
            profile_id=self.projection.profile_id,
            profile_version=self.projection.profile_version,
            target_domain=self.projection.target_domain,
            projection=self.projection,
            renderer_id=self.renderer_id,
            renderer_version=self.renderer_version,
            elements=elements,
            provenance=provenance,
            declared_lossiness=self.projection.declared_lossiness,
        )

    def _representation_id(self, source: ConfirmedMarkdownSource) -> str:
        basis = {
            "orientation_object_id": source.orientation_object_id,
            "source_id": source.source_id,
            "boundary_ref": source.boundary_ref,
            "profile_id": self.projection.profile_id,
            "projection_id": self.projection.projection_id,
            "renderer_id": self.renderer_id,
            "target_domain": self.projection.target_domain,
        }
        return f"representation-{_digest(basis)[:16]}"


def validate_markdown_structural_representation(
    source: ConfirmedMarkdownSource,
    representation: ImmutableMarkdownStructuralRepresentation,
    *,
    renderer: MarkdownStructuralRendererAlpha | None = None,
) -> RepresentationConformance:
    """Externally validate deterministic replay and profile invariants."""

    active_renderer = renderer or MarkdownStructuralRendererAlpha()
    checks: list[str] = []
    errors: list[str] = []

    def check(name: str, condition: bool, error: str) -> None:
        checks.append(name)
        if not condition:
            errors.append(error)

    try:
        source.__post_init__()
        checks.append("confirmed_markdown_source_valid")
    except (TypeError, ValueError) as exc:
        checks.append("confirmed_markdown_source_valid")
        errors.append(str(exc))

    try:
        representation.__post_init__()
        checks.append("representation_shape_valid")
    except (TypeError, ValueError) as exc:
        checks.append("representation_shape_valid")
        errors.append(str(exc))

    try:
        expected = active_renderer.render(source)
    except (TypeError, ValueError) as exc:
        expected = None
        errors.append(f"deterministic replay unavailable: {exc}")

    check(
        "deterministic_replay",
        expected is not None and representation == expected,
        "Representation differs from deterministic replay",
    )
    check(
        "source_traceback",
        representation.source == source.provenance()
        and representation.boundary_ref == source.boundary_ref,
        "Representation does not trace to the confirmed Markdown source",
    )
    check(
        "orientation_object_preserved",
        (
            representation.orientation_object_id,
            representation.orientation_object_version,
        )
        == (
            source.orientation_object_id,
            source.orientation_object_version,
        ),
        "Orientation Object identity was not preserved",
    )
    check(
        "projection_and_profile_identity",
        representation.projection == active_renderer.projection
        and representation.profile_id == MARKDOWN_STRUCTURAL_PROFILE_ID
        and representation.profile_version == MARKDOWN_STRUCTURAL_PROFILE_VERSION,
        "Projection or profile identity mismatch",
    )
    check(
        "renderer_identity",
        (
            representation.renderer_id,
            representation.renderer_version,
        )
        == (
            active_renderer.renderer_id,
            active_renderer.renderer_version,
        ),
        "Renderer identity mismatch",
    )
    check(
        "canonical_ordinals",
        tuple(element.ordinal for element in representation.elements)
        == tuple(range(len(representation.elements))),
        "Structural element ordinals are not canonical",
    )
    check(
        "supported_element_vocabulary",
        all(
            element.element_kind in ALPHA_ELEMENT_KINDS
            for element in representation.elements
        ),
        "Representation contains an element outside the accepted Renderer scope",
    )
    document_locator = representation.elements[0].locator
    check(
        "canonical_locator_bounds",
        document_locator.start_byte == 0
        and document_locator.end_byte == len(source.content.encode("utf-8"))
        and all(
            element.locator.start_byte >= document_locator.start_byte
            and element.locator.end_byte <= document_locator.end_byte
            and (
                element.element_kind == "document"
                or element.locator.end_byte > element.locator.start_byte
            )
            for element in representation.elements
        ),
        "Structural element locator is outside the confirmed source boundary",
    )
    check(
        "one_to_one_projected_declarations",
        expected is not None
        and tuple(
            (
                element.element_kind,
                element.locator,
                element.ordinal,
                element.level,
            )
            for element in representation.elements
        )
        == tuple(
            (
                element.element_kind,
                element.locator,
                element.ordinal,
                element.level,
            )
            for element in expected.elements
        ),
        "Structural declarations differ from canonical Projection replay",
    )

    identity_matches = True
    if expected is not None and len(expected.elements) == len(representation.elements):
        identity_matches = all(
            actual.element_id == replayed.element_id
            for actual, replayed in zip(
                representation.elements,
                expected.elements,
                strict=True,
            )
        )
    else:
        identity_matches = False
    check(
        "deterministic_element_identities",
        identity_matches,
        "Structural element identity mismatch",
    )
    check(
        "unique_element_identities",
        len({element.element_id for element in representation.elements})
        == len(representation.elements),
        "Structural element identities are not unique",
    )
    check(
        "declared_lossiness",
        representation.declared_lossiness == MARKDOWN_STRUCTURAL_LOSSINESS,
        "Declared lossiness differs from the frozen profile",
    )
    forbidden = {
        "concepts",
        "confidence",
        "evidence",
        "report_id",
        "continuations",
        "summary",
        "understand",
    }
    check(
        "no_orientation_or_understand_semantics",
        forbidden.isdisjoint(_nested_keys(asdict(representation))),
        "Representation contains downstream semantics",
    )
    return RepresentationConformance(not errors, tuple(checks), tuple(errors))


def representation_as_dict(
    representation: ImmutableMarkdownStructuralRepresentation,
) -> dict[str, object]:
    """Return the deterministic proof shape."""

    return asdict(representation)


def canonical_representation_bytes(
    representation: ImmutableMarkdownStructuralRepresentation,
) -> bytes:
    """Return deterministic bytes for repeatability comparison."""

    return _canonical_bytes(representation_as_dict(representation))


def _nested_keys(value: object) -> set[str]:
    if isinstance(value, Mapping):
        return set(value).union(
            *(_nested_keys(item) for item in value.values()),
        )
    if isinstance(value, (list, tuple)):
        return set().union(*(_nested_keys(item) for item in value))
    return set()
