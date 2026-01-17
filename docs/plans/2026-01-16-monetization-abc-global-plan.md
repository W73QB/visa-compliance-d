# Monetization A-B-C Global Compliance Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Triển khai monetization theo thứ tự A → B → C với tuân thủ global (US + EU + UK + CA + AU + JP + SG + KR), đảm bảo disclosure rõ ràng, consent hợp lệ, và không phá vỡ nguyên tắc “no source = UNKNOWN”.

**Architecture:** Hugo site + UI tĩnh (`ui/index.html`) dùng region selector lưu `localStorage` để route legal pages và bật/tắt consent; dữ liệu affiliate/lead/payment ở `data/` + schema/validator; legal content tách theo region dưới `content/legal/` và hub pages giữ URL hiện có.

**Tech Stack:** Hugo, vanilla JS (ASCII-only trong `ui/index.html`), PowerShell tests (`tools/tests/*.ps1`), Python validators (`tools/validate.py`), JSON schemas.

---

### Task 0: Worktree setup (required by plan)

**Files:**
- Create: (none)
- Modify: (none)
- Test: (none)

**Step 1: Create worktree**

Run:
```powershell
git status -sb
git worktree add ..\visa-compliance-d-monetization -b feat/monetization-abc-global
Set-Location ..\visa-compliance-d-monetization
```
Expected: new worktree folder exists and branch is checked out.

**Step 2: Confirm repo state**

Run:
```powershell
git status -sb
```
Expected: clean working tree on `feat/monetization-abc-global`.

**Step 3: Commit**

Skip (no changes).

---

## Phase A — Affiliate (Low risk, start here)

### Task 1: Enforce affiliate disclosure requirements in tests

**Files:**
- Modify: `tools/tests/offers_tests.ps1`
- Modify: `tools/tests/ui_compliance_tests.ps1`

**Step 1: Write the failing test**

Add checks to `tools/tests/offers_tests.ps1` for explicit disclosure text:
```powershell
Assert-True ($goodJson.offers[0].disclosure -like "*earn a commission*") "disclosure states commission clearly"
Assert-True ($goodJson.offers[0].disclosure -like "*paid link*") "disclosure mentions paid link"
```
Add checks to `tools/tests/ui_compliance_tests.ps1` for CTA label + disclosure placement:
```powershell
Assert-True ($ui -like "*data-cta-disclosure*") "CTA disclosure container exists"
Assert-True ($ui -like "*Ad label*") "UI renders Ad label near CTA"
```

**Step 2: Run test to verify it fails**

Run:
```powershell
powershell -NoProfile -File tools/tests/offers_tests.ps1
powershell -NoProfile -File tools/tests/ui_compliance_tests.ps1
```
Expected: FAIL for missing disclosure wording / Ad label.

**Step 3: Write minimal implementation**

Update tests to parse JSON and read UI markers (ensure ASCII in UI; only test markers now).

**Step 4: Run test to verify it passes**

Run same commands; expected PASS.

**Step 5: Commit**

```powershell
git add tools/tests/offers_tests.ps1 tools/tests/ui_compliance_tests.ps1
git commit -m "test: enforce affiliate disclosure requirements"
```

---

### Task 2: Require disclosure in offers schema + validator

**Files:**
- Modify: `schemas/offers.schema.json`
- Modify: `tools/validate.py`
- Modify: `tools/tests/offers_tests.ps1`

**Step 1: Write the failing test**

Extend `tools/tests/offers_tests.ps1` to ensure missing `disclosure` fails validation:
```powershell
Assert-True ($procMissingDisclosure.ExitCode -ne 0) "validate fails when disclosure missing"
```

**Step 2: Run test to verify it fails**

Run:
```powershell
powershell -NoProfile -File tools/tests/offers_tests.ps1
```
Expected: FAIL (schema still allows missing disclosure).

**Step 3: Write minimal implementation**

