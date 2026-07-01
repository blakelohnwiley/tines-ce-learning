# Explanation: Alert triage pipelines

**Question:** How do the base and advanced alert triage stories differ, and why were they built this way?

Both stories are learning exercises in SOAR-style **normalize → decide → act** patterns using Tines core actions (Webhook, Event Transform, Condition, HTTP Request).

---

## Base pipeline

![Alert triage base](../diagrams/alert-triage-base.drawio.png)

| Stage | Action | Purpose |
|---|---|---|
| Ingest | `receive_alert` (Webhook) | Accept JSON alert from any sender |
| Normalize | `normalize_alert` (Event Transform) | Stable fields: `alert_id`, `severity`, `source`, timestamps |
| Decide | `check_severity` (Condition) | Match `high` or `critical` |
| Act (high) | `escalate_alert` | Mark for escalation (P1-style payload) |
| Act (low) | `log_alert` | Record-only path (P4-style payload) |

**Flows:** 1 — single trigger with branching, not multiple disconnected chains.

**Teaches:** Liquid templating, Condition rules, branch inspection in Story Runs.

Walkthrough: [`notes/03-alert-triage-workflow.md`](../../notes/03-alert-triage-workflow.md).

---

## Advanced pipeline

![Alert triage advanced](../diagrams/alert-triage-advanced.drawio.png)

Extends the base story with **nested decisions** and **HTTP enrichment**:

| Extension | Behavior |
|---|---|
| `check_critical` | Splits high vs critical on the match path |
| `critical_escalate` / `escalate_alert` | P0 vs P1 priority tiers |
| `enrich_critical` / `enrich_high` | HTTP POST to httpbin (stand-in for a real enrichment API) |
| `check_source` | On the non-severity path, detect firewall-sourced alerts |
| `firewall_log` vs `log_alert` | Audit-style log vs standard low-priority log |

**Actions:** 11 total. **Flows:** still 1 per story.

**Teaches:** Multi-level routing, HTTP Request action, testing four distinct terminal outcomes.

Walkthrough: [`notes/04-alert-triage-advanced.md`](../../notes/04-alert-triage-advanced.md).

---

## Comparison

| Feature | Base | Advanced |
|---|---|---|
| Severity routing | Single condition | Critical vs high split |
| Low-severity path | One log action | Firewall vs generic log |
| HTTP enrichment | None | After escalation paths |
| Priority labels | P1 / P4 | P0 / P1 / P4 / firewall-audit |
| Test paths | 2 | 4 |

---

## Testing matrix

| Payload profile | Expected terminal |
|---|---|
| Low severity, generic source | `log_alert` |
| Low severity, firewall source | `firewall_log` |
| High severity | `escalate_alert` → HTTP enrich |
| Critical severity | `critical_escalate` → HTTP enrich |

```bash
./scripts/test-advanced-branches.sh
```

---

## Design notes

- **httpbin** avoids credentials while demonstrating outbound HTTP and response inspection.
- **Duplicate story** (separate webhook path) keeps base and advanced independently testable and each counting as one flow — preferable to one mega-story for learning.
- Export both JSON files so either pipeline can be re-imported after tenant changes.

---

## Related

- [Tutorial: Getting started](../tutorials/getting-started.md)
- [How-to: Test webhooks locally](../how-to/test-webhooks-locally.md)
- [Reference: Workflow catalog](../reference/workflow-catalog.md)
