# Phase 2: Content Depth Expansion Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Expand 5 top posts with evidence-backed depth, per-visa word count targets calibrated to available data, and updated SEO thresholds — without duplicating existing sections or violating project constraints.

**Architecture:** Each post already has 8-10 H2 sections from Phase 1. We expand existing sections with evidence from `visa_facts.json`, `product_facts.json`, and `mappings/*.json`. New sections are added only where data supports them (e.g., "Mapping results summary" using real GREEN/RED/UNKNOWN counts). Thresholds in `seo_thresholds.json` are raised to match new targets after content lands.

**Tech Stack:** Hugo + PaperMod, Python tools (`lint_content.py`, `seo_audit.py`), JSON data layer, PowerShell test scripts.

---

## Constraints (read before every task)

1. **Evidence-first:** No source = UNKNOWN. Never fabricate visa requirements or rejection anecdotes. Every factual claim must trace to `visa_facts.json`, `product_facts.json`, `mappings/*.json`, or files in `sources/`.
2. **Banned words:** Never use: `best`, `recommend`, `recommended`, `guarantee`, `guaranteed`, `100%`, `approved`, `surely`. Lint enforces this (`tools/lint_content.py:14-23`).
3. **Required sections (lint-enforced):** Every post must contain: "what the authority requires", "how we evaluate", "check in the engine", "disclaimer", "affiliate disclosure", and `snapshot=` in a deep link (`tools/lint_content.py:6-12,34`).
4. **Snapshot param:** Use the latest verified snapshot dates from existing posts. Spain uses `releases/2026-01-16`, others use `releases/2026-01-15`.
5. **Do not duplicate existing H2 sections.** Expand content *within* them or add new H2s only where data justifies it.
6. **Internal links:** Follow relevance, not quotas. Visa-specific posts link to their own route page + related guide/trap. Comparison post can link multiple visa pages.
7. **Do not modify:** `tools/lint_content.py`, `tools/seo_audit.py`, `tools/build_content_hubs.py`, anything in `data/`, anything in `sources/`.

## Evidence inventory (reference data)

### Requirements per visa

| Visa ID | Requirements | Key fields |
|---|---|---|
| ES_DNV_BLS_LONDON_2026 | **8** | mandatory, authorized_in_spain, covers_public_health, comprehensive, unlimited_coverage, no_deductible, no_copayment, no_moratorium |
| DE_FREELANCE_EMBASSY_LONDON_2026 | **2** | mandatory, travel_insurance_accepted=False |
| PT_DNV_VFS_CHINA_2026 | **1** | mandatory |
| CR_DN_DECREE_43619_2026 | **3** | mandatory, must_cover_full_period, min_coverage≥50000 |
| TH_DTV_MFA_2026 | **1** | mandatory=**False** |
| MT_NOMAD_RESIDENCY_2026 | **2** | mandatory, monthly_payments_accepted=False |

### Mapping results per visa (7 products each)

| Visa | GREEN | RED | YELLOW | UNKNOWN | NOT_REQUIRED |
|---|---|---|---|---|---|
| ES_DNV | 1 | 5 | 0 | 1 | 0 |
| DE_FREELANCE | 4 | 2 | 0 | 1 | 0 |
| PT_DNV | 7 | 0 | 0 | 0 | 0 |
| CR_DN | 2 | 0 | 1 | 4 | 0 |
| TH_DTV | 0 | 0 | 0 | 0 | 7 |
| MT_NOMAD | 2 | 1 | 0 | 4 | 0 |

### Products (for comparison post)

| ID | Provider | Product |
|---|---|---|
| ASISA_HEALTH_RESIDENTS_2026 | ASISA | Health Residents |
| DKV_VISADO_2026 | DKV | Visado |
| GENKI_TRAVELER_2026 | Genki | Traveler |
| SAFETYWING_NOMAD_2026 | SafetyWing | Nomad Insurance |
| SANITAS_MAS_SALUD_SIN_COPAGO_2026 | Sanitas | Mas Salud (Sin Copago) |
| WORLDNOMADS_EXPLORER_2026 | World Nomads | Explorer Plan |
| GENERIC_EXPAT_COMPLETE_2026 | GenericInsurer | Expat Complete Health |

