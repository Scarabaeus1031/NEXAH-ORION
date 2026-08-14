# POA-001 — Minimal Proof

This directory is the complete offline implementation of the frozen
[`POA_001_MINIMAL_PROOF.md`](../../docs/experiments/POA_001_MINIMAL_PROOF.md)
design.

It demonstrates one concrete chain:

```text
Reality
  ↓
Observation
  ↓
OLS
  ↓
Processor
  ↓
Record
  ↓
Representation
  ↓
Human
```

The subject outside formal ownership is the pair of supplied orientation
records. `observation.json` is the bounded input about that subject; it is not
reality or independently validated truth.

The only Processor capability is `COMPARE`. The Processor reads
`observation.json` and `expression.json` and writes a candidate Result to
standard output. `render-svg.py` reads only a Result and writes a candidate
static SVG to standard output. Neither program overwrites committed artifacts.

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

cd "$(git rev-parse --show-toplevel)/examples/poa-001"
shasum -a 256 -c SHA256SUMS

POA_REPLAY_DIR="$(mktemp -d)"
echo "Replay candidates: $POA_REPLAY_DIR"

python3 compare.py observation.json expression.json \
  > "$POA_REPLAY_DIR/result.json"
cmp result.json "$POA_REPLAY_DIR/result.json"

python3 render-svg.py "$POA_REPLAY_DIR/result.json" \
  > "$POA_REPLAY_DIR/result.svg"
cmp result.svg "$POA_REPLAY_DIR/result.svg"

python3 -c '
import json
import sys
from pathlib import Path

