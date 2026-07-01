#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "=== Clean URL (expect allow branch) ==="
"$SCRIPT_DIR/send-test-webhook-env.sh" WEBHOOK_URL_URL_REPUTATION "$SCRIPT_DIR/payloads/url-clean.json"
echo ""
echo "=== Suspicious URL (expect block branch) ==="
"$SCRIPT_DIR/send-test-webhook-env.sh" WEBHOOK_URL_URL_REPUTATION "$SCRIPT_DIR/payloads/url-malicious.json"
