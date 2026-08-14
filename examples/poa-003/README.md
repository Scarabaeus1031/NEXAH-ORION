# POA-003 — Representation Independence

This directory implements only the frozen
[`POA_003_REPRESENTATION_INDEPENDENCE.md`](../../docs/experiments/POA_003_REPRESENTATION_INDEPENDENCE.md)
experiment.

It reuses one immutable POA-001 Result. Representation A is the committed
POA-001 static SVG. Representation B is an independently rendered Markdown
table. A deterministic Review compares both completed Representations with the
Result, and a Human inspects the A–B–C relation.

```text
                 POA-001 Result
                    /       \
                   ▼         ▼
             A: SVG       B: Markdown
                   \         /
                    ▼       ▼
                  C: Human Review
```

A, B, and C are explanatory review labels only. POA-003 does not introduce an
A–B–C grammar, a D–E observer axis, an OPU, or another architecture.

## Artifact responsibilities

| Artifact | Responsibility |
| --- | --- |
| `render-markdown.py` | Reads only the immutable Result and deterministically produces Representation B |
| `result-table.md` | Committed non-authoritative Markdown Representation |
| `verify-representations.py` | Verifies the two completed Representations without rendering, processing OLS, or repairing input |
| `representation-review.json` | Immutable machine-readable Review of preservation, differences, and mapping loss |
| `review.md` | Human A–B–C review requiring no source-code inspection |
| `SHA256SUMS` | Integrity digests for all other POA-003 artifacts |

Representation A remains
`../poa-001/result.svg`; POA-003 does not copy or modify it.

## Requirements

- Python 3.11 or later;
- `shasum`;
- `cmp`;
- a POSIX-compatible shell;
- no network or external package.

## Exact offline replay commands

Run this complete block from anywhere inside the repository:

