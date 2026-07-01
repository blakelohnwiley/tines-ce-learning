#!/usr/bin/env bash
# Verify workflow library meets until-loop goals.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
WORKFLOWS="$PROJECT_ROOT/exports/workflows"
GENERATED="$PROJECT_ROOT/exports/generated-workflows.json"

MIN_TOTAL=29
MIN_NEW_COMPLEX=20
MIN_ACTIONS=8

fail() { echo "FAIL: $1" >&2; exit 1; }
pass() { echo "PASS: $1"; }

json_count=$(find "$WORKFLOWS" -maxdepth 1 -name '*.json' | wc -l | tr -d ' ')
[[ "$json_count" -ge "$MIN_TOTAL" ]] || fail "expected >= $MIN_TOTAL workflow JSON files, got $json_count"
pass "$json_count workflow JSON files on disk"

[[ -f "$GENERATED" ]] || fail "missing $GENERATED"
gen_count=$(python3 -c "import json; print(len(json.load(open('$GENERATED'))))")
[[ "$gen_count" -eq "$MIN_NEW_COMPLEX" ]] || fail "expected $MIN_NEW_COMPLEX generated workflows, got $gen_count"
pass "$gen_count generated complex workflows in manifest"

python3 <<'PY'
import json, glob, sys
from pathlib import Path

root = Path("exports/workflows")
generated = {e["id"] for e in json.load(open("exports/generated-workflows.json"))}

for wf_id in sorted(generated):
    path = root / f"{wf_id}.json"
    if not path.exists():
        print(f"FAIL: missing {path}", file=sys.stderr)
        sys.exit(1)
    data = json.load(open(path))
    agents = len(data.get("agents", []))
    if agents < 8:
        print(f"FAIL: {wf_id} has only {agents} actions", file=sys.stderr)
        sys.exit(1)
    payload = Path(f"scripts/payloads/{wf_id}.json")
    test = Path(f"scripts/test-{wf_id}.sh")
    for p in (payload, test):
        if not p.exists():
            print(f"FAIL: missing {p}", file=sys.stderr)
            sys.exit(1)

print(f"PASS: all {len(generated)} generated workflows have >={8} actions, payloads, and test scripts")
PY

[[ -f "$PROJECT_ROOT/docs/README.md" ]] || fail "missing docs/README.md"
pass "Diátaxis docs present"

diagram_count=$(find "$PROJECT_ROOT/docs/diagrams" -name '*.drawio' | wc -l | tr -d ' ')
[[ "$diagram_count" -ge 5 ]] || fail "expected >= 5 draw.io diagrams"
pass "$diagram_count draw.io source files"

echo ""
echo "Library validation complete."
