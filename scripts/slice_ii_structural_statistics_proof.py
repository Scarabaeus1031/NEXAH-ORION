#!/usr/bin/env python3
"""Replay the bounded WP10 Structural Statistics proof."""

from __future__ import annotations

from collections import Counter
from dataclasses import asdict
from hashlib import sha256
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from orion.markdown_structural_renderer_alpha import (  # noqa: E402
    ConfirmedMarkdownSource,
    MarkdownStructuralRendererAlpha,
    canonical_representation_bytes,
    validate_markdown_structural_representation,
)
from orion.understand_source_element_inventory_alpha import (  # noqa: E402
    canonical_inventory_bytes,
    inventory_declared_source_elements,
)
from orion.understand_structural_statistics_alpha import (  # noqa: E402
    CONTAINER_KINDS,
    HEADING_LEVEL_KEYS,
    PROFILE_V1_VOCABULARY,
    STOP_AFTER_STRUCTURAL_STATISTICS,
    canonical_structural_statistics_bytes,
    measure_declared_structure,
    validate_structural_statistics,
)
from orion.understand_structural_summary_alpha import (  # noqa: E402
    canonical_structural_summary_bytes,
    summarize_declared_structure,
    validate_structural_summary,
)


FIXTURE = (
    ROOT
    / "examples"
    / "markdown_structural_renderer_alpha"
    / "structural_statistics_vocabulary.md"
)
FIXTURE_SHA256 = (
    "0c8f0c7d72abff747de6820282ff6d3ae9ee246af94d6bdedc2418562d073b7f"
)


def _full_source() -> ConfirmedMarkdownSource:
    source_bytes = FIXTURE.read_bytes()
    actual_sha256 = sha256(source_bytes).hexdigest()
    if actual_sha256 != FIXTURE_SHA256:
        raise ValueError(
            "Structural Statistics fixture integrity mismatch: "
            f"expected {FIXTURE_SHA256}, received {actual_sha256}"
        )
    return ConfirmedMarkdownSource.create(
        orientation_object_id="orientation-object-structural-statistics",
        orientation_object_version="1",
        source_id="markdown-source-structural-statistics",
        source_owner="human-alpha-reviewer",
        source_ref=(
            "local:examples/markdown_structural_renderer_alpha/"
            "structural_statistics_vocabulary.md"
        ),
        content=source_bytes.decode("utf-8", errors="strict"),
        confirmed_by="human-alpha-reviewer",
        confirmed_revision=1,
    )


def _empty_source() -> ConfirmedMarkdownSource:
    return ConfirmedMarkdownSource.create(
        orientation_object_id="orientation-object-empty-statistics",
        orientation_object_version="1",
        source_id="markdown-source-empty-statistics",
        source_owner="human-alpha-reviewer",
        source_ref="local:empty-statistics.md",
        content="",
        confirmed_by="human-alpha-reviewer",
        confirmed_revision=1,
    )


def _half_open_union(intervals: list[tuple[int, int]]) -> int:
    ordered = sorted((start, end) for start, end in intervals if end > start)
    if not ordered:
        return 0
    groups: list[list[int]] = [[ordered[0][0], ordered[0][1]]]
    for start, end in ordered[1:]:
        if start <= groups[-1][1]:
            groups[-1][1] = max(groups[-1][1], end)
        else:
            groups.append([start, end])
    return sum(end - start for start, end in groups)


def _inclusive_union(intervals: list[tuple[int, int]]) -> int:
    ordered = sorted(intervals)
    if not ordered:
        return 0
    groups: list[list[int]] = [[ordered[0][0], ordered[0][1]]]
    for start, end in ordered[1:]:
        if start <= groups[-1][1] + 1:
            groups[-1][1] = max(groups[-1][1], end)
        else:
            groups.append([start, end])
    return sum(end - start + 1 for start, end in groups)


