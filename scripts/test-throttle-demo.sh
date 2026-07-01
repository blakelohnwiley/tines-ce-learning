#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
for i in 1 2 3 4 5; do
  echo "=== Burst event $i ==="
  sed "s/\"sequence\": 1/\"sequence\": $i/" "$SCRIPT_DIR/payloads/throttle-burst.json" | \
    curl -sS -w "\nHTTP %{http_code}\n" -o /tmp/tines-throttle-response.txt \
      -X POST "$(grep -E '^WEBHOOK_URL_THROTTLE_DEMO=' "$SCRIPT_DIR/../.env" 2>/dev/null | cut -d= -f2-)" \
      -H "Content-Type: application/json" -d @- || true
  cat /tmp/tines-throttle-response.txt 2>/dev/null || true
  echo ""
done
