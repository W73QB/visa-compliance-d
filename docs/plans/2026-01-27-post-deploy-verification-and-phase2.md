# Post-Deploy Verification + Phase 2 Content Plan Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Verify production has the latest changes, confirm GA4/GTM is firing, and publish a concrete Phase 2 content expansion backlog.

**Architecture:** Add two verification docs (production + GA4/GTM) and a Phase 2 content backlog doc with exact targets. This keeps evidence in-repo and creates a clear, reviewable path for the next expansion cycle.

**Tech Stack:** Git, Hugo content, Markdown, curl

---

### Task 1: Create a dedicated worktree

**Files:**
- Create: `.worktrees/post-deploy-phase2` (worktree directory)

**Step 1: Create worktree (use @using-git-worktrees)**

Run:
```bash
git worktree add .worktrees/post-deploy-phase2 -b feat/post-deploy-phase2
```
Expected: New worktree created with clean status.

**Step 2: Enter worktree**

Run:
```bash
cd .worktrees/post-deploy-phase2
git status -s
```
Expected: No changes.

---

### Task 2: Capture production verification evidence

**Files:**
- Create: `docs/ops/production-verification-2026-01-27.md`

**Step 1: Run production checks**

Run:
```bash
curl -I https://visafact.org/ | egrep -i "content-security-policy|report-to|x-frame-options|x-content-type-options|referrer-policy|permissions-policy"
curl -sL https://visafact.org/ | grep -Ei "GTM-N4JLPLC2|googletagmanager|gtm\\.js|gtm-id"
curl -sL https://visafact.org/ui/ | grep -Ei "GTM-N4JLPLC2|googletagmanager|gtm\\.js|gtm-id"
```
Expected: GTM markers present on `/` and `/ui/`. Header output recorded (may be empty if CSP not set).

**Step 2: Write evidence file**

Create `docs/ops/production-verification-2026-01-27.md`:
```markdown
# Production Verification (2026-01-27)

## Header Check
```
PASTE curl -I OUTPUT HERE
```

## GTM Marker Check
```
PASTE curl -sL OUTPUT HERE
```
```

**Step 3: Commit**

```bash
git add docs/ops/production-verification-2026-01-27.md
git commit -m "docs: add production verification evidence"
```

---

### Task 3: Add GA4/GTM verification checklist

**Files:**
- Create: `docs/analytics/ga4-postdeploy-checklist.md`

**Step 1: Add checklist**

Create `docs/analytics/ga4-postdeploy-checklist.md`:
```markdown
# GA4/GTM Post-Deploy Checklist

## GTM container
- GTM ID: GTM-N4JLPLC2
- Verify gtm.js loads on:
  - https://visafact.org/
  - https://visafact.org/ui/

## GA4 (Realtime)
- Measurement ID: G-6BLK7YFGMS
- Expected events:
  - page_view (home + /ui/)
  - run_check (after user clicks “Check Compliance”)
  - select_visa / select_product (when dropdowns change)

## Manual steps
1. Open Chrome Incognito.
2. Disable ad blockers.
3. DevTools → Network → filter `gtm.js`.
4. Confirm request to `https://www.googletagmanager.com/gtm.js?id=GTM-N4JLPLC2`.
5. Tag Assistant Preview should detect container.
6. GA4 Realtime should show page_view within 1–2 minutes.
```

**Step 2: Commit**

```bash
git add docs/analytics/ga4-postdeploy-checklist.md
git commit -m "docs: add GA4/GTM post-deploy checklist"
```

---

### Task 4: Publish Phase 2 content backlog

**Files:**
- Create: `docs/plans/2026-01-27-phase2-content-backlog.md`

**Step 1: Create backlog file**

Create `docs/plans/2026-01-27-phase2-content-backlog.md`:
```markdown
# Phase 2 Content Expansion Backlog (90 days)

## Targets (Top 5 posts)
1) content/posts/spain-dnv-insurance.md
   - Target length: 800–1,200 words
   - Add sections: Eligibility summary, Common pitfalls, Evidence highlights, FAQ (existing), CTA to checker
   - Internal links: /visas/spain/..., /posts/safetywing-vs-worldnomads-vs-genki/

2) content/posts/safetywing-vs-worldnomads-vs-genki.md
   - Target length: 1,200–1,800 words
   - Add sections: Pros/Cons by product, Best for, Pricing notes, Evidence limitations, FAQ
   - Internal links: /visas/spain/..., /visas/germany/..., /posts/safetywing-spain-dnv-rejected/

3) content/posts/germany-freelance-insurance.md
   - Target length: 800–1,200 words
   - Add sections: Travel vs health insurance, Common rejection reasons, Evidence highlights, FAQ (existing)
   - Internal links: /visas/germany/..., /posts/digital-nomad-insurance-europe/

4) content/posts/portugal-dnv-insurance.md
   - Target length: 800–1,200 words
   - Add sections: Coverage expectations, Payment cadence, Evidence highlights, FAQ (existing)
   - Internal links: /visas/portugal/..., /posts/digital-nomad-insurance-europe/

5) content/posts/thailand-dtv-insurance.md
   - Target length: 800–1,200 words
   - Add sections: Why insurance is optional, Risk scenarios, Evidence highlights, FAQ (existing)
   - Internal links: /visas/thailand/..., /posts/digital-nomad-insurance-asia/

## Phase 2 completion criteria
- Each post meets target length range.
- Each post includes at least 2 internal links to /visas/.
- Each post includes a “Check in the engine” CTA.
```

**Step 2: Commit**

```bash
git add docs/plans/2026-01-27-phase2-content-backlog.md
git commit -m "docs: add phase 2 content backlog"
```

---

### Task 5: Verification

**Files:**
- Verify: `docs/ops/production-verification-2026-01-27.md`
- Verify: `docs/analytics/ga4-postdeploy-checklist.md`
- Verify: `docs/plans/2026-01-27-phase2-content-backlog.md`

**Step 1: Ensure working tree is clean**

Run: `git status -s`  
Expected: No changes.

