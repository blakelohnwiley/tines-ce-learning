# Alert Triage Advanced

Duplicate of the alert triage pipeline with extra routing, HTTP enrichment, and tiered escalation.

## Flow

```
receive_alert (Webhook)
    → normalize_alert (Event Transform)
    → check_severity (Condition: high OR critical)
           ├─ MATCH ──► check_critical (Condition: critical only?)
           │                 ├─ MATCH ──► critical_escalate (P0)
           │                 └─ NO MATCH ► escalate_alert (P1)
           │                      └─► enrich_escalation (HTTP POST httpbin.org/post)
           └─ NO MATCH ► check_source (Condition: source contains firewall)
                              ├─ MATCH ──► firewall_log (enhanced log)
                              └─ NO MATCH ► log_alert (standard P4 log)
```

Uses **2 of 3** CE active flows (original + this story).

---

## Extensions vs base workflow

| Feature | Base story | Advanced story |
|---|---|---|
| Severity branch | high/critical → escalate | critical → P0, high → P1 + HTTP enrich |
| Low path | single log | firewall vs generic log |
| HTTP enrichment | none | httpbin echo after escalation |
| Priority tiers | P1 / P4 | P0 / P1 / P4 / firewall-audit |

---

## Test payloads

```bash
# Standard low → log_alert or firewall_log
./scripts/send-test-webhook-advanced.sh low

# High → escalate_alert → enrich_escalation
./scripts/send-test-webhook-advanced.sh high

# Critical → critical_escalate → enrich_escalation
./scripts/send-test-webhook-advanced.sh critical

# Firewall source on low path → firewall_log
./scripts/send-test-webhook-advanced.sh firewall
```

---

## Verification

- [x] Story duplicated and renamed **Alert Triage Advanced** (story 121679)
- [x] All actions connected; 11 actions total
- [x] Four test payloads each return HTTP 201
- [ ] Confirm terminal actions in Story Runs (log_alert, escalate+enrich, critical+enrich, firewall_log)
- [ ] Exported to `exports/alert-triage-advanced.json`
