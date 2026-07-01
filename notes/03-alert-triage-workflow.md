# Alert Triage Workflow

Expand **Your first story** into a branching pipeline that normalizes inbound alerts and routes by severity.

**Flow diagram:**

```
receive_alert (Webhook)
       │
       ▼
normalize_alert (Event Transform)
       │
       ▼
check_severity (Condition)
       ├── severity is high/critical ──► escalate_alert (Event Transform)
       └── else ──────────────────────► log_alert (Event Transform)
```

Still **1 active flow** (one webhook trigger path with branches).

---

## Step 1 — Rename Webhook

1. Select the **Webhook** action
2. Name: `receive_alert`

---

## Step 2 — Add `normalize_alert` (Event Transform)

1. Toolbar → **Event Transform** → place to the right of the webhook
2. Name: `normalize_alert`
3. Connect: `receive_alert` output → `normalize_alert` input
4. Output payload:

```json
{
  "alert_id": "<<WEBHOOK.body.alert>>-<<WEBHOOK.id>>",
  "severity": "<<WEBHOOK.body.severity>>",
  "source": "<<WEBHOOK.body.source>>",
  "received_at": "<<WEBHOOK.date>>",
  "note": "<<WEBHOOK.body.note>>",
  "normalized": true
}
```

> Tines uppercases action names in liquid paths. Your webhook is still named **Webhook**, so use `<<WEBHOOK.body.alert>>`, `<<WEBHOOK.body.severity>>`, etc. After renaming to `receive_alert`, use `<<RECEIVE_ALERT...>>`.

---

## Step 3 — Add `check_severity` (Condition)

1. Toolbar → **Condition** → place after `normalize_alert`
2. Name: `check_severity`
3. Connect: `normalize_alert` → `check_severity`
4. Rule (match **any**):

| Field | Operator | Value |
|---|---|---|
| `<<normalize_alert.severity>>` | equals | `high` |
| `<<normalize_alert.severity>>` | equals | `critical` |

Or use a single expression if your UI supports it:

```
<<normalize_alert.severity>> == "high" or <<normalize_alert.severity>> == "critical"
```

---

## Step 4 — High path: `escalate_alert`

1. Add **Event Transform** on the **true / match** output of the condition
2. Name: `escalate_alert`
3. Output:

```json
{
  "action": "escalate",
  "priority": "P1",
  "alert_id": "<<normalize_alert.alert_id>>",
  "severity": "<<normalize_alert.severity>>",
  "source": "<<normalize_alert.source>>",
  "message": "High-severity alert from <<normalize_alert.source>> requires review",
  "escalated_at": "<<normalize_alert.received_at>>"
}
```

---

## Step 5 — Low path: `log_alert`

1. Add **Event Transform** on the **false / no match** output of the condition
2. Name: `log_alert`
3. Output:

```json
{
  "action": "log",
  "priority": "P4",
  "alert_id": "<<normalize_alert.alert_id>>",
  "severity": "<<normalize_alert.severity>>",
  "source": "<<normalize_alert.source>>",
  "message": "Alert logged for audit",
  "logged_at": "<<normalize_alert.received_at>>"
}
```

---

## Step 6 — Test both branches

### Low severity (→ log path)

```bash
./scripts/send-test-webhook.sh
# default sample-payload.json: severity "low"
```

Expect Story Run: `normalize_alert` → `check_severity` → **`log_alert`**

### High severity (→ escalate path)

```bash
PAYLOAD_FILE=scripts/payload-high-severity.json ./scripts/send-test-webhook.sh
```

Expect Story Run: `normalize_alert` → `check_severity` → **`escalate_alert`**

---

## Step 7 — Publish (when ready)

Click **Publish** so the webhook keeps working when you're not on the storyboard.

---

## Optional extension — HTTP enrichment

After `escalate_alert`, add **HTTP Request**:

- Method: `POST`
- URL: `https://httpbin.org/post`
- Body: `{"escalation": <<escalate_alert>>}`

No credentials needed; httpbin echoes the payload back into Story Runs.

---

## Verification checklist

- [x] Webhook renamed to `receive_alert`
- [x] `normalize_alert` connected and outputs `normalized: true`
- [x] Low-severity test reaches `log_alert` with `action: "log"`
- [x] High-severity test reaches `escalate_alert` with `action: "escalate"`
- [ ] Story published (optional but recommended)
- [ ] Exported to `exports/alert-triage.json`
