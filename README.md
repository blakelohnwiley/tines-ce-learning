# Tines Community Edition — Learning Workspace

Local home base for learning [Tines](https://www.tines.com/) (no-code SOAR / intelligent workflow platform) on the **free Community Edition**.

## Quick links

| Resource | URL |
|---|---|
| Sign up (free, no credit card) | https://login.tines.com/saml_idp/signup |
| Community Edition overview | https://www.tines.com/get-started-with-tines-community-edition/ |
| Tines University (Foundations) | https://www.tines.com/university/tines-foundations/ |
| Story Library | https://www.tines.com/library/ |
| Documentation | https://www.tines.com/docs/ |

## Community Edition limits

- 1 builder, unlimited viewers
- 3 active flows, 25,000 events/month
- 1 team, full platform access for learning

## Documentation

Structured docs follow the [Diátaxis framework](https://diataxis.fr/) — start at **[docs/README.md](docs/README.md)**:

| Type | Start here |
|---|---|
| Tutorial | [Getting started](docs/tutorials/getting-started.md) |
| How-to | [Swap workflows on CE](docs/how-to/swap-workflows-on-ce.md) |
| Reference | [Workflow catalog](docs/reference/workflow-catalog.md) · [Diagrams](docs/reference/diagrams.md) |
| Explanation | [CE operating model](docs/explanation/ce-operating-model.md) |

Architecture diagrams (draw.io + PNG): [`docs/diagrams/`](docs/diagrams/).

**Workflow library:** 29 JSON exports (20 complex generated, 8–11 actions each). Validate: `./scripts/validate-workflow-library.sh`

## Project structure

```
tines/
├── docs/                 # Diátaxis docs + draw.io diagrams
├── SETUP.md              # Account setup checklist (fill in after signup)
├── .env.example          # Tenant URL and webhook placeholders
├── notes/                # Learning notes and walkthroughs
├── scripts/              # Local test scripts (webhook POST)
├── exports/              # Story JSON exports from your tenant
└── templates/            # Story Library import guides
```

## Getting started

1. Complete the signup checklist in [SETUP.md](SETUP.md).
2. Work through [notes/01-foundations.md](notes/01-foundations.md) alongside Tines University.
3. Build your first story using [notes/02-first-story.md](notes/02-first-story.md).
4. **Expand to a branching workflow:** [notes/03-alert-triage-workflow.md](notes/03-alert-triage-workflow.md).
5. **Advanced duplicate story:** [notes/04-alert-triage-advanced.md](notes/04-alert-triage-advanced.md) — 11 actions, HTTP enrichment, 4 test paths.
6. **Workflow catalog + CE export strategy:** [docs/explanation/ce-operating-model.md](docs/explanation/ce-operating-model.md) (formal) or [notes/05-workflow-catalog-and-ce-strategy.md](notes/05-workflow-catalog-and-ce-strategy.md) (extended journal).
7. Copy `.env.example` to `.env`, add webhook URLs, then run:

   ```bash
   ./scripts/send-test-webhook.sh
   ./scripts/test-both-branches.sh          # base story
   ./scripts/test-advanced-branches.sh      # advanced story
   ```

7. Import a Story Library template per [templates/story-library-starter.md](templates/story-library-starter.md) and save the export to `exports/`.
8. Check flow budget: `./scripts/ce-flow-status.sh`

## Security

- Never commit `.env` or real webhook secrets.
- Use `<<CREDENTIAL.name>>` in Tines for API keys — not plaintext in actions.