### Word count targets (calibrated to evidence depth)

| Post | Current words | Evidence depth | Target | New threshold |
|---|---|---|---|---|
| spain-dnv-insurance.md | 322 | 8 requirements, 1G/5R/1U | **500–650** | 425 |
| safetywing-vs-worldnomads-vs-genki.md | 378 | 7 products × 6 visas | **550–800** | 470 |
| germany-freelance-insurance.md | 282 | 2 requirements, 4G/2R/1U | **350–450** | 300 |
| portugal-dnv-insurance.md | 275 | 1 requirement, 7G | **300–400** | 255 |
| thailand-dtv-insurance.md | 228 | mandatory=False, 7 NOT_REQUIRED | **280–370** | 240 |

Threshold formula: `new_threshold = floor(target_min * 0.85)` — 15% buffer below minimum target.

---

## Task 1: Expand Spain DNV post (target 500–650 words)

**Files:**
- Modify: `content/posts/spain-dnv-insurance.md`

Spain has 8 requirements and rich mapping data (5 RED, 1 GREEN, 1 UNKNOWN). This is the highest-evidence post.

**Step 1: Add "Mapping results summary" section**

Add a new H2 after "Current status in the checker" (line 26). This section presents real data from `data/mappings/ES_DNV_BLS_LONDON_2026__*.json`:

```markdown
## Mapping results summary

As of snapshot `releases/2026-01-16`, the checker evaluated 7 products against Spain DNV requirements:

| Status | Count | What it means |
|---|---|---|
| GREEN | 1 | All requirements verified by evidence |
| RED | 5 | At least one requirement fails based on evidence |
| UNKNOWN | 1 | Evidence missing for one or more requirements |

Only ASISA Health Residents achieves GREEN. Five products are marked RED due to at least one verified requirement mismatch (for example: deductible, co-payment, coverage limit, or authorization). One product lacks sufficient evidence and is marked UNKNOWN.
```

**Step 2: Expand "What the authority requires" section**

The current section (line 15-17) is 1 paragraph, 55 words. Expand it to list all 8 requirements explicitly:

Replace the single paragraph with:

```markdown
## What the authority requires

Spain Digital Nomad Visa (BLS London route) requires health insurance meeting all of the following conditions, based on the BLS checklist (page 2, item 9) stored in `sources/ES_DNV_BLS_LONDON_checklist_2026-01-12.pdf`:

- **Mandatory:** Insurance is required for all applicants.
- **Authorized in Spain:** The insurer must be authorized to operate in Spain.
- **Covers public health system risks:** The policy must cover risks insured by the Spanish public health system.
- **Comprehensive:** Full coverage, not travel-only or emergency-only.
- **Unlimited coverage:** No annual or per-incident cap.
- **No deductible:** Zero deductible (excess) allowed.
- **No co-payment:** Zero co-payment allowed.
- **No moratorium:** No waiting period before coverage begins.

Failing any single requirement produces a RED status in the checker.
```

**Step 3: Expand "Common pitfalls" section**

Add 2 evidence-backed bullet points to existing list (line 37-40). Avoid duplicating the existing “monthly payment” pitfall:

```markdown
## Common pitfalls

- Buying travel-only policies when a full health policy is required.
- Accepting deductibles or co-payments when the route requires zero.
- Paying monthly when a full annual policy is expected.
- Assuming coverage is "unlimited" when the policy document states a cap (e.g., $250,000). Spain DNV requires truly unlimited coverage.
- Using policies that do not show authorization to operate in Spain, which conflicts with the route's authorization requirement.
```

**Step 4: Run lint + SEO audit**

Run:
```bash
python3 tools/lint_content.py --path content/posts/spain-dnv-insurance.md
python3 tools/seo_audit.py --config tools/seo_thresholds.json
```

Expected: Both PASS (current threshold is 300, target content should be 500+ words).

**Step 5: Verify word count**

