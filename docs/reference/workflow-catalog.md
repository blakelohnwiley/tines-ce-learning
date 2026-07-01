# Reference: Workflow catalog

Index of exported stories in this repository. Update [`exports/catalog.yaml`](../../exports/catalog.yaml) when you add or change exports.

---

## Active in tenant

| ID | Name | Story ID | Webhook path | `.env` variable | Test script |
|---|---|---|---|---|---|
| `alert-triage` | Your first story | 121670 | `your-first-story` | `WEBHOOK_URL` | `scripts/test-both-branches.sh` |
| `alert-triage-advanced` | Alert Triage Advanced | 121679 | `alert-triage-advanced` | `WEBHOOK_URL_ADVANCED` | `scripts/test-advanced-branches.sh` |

JSON files: `exports/workflows/alert-triage.json`, `exports/workflows/alert-triage-advanced.json`.

---

## Exported only (swap in to run)

| ID | Trigger | Webhook path | Test script |
|---|---|---|---|
| `scheduled-heartbeat` | Schedule `*/15 * * * *` | — | — |
| `ip-enrichment` | Webhook | `ip-enrichment` | `scripts/test-ip-enrichment.sh` |
| `url-reputation-check` | Webhook | `url-reputation-check` | `scripts/test-url-reputation.sh` |
| `dedup-alerts` | Webhook | `dedup-alerts` | `scripts/test-dedup-alerts.sh` |
| `throttle-demo` | Webhook | `throttle-demo` | `scripts/test-throttle-demo.sh` |
| `delay-retry` | Webhook | `delay-retry` | `scripts/test-delay-retry.sh` |
| `geo-block-gate` | Webhook | `geo-block-gate` | `scripts/test-geo-block-gate.sh` |

---

## Story library import

| ID | Source | Credentials |
|---|---|---|
| `analyze-urls-fraud-abuse` | [Tines Library #87699](https://www.tines.com/library/stories/87699/) | Zendesk |

File: `exports/story-library/analyze-urls-fraud-abuse.json`.

---

## Planned (not yet built)

See [`exports/workflows/BUILD.md`](../../exports/workflows/BUILD.md) for Workbench prompts. Planned IDs in catalog: `email-to-ticket-stub`, `manual-run-playbook`, `multi-step-etl`, `case-record-stub`, `slack-alert-notify`, `servicenow-incident`, `ai-alert-summarizer`.

---

## Related

- [How-to: Swap workflows on CE](../how-to/swap-workflows-on-ce.md)
- [Reference: CE limits](ce-limits.md)
