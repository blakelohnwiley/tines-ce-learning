#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "Delay + HTTP test (~5s delay before httpbin call). Check Story Runs for success/retry branches."
exec "$SCRIPT_DIR/send-test-webhook-env.sh" WEBHOOK_URL_DELAY_RETRY "$SCRIPT_DIR/payloads/delay-retry.json"