Update `schemas/offers.schema.json` to require `disclosure`:
```json
"required": ["product_id", "affiliate_url", "label", "disclosure"]
```
Optionally add validator check for banned phrases in `tools/validate.py` (e.g., “best”, “guaranteed”).

**Step 4: Run test to verify it passes**

Run the same test; expected PASS.

**Step 5: Commit**

```powershell
git add schemas/offers.schema.json tools/validate.py tools/tests/offers_tests.ps1
git commit -m "fix: require disclosure for offers"
```

---

### Task 3: Update offers disclosure text (FTC/ASA-compliant)

**Files:**
- Modify: `data/offers/offers.json`

**Step 1: Write the failing test**

Add an assertion in `tools/tests/offers_tests.ps1` to ensure disclosure contains exact wording:
```powershell
Assert-True ($goodJson.offers[0].disclosure -like "*We may earn a commission*") "disclosure uses FTC-friendly wording"
```

**Step 2: Run test to verify it fails**

Run:
```powershell
powershell -NoProfile -File tools/tests/offers_tests.ps1
```
Expected: FAIL because disclosure is currently weak.

**Step 3: Write minimal implementation**

Update `data/offers/offers.json` disclosure:
```json
"disclosure": "Paid link. We may earn a commission if you purchase through this link."
```

**Step 4: Run test to verify it passes**

Run same test; expected PASS.

**Step 5: Commit**

```powershell
git add data/offers/offers.json
git commit -m "docs: strengthen affiliate disclosure wording"
```

---

### Task 4: Add region selector + Ad label near CTA (UI)

**Files:**
- Modify: `ui/index.html`
- Modify: `tools/tests/ui_compliance_tests.ps1`

**Step 1: Write the failing test**

Add UI compliance checks:
```powershell
Assert-True ($ui -like "*vf-region-select*") "region selector exists"
Assert-True ($ui -like "*data-cta-disclosure*") "CTA disclosure container exists"
Assert-True ($ui -like "*Ad label*") "Ad label shown near CTA"
```

**Step 2: Run test to verify it fails**

Run:
```powershell
powershell -NoProfile -File tools/tests/ui_compliance_tests.ps1
```
Expected: FAIL.

**Step 3: Write minimal implementation**

Update `ui/index.html` (ASCII-only) to:
```html
<label for="vf-region-select">Region</label>
<select id="vf-region-select" aria-label="Region selector">
  <option value="us">United States</option>
  <option value="eu-uk">EU + UK</option>
  <option value="ca">Canada</option>
  <option value="apac">AU/JP/SG/KR</option>
</select>
<div class="vf-cta-disclosure" data-cta-disclosure>
  <span class="vf-ad-label">Ad label</span>
  <span class="vf-disclosure-text"></span>
</div>
```
And JS:
```js
const REGION_KEY = "vf_region";
const DISCLOSURE_BY_REGION = {
  "us": "Paid link. We may earn a commission if you purchase through this link.",
  "eu-uk": "Paid link. We may earn a commission if you purchase through this link.",
  "ca": "Paid link. We may earn a commission if you purchase through this link.",
  "apac": "Paid link. We may earn a commission if you purchase through this link."
};
```
Ensure all strings remain ASCII.

**Step 4: Run test to verify it passes**

Run:
```powershell
powershell -NoProfile -File tools/tests/ui_compliance_tests.ps1
```
Expected: PASS.

**Step 5: Commit**

```powershell
git add ui/index.html tools/tests/ui_compliance_tests.ps1
git commit -m "feat: add region selector and CTA disclosure"
```

---

### Task 5: Add region-specific affiliate disclosure pages + hub

**Files:**
- Modify: `content/affiliate-disclosure/_index.md`
- Create: `content/legal/us/affiliate-disclosure.md`
- Create: `content/legal/eu-uk/affiliate-disclosure.md`
- Create: `content/legal/ca/affiliate-disclosure.md`
- Create: `content/legal/apac/affiliate-disclosure.md`
- Modify: `layouts/partials/extend_head.html` (create if missing)
- Create: `tools/tests/legal_pages_tests.ps1`

