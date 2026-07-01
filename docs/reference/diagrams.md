# Reference: Diagrams

Architecture diagrams for this repository. Edit the `.drawio` source in [draw.io](https://app.diagrams.net/) or the desktop app; commit both source and PNG.

---

## Inventory

| Diagram | Description | Source | PNG |
|---|---|---|---|
| CE flow strategy | Three live tenant slots vs unlimited local JSON library | [ce-flow-strategy.drawio](../diagrams/ce-flow-strategy.drawio) | [ce-flow-strategy.drawio.png](../diagrams/ce-flow-strategy.drawio.png) |
| Alert triage (base) | Webhook → normalize → severity branch | [alert-triage-base.drawio](../diagrams/alert-triage-base.drawio) | [alert-triage-base.drawio.png](../diagrams/alert-triage-base.drawio.png) |
| Alert triage (advanced) | Nested conditions, HTTP enrichment, firewall path | [alert-triage-advanced.drawio](../diagrams/alert-triage-advanced.drawio) | [alert-triage-advanced.drawio.png](../diagrams/alert-triage-advanced.drawio.png) |
| Repository layout | `docs/`, `exports/`, `scripts/`, `notes/` | [repo-layout.drawio](../diagrams/repo-layout.drawio) | [repo-layout.drawio.png](../diagrams/repo-layout.drawio.png) |

---

## Regenerate PNG exports

Requires Node.js and Chromium/Chrome (or draw.io desktop on PATH):

```bash
cd ~/.cursor/skills/project-documenter--drawio/scripts && npm install
node drawio-to-png.mjs --dir /path/to/tines/docs/diagrams
```

Single file:

```bash
node drawio-to-png.mjs docs/diagrams/ce-flow-strategy.drawio
```

---

## Style conventions

Diagrams use the project-documenter draw.io palette:

- **Primary / trigger:** blue fill (`#dae8fc`)
- **Processing:** green fill (`#d5e8d4`)
- **Decision:** yellow diamond (`#fff2cc`)
- **Escalation / alert:** red fill (`#f8cecc`)
- **External / storage:** gray or cylinder shapes

---

## Related

- [Explanation: CE operating model](../explanation/ce-operating-model.md)
- [Explanation: Alert triage pipelines](../explanation/alert-triage-pipelines.md)
