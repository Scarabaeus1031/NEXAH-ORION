#!/usr/bin/env python3
"""Render one static view of an immutable POA-002 Equivalence Review."""

from __future__ import annotations

import hashlib
import html
import json
from pathlib import Path
import sys
from typing import Any


def escape(value: Any) -> str:
    return html.escape(str(value), quote=True)


def compact(value: Any) -> str:
    if isinstance(value, bool):
        return "PASS" if value else "FAIL"
    if isinstance(value, list):
        if value and all(isinstance(item, str) for item in value):
            return ", ".join(value)
        if value and all(isinstance(item, dict) for item in value):
            parts = []
            for item in value:
                if "record_ref" in item:
                    parts.append(f"{item['record_ref']}={item.get('value')}")
                elif "case" in item:
                    parts.append(
                        f"{item['case']}:{item.get('status')}:"
                        f"comparison={item.get('comparison_present')}"
                    )
                else:
                    parts.append(json.dumps(item, separators=(",", ":")))
            return "; ".join(parts)
    if isinstance(value, dict):
        if "records" in value and "limitation" in value:
            records = "; ".join(
                f"{item['record_ref']}={item['value']}"
                for item in value["records"]
            )
            return f"{records}; limitation={value['limitation']}"
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return str(value)


def clipped(value: Any, limit: int) -> str:
    rendered = compact(value)
    return rendered if len(rendered) <= limit else rendered[: limit - 1] + "…"


def text_line(x: int, y: int, value: Any, css_class: str = "body") -> str:
    return (
        f'<text x="{x}" y="{y}" class="{css_class}">'
        f"{escape(value)}</text>"
    )


