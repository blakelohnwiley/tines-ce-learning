# Story Library — Recommended Starter Import

Import a pre-built story to learn real-world patterns without building from scratch.

**Library:** https://www.tines.com/library/

---

## Recommended starter (no credentials required to explore)

### Write and improve AI prompts with an AI chatbot

- **Why:** Introduces AI actions and conversational patterns; works on CE with AI credits
- **Tools:** Tavily (optional — can adapt if you skip enrichment)
- **Flows:** Check flow count before import — CE allows 3 active flows total

**Alternative (API-only, good for SOAR learners):**

### List EC2 instances in AWS

- **Why:** Classic pattern: credential → HTTP/API → transform → output
- **Tools:** AWS (requires AWS credential in Tines)
- **Note:** Skip if you don't have AWS access; use the AI chatbot story instead

---

## How to import

1. Log in to your tenant: `https://<your-tenant>.tines.com`
2. Open https://www.tines.com/library/
3. Search or browse for the story title above
4. Click **Import** (or **Import to Tines**)
5. Select your team when prompted
6. Open the imported story on the storyboard — trace the flow:
   - What is the **trigger**?
   - Where is data **transformed**?
   - What **credentials** does it expect?

---

## Adapt for CE limits

Before importing, check your active flow count:

1. Review existing stories — disable unused flows if you're at the 3-flow limit
2. After import, disable flows in stories you're not actively studying

---

## Export to this workspace

After import:

1. Open the story in Tines
2. Story menu → **Export**
3. Save JSON to:

```
exports/story-library-<short-name>.json
```

Example: `exports/story-library-ai-chatbot.json`

---

## Import checklist

- [ ] Chosen story from Story Library
- [ ] Imported to tenant
- [ ] Walked through storyboard (trigger → transforms → outputs)
- [ ] Noted required credentials (if any)
- [ ] Exported JSON saved to `exports/`

---

## Other library stories worth exploring later

| Story | Tools | Pattern |
|---|---|---|
| Create a ServiceNow incident from Slack | ServiceNow, Slack | Multi-integration SOAR |
| Search Elastic data sets and display results | Elastic | Search + display |
| Report on inactive Okta accounts | Okta | Identity hygiene automation |
| Analyze URLs for fraud and abuse | Zendesk | Enrichment + ticketing |

See full catalog: https://www.tines.com/library/
