# Workflow Catalog + CE Flow Strategy

How to build **many** workflows while staying on Community Edition (3 active flows, unlimited stories).

---

## The limit (what actually counts)

| Resource | CE limit | Notes |
|---|---|---|
| **Active flows** | **3** | Connected action chains that can run automatically |
| Stories | Unlimited | Can exist disabled/archived/exported-only |
| Events | 25,000 / month | All stories share this quota |
| Teams | 1 | Personal team |
| Builders | 1 | You |

**Flow** = one connected subgraph on a storyboard (trigger → … → terminal actions).  
A single story can contain **multiple flows** if action groups are **not** connected to each other.

Examples:

- Story with 1 webhook chain → **1 flow**
- Story with 3 separate webhook chains (isolated) → **3 flows** (uses entire CE quota in one story)
- Story disabled in UI → typically **does not consume** an active flow slot while disabled

You already use **2 flows**:

| Story | ID | Flows |
|---|---|---|
| Your first story (alert triage) | 121670 | 1 |
| Alert Triage Advanced | 121679 | 1 |

**1 flow slot left** before you must disable/archive something.

---

## Can exports get around the 3-flow limit?

**Partially — yes, with the right mental model.**

Exports do **not** let you *run* more than 3 flows at once on CE. They let you:

1. **Store unlimited workflow definitions** locally (JSON in `exports/`)
2. **Swap** which 3 are active in the tenant (import → enable → test → export → disable/archive)
3. **Share/version** workflows (git, backup, Story Library–style library of your own)
4. **Re-import** into the same or another tenant later

### What export JSON includes