**Step 1: Write the failing test**

Create `tools/tests/legal_pages_tests.ps1`:
```powershell
$paths = @(
  "content/legal/us/affiliate-disclosure.md",
  "content/legal/eu-uk/affiliate-disclosure.md",
  "content/legal/ca/affiliate-disclosure.md",
  "content/legal/apac/affiliate-disclosure.md"
)
foreach ($p in $paths) {
  Assert-True (Test-Path $p) "$p exists"
}
```

**Step 2: Run test to verify it fails**

Run:
```powershell
powershell -NoProfile -File tools/tests/legal_pages_tests.ps1
```
Expected: FAIL (files missing).

**Step 3: Write minimal implementation**

Create region pages with explicit disclosure text; update hub `content/affiliate-disclosure/_index.md` to explain region routing and link to region pages. Add `layouts/partials/extend_head.html` to redirect hub to region page if `vf_region` exists:
```html
<script>
  (function () {
    var region = localStorage.getItem("vf_region");
    var isHub = location.pathname.endsWith("/affiliate-disclosure/");
    if (region && isHub) {
      location.replace("/legal/" + region + "/affiliate-disclosure/");
    }
  })();
</script>
```

**Step 4: Run test to verify it passes**

Run:
```powershell
powershell -NoProfile -File tools/tests/legal_pages_tests.ps1
```
Expected: PASS.

**Step 5: Commit**

```powershell
git add content/affiliate-disclosure/_index.md content/legal/us/affiliate-disclosure.md content/legal/eu-uk/affiliate-disclosure.md content/legal/ca/affiliate-disclosure.md content/legal/apac/affiliate-disclosure.md layouts/partials/extend_head.html tools/tests/legal_pages_tests.ps1
git commit -m "docs: add region affiliate disclosure pages"
```

---

## Phase B — Lead-gen (Medium risk, add consent + privacy)

### Task 6: Add region privacy pages + GDPR/CASL sections

**Files:**
- Create: `content/privacy/_index.md`
- Create: `content/legal/us/privacy.md`
- Create: `content/legal/eu-uk/privacy.md`
- Create: `content/legal/ca/privacy.md`
- Create: `content/legal/apac/privacy.md`
- Modify: `tools/tests/legal_pages_tests.ps1`

**Step 1: Write the failing test**

Extend `tools/tests/legal_pages_tests.ps1`:
```powershell
$privacyPaths = @(
  "content/legal/us/privacy.md",
  "content/legal/eu-uk/privacy.md",
  "content/legal/ca/privacy.md",
  "content/legal/apac/privacy.md"
)
foreach ($p in $privacyPaths) { Assert-True (Test-Path $p) "$p exists" }
```

**Step 2: Run test to verify it fails**

Run:
```powershell
powershell -NoProfile -File tools/tests/legal_pages_tests.ps1
```
Expected: FAIL.

**Step 3: Write minimal implementation**

Create region privacy pages with sections:
- EU/UK: lawful basis, consent, data subject rights, retention
- CA: CASL consent + unsubscribe
- US/APAC: disclosure, retention, contact
Update `content/privacy/_index.md` as a hub with links to region pages.

**Step 4: Run test to verify it passes**

Run same test; expected PASS.

**Step 5: Commit**

```powershell
git add content/privacy/_index.md content/legal/us/privacy.md content/legal/eu-uk/privacy.md content/legal/ca/privacy.md content/legal/apac/privacy.md tools/tests/legal_pages_tests.ps1
git commit -m "docs: add region privacy pages"
```

---

### Task 7: Add lead-gen form with consent gating

**Files:**
- Modify: `ui/index.html`
- Create: `layouts/shortcodes/lead_form.html`
- Modify: `tools/tests/ui_compliance_tests.ps1`

**Step 1: Write the failing test**

