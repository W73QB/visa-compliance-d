# 4-Week 3-Axis SEO Plan Implementation Plan

**Goal:** Execute a 4-week plan that balances **Content**, **Technical SEO/CWV**, and **Distribution** in weekly phases without breaking evidence-first, lint rules, or CI.

**Architecture:**  
Week 1–2 focus on **Content + Tech** (quality + speed), Week 3–4 add **Distribution** on top of a stable foundation. Content work stays evidence-first with required blocks; tech work avoids repo-generated folders (`static/`), and distribution uses documented templates and UTM tracking.

**Tech Stack:** Hugo, Markdown, Python (lint/audit), PowerShell tests.

**Working agreement:** Do not commit until verify scripts PASS. If commits are desired, use conventional prefixes (`docs:`, `feat:`, `fix:`) per repo guidelines.

---

### Task 1: Week 1 Distribution Tracking Scaffold (Naming + UTM)

**Files:**
- Create: `docs/ops/distribution-week1-log.md`

**Step 1: Add a distribution tracking template**
```md
# Week 1 Distribution Log (Template)

## Channels
- Reddit (r/digitalnomad, r/expats)
- Facebook groups (nomad/expat)
- IndieHackers / Hacker News (if relevant)

## UTM Template
?utm_source=community&utm_medium=post&utm_campaign=dnv-hub-week1&utm_content={{channel}}

## Posts
- Date:
  Channel:
  URL posted:
  Target page:
  Notes:
```

**Step 2: (Optional) Commit**
```bash
git add docs/ops/distribution-week1-log.md
git commit -m "docs: add week1 distribution log template"
```

---

### Task 2: Week 1 Tech — Evidence Image Shortcode (CWV-safe)

**Files:**
- Create: `layouts/shortcodes/evidence_image.html`
- Create: `content/templates/evidence-image-test.md`

**Step 1: Write a simple shortcode**
```html
{{- $src := .Get "src" -}}
{{- $alt := .Get "alt" | default "Evidence snippet" -}}
{{- $width := .Get "width" | default "1200" -}}
{{- $height := .Get "height" | default "800" -}}
{{- $src = relURL $src -}}
<figure class="evidence-figure">
  <img src="{{ $src }}" alt="{{ $alt }}" width="{{ $width }}" height="{{ $height }}" loading="lazy" decoding="async">
  {{- with .Get "caption" -}}
  <figcaption>{{ . }}</figcaption>
  {{- end -}}
</figure>
```

**Step 2: Add a test template**
```md
---
title: "Evidence image test"
draft: true
---

{{< evidence_image src="/posts/spain-dnv-insurance/evidence-es-bls-item9.png" alt="Evidence sample" width="1200" height="600" caption="Source: ES_DNV_BLS_LONDON_checklist_2026-01-12.pdf (Item 9)" >}}
```
**Note:** This test assumes the Spain post bundle exists at `/posts/spain-dnv-insurance/`.

**Step 3: (Optional) Commit**
```bash
git add layouts/shortcodes/evidence_image.html content/templates/evidence-image-test.md
git commit -m "feat: add evidence image shortcode"
```

---

### Task 3: Week 1 Content — Deepen Germany Hub Post (Evidence Depth)

**Files:**
- Modify: `content/posts/germany-freelance-insurance.md`
- Modify: `tools/seo_thresholds.json` (raise threshold after content)

**Step 1: Deepen existing sections (do not duplicate)**
Add one evidence-backed paragraph to each existing section:
- Mapping results summary
- Common pitfalls
- What to prepare

**Step 2: Verify**
```bash
py tools/lint_content.py --path content/posts/germany-freelance-insurance.md
py tools/seo_audit.py --config tools/seo_thresholds.json
```

**Step 3: If word count increased, update threshold**
```json
"content/posts/germany-freelance-insurance.md": <new_min_count>
```

