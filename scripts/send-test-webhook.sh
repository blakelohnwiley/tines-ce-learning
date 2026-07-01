#!/usr/bin/env bash
# POST a test event to your Tines webhook.
# Requires .env with WEBHOOK_URL set (copy from .env.example).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

if [[ -f "$PROJECT_ROOT/.env" ]]; then
  # shellcheck disable=SC1091
  source "$PROJECT_ROOT/.env"
fi

WEBHOOK_URL="${WEBHOOK_URL:-}"
PAYLOAD_FILE="${PAYLOAD_FILE:-$SCRIPT_DIR/sample-payload.json}"

if [[ -z "$WEBHOOK_URL" ]]; then
  echo "Error: WEBHOOK_URL is not set." >&2
  echo "Copy .env.example to .env and add your webhook URL from the Tines Webhook action." >&2
  exit 1
fi

if [[ ! -f "$PAYLOAD_FILE" ]]; then
  echo "Error: Payload file not found: $PAYLOAD_FILE" >&2
  exit 1
fi

echo "POSTing to Tines webhook..."
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
  echo "Success. Check Story Runs in your Tines tenant for the new execution."
  exit 0
fi

echo "Request failed. Verify WEBHOOK_URL includes the correct path and secret." >&2
exit 1
