# Explanation: CE operating model

**Question:** How do you build many workflows on Community Edition when only three can run at once?

---

## The constraint is runtime, not storage

Community Edition limits **active flows** — connected action chains that can execute automatically — not stories and not your ability to design workflows.

You can:

- Create unlimited stories in the tenant (many disabled).
- Store unlimited JSON exports in git under `exports/workflows/`.
- Version, share, and back up definitions independently of what is live.

You cannot:

- Run more than three flows concurrently in one CE tenant.

Exports do **not** bypass the runtime cap. They let you **swap** which three definitions are active.

---

## Recommended model: three live, infinite library

![CE flow strategy](../diagrams/ce-flow-strategy.drawio.png)

| Layer | Role |
|---|---|
| **Tenant** | Up to three flows executing now (webhooks, schedules, etc.) |
| **Local library** | JSON exports + `catalog.yaml` metadata + test scripts |

**Swap cycle:** export (if changed) → disable in tenant → import/enable next story → update `.env` → run test script.

This matches how SOAR teams treat production (few live playbooks) vs development (large playbook library), adapted for CE’s hard limit of three.

---

## Flow vs story

| Term | Meaning |
|---|---|
| **Story** | A Tines container (storyboard, actions, settings) |
| **Flow** | One connected subgraph inside a story |

One story can contain multiple flows if subgraphs are **not** wired together — for example three separate webhook entry points. That packs three tutorials into one file but costs all three CE slots at once.

---

## What exports preserve

Export JSON includes actions, wiring, and configuration. It excludes credentials and historical runs. After import you re-link secrets using Tines credentials (`<<CREDENTIAL.name>>`), not plaintext in actions.

Webhook URLs may change on import; always copy the new URL into `.env`.

---

## Event budget

All stories share **25,000 events per month** on CE. Swapping workflows does not reset the quota. Prefer scheduled stories with sane cadence and test payloads that do not loop.

---

## Related

- [Reference: CE limits](../reference/ce-limits.md)
- [How-to: Swap workflows on CE](../how-to/swap-workflows-on-ce.md)
- [notes/05-workflow-catalog-and-ce-strategy.md](../../notes/05-workflow-catalog-and-ce-strategy.md) — extended catalog and tier list
