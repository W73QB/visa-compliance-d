# Production Readiness Plan - VisaFact

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Transform VisaFact from MVP to production-ready platform with complete rule engine, comprehensive data, robust testing, and operational excellence.

**Architecture:** Evidence-based compliance checker using Hugo static site + JSON data layer + Python rule engine + PowerShell tests + GitHub Actions CI/CD.

**Tech Stack:** Python 3.11, PowerShell, Hugo (PaperMod), GitHub Actions, JSON Schema, Tailwind CSS.

---

## First Principles Analysis (Elon Musk)

### What is the fundamental purpose?
- Help users verify if their insurance meets official visa requirements
- Based ONLY on evidence from primary sources
- No source = UNKNOWN (better than wrong)

### What are the irreducible components?
1. **Data Layer** - Visa requirements + Product specs + Evidence sources
2. **Rule Engine** - Logical evaluation of requirements vs specs
3. **UI** - Present results clearly with evidence links
4. **Trust** - Disclaimers, source verification, no marketing claims

### What assumptions should we question?
- Is the rule engine complete? **NO** - missing rules for authorized_in_spain, comprehensive, covers_public_health_system_risks, unlimited_coverage, no_copayment, no_moratorium
- Is the data sufficient? **NO** - only 4 visas, 2 products
- Is the UI production-ready? **MOSTLY** - needs accessibility audit, performance optimization

---

## Socratic Critical Analysis

| Question | Current State | Gap |
|----------|---------------|-----|
| Does the rule engine evaluate ALL requirements? | Only 5/11 requirement types | 6 missing rules |
| Are all visa requirements evidence-backed? | Yes | None |
| Can users verify every claim? | Yes via source links | None |
| Is the deployment process reliable? | Yes with smoke tests | Minor improvements |
| Is the site legally protected? | Has disclaimers | Need legal review |
| Can we add new visas/products easily? | Yes via JSON | None |
| Do we know when sources change? | source_monitor exists | Need alerting |

---

## Phase 1: Rule Engine Completion (Critical)

### Task 1.1: Add missing rule - insurance.authorized_in_spain

**Files:**
- Modify: `tools/build_mappings.py:54-68`
- Create: `tools/tests/mapping_engine_tests.ps1`

**Step 1: Write the failing test**
Create `tools/tests/mapping_engine_tests.ps1`:
```powershell
$ErrorActionPreference = "Stop"
$failed = $false

function Assert-True {
  param([bool]$Condition, [string]$Message)
  if (-not $Condition) {
    Write-Host "FAIL: $Message" -ForegroundColor Red
    $script:failed = $true
  } else {
    Write-Host "PASS: $Message" -ForegroundColor Green
  }
}

Write-Host "Mapping engine rule tests..." -ForegroundColor Cyan

# Run build_mappings and check output
$proc = Start-Process -FilePath "py" -ArgumentList "tools/build_mappings.py" -Wait -PassThru -NoNewWindow
Assert-True ($proc.ExitCode -eq 0) "build_mappings.py runs successfully"

# Check Spain DNV vs SafetyWing mapping has RED status (unauthorized)
$mapping = Get-Content "data/mappings/ES_DNV_BLS_LONDON_2026__SAFETYWING_NOMAD_2026.json" | ConvertFrom-Json
Assert-True ($mapping.status -eq "RED") "SafetyWing unauthorized in Spain produces RED"

# Check reasons contain authorization failure
$hasAuthReason = $mapping.reasons | Where-Object { $_.text -like "*authorized*" }
Assert-True ($null -ne $hasAuthReason) "Mapping includes authorization failure reason"

if ($failed) {
  Write-Error "One or more checks failed."
  exit 1
}

Write-Host "All checks passed." -ForegroundColor Green
```

**Step 2: Run test (expect FAIL)**
```bash
powershell -NoProfile -File tools/tests/mapping_engine_tests.ps1
```
Expected: FAIL - SafetyWing currently not flagged as unauthorized.

