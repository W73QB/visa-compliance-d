# VisaFact Site Pages UI Refresh Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Make Blog, Methodology, Disclaimer, and Affiliate pages visually consistent with the VisaFact checker and fix encoding defects.

**Architecture:** Add a shared brand layer via Hugo overrides (custom CSS + head partial), then add reusable shortcodes for trust/CTA blocks and update content pages to use them. Include a small regression test for encoding glitches.

**Tech Stack:** Hugo (PaperMod), Markdown, Hugo shortcodes/partials, CSS, PowerShell tests.

**Dependencies:**
- `2026-01-14-ui-upgrade-visafact.md` Phase 1 (Tasks 1-3) must be complete to keep palette/typography aligned.

---

### Task 1: Add encoding regression test for legal pages

**Files:**
- Create: `tools/tests/content_encoding_tests.ps1`

**Step 1: Write the failing test**

```powershell
# tools/tests/content_encoding_tests.ps1
$ErrorActionPreference = "Stop"
$failed = $false

function Assert-True {
  param([bool]$Condition, [string]$Message)
  if (-not $Condition) { Write-Host "FAIL: $Message" -ForegroundColor Red; $script:failed = $true }
  else { Write-Host "PASS: $Message" -ForegroundColor Green }
}

Write-Host "Content encoding checks..." -ForegroundColor Cyan

$paths = @(
  "content/methodology/_index.md",
  "content/disclaimer/_index.md",
  "content/affiliate-disclosure/_index.md"
)

foreach ($p in $paths) {
  $raw = Get-Content -Raw -Path $p
  Assert-True (-not ($raw -match "\u0192\?")) "$p has no broken encoding sequence '\u0192?'"
  Assert-True (-not ($raw -match "\uFFFD")) "$p has no replacement character"
  Assert-True (-not ($raw.StartsWith([char]0xFEFF))) "$p has no BOM"
}

if ($failed) { Write-Error "Encoding checks failed."; exit 1 }
Write-Host "All checks passed." -ForegroundColor Green
```

**Step 2: Run test to verify it fails**

Run: `powershell -NoProfile -File tools/tests/content_encoding_tests.ps1`
Expected: FAIL on broken encoding sequences.

**Step 3: Commit**

```bash
git add tools/tests/content_encoding_tests.ps1
git commit -m "test: add encoding checks for legal pages"
```

---

### Task 2: Fix encoding glitches in legal pages

**Files:**
- Modify: `content/methodology/_index.md`
- Modify: `content/disclaimer/_index.md`
- Modify: `content/affiliate-disclosure/_index.md`

**Step 1: Replace broken sequences**

Replace common glitches like:
- `\u0192?Ts` -> 's
- `\u0192?o...\u0192??` -> "..." or plain ASCII quotes

Use exact replacements in file text so the test passes.

Find all glitches:
```powershell
rg "\u0192\?" content/
```

Example replace (PowerShell):
```powershell
$path = "content/methodology/_index.md"
(Get-Content -Raw $path) -replace "\u0192\?Ts", "'s" | Set-Content -Path $path -Encoding UTF8
```

**Step 2: Run test to verify it passes**

Run: `powershell -NoProfile -File tools/tests/content_encoding_tests.ps1`
Expected: PASS.

**Step 3: Commit**

```bash
git add content/methodology/_index.md content/disclaimer/_index.md content/affiliate-disclosure/_index.md
git commit -m "fix(content): repair encoding in legal pages"
```

---

### Task 3: Add site-wide brand CSS and fonts

**Files:**
- Create: `static/css/visafact.css`
- Create: `layouts/partials/extend_head.html`

**Step 1: Add brand CSS**

Create `static/css/visafact.css`:
```css
:root {
  --primary: #1e3a5f;
  --secondary: #c9a227;
  --theme: #faf8f5;
  --entry: #ffffff;
  --content: #1a1a1a;
  --vf-primary: #1e3a5f;
  --vf-accent: #c9a227;
  --vf-bg: #faf8f5;
  --vf-text: #1a1a1a;
  --vf-surface: #ffffff;
  --vf-border: #e8e4df;
}

html[data-theme="dark"] {
  --theme: #0f1419;
  --entry: #1a232e;
  --content: #f5f5f5;
  --vf-bg: #0f1419;
  --vf-text: #f5f5f5;
  --vf-surface: #1a232e;
  --vf-border: #2d3748;
}

body {
  font-family: "Plus Jakarta Sans", system-ui, sans-serif;
  background: var(--vf-bg);
  color: var(--vf-text);
}

h1, h2, h3, h4 {
  font-family: "DM Serif Display", Georgia, serif;
  letter-spacing: 0.01em;
}

a {
  color: var(--vf-primary);
}

a:hover {
  color: var(--vf-accent);
}

/* PaperMod cards */
.post-entry, .post-single, .entry-content {
  border-radius: 14px;
  background: var(--vf-surface);
  border: 1px solid var(--vf-border);
}

/* Header / footer alignment */
.vf-header {
  border-bottom: 1px solid var(--vf-border);
  background: rgba(250, 248, 245, 0.9);
  backdrop-filter: blur(8px);
}
html[data-theme="dark"] .vf-header {
  background: rgba(15, 20, 25, 0.9);
}
.vf-header .logo a {
  font-family: "DM Serif Display", Georgia, serif;
  color: var(--vf-text);
}
.vf-menu a span {
  font-weight: 600;
}
.vf-footer {
  border-top: 1px solid var(--vf-border);
  background: var(--vf-surface);
}

/* CTA button style */
.vf-cta {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.6rem 1rem;
  background: var(--vf-primary);
  color: #fff;
  border-radius: 10px;
  font-weight: 700;
  text-decoration: none;
}

.vf-cta:hover { background: #152a45; }

/* CTA focus states */
.vf-cta:focus-visible {
  outline: 2px solid var(--vf-accent);
  outline-offset: 2px;
}

/* Trust callout */
.vf-trust {
  border: 2px solid var(--vf-accent);
  padding: 1rem;
  border-radius: 12px;
  background: rgba(201,162,39,0.08);
  font-weight: 600;
}
.vf-trust:focus-within {
  box-shadow: 0 0 0 2px var(--vf-accent);
}
```

