#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "=== US IP (expect allow) ==="
"$SCRIPT_DIR/send-test-webhook-env.sh" WEBHOOK_URL_GEO_BLOCK "$SCRIPT_DIR/payloads/geo-block-us.json"
echo ""
echo "=== RU IP (expect block) ==="
"$SCRIPT_DIR/send-test-webhook-env.sh" WEBHOOK_URL_GEO_BLOCK "$SCRIPT_DIR/payloads/geo-block-ru.json"
