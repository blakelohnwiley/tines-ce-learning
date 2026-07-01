# Reference: Community Edition limits

Facts about Tines Community Edition as used in this workspace. Source of truth for live counts: [`exports/catalog.yaml`](../../exports/catalog.yaml).

---

## Platform limits

| Resource | CE limit |
|---|---|
| Active flows | **3** |
| Stories | Unlimited (can exist disabled/archived) |
| Events | 25,000 / month (shared) |
| Teams | 1 |
| Builders | 1 |
| Viewers | Unlimited |

---

## What counts as a flow

A **flow** is one connected subgraph on a storyboard: trigger through terminal actions.

| Story layout | Flows consumed |
|---|---|
| One webhook chain with branches | 1 |
| Three isolated webhook chains (not connected) | 3 |
| Disabled / archived story | Typically 0 |

---

## Current tenant snapshot

| Field | Value |
|---|---|
| Tenant | `https://wild-tree-3140.tines.com` |
| Max active flows | 3 |
| Used flows | 2 |
| Remaining | 1 |

Active stories:

| Name | Story ID | Flows |
|---|---|---|
| Your first story (alert triage) | 121670 | 1 |
| Alert Triage Advanced | 121679 | 1 |

---

## Check locally

```bash
./scripts/ce-flow-status.sh
```

---

## Related

- [Explanation: CE operating model](../explanation/ce-operating-model.md)
- [How-to: Swap workflows on CE](../how-to/swap-workflows-on-ce.md)
