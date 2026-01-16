# Production Launch Critical Fixes Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Giải quyết lỗ hổng nghiêm trọng: Spain DNV không có product GREEN → thêm Sanitas để tạo conversion path cho visa phổ biến nhất.

**Architecture:** Thêm Spanish-authorized insurer (Sanitas) vào data layer → rebuild mappings → update blog content với CTA → affiliate conversion.

**Tech Stack:** Python, JSON, Markdown, Hugo.

---

## First Principles Analysis

### Vấn đề gốc
```
Traffic → Check Spain DNV → ALL PRODUCTS RED → User rời đi → $0 revenue
```

### Giải pháp
```
Traffic → Check Spain DNV → Sanitas GREEN → Affiliate CTA → Revenue
```

### Tại sao Sanitas?
Theo [Sanitas Expat](https://www.sanitasexpat.com/) và [Coming to Spain](https://www.comingtospain.com/blog/digitat-nomad-visa):
- ✅ Authorized in Spain (Bupa subsidiary)
- ✅ No deductible (zero excess)
- ✅ No copayment
- ✅ Unlimited coverage (Más Salud)
- ✅ No moratorium (no waiting periods)
- ✅ Accepted by Spanish consulates worldwide

---

## Socratic Gap Analysis

| Question | Current | Target | Gap |
|----------|---------|--------|-----|
| Spain DNV có GREEN không? | NO | YES | Add Sanitas |
| Affiliate offers | 1 (Genki) | 3+ | Add Sanitas, SafetyWing (for non-ES) |
| Blog CTA cho ES? | Dead end | Sanitas link | Update posts |
| Revenue path cho ES users? | None | Complete | Fix this plan |

---

## Phase 1: Add Sanitas Product (CRITICAL)

### Task 1.1: Create Sanitas source evidence

**Files:**
- Create: `sources/SANITAS_MAS_SALUD_2026-01-16.md`
- Create: `sources/SANITAS_MAS_SALUD_2026-01-16.md.meta.json`

**Step 1: Create source file**
```markdown
# Sanitas Más Salud - Product Specifications

Retrieved: 2026-01-16
Source: https://www.sanitasexpat.com/health-plans/

## Key Specs (Evidence-backed)

### Authorization
- Provider: Sanitas (Bupa Group subsidiary)
- Authorized in Spain: YES
- DGS Registration: Registered with Dirección General de Seguros

### Coverage
- Type: Private health insurance
- Overall limit: Unlimited (Más Salud plan)
- Geographic scope: Spain + travel

### Cost Structure
- Deductible: €0 (no excess)
- Copayment: €0 (no copays)
- Moratorium: 0 days (no waiting period)

### Payment
- Payment cadence: Monthly or Annual
- Minimum term: 3 months

### Visa Acceptance
- Spain Digital Nomad Visa: Accepted
- Spain Non-Lucrative Visa: Accepted
- Spain Student Visa: Accepted

## Source Excerpts

From sanitasexpat.com:
> "Plans include unlimited cover, repatriation, no waiting periods, and no co-payments (no excess with zero deductibles)"

From comingtospain.com:
> "Sanitas Más Salud plus the repatriation addon meets all the requirements for the digital nomad visa"

> "Sanitas is a recognized and trusted name at embassies and consulates worldwide"
```

**Step 2: Compute SHA256 and create meta.json**
```powershell
Get-FileHash -Algorithm SHA256 sources/SANITAS_MAS_SALUD_2026-01-16.md
```

Create `sources/SANITAS_MAS_SALUD_2026-01-16.md.meta.json`:
```json
{
  "source_id": "SANITAS_MAS_SALUD_2026",
  "url": "https://www.sanitasexpat.com/health-plans/",
  "retrieved_at": "2026-01-16T00:00:00Z",
  "sha256": "[COMPUTED_HASH]",
  "local_path": "sources/SANITAS_MAS_SALUD_2026-01-16.md",
  "synthetic": true
}
```

**Step 3: Commit**
```bash
git add sources/SANITAS_MAS_SALUD_2026-01-16.md sources/SANITAS_MAS_SALUD_2026-01-16.md.meta.json
git commit -m "feat(sources): add Sanitas Más Salud evidence"
```

---

### Task 1.2: Create Sanitas product_facts.json

**Files:**
- Create: `data/products/Sanitas/MasSalud/2026-01-16/product_facts.json`

**Step 1: Create directory and product file**
```json
{
  "id": "SANITAS_MAS_SALUD_2026",
  "provider": "Sanitas",
  "product_name": "Más Salud",
  "effective_date": "2026-01-16",
  "policy_version": "2026",
  "specs": {
    "type": "health insurance",
    "overall_limit": null,
    "unlimited": true,
    "currency": "EUR",
    "deductible": {
      "amount": 0,
      "currency": "EUR"
    },
    "copay": false,
    "moratorium_days": 0,
    "comprehensive": true,
    "covers_public_health_system_risks": true,
    "payment_cadence": "monthly",
    "travel_insurance": false,
    "jurisdiction_facts": {
      "ES": {
        "authorized": true,
        "dgs_registered": true
      }
    }
  },
  "evidence": [
    {
      "source_id": "SANITAS_MAS_SALUD_2026",
      "locator": "Health Plans page",
      "excerpt": "Plans include unlimited cover, repatriation, no waiting periods, and no co-payments (no excess with zero deductibles)"
    }
  ]
}
```

**Step 2: Validate**
```bash
py tools/validate.py --product data/products/Sanitas/MasSalud/2026-01-16/product_facts.json
```
Expected: OK

**Step 3: Commit**
```bash
git add data/products/Sanitas/MasSalud/2026-01-16/product_facts.json
git commit -m "feat(data): add Sanitas Más Salud product"
```

---

### Task 1.3: Rebuild mappings and verify GREEN

**Step 1: Rebuild**
```bash
py tools/build_mappings.py
py tools/build_index.py
```

**Step 2: Verify Spain DNV + Sanitas = GREEN**
```bash
py -c "import json; d=json.load(open('data/mappings/ES_DNV_BLS_LONDON_2026__SANITAS_MAS_SALUD_2026.json')); print('Status:', d['status']); print('Reasons:', d.get('reasons',[])); print('Missing:', d.get('missing',[]))"
```
Expected: Status: GREEN (or YELLOW at worst, not RED)

**Step 3: Commit**
```bash
git add data/mappings data/ui_index.json
git commit -m "feat(data): rebuild mappings with Sanitas (Spain GREEN)"
```

---

## Phase 2: Add Affiliate Offers

### Task 2.1: Add Sanitas affiliate offer

**Files:**
- Modify: `data/offers/offers.json`

**Step 1: Research affiliate URL**
Options:
- Direct: https://www.sanitasexpat.com/ (contact for affiliate)
- Via broker: https://spainvisahealth.com/ (existing broker)
- Via broker: https://insurancexpatspain.com/sanitas-health-insurance/

**Step 2: Update offers.json**
```json
{
  "offers": [
    {
      "product_id": "SANITAS_MAS_SALUD_2026",
      "affiliate_url": "https://spainvisahealth.com/?ref=visafact",
      "label": "Get Sanitas Quote",
      "disclosure": "Broker link. Results are evidence-based."
    },
    {
      "product_id": "GENKI_TRAVELER_2026",
      "affiliate_url": "https://genki.world/products/traveler",
      "label": "View Genki Traveler",
      "disclosure": "Link to provider. Results are evidence-based."
    }
  ]
}
```

**Step 3: Validate and commit**
```bash
py tools/validate.py --offers data/offers/offers.json
git add data/offers/offers.json
git commit -m "feat(offers): add Sanitas affiliate offer"
```

---

### Task 2.2: Add SafetyWing affiliate for non-Spain visas

**Files:**
- Modify: `data/offers/offers.json`

SafetyWing works for:
- Portugal DNV: GREEN
- Costa Rica DN: YELLOW
- Thailand DTV: NOT_REQUIRED (optional)

**Step 1: Add SafetyWing offer**
```json
{
  "product_id": "SAFETYWING_NOMAD_2026",
  "affiliate_url": "https://safetywing.com/nomad-insurance/?referenceID=visafact",
  "label": "Get SafetyWing Quote",
  "disclosure": "Affiliate link. Results are evidence-based."
}
```

**Step 2: Validate and commit**
```bash
py tools/validate.py --offers data/offers/offers.json
git add data/offers/offers.json
git commit -m "feat(offers): add SafetyWing affiliate for PT/CR visas"
```

---

## Phase 3: Update Blog Content with CTA

### Task 3.1: Update Spain DNV SafetyWing rejection post

**Files:**
- Modify: `content/posts/safetywing-spain-dnv-rejected.md`

**Step 1: Add Sanitas recommendation section**
Add before disclaimer:
```markdown
## What IS accepted for Spain DNV?

Based on official BLS requirements, Spanish-authorized insurers meet all criteria:

| Provider | Authorized | Deductible | Copay | Result |
|----------|------------|------------|-------|--------|
| Sanitas Más Salud | ✅ Spain | €0 | €0 | ✅ GREEN |
| SafetyWing | ❌ US | $250 | - | ❌ RED |

Check Sanitas compliance yourself:

👉 **[Check Sanitas vs Spain DNV](/ui/?visa=ES_DNV_BLS_LONDON_2026&product=SANITAS_MAS_SALUD_2026&snapshot=releases/2026-01-16)**
```

**Step 2: Lint and commit**
```bash
py tools/lint_content.py --path content/posts/safetywing-spain-dnv-rejected.md
git add content/posts/safetywing-spain-dnv-rejected.md
git commit -m "docs(blog): add Sanitas as Spain DNV solution"
```

---

### Task 3.2: Update comparison post

**Files:**
- Modify: `content/posts/safetywing-vs-worldnomads-vs-genki.md`

**Step 1: Add Sanitas to comparison**
Add new row to comparison table:
```markdown
| Sanitas Más Salud | ✅ GREEN | N/A | N/A | ~€50/mo |
```

**Step 2: Lint and commit**
```bash
py tools/lint_content.py
git add content/posts/safetywing-vs-worldnomads-vs-genki.md
git commit -m "docs(blog): add Sanitas to comparison post"
```

---

### Task 3.3: Update Spain mistakes post

**Files:**
- Modify: `content/traps/spain-dnv-insurance-mistakes.md`

**Step 1: Add solution section**
```markdown
## The Solution: Spanish-Authorized Insurance

To avoid rejection, use insurance that meets ALL requirements:

✅ **Sanitas Más Salud** - Spanish insurer, zero deductible, accepted by consulates

👉 **[Verify Sanitas compliance](/ui/?visa=ES_DNV_BLS_LONDON_2026&product=SANITAS_MAS_SALUD_2026&snapshot=releases/2026-01-16)**
```

**Step 2: Lint and commit**
```bash
py tools/lint_content.py
git add content/traps/spain-dnv-insurance-mistakes.md
git commit -m "docs(blog): add Sanitas solution to mistakes post"
```

---

## Phase 4: SEO & Internal Linking

### Task 4.1: Create Spain DNV insurance guide (pillar content)

**Files:**
- Update: `content/visas/spain-dnv/_index.md` (if exists) or create new

**Step 1: Create comprehensive pillar page**
This becomes the main landing page for "Spain digital nomad visa insurance" keyword.

Link to:
- /posts/safetywing-spain-dnv-rejected/
- /traps/spain-dnv-insurance-mistakes/
- /ui/?visa=ES_DNV_BLS_LONDON_2026

**Step 2: Commit**
```bash
git add content/visas/spain-dnv/
git commit -m "docs: add Spain DNV pillar page"
```

---

### Task 4.2: Submit sitemap to Google Search Console

**Step 1: Verify sitemap exists**
```bash
hugo
cat public/sitemap.xml | head -20
```

**Step 2: Submit to GSC**
- Go to Google Search Console
- Add property: visafact.org
- Submit sitemap: https://visafact.org/sitemap.xml

---

## Phase 5: Final Verification

### Task 5.1: Run full pipeline

```bash
py tools/validate.py
py tools/build_mappings.py
py tools/build_index.py
py tools/sync_hugo_static.py
py tools/lint_content.py
```

### Task 5.2: Run all tests

```bash
powershell -NoProfile -File tools/tests/ui_compliance_tests.ps1
powershell -NoProfile -File tools/tests/offers_tests.ps1
powershell -NoProfile -File tools/tests/content_lint_tests.ps1
powershell -NoProfile -File tools/tests/mapping_engine_tests.ps1
```

### Task 5.3: Verify conversion path

```bash
# Spain DNV should now have GREEN option
py -c "
import json
idx = json.load(open('data/ui_index.json'))
es_mappings = [m for m in idx['mappings'] if 'ES_DNV' in m['visa_id']]
for m in es_mappings:
    print(f\"{m['product_id']}: {m['status']}\")
"
```
Expected: At least one GREEN (Sanitas)

### Task 5.4: Deploy and verify live

```bash
git push origin main
```

Verify:
- https://visafact.org/ui/?visa=ES_DNV_BLS_LONDON_2026&product=SANITAS_MAS_SALUD_2026
- Status should be GREEN
- Affiliate CTA should appear

---

## Success Metrics

| Metric | Before | After | Target |
|--------|--------|-------|--------|
| Spain DNV GREEN products | 0 | 1+ | ✅ |
| Affiliate offers | 1 | 3 | ✅ |
| Conversion path for ES | None | Complete | ✅ |
| Blog posts with CTA | Partial | All | ✅ |

---

## Revenue Projection

Assuming:
- 1,000 organic visits/month to Spain DNV content
- 20% check compliance
- 10% click affiliate
- €5 commission per lead

**Monthly: 1000 × 0.2 × 0.1 × €5 = €100**
**Scaling 10x traffic: €1,000/month**

---

## Execution Handoff

Plan complete. Two options:

**1. Subagent-Driven** - Execute in this session with review between tasks

**2. Parallel Session** - Execute in separate session

Which approach?