Add checks:
```powershell
Assert-True ($ui -like "*lead-form*") "lead form exists"
Assert-True ($ui -like "*consent-checkbox*") "consent checkbox exists"
```

**Step 2: Run test to verify it fails**

Run:
```powershell
powershell -NoProfile -File tools/tests/ui_compliance_tests.ps1
```
Expected: FAIL.

**Step 3: Write minimal implementation**

Add lead form block in `ui/index.html` for RED/UNKNOWN:
```html
<form id="lead-form" class="vf-lead-form" data-lead-form>
  <label>Email <input type="email" name="email" required></label>
  <label><input type="checkbox" id="lead-consent" required> I agree to be contacted.</label>
  <button type="submit" disabled>Request review</button>
</form>
```
Add JS to enable submit only when consent checked; keep ASCII-only.
Create `layouts/shortcodes/lead_form.html` so blog/legal pages can reuse the form.

**Step 4: Run test to verify it passes**

Run same UI test; expected PASS.

**Step 5: Commit**

```powershell
git add ui/index.html layouts/shortcodes/lead_form.html tools/tests/ui_compliance_tests.ps1
git commit -m "feat: add lead form with consent gating"
```

---

## Phase C — Subscription (Higher risk, add ToS/Refund + payment links)

### Task 8: Add region ToS + Refund policy pages

**Files:**
- Create: `content/terms/_index.md`
- Create: `content/refund/_index.md`
- Create: `content/legal/us/terms.md`
- Create: `content/legal/eu-uk/terms.md`
- Create: `content/legal/ca/terms.md`
- Create: `content/legal/apac/terms.md`
- Create: `content/legal/us/refund.md`
- Create: `content/legal/eu-uk/refund.md`
- Create: `content/legal/ca/refund.md`
- Create: `content/legal/apac/refund.md`
- Modify: `tools/tests/legal_pages_tests.ps1`

**Step 1: Write the failing test**

Add path checks for terms/refund files in `tools/tests/legal_pages_tests.ps1`.

**Step 2: Run test to verify it fails**

Run:
```powershell
powershell -NoProfile -File tools/tests/legal_pages_tests.ps1
```
Expected: FAIL.

**Step 3: Write minimal implementation**

Create hub pages `content/terms/_index.md` and `content/refund/_index.md` with links to region pages. Add region pages with refund terms and delivery SLA.

**Step 4: Run test to verify it passes**

Run same test; expected PASS.

**Step 5: Commit**

```powershell
git add content/terms/_index.md content/refund/_index.md content/legal/us/terms.md content/legal/eu-uk/terms.md content/legal/ca/terms.md content/legal/apac/terms.md content/legal/us/refund.md content/legal/eu-uk/refund.md content/legal/ca/refund.md content/legal/apac/refund.md tools/tests/legal_pages_tests.ps1
git commit -m "docs: add region terms and refund pages"
```

---

### Task 9: Add payment link config + premium report page

**Files:**
- Create: `data/payments/payment_links.json`
- Create: `schemas/payments.schema.json`
- Modify: `tools/validate.py`
- Create: `content/reports/premium/_index.md`
- Modify: `tools/tests/legal_pages_tests.ps1`

**Step 1: Write the failing test**

Add validation test in `tools/tests/legal_pages_tests.ps1`:
```powershell
Assert-True (Test-Path "data/payments/payment_links.json") "payment_links.json exists"
```
And add a validator test to ensure `py tools/validate.py --payments` fails without required fields.

**Step 2: Run test to verify it fails**

Run:
```powershell
powershell -NoProfile -File tools/tests/legal_pages_tests.ps1
```
Expected: FAIL.

**Step 3: Write minimal implementation**

Add schema `schemas/payments.schema.json` with required fields: `region`, `payment_link`, `label`. Update `tools/validate.py` to accept `--payments`. Create `data/payments/payment_links.json` with placeholder links per region. Create `content/reports/premium/_index.md` using Hugo data:
```md
{{ $region := "us" }}
{{ $link := index .Site.Data.payments.payment_links $region }}
[{{ $link.label }}]({{ $link.payment_link }})
```