**Step 4: (Optional) Commit**
```bash
git add content/posts/germany-freelance-insurance.md tools/seo_thresholds.json
git commit -m "docs: deepen germany hub post and align thresholds"
```

---

### Task 4: Week 2 Content — Deepen Portugal Hub Post (Evidence Depth)

**Files:**
- Modify: `content/posts/portugal-dnv-insurance.md`
- Modify: `tools/seo_thresholds.json`

**Step 1: Deepen existing sections (do not duplicate)**
Add one evidence-backed paragraph to each existing section:
- Mapping results summary
- Common pitfalls
- What to prepare

**Step 2: Verify + adjust threshold**
```bash
py tools/lint_content.py --path content/posts/portugal-dnv-insurance.md
py tools/seo_audit.py --config tools/seo_thresholds.json
```

**Step 3: (Optional) Commit**
```bash
git add content/posts/portugal-dnv-insurance.md tools/seo_thresholds.json
git commit -m "docs: deepen portugal hub post and align thresholds"
```

---

### Task 5: Week 2 Content — Deepen Thailand DTV Hub Post (Not-Required + Risk)

**Files:**
- Modify: `content/posts/thailand-dtv-insurance.md`
- Modify: `tools/seo_thresholds.json`

**Step 1: Deepen existing sections**
Add one evidence-backed paragraph to:
- Why NOT_REQUIRED matters
- Common pitfalls / risk scenarios

**Step 2: Verify + adjust threshold**
```bash
py tools/lint_content.py --path content/posts/thailand-dtv-insurance.md
py tools/seo_audit.py --config tools/seo_thresholds.json
```

**Step 3: (Optional) Commit**
```bash
git add content/posts/thailand-dtv-insurance.md tools/seo_thresholds.json
git commit -m "docs: deepen thailand hub post and align thresholds"
```

---

### Task 6: Week 3 Content — Deepen Comparison Post (Decision Matrix)

**Files:**
- Modify: `content/posts/safetywing-vs-worldnomads-vs-genki.md`
- Modify: `tools/seo_thresholds.json`

**Step 1: Deepen existing comparison section**
Add one evidence-backed paragraph under:
- Decision matrix (by route)
- When each plan fails

**Step 2: Verify + adjust threshold**
```bash
py tools/lint_content.py --path content/posts/safetywing-vs-worldnomads-vs-genki.md
py tools/seo_audit.py --config tools/seo_thresholds.json
```

**Step 3: (Optional) Commit**
```bash
git add content/posts/safetywing-vs-worldnomads-vs-genki.md tools/seo_thresholds.json
git commit -m "docs: deepen comparison hub post and align thresholds"
```

---

### Task 7: Week 3 Tech — CWV Baseline Snapshot (Defined URLs)

**Files:**
- Create: `docs/ops/cwv-baseline.md`

**Step 1: Capture baseline**
```md
# CWV Baseline (Week 3)
- LCP:
- CLS:
- INP:
- Tools: PageSpeed Insights / WebPageTest
- URLs:
  - https://visafact.org/
  - https://visafact.org/ui/
  - https://visafact.org/posts/spain-dnv-insurance/
```

**Step 2: (Optional) Commit**
```bash
git add docs/ops/cwv-baseline.md
git commit -m "docs: add CWV baseline snapshot"
```

---

### Task 8: Week 4 Distribution — Post & Measure

**Files:**
- Create: `docs/ops/distribution-week4-log.md`

**Step 1: Log outreach results**
- Fill in channels and outcomes for the 4 hub posts.

**Step 2: (Optional) Commit**
```bash
git add docs/ops/distribution-week4-log.md
git commit -m "docs: log distribution results for week4"
```

---

### Verification Checklist (Weekly)

```bash
py tools/seo_audit.py --config tools/seo_thresholds.json
py tools/lint_content.py --path <file>
pwsh -File tools/tests/seo_audit_tests.ps1
```

Expected: **PASS**.
