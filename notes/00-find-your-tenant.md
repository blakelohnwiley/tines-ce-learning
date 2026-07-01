# Find Your Tines Tenant URL

Your **tenant URL** is the web address where your Tines workspace lives. It always ends in `.tines.com`.

## Where to look

1. **Browser address bar** — while logged into Tines, look at the URL:
   ```
   https://YOUR-NAME-HERE.tines.com/...
   ```
   Copy everything up to `.tines.com` (no trailing slash needed).

2. **Examples of valid tenant URLs:**
   - `https://acme-corp.tines.com`
   - `https://blake-learning.tines.com`
   - `https://friendly-panda-1234.tines.com`

3. **What it is NOT:**
   - `https://login.tines.com` — that's the login portal, not your tenant
   - `https://www.tines.com` — marketing site
   - A path like `/stories` — that's a page inside your tenant

## Quick check

If you can see **Stories** in the left sidebar and a storyboard, you're on your tenant. The hostname in the address bar is what you need.

## After you find it

1. Add it to [SETUP.md](../SETUP.md) under "Your tenant details"
2. Copy `.env.example` → `.env` and set:
   ```bash
   TENANT_URL=https://YOUR-NAME-HERE.tines.com
   ```

Do **not** commit `.env` — it may contain webhook secrets later.
