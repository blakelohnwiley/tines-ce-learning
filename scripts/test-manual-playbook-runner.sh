#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "$SCRIPT_DIR/send-test-webhook-env.sh" WEBHOOK_URL_MANUAL_PLAYBOOK_RUNNER "$SCRIPT_DIR/payloads/manual-playbook-runner.json"
