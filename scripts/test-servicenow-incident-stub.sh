#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "$SCRIPT_DIR/send-test-webhook-env.sh" WEBHOOK_URL_SERVICENOW_INCIDENT_STUB "$SCRIPT_DIR/payloads/servicenow-incident-stub.json"
