#!/usr/bin/env python3
"""POA-003: bounded verifier for two completed Representations."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Any
import xml.etree.ElementTree as ET


EXPECTED_RESULT_KEYS = {
    "id",
    "status",
    "expression_ref",
    "expression_sha256",
    "processor",
    "processor_sha256",
    "evidence",
    "uncertainty",
    "prohibited_implications",
    "comparison",
}
EXPECTED_SVG_SHA256 = (
    "857d4aa28e531445a6e884eff1ab913d3821de88a975135c3d26fbad530effeb"
)
EXPECTED_MARKDOWN_SHA256 = (
    "b2739204f3d764b9754d305c37ee91cf2583163883b156b586914f6e2da0187e"
)
SVG_REQUIRED_PATHS = {
    "/id",
    "/comparison/sources/0",
    "/evidence/0",
    "/comparison/sources/1",
    "/evidence/1",
    "/comparison/signed_difference",
    "/uncertainty",
    "/prohibited_implications",
    "/processor",
}
AUTHORITY_CLAIMS = (
    "recommendation: approved",
    "approval: granted",
    "domain validity: confirmed",
    "semantic authority: true",
)
META_PATTERN = re.compile(r"^<!-- poa-003:([^=]+)=([^\n]+) -->$", re.MULTILINE)
ROW_PATTERN = re.compile(r"^\| `(/[^`]+)` \| `([^`]*)` \|$", re.MULTILINE)


class VerificationError(ValueError):
    """A completed Representation violated the frozen POA-003 boundary."""

    def __init__(self, reason: str):
        super().__init__(reason)
        self.reason = reason


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def load_result(path: Path) -> tuple[bytes, dict[str, Any]]:
    raw = path.read_bytes()
    try:
        result = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise VerificationError("invalid_result_json") from exc
    if (
        not isinstance(result, dict)
        or set(result) != EXPECTED_RESULT_KEYS
        or result.get("status") != "complete"
    ):
        raise VerificationError("invalid_frozen_result_shape")
    return raw, result


def expected_markdown_paths(result: dict[str, Any]) -> dict[str, Any]:
    comparison = result["comparison"]
    return {
        "/id": result["id"],
        "/status": result["status"],
        "/expression_ref": result["expression_ref"],
        "/expression_sha256": result["expression_sha256"],
        "/processor": result["processor"],
        "/processor_sha256": result["processor_sha256"],
        "/comparison/field": comparison["field"],
        "/comparison/sources/0/record_ref": comparison["sources"][0]["record_ref"],
        "/comparison/sources/0/value": comparison["sources"][0]["value"],
        "/comparison/sources/1/record_ref": comparison["sources"][1]["record_ref"],
        "/comparison/sources/1/value": comparison["sources"][1]["value"],
        "/comparison/signed_difference": comparison["signed_difference"],
        "/evidence/0/record_ref": result["evidence"][0]["record_ref"],
        "/evidence/0/value": result["evidence"][0]["value"],
        "/evidence/1/record_ref": result["evidence"][1]["record_ref"],
        "/evidence/1/value": result["evidence"][1]["value"],
        "/uncertainty/records/0/record_ref": (
            result["uncertainty"]["records"][0]["record_ref"]
        ),
        "/uncertainty/records/0/value": (
            result["uncertainty"]["records"][0]["value"]
        ),
        "/uncertainty/records/1/record_ref": (
            result["uncertainty"]["records"][1]["record_ref"]
        ),
        "/uncertainty/records/1/value": (
            result["uncertainty"]["records"][1]["value"]
        ),
        "/uncertainty/limitation": result["uncertainty"]["limitation"],
        "/prohibited_implications/0": result["prohibited_implications"][0],
        "/prohibited_implications/1": result["prohibited_implications"][1],
        "/prohibited_implications/2": result["prohibited_implications"][2],
    }


def element_text(element: ET.Element) -> str:
    return " ".join(" ".join(element.itertext()).split())


def verify_svg(raw: bytes, result: dict[str, Any], result_digest: str) -> dict[str, Any]:
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as exc:
        raise VerificationError("representation_a_invalid_svg") from exc

    lineage = next(
        (
            item
            for item in root.iter()
            if item.attrib.get("id") == "poa-001-lineage"
        ),
        None,
    )
    if lineage is None:
        raise VerificationError("representation_a_missing_lineage")
    if (
        lineage.attrib.get("data-result-id") != result["id"]
        or lineage.attrib.get("data-result-sha256") != result_digest
    ):
        raise VerificationError("representation_a_stale_result_digest")

    by_path = {
        item.attrib["data-result-path"]: item
        for item in root.iter()
        if "data-result-path" in item.attrib
    }
    if set(by_path) != SVG_REQUIRED_PATHS:
        raise VerificationError("representation_a_missing_required_trace_path")

    comparison = result["comparison"]
    checks = {
        "/id": [result["id"]],
        "/comparison/sources/0": [
            comparison["sources"][0]["record_ref"],
            str(comparison["sources"][0]["value"]),
            comparison["field"],
        ],
        "/evidence/0": [result["evidence"][0]["value"]],
        "/comparison/sources/1": [
            comparison["sources"][1]["record_ref"],
            str(comparison["sources"][1]["value"]),
            comparison["field"],
        ],
        "/evidence/1": [result["evidence"][1]["value"]],
        "/comparison/signed_difference": [
            str(comparison["signed_difference"]),
        ],
        "/uncertainty": [
            result["uncertainty"]["records"][0]["record_ref"],
            result["uncertainty"]["records"][0]["value"],
            result["uncertainty"]["records"][1]["record_ref"],
            result["uncertainty"]["records"][1]["value"],
            result["uncertainty"]["limitation"],
        ],
        "/prohibited_implications": result["prohibited_implications"],
        "/processor": [result["processor"], result_digest],
    }
    for path, values in checks.items():
        visible = element_text(by_path[path])
        if any(str(value) not in visible for value in values):
            if path.startswith("/evidence"):
                reason = "representation_a_changed_or_missing_evidence"
            elif path == "/uncertainty":
                reason = "representation_a_changed_or_missing_uncertainty"
            elif path == "/prohibited_implications":
                reason = "representation_a_missing_prohibited_implication"
            else:
                reason = "representation_a_changed_or_invented_value"
            raise VerificationError(reason)

    visible_all = element_text(root).lower()
    if any(claim in visible_all for claim in AUTHORITY_CLAIMS):
        raise VerificationError("representation_a_claims_authority")
    if digest(raw) != EXPECTED_SVG_SHA256:
        raise VerificationError("representation_a_unexpected_content")

    return {
        "id": "poa-001-static-svg",
        "media": "image/svg+xml",
        "sha256": digest(raw),
        "result_binding": "pass",
        "required_semantics": "pass",
        "non_authoritative": "pass",
        "visible_result_paths": sorted(SVG_REQUIRED_PATHS),
        "result_paths_reachable_by_digest": [
            "/expression_ref",
            "/expression_sha256",
            "/processor_sha256",
            "/status",
        ],
        "mapping_loss": [
            "JSON types and full nesting are not directly visible",
            "four lineage fields require following the bound Result digest",
            "spatial placement and an arrow are presentational additions",
        ],
    }


def verify_markdown(
    raw: bytes, result: dict[str, Any], result_digest: str
) -> dict[str, Any]:
    try:
        content = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise VerificationError("representation_b_invalid_utf8") from exc

    metadata_pairs = META_PATTERN.findall(content)
    metadata = dict(metadata_pairs)
    if len(metadata_pairs) != 4 or len(metadata) != 4:
        raise VerificationError("representation_b_invalid_metadata")
    if metadata.get("representation-id") != "poa-003-markdown-table":
        raise VerificationError("representation_b_identity_mismatch")
    if (
        metadata.get("result-id") != result["id"]
        or metadata.get("result-sha256") != result_digest
    ):
        raise VerificationError("representation_b_stale_result_digest")
    if metadata.get("authority") != "non-authoritative":
        raise VerificationError("representation_b_claims_authority")

    parsed_rows: dict[str, Any] = {}
    for path, encoded in ROW_PATTERN.findall(content):
        if path in parsed_rows:
            raise VerificationError("representation_b_duplicate_trace_path")
        try:
            parsed_rows[path] = json.loads(encoded)
        except json.JSONDecodeError as exc:
            raise VerificationError("representation_b_invalid_json_literal") from exc

    expected = expected_markdown_paths(result)
    if set(parsed_rows) != set(expected):
        missing = set(expected) - set(parsed_rows)
        if any(path.startswith("/evidence") for path in missing):
            reason = "representation_b_changed_or_missing_evidence"
        elif any(path.startswith("/uncertainty") for path in missing):
            reason = "representation_b_changed_or_missing_uncertainty"
        elif any(path.startswith("/prohibited_implications") for path in missing):
            reason = "representation_b_missing_prohibited_implication"
        else:
            reason = "representation_b_missing_required_trace_path"
        raise VerificationError(reason)

    for path, expected_value in expected.items():
        if parsed_rows[path] != expected_value:
            if path.startswith("/evidence"):
                reason = "representation_b_changed_or_missing_evidence"
            elif path.startswith("/uncertainty"):
                reason = "representation_b_changed_or_missing_uncertainty"
            elif path.startswith("/prohibited_implications"):
                reason = "representation_b_missing_prohibited_implication"
            else:
                reason = "representation_b_changed_or_invented_value"
            raise VerificationError(reason)

    lowered = content.lower()
    if any(claim in lowered for claim in AUTHORITY_CLAIMS):
        raise VerificationError("representation_b_claims_authority")
    if "## declared mapping loss" not in lowered:
        raise VerificationError("representation_b_missing_loss_disclosure")
    if digest(raw) != EXPECTED_MARKDOWN_SHA256:
        raise VerificationError("representation_b_unexpected_content")

    return {
        "id": "poa-003-markdown-table",
        "media": "text/markdown",
        "sha256": digest(raw),
        "result_binding": "pass",
        "required_semantics": "pass",
        "non_authoritative": "pass",
        "visible_result_paths": sorted(expected),
        "result_paths_reachable_by_digest": [],
        "mapping_loss": [
            "JSON nesting is flattened into explicit Result paths",
            "the SVG spatial relation and arrow are not reproduced",
        ],
    }


def complete_review(
    result_raw: bytes,
    result: dict[str, Any],
    svg_raw: bytes,
    markdown_raw: bytes,
) -> dict[str, Any]:
    result_digest = digest(result_raw)
    representation_a = verify_svg(svg_raw, result, result_digest)
    representation_b = verify_markdown(markdown_raw, result, result_digest)
    if representation_a["sha256"] == representation_b["sha256"]:
        raise VerificationError("representations_unexpectedly_byte_identical")
    if representation_a["media"] == representation_b["media"]:
        raise VerificationError("representations_not_media_distinct")

    return {
        "id": "poa-003-representation-review",
        "status": "complete",
        "claim": "representation-independence-for-one-frozen-result",
        "result": {
            "id": result["id"],
            "sha256": result_digest,
            "unchanged": True,
        },
        "representation_a": representation_a,
        "representation_b": representation_b,
        "preserved": {
            "comparison": "pass",
            "evidence": "pass",
            "uncertainty": "pass",
            "limitation": "pass",
            "prohibited_implications": "pass",
            "processor_lineage": "pass",
            "result_identity_and_digest": "pass",
        },
        "differences": [
            {
                "concern": "media",
                "a": "image/svg+xml",
                "b": "text/markdown",
                "classification": "representation-specific",
            },
            {
                "concern": "structure",
                "a": "spatial groups and arrow",
                "b": "ordered path-value rows",
                "classification": "representation-specific",
            },
            {
                "concern": "lineage visibility",
                "a": "selected paths plus exact Result binding",
                "b": "all frozen leaf paths plus exact Result binding",
                "classification": "disclosed mapping loss",
            },
        ],
        "discarded_differences": 0,
        "semantic_authority": "immutable-result-only",
        "human_authority": "review-required",
        "verdict": "pass",
        "bounded_conclusion": (
            "The two completed Representations preserve the frozen required "
            "meaning and boundaries for result-001; no general conformance is claimed."
        ),
    }


def blocked_review(reason: str, result_raw: bytes | None) -> dict[str, Any]:
    return {
        "id": "poa-003-representation-review",
        "status": "blocked",
        "reason": reason,
        "result_sha256": digest(result_raw) if result_raw is not None else None,
        "repair_attempted": False,
        "verdict": "fail",
    }


def main(argv: list[str]) -> int:
    if len(argv) != 4:
        sys.stderr.write(
            "usage: verify-representations.py RESULT REPRESENTATION_A_SVG "
            "REPRESENTATION_B_MARKDOWN\n"
        )
        return 64

    result_raw: bytes | None = None
    try:
        result_raw, result = load_result(Path(argv[1]))
        svg_raw = Path(argv[2]).read_bytes()
        markdown_raw = Path(argv[3]).read_bytes()
        review = complete_review(result_raw, result, svg_raw, markdown_raw)
        sys.stdout.write(json.dumps(review, ensure_ascii=False, indent=2) + "\n")
        return 0
    except VerificationError as exc:
        review = blocked_review(exc.reason, result_raw)
        sys.stdout.write(json.dumps(review, ensure_ascii=False, indent=2) + "\n")
        return 2
    except (IndexError, KeyError, OSError, TypeError, ValueError) as exc:
        review = blocked_review(f"invalid_required_input:{exc}", result_raw)
        sys.stdout.write(json.dumps(review, ensure_ascii=False, indent=2) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
