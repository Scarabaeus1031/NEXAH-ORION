"""Deterministic Structural Statistics inside UNDERSTAND Stage 2.

Statistics consumes exactly one accepted immutable Declared Source Element
Inventory. It measures only declared fields and never accesses source content,
Representation, Projection, Renderer, semantics, relations, or navigation.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from typing import Mapping

from orion.understand_source_element_inventory_alpha import (
    ALPHA_ELEMENT_KINDS,
    CANONICAL_STAGE,
    OPERATOR_ID,
    OPERATOR_VERSION,
    DeclaredSourceElementInventoryDiagnostic,
    canonical_inventory_bytes,
)


STATISTICS_DIAGNOSTIC_VERSION = "0.1-alpha"
RESPONSIBILITY = "structural_statistics"
INPUT_BOUNDARY = "declared_source_element_inventory"
STOP_AFTER_STRUCTURAL_STATISTICS = "after_structural_statistics"
PROFILE_V1_VOCABULARY = ALPHA_ELEMENT_KINDS
CONTAINER_KINDS = (
    "document",
    "block_quote",
    "ordered_list",
    "unordered_list",
    "list_item",
)
LEAF_KINDS = tuple(
    kind for kind in PROFILE_V1_VOCABULARY if kind not in CONTAINER_KINDS
)
HEADING_LEVEL_KEYS = tuple(
    [("atx_heading", level) for level in range(1, 7)]
    + [("setext_heading", level) for level in range(1, 3)]
)


def _canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _digest(value: object) -> str:
    return sha256(_canonical_bytes(value)).hexdigest()


def _require_text(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{field_name} must be exact non-empty text")


def _require_sha256_ref(value: str, field_name: str) -> None:
    _require_text(value, field_name)
    prefix = "sha256:"
    digest = value[len(prefix) :] if value.startswith(prefix) else ""
    if len(digest) != 64 or any(
        character not in "0123456789abcdef" for character in digest
    ):
        raise ValueError(f"{field_name} must be a SHA-256 reference")


def _require_non_negative(value: int, field_name: str) -> None:
    if type(value) is not int or value < 0:
        raise ValueError(f"{field_name} must be a non-negative integer")


@dataclass(frozen=True, slots=True)
class ElementKindCount:
    """Exact count for one Profile v1 kind."""

    element_kind: str
    count: int

    def __post_init__(self) -> None:
        if self.element_kind not in PROFILE_V1_VOCABULARY:
            raise ValueError("element count kind is outside Profile v1")
        _require_non_negative(self.count, "element kind count")


@dataclass(frozen=True, slots=True)
class HeadingLevelCount:
    """Exact count for one declared heading kind and level."""

    element_kind: str
    level: int
    count: int

    def __post_init__(self) -> None:
        if (self.element_kind, self.level) not in HEADING_LEVEL_KEYS:
            raise ValueError("heading distribution key is outside Profile v1")
        _require_non_negative(self.count, "heading level count")


@dataclass(frozen=True, slots=True)
class ElementStructuralSpan:
    """Byte and physical-line width of one exact declared element."""

    element_id: str
    ordinal: int
    byte_span: int
    physical_line_span: int

    def __post_init__(self) -> None:
        _require_text(self.element_id, "element_id")
        _require_non_negative(self.ordinal, "element ordinal")
        _require_non_negative(self.byte_span, "element byte span")
        _require_non_negative(
            self.physical_line_span,
            "element physical-line span",
        )
        if self.byte_span == 0 and self.physical_line_span != 0:
            raise ValueError("zero-width element must have zero line span")
        if self.byte_span > 0 and self.physical_line_span < 1:
            raise ValueError("non-empty element must span a physical line")


@dataclass(frozen=True, slots=True)
class DocumentByteBoundary:
    """Exact root document byte boundary."""

    start_byte: int
    end_byte: int
    byte_width: int

    def __post_init__(self) -> None:
        _require_non_negative(self.start_byte, "document start byte")
        _require_non_negative(self.end_byte, "document end byte")
        _require_non_negative(self.byte_width, "document byte width")
        if self.start_byte != 0:
            raise ValueError("document byte boundary must begin at zero")
        if self.end_byte < self.start_byte:
            raise ValueError("document byte boundary is reversed")
        if self.byte_width != self.end_byte - self.start_byte:
            raise ValueError("document byte width does not match boundary")


@dataclass(frozen=True, slots=True)
class DeclaredCoverage:
    """Exact covered, available, and uncovered unit counts."""

    covered: int
    available: int
    uncovered: int

    def __post_init__(self) -> None:
        _require_non_negative(self.covered, "covered units")
        _require_non_negative(self.available, "available units")
        _require_non_negative(self.uncovered, "uncovered units")
        if self.covered > self.available:
            raise ValueError("covered units exceed available units")
        if self.covered + self.uncovered != self.available:
            raise ValueError("coverage does not reconcile with available units")


@dataclass(frozen=True, slots=True)
class StructuralStatisticsDiagnostic:
    """Immutable internal measurements of declared document structure."""

    statistics_id: str
    diagnostic_version: str
    canonical_stage: str
    operator_id: str
    operator_version: str
    responsibility: str
    input_boundary: str
    input_inventory_ref: str
    orientation_object_id: str
    orientation_object_version: str
    representation_id: str
    representation_version: str
    representation_integrity: str
    source_id: str
    source_revision: str
    source_integrity: str
    source_boundary: str
    total_ordered_elements: int
    count_by_element_kind: tuple[ElementKindCount, ...]
    heading_level_distribution: tuple[HeadingLevelCount, ...]
    declared_container_kind_count: int
    declared_leaf_kind_count: int
    element_spans: tuple[ElementStructuralSpan, ...]
    first_canonical_ordinal: int
    final_canonical_ordinal: int
    document_byte_boundary: DocumentByteBoundary
    non_document_byte_coverage: DeclaredCoverage
    non_document_line_coverage: DeclaredCoverage
    present_block_kind_count: int
    absent_block_kind_count: int
    nesting_depth: str
    responsibility_state: str
    canonical_stage_state: str
    stop: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "count_by_element_kind",
            tuple(self.count_by_element_kind),
        )
        object.__setattr__(
            self,
            "heading_level_distribution",
            tuple(self.heading_level_distribution),
        )
        object.__setattr__(self, "element_spans", tuple(self.element_spans))
        for field_name in (
            "statistics_id",
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
            "representation_integrity",
            "source_id",
            "source_revision",
            "source_integrity",
            "source_boundary",
            "nesting_depth",
            "responsibility_state",
            "canonical_stage_state",
            "stop",
        ):
            _require_text(getattr(self, field_name), field_name)
        _require_sha256_ref(self.input_inventory_ref, "input_inventory_ref")
        _require_non_negative(
            self.total_ordered_elements,
            "total ordered elements",
        )
        if self.total_ordered_elements < 1:
            raise ValueError("Statistics requires the declared document root")
        if tuple(
            count.element_kind for count in self.count_by_element_kind
        ) != PROFILE_V1_VOCABULARY:
            raise ValueError("element counts must use Profile v1 order")
        for count in self.count_by_element_kind:
            if not isinstance(count, ElementKindCount):
                raise TypeError("element counts must be immutable count entries")
            count.__post_init__()
        if (
            sum(count.count for count in self.count_by_element_kind)
            != self.total_ordered_elements
        ):
            raise ValueError("element kind counts do not equal total elements")
        if tuple(
            (count.element_kind, count.level)
            for count in self.heading_level_distribution
        ) != HEADING_LEVEL_KEYS:
            raise ValueError("heading distribution must use canonical order")
        for count in self.heading_level_distribution:
            if not isinstance(count, HeadingLevelCount):
                raise TypeError("heading distribution contains invalid entry")
            count.__post_init__()
        _require_non_negative(
            self.declared_container_kind_count,
            "declared container-kind count",
        )
        _require_non_negative(
            self.declared_leaf_kind_count,
            "declared leaf-kind count",
        )
        if (
            self.declared_container_kind_count
            + self.declared_leaf_kind_count
            != self.total_ordered_elements
        ):
            raise ValueError("container and leaf counts do not equal total")
        if len(self.element_spans) != self.total_ordered_elements:
            raise ValueError("element spans do not equal total elements")
        for span in self.element_spans:
            if not isinstance(span, ElementStructuralSpan):
                raise TypeError("element spans must be immutable span entries")
            span.__post_init__()
        if tuple(span.ordinal for span in self.element_spans) != tuple(
            range(self.total_ordered_elements)
        ):
            raise ValueError("element spans must preserve canonical ordinals")
        if self.first_canonical_ordinal != 0:
            raise ValueError("first canonical ordinal must be zero")
        if (
            self.final_canonical_ordinal
            != self.total_ordered_elements - 1
        ):
            raise ValueError("final canonical ordinal does not match total")
        if not isinstance(self.document_byte_boundary, DocumentByteBoundary):
            raise TypeError("document byte boundary has invalid type")
        self.document_byte_boundary.__post_init__()
        if not isinstance(self.non_document_byte_coverage, DeclaredCoverage):
            raise TypeError("non-document byte coverage has invalid type")
        self.non_document_byte_coverage.__post_init__()
        if (
            self.non_document_byte_coverage.available
            != self.document_byte_boundary.byte_width
        ):
            raise ValueError("byte coverage differs from document width")
        if not isinstance(self.non_document_line_coverage, DeclaredCoverage):
            raise TypeError("non-document line coverage has invalid type")
        self.non_document_line_coverage.__post_init__()
        _require_non_negative(
            self.present_block_kind_count,
            "present block-kind count",
        )
        _require_non_negative(
            self.absent_block_kind_count,
            "absent block-kind count",
        )
        if (
            self.present_block_kind_count + self.absent_block_kind_count
            != len(PROFILE_V1_VOCABULARY)
        ):
            raise ValueError("block-kind coverage does not equal Profile v1")
        if self.nesting_depth != "unavailable":
            raise ValueError("nesting depth must remain unavailable")


@dataclass(frozen=True, slots=True)
class StructuralStatisticsConformance:
    """External verification of every declared Statistics field."""

    valid: bool
    checks: tuple[str, ...]
    errors: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "checks", tuple(self.checks))
        object.__setattr__(self, "errors", tuple(self.errors))
        if type(self.valid) is not bool:
            raise TypeError("valid must be boolean")
        if any(not isinstance(check, str) or not check for check in self.checks):
            raise ValueError("conformance checks must be non-empty text")
        if any(not isinstance(error, str) or not error for error in self.errors):
            raise ValueError("conformance errors must be non-empty text")
        if self.valid != (not self.errors):
            raise ValueError("conformance validity must match its errors")


def _inventory_ref(
    inventory: DeclaredSourceElementInventoryDiagnostic,
) -> str:
    return f"sha256:{sha256(canonical_inventory_bytes(inventory)).hexdigest()}"


def _statistics_identity(input_inventory_ref: str) -> str:
    basis = {
        "diagnostic_version": STATISTICS_DIAGNOSTIC_VERSION,
        "operator_id": OPERATOR_ID,
        "operator_version": OPERATOR_VERSION,
        "responsibility": RESPONSIBILITY,
        "input_inventory_ref": input_inventory_ref,
    }
    return f"structural-statistics-{_digest(basis)[:24]}"


def _validate_inventory_boundary(
    inventory: DeclaredSourceElementInventoryDiagnostic,
) -> None:
    inventory.__post_init__()
    document = inventory.elements[0]
    if document.element_kind != "document":
        raise ValueError("Statistics requires the declared document root")
    if document.locator.start_byte != 0:
        raise ValueError("document locator must begin at byte zero")
    if document.locator.end_byte == 0 and len(inventory.elements) != 1:
        raise ValueError("empty document cannot contain declared child elements")
    for element in inventory.elements:
        locator = element.locator
        if (
            locator.start_byte < document.locator.start_byte
            or locator.end_byte > document.locator.end_byte
        ):
            raise ValueError("element locator is outside document byte boundary")
        if element.element_kind != "document" and (
            locator.end_byte <= locator.start_byte
        ):
            raise ValueError("non-document element must have positive byte width")
        if document.locator.end_byte > 0 and (
            locator.start_line < document.locator.start_line
            or locator.end_line > document.locator.end_line
        ):
            raise ValueError("element locator is outside document line boundary")


def _union_half_open(intervals: tuple[tuple[int, int], ...]) -> int:
    non_empty = sorted((start, end) for start, end in intervals if end > start)
    if not non_empty:
        return 0
    covered = 0
    current_start, current_end = non_empty[0]
    for start, end in non_empty[1:]:
        if start <= current_end:
            current_end = max(current_end, end)
        else:
            covered += current_end - current_start
            current_start, current_end = start, end
    return covered + current_end - current_start


def _union_inclusive(intervals: tuple[tuple[int, int], ...]) -> int:
    if not intervals:
        return 0
    ordered = sorted(intervals)
    covered = 0
    current_start, current_end = ordered[0]
    for start, end in ordered[1:]:
        if start <= current_end + 1:
            current_end = max(current_end, end)
        else:
            covered += current_end - current_start + 1
            current_start, current_end = start, end
    return covered + current_end - current_start + 1


def measure_declared_structure(
    inventory: DeclaredSourceElementInventoryDiagnostic,
) -> StructuralStatisticsDiagnostic:
    """Measure only exact immutable Inventory fields."""

    if not isinstance(inventory, DeclaredSourceElementInventoryDiagnostic):
        raise TypeError(
            "Structural Statistics requires an immutable Source Element Inventory"
        )
    _validate_inventory_boundary(inventory)
    input_inventory_ref = _inventory_ref(inventory)
    kind_counts = tuple(
        ElementKindCount(
            element_kind=kind,
            count=sum(
                1 for element in inventory.elements if element.element_kind == kind
            ),
        )
        for kind in PROFILE_V1_VOCABULARY
    )
    heading_counts = tuple(
        HeadingLevelCount(
            element_kind=kind,
            level=level,
            count=sum(
                1
                for element in inventory.elements
                if element.element_kind == kind and element.level == level
            ),
        )
        for kind, level in HEADING_LEVEL_KEYS
    )
    element_spans = tuple(
        ElementStructuralSpan(
            element_id=element.element_id,
            ordinal=element.ordinal,
            byte_span=element.locator.end_byte - element.locator.start_byte,
            physical_line_span=(
                0
                if element.locator.end_byte == element.locator.start_byte
                else element.locator.end_line - element.locator.start_line + 1
            ),
        )
        for element in inventory.elements
    )
    document = inventory.elements[0]
    document_byte_width = (
        document.locator.end_byte - document.locator.start_byte
    )
    byte_intervals = tuple(
        (element.locator.start_byte, element.locator.end_byte)
        for element in inventory.elements[1:]
    )
    covered_bytes = _union_half_open(byte_intervals)
    available_lines = (
        0
        if document_byte_width == 0
        else document.locator.end_line - document.locator.start_line + 1
    )
    line_intervals = tuple(
        (element.locator.start_line, element.locator.end_line)
        for element in inventory.elements[1:]
        if element.locator.end_byte > element.locator.start_byte
    )
    covered_lines = _union_inclusive(line_intervals)
    present_kinds = {
        element.element_kind for element in inventory.elements
    }
    statistics = StructuralStatisticsDiagnostic(
        statistics_id=_statistics_identity(input_inventory_ref),
        diagnostic_version=STATISTICS_DIAGNOSTIC_VERSION,
        canonical_stage=CANONICAL_STAGE,
        operator_id=OPERATOR_ID,
        operator_version=OPERATOR_VERSION,
        responsibility=RESPONSIBILITY,
        input_boundary=INPUT_BOUNDARY,
        input_inventory_ref=input_inventory_ref,
        orientation_object_id=inventory.orientation_object_id,
        orientation_object_version=inventory.orientation_object_version,
        representation_id=inventory.representation_id,
        representation_version=inventory.representation_version,
        representation_integrity=inventory.representation_integrity,
        source_id=inventory.source_id,
        source_revision=inventory.source_revision,
        source_integrity=inventory.source_integrity,
        source_boundary=inventory.source_boundary,
        total_ordered_elements=inventory.ordered_element_count,
        count_by_element_kind=kind_counts,
        heading_level_distribution=heading_counts,
        declared_container_kind_count=sum(
            count.count
            for count in kind_counts
            if count.element_kind in CONTAINER_KINDS
        ),
        declared_leaf_kind_count=sum(
            count.count
            for count in kind_counts
            if count.element_kind in LEAF_KINDS
        ),
        element_spans=element_spans,
        first_canonical_ordinal=inventory.elements[0].ordinal,
        final_canonical_ordinal=inventory.elements[-1].ordinal,
        document_byte_boundary=DocumentByteBoundary(
            start_byte=document.locator.start_byte,
            end_byte=document.locator.end_byte,
            byte_width=document_byte_width,
        ),
        non_document_byte_coverage=DeclaredCoverage(
            covered=covered_bytes,
            available=document_byte_width,
            uncovered=document_byte_width - covered_bytes,
        ),
        non_document_line_coverage=DeclaredCoverage(
            covered=covered_lines,
            available=available_lines,
            uncovered=available_lines - covered_lines,
        ),
        present_block_kind_count=len(present_kinds),
        absent_block_kind_count=len(PROFILE_V1_VOCABULARY) - len(present_kinds),
        nesting_depth="unavailable",
        responsibility_state="completed",
        canonical_stage_state="incomplete",
        stop=STOP_AFTER_STRUCTURAL_STATISTICS,
    )
    statistics.__post_init__()
    return statistics


def validate_structural_statistics(
    inventory: DeclaredSourceElementInventoryDiagnostic,
    statistics: StructuralStatisticsDiagnostic,
) -> StructuralStatisticsConformance:
    """Independently verify Statistics against one exact input Inventory."""

    checks: list[str] = []
    errors: list[str] = []

    def check(name: str, condition: bool, error: str) -> None:
        checks.append(name)
        if not condition:
            errors.append(error)

    try:
        _validate_inventory_boundary(inventory)
        checks.append("input_inventory_valid")
    except (AttributeError, TypeError, ValueError) as exc:
        checks.append("input_inventory_valid")
        errors.append(str(exc))

    try:
        statistics.__post_init__()
        checks.append("statistics_shape_valid")
    except (AttributeError, TypeError, ValueError) as exc:
        checks.append("statistics_shape_valid")
        errors.append(str(exc))

    try:
        expected = measure_declared_structure(inventory)
    except (AttributeError, TypeError, ValueError) as exc:
        expected = None
        errors.append(f"deterministic measurement unavailable: {exc}")

    check(
        "deterministic_measurement",
        expected is not None and statistics == expected,
        "Statistics differs from deterministic Inventory measurement",
    )
    check(
        "diagnostic_identity_and_version",
        statistics.statistics_id
        == _statistics_identity(statistics.input_inventory_ref)
        and statistics.diagnostic_version == STATISTICS_DIAGNOSTIC_VERSION,
        "Statistics diagnostic identity or version is not deterministic",
    )
    check(
        "responsibility_and_stop",
        statistics.canonical_stage == CANONICAL_STAGE
        and statistics.operator_id == OPERATOR_ID
        and statistics.operator_version == OPERATOR_VERSION
        and statistics.responsibility == RESPONSIBILITY
        and statistics.input_boundary == INPUT_BOUNDARY
        and statistics.responsibility_state == "completed"
        and statistics.canonical_stage_state == "incomplete"
        and statistics.stop == STOP_AFTER_STRUCTURAL_STATISTICS,
        "Statistics responsibility or STOP boundary changed",
    )
    check(
        "inventory_reference",
        statistics.input_inventory_ref == _inventory_ref(inventory),
        "Statistics does not identify the exact input Inventory",
    )
    check(
        "orientation_object_lineage",
        (
            statistics.orientation_object_id,
            statistics.orientation_object_version,
        )
        == (
            inventory.orientation_object_id,
            inventory.orientation_object_version,
        ),
        "Orientation Object lineage was not preserved",
    )
    check(
        "representation_lineage",
        (
            statistics.representation_id,
            statistics.representation_version,
            statistics.representation_integrity,
        )
        == (
            inventory.representation_id,
            inventory.representation_version,
            inventory.representation_integrity,
        ),
        "Representation lineage was not preserved",
    )
    check(
        "source_lineage",
        (
            statistics.source_id,
            statistics.source_revision,
            statistics.source_integrity,
            statistics.source_boundary,
        )
        == (
            inventory.source_id,
            inventory.source_revision,
            inventory.source_integrity,
            inventory.source_boundary,
        ),
        "source lineage was not preserved",
    )
    check(
        "element_measurements",
        expected is not None
        and statistics.total_ordered_elements
        == expected.total_ordered_elements
        and statistics.count_by_element_kind
        == expected.count_by_element_kind
        and statistics.heading_level_distribution
        == expected.heading_level_distribution
        and statistics.declared_container_kind_count
        == expected.declared_container_kind_count
        and statistics.declared_leaf_kind_count
        == expected.declared_leaf_kind_count
        and statistics.element_spans == expected.element_spans
        and statistics.first_canonical_ordinal
        == expected.first_canonical_ordinal
        and statistics.final_canonical_ordinal
        == expected.final_canonical_ordinal,
        "element measurements differ from Inventory",
    )
    check(
        "coverage_measurements",
        expected is not None
        and statistics.document_byte_boundary
        == expected.document_byte_boundary
        and statistics.non_document_byte_coverage
        == expected.non_document_byte_coverage
        and statistics.non_document_line_coverage
        == expected.non_document_line_coverage
        and statistics.present_block_kind_count
        == expected.present_block_kind_count
        and statistics.absent_block_kind_count
        == expected.absent_block_kind_count,
        "coverage measurements differ from Inventory",
    )
    check(
        "nesting_depth_unavailable",
        statistics.nesting_depth == "unavailable",
        "Statistics inferred unavailable nesting depth",
    )
    forbidden = {
        "claim",
        "claims",
        "concept",
        "concepts",
        "confidence",
        "content",
        "entities",
        "entity",
        "evidence",
        "intent",
        "meaning",
        "navigation",
        "relations",
        "semantic",
        "summary_text",
        "topic",
        "topics",
    }
    check(
        "no_semantic_relation_or_navigation_fields",
        forbidden.isdisjoint(_nested_keys(asdict(statistics))),
        "Statistics contains semantic or downstream fields",
    )
    return StructuralStatisticsConformance(
        not errors,
        tuple(checks),
        tuple(errors),
    )


def structural_statistics_as_dict(
    statistics: StructuralStatisticsDiagnostic,
) -> dict[str, object]:
    """Return the deterministic internal Statistics proof shape."""

    statistics.__post_init__()
    return asdict(statistics)


def canonical_structural_statistics_bytes(
    statistics: StructuralStatisticsDiagnostic,
) -> bytes:
    """Return stable bytes for deterministic replay verification."""

    return _canonical_bytes(structural_statistics_as_dict(statistics))


def _nested_keys(value: object) -> set[str]:
    if isinstance(value, Mapping):
        return set(value).union(
            *(_nested_keys(item) for item in value.values()),
        )
    if isinstance(value, (list, tuple)):
        return set().union(*(_nested_keys(item) for item in value))
    return set()


__all__: tuple[str, ...] = ()
