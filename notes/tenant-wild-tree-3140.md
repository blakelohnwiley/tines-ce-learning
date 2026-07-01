# Tenant: wild-tree-3140

| Item | Value |
|---|---|
| Tenant | https://wild-tree-3140.tines.com |
| Stories list | https://wild-tree-3140.tines.com/stories |
| Current story | https://wild-tree-3140.tines.com/stories/121670 |

## Get webhook URL from story 121670

1. Open the story link above (must be logged in).
2. Click the **Webhook** action on the storyboard.
3. In the action panel, copy the full **Webhook URL** (includes secret path).
4. ~~Add to `.env`~~ — configured; local test returned **HTTP 201** `{"status":"ok"}`

## Alert triage pipeline (built 2026-07-01)

Story 121670 expanded via Workbench:

`receive_alert` → `normalize_alert` → `check_severity` → `escalate_alert` | `log_alert`

## Imported complex batch (2026-07-01)

Twenty generated workflows imported via UI; all **disabled** to keep CE at 2/3 active flows:

- Active: **121670** (Your first story), **121679** (Alert Triage Advanced)
- Imported disabled pool: **121699–121719** (see `exports/catalog.yaml`)

To test one: enable story → copy webhook URL → update `.env` → run `scripts/test-<id>.sh`.

## Alert Triage Advanced (built 2026-07-01)

Story 121679 — duplicate + extended (11 actions):

`receive_alert` → `normalize_alert` → `check_severity` → `check_critical` → `critical_escalate` → `enrich_critical` | `escalate_alert` → `enrich_high` | `check_source` → `firewall_log` | `log_alert`

Webhook: `/webhook/alert-triage-advanced/...` — set `WEBHOOK_URL_ADVANCED` in `.env`

```bash
./scripts/test-advanced-branches.sh
```

If this story has no Webhook yet, add one per [NOW-build-hello-tines.md](NOW-build-hello-tines.md).
