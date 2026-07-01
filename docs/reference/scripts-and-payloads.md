# Reference: Scripts and payloads

Local shell scripts for posting test events to Tines webhooks. All scripts expect `.env` in the repo root (gitignored).

---

## Utility scripts

| Script | Purpose |
|---|---|
| `scripts/ce-flow-status.sh` | Print CE flow budget from `exports/catalog.yaml` |
| `scripts/send-test-webhook.sh` | POST default payload to `WEBHOOK_URL` |
| `scripts/send-test-webhook-advanced.sh` | POST named payload to `WEBHOOK_URL_ADVANCED` |
| `scripts/send-test-webhook-env.sh` | POST using arbitrary `webhook_env` from catalog |

---

## Branch test suites

| Script | Story |
|---|---|
| `scripts/test-both-branches.sh` | Base alert triage (high + low) |
| `scripts/test-advanced-branches.sh` | Advanced (low, high, critical, firewall) |

---

## Per-workflow tests (exported-only)

| Script | Payload directory |
|---|---|
| `scripts/test-ip-enrichment.sh` | `scripts/payloads/ip-enrichment.json` |
| `scripts/test-url-reputation.sh` | `scripts/payloads/url-clean.json`, `url-malicious.json` |
| `scripts/test-dedup-alerts.sh` | `scripts/payloads/dedup-alert.json` |
| `scripts/test-throttle-demo.sh` | `scripts/payloads/throttle-burst.json` |
| `scripts/test-delay-retry.sh` | `scripts/payloads/delay-retry.json` |
| `scripts/test-geo-block-gate.sh` | `scripts/payloads/geo-block-us.json`, `geo-block-ru.json` |

Advanced story one-offs in `scripts/`: `payload-high-severity.json`, `payload-critical-severity.json`, `payload-firewall-low.json`, `sample-payload.json`.

---

## Environment variables

See [`.env.example`](../../.env.example). Never commit `.env`.

---

## Related

- [How-to: Test webhooks locally](../how-to/test-webhooks-locally.md)
- [Reference: Workflow catalog](workflow-catalog.md)