Run:
```bash
python3 -c "
import re
text = open('content/posts/spain-dnv-insurance.md').read().lstrip('\ufeff')
parts = text.split('---', 2)
body = parts[2]
words = len(re.findall(r'\b\w+\b', body))
print(f'Word count: {words}')
assert 500 <= words <= 650, f'Out of target range: {words}'
print('OK: within target 500-650')
"
```

Expected: Word count between 500-650.

**Step 6: Commit**

```bash
git add content/posts/spain-dnv-insurance.md
git commit -m "docs: expand Spain DNV post with mapping results and requirement details"
```

---

## Task 2: Expand comparison post (target 550–800 words)

**Files:**
- Modify: `content/posts/safetywing-vs-worldnomads-vs-genki.md`

This post compares 3 products but the system has 7. The mapping data spans 6 visas × 7 products = 42 results.

**Step 1: Add "Compliance snapshot across visas" section**

Add after "Evidence coverage notes" (line 53). This is the highest-value addition — a cross-visa compliance matrix using real mapping data:

```markdown
## Compliance snapshot across visas

The checker evaluates each product against every visa in the system. Below is a summary as of snapshot `releases/2026-01-15` for the three products compared in this post:

| Visa | SafetyWing | World Nomads | Genki |
|---|---|---|---|
| Spain DNV | RED | RED | RED |
| Germany Freelance | RED | RED | UNKNOWN |
| Portugal DNV | GREEN | GREEN | GREEN |
| Costa Rica DN | YELLOW | GREEN | GREEN |
| Thailand DTV | NOT_REQUIRED | NOT_REQUIRED | NOT_REQUIRED |
| Malta Nomad | RED | UNKNOWN | UNKNOWN |

**Reading this table:**
- **GREEN:** All requirements verified by evidence.
- **RED:** At least one requirement conflicts with evidence.
- **YELLOW:** Partial concern (e.g., monthly subscription for a full-period requirement).
- **UNKNOWN:** Evidence missing — cannot confirm or deny.
- **NOT_REQUIRED:** The visa does not require insurance.

No product achieves GREEN for Spain DNV except ASISA Health Residents (a Spanish insurer not shown above). This reflects the strict requirements: zero deductible, zero co-payment, unlimited coverage, and Spanish authorization.
```

**Step 2: Expand "Quick chooser" section**

Add route-specific guidance based on mapping data (line 47-49):

```markdown
## Quick chooser

Use this as a starting point — always verify with the checker.

- **Spain DNV route:** None of the three products above achieves GREEN. Consider a Spain-authorized insurer instead; check the engine for current GREEN options.
- **Portugal DNV route:** All three products achieve GREEN — Portugal's single requirement (mandatory insurance) is easily met.
- **Germany Freelance route:** SafetyWing and World Nomads are RED because Germany does not accept travel insurance. Look for health insurance (not travel insurance) and verify in the checker.
- **Costa Rica DN route:** World Nomads and Genki achieve GREEN. SafetyWing is YELLOW due to its monthly subscription model vs. the full-period coverage requirement.
- **Thailand DTV route:** Insurance is not required. All products show NOT_REQUIRED.
```

**Step 3: Add internal link to Malta**

In "Related reading" (line 57-62), add:

```markdown
- [Malta nomad insurance](/posts/malta-nomad-insurance/)
```

This is relevant because the comparison table now includes Malta.

**Step 4: Run lint + SEO audit**

```bash
python3 tools/lint_content.py --path content/posts/safetywing-vs-worldnomads-vs-genki.md
python3 tools/seo_audit.py --config tools/seo_thresholds.json
```

Expected: Both PASS.

**Step 5: Verify word count**

```bash
python3 -c "
import re
text = open('content/posts/safetywing-vs-worldnomads-vs-genki.md').read().lstrip('\ufeff')
parts = text.split('---', 2)
body = parts[2]
words = len(re.findall(r'\b\w+\b', body))
print(f'Word count: {words}')
assert 550 <= words <= 800, f'Out of target range: {words}'
print('OK: within target 550-800')
"
```

**Step 6: Commit**

```bash
git add content/posts/safetywing-vs-worldnomads-vs-genki.md
git commit -m "docs: expand comparison post with cross-visa compliance matrix"
```

