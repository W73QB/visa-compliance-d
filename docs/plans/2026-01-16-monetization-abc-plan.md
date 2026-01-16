# Monetization A-B-C Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Launch affiliate monetization first, then add lead-gen, then subscription reports while preserving evidence-first compliance.

**Architecture:** Phase A adds affiliate eligibility + disclosures + tracking. Phase B adds compliant lead capture. Phase C adds subscription/report workflow and access flow. All changes keep “no source = UNKNOWN” and clear disclosures.

**Tech Stack:** Hugo (PaperMod), static UI (`ui/index.html`), JSON data (`data/offers/`), Python tooling (`tools/*.py`), PowerShell tests (`tools/tests/*.ps1`).

---

### Task 0: Create isolated worktree for monetization work

**Files:**
- Create: none

**Step 1: Create worktree**

Run: `git worktree add -b feat/monetization-abc .worktrees/monetization-abc`

**Step 2: Verify worktree**

Run: `git worktree list`
Expected: shows `.worktrees/monetization-abc`

**Step 3: Commit**

Skip (no file changes).

---

### Task 1: Add affiliate policy doc (FTC/CAP-aligned disclosure rules)

**Files:**
- Create: `docs/monetization/affiliate-policy.md`

**Step 1: Write the failing test**

Create `tools/tests/affiliate_policy_tests.ps1`:
```powershell
$ErrorActionPreference = "Stop"
if (-not (Test-Path "docs/monetization/affiliate-policy.md")) { throw "missing affiliate policy" }
$text = Get-Content -Raw "docs/monetization/affiliate-policy.md"
if ($text -notmatch "clear and conspicuous") { throw "missing disclosure language" }
Write-Host "OK"
```

**Step 2: Run test to verify it fails**

Run: `powershell -NoProfile -File tools/tests/affiliate_policy_tests.ps1`
Expected: FAIL with "missing affiliate policy"

**Step 3: Write minimal implementation**

Create `docs/monetization/affiliate-policy.md`:
```markdown
# Affiliate Policy

We disclose affiliate relationships clearly and conspicuously near any affiliate link or CTA.
We do not make claims without official sources. No source = UNKNOWN.
Affiliate links never change compliance outcomes.
```

**Step 4: Run test to verify it passes**

Run: `powershell -NoProfile -File tools/tests/affiliate_policy_tests.ps1`
Expected: PASS

**Step 5: Commit**

```bash
git add docs/monetization/affiliate-policy.md tools/tests/affiliate_policy_tests.ps1
git commit -m "docs: add affiliate policy"
```

---

### Task 2: Gate affiliate CTA by compliance status (GREEN/YELLOW only)

**Files:**
- Modify: `ui/index.html`
- Modify: `tools/tests/ui_compliance_tests.ps1`

**Step 1: Write the failing test**

Append to `tools/tests/ui_compliance_tests.ps1`:
```powershell
$ui = Get-Content -Raw "ui/index.html"
Assert-True ($ui -like "*offerCta*") "offer CTA exists"
Assert-True ($ui -like "*status === \"GREEN\"*") "offer gated by GREEN"
Assert-True ($ui -like "*status === \"YELLOW\"*") "offer gated by YELLOW"
```

**Step 2: Run test to verify it fails**

Run: `powershell -NoProfile -File tools/tests/ui_compliance_tests.ps1`
Expected: FAIL on missing gating

**Step 3: Write minimal implementation**

In `ui/index.html`, update `renderOffer()` to only display CTA for GREEN/YELLOW, otherwise hide:
```js
if (!offer || (status !== "GREEN" && status !== "YELLOW")) {
  box.classList.add("hidden");
  return;
}
```

**Step 4: Run test to verify it passes**

Run: `powershell -NoProfile -File tools/tests/ui_compliance_tests.ps1`
Expected: PASS

**Step 5: Commit**

