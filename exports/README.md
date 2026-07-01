# Story exports

Store JSON exports from your Tines tenant here. Exports are your **unlimited local library**; CE only allows **3 active flows** in the tenant at once.

**Current library:** 29 workflow JSON files (2 active, 7 standard exported, 20 complex generated). See [docs/reference/workflow-catalog.md](../docs/reference/workflow-catalog.md).

## Layout

```
exports/
├── catalog.yaml           # index + CE flow budget
├── workflows/             # your custom stories
└── story-library/         # imports from tines.com/library
```

## How to export a story

1. Open the story in your Tines tenant.
2. Deselect all actions on the storyboard.
3. Top-right **⋯ → Export story**.
4. Save to `exports/workflows/<name>.json`.
5. Update `exports/catalog.yaml`.

## Import back into tenant

1. Stories → **Import** → select JSON.
2. If name collision: **Replace** or rename first.
3. Copy webhook URL → `.env`.
4. At 3-flow limit: **disable or archive** another story first.

## Recommended exports

- `workflows/alert-triage.json` — story 121670
- `workflows/alert-triage-advanced.json` — story 121679

Full strategy: [docs/explanation/ce-operating-model.md](../docs/explanation/ce-operating-model.md) · Catalog: [docs/reference/workflow-catalog.md](../docs/reference/workflow-catalog.md)

Check budget: `./scripts/ce-flow-status.sh`