**Step 3: Implement authorized_in_spain rule in build_mappings.py**
Add after line 68 in `tools/build_mappings.py`:
```python
    # Authorized to operate in jurisdiction
    req = get_req(visa, "insurance.authorized_in_spain")
    if req and req["value"] == True:
        country = visa.get("country", "").upper()[:2]
        if country == "ES":
            jf = product_spec(product, f"jurisdiction_facts.{country}.authorized")
            if jf is None:
                if status == "GREEN":
                    status = "UNKNOWN"
                missing.append(f"specs.jurisdiction_facts.{country}.authorized")
            elif jf == False:
                status = "RED"
                reasons.append({
                    "text": f"Insurer not authorized to operate in {visa.get('country', 'jurisdiction')}",
                    "evidence": req["evidence"]
                })
```

**Step 4: Run test (expect PASS)**
```bash
powershell -NoProfile -File tools/tests/mapping_engine_tests.ps1
```
Expected: PASS.

**Step 5: Commit**
```bash
git add tools/build_mappings.py tools/tests/mapping_engine_tests.ps1
git commit -m "feat(engine): add authorized_in_spain rule"
```

---

### Task 1.2: Add missing rule - insurance.comprehensive

**Files:**
- Modify: `tools/build_mappings.py`
- Modify: `tools/tests/mapping_engine_tests.ps1`

**Step 1: Add test case**
Append to `tools/tests/mapping_engine_tests.ps1`:
```powershell
# Test comprehensive requirement
# (Add when product has comprehensive: false)
```

**Step 2: Add rule to build_mappings.py**
```python
    # Comprehensive coverage
    req = get_req(visa, "insurance.comprehensive")
    if req and req["value"] == True:
        comprehensive = product_spec(product, "comprehensive")
        if comprehensive is None:
            # If not specified, cannot verify
            if status == "GREEN":
                status = "UNKNOWN"
            missing.append("specs.comprehensive")
```

**Step 3: Run test**
```bash
powershell -NoProfile -File tools/tests/mapping_engine_tests.ps1
```

**Step 4: Commit**
```bash
git add tools/build_mappings.py tools/tests/mapping_engine_tests.ps1
git commit -m "feat(engine): add comprehensive coverage rule"
```

---

### Task 1.3: Add missing rule - insurance.covers_public_health_system_risks

**Files:**
- Modify: `tools/build_mappings.py`
- Modify: `tools/tests/mapping_engine_tests.ps1`

**Step 1: Add test case**
Append to `tools/tests/mapping_engine_tests.ps1`:
```powershell
# ES DNV should become UNKNOWN if public health system risks coverage is missing
$mapping = Get-Content "data/mappings/ES_DNV_BLS_LONDON_2026__GENERIC_EXPAT_COMPLETE_2026.json" | ConvertFrom-Json
Assert-True ($mapping.status -eq "UNKNOWN") "Missing covers_public_health_system_risks yields UNKNOWN"
```

**Step 2: Add rule to build_mappings.py**
```python
    # Covers risks insured by public health system
    req = get_req(visa, "insurance.covers_public_health_system_risks")
    if req and req["value"] == True:
        covers = product_spec(product, "covers_public_health_system_risks")
        if covers is None:
            if status == "GREEN":
                status = "UNKNOWN"
            missing.append("specs.covers_public_health_system_risks")
        elif covers == False:
            status = "RED"
            reasons.append({
                "text": "Visa requires coverage of public health system risks",
                "evidence": req["evidence"]
            })
```

**Step 3: Run test**
```bash
powershell -NoProfile -File tools/tests/mapping_engine_tests.ps1
```

**Step 4: Commit**
```bash
git add tools/build_mappings.py tools/tests/mapping_engine_tests.ps1
git commit -m "feat(engine): add covers_public_health_system_risks rule"
```

---

