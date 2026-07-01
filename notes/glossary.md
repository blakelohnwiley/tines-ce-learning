# Tines Glossary

Quick reference for Community Edition learning.

| Term | Definition |
|---|---|
| **Story** | Visual workflow blueprint on the storyboard |
| **Action** | Single step in a story (webhook, HTTP request, transform, etc.) |
| **Event** | JSON payload emitted by an action; passed to connected downstream actions |
| **Flow** | Connected chain of actions on the storyboard. CE limit: **3 active flows** |
| **Story Run** | One execution of a story; inspect event history per action |
| **Webhook** | Trigger action exposing an HTTP endpoint to start a flow |
| **Event Transform** | Action that maps/filters/restructures JSON |
| **HTTP Request** | Action that calls external APIs |
| **Credential** | Securely stored secret referenced as `<<CREDENTIAL.name>>` |
| **Formula / Liquid** | Expression syntax to reference event data, e.g. `<<webhook.body.field>>` |
| **Send to Story** | Invoke another story with an event (modular design) |
| **Resource** | Reusable config snippet (Builder: Core topic) |
| **Workbench** | AI assistant in the Tines UI for building and debugging |
| **Story Library** | Pre-built templates at https://www.tines.com/library/ |
| **Community Edition** | Free tier: 1 builder, 3 flows, 25K events/month |
| **Tenant** | Your isolated Tines instance at `https://name.tines.com` |
| **Team** | Container for stories and credentials (CE: 1 team) |
| **Builder** | User who can edit stories (CE: 1 builder) |
| **Viewer** | Read-only user (CE: unlimited viewers) |

## SOAR mapping

| SOAR concept | Tines equivalent |
|---|---|
| Playbook | Story |
| Trigger / ingestion | Webhook, Email, Schedule |
| Enrichment | HTTP Request + Event Transform |
| Decision | IF / Switch actions |
| Response action | HTTP Request, Email, Case update |
| Case management | Tines Cases (built-in, basic on CE) |