Per [Tines docs — Importing and exporting](https://www.tines.com/docs/stories/importing-and-exporting/):

- All actions, connections, options, names
- **Not** event/run history
- **Not** credentials (re-wire or recreate after import)
- Webhook URLs may change on import unless you manage paths deliberately

### Export (UI)

1. Open story on storyboard
2. Deselect all actions
3. Top-right **⋯ → Export story**
4. Save to `exports/workflows/<name>.json`

### Import (UI)

1. **Stories → Import**
2. Drag JSON file
3. If name collision: choose **Replace** or rename in JSON first
4. Open story → copy new webhook URL → update `.env`

### Import (API)

`POST /api/v1/stories/import` with story JSON — requires API credential (may need paid tier; CE often UI-only for learning).

---

## Recommended CE operating model: “3 live, ∞ in the library”

```
┌─────────────────────────────────────────────────────────┐
│  TENANT (max 3 active flows)                            │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐                   │
│  │ Live A  │ │ Live B  │ │ Live C  │  ← running now    │
│  └─────────┘ └─────────┘ └─────────┘                   │
└─────────────────────────────────────────────────────────┘
         ▲ import/enable          │ export + disable
         │                        ▼
┌─────────────────────────────────────────────────────────┐
│  LOCAL exports/workflows/  (unlimited JSON backups)     │
│  + catalog.yaml (metadata, webhook paths, test scripts) │
└─────────────────────────────────────────────────────────┘
```

**Swap workflow:**

1. Export current story (if changed) → commit JSON
2. **Disable** or **archive** story in Tines (frees flow slot)
3. Import next JSON from library OR enable a disabled copy
4. Update `.env` webhook URL, run test script

**Flow packing (advanced):** Put up to **3 small tutorials** in **one story** as 3 isolated webhook chains → 1 story file, 3 flows, good for demos — but harder to maintain than separate stories.

---

## Workflow catalog (CE-friendly)

Ranked by learning value and no/low external credentials.  
**Flows** = estimated active flows if built as standalone story.

### Tier 1 — Core patterns (you’ve done some)

| # | Workflow | Trigger | Key actions | Flows | Status |
|---|---|---|---|---|---|
| 1 | Hello Webhook | Webhook | Event Transform | 1 | ✅ Original tutorial |
| 2 | Alert Triage | Webhook | Transform → Condition → branches | 1 | ✅ Story 121670 |
| 3 | Alert Triage Advanced | Webhook | + nested conditions, HTTP httpbin | 1 | ✅ Story 121679 |
| 4 | Scheduled heartbeat | Schedule | Transform → HTTP httpbin | 1 | Poll-less; 1 event/run |
| 5 | Email-to-ticket stub | Email | Transform → Condition | 1 | Needs inbound email config |
| 6 | Manual run playbook | Manual / Page | Transform → HTTP | 1 | No webhook; good for UI testing |

### Tier 2 — Integration stubs (httpbin / public APIs, no secrets)

| # | Workflow | Pattern | Flows |
|---|---|---|---|
| 7 | IP enrichment | Webhook → HTTP (ipinfo/ip-api) → Transform | 1 |
| 8 | URL reputation check | Webhook → HTTP → Condition (malicious?) | 1 |
| 9 | Geo block gate | Webhook → enrich IP → Condition country | 1 |
| 10 | Multi-step ETL | Webhook → Explode list → Transform → Implode | 1 |
| 11 | Rate limit demo | Webhook → Throttle → Transform | 1 |
| 12 | Dedup alerts | Webhook → Deduplicate → Transform | 1 |
| 13 | Delay + retry | Webhook → Delay → HTTP → Condition retry | 1 |
| 14 | Case record stub | Webhook → Transform → Page (display) | 1 |

### Tier 3 — SOAR-shaped (credentials later)

| # | Workflow | Tools | Flows |
|---|---|---|---|
| 15 | Slack alert notify | Slack webhook/credential | 1 |
| 16 | ServiceNow incident | ServiceNow REST | 1 |
| 17 | Okta user suspend path | Okta API + Condition | 1–2 |
| 18 | AWS EC2 list | AWS credential | 1 |
| 19 | Elastic hunt export | Elastic API | 1 |
| 20 | Jira create issue | Jira REST | 1 |

### Tier 4 — AI / Workbench (CE AI credits)

| # | Workflow | Pattern | Flows |
|---|---|---|---|
| 21 | AI alert summarizer | Webhook → AI Action → Transform | 1 |
| 22 | AI triage classifier | Webhook → AI → Condition severity | 1 |
| 23 | Story Library AI chatbot | Import from library | 1–2 |

### Tier 5 — Multi-flow single story (uses 2–3 slots in one export)

| # | Workflow | Design | Flows |
|---|---|---|---|
| 24 | SOC triplet pack | 3 webhooks: ingest / enrich / notify (isolated) | 3 |
| 25 | Dev test harness | Webhook + Schedule + Manual trigger chains | 3 |

### Tier 6 — Story Library imports (export after import)

| Story (library) | Pattern |
|---|---|
| Write and improve AI prompts (chatbot) | AI + conversation |
| List EC2 instances | Cloud API |
| Create ServiceNow incident from Slack | Multi-integration |
| Report inactive Okta accounts | Identity hygiene |
| Analyze URLs for fraud | Enrichment |

Catalog: https://www.tines.com/library/

---

## Suggested build order (max learning, min quota pain)

1. **Export both current stories** → `exports/workflows/` (do this now)
2. Keep **2 live** (triage + advanced), build **1 more** in the last slot
3. Good third story: **Scheduled heartbeat** OR **IP enrichment** (httpbin/public API)
4. Export #3 → disable one of the three when you want to import a Story Library template
5. Maintain `exports/catalog.yaml` (see below) as your local index

---

## Local library layout

```
exports/
├── catalog.yaml              # index of all exported workflows
├── workflows/
│   ├── alert-triage.json
│   ├── alert-triage-advanced.json
│   ├── scheduled-heartbeat.json
│   └── ...
└── story-library/            # imports from tines.com/library
    └── ai-chatbot.json
```

---

## catalog.yaml template

```yaml
workflows:
  - id: alert-triage
    file: workflows/alert-triage.json
    story_id: 121670
    flows: 1
    webhook_env: WEBHOOK_URL
    test: scripts/test-both-branches.sh
    status: active

  - id: alert-triage-advanced
    file: workflows/alert-triage-advanced.json
    story_id: 121679
    flows: 1
    webhook_env: WEBHOOK_URL_ADVANCED
    test: scripts/test-advanced-branches.sh
    status: active
```

---

## Quick reference: free a flow slot

| Action | Effect |
|---|---|
| **Disable story** | Stops runs; frees flow (verify in Stories list) |
| **Archive story** | Removes from active count; restore needs free slot |
| **Export then delete** | Slot freed; restore via Import JSON |
| **Disconnect actions** | Splits one story into multiple flows — usually avoid |

---

## What you cannot do on CE

- Run **4+ flows simultaneously** (even with exports)
- Bypass **25K events/month** with exports
- Export **credentials** — document required creds in catalog notes
- Expect **identical webhook URLs** after import (path/secret may differ)

---

## Next actions

- [x] Export stories 121670 + 121679 to `exports/workflows/`
- [x] Add `exports/catalog.yaml` entries (9 workflows + 1 story-library import)
- [x] Built Tier 2 batch: scheduled-heartbeat, ip-enrichment, url-reputation-check, dedup-alerts, throttle-demo, delay-retry, geo-block-gate
- [x] Imported Story Library: Analyze URLS for fraud and abuse → `exports/story-library/`
- [ ] Tier 3+ workflows: see `exports/workflows/BUILD.md` for Workbench prompts
- [ ] When testing exported workflows: enable story → copy webhook URL to `.env` → run test script → disable again

See also: [glossary.md](glossary.md) · [templates/story-library-starter.md](../templates/story-library-starter.md)