```bash
git add ui/index.html tools/tests/ui_compliance_tests.ps1
git commit -m "feat(ui): gate affiliate CTA by status"
```

---

### Task 3: Strengthen affiliate disclosure near CTA

**Files:**
- Modify: `ui/index.html`
- Test: `tools/tests/ui_compliance_tests.ps1`

**Step 1: Write the failing test**

Append to `tools/tests/ui_compliance_tests.ps1`:
```powershell
$ui = Get-Content -Raw "ui/index.html"
Assert-True ($ui -like "*Affiliate link. Results are evidence-based.*") "CTA disclosure present"
```

**Step 2: Run test to verify it fails**

Run: `powershell -NoProfile -File tools/tests/ui_compliance_tests.ps1`
Expected: FAIL if disclosure missing

**Step 3: Write minimal implementation**

In `ui/index.html`, set the disclosure text in `renderOffer()`:
```js
disclosure.textContent = "Affiliate link. Results are evidence-based.";
```

**Step 4: Run test to verify it passes**

Run: `powershell -NoProfile -File tools/tests/ui_compliance_tests.ps1`
Expected: PASS

**Step 5: Commit**

```bash
git add ui/index.html tools/tests/ui_compliance_tests.ps1
git commit -m "docs(ui): clarify affiliate disclosure near CTA"
```

---

### Task 4: Add affiliate click tracking (privacy-first)

**Files:**
- Modify: `ui/index.html`
- Modify: `hugo.toml`
- Test: `tools/tests/ui_compliance_tests.ps1`

**Step 1: Write the failing test**

Append to `tools/tests/ui_compliance_tests.ps1`:
```powershell
$ui = Get-Content -Raw "ui/index.html"
Assert-True ($ui -like "*trackAffiliateClick*") "affiliate click tracking hook"
```

**Step 2: Run test to verify it fails**

Run: `powershell -NoProfile -File tools/tests/ui_compliance_tests.ps1`
Expected: FAIL

**Step 3: Write minimal implementation**

In `ui/index.html`, add a JS function:
```js
function trackAffiliateClick(productId){
  if (window.plausible) plausible("AffiliateClick", { props: { productId } });
}
```
And attach to CTA:
```js
link.addEventListener("click", () => trackAffiliateClick(productId));
```
In `hugo.toml`, enable Plausible (or keep commented with placeholder):
```toml
[params]
plausibleDomain = "visafact.org"
```

**Step 4: Run test to verify it passes**

Run: `powershell -NoProfile -File tools/tests/ui_compliance_tests.ps1`
Expected: PASS

**Step 5: Commit**

```bash
git add ui/index.html hugo.toml tools/tests/ui_compliance_tests.ps1
git commit -m "feat(ui): add affiliate click tracking hook"
```

---

### Task 5: Lead-gen (Phase B) – add “Request compliance review” form

**Files:**
- Create: `content/contact/_index.md`
- Modify: `ui/index.html`
- Test: `tools/tests/content_lint_tests.ps1`

**Step 1: Write the failing test**

Add to `tools/tests/content_lint_tests.ps1`:
```powershell
Assert-True (Test-Path "content/contact/_index.md") "contact page exists"
```

**Step 2: Run test to verify it fails**

Run: `powershell -NoProfile -File tools/tests/content_lint_tests.ps1`
Expected: FAIL

**Step 3: Write minimal implementation**

Create `content/contact/_index.md` with disclosure and form instructions (no legal advice).
Update `ui/index.html` to show a small form after RED/UNKNOWN results with a mailto or Formspree endpoint.

**Step 4: Run test to verify it passes**

Run: `powershell -NoProfile -File tools/tests/content_lint_tests.ps1`
Expected: PASS

**Step 5: Commit**

```bash
git add content/contact/_index.md ui/index.html tools/tests/content_lint_tests.ps1
git commit -m "feat: add compliance review lead form"
```

---

### Task 6: Lead-gen governance (Phase B) – privacy + consent