---

## Task 3: Expand Germany Freelance post (target 350–450 words)

**Files:**
- Modify: `content/posts/germany-freelance-insurance.md`

Germany has only 2 requirements but a critical distinction: travel insurance is explicitly rejected.

**Step 1: Add "Mapping results summary" section**

Add after "Check in the engine" section. Data from `data/mappings/DE_FREELANCE_EMBASSY_LONDON_2026__*.json`:

```markdown
## Mapping results summary

As of snapshot `releases/2026-01-15`, the checker evaluated 7 products:

| Status | Count | Implication |
|---|---|---|
| GREEN | 4 | Insurance type confirmed as health (not travel) |
| RED | 2 | Product classified as travel insurance |
| UNKNOWN | 1 | Insurance type not confirmed by evidence |

The key differentiator is `travel_insurance_accepted = False`. Products classified as travel insurance (SafetyWing Nomad, World Nomads Explorer) are marked RED regardless of their coverage limits or deductibles.
```

**Step 2: Expand "What the authority requires"**

The current section is a single short paragraph. Expand:

```markdown
## What the authority requires

The German Embassy London requires health insurance for the freelance visa (national visa type D). Two requirements are verified by evidence:

1. **Mandatory:** Insurance is required for all applicants.
2. **Travel insurance not accepted:** The embassy explicitly rejects travel insurance policies. You need a health insurance policy (Krankenversicherung), not a travel medical policy.

Evidence is stored in `sources/DE_HEALTH_INSURANCE_REQUIREMENTS_2026-01-15.html`. The distinction between "travel insurance" and "health insurance" is the primary compliance gate for this route.
```

**Step 3: Expand "Common pitfalls"**

Add 1 evidence-backed bullet:

```markdown
- Submitting a travel insurance certificate when the embassy requires health insurance. Mapping results show 2 out of 7 evaluated products are RED because they are classified as travel insurance.
```

**Step 4: Run lint + SEO audit + word count check**

```bash
python3 tools/lint_content.py --path content/posts/germany-freelance-insurance.md
python3 tools/seo_audit.py --config tools/seo_thresholds.json
python3 -c "
import re
text = open('content/posts/germany-freelance-insurance.md').read().lstrip('\ufeff')
body = text.split('---', 2)[2]
words = len(re.findall(r'\b\w+\b', body))
print(f'Word count: {words}')
assert 350 <= words <= 450, f'Out of target range: {words}'
print('OK: within target 350-450')
"
```

**Step 5: Commit**

```bash
git add content/posts/germany-freelance-insurance.md
git commit -m "docs: expand Germany freelance post with mapping results and requirement detail"
```

---

## Task 4: Expand Portugal DNV post (target 300–400 words)

**Files:**
- Modify: `content/posts/portugal-dnv-insurance.md`

Portugal has only 1 requirement (`mandatory=true`) and all 7 products are GREEN. Content expansion must be honest about this simplicity. Do not introduce additional requirements (coverage limits, deductibles, payment cadence) unless they are in `visa_facts.json`.

**Step 1: Add "Mapping results summary" section**

Add after "Check in the engine":

```markdown
## Mapping results summary

As of snapshot `releases/2026-01-15`, the checker evaluated 7 products — all are GREEN:

| Status | Count |
|---|---|
| GREEN | 7 |

Portugal's single verified requirement is that insurance is mandatory. Because there are no constraints on coverage limits, deductibles, authorization jurisdiction, or payment cadence, all products in the system pass.

This does not mean Portugal has no preferences — it means the evidence we have only confirms the mandatory requirement. If additional requirements emerge from official sources, some products may shift to RED or UNKNOWN.
```

**Step 2: Expand "Common pitfalls"**

Add evidence-based warnings:

```markdown
- Assuming all GREEN means the policy is fully accepted. GREEN reflects current evidence only — Portugal authorities may request additional documents not yet captured in our sources.
- Not having documentation that shows active coverage. Even though all products pass the checker, you still need proof that your policy is active for your intended dates.
```

**Step 3: Run lint + SEO audit + word count check**