### Task 1.4: Add missing rule - insurance.unlimited_coverage

**Files:**
- Modify: `tools/build_mappings.py`

**Step 1: Add rule**
```python
    # Unlimited coverage
    req = get_req(visa, "insurance.unlimited_coverage")
    if req and req["value"] == True:
        limit = product_spec(product, "overall_limit")
        unlimited = product_spec(product, "unlimited")
        if unlimited == True:
            pass  # OK
        elif limit is None and unlimited is None:
            if status == "GREEN":
                status = "UNKNOWN"
            missing.append("specs.overall_limit or specs.unlimited")
        elif unlimited == False or (limit is not None and limit < 10000000):
            status = "RED"
            reasons.append({
                "text": f"Unlimited coverage required, product has limit of {limit}",
                "evidence": req["evidence"]
            })
```

**Step 2: Run pipeline**
```bash
py tools/build_mappings.py
powershell -NoProfile -File tools/tests/mapping_engine_tests.ps1
```

**Step 3: Commit**
```bash
git add tools/build_mappings.py
git commit -m "feat(engine): add unlimited_coverage rule"
```

---

### Task 1.5: Add missing rule - insurance.no_copayment

**Files:**
- Modify: `tools/build_mappings.py`

**Step 1: Add rule**
```python
    # No co-payment
    req = get_req(visa, "insurance.no_copayment")
    if req and req["value"] == True:
        copay = product_spec(product, "copay")
        if copay is None:
            if status == "GREEN":
                status = "UNKNOWN"
            missing.append("specs.copay")
        elif copay == True:
            status = "RED"
            reasons.append({
                "text": "No co-payments required, product has co-payments",
                "evidence": req["evidence"]
            })
```

**Step 2: Run and commit**
```bash
py tools/build_mappings.py
git add tools/build_mappings.py
git commit -m "feat(engine): add no_copayment rule"
```

---

### Task 1.6: Add missing rule - insurance.no_moratorium

**Files:**
- Modify: `tools/build_mappings.py`

**Step 1: Add rule**
```python
    # No moratorium/waiting period
    req = get_req(visa, "insurance.no_moratorium")
    if req and req["value"] == True:
        moratorium = product_spec(product, "moratorium_days")
        if moratorium is None:
            if status == "GREEN":
                status = "UNKNOWN"
            missing.append("specs.moratorium_days")
        elif moratorium > 0:
            status = "RED"
            reasons.append({
                "text": f"No moratorium required, product has {moratorium} day waiting period",
                "evidence": req["evidence"]
            })
```

**Step 2: Run and commit**
```bash
py tools/build_mappings.py
git add tools/build_mappings.py
git commit -m "feat(engine): add no_moratorium rule"
```

---

## Phase 2: Data Expansion

### Task 2.1: Add Spain-authorized insurance product (GenericInsurer)

**Files:**
- Verify: `data/products/GenericInsurer/Expat-Complete/2026-01-12/product_facts.json`

**Step 1: Verify product has jurisdiction_facts.ES.authorized = true**
```bash
py -c "import json; d=json.load(open('data/products/GenericInsurer/Expat-Complete/2026-01-12/product_facts.json')); print(d.get('specs',{}).get('jurisdiction_facts',{}).get('ES',{}).get('authorized'))"
```
Expected: True (or add if missing)

**Step 2: Rebuild mappings and verify**
```bash
py tools/build_mappings.py
py tools/build_index.py
```

**Step 3: Verify mapping status**
```bash
py -c "import json; d=json.load(open('data/mappings/ES_DNV_BLS_LONDON_2026__GENERIC_EXPAT_COMPLETE_2026.json')); print(d['status'])"
```
Expected: GREEN or YELLOW (not RED due to authorization)

---

### Task 2.2: Add Portugal Digital Nomad Visa

