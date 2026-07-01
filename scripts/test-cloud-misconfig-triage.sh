#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "$SCRIPT_DIR/send-test-webhook-env.sh" WEBHOOK_URL_CLOUD_MISCONFIG_TRIAGE "$SCRIPT_DIR/payloads/cloud-misconfig-triage.json"
