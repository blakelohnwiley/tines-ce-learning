# How-to: Test webhooks from your local machine

**Problem:** You want to send test payloads to a Tines webhook and confirm the correct branch runs.

**Prerequisite:** `.env` contains the webhook URL for the story under test.

---

## Setup

```bash
cp .env.example .env
```

Set variables from the Webhook action in Tines. Active stories in this repo use:

| Story | `.env` variable |
|---|---|
| Alert triage (base) | `WEBHOOK_URL` |
| Alert triage (advanced) | `WEBHOOK_URL_ADVANCED` |

Exported-only workflows have their own `WEBHOOK_URL_*` names in [`exports/catalog.yaml`](../../exports/catalog.yaml).

---

## Base alert triage

```bash
./scripts/send-test-webhook.sh          # default low-severity payload
./scripts/test-both-branches.sh       # high + low paths
```

Payload files live in `scripts/` (`payload-high-severity.json`, etc.).

---

## Advanced alert triage

```bash
./scripts/test-advanced-branches.sh
```

Or individual payloads:

```bash
./scripts/send-test-webhook-advanced.sh low
./scripts/send-test-webhook-advanced.sh high
./scripts/send-test-webhook-advanced.sh critical
./scripts/send-test-webhook-advanced.sh firewall
```

Expected terminal actions: `log_alert`, `escalate_alert` + enrich, `critical_escalate` + enrich, or `firewall_log`. Confirm in **Story Runs**.

---

## Exported-only and generated workflows

Standard exports and the 20 complex generated workflows each have `scripts/test-<id>.sh` and `scripts/payloads/<id>.json`:

```bash
./scripts/test-ip-enrichment.sh
./scripts/test-phishing-analyzer.sh   # complex generated example
```

Full index: [Reference: Workflow catalog](../reference/workflow-catalog.md).

Validate the library: `./scripts/validate-workflow-library.sh`

---

## Troubleshooting

| Symptom | Check |
|---|---|
| HTTP 404 | Webhook path or story disabled |
| Wrong branch | Payload severity/source fields; Condition rules in Tines |
| No runs | Story not published; flow slot not active |

```bash
./scripts/ce-flow-status.sh
```

---

## Related

- [Reference: Scripts and payloads](../reference/scripts-and-payloads.md)
- [Explanation: Alert triage pipelines](../explanation/alert-triage-pipelines.md)
