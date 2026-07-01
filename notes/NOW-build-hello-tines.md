# Build Hello Tines Now (you're logged in)

Follow these steps in your Tines tenant. Takes ~10 minutes.

## Before you start

- CE limit: **3 active flows** total. If the tutorial left stories running, that's fine — this adds 1 flow.
- Keep this doc open beside Tines.

---

## Step 1 — New story

1. In the left nav, click **Stories**
2. Click **+ New story** (or **Create story**)
3. Name: `Hello Tines`
4. Open the story on the storyboard

---

## Step 2 — Webhook trigger

1. On the storyboard, click **+** → add **Webhook**
2. Rename the action: `receive_alert`
3. In the action panel, find **Webhook URL** — copy the **full URL** (includes secret path)
4. Save/note it — you'll paste into `.env` as `WEBHOOK_URL`

---

## Step 3 — Event Transform

1. Add **Event Transform** to the right of the webhook
2. Name: `format_output`
3. Drag/connect: `receive_alert` output → `format_output` input
4. Set output to something like:

```json
{
  "message": "Alert from <<receive_alert.body.source>>",
  "alert": "<<receive_alert.body.alert>>",
  "severity": "<<receive_alert.body.severity>>",
  "processed": true
}
```

> If fields are empty in Story Runs, click the webhook event and check the actual JSON shape — adjust `body.` paths accordingly.

---

## Step 4 — Test in Tines

1. Select the **Webhook** action
2. Use **Run test** / **Send test event**
3. Payload:

```json
{
  "alert": "test",
  "severity": "low",
  "source": "tines-ui"
}
```

4. Open **Story Runs** (history icon)
5. Confirm `format_output` shows `"processed": true`

---

## Step 5 — Local webhook test

In terminal:

```bash
cd /Users/blakelohn-wiley/dev/tines
cp .env.example .env   # skip if .env exists
# Edit .env: set TENANT_URL and WEBHOOK_URL
./scripts/send-test-webhook.sh
```

Check Story Runs again for `"source": "local-script"`.

---

## Step 6 — Export backup

1. Deselect all actions on the storyboard
2. Top-right menu → **Export story**
3. Save to: `exports/hello-tines.json`

---

## Next after Hello Tines

1. [Story Library import](../templates/story-library-starter.md) — pick the AI chatbot template (no extra credentials)
2. [Tines University Foundations](https://www.tines.com/university/tines-foundations/) — work through modules with [01-foundations.md](01-foundations.md)

---

## Checklist

- [ ] Story `Hello Tines` created
- [ ] Webhook URL copied to `.env`
- [ ] In-app test passed
- [ ] `./scripts/send-test-webhook.sh` succeeded
- [ ] Exported to `exports/hello-tines.json`
