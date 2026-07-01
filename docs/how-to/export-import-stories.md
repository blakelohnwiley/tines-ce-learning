# How-to: Export and import Tines stories

**Problem:** You need a portable copy of a story for git, backup, or import into another tenant.

---

## Export from the Tines UI

1. Open the story on the storyboard.
2. **Deselect all actions** (click empty canvas).
3. Top-right **⋯ → Export story**.
4. Save to `exports/workflows/<descriptive-name>.json`.
5. Add or update the entry in [`exports/catalog.yaml`](../../exports/catalog.yaml).

For Story Library imports, save under `exports/story-library/`.

---

## What export JSON contains

| Included | Not included |
|---|---|
| Actions, connections, options, names | Credentials |
| Webhook paths (may change on re-import) | Event / run history |

After import, recreate or re-link credentials. Webhook URLs often change unless you manage paths deliberately.

Official reference: [Tines — Importing and exporting](https://www.tines.com/docs/stories/importing-and-exporting/).

---

## Import into the tenant

1. **Stories → Import** → drag the JSON file.
2. Resolve name collisions (**Replace** or rename in JSON).
3. Open the story and copy the webhook URL into `.env`.
4. If at the three-flow limit, [disable another story](swap-workflows-on-ce.md) first.

---

## Import via API (optional)

`POST /api/v1/stories/import` accepts story JSON. Requires an API credential; CE tenants often use the UI for learning.

---

## Related

- [`exports/README.md`](../../exports/README.md)
- [Reference: Workflow catalog](../reference/workflow-catalog.md)
