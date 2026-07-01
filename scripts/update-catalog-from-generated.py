#!/usr/bin/env python3
"""Merge exports/generated-workflows.json into exports/catalog.yaml."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "exports" / "catalog.yaml"
MANIFEST = ROOT / "exports" / "generated-workflows.json"

HEADER = """# Local workflow library index
# Update when you export/import stories. Do not commit secrets.

"""

EXISTING_ACTIVE = """
  - id: alert-triage
    name: Your first story
    file: workflows/alert-triage.json
    tenant_story_id: 121670
    flows: 1
    webhook_env: WEBHOOK_URL
    webhook_path: your-first-story
    test_script: scripts/test-both-branches.sh
    status: active
    complexity: standard

  - id: alert-triage-advanced
    name: Alert Triage Advanced
    file: workflows/alert-triage-advanced.json
    tenant_story_id: 121679
    flows: 1
    webhook_env: WEBHOOK_URL_ADVANCED
    webhook_path: alert-triage-advanced
    test_script: scripts/test-advanced-branches.sh
    status: active
    complexity: complex
    actions: 11

  - id: scheduled-heartbeat
    name: Scheduled Heartbeat
    file: workflows/scheduled-heartbeat.json
    tenant_story_id: 121683
    flows: 1
    webhook_env: null
    trigger: schedule
    schedule: "*/15 * * * *"
    notes: "Schedule trigger via cron; re-import and enable to run."
    status: exported-only
    complexity: standard

  - id: ip-enrichment
    name: IP Enrichment
    file: workflows/ip-enrichment.json
    tenant_story_id: 121684
    flows: 1
    webhook_env: WEBHOOK_URL_IP_ENRICHMENT
    webhook_path: ip-enrichment
    test_script: scripts/test-ip-enrichment.sh
    status: exported-only
    complexity: standard

  - id: url-reputation-check
    name: URL Reputation Check
    file: workflows/url-reputation-check.json
    tenant_story_id: 121686
    flows: 1
    webhook_env: WEBHOOK_URL_URL_REPUTATION
    webhook_path: url-reputation-check
    test_script: scripts/test-url-reputation.sh
    status: exported-only
    complexity: standard

  - id: dedup-alerts
    name: Dedup Alerts
    file: workflows/dedup-alerts.json
    tenant_story_id: 121688
    flows: 1
    webhook_env: WEBHOOK_URL_DEDUP_ALERTS
    webhook_path: dedup-alerts
    test_script: scripts/test-dedup-alerts.sh
    status: exported-only
    complexity: standard

  - id: throttle-demo
    name: Throttle Demo
    file: workflows/throttle-demo.json
    tenant_story_id: 121689
    flows: 1
    webhook_env: WEBHOOK_URL_THROTTLE_DEMO
    webhook_path: throttle-demo
    test_script: scripts/test-throttle-demo.sh
    status: exported-only
    complexity: standard

  - id: delay-retry
    name: Delay Retry
    file: workflows/delay-retry.json
    tenant_story_id: 121690
    flows: 1
    webhook_env: WEBHOOK_URL_DELAY_RETRY
    webhook_path: delay-retry
    test_script: scripts/test-delay-retry.sh
    status: exported-only
    complexity: standard

  - id: geo-block-gate
    name: Geo Block Gate
    file: workflows/geo-block-gate.json
    tenant_story_id: 121691
    flows: 1
    webhook_env: WEBHOOK_URL_GEO_BLOCK
    webhook_path: geo-block-gate
    test_script: scripts/test-geo-block-gate.sh
    status: exported-only
    complexity: standard
"""

STORY_LIBRARY = """
story_library:
  - id: analyze-urls-fraud-abuse
    name: Analyze URLS for fraud and abuse
    file: story-library/analyze-urls-fraud-abuse.json
    tenant_story_id: 121692
    source: https://www.tines.com/library/stories/87699/
    flows: 1
    credentials: [Zendesk]
    status: exported-only
"""

FOOTER = """
library_stats:
  total_workflow_exports: 29
  complex_workflows: 21
  generated_complex_batch: 20
  standard_workflows: 8

ce_budget:
  max_active_flows: 3
  used_flows: 2
  remaining_flows: 1
  max_events_per_month: 25000
  tenant: https://wild-tree-3140.tines.com
"""


def main() -> None:
    entries = json.loads(MANIFEST.read_text())
    generated_block = ""
    for e in entries:
        wid = e["id"]
        generated_block += f"""
  - id: {wid}
    name: {e['name']}
    file: {e['file']}
    tenant_story_id: null
    flows: 1
    webhook_env: {e['env']}
    webhook_path: {wid}
    test_script: scripts/test-{wid}.sh
    status: generated-only
    complexity: complex
    actions: {e['actions']}
    notes: "Generated JSON — import to tenant to run; not yet live in CE."
"""

    content = (
        HEADER
        + "workflows:"
        + EXISTING_ACTIVE
        + generated_block
        + STORY_LIBRARY
        + FOOTER
    )
    CATALOG.write_text(content)
    print(f"Updated {CATALOG} with {len(entries)} generated workflows")


if __name__ == "__main__":
    main()