def group(group_id: str, path: str, lines: list[str]) -> str:
    return (
        f'<g id="{escape(group_id)}" '
        f'data-equivalence-review-path="{escape(path)}">'
        + "".join(lines)
        + "</g>"
    )


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: render-svg.py EQUIVALENCE_REVIEW")

    review_path = Path(sys.argv[1])
    review_raw = review_path.read_bytes()
    review = json.loads(review_raw)
    required = {
        "id",
        "inputs",
        "processors",
        "results",
        "byte_equivalence",
        "structural_equivalence",
        "semantic_equivalence",
        "differences",
        "boundary_checks",
        "verdict",
    }
    if not isinstance(review, dict) or set(review) != required:
        raise SystemExit("invalid Equivalence Review shape")

    review_digest = hashlib.sha256(review_raw).hexdigest()
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="2000" '
        'viewBox="0 0 1800 2000" role="img" '
        'aria-labelledby="title description">',
        (
            f'<metadata data-equivalence-review-id="{escape(review["id"])}" '
            f'data-equivalence-review-sha256="{review_digest}"/>'
        ),
        "<title id=\"title\">POA-002 Processor Equivalence</title>",
        (
            "<desc id=\"description\">Static, non-authoritative view of the "
            "immutable POA-002 Equivalence Review.</desc>"
        ),
        """<style>
        .canvas { fill: #f5f2ea; }
        .panel { fill: #fffdf8; stroke: #273746; stroke-width: 2; }
        .pass { fill: #e7f4ea; stroke: #23683b; stroke-width: 2; }
        .identity { fill: #e9eff7; stroke: #345a78; stroke-width: 2; }
        .title { font: 700 32px system-ui, sans-serif; fill: #17202a; }
        .section { font: 700 21px system-ui, sans-serif; fill: #17202a; }
        .body { font: 16px ui-monospace, SFMono-Regular, monospace; fill: #17202a; }
        .small { font: 13px ui-monospace, SFMono-Regular, monospace; fill: #273746; }
        .verdict { font: 700 25px system-ui, sans-serif; fill: #174c2b; }
        </style>""",
        group(
            "canvas",
            "/id",
            ['<rect class="canvas" x="0" y="0" width="1800" height="2000"/>'],
        ),
        group(
            "review-title",
            "/id",
            [
                text_line(70, 65, "POA-002 — Processor Equivalence", "title"),
                text_line(70, 95, f"Review: {review['id']}", "body"),
            ],
        ),
    ]

    inputs = review["inputs"]
    parts.append(
        group(
            "shared-inputs",
            "/inputs",
            [
                '<rect class="panel" x="55" y="125" width="1690" height="165" rx="12"/>',
                text_line(80, 160, "Shared frozen inputs", "section"),
                text_line(80, 195, f"Request     {inputs['request']['sha256']}", "body"),
                text_line(
                    80, 230, f"Observation {inputs['observation']['sha256']}", "body"
                ),
                text_line(
                    80, 265, f"Expression  {inputs['expression']['sha256']}", "body"
                ),
            ],
        )
    )

    for key, x in (("processor_a", 55), ("processor_b", 915)):
        processor = review["processors"][key]
        path = f"/processors/{key}"
        parts.append(
            group(
                key,
                path,
                [
                    f'<rect class="identity" x="{x}" y="320" width="830" height="180" rx="12"/>',
                    text_line(x + 25, 355, processor["identity"], "section"),
                    text_line(
                        x + 25, 390, f"source {processor['source_path']}", "body"
                    ),
                    text_line(
                        x + 25, 420, f"sha256 {processor['source_sha256']}", "small"
                    ),
                    text_line(
                        x + 25,
                        450,
                        f"workdir {processor['working_directory']}",
                        "body",
                    ),
                    text_line(
                        x + 25,
                        480,
                        f"method {clipped(processor['method_summary'], 92)}",
                        "small",
                    ),
                ],
            )
        )

    results = review["results"]
    parts.append(
        group(
            "result-identities",
            "/results",
            [
                '<rect class="panel" x="55" y="530" width="1690" height="125" rx="12"/>',
                text_line(80, 565, "Independent Results", "section"),
                text_line(
                    80,
                    600,
                    f"A {results['result_a']['id']}  {results['result_a']['sha256']}",
                    "body",
                ),
                text_line(
                    80,
                    630,
                    f"B {results['result_b']['id']}  {results['result_b']['sha256']}",
                    "body",
                ),
            ],
        )
    )

    overview = [
        f"Byte equivalence: {'YES' if review['byte_equivalence']['equal'] else 'NO'} "
        "(not required)",
        f"Structural equivalence: {compact(review['structural_equivalence']['equal'])}",
        f"Semantic equivalence: {compact(review['semantic_equivalence']['equal'])}",
    ]
    parts.append(
        group(
            "equivalence-levels",
            "/semantic_equivalence/equal",
            [
                '<rect class="pass" x="55" y="685" width="1690" height="95" rx="12"/>',
                text_line(80, 720, overview[0], "body"),
                text_line(650, 720, overview[1], "body"),
                text_line(1180, 720, overview[2], "body"),
                text_line(
                    80,
                    755,
                    "Required level: semantic equivalence; implementation identities remain visible.",
                    "small",
                ),
            ],
        )
    )

    y = 825
    parts.append(
        group(
            "semantic-heading",
            "/semantic_equivalence/comparisons",
            [text_line(70, y, "Semantic comparison rows", "section")],
        )
    )
    y += 35
    for index, row in enumerate(review["semantic_equivalence"]["comparisons"]):
        path = f"/semantic_equivalence/comparisons/{index}"
        left = clipped(row["result_a"], 68)
        right = clipped(row["result_b"], 68)
        parts.append(
            group(
                f"semantic-row-{index + 1}",
                path,
                [
                    text_line(
                        80,
                        y,
                        f"{row['concern']}: {compact(row['pass'])} | {row['required_relation']}",
                        "body",
                    ),
                    text_line(540, y, f"A={left}", "small"),
                    text_line(1160, y, f"B={right}", "small"),
                ],
            )
        )
        y += 42

    y += 5
    parts.append(
        group(
            "difference-heading",
            "/differences",
            [
                text_line(70, y, "Visible implementation-specific differences", "section"),
                text_line(
                    730,
                    y,
                    (
                        f"raw segments={review['differences']['raw_segment_count']}; "
                        f"discarded={review['differences']['discarded_before_classification']}"
                    ),
                    "body",
                ),
            ],
        )
    )
    y += 38
    for index, difference in enumerate(review["differences"]["parsed"]):
        parts.append(
            group(
                f"difference-{index + 1}",
                f"/differences/parsed/{index}",
                [
                    text_line(
                        80,
                        y,
                        (
                            f"{difference['path']}: "
                            f"A={clipped(difference['result_a'], 50)} | "
                            f"B={clipped(difference['result_b'], 50)} | "
                            f"{difference['classification']}"
                        ),
                        "body",
                    )
                ],
            )
        )
        y += 34

    boundary = review["boundary_checks"]
    y += 10
    boundary_rows = [
        ("Evidence preserved", "evidence_preserved"),
        ("Uncertainty and limitation preserved", "uncertainty_and_limitation_preserved"),
        ("Prohibited implications preserved", "prohibited_implications_preserved"),
        ("No invented information", "invented_information"),
        ("Equivalent STOP behavior", "stop_equivalence"),
        ("No silent repair", "silent_repair"),
        ("No Processor communication", "processor_communication"),
    ]
    parts.append(
        group(
            "boundary-heading",
            "/boundary_checks",
            [text_line(70, y, "Boundary checks", "section")],
        )
    )
    y += 38
    for index, (label, key) in enumerate(boundary_rows):
        value = boundary[key]
        if key == "invented_information":
            value = value["pass"]
        elif key in {"silent_repair", "processor_communication"}:
            value = not value
        parts.append(
            group(
                f"boundary-{index + 1}",
                f"/boundary_checks/{key}",
                [text_line(80 + (index % 2) * 820, y, f"{label}: {compact(value)}", "body")],
            )
        )
        if index % 2 == 1:
            y += 36
    if len(boundary_rows) % 2:
        y += 36

    for index, stop in enumerate(boundary["stop_cases"]):
        parts.append(
            group(
                f"stop-case-{index + 1}",
                f"/boundary_checks/stop_cases/{index}",
                [
                    text_line(
                        80,
                        y,
                        (
                            f"STOP {stop['case']}: "
                            f"A={stop['processor_a']['reason']} | "
                            f"B={stop['processor_b']['reason']} | "
                            f"equivalent={compact(stop['boundary_equivalent'])}"
                        ),
                        "small",
                    )
                ],
            )
        )
        y += 30

    parts.append(
        group(
            "verdict",
            "/verdict",
            [
                f'<rect class="pass" x="55" y="{y + 15}" width="1690" height="100" rx="12"/>',
                text_line(
                    80,
                    y + 58,
                    f"VERDICT: {review['verdict']['status'].upper()}",
                    "verdict",
                ),
                text_line(300, y + 58, review["verdict"]["claim"], "body"),
                text_line(
                    80,
                    y + 92,
                    f"Review SHA-256: {review_digest}",
                    "small",
                ),
            ],
        )
    )
    parts.append("</svg>\n")
    sys.stdout.write("".join(parts))


if __name__ == "__main__":
    main()
