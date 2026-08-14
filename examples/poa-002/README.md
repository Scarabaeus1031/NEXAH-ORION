# POA-002 — Processor Equivalence

This directory implements only the frozen
[`POA_002_PROCESSOR_EQUIVALENCE.md`](../../docs/experiments/POA_002_PROCESSOR_EQUIVALENCE.md)
experiment.

It reuses the exact committed POA-001 Request, Observation, OLS Expression,
Processor A, and Result A. It adds one independently implemented Processor B,
one Equivalence Review, one static Representation, and one Human Review.

```text
Observation + OLS Expression
          ├────────────────┐
          ↓                ↓
     Processor A      Processor B
          ↓                ↓
       Result A          Result B
          └───────┬────────┘
                  ↓
        Equivalence Review
                  ↓
          static SVG → Human
```

The required level is semantic equivalence. Byte equivalence between Results is
not required and is expected to be false because their Result and Processor
identities must differ.

## Implementation independence

Processor A is the frozen POA-001 implementation. Processor B was authored anew
in a separate implementation task from the frozen POA-002 artifact
requirements. It does not copy, import, call, generate from, wrap, or
communicate with Processor A.

Predeclared method summaries:

- Processor A validates the frozen shapes and lineage, then subtracts the first
  ordered declared value from the second.
- Processor B indexes the two validated records by identifier, resolves the
  declared order, and sums the second value with the negated first.

The replay invokes each Processor as a separate process, in a separate empty
temporary working directory, with a clean environment, separate output paths,
and only the same Observation and Expression as data arguments. Neither
Processor reads the other's Result. This demonstrates implementation
independence for this experiment; it does not claim separate human authorship
or general independence.

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
POA2="$POA_ROOT/examples/poa-002"
cd "$POA2"

(cd "$POA1" && shasum -a 256 -c SHA256SUMS)
shasum -a 256 -c SHA256SUMS

POA_REPLAY_DIR="$(mktemp -d)"
POA_WORK_A="$POA_REPLAY_DIR/processor-a-work"
POA_WORK_B="$POA_REPLAY_DIR/processor-b-work"
POA_OUT_A="$POA_REPLAY_DIR/processor-a-output"
POA_OUT_B="$POA_REPLAY_DIR/processor-b-output"
POA_NEGATIVE="$POA_REPLAY_DIR/negative-inputs"
mkdir "$POA_WORK_A" "$POA_WORK_B" "$POA_OUT_A" "$POA_OUT_B" "$POA_NEGATIVE"

test -z "$(find "$POA_WORK_A" -mindepth 1 -print -quit)"
test -z "$(find "$POA_WORK_B" -mindepth 1 -print -quit)"

POA_PYTHON="$(command -v python3)"
POA_CLEAN_PATH="$(dirname "$POA_PYTHON"):/usr/bin:/bin"

(cd "$POA_WORK_A" && \
  env -i PATH="$POA_CLEAN_PATH" "$POA_PYTHON" "$POA1/compare.py" \
    "$POA1/observation.json" "$POA1/expression.json") \
  > "$POA_OUT_A/result-a-1.json"
(cd "$POA_WORK_A" && \
  env -i PATH="$POA_CLEAN_PATH" "$POA_PYTHON" "$POA1/compare.py" \
    "$POA1/observation.json" "$POA1/expression.json") \
  > "$POA_OUT_A/result-a-2.json"

(cd "$POA_WORK_B" && \
  env -i PATH="$POA_CLEAN_PATH" "$POA_PYTHON" "$POA2/processor-b.py" \
    "$POA1/observation.json" "$POA1/expression.json") \
  > "$POA_OUT_B/result-b-1.json"
(cd "$POA_WORK_B" && \
  env -i PATH="$POA_CLEAN_PATH" "$POA_PYTHON" "$POA2/processor-b.py" \
    "$POA1/observation.json" "$POA1/expression.json") \
  > "$POA_OUT_B/result-b-2.json"

cmp "$POA_OUT_A/result-a-1.json" "$POA_OUT_A/result-a-2.json"
cmp "$POA1/result.json" "$POA_OUT_A/result-a-1.json"
cmp "$POA_OUT_B/result-b-1.json" "$POA_OUT_B/result-b-2.json"
cmp "$POA2/result-b.json" "$POA_OUT_B/result-b-1.json"
! cmp -s "$POA_OUT_A/result-a-1.json" "$POA_OUT_B/result-b-1.json"

