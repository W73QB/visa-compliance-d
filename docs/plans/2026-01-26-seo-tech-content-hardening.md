# SEO/Content/Technical Hardening Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Close the remaining SEO/content/technical gaps flagged by internal reviews (Claude Code & Gemini) and align site with evidence-first positioning: schema coverage, CTA shortcode, safe programmatic controls, CSP simulation, and CI hygiene.

**Architecture:** Hugo + PaperMod theme for content; static UI checker; Cloudflare for headers; PowerShell tests and Python tools for generation. We will add small Hugo partials/shortcodes, adjust CI, and enforce publishing rules without changing core engine.

**Tech Stack:** Hugo, Go templates, PowerShell tests, Python scripts, GitHub Actions, Cloudflare headers (docs), Tailwind build.

---

## Task 1: Add schema support (FAQ, Article, Organization, Breadcrumb, Sitelinks)

**Files:**
- Create: `layouts/partials/schema/faq.html`
- Modify: `layouts/partials/extend_head.html`
- Modify: `layouts/_default/baseof.html` or theme equivalent include point
- (Optional) Create: `layouts/partials/schema/org.html`, `layouts/partials/schema/article.html`, `layouts/partials/schema/breadcrumb.html`, `layouts/partials/schema/website.html`
- Test: `tools/tests/analytics_tests.ps1` (ensures Hugo build), add new PowerShell test `tools/tests/schema_tests.ps1`

**Step 1: Write failing test**
- Create `tools/tests/schema_tests.ps1` to build Hugo with `HUGO_SCHEMA_TEST=1` and assert presence of `FAQPage`, `Organization`, `WebSite`, `BreadcrumbList` JSON-LD in a sample page (e.g., public/index.html and one post).

**Step 2: Run test to verify FAIL**
- `export PATH="$PWD/.bin:$PATH" && pwsh -NoProfile -File tools/tests/schema_tests.ps1`
- Expected: FAIL (schemas missing).

**Step 3: Implement schema partials**
- Add JSON-LD partials:
  - FAQ: read front matter `faq` array; skip if empty.
  - Article: for posts/guides/traps, using title, description, date, author.
  - Organization: site-wide constants (VisaFact, url, logo if available).
  - WebSite + Sitelinks search box: use baseURL and `/ui/` as target.
  - Breadcrumb: build from `.CurrentSection` and page.
- Include partials in `extend_head.html` guarded by `.IsPage` / `.IsHome`.

**Step 4: Run test to verify PASS**
- Same command as Step 2; expect PASS.

**Step 5: Commit**
- `git add layouts/partials/schema* tools/tests/schema_tests.ps1 layouts/partials/extend_head.html`
- `git commit -m "feat(seo): add schema partials (FAQ/Article/Org/Breadcrumb/WebSite)"`

---

## Task 2: Add checker CTA shortcode to prevent link rot

**Files:**
- Create: `layouts/shortcodes/checker_cta.html`
- Modify: sample content to adopt shortcode (one post + one visa page)
- Test: extend `tools/tests/ui_compliance_tests.ps1` to assert checker link presence via shortcode marker (optional), or add small test `tools/tests/shortcode_tests.ps1` rendering a fixture page.

**Step 1: Write failing test**
- Add `tools/tests/shortcode_tests.ps1`: run `hugo --minify -D` on fixture content `content/templates/checker-cta-test.md` (create) that uses `{{< checker_cta visa="ES_DNV_BLS_LONDON_2026" snapshot="latest" label="Run Checker" >}}`; assert rendered HTML contains `/ui/?visa=ES_DNV_BLS_LONDON_2026&snapshot=latest`.

**Step 2: Run test → expect FAIL**  
- `pwsh -NoProfile -File tools/tests/shortcode_tests.ps1`

**Step 3: Implement shortcode**
- Shortcode parameters: `visa` (required), `product` (optional), `snapshot` (default `latest`), `label` (default “Open Compliance Checker”).
- Output: `<a class="vf-cta" href="/ui/?visa={{ visa }}{{ if product }}&product={{ product }}{{ end }}&snapshot={{ snapshot }}">…</a>` plus a small span “Evidence-based · No source = UNKNOWN”.

**Step 4: Update one post and one visa page to use shortcode**
- Example: `content/posts/spain-dnv-insurance.md` replace manual link with shortcode.

**Step 5: Run test → PASS**
- Re-run `tools/tests/shortcode_tests.ps1`.

**Step 6: Commit**
- `git add layouts/shortcodes/checker_cta.html tools/tests/shortcode_tests.ps1 content/posts/spain-dnv-insurance.md`
- `git commit -m "feat: add checker_cta shortcode and test"`

---

## Task 3: Enforce programmatic publishing safety (evidence gate)

