# First Story Walkthrough — Hello Tines

Build your first custom story: **Webhook → Event Transform**. Uses **1 flow** (CE limit: 3 total).

---

## Prerequisites

- Community Edition tenant created ([SETUP.md](../SETUP.md))
- First-login interactive tutorial completed

---

## Step 1 — Create the story

1. Log in to `https://<your-tenant>.tines.com`
2. Click **+ New story** (or **Create story**)
3. Name: `Hello Tines`
4. Open the story on the storyboard

---

## Step 2 — Add Webhook trigger

1. Click **+** on the storyboard → add **Webhook** action
2. Name it: `receive_alert`
3. In the action panel, note:
   - **Webhook URL** (full URL with secret)
   - **Secret** path segment
4. Default access: **Anyone with the secret** (fine for learning)

Copy the full webhook URL — you'll need it for `.env` and `scripts/send-test-webhook.sh`.

---

## Step 3 — Add Event Transform

1. Add **Event Transform** action to the right of the webhook
2. Name it: `format_output`
3. Connect: `receive_alert` → `format_output` (drag from output port to input)
4. Configure output mode to define a clean payload, e.g.:

```json
{
  "message": "Received alert from <<receive_alert.body.source>>",
  "alert": "<<receive_alert.body.alert>>",
  "severity": "<<receive_alert.body.severity>>",
  "processed": true
}
```

Adjust field paths to match your test payload (`body` is typical for webhook JSON).

---

## Step 4 — Test inside Tines

1. Select the **Webhook** action
2. Click **Run test** / **Send test event** (wording varies by UI version)
3. Use sample payload:

```json
{
  "alert": "test",
  "severity": "low",
  "source": "tines-ui"
}
```

4. Open **Story Runs** (clock/history icon)
5. Click the latest run → inspect events at `receive_alert` and `format_output`
6. Confirm `format_output` shows `"processed": true`

---

## Step 5 — Test from your machine

1. Copy `.env.example` → `.env`
2. Set `WEBHOOK_URL` to the full webhook URL from Step 2
3. Run:

```bash
cd /Users/blakelohn-wiley/dev/tines
./scripts/send-test-webhook.sh
```

4. Check **Story Runs** in Tines for a new run with `"source": "local-script"`

---

## Step 6 — Optional extension (Workflow B)

Add one more action for the **enrich** pattern (still 1 flow if linear):

1. After `format_output`, add **HTTP Request**
2. Method: `POST`
3. URL: `https://httpbin.org/post`
4. Content type: `application/json`
5. Payload:

```json
{
  "upstream": <<format_output>>,
  "echo": "enrichment step"
}
```

6. Run webhook test again — inspect httpbin response in Story Runs

**CE tip:** This optional HTTP step adds 1 event per run. Stay well under 25K/month for learning.

---

## Step 7 — Export backup

1. Story menu → **Export**
2. Save to `exports/hello-tines.json`

---

## Verification checklist

- [ ] Story `Hello Tines` created
- [ ] Webhook → Event Transform connected
- [ ] In-app test run succeeds
- [ ] Story Runs show expected JSON at each step
- [ ] Local `send-test-webhook.sh` triggers a new run
- [ ] Story exported to `exports/`

---

## Troubleshooting

| Symptom | Likely cause |
|---|---|
| Empty fields in transform | Wrong liquid path — check Story Runs for actual webhook event shape |
| 401/403 on webhook | Secret missing from URL or wrong path |
| Flow won't save | CE 3-flow limit — disable flows in other stories |
| httpbin timeout | Transient; retry or skip optional step |
