#!/usr/bin/env python3
"""POA-001: deterministic static projection of one immutable Result."""

from __future__ import annotations

import hashlib
from html import escape
import json
from pathlib import Path
import sys
from typing import Any


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
EXPECTED_COMPARISON_KEYS = {"field", "sources", "signed_difference"}
EXPECTED_SOURCE_KEYS = {"record_ref", "value"}


def text(value: Any) -> str:
    return escape(str(value), quote=True)


def load_complete_result(path: Path) -> tuple[bytes, dict[str, Any]]:
    raw = path.read_bytes()
    try:
        result = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("Result is not valid JSON") from exc

    if not isinstance(result, dict) or set(result) != EXPECTED_RESULT_KEYS:
        raise ValueError("Result does not have the frozen complete shape")
    comparison = result.get("comparison")
    if (
        result.get("status") != "complete"
        or not isinstance(comparison, dict)
        or set(comparison) != EXPECTED_COMPARISON_KEYS
        or not isinstance(comparison.get("sources"), list)
        or len(comparison["sources"]) != 2
        or any(
            not isinstance(source, dict) or set(source) != EXPECTED_SOURCE_KEYS
            for source in comparison["sources"]
        )
        or not isinstance(result.get("evidence"), list)
        or len(result["evidence"]) != 2
        or not isinstance(result.get("uncertainty"), dict)
        or not isinstance(result.get("prohibited_implications"), list)
    ):
        raise ValueError("Result cannot be projected without reinterpretation")
    return raw, result


def render(result_raw: bytes, result: dict[str, Any]) -> str:
    comparison = result["comparison"]
    sources = comparison["sources"]
    evidence = result["evidence"]
    uncertainty = result["uncertainty"]
    uncertainty_records = uncertainty["records"]
    result_sha256 = hashlib.sha256(result_raw).hexdigest()

    source_a = sources[0]
    source_b = sources[1]
    uncertainty_text = (
        f'{uncertainty_records[0]["record_ref"]}: '
        f'{uncertainty_records[0]["value"]}; '
        f'{uncertainty_records[1]["record_ref"]}: '
        f'{uncertainty_records[1]["value"]}'
    )
    limitation_text = uncertainty["limitation"]
    prohibited_text = ", ".join(result["prohibited_implications"])

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="960" height="500" viewBox="0 0 960 500" role="img" aria-labelledby="title description">
  <title id="title">POA-001 comparison result</title>
  <desc id="description">A traceable static representation of {text(result["id"])}.</desc>
  <metadata id="poa-001-lineage" data-result-id="{text(result["id"])}" data-result-sha256="{result_sha256}" />
  <style>
    .background {{ fill: #f7f4ed; }}
    .panel {{ fill: #ffffff; stroke: #243447; stroke-width: 2; }}
    .heading {{ fill: #17212b; font: 700 24px sans-serif; }}
    .label {{ fill: #243447; font: 700 17px sans-serif; }}
    .value {{ fill: #0b6e4f; font: 700 36px sans-serif; }}
    .detail {{ fill: #425466; font: 14px sans-serif; }}
    .difference {{ fill: #8a3ffc; font: 700 20px sans-serif; }}
    .boundary {{ fill: #7a3e00; font: 14px sans-serif; }}
    .footer {{ fill: #5b6573; font: 12px monospace; }}
    .arrow {{ stroke: #8a3ffc; stroke-width: 4; fill: none; }}
  </style>
  <g id="result-title" data-result-path="/id">
    <rect class="background" x="0" y="0" width="960" height="500" />
    <text class="heading" x="40" y="48">Result: {text(result["id"])}</text>
  </g>
  <g id="record-a" data-result-path="/comparison/sources/0">
    <rect class="panel" x="70" y="95" width="300" height="150" rx="8" />
    <text class="label" x="95" y="130">{text(source_a["record_ref"])}</text>
    <text class="value" x="95" y="185">{text(source_a["value"])}</text>
    <text class="detail" x="95" y="218">field: {text(comparison["field"])}</text>
  </g>
  <g id="record-a-evidence" data-result-path="/evidence/0">
    <text class="detail" x="95" y="238">evidence: {text(evidence[0]["value"])}</text>
  </g>
  <g id="record-b" data-result-path="/comparison/sources/1">
    <rect class="panel" x="590" y="95" width="300" height="150" rx="8" />
    <text class="label" x="615" y="130">{text(source_b["record_ref"])}</text>
    <text class="value" x="615" y="185">{text(source_b["value"])}</text>
    <text class="detail" x="615" y="218">field: {text(comparison["field"])}</text>
  </g>
  <g id="record-b-evidence" data-result-path="/evidence/1">
    <text class="detail" x="615" y="238">evidence: {text(evidence[1]["value"])}</text>
  </g>
  <g id="signed-difference" data-result-path="/comparison/signed_difference">
    <path class="arrow" d="M 390 165 L 565 165" />
    <path class="arrow" d="M 550 153 L 565 165 L 550 177" />
    <text class="difference" x="425" y="145">difference: {text(comparison["signed_difference"])}</text>
  </g>
  <g id="uncertainty" data-result-path="/uncertainty">
    <text class="boundary" x="40" y="295">Uncertainty: {text(uncertainty_text)}</text>
    <text class="boundary" x="40" y="325">Limitation: {text(limitation_text)}</text>
  </g>
  <g id="prohibited-implications" data-result-path="/prohibited_implications">
    <text class="boundary" x="40" y="365">Does not imply: {text(prohibited_text)}</text>
  </g>
  <g id="processor-footer" data-result-path="/processor">
    <text class="footer" x="40" y="420">processor: {text(result["processor"])}</text>
    <text class="footer" x="40" y="445">result sha256: {result_sha256}</text>
  </g>
</svg>
"""


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        sys.stderr.write("usage: render-svg.py RESULT\n")
        return 64
    try:
        raw, result = load_complete_result(Path(argv[1]))
        sys.stdout.write(render(raw, result))
        return 0
    except (KeyError, OSError, TypeError, ValueError) as exc:
        sys.stderr.write(f"cannot render Result: {exc}\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
