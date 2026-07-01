#!/usr/bin/env bash
# POST test events to the Alert Triage Advanced story webhook.
# Usage: ./send-test-webhook-advanced.sh [low|high|critical|firewall]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

if [[ -f "$PROJECT_ROOT/.env" ]]; then
  # shellcheck disable=SC1091
  source "$PROJECT_ROOT/.env"
fi

WEBHOOK_URL="${WEBHOOK_URL_ADVANCED:-${WEBHOOK_URL:-}}"
SCENARIO="${1:-low}"

case "$SCENARIO" in
  low)       PAYLOAD_FILE="$SCRIPT_DIR/sample-payload.json" ;;
  high)      PAYLOAD_FILE="$SCRIPT_DIR/payload-high-severity.json" ;;
  critical)  PAYLOAD_FILE="$SCRIPT_DIR/payload-critical-severity.json" ;;
  firewall)  PAYLOAD_FILE="$SCRIPT_DIR/payload-firewall-low.json" ;;
  *)
    echo "Usage: $0 [low|high|critical|firewall]" >&2
    exit 1
    ;;
esac

if [[ -z "$WEBHOOK_URL" ]]; then
  echo "Error: WEBHOOK_URL_ADVANCED (or WEBHOOK_URL) is not set in .env" >&2
  exit 1
fi

export WEBHOOK_URL PAYLOAD_FILE
echo "Scenario: $SCENARIO"
exec "$SCRIPT_DIR/send-test-webhook.sh"
