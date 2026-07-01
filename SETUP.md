# Tines CE Setup Checklist

Complete these steps in order. Check each box as you go.

## Phase 1 — Create your free tenant

> **Setup opened:** The signup page was launched in your browser during workspace setup. Re-open anytime: https://login.tines.com/saml_idp/signup

- [x] Open https://login.tines.com/saml_idp/signup
- [x] Choose region: **U.S.** or **Europe** (closest to you)
- [x] Sign up with work email, Google, or Microsoft — **no credit card required**
- [x] Complete the profile form on first login
- [x] Note your tenant URL: `https://wild-tree-3140.tines.com`
- [x] Complete the **interactive first-story tutorial** shown on welcome screen

### Your tenant details (fill in after signup)

| Field | Value |
|---|---|
| Tenant URL | https://wild-tree-3140.tines.com |
| Region | (add if known) |
| Signup date | 2026-07-01 |
| Edition | Community Edition |
| Active story | https://wild-tree-3140.tines.com/stories/121670 |
| Advanced story | https://wild-tree-3140.tines.com/stories/121679 |

## Phase 2 — Configure local environment

- [x] Copy `.env.example` to `.env`
- [x] Set `TENANT_URL` to your tenant URL (no trailing slash)
- [x] Webhook configured in `.env` (story: your-first-story / 121670)

## Phase 3 — First custom story

**→ Expand workflow:** [notes/03-alert-triage-workflow.md](notes/03-alert-triage-workflow.md) — Webhook → normalize → condition → escalate/log

Basics: [notes/02-first-story.md](notes/02-first-story.md) · Quick start: [notes/NOW-build-hello-tines.md](notes/NOW-build-hello-tines.md)

- [x] Expand **Your first story** (alert triage pipeline built)
- [x] Add Webhook → Event Transform → Condition → branch transforms
- [x] Run `./scripts/test-both-branches.sh` to test low and high paths
- [ ] Run test from Tines UI; inspect **Story Runs**
- [x] Run `./scripts/send-test-webhook.sh` from this machine

## Phase 4 — Story Library import

Follow [templates/story-library-starter.md](templates/story-library-starter.md):

- [ ] Import recommended starter story into your tenant
- [ ] Export story JSON from Tines UI → save to `exports/`

## Phase 5 — Tines University

Work through modules while taking notes in [notes/01-foundations.md](notes/01-foundations.md):

- [ ] [Tines Foundations](https://www.tines.com/university/tines-foundations/)
- [ ] [Stories module](https://www.tines.com/university/tines-foundations/stories/)
- [ ] [Actions module](https://www.tines.com/university/tines-foundations/actions/)
- [ ] [Events module](https://www.tines.com/university/tines-foundations/events/) (if available)

## Troubleshooting

| Issue | Fix |
|---|---|
| Webhook returns 404 | Verify full URL including secret path segment |
| Flow limit reached | CE allows 3 active flows — disable unused flows in other stories |
| Event quota | CE: 25,000 events/month — avoid tight polling loops |
| Script fails locally | Ensure `.env` exists and `WEBHOOK_URL` is set |
