#!/usr/bin/env bash
# Exercise all four branches of Alert Triage Advanced.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

for scenario in low high critical firewall; do
  echo "=== $scenario ==="
  "$SCRIPT_DIR/send-test-webhook-advanced.sh" "$scenario"
  echo ""
done

echo "Done. Check Story Runs on Alert Triage Advanced for each branch."