```bash
python3 tools/lint_content.py --path content/posts/portugal-dnv-insurance.md
python3 tools/seo_audit.py --config tools/seo_thresholds.json
python3 -c "
import re
text = open('content/posts/portugal-dnv-insurance.md').read().lstrip('\ufeff')
body = text.split('---', 2)[2]
words = len(re.findall(r'\b\w+\b', body))
print(f'Word count: {words}')
assert 300 <= words <= 400, f'Out of target range: {words}'
print('OK: within target 300-400')
"
```

**Step 4: Commit**

```bash
git add content/posts/portugal-dnv-insurance.md
git commit -m "docs: expand Portugal DNV post with mapping results and evidence caveats"
```

---

## Task 5: Expand Thailand DTV post (target 280–370 words)

**Files:**
- Modify: `content/posts/thailand-dtv-insurance.md`

Thailand DTV does NOT require insurance. All 7 products return NOT_REQUIRED. This post needs a fundamentally different approach: explain WHY it's not required and what risks remain.

**Step 1: Expand "What the authority requires"**

Replace the current single-sentence section:

```markdown
## What the authority requires

The official DTV required documents list (Thai MFA) does not include insurance. Evidence: Thai MFA DTV requirements captured in `sources/TH_DTV_MFA_requirements_2026-01-12.md`. Add one sentence noting that consulate requirements can vary and applicants should verify the current checklist for their filing location.

As a result, the checker returns **NOT_REQUIRED** for all 7 evaluated products. This means no product fails or passes — insurance is simply outside the scope of this visa's documented requirements.

Note: This reflects the evidence as of the last verification date. Thai authorities may update requirements without notice. Always confirm the current checklist before your appointment.
```

**Step 2: Add "Why NOT_REQUIRED matters" section**

Add after "Plain-English summary":

```markdown
## Why NOT_REQUIRED matters

When the checker returns NOT_REQUIRED, it means:

- The official documents list does **not** mention insurance.
- No product can be GREEN or RED because there is no requirement to evaluate against.
- Buying insurance is a personal risk decision, not a compliance requirement.

This is different from UNKNOWN (where a requirement exists but evidence is missing). NOT_REQUIRED means the authority has published a requirements list and insurance is not on it.
```

**Step 3: Expand "Common pitfalls"**

Add:

```markdown
- Confusing NOT_REQUIRED with "insurance is unnecessary." The visa does not require it, but medical costs in Thailand are your responsibility and can be significant without coverage.
```

**Step 4: Run lint + SEO audit + word count check**

```bash
python3 tools/lint_content.py --path content/posts/thailand-dtv-insurance.md
python3 tools/seo_audit.py --config tools/seo_thresholds.json
python3 -c "
import re
text = open('content/posts/thailand-dtv-insurance.md').read().lstrip('\ufeff')
body = text.split('---', 2)[2]
words = len(re.findall(r'\b\w+\b', body))
print(f'Word count: {words}')
assert 280 <= words <= 370, f'Out of target range: {words}'
print('OK: within target 280-370')
"
```

**Step 5: Commit**

```bash
git add content/posts/thailand-dtv-insurance.md
git commit -m "docs: expand Thailand DTV post with NOT_REQUIRED explanation and risk context"
```

---

## Task 6: Update SEO thresholds

**Files:**
- Modify: `tools/seo_thresholds.json`

Update thresholds AFTER all content tasks (1-5) are merged. New thresholds = `floor(target_min × 0.85)`.

**Step 1: Update thresholds**

In `tools/seo_thresholds.json`, change `min_word_count` values:

```json
{
  "min_word_count": {
    "default": 150,
    "content/posts/spain-dnv-insurance.md": 425,
    "content/posts/germany-freelance-insurance.md": 300,
    "content/posts/portugal-dnv-insurance.md": 255,
    "content/posts/thailand-dtv-insurance.md": 240,
    "content/posts/safetywing-vs-worldnomads-vs-genki.md": 470,
    "content/posts/digital-nomad-insurance-europe.md": 350,
    "content/posts/digital-nomad-insurance-asia.md": 250,
    "content/posts/digital-nomad-insurance-americas.md": 250,
    "content/posts/costa-rica-dn-insurance.md": 225,
    "content/guides/how-to-read-results.md": 150
  }
}
```