def _independent_recomputation(inventory, statistics) -> bool:
    elements = inventory.elements
    counts = Counter(element.element_kind for element in elements)
    expected_kind_counts = tuple(
        (kind, counts[kind]) for kind in PROFILE_V1_VOCABULARY
    )
    expected_heading_counts = tuple(
        (
            kind,
            level,
            sum(
                1
                for element in elements
                if element.element_kind == kind and element.level == level
            ),
        )
        for kind, level in HEADING_LEVEL_KEYS
    )
    expected_spans = tuple(
        (
            element.element_id,
            element.ordinal,
            element.locator.end_byte - element.locator.start_byte,
            (
                0
                if element.locator.end_byte == element.locator.start_byte
                else element.locator.end_line - element.locator.start_line + 1
            ),
        )
        for element in elements
    )
    document = elements[0]
    document_width = document.locator.end_byte - document.locator.start_byte
    covered_bytes = _half_open_union(
        [
            (element.locator.start_byte, element.locator.end_byte)
            for element in elements[1:]
        ]
    )
    available_lines = (
        0
        if document_width == 0
        else document.locator.end_line - document.locator.start_line + 1
    )
    covered_lines = _inclusive_union(
        [
            (element.locator.start_line, element.locator.end_line)
            for element in elements[1:]
            if element.locator.end_byte > element.locator.start_byte
        ]
    )
    actual_kind_counts = tuple(
        (count.element_kind, count.count)
        for count in statistics.count_by_element_kind
    )
    actual_heading_counts = tuple(
        (count.element_kind, count.level, count.count)
        for count in statistics.heading_level_distribution
    )
    actual_spans = tuple(
        (
            span.element_id,
            span.ordinal,
            span.byte_span,
            span.physical_line_span,
        )
        for span in statistics.element_spans
    )
    present_kinds = set(counts)
    return all(
        (
            statistics.total_ordered_elements == len(elements),
            actual_kind_counts == expected_kind_counts,
            actual_heading_counts == expected_heading_counts,
            statistics.declared_container_kind_count
            == sum(counts[kind] for kind in CONTAINER_KINDS),
            statistics.declared_leaf_kind_count
            == len(elements)
            - sum(counts[kind] for kind in CONTAINER_KINDS),
            actual_spans == expected_spans,
            statistics.first_canonical_ordinal == elements[0].ordinal,
            statistics.final_canonical_ordinal == elements[-1].ordinal,
            statistics.document_byte_boundary.start_byte
            == document.locator.start_byte,
            statistics.document_byte_boundary.end_byte
            == document.locator.end_byte,
            statistics.document_byte_boundary.byte_width == document_width,
            statistics.non_document_byte_coverage.covered == covered_bytes,
            statistics.non_document_byte_coverage.available == document_width,
            statistics.non_document_byte_coverage.uncovered
            == document_width - covered_bytes,
            statistics.non_document_line_coverage.covered == covered_lines,
            statistics.non_document_line_coverage.available == available_lines,
            statistics.non_document_line_coverage.uncovered
            == available_lines - covered_lines,
            statistics.present_block_kind_count == len(present_kinds),
            statistics.absent_block_kind_count
            == len(PROFILE_V1_VOCABULARY) - len(present_kinds),
            statistics.nesting_depth == "unavailable",
        )
    )


