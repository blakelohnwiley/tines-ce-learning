#!/usr/bin/env bash
# Print CE flow budget and local catalog status.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CATALOG="$PROJECT_ROOT/exports/catalog.yaml"

echo "Tines CE flow budget"
echo "===================="

if [[ -f "$CATALOG" ]]; then
  grep -E 'max_active_flows|used_flows|remaining_flows' "$CATALOG" | sed 's/^/  /'
  echo ""
  echo "Catalogued workflows:"
  grep -E '^\s+- id:|^\s+name:|^\s+status:|^\s+file:' "$CATALOG" | sed 's/^/  /'
else
  echo "  No catalog at exports/catalog.yaml"
fi

echo ""
echo "JSON exports on disk:"
if compgen -G "$PROJECT_ROOT/exports/workflows/*.json" >/dev/null; then
  ls -1 "$PROJECT_ROOT/exports/workflows/"*.json | sed "s|$PROJECT_ROOT/|  |"
else
  echo "  (none yet — export stories from Tines UI to exports/workflows/)"
fi

echo ""
echo "Swap pattern: Export → Disable/Archive in tenant → Import next JSON"
echo "Docs: notes/05-workflow-catalog-and-ce-strategy.md"
