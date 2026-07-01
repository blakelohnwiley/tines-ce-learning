#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "=== First event (should process) ==="
"$SCRIPT_DIR/send-test-webhook-env.sh" WEBHOOK_URL_DEDUP_ALERTS "$SCRIPT_DIR/payloads/dedup-alert.json"
echo ""
echo "=== Duplicate within 5 min (should dedupe) ==="
"$SCRIPT_DIR/send-test-webhook-env.sh" WEBHOOK_URL_DEDUP_ALERTS "$SCRIPT_DIR/payloads/dedup-alert.json"
