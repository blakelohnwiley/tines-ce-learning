#!/usr/bin/env bash
# POST a test event using a named webhook env var from .env
# Usage: send-test-webhook-env.sh WEBHOOK_URL_IP_ENRICHMENT scripts/payloads/ip-enrichment.json

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

ENV_VAR="${1:-}"
PAYLOAD_FILE="${2:-$SCRIPT_DIR/sample-payload.json}"

if [[ -z "$ENV_VAR" ]]; then
  echo "Usage: $0 <ENV_VAR_NAME> [payload.json]" >&2
  exit 1
fi

if [[ -f "$PROJECT_ROOT/.env" ]]; then
  # shellcheck disable=SC1091
  source "$PROJECT_ROOT/.env"
fi

WEBHOOK_URL="${!ENV_VAR:-}"

if [[ -z "$WEBHOOK_URL" ]]; then
  echo "Error: $ENV_VAR is not set in .env" >&2
  echo "Enable the story in Tines, copy the webhook URL, and add to .env" >&2
  exit 1
fi

if [[ ! -f "$PAYLOAD_FILE" ]]; then
  echo "Error: Payload file not found: $PAYLOAD_FILE" >&2
  exit 1
fi

echo "POSTing to Tines webhook ($ENV_VAR)..."
echo "Payload: $PAYLOAD_FILE"
echo ""

HTTP_CODE=$(curl -sS -w "%{http_code}" -o /tmp/tines-webhook-response.txt \
  -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d @"$PAYLOAD_FILE")

echo "HTTP status: $HTTP_CODE"
echo "Response body:"
cat /tmp/tines-webhook-response.txt
echo ""

if [[ "$HTTP_CODE" -ge 200 && "$HTTP_CODE" -lt 300 ]]; then
  echo "Success. Check Story Runs in your Tines tenant."
  exit 0
fi

echo "Request failed. Verify webhook URL in .env." >&2
exit 1
