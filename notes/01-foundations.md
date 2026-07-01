# Tines Foundations — Learning Notes

Study alongside [Tines University: Foundations](https://www.tines.com/university/tines-foundations/). Each section maps to a University module (~30 min each).

---

## Module 1 — Platform overview

**Goal:** Understand what Tines is and how data moves between systems.

Tines is a **no-code intelligent workflow platform** used heavily in security (SOAR) but also for IT/Ops automation. You build **stories** on a visual canvas; data flows between **actions** as **events** (JSON).

### Why teams use it

- Connect any tool with an HTTP/API — no vendor-specific connectors required
- Visual builder — no Python/SPL scripting for basic automations
- Audit trail via Story Runs — see every event payload at each step

### Community Edition (your tier)

| Limit | Value |
|---|---|
| Builders | 1 |
| Active flows | 3 |
| Events/month | 25,000 |
| Teams | 1 |

**Notes from my session:**

- [ ] Completed Foundations intro
- Key takeaway:

---

## Module 2 — Core UI navigation

**Goal:** Navigate the tenant, teams, and story editor.

### Main areas

| Area | Purpose |
|---|---|
| **Home / Stories list** | All stories in your team |
| **Storyboard** | Canvas where you place and connect actions |
| **Editor panel** | Configure the selected action |
| **Properties panel** | Story metadata, tags, change control |
| **Story Runs** | Execution history — inspect event JSON at each step |
| **Credentials** | Team menu → Credentials — secure API key storage |
| **Workbench** | AI assistant for building/troubleshooting (CE: ~20 msgs/day) |

### Sign-in URL pattern

After signup: `https://<generated-name>.tines.com`

**Notes from my session:**

- [ ] Completed UI navigation module
- My tenant URL: _(see SETUP.md)_

---

## Module 3 — Stories

**Resource:** https://www.tines.com/university/tines-foundations/stories/

**Goal:** Define stories and navigate the story UI.

### What is a story?

A **story** is the blueprint for a workflow or agent. It visually shows:

- What steps run (actions)
- In what order (connections)
- How data transforms along the way

Every automation you build lives inside a story. You can have **unlimited stories** on CE, but only **3 active flows** total across your tenant.

### Story UI components

1. **Editor panel** — configure selected action (URL, payload, formulas)
2. **Storyboard** — drag/connect actions into flows
3. **Properties panel** — story name, description, tags

### Real-world examples → stories

| Manual task | Tines story pattern |
|---|---|
| Alert arrives → lookup IP → post to Slack | Webhook → HTTP Request → Slack action |
| Weekly inactive user report | Schedule trigger → Okta API → Email |
| Access request approval | Form/Page → conditional branch → provision API |

**Notes from my session:**

- [ ] Completed Stories module
- Key takeaway:

---

## Module 4 — Actions

**Resource:** https://www.tines.com/university/tines-foundations/actions/

**Goal:** Identify action types and how they chain together.

### What is an action?

An **action** is one step in a story. Each action:

1. Receives an **event** (JSON) from upstream actions (or a trigger)
2. Performs work (HTTP call, transform, send email, etc.)
3. **Emits** a new event for downstream actions

### Main action categories

| Category | Examples | Typical role |
|---|---|---|
| **Triggers** | Webhook, Email, Schedule | Start a flow |
| **Communication** | HTTP Request, Send to Story, Email | Call APIs, hand off to other stories |
| **Data** | Event Transform, Trigger, Group | Shape, filter, merge JSON |
| **Logic** | IF, Switch, Loop | Branch on conditions |
| **AI** | AI Action, Agent | LLM-powered steps (CE has AI credits) |
| **Cases** | Create/update case | Lightweight case management |

### SOAR pattern (ingest → enrich → decide → act)

```
Webhook (ingest alert)
    → Event Transform (normalize fields)
    → HTTP Request (enrich from threat intel API)
    → IF (decide severity)
        → true: HTTP Request (create ticket)
        → false: Event Transform (log and close)
```

**Notes from my session:**

- [ ] Completed Actions module
- Actions I want to try next:

---

## Module 5 — Events and JSON

**Goal:** Understand how data flows between actions.

### Events

- Every action output is an **event** — a JSON object
- Downstream actions reference upstream data with **liquid-style formulas**, e.g.:
  - `<<webhook.body.alert>>`
  - `<<http_request.body.data>>`
- **Story Runs** shows the full event at each step — essential for debugging

### Event Transform

Use **Event Transform** to:

- Rename/map fields
- Add computed values
- Filter arrays
- Prepare payload for next HTTP Request

Example output shape:

```json
{
  "summary": "Alert from local-script",
  "severity": "low",
  "received_at": "2026-07-01T12:00:00Z"
}
```

**Notes from my session:**

- [ ] Completed Events/JSON module
- Formula I used:

---

## Module 6 — Credentials (preview)

Full coverage is in **Builder: Core** path. Basics for now:

- Store secrets in **Credentials** — never paste API keys into action config as plaintext
- Reference in formulas: `<<CREDENTIAL.my_api_key>>`
- Types: Text, OAuth2, AWS, JWT, product-specific connect flows

Docs: https://www.tines.com/docs/credentials/

---

## Progress checklist

- [ ] Foundations intro
- [ ] UI navigation
- [ ] Stories
- [ ] Actions
- [ ] Events / JSON
- [ ] Ready for Builder: Core path

## Next steps after Foundations

1. [Builder: Core](https://www.tines.com/university/) — resources, functions, story design
2. Import from [Story Library](https://www.tines.com/library/)
3. Join Tines Slack community (link on tines.com footer)
