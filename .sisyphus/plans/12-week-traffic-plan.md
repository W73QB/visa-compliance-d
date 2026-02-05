# 12-Week English Traffic Growth Plan (Compliance-First, Mixed Monetization)

## TL;DR

> **Quick Summary**: Raise content depth and internal linking across existing posts, traps, guides, and visa route pages using an evidence-first template, while applying compliance-first monetization and measurable lead KPIs.
>
> **Deliverables**:
> - Updated content across existing posts/traps/guides/visa routes (no new routes)
> - Hub/spoke link matrix + per-page link targets (Week 1)
> - Weekly lint + SEO audit gates and word-count targets
> - Monetization placement rules (affiliate only when compliant; ads/lead-gen elsewhere)
>
> **Estimated Effort**: Large
> **Parallel Execution**: YES - 3 waves
> **Critical Path**: Baseline audit -> Hub/spoke matrix -> Core route rewrites -> Visa route rewrites -> QA gates

---

## Context

### Original Request
Evaluate the accuracy of an external report, then produce a precise 12-week plan to increase organic traffic and monetize via compliance-first content on visafact.org.

### Interview Summary
**Key Decisions**:
- Language: English (global audience).
- Monetization: Mixed (compliance-first; affiliate only when compliant; ads/lead-gen on non-affiliate high-traffic pages).
- No promises of 1k/day; use lead KPIs only.

**Repo Constraints**:
- Content lint requires blocks: "what the authority requires", "how we evaluate", "check in the engine", "disclaimer", "affiliate disclosure", "evidence log".
- Banned words list in lint (best, recommend, recommended, guarantee, guaranteed, 100%, approved, surely).
- SEO audit requires links to /ui/ and specific internal paths per content type and FAQ frontmatter for specified files.
- Existing content inventory (no new routes): 11 posts, 4 guides, 4 traps, 13 visa files.

### Prior Plans Status
This plan supersedes `docs/plans/2026-02-04-12-week-post-rewrite-plan.md` and any earlier SEO/content plans under `docs/plans/`. Task 1 must confirm what is already completed to avoid duplicate work.

