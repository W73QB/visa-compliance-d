# Cloudflare Cache Everything + Purge on Deploy Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Enable cache-everything for static HTML across visafact.org, with Cloudflare purge-on-deploy in GitHub Actions.

**Architecture:** Cloudflare caches all HTML for the hostname with long TTLs. GitHub Actions triggers a Cloudflare “purge everything” call immediately after Pages deploy to prevent stale HTML or JSON. Documentation is updated to match the new cache strategy.

**Tech Stack:** Cloudflare Cache Rules + API, GitHub Actions, curl, Hugo Pages.

---

### Task 1: Baseline Cache Status + Worktree

**Files:**
- Create: none
- Modify: none
- Test: none

**Step 1: Baseline check (expected FAIL for target state)**

Run:
```bash
curl -I https://visafact.org/ | grep -i cf-cache-status
curl -I https://visafact.org/visas/costa-rica/digital-nomad-visa/ | grep -i cf-cache-status
```
Expected: `DYNAMIC` or `MISS` (not `HIT`).

**Step 2: Create worktree (isolated branch)**

Run:
```bash
git worktree add .worktrees/cache-everything -b feat/cache-everything
```

**Step 3: Enter worktree**

Run:
```bash
cd .worktrees/cache-everything
```

---

### Task 2: Cloudflare Cache Rule (Manual)

**Files:**
- Create: none
- Modify: none
- Test: none

**Step 1: Remove old cache rules (Cloudflare UI)**

In Cloudflare → Rules → Cache Rules:
- Delete or disable the existing rules that bypass HTML and ui_index.json, and the asset cache rules.
- Reason: a bypass rule on HTML will override “Cache Everything” and prevent HITs.

**Step 2: Create Cache Rule (Cloudflare UI)**

Cloudflare → Rules → Cache Rules → Create rule:
- Name: `cache-everything-host`
- Condition: `Hostname` equals `visafact.org`
- Action: `Cache Everything`
- Edge TTL: `24 hours`
- Browser TTL: `1 hour`

**Step 3: Ensure rule order**
- Place above any future bypass rules.

**Step 4: Record evidence**
- Capture a screenshot or note of the rule in ops log (optional).

---

### Task 3: Add GitHub Secrets (Manual)

**Files:**
- Create: none
- Modify: none
- Test: none

**Step 1: Create Cloudflare API Token**
- Permissions: `Zone.Cache Purge: Edit`
- Scope: `visafact.org` zone only

**Step 2: Add GitHub Secrets**
- Repo → Settings → Secrets and variables → Actions
- Add:
  - `CF_API_TOKEN`
  - `CF_ZONE_ID`

---

### Task 4: Purge Cache After Deploy (GitHub Actions)

**Files:**
- Modify: `.github/workflows/pages.yml`

**Step 1: Write a failing check (dry-run command in local shell)**

Run (will fail until secrets exist in CI):
```bash
curl -sS -X POST "https://api.cloudflare.com/client/v4/zones/${CF_ZONE_ID}/purge_cache" \
  -H "Authorization: Bearer ${CF_API_TOKEN}" \
  -H "Content-Type: application/json" \
  --data '{"purge_everything":true}'
```
Expected: failure locally (missing env). This is the pre-check.

**Step 2: Add purge step in deploy job**

Insert after `actions/deploy-pages@v4` in `deploy` job:
```yaml
      - name: Purge Cloudflare cache
        env:
          CF_API_TOKEN: ${{ secrets.CF_API_TOKEN }}
          CF_ZONE_ID: ${{ secrets.CF_ZONE_ID }}
        run: |
          set -euo pipefail
          response=$(curl -sS -X POST "https://api.cloudflare.com/client/v4/zones/${CF_ZONE_ID}/purge_cache" \
            -H "Authorization: Bearer ${CF_API_TOKEN}" \
            -H "Content-Type: application/json" \
            --data '{"purge_everything":true}')
          echo "$response" | python -c "import json,sys; data=json.load(sys.stdin); \
          (print('Purge OK') if data.get('success') else (_ for _ in ()).throw(SystemExit(f'Purge failed: {data}')))"
```

**Step 3: Commit**
```bash
git add .github/workflows/pages.yml
git commit -m "ci: purge Cloudflare cache after deploy"
```

---

### Task 5: Update Cloudflare Cache Ops Doc

**Files:**
- Modify: `docs/ops/cloudflare-security-cache.md`

**Step 1: Update cache rules section**
Replace existing cache rule guidance with:
- Remove legacy cache rules (HTML bypass + ui_index bypass + asset-only caching)
- Cache Everything for `Hostname = visafact.org`
- Edge TTL 24h, Browser TTL 1h
- Purge on deploy via GitHub Actions (reference workflow step)

**Step 2: Update manual verification**
Add:
```bash
curl -I https://visafact.org/ | grep -i cf-cache-status
curl -I https://visafact.org/posts/digital-nomad-insurance-europe/ | grep -i cf-cache-status
```
Expected: `HIT` on second request.

**Step 3: Commit**
```bash
git add docs/ops/cloudflare-security-cache.md
git commit -m "docs: update Cloudflare cache strategy"
```

---

### Task 6: Verify in CI + Production

**Files:**
- Test: none

**Step 1: Merge to main or run workflow_dispatch**
- Deploy workflow only runs on `main` push. Either:
  - Open PR and merge to `main`, or
  - Trigger `workflow_dispatch` from GitHub Actions UI on `main`.

**Step 2: Verify GitHub Actions logs**
- Confirm `Purge Cloudflare cache` step prints `Purge OK` in the deploy job.

**Step 3: Verify cache hits**
Run twice for each URL:
```bash
curl -I https://visafact.org/ | grep -i cf-cache-status
curl -I https://visafact.org/visas/costa-rica/digital-nomad-visa/ | grep -i cf-cache-status
```
Expected: first request `MISS`/`DYNAMIC`, second request `HIT`.

---

### Task 7: Merge & Cleanup

**Files:**
- Test: none

**Step 1: Open PR and merge**
- Title: `ci: purge Cloudflare cache after deploy`
- Include tests run + link to successful workflow.

**Step 2: Delete feature branch + worktree**
```bash
git worktree remove .worktrees/cache-everything
git branch -d feat/cache-everything
```