Changes: Spain 300→425, Germany 250→300, Portugal 250→255, Thailand 200→240, Comparison 350→470. Other values unchanged.

**Step 2: Run full SEO audit**

```bash
python3 tools/seo_audit.py --config tools/seo_thresholds.json
```

Expected: PASS (all 5 expanded posts should exceed their new thresholds).

**Step 3: Run full test suite**

```bash
python3 tools/lint_content.py
python3 tools/validate.py
python3 tools/build_mappings.py
python3 tools/build_index.py
```

Expected: All PASS.

**Step 4: Commit**

```bash
git add tools/seo_thresholds.json
git commit -m "ci: raise SEO word count thresholds to match Phase 2 content targets"
```

---

## Task 7: Final verification

**Files:** None (read-only verification).

**Step 1: Run full pipeline**

```bash
python3 tools/validate.py && python3 tools/build_mappings.py && python3 tools/build_index.py
```

Expected: All PASS.

**Step 2: Run all tests**

```bash
python3 tools/lint_content.py
python3 tools/seo_audit.py --config tools/seo_thresholds.json
```

Expected: All PASS.

**Step 3: Verify no banned words**

```bash
python3 -c "
import re
banned = ['best', 'recommend', 'recommended', 'guarantee', 'guaranteed', '100%', 'approved', 'surely']
files = [
    'content/posts/spain-dnv-insurance.md',
    'content/posts/safetywing-vs-worldnomads-vs-genki.md',
    'content/posts/germany-freelance-insurance.md',
    'content/posts/portugal-dnv-insurance.md',
    'content/posts/thailand-dtv-insurance.md',
]
for f in files:
    text = open(f).read().lower()
    for w in banned:
        if re.search(rf'\b{re.escape(w)}\b', text):
            print(f'FAIL: {f} contains banned word: {w}')
            exit(1)
print('OK: no banned words found')
"
```

Expected: OK.

**Step 4: Verify word counts meet targets**

```bash
python3 -c "
import re
targets = {
    'content/posts/spain-dnv-insurance.md': (500, 650),
    'content/posts/safetywing-vs-worldnomads-vs-genki.md': (550, 800),
    'content/posts/germany-freelance-insurance.md': (350, 450),
    'content/posts/portugal-dnv-insurance.md': (300, 400),
    'content/posts/thailand-dtv-insurance.md': (280, 370),
}
for f, (lo, hi) in targets.items():
    text = open(f).read().lstrip('\ufeff')
    body = text.split('---', 2)[2]
    wc = len(re.findall(r'\b\w+\b', body))
    status = 'OK' if lo <= wc <= hi else 'FAIL'
    print(f'{status}: {f.split(\"/\")[-1]} = {wc} words (target {lo}-{hi})')
    if status == 'FAIL':
        exit(1)
print('All word counts within target.')
"
```

Expected: All OK.

**Step 5: Verify internal links**

```bash
python3 tools/seo_audit.py --config tools/seo_thresholds.json
```

Already covered by SEO audit but confirm explicitly.

---

## Summary

| Task | Post | Current → Target | New threshold | Key addition |
|---|---|---|---|---|
| 1 | Spain DNV | 322 → 500-650 | 425 | Mapping results (1G/5R/1U), 8 requirements listed |
| 2 | Comparison | 378 → 550-800 | 470 | Cross-visa compliance matrix, route-specific chooser |
| 3 | Germany | 282 → 350-450 | 300 | Travel vs health distinction, mapping results |
| 4 | Portugal | 275 → 300-400 | 255 | All-GREEN explanation, evidence caveat |
| 5 | Thailand | 228 → 280-370 | 240 | NOT_REQUIRED explanation, risk context |
| 6 | Thresholds | — | — | Update `seo_thresholds.json` |
| 7 | Verification | — | — | Full pipeline + banned words + word counts |

Total commits: 6 (one per content task + one for thresholds).
