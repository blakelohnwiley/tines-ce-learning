#!/usr/bin/env bash
# Send low- and high-severity test payloads to exercise both branches
# of the alert triage workflow (see notes/03-alert-triage-workflow.md).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== Branch test 1: low severity → log_alert ==="
PAYLOAD_FILE="$SCRIPT_DIR/sample-payload.json" "$SCRIPT_DIR/send-test-webhook.sh"
echo ""

echo "=== Branch test 2: high severity → escalate_alert ==="
PAYLOAD_FILE="$SCRIPT_DIR/payload-high-severity.json" "$SCRIPT_DIR/send-test-webhook.sh"
echo ""

echo "Done. Open Story Runs and confirm each run took the expected branch."
