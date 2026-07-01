# Tutorial: Getting started with Tines CE workflows

**Audience:** Developers new to Tines Community Edition who want a successful first end-to-end run.

**Goal:** Sign up, build a branching alert-triage story, test it from your machine, and understand where exports fit in.

**Time:** About 2–3 hours if you follow Tines University alongside this repo.

---

## What you will accomplish

By the end of this tutorial you will:

1. Have a CE tenant and local workspace configured.
2. Run a webhook-triggered story that branches on severity.
3. Post test payloads from your terminal and inspect Story Runs.
4. Know where to find exported JSON and the CE flow budget.

---

## Step 1 — Create your tenant

1. Sign up at [login.tines.com](https://login.tines.com/saml_idp/signup) (free, no credit card).
2. Complete the in-product first-login tutorial.
3. Record your tenant URL in [`SETUP.md`](../../SETUP.md) and copy [`.env.example`](../../.env.example) to `.env`.

---

## Step 2 — Learn the UI

Work through [`notes/01-foundations.md`](../../notes/01-foundations.md) while taking [Tines University Foundations](https://www.tines.com/university/tines-foundations/).

You need to be comfortable with:

- Stories and the storyboard
- Webhook, Event Transform, and Condition actions
- Story Runs and event inspection

---

## Step 3 — Build the base alert triage story

Follow [`notes/03-alert-triage-workflow.md`](../../notes/03-alert-triage-workflow.md).

The pipeline looks like this:

![Alert triage base flow](../diagrams/alert-triage-base.drawio.png)

1. Rename the webhook to `receive_alert`.
2. Add `normalize_alert` (Event Transform).
3. Add `check_severity` (Condition: high or critical).
4. Branch to `escalate_alert` or `log_alert`.

This story uses **one active flow**.

---

## Step 4 — Test from your machine

```bash
cp .env.example .env   # add WEBHOOK_URL from the Tines UI
./scripts/send-test-webhook.sh
./scripts/test-both-branches.sh
```

Open **Story Runs** in Tines and confirm both branches execute.

---

## Step 5 — Export your work

1. Deselect all actions on the storyboard.
2. **⋯ → Export story** → save to `exports/workflows/alert-triage.json`.
3. Update [`exports/catalog.yaml`](../../exports/catalog.yaml) if metadata changed.

See [How-to: Export and import stories](../how-to/export-import-stories.md) for the full procedure.

---

## Step 6 — Check your flow budget

```bash
./scripts/ce-flow-status.sh
```

Community Edition allows **three active flows**. You will use two if you also build the advanced story ([`notes/04-alert-triage-advanced.md`](../../notes/04-alert-triage-advanced.md)).

Read [Explanation: CE operating model](../explanation/ce-operating-model.md) to understand why exports matter even when you hit the flow cap.

---

## Next steps

| If you want to… | Read |
|---|---|
| Add nested routing and HTTP enrichment | [`notes/04-alert-triage-advanced.md`](../../notes/04-alert-triage-advanced.md) |
| Build many workflows on CE | [Explanation: CE operating model](../explanation/ce-operating-model.md) |
| Swap which stories are live | [How-to: Swap workflows on CE](../how-to/swap-workflows-on-ce.md) |
| Look up every export and test script | [Reference: Workflow catalog](../reference/workflow-catalog.md) |