value = json.loads(Path("expression.json").read_text(encoding="utf-8"))
value["operator"] = "OBSERVE"
Path(sys.argv[1]).write_text(
    json.dumps(value, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
' "$POA_REPLAY_DIR/unsupported-operator.json"

set +e
python3 compare.py observation.json \
  "$POA_REPLAY_DIR/unsupported-operator.json" \
  > "$POA_REPLAY_DIR/blocked-unsupported.json"
POA_STATUS=$?
set -e
test "$POA_STATUS" -eq 2

python3 -c '
import json
import sys
from pathlib import Path

value = json.loads(Path("observation.json").read_text(encoding="utf-8"))
value["records"][1]["declared_value"] = 6
Path(sys.argv[1]).write_text(
    json.dumps(value, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
' "$POA_REPLAY_DIR/changed-observation.json"

set +e
python3 compare.py "$POA_REPLAY_DIR/changed-observation.json" expression.json \
  > "$POA_REPLAY_DIR/blocked-stale-digest.json"
POA_STATUS=$?
set -e
test "$POA_STATUS" -eq 2

python3 -c '
import json
import sys
from pathlib import Path

value = json.loads(Path("expression.json").read_text(encoding="utf-8"))
del value["field"]
Path(sys.argv[1]).write_text(
    json.dumps(value, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
' "$POA_REPLAY_DIR/invalid-shape.json"

set +e
python3 compare.py observation.json "$POA_REPLAY_DIR/invalid-shape.json" \
  > "$POA_REPLAY_DIR/blocked-invalid-shape.json"
POA_STATUS=$?
set -e
test "$POA_STATUS" -eq 2

python3 - "$POA_REPLAY_DIR" <<'PY'
import json
from pathlib import Path
import sys

root = Path(sys.argv[1])
expected_evidence = [
    {"record_ref": "record-a", "value": "supplied-record-a"},
    {"record_ref": "record-b", "value": "supplied-record-b"},
]
expected_uncertainty = {
    "records": [
        {"record_ref": "record-a", "value": "none-declared"},
        {"record_ref": "record-b", "value": "none-declared"},
    ],
    "limitation": "The supplied values are not independently validated.",
}
expected_prohibited = [
    "preference",
    "recommendation",
    "domain-validity",
]
cases = {
    "blocked-unsupported.json": "unsupported_operator",
    "blocked-stale-digest.json": "observation_digest_mismatch",
    "blocked-invalid-shape.json": "invalid_required_input_shape",
}
for filename, reason in cases.items():
    result = json.loads((root / filename).read_text(encoding="utf-8"))
    assert result["status"] == "blocked"
    assert result["reason"] == reason
    assert "comparison" not in result
    assert result["evidence"] == expected_evidence
    assert result["uncertainty"] == expected_uncertainty
    assert result["prohibited_implications"] == expected_prohibited
PY

python3 - <<'PY'
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

request = json.loads(Path("request.json").read_text(encoding="utf-8"))
observation = json.loads(Path("observation.json").read_text(encoding="utf-8"))
expression = json.loads(Path("expression.json").read_text(encoding="utf-8"))
result = json.loads(Path("result.json").read_text(encoding="utf-8"))

assert request["observation_ref"] == observation["id"]
assert expression["request_ref"] == request["id"]
assert expression["request_sha256"] == digest("request.json")
assert expression["observation_ref"] == observation["id"]
assert expression["observation_sha256"] == digest("observation.json")
assert result["expression_ref"] == expression["id"]
assert result["expression_sha256"] == digest("expression.json")
assert result["processor_sha256"] == digest("compare.py")

tree = ET.parse("result.svg")
root = tree.getroot()
metadata = next(element for element in root if element.tag.endswith("metadata"))
assert metadata.attrib["data-result-id"] == result["id"]
assert metadata.attrib["data-result-sha256"] == digest("result.json")

def resolve(value, pointer):
    for part in pointer.lstrip("/").split("/"):
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value

paths = [
    element.attrib["data-result-path"]
    for element in root.iter()
    if "data-result-path" in element.attrib
]
assert paths
for path in paths:
    resolve(result, path)
PY

python3 -c '
import sys
from pathlib import Path

source = Path("compare.py").read_text(encoding="utf-8")
old = "PROCESSOR_ID = \"poa-001-compare\""
new = "PROCESSOR_ID = \"poa-001-compare-mutated\""
assert source.count(old) == 1
Path(sys.argv[1]).write_text(source.replace(old, new), encoding="utf-8")
' "$POA_REPLAY_DIR/compare-mutated.py"

python3 "$POA_REPLAY_DIR/compare-mutated.py" \
  observation.json expression.json \
  > "$POA_REPLAY_DIR/result-mutated-processor.json"
! cmp -s result.json "$POA_REPLAY_DIR/result-mutated-processor.json"

python3 - "$POA_REPLAY_DIR/result-mutated-processor.json" <<'PY'
import json
from pathlib import Path
import sys

committed = json.loads(Path("result.json").read_text(encoding="utf-8"))
mutated = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
assert mutated["processor"] != committed["processor"]
assert mutated["processor_sha256"] != committed["processor_sha256"]
assert mutated["comparison"] == committed["comparison"]
assert mutated["evidence"] == committed["evidence"]
assert mutated["uncertainty"] == committed["uncertainty"]
assert mutated["prohibited_implications"] == committed["prohibited_implications"]
PY

cp result.svg "$POA_REPLAY_DIR/result-edited.svg"
printf '\n<!-- temporary representation-only edit -->\n' \
  >> "$POA_REPLAY_DIR/result-edited.svg"
! cmp -s result.svg "$POA_REPLAY_DIR/result-edited.svg"

shasum -a 256 -c SHA256SUMS
echo "POA-001 PASS"
```

The temporary directory is intentionally left available for inspection. It
contains only replay candidates and negative-test outputs.

## Expected positive Result

- status: `complete`;
- source values: `2`, then `5`;
- signed difference: `3`;
- evidence: `supplied-record-a`, `supplied-record-b`;
- uncertainty: `none-declared` for both records;
- limitation: the supplied values are not independently validated;
- prohibited implications: preference, recommendation, domain validity.

## Expected negative Results

| Case | Exit | Result status | Reason |
| --- | ---: | --- | --- |
| Unsupported operator | `2` | `blocked` | `unsupported_operator` |
| Changed Observation with stale digest | `2` | `blocked` | `observation_digest_mismatch` |
| Missing required Expression field | `2` | `blocked` | `invalid_required_input_shape` |

Every blocked Result has no `comparison` and preserves the original evidence,
uncertainty, limitation, and prohibited implications. The Processor neither
repairs the input nor invents a replacement value.

## Human inspection

Open `result.svg`, then read `review.md`. The review answers the five frozen
Human questions and maps every visible SVG group through `result.json`,
`expression.json`, and `observation.json`.

## Claim boundary

This concrete POA-001 experiment passes only the frozen POA-001 criteria. It
does not generally prove OLS, Processor interchangeability, scientific
validity, domain applicability, or the NEXAH architecture.