**Step 2: Add head partial to load fonts and CSS**

Create `layouts/partials/extend_head.html`:
```html
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="{{ "css/visafact.css" | relURL }}" />
```

**Step 3: Commit**

```bash
git add static/css/visafact.css layouts/partials/extend_head.html
git commit -m "feat(site): add VisaFact brand fonts and CSS"
```

---

### Task 4: Override header/footer for brand consistency

**Files:**
- Create: `layouts/partials/header.html`
- Create: `layouts/partials/footer.html`

**Step 1: Copy theme partials**

Run:
```powershell
Copy-Item themes/PaperMod/layouts/partials/header.html layouts/partials/header.html
Copy-Item themes/PaperMod/layouts/partials/footer.html layouts/partials/footer.html
```

**Step 2: Add VisaFact class hooks**

Update `layouts/partials/header.html`:
```html
<header class="header vf-header">
```
```html
<nav class="nav vf-nav">
```
```html
<ul id="menu" class="vf-menu">
```

Update `layouts/partials/footer.html`:
```html
<footer class="footer vf-footer">
```

**Step 3: Commit**

```bash
git add layouts/partials/header.html layouts/partials/footer.html
git commit -m "feat(site): override header/footer with VisaFact hooks"
```

---

### Task 5: Add shortcodes for CTA and trust blocks

**Files:**
- Create: `layouts/shortcodes/vf-cta.html`
- Create: `layouts/shortcodes/vf-trust.html`

**Step 1: Create CTA shortcode**

```html
<!-- layouts/shortcodes/vf-cta.html -->
<a class="vf-cta" href="{{ .Get "href" }}">
  {{ .Get "label" }}
</a>
```

**Step 2: Create trust callout shortcode**

```html
<!-- layouts/shortcodes/vf-trust.html -->
<div class="vf-trust">
  {{ .Inner }}
</div>
```

**Step 3: Commit**

```bash
git add layouts/shortcodes/vf-cta.html layouts/shortcodes/vf-trust.html
git commit -m "feat(site): add CTA and trust shortcodes"
```

---

### Task 6: Add Blog index hero and CTA

**Files:**
- Create: `content/posts/_index.md`

**Step 0: Check existing file**

```powershell
if (Test-Path content/posts/_index.md) {
  Write-Host "content/posts/_index.md already exists; edit instead of create."
}
```

**Step 1: Add hero content**

```markdown
---
title: "Blog"
---

{{< vf-trust >}}
Evidence-based visa insurance updates. No source = UNKNOWN.
{{< /vf-trust >}}

{{< vf-cta href="/ui/" label="Open Compliance Checker" >}}
```

**Step 2: Commit**

```bash
git add content/posts/_index.md
git commit -m "feat(content): add blog hero and CTA"
```

---

### Task 7: Add trust + CTA blocks to legal pages

**Files:**
- Modify: `content/methodology/_index.md`
- Modify: `content/disclaimer/_index.md`
- Modify: `content/affiliate-disclosure/_index.md`

**Step 1: Insert trust block near top**

Example:
```markdown
{{< vf-trust >}}
All results are evidence-based. Missing evidence -> UNKNOWN.
{{< /vf-trust >}}
```

**Step 2: Add CTA to checker at end of page**

```markdown
{{< vf-cta href="/ui/" label="Open Compliance Checker" >}}
```

**Step 3: Commit**

```bash
git add content/methodology/_index.md content/disclaimer/_index.md content/affiliate-disclosure/_index.md
git commit -m "feat(content): add trust and CTA blocks to legal pages"
```

---

### Task 8: Verify content lint and run Hugo server

**Files:**
- Run: `py tools/lint_content.py`
- Run: `hugo --minify`
- Run: `hugo server -D`

**Step 1: Run lint**

Run: `py tools/lint_content.py`
Expected: PASS.

**Step 2: Run Hugo build**

Run: `hugo --minify`
Expected: No errors.

**Step 3: Run Hugo server**

Run: `hugo server -D`
Expected: Server starts at `http://localhost:1313/`.

**Step 4: Manual review**

Check:
- Blog index shows trust box + CTA
- Methodology/Disclaimer/Affiliate show trust box + CTA
- Typography matches checker (DM Serif + Plus Jakarta Sans)
- Colors align with navy + gold

**Step 4: Commit**

```bash
# No commit unless lint fixes were required
```

---

## Test Commands Reference

```bash
powershell -NoProfile -File tools/tests/content_encoding_tests.ps1
py tools/lint_content.py
hugo --minify
hugo server -D
```

---

*Plan created: 2026-01-14*
*Based on: UI.md*