```bash
set -eu

POA_ROOT="$(git rev-parse --show-toplevel)"
POA1="$POA_ROOT/examples/poa-001"
POA3="$POA_ROOT/examples/poa-003"
cd "$POA3"

(cd "$POA1" && shasum -a 256 -c SHA256SUMS)
shasum -a 256 -c SHA256SUMS

POA_REPLAY_DIR="$(mktemp -d)"
POA_REP_A="$POA_REPLAY_DIR/representation-a"
POA_REP_B="$POA_REPLAY_DIR/representation-b"
POA_REVIEWS="$POA_REPLAY_DIR/reviews"
POA_NEGATIVE="$POA_REPLAY_DIR/negative"
mkdir "$POA_REP_A" "$POA_REP_B" "$POA_REVIEWS" "$POA_NEGATIVE"

POA_PYTHON="$(command -v python3)"
POA_CLEAN_PATH="$(dirname "$POA_PYTHON"):/usr/bin:/bin"

env -i PATH="$POA_CLEAN_PATH" "$POA_PYTHON" "$POA1/render-svg.py" \
  "$POA1/result.json" > "$POA_REP_A/result-1.svg"
env -i PATH="$POA_CLEAN_PATH" "$POA_PYTHON" "$POA1/render-svg.py" \
  "$POA1/result.json" > "$POA_REP_A/result-2.svg"

env -i PATH="$POA_CLEAN_PATH" "$POA_PYTHON" "$POA3/render-markdown.py" \
  "$POA1/result.json" > "$POA_REP_B/result-table-1.md"
env -i PATH="$POA_CLEAN_PATH" "$POA_PYTHON" "$POA3/render-markdown.py" \
  "$POA1/result.json" > "$POA_REP_B/result-table-2.md"

cmp "$POA_REP_A/result-1.svg" "$POA_REP_A/result-2.svg"
cmp "$POA1/result.svg" "$POA_REP_A/result-1.svg"
cmp "$POA_REP_B/result-table-1.md" "$POA_REP_B/result-table-2.md"
cmp "$POA3/result-table.md" "$POA_REP_B/result-table-1.md"
! cmp -s "$POA_REP_A/result-1.svg" "$POA_REP_B/result-table-1.md"

env -i PATH="$POA_CLEAN_PATH" "$POA_PYTHON" \
  "$POA3/verify-representations.py" \
  "$POA1/result.json" \
  "$POA_REP_A/result-1.svg" \
  "$POA_REP_B/result-table-1.md" \
  > "$POA_REVIEWS/review-1.json"
env -i PATH="$POA_CLEAN_PATH" "$POA_PYTHON" \
  "$POA3/verify-representations.py" \
  "$POA1/result.json" \
  "$POA_REP_A/result-2.svg" \
  "$POA_REP_B/result-table-2.md" \
  > "$POA_REVIEWS/review-2.json"

cmp "$POA_REVIEWS/review-1.json" "$POA_REVIEWS/review-2.json"
cmp "$POA3/representation-review.json" "$POA_REVIEWS/review-1.json"

"$POA_PYTHON" - "$POA_REP_B/result-table-1.md" "$POA_NEGATIVE" <<'PY'
from pathlib import Path
import sys

source = Path(sys.argv[1]).read_text(encoding="utf-8")
target = Path(sys.argv[2])

cases = {
    "stale-digest.md": (
        "<!-- poa-003:result-sha256="
        "6d565b327ed812f7b4e3b2239298e07715bdf3ac077d759d48263ce1279bb6b3 -->",
        "<!-- poa-003:result-sha256="
        "0000000000000000000000000000000000000000000000000000000000000000 -->",
    ),
    "invented-value.md": (
        "| `/comparison/signed_difference` | `3` |",
        "| `/comparison/signed_difference` | `4` |",
    ),
    "missing-uncertainty.md": (
        "| `/uncertainty/limitation` | "
        '`"The supplied values are not independently validated."` |\n',
        "",
    ),
    "missing-evidence.md": (
        '| `/evidence/1/value` | `"supplied-record-b"` |\n',
        "",
    ),
    "missing-prohibition.md": (
        '| `/prohibited_implications/2` | `"domain-validity"` |\n',
        "",
    ),
    "authority-claim.md": (
        "<!-- poa-003:authority=non-authoritative -->",
        "<!-- poa-003:authority=semantic -->",
    ),
    "missing-trace-path.md": (
        '| `/id` | `"result-001"` |\n',
        "",
    ),
}

for name, (old, new) in cases.items():
    if old not in source:
        raise SystemExit(f"negative fixture source not found: {name}")
    (target / name).write_text(
        source.replace(old, new, 1),
        encoding="utf-8",
    )
PY

for POA_CASE in \
  stale-digest \
  invented-value \
  missing-uncertainty \
  missing-evidence \
  missing-prohibition \
  authority-claim \
  missing-trace-path
do
  set +e
  env -i PATH="$POA_CLEAN_PATH" "$POA_PYTHON" \
    "$POA3/verify-representations.py" \
    "$POA1/result.json" \
    "$POA_REP_A/result-1.svg" \
    "$POA_NEGATIVE/$POA_CASE.md" \
    > "$POA_NEGATIVE/$POA_CASE.json"
  POA_CASE_EXIT=$?
  set -e
  test "$POA_CASE_EXIT" -eq 2
done

"$POA_PYTHON" - "$POA_NEGATIVE" <<'PY'
import json
from pathlib import Path
import sys

target = Path(sys.argv[1])
expected = {
    "stale-digest": "representation_b_stale_result_digest",
    "invented-value": "representation_b_changed_or_invented_value",
    "missing-uncertainty": "representation_b_changed_or_missing_uncertainty",
    "missing-evidence": "representation_b_changed_or_missing_evidence",
    "missing-prohibition": "representation_b_missing_prohibited_implication",
    "authority-claim": "representation_b_claims_authority",
    "missing-trace-path": "representation_b_missing_required_trace_path",
}
for name, reason in expected.items():
    record = json.loads((target / f"{name}.json").read_text(encoding="utf-8"))
    assert record == {
        "id": "poa-003-representation-review",
        "status": "blocked",
        "reason": reason,
        "result_sha256": (
            "6d565b327ed812f7b4e3b2239298e07715bdf3ac077d759d48263ce1279bb6b3"
        ),
        "repair_attempted": False,
        "verdict": "fail",
    }
PY

"$POA_PYTHON" - "$POA3" <<'PY'
import ast
from pathlib import Path
import sys

root = Path(sys.argv[1])
renderer = root / "render-markdown.py"
source = renderer.read_text(encoding="utf-8")
tree = ast.parse(source, filename=str(renderer))
local_or_external = []
for node in ast.walk(tree):
    if isinstance(node, ast.Import):
        local_or_external.extend(alias.name for alias in node.names)
    elif isinstance(node, ast.ImportFrom) and node.module != "__future__":
        local_or_external.append(node.module or "")
allowed = {"hashlib", "json", "pathlib", "sys", "typing"}
assert set(local_or_external) <= allowed
assert "result.svg" not in source
assert "render-svg.py" not in source
assert "compare.py" not in source
PY

(cd "$POA1" && shasum -a 256 -c SHA256SUMS)
shasum -a 256 -c SHA256SUMS

echo "Representation A deterministic replay: PASS"
echo "Representation B deterministic replay: PASS"
echo "Committed Representation comparison: PASS"
echo "Representation Review deterministic replay: PASS"
echo "stale Result digest blocked: PASS"
echo "invented value blocked: PASS"
echo "missing uncertainty blocked: PASS"
echo "missing evidence blocked: PASS"
echo "missing prohibited implication blocked: PASS"
echo "authority claim blocked: PASS"
echo "missing trace path blocked: PASS"
echo "checksum verification: PASS"
echo "POA-003 PASS"
```

All generated candidates and negative evidence are written below one temporary
directory. No replay command overwrites committed POA-001 or POA-003 evidence.

To execute the exact block from the repository root:

```bash
awk 'BEGIN {inside=0} /^```bash$/ {inside=1; next} inside && /^```$/ {exit} inside {print}' \
  examples/poa-003/README.md | bash
```

## Expected bounded result

The experiment passes only if the committed SVG and Markdown table bind the
same immutable Result and preserve the required comparison, evidence,
uncertainty, limitation, prohibited implications, and lineage. Their bytes,
media, structures, visibility, and mapping losses remain different.

This is evidence only for two Representations of `result-001`. It is not
general Representation conformance, domain validation, an observer theory, or
proof of OLS, Processor, Runtime, OPU, or application behavior.