**Files:**
- Create: `data/visas/PT/DNV/vfs-london/2026-01-15/visa_facts.json`
- Create: `sources/PT_DNV_VFS_LONDON_checklist_2026-01-15.pdf` (or .md for synthetic)
- Create: `sources/PT_DNV_VFS_LONDON_checklist_2026-01-15.pdf.meta.json`

**Step 1: Research requirements**
Portugal D7/Digital Nomad visa requires:
- Health insurance valid in Portugal
- Minimum coverage (verify amount)
- Duration covering stay

**Step 2: Create visa_facts.json**
```json
{
  "id": "PT_DNV_VFS_LONDON_2026",
  "country": "Portugal",
  "visa_name": "Digital Nomad Visa",
  "route": "VFS London",
  "authority": "VFS Global London",
  "last_verified": "2026-01-15",
  "sources": [
    {
      "source_id": "VFS_PT_DNV_LONDON_2026",
      "url": "https://visa.vfsglobal.com/gbr/en/prt",
      "retrieved_at": "2026-01-15T00:00:00Z",
      "sha256": "[compute after creating source file]",
      "local_path": "sources/PT_DNV_VFS_LONDON_checklist_2026-01-15.md"
    }
  ],
  "requirements": [
    {
      "key": "insurance.mandatory",
      "op": "==",
      "value": true,
      "evidence": [
        {
          "source_id": "VFS_PT_DNV_LONDON_2026",
          "locator": "Requirements section",
          "excerpt": "Health insurance covering the duration of stay"
        }
      ]
    }
  ]
}
```

**Step 3: Create source file and meta.json**

**Step 4: Validate and commit**
```bash
py tools/validate.py --visa data/visas/PT/DNV/vfs-london/2026-01-15/visa_facts.json
git add data/visas/PT sources/PT_*
git commit -m "feat(data): add Portugal DNV visa facts"
```

---

### Task 2.3: Add Germany Freelance Visa

**Files:**
- Create: `data/visas/DE/FREELANCE/embassy-london/2026-01-15/visa_facts.json`
- Create: `sources/DE_FREELANCE_EMBASSY_LONDON_2026-01-15.md` (or official PDF)
- Create: `sources/DE_FREELANCE_EMBASSY_LONDON_2026-01-15.md.meta.json`

**Step 1: Research requirements (official source only)**
Capture the official embassy/VFS checklist and save to `sources/`.

**Step 2: Create visa_facts.json** (mirror structure from Task 2.2)

**Step 3: Create source file and meta.json**
Compute SHA256:
```powershell
Get-FileHash -Algorithm SHA256 sources/DE_FREELANCE_EMBASSY_LONDON_2026-01-15.md
```
Update meta with `source_id`, `sha256`, `local_path`.

**Step 4: Validate and commit**
```bash
py tools/validate.py --visa data/visas/DE/FREELANCE/embassy-london/2026-01-15/visa_facts.json
git add data/visas/DE sources/DE_*
git commit -m "feat(data): add Germany freelance visa facts"
```

---

### Task 2.4: Add World Nomads product

**Files:**
- Create: `data/products/WorldNomads/Explorer/2026-01-15/product_facts.json`
- Create: `sources/WORLDNOMADS_EXPLORER_2026.md`
- Create: `sources/WORLDNOMADS_EXPLORER_2026.md.meta.json`

**Step 1: Research product specs from official source**

**Step 2: Create product_facts.json with all required fields**

**Step 3: Create meta.json**
Compute SHA256:
```powershell
Get-FileHash -Algorithm SHA256 sources/WORLDNOMADS_EXPLORER_2026.md
```

**Step 4: Validate and commit**
```bash
py tools/validate.py --product data/products/WorldNomads/Explorer/2026-01-15/product_facts.json
git add data/products/WorldNomads sources/WORLDNOMADS_*
git commit -m "feat(data): add World Nomads Explorer product"
```

---

## Phase 3: UI/UX Production Hardening

### Task 3.1: Add structured data (JSON-LD) for SEO