**Files:**
- Modify: `tools/build_content_hubs.py`
- Modify: `tools/tests/visa_hubs_tests.ps1`
- Optional: add `tools/tests/programmatic_safety_tests.ps1`

**Policy:** Only publish/index if there is ≥1 evidence item; otherwise write page with badge “UNKNOWN – no evidence found” and add `draft: true` or `front_matter: { noindex: true }`.

**Step 1: Write failing test**
- Extend `visa_hubs_tests.ps1` to load each generated detail page and assert either (a) there is at least one evidence link OR (b) front matter has `draft: true` / `noindex: true` badge text.

**Step 2: Run test → expect FAIL**  
- `pwsh -NoProfile -File tools/tests/visa_hubs_tests.ps1`

**Step 3: Implement gate**
- In `render_detail`, count evidence items; if zero → add `draft: true` (or `noindex: true`) and prepend notice “UNKNOWN – missing evidence; not indexed”.
- Optionally skip writing page entirely when no evidence (but still log).

**Step 4: Run test → PASS**  
- Re-run tests above.

**Step 5: Commit**  
- `git commit -m "chore: gate programmatic visa pages without evidence"`

---

## Task 4: Dev CSP/header simulation for local testing

**Files:**
- Create: `static/_headers` (for dev parity; Cloudflare prod still uses Transform Rules)
- Modify: docs if needed `docs/ops/cloudflare-security-cache.md` to mention local parity.
- Optional: small PowerShell test `tools/tests/headers_dev_tests.ps1` to assert file exists.

**Headers:** mirror runbook:  
```
/*
  X-Frame-Options: DENY
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: geolocation=(), microphone=(), camera=()
  Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; img-src 'self' data:; connect-src 'self'; base-uri 'self'; frame-ancestors 'none'; object-src 'none'
```

**Step 1:** Add `_headers` file.  
**Step 2:** Add brief test or checklist entry.  
**Step 3:** Commit `git commit -m "chore: add local _headers for CSP parity"`.

---

## Task 5: Schema & CTA rollout to existing content

**Files:**
- Modify: top 5 posts + 6 visa detail pages to add FAQ data in front matter (questions/answers) and replace manual checker links with shortcode.

**Step 1:** Pick pages: `spain-dnv-insurance.md`, `germany-freelance-insurance.md`, `portugal-dnv-insurance.md`, `thailand-dtv-insurance.md`, `costa-rica-dn-insurance.md`; visa detail pages under `content/visas/**/index.md`.

**Step 2:** Add front matter `faq` list (3–5 Q/A each).  
**Step 3:** Replace manual links with `{{< checker_cta visa="..." snapshot="latest" >}}`.  
**Step 4:** Run lint & schema tests.  
**Step 5:** Commit `git commit -m "content: add FAQ data and checker CTA shortcode to key pages"`.

---

## Task 6: CI hygiene & Browserslist

**Files:**
- Modify (if not already): `.github/workflows/pages.yml` ensure step order: npm ci → update-browserslist-db → build:css → build_content_hubs → rest.
- Optional: add `BROWSERSLIST_IGNORE_OLD_DATA=1` env to CSS build step to silence noise if cache stale.

**Step:** Verify with `pwsh -NoProfile -File tools/tests/pagefind_tests.ps1` and `ui_compliance_tests.ps1`.  
**Commit:** `git commit -m "ci: harden css build and browserslist update"` (only if changes).

---

## Task 7: Monitoring & tracking events (spec only)

**Files:**
- Draft GA4/GTM event mapping doc: `docs/analytics/ga4-events.md`
- (Implementation can be separate plan.)

**Step:** Document events: `select_visa`, `select_product`, `run_check`, `open_evidence`, `open_snapshot`, `copy_link`, `click_affiliate`, `notify_changes`; include parameters (visa_id, product_id, snapshot_id, status).  
**Commit:** `git commit -m "docs: add GA4 event mapping for checker funnel"`.

---

## Verification Checklist (run before claiming done)
- `pwsh -NoProfile -File tools/tests/schema_tests.ps1`
- `pwsh -NoProfile -File tools/tests/shortcode_tests.ps1`
- `pwsh -NoProfile -File tools/tests/visa_hubs_tests.ps1`
- `pwsh -NoProfile -File tools/tests/pagefind_tests.ps1`
- `pwsh -NoProfile -File tools/tests/ui_compliance_tests.ps1`
- `hugo --minify`

---

## Expected Outputs
- New schema partials rendering FAQ/Article/Org/Breadcrumb/WebSite/Sitelinks.
- Checker CTA shortcode reused across content; no hardcoded query links.
- Programmatic visa pages gated by evidence or marked noindex/draft.
- Local `_headers` to mirror CSP/security headers.
- Top posts + visa pages enriched with FAQs + shortcode.
- Updated CI keeps Browserslist fresh and pagefind clean.
- GA4 event mapping doc.

---
