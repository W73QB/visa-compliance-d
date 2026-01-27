# Hub & Spoke Content Strategy Implementation Plan (Revised)

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Implement the "Hub & Spoke" SEO strategy safely, without breaking CI or repo conventions. Hubs (blog posts) can be deep and long; spokes (route pages) remain evidence-focused and concise.

**Architecture:**
- **Hubs (Blog Posts):** TOFU/MOFU, long-form, context + comparison, link to Route Pages + checker.
- **Spokes (Route Pages):** BOFU, strict evidence, wiki-style, link to checker + related Hub.
- **Config:** Keep audit scope stable; only raise word-count thresholds when content expansion lands in the same PR.
- **Tech:** Use existing `checker_cta` shortcode; do not introduce Tailwind-only classes.

**Tech Stack:** Hugo, Python (lint/audit), Markdown.

---

### Task 1: Safe SEO Thresholds (Staged)

**Files:**
- Read: `tools/seo_thresholds.json`
- Modify (only if content expansion is included in the same PR): `tools/seo_thresholds.json`

**Step 1: Confirm current thresholds and audit scope**
Run:
```bash
cat tools/seo_thresholds.json
python3 tools/seo_audit.py --config tools/seo_thresholds.json
```

**Step 2: Stage threshold changes (if and only if content is expanded in the same PR)**
- Do **not** jump to 1000–1200 immediately.
- If you raise thresholds, set each file’s minimum to **current word count − 10–15% buffer**.
- Keep `include_globs` for **posts, guides, traps, visas** (current behavior).

**Note:** The plan’s earlier Portugal path was incorrect. The real path is:
`content/visas/portugal/temporary-stay-visa-for-remote-work-e11/vfs-global-china/index.md`

**Step 3: Commit (only if updated)**
```bash
git add tools/seo_thresholds.json
git commit -m "chore(seo): stage hub/spoke thresholds safely"
```

---

### Task 2: Verify checker_cta (No Tailwind Rewrite)

**Files:**
- Read: `layouts/shortcodes/checker_cta.html`

**Step 1: Inspect current shortcode**
Run:
```bash
cat layouts/shortcodes/checker_cta.html
```

**Step 2: Confirm**
- Accepts `visa`, `product`, `snapshot`.
- Generates `snapshot=` in the query.
- Uses existing CSS class `vf-cta` (no Tailwind).

**No change needed unless a parameter is missing.**

---

### Task 3: Expand the Spain Hub Post (Evidence‑First)

**Files:**
- Modify: `content/posts/spain-dnv-insurance.md`
- Evidence reference: `sources/ES_DNV_BLS_LONDON_checklist_2026-01-12.pdf`

**Step 1: Expand content while preserving required blocks**
**Must keep these exact headings** (lint requirement):
- “What the authority requires”
- “How we evaluate”
- “Check in the engine”
- “Disclaimer”
- “Affiliate disclosure”

**Avoid banned words**: best, recommend, guaranteed, approved, 100%, surely…

**Suggested additions (evidence-backed, no padding):**
- Mapping summary (GREEN/RED/UNKNOWN by product)
- Why “travel insurance” fails (tie to deductible/copay requirements)
- Submission checklist (how to highlight clauses in policy)

**CTA**:
```md
{{< checker_cta visa="ES_DNV_BLS_LONDON_2026" snapshot="latest" >}}
```

**Step 2: Verify lint + audit**
```bash
py tools/lint_content.py --path content/posts/spain-dnv-insurance.md
python3 tools/seo_audit.py --config tools/seo_thresholds.json
```

**Step 3: Commit**
```bash
git add content/posts/spain-dnv-insurance.md
git commit -m "content(spain): expand dnv hub post with evidence-backed depth"
```

---

### Task 4: Evidence Visuals (No static/ placeholders)

**Rule:** Do **not** place new assets under `static/` directly. It is generated/ignored.

**Option A (Preferred):** Use text excerpts + link to official source in `sources/`.
**Option B (If you want images):** Use a page bundle (requires moving the post):
- `content/posts/spain-dnv-insurance/index.md`
- `content/posts/spain-dnv-insurance/evidence-snippet.png`

**Only do Option B if you want to restructure the post.**

**If adding an evidence screenshot:**
- Keep it **small** and **attributed** (source link + date).
- Do **not** claim legal certainty about fair use.

---

### Verification Checklist (Always)

```bash
python3 tools/seo_audit.py --config tools/seo_thresholds.json
py tools/lint_content.py --path content/posts/spain-dnv-insurance.md
```

Expected: **PASS**.
