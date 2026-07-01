#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "$SCRIPT_DIR/send-test-webhook-env.sh" WEBHOOK_URL_RANSOMWARE_RESPONSE "$SCRIPT_DIR/payloads/ransomware-response.json"