**Files:**
- Modify: `ui/index.html`

**Step 1: Add JSON-LD schema in head**
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebApplication",
  "name": "VisaFact Compliance Checker",
  "description": "Evidence-based visa insurance compliance verification",
  "applicationCategory": "FinanceApplication",
  "operatingSystem": "Web",
  "offers": {
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "USD"
  }
}
</script>
```

**Step 2: Add test to ui_compliance_tests.ps1**
```powershell
$uiHtml = Get-Content -Raw -Path "ui/index.html"
Assert-True ($uiHtml -like '*application/ld+json*') "UI has structured data"
```

**Step 3: Run test and commit**
```bash
powershell -NoProfile -File tools/tests/ui_compliance_tests.ps1
git add ui/index.html tools/tests/ui_compliance_tests.ps1
git commit -m "feat(ui): add JSON-LD structured data for SEO"
```

---

### Task 3.2: Add accessibility ARIA labels

**Files:**
- Modify: `ui/index.html`

**Step 1: Add aria-label to interactive elements**
- Select dropdowns: `aria-label="Select visa type"`
- Buttons: `aria-label` already on some, verify all
- Results area: `aria-live="polite"`

**Step 2: Add test**
```powershell
Assert-True ($uiHtml -like '*aria-live*') "UI has aria-live region"
```

**Step 3: Commit**
```bash
git add ui/index.html tools/tests/ui_compliance_tests.ps1
git commit -m "feat(ui): improve accessibility with ARIA labels"
```

---

### Task 3.3: Add skip-to-content link

**Files:**
- Modify: `ui/index.html`

**Step 1: Add skip link at top of body**
```html
<a href="#main-content" class="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 bg-primary text-white px-4 py-2 rounded z-50">
  Skip to main content
</a>
```

**Step 2: Add id="main-content" to main element**

**Step 3: Commit**
```bash
git add ui/index.html
git commit -m "feat(ui): add skip-to-content link for accessibility"
```

---

### Task 3.4: Add error boundary for fetch failures

**Files:**
- Modify: `ui/index.html`

**Step 1: Improve error handling in init()**
Already has try/catch - verify it shows user-friendly message.

**Step 2: Add retry button**
```javascript
$("loadingState").innerHTML = `
  <div class="text-center py-8">
    <span class="material-symbols-outlined text-error-red text-4xl mb-2">error</span>
    <p class="text-error-red font-medium">Failed to load data</p>
    <p class="text-text-secondary text-sm mt-1">Please check your connection.</p>
    <button onclick="location.reload()" class="mt-4 px-4 py-2 bg-primary text-white rounded">
      Retry
    </button>
  </div>
`;
```

**Step 3: Commit**
```bash
git add ui/index.html
git commit -m "feat(ui): add retry button on fetch failure"
```

---

## Phase 4: Content & Trust Building

### Task 4.1: Create comprehensive methodology page

**Files:**
- Modify: `content/methodology/_index.md`

**Step 1: Expand methodology to cover**
- How requirements are extracted from sources
- How the rule engine evaluates compliance
- What each status means (GREEN/YELLOW/RED/UNKNOWN/NOT_REQUIRED)
- How evidence is stored and verified
- SHA256 hash verification process

**Step 2: Lint and commit**
```bash
py tools/lint_content.py --path content/methodology/_index.md
git add content/methodology/_index.md
git commit -m "docs: expand methodology page"
```

---

### Task 4.2: Add "How to read results" guide

**Files:**
- Create: `content/guides/how-to-read-results.md`

**Step 1: Create guide with required sections**
Include: what the authority requires, how we evaluate, check in the engine, disclaimer, affiliate disclosure, snapshot= link

**Step 2: Lint and commit**
```bash
py tools/lint_content.py --path content/guides/how-to-read-results.md
git add content/guides/how-to-read-results.md
git commit -m "docs: add how to read results guide"
```

---

### Task 4.3: Add Costa Rica DNV blog post

**Files:**
- Create: `content/posts/costa-rica-dn-insurance.md`

**Step 1: Create post following template**
Copy from `content/templates/compliance-post-template.md`

**Step 2: Lint and commit**
```bash
py tools/lint_content.py
git add content/posts/costa-rica-dn-insurance.md
git commit -m "docs: add Costa Rica DN insurance post"
```

---

### Task 4.4: Add Malta Nomad Residence blog post

**Files:**
- Create: `content/posts/malta-nomad-insurance.md`

(Similar to Task 4.3)

---

## Phase 5: Operational Excellence

### Task 5.1: Add source freshness monitoring

**Files:**
- Verify: `tools/check_source_changes.py` exists and works

**Step 1: Review current implementation**
```bash
py tools/check_source_changes.py --help
```

**Step 2: Add scheduled workflow**
Create `.github/workflows/source-monitor.yml`:
```yaml
name: Monitor Sources