test -z "$(find "$POA_WORK_A" -mindepth 1 -print -quit)"
test -z "$(find "$POA_WORK_B" -mindepth 1 -print -quit)"

"$POA_PYTHON" - "$POA1" "$POA_NEGATIVE" <<'PY'
import json
from pathlib import Path
import sys

poa1 = Path(sys.argv[1])
target = Path(sys.argv[2])
expression = json.loads((poa1 / "expression.json").read_text(encoding="utf-8"))
observation = json.loads((poa1 / "observation.json").read_text(encoding="utf-8"))

unsupported = dict(expression)
unsupported["operator"] = "OBSERVE"
(target / "unsupported-operator.json").write_text(
    json.dumps(unsupported, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)

stale_observation = observation
stale_observation["records"][1]["declared_value"] = 6
(target / "stale-observation.json").write_text(
    json.dumps(stale_observation, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)

invalid_shape = dict(expression)
del invalid_shape["field"]
(target / "invalid-shape.json").write_text(
    json.dumps(invalid_shape, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
PY

set +e
(cd "$POA_WORK_A" && \
  env -i PATH="$POA_CLEAN_PATH" "$POA_PYTHON" "$POA1/compare.py" \
    "$POA1/observation.json" "$POA_NEGATIVE/unsupported-operator.json") \
  > "$POA_OUT_A/unsupported-operator.json"
POA_STATUS_A=$?
(cd "$POA_WORK_B" && \
  env -i PATH="$POA_CLEAN_PATH" "$POA_PYTHON" "$POA2/processor-b.py" \
    "$POA1/observation.json" "$POA_NEGATIVE/unsupported-operator.json") \
  > "$POA_OUT_B/unsupported-operator.json"
POA_STATUS_B=$?
set -e
test "$POA_STATUS_A" -eq 2
test "$POA_STATUS_B" -eq 2

set +e
(cd "$POA_WORK_A" && \
  env -i PATH="$POA_CLEAN_PATH" "$POA_PYTHON" "$POA1/compare.py" \
    "$POA_NEGATIVE/stale-observation.json" "$POA1/expression.json") \
  > "$POA_OUT_A/stale-observation.json"
POA_STATUS_A=$?
(cd "$POA_WORK_B" && \
  env -i PATH="$POA_CLEAN_PATH" "$POA_PYTHON" "$POA2/processor-b.py" \
    "$POA_NEGATIVE/stale-observation.json" "$POA1/expression.json") \
  > "$POA_OUT_B/stale-observation.json"
POA_STATUS_B=$?
set -e
test "$POA_STATUS_A" -eq 2
test "$POA_STATUS_B" -eq 2

set +e
(cd "$POA_WORK_A" && \
  env -i PATH="$POA_CLEAN_PATH" "$POA_PYTHON" "$POA1/compare.py" \
    "$POA1/observation.json" "$POA_NEGATIVE/invalid-shape.json") \
  > "$POA_OUT_A/invalid-shape.json"
POA_STATUS_A=$?
(cd "$POA_WORK_B" && \
  env -i PATH="$POA_CLEAN_PATH" "$POA_PYTHON" "$POA2/processor-b.py" \
    "$POA1/observation.json" "$POA_NEGATIVE/invalid-shape.json") \
  > "$POA_OUT_B/invalid-shape.json"
POA_STATUS_B=$?
set -e
test "$POA_STATUS_A" -eq 2
test "$POA_STATUS_B" -eq 2

"$POA_PYTHON" verify-equivalence.py \
  "$POA1" "$POA2" \
  "$POA_OUT_A/result-a-1.json" "$POA_OUT_B/result-b-1.json" \
  "$POA_OUT_A" "$POA_OUT_B" \
  > "$POA_REPLAY_DIR/equivalence-review-1.json"
"$POA_PYTHON" verify-equivalence.py \
  "$POA1" "$POA2" \
  "$POA_OUT_A/result-a-2.json" "$POA_OUT_B/result-b-2.json" \
  "$POA_OUT_A" "$POA_OUT_B" \
  > "$POA_REPLAY_DIR/equivalence-review-2.json"

cmp equivalence-review.json "$POA_REPLAY_DIR/equivalence-review-1.json"
cmp "$POA_REPLAY_DIR/equivalence-review-1.json" \
  "$POA_REPLAY_DIR/equivalence-review-2.json"

"$POA_PYTHON" render-svg.py \
  "$POA_REPLAY_DIR/equivalence-review-1.json" \
  > "$POA_REPLAY_DIR/equivalence-1.svg"
"$POA_PYTHON" render-svg.py \
  "$POA_REPLAY_DIR/equivalence-review-2.json" \
  > "$POA_REPLAY_DIR/equivalence-2.svg"

cmp equivalence.svg "$POA_REPLAY_DIR/equivalence-1.svg"
cmp "$POA_REPLAY_DIR/equivalence-1.svg" "$POA_REPLAY_DIR/equivalence-2.svg"

"$POA_PYTHON" - "$POA_REPLAY_DIR/equivalence-review-1.json" \
  "$POA_REPLAY_DIR/equivalence-1.svg" <<'PY'
import hashlib
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

review_path = Path(sys.argv[1])
svg_path = Path(sys.argv[2])
review = json.loads(review_path.read_text(encoding="utf-8"))

assert review["verdict"]["status"] == "pass"
assert review["byte_equivalence"]["equal"] is False
assert review["structural_equivalence"]["equal"] is True
assert review["semantic_equivalence"]["equal"] is True
assert review["differences"]["discarded_before_classification"] == 0
assert review["differences"]["parsed_path_count"] == 3
assert all(
    difference["classification"] == "implementation-specific"
    for difference in review["differences"]["parsed"]
)
assert all(
    case["boundary_equivalent"]
    for case in review["boundary_checks"]["stop_cases"]
)

root = ET.parse(svg_path).getroot()
metadata = next(element for element in root if element.tag.endswith("metadata"))
assert metadata.attrib["data-equivalence-review-id"] == review["id"]
assert metadata.attrib["data-equivalence-review-sha256"] == hashlib.sha256(
    review_path.read_bytes()
).hexdigest()

def resolve(value, pointer):
    for part in pointer.lstrip("/").split("/"):
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value

groups = [element for element in root.iter() if element.tag.endswith("}g")]
assert groups
for element in groups:
    assert element.attrib["id"]
    resolve(review, element.attrib["data-equivalence-review-path"])
PY

cp equivalence.svg "$POA_REPLAY_DIR/equivalence-edited.svg"
printf '\n<!-- temporary Representation-only edit -->\n' \
  >> "$POA_REPLAY_DIR/equivalence-edited.svg"
! cmp -s equivalence.svg "$POA_REPLAY_DIR/equivalence-edited.svg"
cmp equivalence-review.json "$POA_REPLAY_DIR/equivalence-review-1.json"
cmp "$POA1/result.json" "$POA_OUT_A/result-a-1.json"
cmp result-b.json "$POA_OUT_B/result-b-1.json"

grep -F -- "- Review status: **PASS**" review.md > /dev/null
(cd "$POA1" && shasum -a 256 -c SHA256SUMS)
shasum -a 256 -c SHA256SUMS

echo "Replay candidates: $POA_REPLAY_DIR"
echo "POA-002 PASS"
```

The temporary directory is deliberately retained for inspection. It contains
both deterministic positive replays, every blocked negative Result, two
Equivalence Review replays, and two SVG replays. No committed artifact is
overwritten.

## Expected outcome

- Processor A reproduces committed POA-001 `result.json`.
- Processor B reproduces committed `result-b.json`.
- Each Processor is byte-stable against itself.
- Result A and Result B are not byte-equivalent.
- Both Results are structurally equivalent.
- Both Results are semantically equivalent for the frozen `COMPARE` slice.
- The only parsed differences are Result identity, Processor identity, and
  Processor source digest.
- Both Processors block all three negative cases with equivalent boundaries.
- The Equivalence Review and SVG reproduce committed bytes.
- `equivalence.svg` remains a non-authoritative projection of the Review.

## Human inspection

Open `equivalence.svg`, then read `review.md`. They expose the shared inputs,
both implementations, both Results, all semantic comparison rows, every
identity difference, all STOP outcomes, and the final bounded verdict without
requiring Processor source inspection.

## Claim boundary

POA-002 validates semantic equivalence between these two independent Processor
implementations only for this single frozen experiment. It does not validate
general Processor conformance, arbitrary OLS operators, Representation
independence beyond this experiment, distributed execution, interoperability
in general, or domain validity.