**Step 4: Run test to verify it passes**

Run same test; expected PASS.

**Step 5: Commit**

```powershell
git add data/payments/payment_links.json schemas/payments.schema.json tools/validate.py content/reports/premium/_index.md tools/tests/legal_pages_tests.ps1
git commit -m "feat: add payment links and premium report page"
```

---

### Task 10: Add cookie consent banner (EU/UK only)

**Files:**
- Create: `layouts/partials/cookie_banner.html`
- Modify: `layouts/partials/extend_head.html`
- Modify: `tools/tests/legal_pages_tests.ps1`

**Step 1: Write the failing test**

Add check for cookie banner partial presence:
```powershell
Assert-True (Test-Path "layouts/partials/cookie_banner.html") "cookie banner partial exists"
```

**Step 2: Run test to verify it fails**

Run:
```powershell
powershell -NoProfile -File tools/tests/legal_pages_tests.ps1
```
Expected: FAIL.

**Step 3: Write minimal implementation**

Create `layouts/partials/cookie_banner.html` with banner markup and `Accept` button that sets `vf_cookie_consent=1`. In `extend_head.html`, load a small script to display banner only when `vf_region == "eu-uk"` and consent not set.

**Step 4: Run test to verify it passes**

Run same test; expected PASS.

**Step 5: Commit**

```powershell
git add layouts/partials/cookie_banner.html layouts/partials/extend_head.html tools/tests/legal_pages_tests.ps1
git commit -m "feat: add EU/UK cookie consent banner"
```

---

### Task 11: Add analytics gating (privacy-first)

**Files:**
- Modify: `layouts/partials/extend_head.html`
- Modify: `tools/tests/legal_pages_tests.ps1`

**Step 1: Write the failing test**

Add check for analytics gating:
```powershell
Assert-True ($head -like "*vf_analytics_allowed*") "analytics gating script exists"
```

**Step 2: Run test to verify it fails**

Run:
```powershell
powershell -NoProfile -File tools/tests/legal_pages_tests.ps1
```
Expected: FAIL.

**Step 3: Write minimal implementation**

Add a gating function in `extend_head.html`:
```html
<script>
  function vfAnalyticsAllowed() {
    var region = localStorage.getItem("vf_region");
    if (region === "eu-uk") return localStorage.getItem("vf_cookie_consent") === "1";
    return true;
  }
</script>
```
Load analytics script only when allowed.

**Step 4: Run test to verify it passes**

Run same test; expected PASS.

**Step 5: Commit**

```powershell
git add layouts/partials/extend_head.html tools/tests/legal_pages_tests.ps1
git commit -m "feat: gate analytics by region consent"
```

---

## Verification Sweep

### Task 12: Full verification and cleanup

**Files:**
- Modify: (none)
- Test: `tools/tests/*.ps1`

**Step 1: Run full validation**

Run:
```powershell
py tools/validate.py
py tools/build_mappings.py
py tools/build_index.py
py tools/sync_hugo_static.py
py tools/lint_content.py
powershell -NoProfile -File tools/tests/ui_compliance_tests.ps1
powershell -NoProfile -File tools/tests/offers_tests.ps1
powershell -NoProfile -File tools/tests/legal_pages_tests.ps1
```
Expected: all PASS.

**Step 2: Ensure no generated artifacts are staged**

Run:
```powershell
git status -sb
```
Expected: no `static/` or `data/snapshots/` staged.

**Step 3: Commit**

Skip (verification only).

---

## Execution Notes

- Keep `ui/index.html` ASCII-only; re-run `ui_compliance_tests.ps1` after any UI edit.
- Region key: `vf_region` stored in `localStorage`.
- Hub pages (`/affiliate-disclosure/`, `/privacy/`, `/terms/`, `/refund/`) must remain available.
- All new legal content should avoid claims beyond evidence (keep “no source = UNKNOWN”).
