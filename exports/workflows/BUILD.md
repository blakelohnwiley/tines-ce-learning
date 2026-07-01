# Remaining catalog workflows — Workbench build prompts

Use the **3 live, ∞ in library** pattern: disable an active story → import JSON or build via prompt → test → export → disable.

Tenant: `https://wild-tree-3140.tines.com`

---

## Tier 1 — Core patterns

### email-to-ticket-stub

```
Build an email-to-ticket stub workflow. Rename story to "Email to Ticket Stub".

1. Email trigger named inbound_email (use default inbound email settings).
2. Event Transform named parse_email connected from inbound_email with output:
{
  "from": "<<inbound_email.from>>",
  "subject": "<<inbound_email.subject>>",
  "body_preview": "<<inbound_email.body>>",
  "received_at": "<<inbound_email.date>>"
}
3. Condition named is_urgent: MATCH if subject contains "urgent" OR "critical".
4. MATCH → Event Transform priority_ticket {"priority":"P1","subject":"<<parse_email.subject>>"}
5. NO MATCH → Event Transform normal_ticket {"priority":"P4","subject":"<<parse_email.subject>>"}

Connect and apply all changes.
```

### manual-run-playbook

```
Build a manual-run playbook workflow. Rename story to "Manual Run Playbook".

1. Manual trigger named run_playbook.
2. Event Transform named build_context with output:
{
  "operator": "manual",
  "started_at": "<<run_playbook.date>>",
  "note": "Manual test run"
}
3. HTTP Request named ping_httpbin: POST https://httpbin.org/post with JSON body from build_context.

Connect and apply all changes.
```

---

## Tier 2 — Integration stubs

### multi-step-etl

```
Build a multi-step ETL demo. Rename story to "Multi Step ETL".

1. Webhook named receive_batch with path multi-step-etl.
2. Event Transform named explode_items that outputs a list from receive_batch.body.items (use explode/implode pattern if available, else loop via standard lib).
3. Event Transform named normalize_item per item with id and value fields.
4. Event Transform named aggregate_results that collects normalized items.

Connect and apply all changes.
```

### case-record-stub

```
Build a case record stub. Rename story to "Case Record Stub".

1. Webhook named open_case with path case-record-stub.
2. Event Transform named format_case with output:
{
  "case_id": "CASE-<<open_case.body.incident_id>>",
  "title": "<<open_case.body.title>>",
  "status": "open",
  "opened_at": "<<open_case.date>>"
}
3. Page action named display_case showing format_case fields.

Connect and apply all changes.
```

---

## Tier 3 — SOAR-shaped (credentials required)

### slack-alert-notify

```
Build a Slack alert notification stub. Rename story to "Slack Alert Notify".

1. Webhook named receive_alert with path slack-alert-notify.
2. Event Transform named format_slack_message with markdown-friendly text from alert fields.
3. HTTP Request named post_slack using Slack incoming webhook URL placeholder in options (document credential needed).

Connect and apply. Note: requires Slack webhook credential.
```

### servicenow-incident

```
Build a ServiceNow incident stub. Rename story to "ServiceNow Incident".

1. Webhook named receive_incident with path servicenow-incident.
2. Event Transform named map_incident fields: short_description, urgency, category.
3. HTTP Request named create_incident POST to ServiceNow table API (placeholder URL; document credential).

Connect and apply. Note: requires ServiceNow credential.
```

---

## Tier 4 — AI / Workbench

### ai-alert-summarizer

```
Build an AI alert summarizer. Rename story to "AI Alert Summarizer".

1. Webhook named receive_alert with path ai-alert-summarizer.
2. AI Action named summarize_alert: summarize receive_alert.body into 2-3 sentences.
3. Event Transform named output_summary with summary, severity, alert_id.

Connect and apply. Uses CE AI credits.
```

---

## Import path (no build)

For Story Library templates not yet exported, use **Stories → New → Story library** in the tenant, search, import, export to `exports/story-library/`, then disable.

Recommended next imports:
- Write and improve AI prompts with an AI chatbot
- List EC2 instances in AWS (needs AWS cred)
- Report inactive Okta accounts (needs Okta cred)
