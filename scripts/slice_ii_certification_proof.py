#!/usr/bin/env python3
"""Certify the complete bounded Vertical Slice II execution chain."""

from __future__ import annotations

from dataclasses import FrozenInstanceError, asdict, replace
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
from typing import Mapping


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from orion.markdown_structural_renderer_alpha import (  # noqa: E402
    ALPHA_ELEMENT_KINDS,
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
from slice_ii_structural_statistics_proof import (  # noqa: E402
    FIXTURE,
    FIXTURE_SHA256,
    _full_source,
    _independent_recomputation,
)


CERTIFICATION_STATE = "slice_ii_complete"
STOP_AT_SLICE_II_COMPLETE = "at_slice_ii_complete"
CAPABILITY_PROOFS = (
    "markdown_structural_renderer_alpha_proof.py",
    "understand_source_element_inventory_alpha_proof.py",
    "slice_ii_structural_expansion_i_proofs.py",
    "slice_ii_structural_expansion_ii_proofs.py",
    "slice_ii_complete_vocabulary_proof.py",
    "slice_ii_structural_summary_proof.py",
    "slice_ii_structural_statistics_proof.py",
)


def _canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _artifact_record(value: bytes) -> dict[str, object]:
    return {
        "sha256": sha256(value).hexdigest(),
        "byte_length": len(value),
    }


def _proof_replays() -> tuple[dict[str, object], ...]:
    results = []
    for proof_name in CAPABILITY_PROOFS:
        outputs = []
        for _ in range(2):
            process = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / proof_name)],
                cwd=ROOT,
                check=False,
                capture_output=True,
            )
            outputs.append(process.stdout)
            if process.returncode != 0 or process.stderr:
                raise ValueError(
                    f"{proof_name} failed: returncode={process.returncode}; "
                    f"stderr={process.stderr.decode()}"
                )
        results.append(
            {
                "proof": proof_name,
                "byte_identical": outputs[0] == outputs[1],
                "sha256": sha256(outputs[0]).hexdigest(),
                "byte_length": len(outputs[0]),
            }
        )
    return tuple(results)


def _is_frozen(instance: object, field_name: str) -> bool:
    parameters = getattr(type(instance), "__dataclass_params__", None)
    if parameters is None or not parameters.frozen:
        return False
    try:
        setattr(instance, field_name, "changed")
    except (FrozenInstanceError, AttributeError, TypeError):
        return True
    return False


def _nested_keys(value: object) -> set[str]:
    if isinstance(value, Mapping):
        return set(value).union(
            *(_nested_keys(item) for item in value.values()),
        )
    if isinstance(value, (list, tuple)):
        return set().union(*(_nested_keys(item) for item in value))
    return set()


def _negative_boundary_checks(
    source: ConfirmedMarkdownSource,
    representation,
    inventory,
    summary,
    statistics,
) -> dict[str, bool]:
    unsupported_source = ConfirmedMarkdownSource.create(
        orientation_object_id="orientation-object-negative",
        orientation_object_version="1",
        source_id="markdown-source-negative",
        source_owner="human-alpha-reviewer",
        source_ref="local:unsupported.md",
        content="<div>\n",
        confirmed_by="human-alpha-reviewer",
        confirmed_revision=1,
    )
    unsupported_rejected = False
    try:
        MarkdownStructuralRendererAlpha().render(unsupported_source)
    except ValueError:
        unsupported_rejected = True

    tampered_representation = replace(
        representation,
        orientation_object_version="tampered",
    )
    representation_tamper_rejected = not (
        validate_markdown_structural_representation(
            source,
            tampered_representation,
        ).valid
    )

    broken_inventory_rejected = False
    try:
        replace(
            inventory,
            elements=(
                inventory.elements[0],
                replace(inventory.elements[1], ordinal=99),
                *inventory.elements[2:],
            ),
        )
    except ValueError:
        broken_inventory_rejected = True

    tampered_summary = replace(summary, source_id="tampered-source")
    summary_tamper_rejected = not validate_structural_summary(
        inventory,
        tampered_summary,
    ).valid

    tampered_statistics = replace(statistics, source_id="tampered-source")
    statistics_tamper_rejected = not validate_structural_statistics(
        inventory,
        tampered_statistics,
    ).valid

    return {
        "unsupported_source_rejected": unsupported_rejected,
        "representation_tamper_rejected": representation_tamper_rejected,
        "broken_inventory_rejected": broken_inventory_rejected,
        "summary_tamper_rejected": summary_tamper_rejected,
        "statistics_tamper_rejected": statistics_tamper_rejected,
    }