**Files:**
- Create: `content/privacy/_index.md`
- Modify: `content/disclaimer/_index.md`
- Test: `tools/tests/content_lint_tests.ps1`

**Step 1: Write the failing test**

Append to `tools/tests/content_lint_tests.ps1`:
```powershell
Assert-True (Test-Path "content/privacy/_index.md") "privacy page exists"
```

**Step 2: Run test to verify it fails**

Run: `powershell -NoProfile -File tools/tests/content_lint_tests.ps1`
Expected: FAIL

**Step 3: Write minimal implementation**

Create `content/privacy/_index.md` with data collection scope and retention.
Add a short lead-gen disclaimer to `content/disclaimer/_index.md`.

**Step 4: Run test to verify it passes**

Run: `powershell -NoProfile -File tools/tests/content_lint_tests.ps1`
Expected: PASS

**Step 5: Commit**

```bash
git add content/privacy/_index.md content/disclaimer/_index.md tools/tests/content_lint_tests.ps1
git commit -m "docs: add privacy and lead-gen disclosure"
```

---

### Task 7: Subscription (Phase C) – report landing page + sample

**Files:**
- Create: `content/reports/_index.md`
- Create: `content/reports/sample.md`
- Test: `tools/tests/content_lint_tests.ps1`

**Step 1: Write the failing test**

Append to `tools/tests/content_lint_tests.ps1`:
```powershell
Assert-True (Test-Path "content/reports/_index.md") "reports page exists"
```

**Step 2: Run test to verify it fails**

Run: `powershell -NoProfile -File tools/tests/content_lint_tests.ps1`
Expected: FAIL

**Step 3: Write minimal implementation**

Create a landing page that explains subscription value and a sample report page.

**Step 4: Run test to verify it passes**

Run: `powershell -NoProfile -File tools/tests/content_lint_tests.ps1`
Expected: PASS

**Step 5: Commit**

```bash
git add content/reports/_index.md content/reports/sample.md tools/tests/content_lint_tests.ps1
git commit -m "docs: add subscription report landing pages"
```

---

### Task 8: Subscription (Phase C) – gated delivery workflow

**Files:**
- Create: `docs/monetization/subscription-ops.md`
- Modify: `ui/index.html`
- Test: `tools/tests/affiliate_policy_tests.ps1`

**Step 1: Write the failing test**

Append to `tools/tests/affiliate_policy_tests.ps1`:
```powershell
Assert-True (Test-Path "docs/monetization/subscription-ops.md") "subscription ops doc exists"
```

**Step 2: Run test to verify it fails**

Run: `powershell -NoProfile -File tools/tests/affiliate_policy_tests.ps1`
Expected: FAIL

**Step 3: Write minimal implementation**

Document the manual delivery flow (collect email + invoice + send report).
Add a CTA button in UI to request a paid report (link to /reports/).

**Step 4: Run test to verify it passes**

Run: `powershell -NoProfile -File tools/tests/affiliate_policy_tests.ps1`
Expected: PASS

**Step 5: Commit**

```bash
git add docs/monetization/subscription-ops.md ui/index.html tools/tests/affiliate_policy_tests.ps1
git commit -m "docs: add subscription ops flow"
```

---

### Task 9: Verification sweep

**Files:**
- Test: `tools/tests/ui_compliance_tests.ps1`
- Test: `tools/tests/content_lint_tests.ps1`
- Test: `tools/tests/offers_tests.ps1`

**Step 1: Run content lint**

Run: `py tools/lint_content.py`
Expected: PASS

**Step 2: Run UI and offers tests**

Run:
```bash
powershell -NoProfile -File tools/tests/ui_compliance_tests.ps1
powershell -NoProfile -File tools/tests/offers_tests.ps1
```
Expected: PASS

**Step 3: Commit**

Skip (verification only).

---

Plan complete. After approval, execute in order A → B → C.