on:
  schedule:
    - cron: '0 9 * * 1'  # Weekly on Monday 9am UTC
  workflow_dispatch:

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Check sources
        run: python tools/check_source_changes.py
```

**Step 3: Commit**
```bash
git add .github/workflows/source-monitor.yml
git commit -m "ci: add weekly source freshness monitoring"
```

---

### Task 5.2: Add Dependabot for security updates

**Files:**
- Create: `.github/dependabot.yml`

**Step 1: Create dependabot config**
```yaml
version: 2
updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
```

**Step 2: Commit**
```bash
git add .github/dependabot.yml
git commit -m "ci: add Dependabot for security updates"
```

---

### Task 5.3: Add CONTRIBUTING.md

**Files:**
- Create: `CONTRIBUTING.md`

**Step 1: Document contribution process**
- How to add a new visa
- How to add a new product
- How to update sources
- Testing requirements
- Commit message format

**Step 2: Commit**
```bash
git add CONTRIBUTING.md
git commit -m "docs: add CONTRIBUTING.md"
```

---

### Task 5.4: Add SECURITY.md

**Files:**
- Create: `SECURITY.md`

**Step 1: Document security policy**
- How to report vulnerabilities
- Supported versions
- Response timeline

**Step 2: Commit**
```bash
git add SECURITY.md
git commit -m "docs: add SECURITY.md"
```

---

## Phase 6: Performance & Analytics

### Task 6.1: Add performance budget test

**Files:**
- Create: `tools/tests/performance_tests.ps1`

**Step 1: Create performance test**
```powershell
$ErrorActionPreference = "Stop"
$failed = $false

function Assert-True {
  param([bool]$Condition, [string]$Message)
  if (-not $Condition) {
    Write-Host "FAIL: $Message" -ForegroundColor Red
    $script:failed = $true
  } else {
    Write-Host "PASS: $Message" -ForegroundColor Green
  }
}

Write-Host "Performance budget tests..." -ForegroundColor Cyan

# ui/index.html should be under 100KB
$uiSize = (Get-Item "ui/index.html").Length
Assert-True ($uiSize -lt 102400) "ui/index.html under 100KB ($uiSize bytes)"

# ui_index.json should be under 500KB
$indexSize = (Get-Item "data/ui_index.json").Length
Assert-True ($indexSize -lt 512000) "ui_index.json under 500KB ($indexSize bytes)"

if ($failed) {
  Write-Error "One or more checks failed."
  exit 1
}

