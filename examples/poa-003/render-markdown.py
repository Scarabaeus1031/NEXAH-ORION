#!/usr/bin/env python3
"""POA-003: deterministic Markdown projection of one immutable Result."""

from __future__ import annotations

import hashlib
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
EXPECTED_EVIDENCE_KEYS = {"record_ref", "value"}
EXPECTED_UNCERTAINTY_KEYS = {"records", "limitation"}
EXPECTED_UNCERTAINTY_RECORD_KEYS = {"record_ref", "value"}


def load_complete_result(path: Path) -> tuple[bytes, dict[str, Any]]:
    raw = path.read_bytes()
    try:
        result = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("Result is not valid JSON") from exc

    if not isinstance(result, dict) or set(result) != EXPECTED_RESULT_KEYS:
        raise ValueError("Result does not have the frozen complete shape")
    if result.get("status") != "complete":
        raise ValueError("Result is not complete")

    comparison = result.get("comparison")
    evidence = result.get("evidence")
    uncertainty = result.get("uncertainty")
    if (
        not isinstance(comparison, dict)
        or set(comparison) != EXPECTED_COMPARISON_KEYS
        or not isinstance(comparison.get("sources"), list)
        or len(comparison["sources"]) != 2
        or any(
            not isinstance(item, dict) or set(item) != EXPECTED_SOURCE_KEYS
            for item in comparison["sources"]
        )
        or not isinstance(evidence, list)
        or len(evidence) != 2
        or any(
            not isinstance(item, dict) or set(item) != EXPECTED_EVIDENCE_KEYS
            for item in evidence
        )
        or not isinstance(uncertainty, dict)
        or set(uncertainty) != EXPECTED_UNCERTAINTY_KEYS
        or not isinstance(uncertainty.get("records"), list)
        or len(uncertainty["records"]) != 2
        or any(
            not isinstance(item, dict)
            or set(item) != EXPECTED_UNCERTAINTY_RECORD_KEYS
            for item in uncertainty["records"]
        )
        or not isinstance(result.get("prohibited_implications"), list)
    ):
        raise ValueError("Result cannot be projected without reinterpretation")
    return raw, result


def literal(value: Any) -> str:
    encoded = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return encoded.replace("|", "\\u007c").replace("`", "\\u0060")


def rows(result: dict[str, Any]) -> list[tuple[str, Any]]:
    comparison = result["comparison"]
    return [
        ("/id", result["id"]),
        ("/status", result["status"]),
        ("/expression_ref", result["expression_ref"]),
        ("/expression_sha256", result["expression_sha256"]),
        ("/processor", result["processor"]),
        ("/processor_sha256", result["processor_sha256"]),
        ("/comparison/field", comparison["field"]),
        (
            "/comparison/sources/0/record_ref",
            comparison["sources"][0]["record_ref"],
        ),
        ("/comparison/sources/0/value", comparison["sources"][0]["value"]),
        (
            "/comparison/sources/1/record_ref",
            comparison["sources"][1]["record_ref"],
        ),
        ("/comparison/sources/1/value", comparison["sources"][1]["value"]),
        (
            "/comparison/signed_difference",
            comparison["signed_difference"],
        ),
        ("/evidence/0/record_ref", result["evidence"][0]["record_ref"]),
        ("/evidence/0/value", result["evidence"][0]["value"]),
        ("/evidence/1/record_ref", result["evidence"][1]["record_ref"]),
        ("/evidence/1/value", result["evidence"][1]["value"]),
        (
            "/uncertainty/records/0/record_ref",
            result["uncertainty"]["records"][0]["record_ref"],
        ),
        (
            "/uncertainty/records/0/value",
            result["uncertainty"]["records"][0]["value"],
        ),
        (
            "/uncertainty/records/1/record_ref",
            result["uncertainty"]["records"][1]["record_ref"],
        ),
        (
            "/uncertainty/records/1/value",
            result["uncertainty"]["records"][1]["value"],
        ),
        ("/uncertainty/limitation", result["uncertainty"]["limitation"]),
        (
            "/prohibited_implications/0",
            result["prohibited_implications"][0],
        ),
        (
            "/prohibited_implications/1",
            result["prohibited_implications"][1],
        ),
        (
            "/prohibited_implications/2",
            result["prohibited_implications"][2],
        ),
    ]


def render(raw: bytes, result: dict[str, Any]) -> str:
    digest = hashlib.sha256(raw).hexdigest()
    table = "\n".join(
        f"| `{path}` | `{literal(value)}` |" for path, value in rows(result)
    )
    return f"""<!-- poa-003:representation-id=poa-003-markdown-table -->
<!-- poa-003:result-id={result["id"]} -->
<!-- poa-003:result-sha256={digest} -->
<!-- poa-003:authority=non-authoritative -->

# POA-003 Representation B — Tabular Result

This deterministic table presents the immutable Result identified below. It is
a non-authoritative Representation. It does not validate the source, recommend,
approve, decide, or change the Result.

| Binding | Value |
| --- | --- |
| Result | `{result["id"]}` |
| Result SHA-256 | `{digest}` |
| Media | `text/markdown` |
| Authority | `non-authoritative` |

## Result paths

Values are JSON literals so that strings and numbers remain distinguishable.

| Result path | JSON value |
| --- | --- |
{table}

## Declared mapping loss

- JSON nesting is flattened into explicit Result paths.
- The SVG's spatial relation and arrow are not reproduced.
- No value, evidence item, uncertainty statement, limitation, or prohibited
  implication is intentionally omitted.

The immutable Result, not this table, remains the semantic source.
"""


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        sys.stderr.write("usage: render-markdown.py RESULT\n")
        return 64
    try:
        raw, result = load_complete_result(Path(argv[1]))
        sys.stdout.write(render(raw, result))
        return 0
    except (IndexError, KeyError, OSError, TypeError, ValueError) as exc:
        sys.stderr.write(f"cannot render Result: {exc}\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
