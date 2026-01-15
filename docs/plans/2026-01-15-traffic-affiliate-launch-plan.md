# Traffic & Affiliate Launch Plan - VisaFact

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Launch evidence-based content that drives qualified traffic to the checker and supports affiliate conversion without violating compliance rules.

**Architecture:** SEO blog content (Hugo/PaperMod) + evidence-based checker + affiliate CTA shown only after results. Every claim in content must be backed by a source in `sources/` or phrased as a non-claim.

**Tech Stack:** Hugo, Markdown, Python (`lint_content.py`), PowerShell tests.

---

## Guardrails (Non-negotiable)

1. **No source = no claim.** Any factual statement about visa requirements or product specs must be tied to official evidence in `sources/`.
2. **No banned words** (lint will fail): best, recommend, recommended, guarantee, guaranteed, 100%, approved, surely.
3. **Affiliate copy must be neutral** and must not imply influence on results.
4. **Use snapshot links** in every post: `/ui/?...&snapshot=releases/YYYY-MM-DD`.
5. **Do not overwrite existing posts** unless explicitly updating them.

---

## Phase 1: Priority Content (High-Intent)

### Task 1.1: Spain DNV â€“ SafetyWing rejection analysis

**Files:**
- Create: `content/posts/safetywing-spain-dnv-rejected.md`
- Evidence: `sources/ES_DNV_BLS_LONDON_checklist_2026-01-12.pdf`

**Steps:**
1) Verify mapping is RED:
```bash
py -c "import json; d=json.load(open('data/mappings/ES_DNV_BLS_LONDON_2026__SAFETYWING_NOMAD_2026.json')); print(d['status'])"
```
Expected: RED.

2) Draft post using the template blocks. Keep only evidence-backed statements:
- Authorized in Spain requirement (BLS checklist)
- No deductible / no co-payments requirement (BLS checklist)
- SafetyWing deductible and authorization status must be evidenced from `sources/` before stating

3) Lint:
```bash
py tools/lint_content.py --path content/posts/safetywing-spain-dnv-rejected.md
```

4) Commit:
```bash
git add content/posts/safetywing-spain-dnv-rejected.md
git commit -m "docs(blog): add Spain DNV SafetyWing evidence analysis"
```

---

### Task 1.2: Spain DNV â€“ Common mistakes (traps)

**Files:**
- Create: `content/traps/spain-dnv-insurance-mistakes.md`

**Steps:**
1) Only include mistakes that are proven by official sources:
- Authorized insurer requirement (BLS)
- No deductible / no co-payment requirement (BLS)
- Unlimited coverage requirement (BLS)
- No moratorium requirement (BLS)

2) Draft post with required blocks and snapshot link.
3) Lint and commit:
```bash
py tools/lint_content.py --path content/traps/spain-dnv-insurance-mistakes.md
git add content/traps/spain-dnv-insurance-mistakes.md
git commit -m "docs(blog): add Spain DNV insurance mistakes guide"
```

---

### Task 1.3: Comparison post (evidence-based)

**Files:**
- Create: `content/posts/safetywing-vs-worldnomads-vs-genki.md`

**Constraints:**
- Do not include Genki unless evidence is added to `sources/` and `data/products/`.
- Avoid claims like "only checker" or "best".
- Present results as evidence-based outputs of the engine.

**Steps:**
1) If Genki is included, complete Phase 3 Task 3.1 first.
2) Draft the post using only evidence-backed facts.
3) Lint and commit.

---

### Task 1.4: Schengen 30,000 insurance guide

**Files:**
- Create: `content/guides/schengen-30000-insurance.md`

**Constraints:**
- Must include official Schengen regulation or embassy checklist in `sources/`.
- Do not include non-sourced statements (e.g., "automatic rejection").

**Steps:**
1) Add official source to `sources/` and `.meta.json`.
2) Draft post with required blocks + snapshot link.
3) Lint and commit.

---

## Phase 2: Medium-Intent Content

### Task 2.1: Thailand DTV â€“ Insurance required or not?

**Files:**
- Update existing: `content/posts/thailand-dtv-insurance.md`

**Steps:**
1) Ensure statements match evidence in `sources/TH_DTV_MFA_requirements_2026-01-12.md`.
2) Add snapshot link and keep required blocks.
3) Lint and commit.

---

### Task 2.2: Malta â€“ Monthly payments rejected

**Files:**
- Create: `content/traps/malta-nomad-monthly-payments.md`

**Constraints:**
- Use official Residency Malta source in `sources/MT_NOMAD_RESIDENCY_FAQ_2026-01-12.md`.

**Steps:**
1) Draft post with required blocks + snapshot link.
2) Lint and commit.

---

### Task 2.3: Portugal DNV (E11) requirements

**Files:**
- Create: `content/posts/portugal-dnv-insurance.md`

**Constraints:**
- Use `sources/PT_E11_VFS_CHINA_2025-07.pdf` (current evidence).
- If you want D8 (UK) route, add proper evidence first and update the plan.

**Steps:**
1) Draft post with required blocks + snapshot link.
2) Lint and commit.

---

### Task 2.4: Germany Freelance (National D) insurance guide

**Files:**
- Create: `content/posts/germany-freelance-insurance.md`

**Constraints:**
- Use `sources/DE_HEALTH_INSURANCE_REQUIREMENTS_2026-01-15.html`.

**Steps:**
1) Draft post with required blocks + snapshot link.
2) Lint and commit.

---

## Phase 3: Data & Affiliate Setup

### Task 3.1: Add Genki product (optional)

**Files:**
- Create: `data/products/Genki/WorldExplorer/2026-01-15/product_facts.json`
- Create: `sources/GENKI_WORLD_EXPLORER_2026.md`
- Create: `sources/GENKI_WORLD_EXPLORER_2026.md.meta.json`

**Constraints:**
- Every spec must be backed by evidence.
- If evidence is not available, leave spec as null and expect UNKNOWN.

**Steps:**
1) Capture official evidence from Genki site.
2) Compute SHA256 and create meta.
3) Validate and commit.

---

### Task 3.2: Update affiliate offers

**Files:**
- Modify: `data/offers/offers.json`

**Constraints:**
- Labels/disclosures must avoid banned words.

**Steps:**
1) Add offer entries for products that exist in data.
2) Validate and commit.

---

## Phase 4: SEO & Technical Checks

1) Verify `hugo.toml` has `enableRobotsTXT = true`.
2) Ensure sitemap is generated (`/sitemap.xml`).
3) Verify OG/meta are correct (PaperMod defaults).
4) Optional: add keywords meta support if needed.

---

## Phase 5: Launch Verification

1) Run full pipeline and tests.
2) Local preview: `hugo server -D`.
3) Deploy and verify URLs live:
   - `/posts/safetywing-spain-dnv-rejected/`
   - `/traps/spain-dnv-insurance-mistakes/`
   - `/ui/`

---

## Metrics (Privacy-first)

Track using a privacy-first analytics tool (Plausible/Fathom):
- Organic sessions
- Checker usage
- Affiliate click-through
- Bounce rate

---

## Execution Handoff

Plan ready for execution after evidence sources are added and encoding issues are resolved.
