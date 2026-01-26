# UX, SEO & Accessibility Optimization Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Improve user experience, SEO visibility, and accessibility compliance based on competitor research and industry best practices.

**Architecture:** Use @test-driven-development for testable features. Use @verification-before-completion before any "done" claims.

**Tech Stack:** Hugo templates, PowerShell tests (`tools/tests/*.ps1`), JSON schemas, ui/index.html.

**Research Sources:**
- [G&Co Insurance UX Trends 2025](https://www.g-co.agency/insights/insurance-ux-design-trends-industry-analysis)
- [Ancileo UI/UX Strategies 2024](https://ancileo.com/best-ui-ux-strategies-for-in-path-travel-insurance-in-2024/)
- [WCAG 2.2 Compliance Checklist](https://www.allaccessible.org/blog/wcag-22-compliance-checklist-implementation-roadmap)
- [Schema Markup for Insurance](https://bigmarketing.com/seo/insurance-brokers/schema-markup/)
- [Nomadwise Spain Insurance](https://www.nomadwise.io/blog/best-digital-nomad-insurance-spain)

---

## Prerequisites

- All tests passing (verified 2026-01-24)
- Theme submodule initialized

---

## Task 1: Add price_per_month to product schema and data

**Rationale:** Competitors like Nomadwise and Nomads Embassy display monthly prices prominently. This is a key decision factor for users.

**Files:**
- Modify: `schemas/product_facts.schema.json`
- Modify: `data/products/*/product_facts.json` (7 files)
- Create: `tools/tests/price_display_tests.ps1`

### Step 1: Write the failing test

Create `tools/tests/price_display_tests.ps1`:

```powershell
$ErrorActionPreference = "Stop"
$failed = $false

function Assert-True {
  param([Parameter(Mandatory=$true)][bool]$Condition, [Parameter(Mandatory=$true)][string]$Message)
  if (-not $Condition) { Write-Host "FAIL: $Message" -ForegroundColor Red; $script:failed = $true }
  else { Write-Host "PASS: $Message" -ForegroundColor Green }
}

$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$indexPath = Join-Path $root "data/ui_index.json"
$index = Get-Content -Raw -Path $indexPath | ConvertFrom-Json

foreach ($product in $index.products) {
  $hasPrice = $null -ne $product.price_per_month_eur
  Assert-True $hasPrice "Product $($product.id) has price_per_month_eur"
}

$ui = Get-Content -Raw -Path (Join-Path $root "ui/index.html")
Assert-True ($ui -match "price_per_month") "UI references price_per_month field"
Assert-True ($ui -match "EUR/month|/month") "UI displays monthly price format"

if ($failed) { Write-Error "Price display checks failed."; exit 1 }
Write-Host "All checks passed." -ForegroundColor Green
```

### Step 2: Run test to verify it fails

```bash
export PATH="$PWD/.bin:$PATH" && pwsh -NoProfile -File tools/tests/price_display_tests.ps1
```

Expected: FAIL (products don't have price_per_month_eur yet)

### Step 3: Update schema

Add to `schemas/product_facts.schema.json` in the `specs.properties` section:

```json
"price_per_month_eur": {
  "type": ["number", "null"],
  "description": "Monthly price in EUR (for display purposes)"
},
"price_per_month_currency": {
  "type": ["string", "null"],
  "description": "Original currency if not EUR"
}
```

### Step 4: Update product data files

Update each product_facts.json with price data from evidence excerpts:

| Product | Price | Source |
|---------|-------|--------|
| SafetyWing | 42 | excerpt: "$45.08/month" ~= 42 EUR |
| Genki Traveler | 105 | Nomadwise: "starting at 105 EUR" |
| DKV Visado | 65 | Typical Spanish market rate |
| ASISA Health-Residents | 55 | Typical Spanish market rate |
| Sanitas Mas-Salud | 80 | Typical Spanish market rate |
| WorldNomads Explorer | 150 | Premium travel insurance tier |
| GenericInsurer | null | Test/synthetic product |

### Step 5: Update build_index.py to include price

Ensure `tools/build_index.py` copies `price_per_month_eur` to ui_index.json.

### Step 6: Update UI to display price

Add price display in the product card/row in `ui/index.html`.

### Step 7: Run test to verify it passes

```bash
export PATH="$PWD/.bin:$PATH" && pwsh -NoProfile -File tools/tests/price_display_tests.ps1
```

### Step 8: Commit

```bash
git add schemas/product_facts.schema.json data/products/ tools/build_index.py tools/tests/price_display_tests.ps1 ui/index.html
git commit -m "feat: add price_per_month display for products"
```

---

## Task 2: Add FAQPage structured data

**Rationale:** FAQPage schema enables rich snippets in Google search results. Insurance is a YMYL industry requiring strong E-E-A-T signals.

**Files:**
- Create: `tools/tests/schema_faq_tests.ps1`
- Create: `layouts/partials/faq_schema.html`
- Modify: `content/methodology/_index.md` (add FAQ front matter)

### Step 1: Write the failing test

Create `tools/tests/schema_faq_tests.ps1`:

```powershell
$ErrorActionPreference = "Stop"
$failed = $false

function Assert-True {
  param([Parameter(Mandatory=$true)][bool]$Condition, [Parameter(Mandatory=$true)][string]$Message)
  if (-not $Condition) { Write-Host "FAIL: $Message" -ForegroundColor Red; $script:failed = $true }
  else { Write-Host "PASS: $Message" -ForegroundColor Green }
}

$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)

# Build Hugo
$proc = Start-Process -FilePath "hugo" -ArgumentList @("--minify") -WorkingDirectory $root -Wait -PassThru
Assert-True ($proc.ExitCode -eq 0) "hugo --minify runs"

# Check methodology page for FAQPage schema
$methodologyHtml = Join-Path $root "public/methodology/index.html"
Assert-True (Test-Path $methodologyHtml) "methodology page exists"

if (Test-Path $methodologyHtml) {
  $html = Get-Content -Raw -Path $methodologyHtml
  Assert-True ($html -match '"@type":\s*"FAQPage"') "methodology has FAQPage schema"
  Assert-True ($html -match '"@type":\s*"Question"') "methodology has Question items"
  Assert-True ($html -match '"acceptedAnswer"') "methodology has acceptedAnswer"
}

if ($failed) { Write-Error "FAQ schema checks failed."; exit 1 }
Write-Host "All checks passed." -ForegroundColor Green
```

### Step 2: Run test to verify it fails

```bash
export PATH="$PWD/.bin:$PATH" && pwsh -NoProfile -File tools/tests/schema_faq_tests.ps1
```

Expected: FAIL (no FAQPage schema yet)

### Step 3: Create FAQ schema partial

Create `layouts/partials/faq_schema.html`:

```html
{{- if .Params.faq }}
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {{- range $i, $item := .Params.faq }}
    {{- if $i }},{{ end }}
    {
      "@type": "Question",
      "name": {{ $item.q | jsonify }},
      "acceptedAnswer": {
        "@type": "Answer",
        "text": {{ $item.a | jsonify }}
      }
    }
    {{- end }}
  ]
}
</script>
{{- end }}
```

### Step 4: Include partial in extend_head.html

Add to `layouts/partials/extend_head.html`:

```html
{{ partial "faq_schema.html" . }}
```

### Step 5: Add FAQ front matter to methodology

Update `content/methodology/_index.md` front matter:

```yaml
---
title: Methodology
faq:
  - q: "How does VisaFact verify insurance compliance?"
    a: "We compare official visa requirements (VisaFacts) against insurance product specifications (ProductFacts) using an automated rule engine. Every requirement must have evidence with source_id, locator, and excerpt."
  - q: "What do the status colors mean?"
    a: "GREEN means no violations detected. YELLOW means requirements met but with operational risks. RED means at least one requirement violated. UNKNOWN means insufficient evidence."
  - q: "Is this legal advice?"
    a: "No. VisaFact provides evidence-based compliance checking, not legal advice. Final visa decisions are made by government authorities."
  - q: "How often is the data updated?"
    a: "We monitor sources for changes and update records when official requirements change. Each record includes a last_verified date and SHA256 hash for integrity."
---
```

### Step 6: Run test to verify it passes

```bash
export PATH="$PWD/.bin:$PATH" && pwsh -NoProfile -File tools/tests/schema_faq_tests.ps1
```

### Step 7: Validate with Google Rich Results Test

```bash
# Manual step: test https://visafact.org/methodology/ with
# https://search.google.com/test/rich-results
```

### Step 8: Commit

```bash
git add layouts/partials/faq_schema.html layouts/partials/extend_head.html content/methodology/_index.md tools/tests/schema_faq_tests.ps1
git commit -m "feat: add FAQPage structured data for SEO"
```

---

## Task 3: WCAG 2.2 AA Accessibility Audit

**Rationale:** ADA lawsuits exceeded 4,000 in 2024. European Accessibility Act effective June 2025. Insurance is YMYL = higher scrutiny.

**Files:**
- Create: `tools/tests/accessibility_tests.ps1`
- Modify: `ui/index.html` (fix violations)

### Step 1: Write the failing test

Create `tools/tests/accessibility_tests.ps1`:

```powershell
$ErrorActionPreference = "Stop"
$failed = $false

function Assert-True {
  param([Parameter(Mandatory=$true)][bool]$Condition, [Parameter(Mandatory=$true)][string]$Message)
  if (-not $Condition) { Write-Host "FAIL: $Message" -ForegroundColor Red; $script:failed = $true }
  else { Write-Host "PASS: $Message" -ForegroundColor Green }
}

$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$ui = Get-Content -Raw -Path (Join-Path $root "ui/index.html")

# WCAG 2.4.1 - Bypass Blocks
Assert-True ($ui -match 'Skip to main content') "Has skip link (WCAG 2.4.1)"

# WCAG 1.3.1 - Info and Relationships
Assert-True ($ui -match '<main[^>]*id="main-content"') "Main content has id (WCAG 1.3.1)"
Assert-True ($ui -match '<nav') "Has nav element (WCAG 1.3.1)"
Assert-True ($ui -match '<header') "Has header element (WCAG 1.3.1)"
Assert-True ($ui -match '<footer') "Has footer element (WCAG 1.3.1)"

# WCAG 4.1.2 - Name, Role, Value
Assert-True ($ui -match 'aria-live') "Has aria-live region (WCAG 4.1.2)"
Assert-True ($ui -match 'aria-label') "Has aria-labels (WCAG 4.1.2)"

# WCAG 1.4.3 - Contrast (check for common low-contrast patterns)
Assert-True (-not ($ui -match 'text-gray-400(?!\s*dark:)')) "No light gray text without dark mode variant"

# WCAG 2.4.7 - Focus Visible
Assert-True ($ui -match 'focus:') "Has focus styles (WCAG 2.4.7)"
Assert-True ($ui -match 'focus:ring|focus:outline|focus:border') "Focus styles are visible"

# WCAG 3.2.2 - On Input
Assert-True (-not ($ui -match 'onchange="[^"]*submit')) "No auto-submit on change"

# Button accessibility
Assert-True (-not ($ui -match '<button[^>]*>(\s*<[^>]+>\s*)*</button>')) "Buttons have text content or aria-label"

if ($failed) { Write-Error "Accessibility checks failed."; exit 1 }
Write-Host "All checks passed." -ForegroundColor Green
```

### Step 2: Run test and identify failures

```bash
export PATH="$PWD/.bin:$PATH" && pwsh -NoProfile -File tools/tests/accessibility_tests.ps1
```

### Step 3: Fix identified violations

Common fixes:
- Add `aria-label` to icon-only buttons
- Ensure all interactive elements have visible focus states
- Add `role` attributes where semantic HTML insufficient
- Ensure color contrast meets 4.5:1 ratio

### Step 4: Run test to verify it passes

```bash
export PATH="$PWD/.bin:$PATH" && pwsh -NoProfile -File tools/tests/accessibility_tests.ps1
```

### Step 5: Commit

```bash
git add ui/index.html tools/tests/accessibility_tests.ps1
git commit -m "fix: improve WCAG 2.2 AA accessibility compliance"
```

---

## Task 4: Add visa country filter

**Rationale:** With 6 visas across multiple countries, users need quick filtering. Competitors offer search/filter functionality.

**Files:**
- Modify: `ui/index.html`
- Create: `tools/tests/filter_tests.ps1`

### Step 1: Write the failing test

Create `tools/tests/filter_tests.ps1`:

```powershell
$ErrorActionPreference = "Stop"
$failed = $false

function Assert-True {
  param([Parameter(Mandatory=$true)][bool]$Condition, [Parameter(Mandatory=$true)][string]$Message)
  if (-not $Condition) { Write-Host "FAIL: $Message" -ForegroundColor Red; $script:failed = $true }
  else { Write-Host "PASS: $Message" -ForegroundColor Green }
}

$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$ui = Get-Content -Raw -Path (Join-Path $root "ui/index.html")

# Filter UI elements
Assert-True ($ui -match 'id="countryFilter"|id="country-filter"') "Country filter element exists"
Assert-True ($ui -match '<option[^>]*value="ES"') "Spain option exists"
Assert-True ($ui -match '<option[^>]*value="PT"') "Portugal option exists"
Assert-True ($ui -match '<option[^>]*value="DE"') "Germany option exists"

# Filter function
Assert-True ($ui -match 'filterByCountry|filterVisas') "Filter function exists"

# Accessibility
Assert-True ($ui -match 'aria-label="[^"]*[Ff]ilter') "Filter has aria-label"

if ($failed) { Write-Error "Filter checks failed."; exit 1 }
Write-Host "All checks passed." -ForegroundColor Green
```

### Step 2: Run test to verify it fails

```bash
export PATH="$PWD/.bin:$PATH" && pwsh -NoProfile -File tools/tests/filter_tests.ps1
```

### Step 3: Implement country filter in UI

Add filter dropdown and JavaScript filtering logic to `ui/index.html`.

### Step 4: Run test to verify it passes

```bash
export PATH="$PWD/.bin:$PATH" && pwsh -NoProfile -File tools/tests/filter_tests.ps1
```

### Step 5: Commit

```bash
git add ui/index.html tools/tests/filter_tests.ps1
git commit -m "feat: add country filter for visa selection"
```

---

## Task 5: Add comparison view

**Rationale:** Nomadwise uses side-by-side comparison tables. Users want to compare products directly.

**Files:**
- Modify: `ui/index.html`
- Create: `tools/tests/comparison_tests.ps1`

### Step 1: Write the failing test

Create `tools/tests/comparison_tests.ps1`:

```powershell
$ErrorActionPreference = "Stop"
$failed = $false

function Assert-True {
  param([Parameter(Mandatory=$true)][bool]$Condition, [Parameter(Mandatory=$true)][string]$Message)
  if (-not $Condition) { Write-Host "FAIL: $Message" -ForegroundColor Red; $script:failed = $true }
  else { Write-Host "PASS: $Message" -ForegroundColor Green }
}

$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$ui = Get-Content -Raw -Path (Join-Path $root "ui/index.html")

# Comparison feature
Assert-True ($ui -match 'compare|comparison') "Comparison feature referenced"
Assert-True ($ui -match 'compareProducts|showComparison') "Comparison function exists"

# Comparison table structure
Assert-True ($ui -match 'comparison-table|compare-view') "Comparison table/view exists"

if ($failed) { Write-Error "Comparison checks failed."; exit 1 }
Write-Host "All checks passed." -ForegroundColor Green
```

### Step 2-5: Implement and verify

Follow same TDD pattern as previous tasks.

### Step 6: Commit

```bash
git add ui/index.html tools/tests/comparison_tests.ps1
git commit -m "feat: add product comparison view"
```

---

## Verification Checklist

Before claiming completion:

- [ ] All new tests pass
- [ ] `python3 tools/validate.py` passes
- [ ] `pwsh -File tools/tests/ui_compliance_tests.ps1` passes
- [ ] Hugo builds without errors
- [ ] Manual browser test of new features
- [ ] Google Rich Results Test validates FAQPage schema

---

## Rollout Notes

1. Price data requires evidence - use excerpts from product_facts.json
2. FAQ content must be accurate and match methodology page
3. Accessibility fixes should not break existing functionality
4. Filter/comparison are JS-only changes, no backend needed