def _proof_case(
    case: str,
    source: ConfirmedMarkdownSource,
) -> tuple[dict[str, object], bool]:
    renderer = MarkdownStructuralRendererAlpha()
    mapping = renderer.project(source)
    representation = renderer.render(source)
    representation_replay = renderer.render(source)
    representation_conformance = validate_markdown_structural_representation(
        source,
        representation,
        renderer=renderer,
    )
    inventory = inventory_declared_source_elements(representation)
    inventory_replay = inventory_declared_source_elements(representation)
    summary = summarize_declared_structure(inventory)
    summary_replay = summarize_declared_structure(inventory)
    summary_conformance = validate_structural_summary(inventory, summary)
    statistics = measure_declared_structure(inventory)
    statistics_replay = measure_declared_structure(inventory)
    statistics_conformance = validate_structural_statistics(
        inventory,
        statistics,
    )

    representation_replay_identical = canonical_representation_bytes(
        representation
    ) == canonical_representation_bytes(representation_replay)
    inventory_replay_identical = canonical_inventory_bytes(
        inventory
    ) == canonical_inventory_bytes(inventory_replay)
    summary_replay_identical = canonical_structural_summary_bytes(
        summary
    ) == canonical_structural_summary_bytes(summary_replay)
    statistics_replay_identical = canonical_structural_statistics_bytes(
        statistics
    ) == canonical_structural_statistics_bytes(statistics_replay)
    independent_values_verified = _independent_recomputation(
        inventory,
        statistics,
    )
    provenance_preserved = (
        statistics.orientation_object_id
        == representation.orientation_object_id
        and statistics.orientation_object_version
        == representation.orientation_object_version
        and statistics.representation_id == representation.representation_id
        and statistics.representation_version
        == representation.representation_version
        and statistics.representation_integrity
        == representation.representation_sha256
        and statistics.source_id == representation.source.entry_id
        and statistics.source_revision == representation.source.revision
        and statistics.source_integrity == representation.source.content_sha256
        and statistics.source_boundary == representation.boundary_ref
    )
    valid = (
        representation_conformance.valid
        and summary_conformance.valid
        and statistics_conformance.valid
        and representation_replay_identical
        and inventory_replay_identical
        and summary_replay_identical
        and statistics_replay_identical
        and independent_values_verified
        and provenance_preserved
        and statistics.stop == STOP_AFTER_STRUCTURAL_STATISTICS
    )
    return (
        {
            "case": case,
            "source": {
                "orientation_object_id": source.orientation_object_id,
                "orientation_object_version": source.orientation_object_version,
                "source_id": source.source_id,
                "source_revision": source.source_revision,
                "source_integrity": source.content_sha256,
                "boundary_ref": source.boundary_ref,
                "confirmation_id": source.confirmation_id,
            },
            "projection": {
                "projection_id": renderer.projection.projection_id,
                "projection_version": renderer.projection.projection_version,
                "ordered_block_kinds": tuple(
                    block.element_kind for block in mapping.blocks
                ),
            },
            "representation": {
                "representation_id": representation.representation_id,
                "representation_version": (
                    representation.representation_version
                ),
                "representation_integrity": (
                    representation.representation_sha256
                ),
                "profile_id": representation.profile_id,
                "profile_version": representation.profile_version,
                "renderer_id": representation.renderer_id,
                "renderer_version": representation.renderer_version,
            },
            "external_representation_conformance": asdict(
                representation_conformance
            ),
            "inventory": {
                "ordered_element_count": inventory.ordered_element_count,
                "representation_id": inventory.representation_id,
                "representation_integrity": (
                    inventory.representation_integrity
                ),
                "stop": inventory.stop,
            },
            "summary": {
                "summary_id": summary.summary_id,
                "input_inventory_ref": summary.input_inventory_ref,
                "stop": summary.stop,
            },
            "external_summary_conformance": asdict(summary_conformance),
            "structural_statistics": asdict(statistics),
            "external_statistics_conformance": asdict(
                statistics_conformance
            ),
            "verification": {
                "representation_byte_identical_replay": (
                    representation_replay_identical
                ),
                "inventory_byte_identical_replay": (
                    inventory_replay_identical
                ),
                "summary_byte_identical_replay": summary_replay_identical,
                "statistics_byte_identical_replay": (
                    statistics_replay_identical
                ),
                "statistics_independently_recomputed": (
                    independent_values_verified
                ),
                "provenance_preserved": provenance_preserved,
            },
            "valid": valid,
            "stop": STOP_AFTER_STRUCTURAL_STATISTICS,
        },
        valid,
    )


def build_structural_statistics_proof() -> tuple[dict[str, object], bool]:
    """Build complete-vocabulary and empty-document Statistics proofs."""

    full, full_valid = _proof_case("complete_vocabulary_utf8", _full_source())
    empty, empty_valid = _proof_case("empty_document", _empty_source())
    valid = full_valid and empty_valid
    proof = {
        "milestone": "WP10 — Structural Statistics",
        "fixture": {
            "path": str(FIXTURE.relative_to(ROOT)),
            "sha256": FIXTURE_SHA256,
            "contains_all_profile_v1_kinds": True,
            "contains_utf8_source_bytes": True,
            "contains_overlapping_declared_locators": True,
            "contains_blank_physical_lines": True,
        },
        "cases": (full, empty),
        "statistics_boundary": {
            "input": "declared_source_element_inventory",
            "raw_markdown_available": False,
            "source_document_accessed": False,
            "representation_accessed": False,
            "parser_accessed": False,
            "projection_accessed": False,
            "renderer_accessed": False,
            "semantic_interpretation_performed": False,
            "relation_inference_performed": False,
            "navigation_performed": False,
        },
        "downstream_execution": {
            "relations": False,
            "navigation": False,
            "orientation_map": False,
            "lyra": False,
            "sirius": False,
            "runtime": False,
            "gateway": False,
            "slice_ii_closure": False,
        },
        "proof_valid": valid,
        "stop": STOP_AFTER_STRUCTURAL_STATISTICS,
    }
    return proof, valid


def canonical_proof_bytes(proof: dict[str, object]) -> bytes:
    """Serialize the canonical proof deterministically."""

    return json.dumps(
        proof,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def main() -> int:
    try:
        proof, valid = build_structural_statistics_proof()
    except (OSError, UnicodeError, TypeError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    sys.stdout.buffer.write(canonical_proof_bytes(proof) + b"\n")
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