**Search Central Constraints (citations)**:
- "A sitemap helps search engines discover URLs on your site, but it doesn't guarantee that all items in your sitemap will be crawled and indexed." (https://developers.google.com/search/docs/crawling-indexing/sitemaps/overview)
- "Just because a page is indexed doesn't guarantee that it will show up in your search results." (https://support.google.com/webmasters/answer/9012289)

### Metis Review (Gaps Addressed)
- Added hub/spoke link matrix in Week 1.
- Moved internal linking to Week 1 (not Week 10).
- Monetization aligned with offers.json (only Genki is affiliate).
- Explicit guardrails: no new routes, no UI changes, no analytics setup.
- Added acceptance criteria: lint, SEO audit, word count, link density, and FAQ schema checks.

---

## Work Objectives

### Core Objective
Increase organic traffic by improving evidence-based depth and internal link architecture across existing content while keeping compliance-first positioning.

### Concrete Deliverables
- Hub/spoke link matrix (posts <-> visas <-> traps <-> guides) with per-page link targets.
- Updated posts, traps, guides, and visa route pages to meet target word count and lint/SEO audits.
- Monetization placement rules and disclosures applied consistently.

### Definition of Done
- All updated content passes `python3 tools/lint_content.py` and `python3 tools/seo_audit.py --config tools/seo_thresholds.json`.
- All updated pages include required internal links (/ui/ + /visas/ or /posts/ + /methodology for traps).
- Word counts fall within defined target ranges (not just minimum thresholds).
- Evidence log present on all non-_index.md pages.
- Compliance-first monetization rules applied (affiliate only when compliant).

### Must Have
- Evidence-first writing with explicit sources and evidence logs.
- Internal link density: minimum 5 internal links per page (with required link types).
- Week-by-week QA gates (lint + SEO audit) before moving to next week.

### Must NOT Have (Guardrails)
- No new visa routes or new content types (no /reports, /contact, etc.).
- No UI changes under ui/.
- No analytics setup changes.
- No affiliate placement where product is not compliant for the route.
- No padding content beyond evidence (especially for Portugal with limited evidence).
- Do not change `tools/seo_thresholds.json` or lint rules.
- Do not change URLs/slugs or convert file structures (no page bundle migrations).

### Lint Guardrails (Explicit)
- Required blocks (case-insensitive): what the authority requires; how we evaluate; check in the engine; disclaimer; affiliate disclosure; evidence log (not required for _index.md).
- Banned words: best, recommend, recommended, guarantee, guaranteed, 100%, approved, surely.
- Each page must include a deep link with `snapshot=`.

### Word Count Targets (Editorial)
- These are editorial ranges on top of minimum thresholds in `tools/seo_thresholds.json`.
- Route posts: 900-1200 words (Portugal may cap at 700 if evidence remains thin).
- Comparison/rejected: 1000-1400 words.
- Regional hubs: 900-1200 words.
- Trap posts: 700-900 words.
- Visa route pages: 900-1300 words.
- Guides: 400-700 words.

---

## Verification Strategy (MANDATORY)

### Test Decision
- **Infrastructure exists**: YES (lint_content.py, seo_audit.py)
- **Automated tests**: Tests-after (lint + audit after each batch)
- **Framework**: Python scripts

### Editorial Word Count Enforcement

`tools/seo_thresholds.json` enforces **minimum** thresholds only (e.g., Malta = 150 words). Editorial targets (e.g., Malta = 900-1200 words) are much higher. To close this gap without modifying `seo_thresholds.json`, Task 1 must create `tools/editorial_targets.json` and `tools/check_editorial_targets.py`.

**`tools/editorial_targets.json`** — per-file min/max word count ranges:
```json
{
  "content/posts/spain-dnv-insurance/index.md": [900, 1200],
  "content/posts/portugal-dnv-insurance.md": [450, 700],
  "content/posts/germany-freelance-insurance.md": [900, 1200],
  "content/posts/thailand-dtv-insurance.md": [900, 1200],
  "content/posts/malta-nomad-insurance.md": [900, 1200],
  "content/posts/costa-rica-dn-insurance.md": [900, 1200],
  "content/posts/safetywing-spain-dnv-rejected.md": [1000, 1400],
  "content/posts/safetywing-vs-worldnomads-vs-genki.md": [1000, 1400],
  "content/posts/digital-nomad-insurance-europe.md": [900, 1200],
  "content/posts/digital-nomad-insurance-asia.md": [900, 1200],
  "content/posts/digital-nomad-insurance-americas.md": [900, 1200],
  "content/traps/germany-travel-insurance-rejected.md": [700, 900],
  "content/traps/spain-dnv-coverage-cap-trap.md": [700, 900],
  "content/traps/spain-dnv-insurance-mistakes.md": [700, 900],
  "content/traps/malta-nomad-monthly-payments.md": [700, 900],
  "content/visas/spain/digital-nomad-visa/consulate-via-bls-london/index.md": [900, 1300],
  "content/visas/germany/freelance-visa-national-d/embassy-london/index.md": [900, 1300],
  "content/visas/portugal/temporary-stay-visa-for-remote-work-e11/vfs-global-china/index.md": [900, 1300],
  "content/visas/costa-rica/digital-nomad-visa/executive-decree-43619/index.md": [900, 1300],
  "content/visas/thailand/digital-nomad-visa-dtv/thai-e-visa/index.md": [900, 1300],
  "content/visas/malta/nomad-residence-permit/residency-malta-agency/index.md": [900, 1300],
  "content/guides/compliance-status-meaning.md": [400, 700],
  "content/guides/how-to-choose-dnv-insurance.md": [400, 700],
  "content/guides/how-to-read-results.md": [400, 700],
  "content/guides/schengen-30000-insurance.md": [400, 700]
}
```

**`tools/check_editorial_targets.py`** — reuses the same `word_count()` function from `seo_audit.py` to ensure consistent counting. Exits non-zero if any file falls outside its editorial range.

This script is a **Task 1 deliverable**. All subsequent tasks (3-10) must run it as part of QA.

### Agent-Executed QA Scenarios
All tasks include:
- Lint verification (`python3 tools/lint_content.py`)
- SEO audit verification (`python3 tools/seo_audit.py --config tools/seo_thresholds.json`)
- Editorial target verification (`python3 tools/check_editorial_targets.py`)
- Link density checks via grep
- Optional build + FAQ schema check for FAQ frontmatter pages

---

## Execution Strategy

### Parallel Execution Waves

Wave 1 (Baseline + Link Matrix)
- Task 1: Baseline audit and prior plan completion matrix
- Task 2: Hub/spoke link matrix + per-page link targets

Wave 2 (Core Routes + Comparisons)
- Task 3: Core route posts (Spain/Portugal)
- Task 4a: Core route posts (Germany/Thailand)
- Task 4b: Core route posts (Malta/Costa Rica)
- Task 5: Comparison/Rejected posts

Wave 3 (Hubs + Traps + Visa Routes + QA)
- Task 6: Regional hubs (Europe/Asia/Americas)
- Task 7: Traps batch
- Task 8: Visa route pages batch
- Task 10: Guides batch
- Task 9: Final QA + indexing requests

### Dependency Matrix

| Task | Depends On | Blocks | Can Parallelize With |
|------|------------|--------|----------------------|
| 1 | None | 2-10 | None |
| 2 | 1 | 3-10 | None |
| 3 | 2 | 6-10 | 4a,4b,5 |
| 4a | 2 | 6-10 | 3,4b,5 |
| 4b | 2 | 6-10 | 3,4a,5 |
| 5 | 2 | 6-10 | 3,4a,4b |
| 6 | 3,4a,4b | 9 | 7,8,10 |
| 7 | 2,3,4a,4b | 9 | 6,8,10 |
| 8 | 2 | 9 | 6,7,10 |
| 10 | 2,3,4a,4b | 9 | 6,7,8 |
| 9 | 3-8,10 | None | None |

---

### Week Mapping (12-week calendar)

| Week | Primary Focus | Tasks |
|------|---------------|-------|
| 1 | Baseline + link matrix + prioritization | 1, 2 |
| 2 | Core route posts (Spain/Portugal) | 3 |
| 3 | Core route posts (Germany/Thailand) | 4a |
| 4 | Core route posts (Malta/Costa Rica) | 4b |
| 5 | Comparison/Rejected posts | 5 |
| 6 | Regional hubs | 6 |
| 7 | Traps + visa routes (start) | 7, 8 (part 1) |
| 8 | Visa routes (continue) | 8 (part 2) |
| 9 | Guides batch | 10 |
| 10 | Final QA + indexing requests | 9 |
| 11 | Buffer/catch-up | any delayed tasks |
| 12 | Report + next cycle notes | 9 (reporting addendum) |

---

## TODOs

> Implementation + Test = ONE Task. No new routes. Each task has QA scenarios.

- [ ] 1. Baseline audit + prior plan completion matrix

  **What to do**:
  - Run lint + SEO audit on current content.
  - Generate a table listing all target files from the 12-week plan with current word count and pass/fail status.
  - Mark which files already meet targets to avoid duplicate work.
  - Build a monetization eligibility matrix per route using data/ui_index.json + data/offers/offers.json.
  - Prioritize pages using GSC Performance export (last 90 days). If no export is available, use proxy scoring: evidence density + word count gap + route importance.
  - Note: `gsc-overview*.md` files are UI dumps and are not usable metrics; do not use them for prioritization.
  - Create `tools/editorial_targets.json` and `tools/check_editorial_targets.py` (see Editorial Word Count Enforcement section). The script must reuse the same `word_count()` logic from `tools/seo_audit.py` and exit non-zero if any file is outside its editorial range.

  **Must NOT do**:
  - Do not edit content in this task.

  **Recommended Agent Profile**:
  - **Category**: writing
    - Reason: plan documentation and audit summary
  - **Skills**: ["doc-coauthoring", "verification-before-completion"]
    - doc-coauthoring: structure the audit summary
    - verification-before-completion: enforce command evidence
  - **Skills Evaluated but Omitted**:
    - playwright: not needed for local audits

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1
  - **Blocks**: Tasks 2-10
  - **Blocked By**: None

  **References**:
  - `tools/lint_content.py` - required blocks and banned words
  - `tools/seo_audit.py` - word count + required links checks
  - `tools/seo_thresholds.json` - min word count and link rules
  - `docs/plans/2026-02-04-12-week-post-rewrite-plan.md` - base file list and target ranges
  - `data/ui_index.json` - route compliance results
  - `data/offers/offers.json` - affiliate vs non-affiliate links

  **Acceptance Criteria**:
  - `python3 tools/lint_content.py` -> exit 0
  - `python3 tools/seo_audit.py --config tools/seo_thresholds.json` -> exit 0
  - `tools/editorial_targets.json` created with per-file [min, max] word count ranges
  - `tools/check_editorial_targets.py` created, runnable, and uses same `word_count()` logic as `seo_audit.py`
  - `python3 tools/check_editorial_targets.py` -> reports current gaps (expected to fail before content updates)
  - A completion matrix is produced listing each target file with current word count, editorial target, and gap
  - A monetization eligibility matrix lists Genki compliance per route and where affiliate CTA is allowed
  - A prioritization list exists, with top 6 pages to update first (based on GSC export or proxy scoring)

  **Agent-Executed QA Scenarios**:
  Scenario: Run lint, SEO audit, and editorial check
    Tool: Bash
    Preconditions: Repo available
    Steps:
      1. Run `python3 tools/lint_content.py`
      2. Run `python3 tools/seo_audit.py --config tools/seo_thresholds.json`
      3. Run `python3 tools/check_editorial_targets.py` (expected to show gaps pre-update)
      4. Capture outputs
    Expected Result: Lint and SEO audit exit 0; editorial check reports gaps
    Evidence: Terminal output capture

- [ ] 2. Hub/spoke link matrix + per-page link targets (Week 1)

  **What to do**:
  - Define hub/spoke topology for existing routes (Spain/Portugal/Germany/Thailand/Malta/Costa Rica).
  - Produce a matrix: each content type (route post, trap, guide, visa spoke, regional hub) with required internal links.

  **Must NOT do**:
  - Do not add new route pages.

  **Recommended Agent Profile**:
  - **Category**: writing
  - **Skills**: ["doc-coauthoring", "brainstorming"]
    - doc-coauthoring: produce structured matrix
    - brainstorming: ensure coverage of link paths
  - **Skills Evaluated but Omitted**:
    - playwright: not needed

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1
  - **Blocks**: Tasks 3-9
  - **Blocked By**: Task 1

  **References**:
  - `tools/seo_thresholds.json` - required links
  - `content/posts/` and `content/visas/` - existing route pages

  **Acceptance Criteria**:
  - Matrix includes per-page link targets:
    - Route post -> visa spoke + 1 trap + 1 regional hub + /ui/
    - Trap -> route post + visa spoke + /methodology/
    - Guide -> route post + visa spoke + /ui/
    - Visa spoke -> route post + country hub + /ui/
    - Regional hub -> all country route posts + /ui/

  **Agent-Executed QA Scenarios**:
  Scenario: Validate matrix completeness
    Tool: Bash
    Preconditions: Matrix drafted
    Steps:
      1. Ensure all 6 routes appear as nodes
      2. Check that each content type has link targets
    Expected Result: Matrix covers all routes and link paths
    Evidence: Matrix output file

- [ ] 3. Core route posts batch A (Spain, Portugal)

  **What to do**:
  - Update `content/posts/spain-dnv-insurance/index.md` and `content/posts/portugal-dnv-insurance.md` to target range 900-1200 words (Portugal may be lower if evidence limited).
  - Apply 11-block template, evidence excerpts, and link matrix.

  **Must NOT do**:
  - Do not add claims without evidence.

  **Recommended Agent Profile**:
  - **Category**: writing
  - **Skills**: ["doc-coauthoring", "verification-before-completion"]
  - **Skills Evaluated but Omitted**:
    - brainstorming (template already defined)

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2
  - **Blocks**: Task 6-9
  - **Blocked By**: Task 2

  **References**:
  - `docs/sop/content-workflow.md` - required template
  - `tools/lint_content.py` - required blocks and banned words
  - `content/posts/spain-dnv-insurance/index.md` - pattern example

  **Acceptance Criteria**:
  - `python3 tools/lint_content.py --path content/posts/spain-dnv-insurance/index.md` -> OK
  - `python3 tools/lint_content.py --path content/posts/portugal-dnv-insurance.md` -> OK
  - `python3 tools/seo_audit.py --config tools/seo_thresholds.json` -> pass
  - Word count within target range (Portugal: 450-700 if evidence remains thin; must be >= threshold)

  **Agent-Executed QA Scenarios**:
  Scenario: Verify word count and links
    Tool: Bash
    Preconditions: Files updated
    Steps:
      1. `wc -w < content/posts/spain-dnv-insurance/index.md`
      2. `grep -c '/visas/' content/posts/spain-dnv-insurance/index.md`
      3. `grep -c '/ui/' content/posts/spain-dnv-insurance/index.md`
      4. `grep -Eo '/(posts|visas|guides|traps|ui)/' content/posts/spain-dnv-insurance/index.md | wc -l`
    Expected Result: word count in range; required links present
    Evidence: Terminal output

- [ ] 4a. Core route posts batch B-1 (Germany, Thailand)

  **What to do**:
  - Update `content/posts/germany-freelance-insurance.md` and `content/posts/thailand-dtv-insurance.md` to target range 900-1200 words.
  - Apply 11-block template, evidence excerpts, and link matrix.

  **Must NOT do**:
  - Do not add new routes.
  - Do not add claims without evidence.

  **Recommended Agent Profile**:
  - **Category**: writing
  - **Skills**: ["doc-coauthoring", "verification-before-completion"]

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2
  - **Blocks**: Task 6-10
  - **Blocked By**: Task 2

  **References**:
  - `content/posts/germany-freelance-insurance.md`
  - `content/posts/thailand-dtv-insurance.md`
  - `docs/sop/content-workflow.md` - required template

  **Acceptance Criteria**:
  - `python3 tools/lint_content.py --path content/posts/germany-freelance-insurance.md` -> OK
  - `python3 tools/lint_content.py --path content/posts/thailand-dtv-insurance.md` -> OK
  - `python3 tools/seo_audit.py --config tools/seo_thresholds.json` -> pass
  - Word count within 900-1200 range per file
  - Required links per file present (per link matrix)

  **Agent-Executed QA Scenarios**:
  Scenario: Lint and verify word count
    Tool: Bash
    Preconditions: Files updated
    Steps:
      1. Run lint on each file
      2. Run SEO audit
      3. Run `python3 tools/check_editorial_targets.py` (see Task 1 deliverable)
    Expected Result: all OK, word counts in range
    Evidence: Terminal output

- [ ] 4b. Core route posts batch B-2 (Malta, Costa Rica)

  **What to do**:
  - Update `content/posts/malta-nomad-insurance.md` and `content/posts/costa-rica-dn-insurance.md` to target range 900-1200 words.
  - Apply 11-block template, evidence excerpts, and link matrix.

  **Must NOT do**:
  - Do not add new routes.
  - Do not add claims without evidence.

  **Recommended Agent Profile**:
  - **Category**: writing
  - **Skills**: ["doc-coauthoring", "verification-before-completion"]

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2
  - **Blocks**: Task 6-10
  - **Blocked By**: Task 2

  **References**:
  - `content/posts/malta-nomad-insurance.md`
  - `content/posts/costa-rica-dn-insurance.md`
  - `docs/sop/content-workflow.md` - required template

  **Acceptance Criteria**:
  - `python3 tools/lint_content.py --path content/posts/malta-nomad-insurance.md` -> OK
  - `python3 tools/lint_content.py --path content/posts/costa-rica-dn-insurance.md` -> OK
  - `python3 tools/seo_audit.py --config tools/seo_thresholds.json` -> pass
  - Word count within 900-1200 range per file
  - Required links per file present (per link matrix)

  **Agent-Executed QA Scenarios**:
  Scenario: Lint and verify word count
    Tool: Bash
    Preconditions: Files updated
    Steps:
      1. Run lint on each file
      2. Run SEO audit
      3. Run `python3 tools/check_editorial_targets.py` (see Task 1 deliverable)
    Expected Result: all OK, word counts in range
    Evidence: Terminal output

- [ ] 5. Comparison/Rejected posts

  **What to do**:
  - Update `content/posts/safetywing-spain-dnv-rejected.md` and `content/posts/safetywing-vs-worldnomads-vs-genki.md`.
  - Add compliance-first monetization: Genki only if compliant for referenced routes.

  **Must NOT do**:
  - Do not imply compliance where evidence says RED.

  **Recommended Agent Profile**:
  - **Category**: writing
  - **Skills**: ["doc-coauthoring", "verification-before-completion"]

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2
  - **Blocks**: Task 6-9
  - **Blocked By**: Task 2

  **References**:
  - `data/offers/offers.json` - affiliate disclosures
  - `data/products/**/product_facts.json` - compliance facts (versioned directories)

  **Acceptance Criteria**:
  - Lint and SEO audit pass
  - Disclosures present for affiliate links
  - Affiliate link only where compliant

  **Agent-Executed QA Scenarios**:
  Scenario: Verify disclosure text
    Tool: Bash
    Preconditions: Files updated
    Steps:
      1. `grep -n "affiliate disclosure" -i content/posts/safetywing-vs-worldnomads-vs-genki.md`
      2. `grep -n "Paid link" -i content/posts/safetywing-vs-worldnomads-vs-genki.md`
    Expected Result: Disclosure present
    Evidence: Terminal output

- [ ] 6. Regional hubs (Europe/Asia/Americas)

  **What to do**:
  - Update hub posts to include links to every country route post + /ui/.
  - Ensure hubs are not thin link lists; include evidence-based summaries.

  **Must NOT do**:
  - Do not add new country routes.

  **Recommended Agent Profile**:
  - **Category**: writing
  - **Skills**: ["doc-coauthoring"]

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3
  - **Blocks**: Task 9
  - **Blocked By**: Tasks 3, 4a, 4b, 5

  **References**:
  - `content/posts/digital-nomad-insurance-europe.md`
  - `content/posts/digital-nomad-insurance-asia.md`
  - `content/posts/digital-nomad-insurance-americas.md`

  **Acceptance Criteria**:
  - Each hub links to all existing country route posts
  - Lint and SEO audit pass

  **Agent-Executed QA Scenarios**:
  Scenario: Verify hub links
    Tool: Bash
    Preconditions: Files updated
    Steps:
      1. `grep -c '/posts/' content/posts/digital-nomad-insurance-europe.md`
      2. `grep -c '/ui/' content/posts/digital-nomad-insurance-europe.md`
      3. `grep -Eo '/(posts|visas|guides|traps|ui)/' content/posts/digital-nomad-insurance-europe.md | wc -l`
    Expected Result: link counts >= required targets
    Evidence: Terminal output

- [ ] 7. Traps batch

  **What to do**:
  - Update traps to include methodology link and route/visa links per matrix.

  **Must NOT do**:
  - No new traps beyond existing four.

  **Recommended Agent Profile**:
  - **Category**: writing
  - **Skills**: ["doc-coauthoring"]

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3
  - **Blocks**: Task 9
  - **Blocked By**: Tasks 2, 3, 4a, 4b

  **References**:
  - `content/traps/*.md`

  **Acceptance Criteria**:
  - Each trap includes /methodology and at least one /posts/ or /visas/ link
  - Lint and SEO audit pass

  **Agent-Executed QA Scenarios**:
  Scenario: Verify methodology link
    Tool: Bash
    Preconditions: Files updated
    Steps:
      1. `grep -c '/methodology' content/traps/spain-dnv-coverage-cap-trap.md`
      2. `grep -Eo '/(posts|visas|guides|traps|ui|methodology)/' content/traps/spain-dnv-coverage-cap-trap.md | wc -l`
    Expected Result: count >= 1
    Evidence: Terminal output

- [ ] 8. Visa route pages batch

  **What to do**:
  - Update visa route pages with link matrix (route post + country hub + /ui/).

  **Must NOT do**:
  - No new visa routes.

  **Recommended Agent Profile**:
  - **Category**: writing
  - **Skills**: ["doc-coauthoring"]

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3
  - **Blocks**: Task 9
  - **Blocked By**: Task 2

  **References**:
  - `content/visas/**/index.md`

  **Acceptance Criteria**:
  - Each visa page includes /ui/ and at least one /posts/ link
  - Lint and SEO audit pass

  **Agent-Executed QA Scenarios**:
  Scenario: Verify visa link targets
    Tool: Bash
    Preconditions: Files updated
    Steps:
      1. `grep -c '/posts/' content/visas/spain/digital-nomad-visa/consulate-via-bls-london/index.md`
      2. `grep -Eo '/(posts|visas|guides|traps|ui)/' content/visas/spain/digital-nomad-visa/consulate-via-bls-london/index.md | wc -l`
    Expected Result: count >= 1
    Evidence: Terminal output

- [ ] 10. Guides batch

  **What to do**:
  - Update guides to include evidence-first structure, FAQ frontmatter (where required), and link matrix requirements.
  - Target files:
    - `content/guides/compliance-status-meaning.md`
    - `content/guides/how-to-choose-dnv-insurance.md`
    - `content/guides/how-to-read-results.md`
    - `content/guides/schengen-30000-insurance.md`

  **Must NOT do**:
  - No new guides or new content types.

  **Recommended Agent Profile**:
  - **Category**: writing
  - **Skills**: ["doc-coauthoring"]

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3
  - **Blocks**: Task 9
  - **Blocked By**: Tasks 2, 3, 4a, 4b

  **References**:
  - `content/guides/*.md`
  - `tools/seo_thresholds.json` - required links + FAQ requirements

  **Acceptance Criteria**:
  - `python3 tools/lint_content.py --path content/guides/compliance-status-meaning.md` -> OK
  - `python3 tools/lint_content.py --path content/guides/how-to-choose-dnv-insurance.md` -> OK
  - `python3 tools/lint_content.py --path content/guides/how-to-read-results.md` -> OK
  - `python3 tools/lint_content.py --path content/guides/schengen-30000-insurance.md` -> OK
  - `python3 tools/seo_audit.py --config tools/seo_thresholds.json` -> pass
  - Each guide includes /ui/ and at least one of /posts/ or /visas/

  **Agent-Executed QA Scenarios**:
  Scenario: Verify guide link requirements
    Tool: Bash
    Preconditions: Files updated
    Steps:
      1. `grep -c '/ui/' content/guides/how-to-choose-dnv-insurance.md`
      2. `grep -Eo '/(posts|visas)/' content/guides/how-to-choose-dnv-insurance.md | wc -l`
    Expected Result: /ui/ present and at least one posts/visas link
    Evidence: Terminal output

- [ ] 9. Final QA + indexing requests

  **What to do**:
  - Run full lint and SEO audit.
  - Build site and verify FAQPage schema presence for FAQ pages.
  - Verify sitemap contains updated URLs.
  - Request indexing for homepage + 2-3 core pages.

  **Must NOT do**:
  - Do not request indexing for every page; only core pages.

  **Recommended Agent Profile**:
  - **Category**: writing
  - **Skills**: ["verification-before-completion", "playwright"]
    - playwright: for GSC indexing requests if credentials exist

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 3
  - **Blocks**: None
  - **Blocked By**: Tasks 3-8, 10

  **References**:
  - `docs/ops/gsc-indexing-checklist.md` - indexing sanity checks

  **Acceptance Criteria**:
  - `python3 tools/lint_content.py` -> exit 0
  - `python3 tools/seo_audit.py --config tools/seo_thresholds.json` -> exit 0
  - `hugo --quiet` -> exit 0
  - `grep -l 'FAQPage' public/posts/*/index.html` -> returns at least 3 files
  - `grep -c '<url>' public/sitemap.xml` -> count >= number of updated pages
  - Canonical tag sanity check for 3 sample pages (no duplicated baseURL)

  **Agent-Executed QA Scenarios**:
  Scenario: Build and verify FAQ schema
    Tool: Bash
    Preconditions: Hugo installed
    Steps:
      1. Run `hugo --quiet`
      2. Run `grep -l 'FAQPage' public/posts/*/index.html`
    Expected Result: At least 3 FAQPage outputs found
    Evidence: Terminal output
  Scenario: Canonical sanity check
    Tool: Bash
    Preconditions: Hugo build complete
    Steps:
      1. `grep -n '<link rel="canonical"' public/posts/spain-dnv-insurance/index.html`
      2. `grep -n 'https://visafact.org/https://visafact.org' public/posts/spain-dnv-insurance/index.html`
    Expected Result: Canonical present; no double baseURL string
    Evidence: Terminal output

---

## Commit Strategy

Use semantic prefixes per repo guidelines: `docs:` for content updates.

| After Task | Message | Files | Verification |
|------------|---------|-------|--------------|
| 3 | `docs: expand spain and portugal route posts` | content/posts/... | lint + SEO + editorial |
| 4a | `docs: expand germany and thailand route posts` | content/posts/... | lint + SEO + editorial |
| 4b | `docs: expand malta and costa-rica route posts` | content/posts/... | lint + SEO + editorial |
| 5 | `docs: update comparison and rejected posts` | content/posts/... | lint + SEO audit |
| 6 | `docs: deepen regional hub posts` | content/posts/... | lint + SEO audit |
| 7 | `docs: update traps content` | content/traps/... | lint + SEO audit |
| 8 | `docs: update visa route pages` | content/visas/... | lint + SEO audit |
| 10 | `docs: update guides content` | content/guides/... | lint + SEO audit |

---

## Success Criteria

### Verification Commands
```bash
python3 tools/lint_content.py
python3 tools/seo_audit.py --config tools/seo_thresholds.json
python3 tools/check_editorial_targets.py
hugo --quiet
```

### Final Checklist
- [ ] All updated pages pass lint and SEO audit
- [ ] Internal link matrix applied across content types
- [ ] Evidence logs present on all non-_index.md pages
- [ ] Word counts within target editorial ranges (`python3 tools/check_editorial_targets.py` -> exit 0)
- [ ] No URL/slug changes (paths and slugs unchanged)
- [ ] Monetization placements comply with compliance-first rules
- [ ] No new routes or UI changes introduced
