#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "$SCRIPT_DIR/send-test-webhook-env.sh" WEBHOOK_URL_AUTH_ANOMALY_DETECTOR "$SCRIPT_DIR/payloads/auth-anomaly-detector.json"