def build_slice_ii_certification() -> tuple[dict[str, object], bool]:
    """Rebuild, verify, replay, and certify the complete Slice II chain."""

    source = _full_source()
    fixture_integrity_verified = (
        sha256(FIXTURE.read_bytes()).hexdigest() == FIXTURE_SHA256
    )
    renderer = MarkdownStructuralRendererAlpha()
    mapping = renderer.project(source)
    mapping_replay = renderer.project(source)
    representation = renderer.render(source)
    representation_replay = renderer.render(source)
    representation_conformance = validate_markdown_structural_representation(
        source,
        representation,
        renderer=renderer,
    )
    inventory = inventory_declared_source_elements(representation)
    inventory_replay = inventory_declared_source_elements(
        representation_replay
    )
    summary = summarize_declared_structure(inventory)
    summary_replay = summarize_declared_structure(inventory_replay)
    summary_conformance = validate_structural_summary(inventory, summary)
    statistics = measure_declared_structure(inventory)
    statistics_replay = measure_declared_structure(inventory_replay)
    statistics_conformance = validate_structural_statistics(
        inventory,
        statistics,
    )

    mapping_bytes = _canonical_bytes(asdict(mapping))
    mapping_replay_bytes = _canonical_bytes(asdict(mapping_replay))
    representation_bytes = canonical_representation_bytes(representation)
    representation_replay_bytes = canonical_representation_bytes(
        representation_replay
    )
    inventory_bytes = canonical_inventory_bytes(inventory)
    inventory_replay_bytes = canonical_inventory_bytes(inventory_replay)
    summary_bytes = canonical_structural_summary_bytes(summary)
    summary_replay_bytes = canonical_structural_summary_bytes(summary_replay)
    statistics_bytes = canonical_structural_statistics_bytes(statistics)
    statistics_replay_bytes = canonical_structural_statistics_bytes(
        statistics_replay
    )

    complete_vocabulary = (
        set(element.element_kind for element in representation.elements)
        == set(ALPHA_ELEMENT_KINDS)
        and set(element.element_kind for element in inventory.elements)
        == set(ALPHA_ELEMENT_KINDS)
    )
    one_to_one_declarations = tuple(
        (
            block.element_kind,
            block.locator,
            block.ordinal,
            block.level,
        )
        for block in mapping.blocks
    ) == tuple(
        (
            element.element_kind,
            element.locator,
            element.ordinal,
            element.level,
        )
        for element in representation.elements
    )
    provenance_verified = (
        representation.source == source.provenance()
        and inventory.orientation_object_id == source.orientation_object_id
        and inventory.orientation_object_version
        == source.orientation_object_version
        and inventory.representation_id == representation.representation_id
        and inventory.representation_version
        == representation.representation_version
        and inventory.representation_integrity
        == representation.representation_sha256
        and summary.input_inventory_ref == statistics.input_inventory_ref
        and summary.representation_id == representation.representation_id
        and statistics.representation_id == representation.representation_id
        and summary.source_integrity == source.content_sha256
        and statistics.source_integrity == source.content_sha256
    )
    immutability = {
        "representation": _is_frozen(
            representation,
            "representation_id",
        )
        and isinstance(representation.elements, tuple)
        and all(
            _is_frozen(element, "element_id")
            for element in representation.elements
        ),
        "inventory": _is_frozen(inventory, "representation_id")
        and isinstance(inventory.elements, tuple)
        and all(
            _is_frozen(element, "element_id")
            for element in inventory.elements
        ),
        "summary": _is_frozen(summary, "summary_id")
        and isinstance(summary.declared_headings, tuple)
        and all(
            _is_frozen(heading, "element_id")
            for heading in summary.declared_headings
        ),
        "statistics": _is_frozen(statistics, "statistics_id")
        and isinstance(statistics.element_spans, tuple)
        and all(
            _is_frozen(span, "element_id")
            for span in statistics.element_spans
        ),
    }
    forbidden_fields = {
        "claims",
        "concepts",
        "entities",
        "evidence",
        "meaning",
        "navigation",
        "relations",
        "semantic",
        "summary_text",
        "topics",
    }
    mapping_shape = asdict(mapping)
    projection_mapping_only = (
        set(mapping_shape)
        == {
            "source_id",
            "source_revision",
            "boundary_ref",
            "blocks",
            "declared_lossiness",
        }
        and all(
            set(block)
            == {
                "element_kind",
                "boundary_ref",
                "locator",
                "ordinal",
                "level",
            }
            for block in mapping_shape["blocks"]
        )
        and forbidden_fields.isdisjoint(_nested_keys(mapping_shape))
    )
    responsibility_boundaries = {
        "projection_defines_mapping_only": projection_mapping_only,
        "renderer_executes_projection_only": (
            one_to_one_declarations
            and representation.projection == renderer.projection
        ),
        "representation_preserves_declarations_only": (
            forbidden_fields.isdisjoint(_nested_keys(asdict(representation)))
        ),
        "external_conformance_validates_representation": (
            representation_conformance.valid
        ),
        "inventory_consumes_representation_only": (
            inventory.input_boundary == "immutable_structural_representation"
        ),
        "summary_consumes_inventory_only": (
            summary.input_boundary == "declared_source_element_inventory"
        ),
        "statistics_consumes_inventory_only": (
            statistics.input_boundary == "declared_source_element_inventory"
        ),
        "no_semantic_or_downstream_fields": forbidden_fields.isdisjoint(
            _nested_keys(asdict(summary))
            | _nested_keys(asdict(statistics))
        ),
    }
    negative_checks = _negative_boundary_checks(
        source,
        representation,
        inventory,
        summary,
        statistics,
    )
    capability_proof_replays = _proof_replays()
    all_capability_proofs_replay = all(
        proof["byte_identical"] for proof in capability_proof_replays
    )
    artifacts_replay = {
        "projection": mapping_bytes == mapping_replay_bytes,
        "representation": representation_bytes == representation_replay_bytes,
        "inventory": inventory_bytes == inventory_replay_bytes,
        "summary": summary_bytes == summary_replay_bytes,
        "statistics": statistics_bytes == statistics_replay_bytes,
    }
    utf8_verified = (
        len(source.content.encode("utf-8")) > len(source.content)
        and statistics.document_byte_boundary.byte_width
        == len(source.content.encode("utf-8"))
    )
    interval_union_verified = _independent_recomputation(
        inventory,
        statistics,
    )
    definition_of_done = {
        "profile_v1_vocabulary_complete": complete_vocabulary,
        "projection_byte_identical": artifacts_replay["projection"],
        "supported_nodes_declared_once": one_to_one_declarations,
        "canonical_order_and_ordinals_replayed": (
            tuple(element.ordinal for element in representation.elements)
            == tuple(range(len(representation.elements)))
        ),
        "canonical_locators_conformant": representation_conformance.valid,
        "element_identity_and_integrity_replayed": (
            artifacts_replay["representation"]
        ),
        "representation_vocabulary_closed": complete_vocabulary,
        "setext_levels_preserved": {
            element.level
            for element in representation.elements
            if element.element_kind == "setext_heading"
        }.issubset({1, 2}),
        "external_conformance_complete": (
            representation_conformance.valid
        ),
        "inventory_boundary_preserved": (
            responsibility_boundaries[
                "inventory_consumes_representation_only"
            ]
        ),
        "inventory_lineage_preserved": provenance_verified,
        "structural_summary_complete": summary_conformance.valid,
        "structural_summary_replayed": artifacts_replay["summary"],
        "structural_statistics_complete": statistics_conformance.valid,
        "structural_statistics_replayed": artifacts_replay["statistics"],
        "nesting_depth_unavailable": (
            statistics.nesting_depth == "unavailable"
        ),
        "no_relation_inferred": (
            responsibility_boundaries["no_semantic_or_downstream_fields"]
        ),
        "capability_proofs_reproducible": all_capability_proofs_replay,
        "complete_vocabulary_proof_reproducible": next(
            proof["byte_identical"]
            for proof in capability_proof_replays
            if proof["proof"] == "slice_ii_complete_vocabulary_proof.py"
        ),
        "summary_and_statistics_proofs_reproducible": all(
            proof["byte_identical"]
            for proof in capability_proof_replays
            if proof["proof"]
            in (
                "slice_ii_structural_summary_proof.py",
                "slice_ii_structural_statistics_proof.py",
            )
        ),
        "full_slice_ii_chain_replayed": all(artifacts_replay.values()),
        "negative_boundaries_verified": all(negative_checks.values()),
        "fixture_integrity_verified": fixture_integrity_verified,
        "utf8_verified": utf8_verified,
        "interval_union_verified": interval_union_verified,
        "artifacts_immutable": all(immutability.values()),
        "provenance_verified": provenance_verified,
        "implementation_stop_preserved": (
            statistics.stop == STOP_AFTER_STRUCTURAL_STATISTICS
        ),
    }
    certified = (
        all(definition_of_done.values())
        and all(responsibility_boundaries.values())
        and representation_conformance.valid
        and summary_conformance.valid
        and statistics_conformance.valid
    )
    proof = {
        "milestone": "WP11 — Vertical Slice II Certification & Closeout",
        "renderer_version": representation.renderer_version,
        "fixture": {
            "path": str(FIXTURE.relative_to(ROOT)),
            "sha256": FIXTURE_SHA256,
            "integrity_verified": fixture_integrity_verified,
        },
        "chain": (
            "confirmed_markdown",
            "projection",
            "renderer",
            "immutable_structural_representation",
            "external_conformance",
            "understand_inventory",
            "structural_summary",
            "structural_statistics",
            CERTIFICATION_STATE,
            "stop",
        ),
        "artifacts": {
            "projection": _artifact_record(mapping_bytes),
            "representation": _artifact_record(representation_bytes),
            "inventory": _artifact_record(inventory_bytes),
            "summary": _artifact_record(summary_bytes),
            "statistics": _artifact_record(statistics_bytes),
        },
        "artifact_replay": artifacts_replay,
        "external_conformance": {
            "representation": asdict(representation_conformance),
            "summary": asdict(summary_conformance),
            "statistics": asdict(statistics_conformance),
        },
        "immutability": immutability,
        "provenance_verified": provenance_verified,
        "responsibility_boundaries": responsibility_boundaries,
        "negative_boundary_checks": negative_checks,
        "capability_proof_replays": capability_proof_replays,
        "utf8_verified": utf8_verified,
        "interval_union_verified": interval_union_verified,
        "definition_of_done": definition_of_done,
        "downstream_execution": {
            "slice_iii": False,
            "relations": False,
            "navigation": False,
            "orientation_map": False,
            "lyra": False,
            "sirius": False,
            "semantic_interpretation": False,
            "runtime": False,
            "gateway": False,
        },
        "certification_state": (
            CERTIFICATION_STATE if certified else "certification_failed"
        ),
        "certified": certified,
        "stop": STOP_AT_SLICE_II_COMPLETE,
    }
    return proof, certified


def canonical_certification_bytes(proof: dict[str, object]) -> bytes:
    """Serialize the certification deterministically."""

    return _canonical_bytes(proof)


def main() -> int:
    try:
        proof, certified = build_slice_ii_certification()
    except (OSError, UnicodeError, TypeError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    sys.stdout.buffer.write(canonical_certification_bytes(proof) + b"\n")
    return 0 if certified else 1


if __name__ == "__main__":
    raise SystemExit(main())
