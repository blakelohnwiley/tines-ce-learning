# How-to: Swap active workflows on Community Edition

**Problem:** You need to run a different workflow in your tenant, but CE only allows three active flows and all slots are in use.

**Prerequisite:** The target workflow is exported as JSON in `exports/workflows/`.

---

## Procedure

### 1. Export anything you changed in the UI

If you edited a live story since the last commit:

1. Open the story → deselect all actions → **⋯ → Export story**.
2. Overwrite the matching file under `exports/workflows/`.
3. Commit the JSON if you use git.

### 2. Free a flow slot

In Tines, **disable** or **archive** a story that currently consumes a slot.

Disabled stories typically stop counting against the three-flow limit.

### 3. Import or enable the next workflow

**Option A — Import from JSON**

1. Stories → **Import** → select `exports/workflows/<name>.json`.
2. On name collision, choose **Replace** or rename in the JSON first.

**Option B — Enable an existing disabled copy**

Open the story and enable it if you already imported it earlier.

### 4. Update local configuration

1. Copy the new webhook URL from the Webhook action.
2. Set the matching variable in `.env` (see [`exports/catalog.yaml`](../../exports/catalog.yaml) for `webhook_env` names).
3. Run the test script listed in the catalog.

### 5. Verify

```bash
./scripts/ce-flow-status.sh
# then the workflow-specific test script, e.g.:
./scripts/test-ip-enrichment.sh
```

Check **Story Runs** for a successful terminal action.

---

## Visual model

![CE flow strategy](../diagrams/ce-flow-strategy.drawio.png)

The tenant holds at most three live flows. The local `exports/workflows/` directory holds unlimited definitions. Arrows represent **export + disable** (tenant → library) and **import + enable** (library → tenant).

---

## Advanced: flow packing

You can place up to **three isolated webhook chains** in a single story (unconnected subgraphs). That uses all three CE slots in one file — useful for demos, harder to maintain than separate stories.

---

## Related

- [How-to: Export and import stories](export-import-stories.md)
- [Reference: CE limits](../reference/ce-limits.md)
- [Reference: Workflow catalog](../reference/workflow-catalog.md)