Write-Host "All checks passed." -ForegroundColor Green
```

**Step 2: Add to CI**
Add to `.github/workflows/pages.yml`:
```yaml
powershell -NoProfile -File tools/tests/performance_tests.ps1
```

**Step 3: Commit**
```bash
git add tools/tests/performance_tests.ps1 .github/workflows/pages.yml
git commit -m "test: add performance budget tests"
```

---

### Task 6.2: Add privacy-first analytics placeholder

**Files:**
- Modify: `ui/index.html`

**Step 1: Add comment placeholder for analytics**
```html
<!-- Privacy-first analytics: Add Plausible/Fathom/SimpleAnalytics here if needed -->
<!-- Example: <script defer data-domain="visafact.org" src="https://plausible.io/js/script.js"></script> -->
```

**Step 2: Commit**
```bash
git add ui/index.html
git commit -m "chore: add analytics placeholder comment"
```

---

## Phase 7: Final Verification

### Task 7.1: Run full pipeline locally

**Step 1: Execute all commands**
```bash
py tools/validate.py
py tools/build_mappings.py
py tools/build_index.py
py tools/sync_hugo_static.py
py tools/lint_content.py
```

**Step 2: Run all tests**
```bash
powershell -NoProfile -File tools/tests/ui_compliance_tests.ps1
powershell -NoProfile -File tools/tests/validate_product_sources_tests.ps1
powershell -NoProfile -File tools/tests/snapshot_tests.ps1
powershell -NoProfile -File tools/tests/snapshot_routing_tests.ps1
powershell -NoProfile -File tools/tests/release_snapshot_tests.ps1
powershell -NoProfile -File tools/tests/verify_snapshot_manifest_tests.ps1
powershell -NoProfile -File tools/tests/offers_tests.ps1
powershell -NoProfile -File tools/tests/content_lint_tests.ps1
powershell -NoProfile -File tools/tests/source_monitor_tests.ps1
powershell -NoProfile -File tools/tests/hugo_integration_tests.ps1
powershell -NoProfile -File tools/tests/sync_hugo_static_tests.ps1
powershell -NoProfile -File tools/tests/verify_static_bundle_tests.ps1
powershell -NoProfile -File tools/tests/smoke_tests.ps1
powershell -NoProfile -File tools/tests/mapping_engine_tests.ps1
powershell -NoProfile -File tools/tests/performance_tests.ps1
```

**Step 3: Build Hugo locally**
```bash
hugo server -D
```
Visit http://localhost:1313/ui/ and verify functionality.

---

### Task 7.2: Create release snapshot

**Step 1: Create release**
```bash
py tools/build_release_snapshot.py --release-id 2026-01-15
py tools/sync_hugo_static.py
```

**Step 2: Verify snapshot exists**
```bash
ls data/snapshots/releases/2026-01-15/
```

**Step 3: Do not commit snapshots**
Snapshots are generated artifacts; keep them local or store in a release artifact, per repo policy.

---

### Task 7.3: Deploy and verify

**Step 1: Push to main**
```bash
git push origin main
```

**Step 2: Monitor GitHub Actions**
Wait for build + deploy + post_deploy_smoke to pass.

**Step 3: Manual verification**
Visit https://visafact.org/ui/ and test:
- [ ] Spain DNV + SafetyWing = RED (unauthorized)
- [ ] Spain DNV + GenericInsurer = GREEN or YELLOW
- [ ] Thailand DTV = NOT_REQUIRED
- [ ] Deep link with snapshot works
- [ ] Evidence modal opens
- [ ] Mobile responsive

---

## Verification Checklist (per task)

Each task MUST pass these checks before marked complete:

- [ ] Test written FIRST (TDD)
- [ ] Test fails before implementation
- [ ] Implementation minimal
- [ ] Test passes after implementation
- [ ] No regressions (full test suite passes)
- [ ] Commit with proper prefix (feat/fix/test/docs/ci)
- [ ] Code reviewed (self or peer)

---

## Execution Handoff

Plan complete and saved to `docs/plans/2026-01-15-production-readiness-plan.md`.

Two execution options:

**1. Subagent-Driven (this session)** - I dispatch fresh subagent per task, review between tasks, fast iteration

**2. Parallel Session (separate)** - Open new session with executing-plans, batch execution with checkpoints

Which approach?
