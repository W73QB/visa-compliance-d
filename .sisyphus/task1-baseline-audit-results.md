# Task 1: Baseline Audit + Prioritization - COMPLETE

**Completed**: 2026-02-05  
**Status**: ✅ All acceptance criteria met

## Deliverables

### 1. ✅ Lint + SEO Audit Passed
```bash
$ python3 tools/lint_content.py
# Exit 0 - ALL 34 files PASS

$ python3 tools/seo_audit.py --config tools/seo_thresholds.json
# Exit 0 - SEO audit passed
```

### 2. ✅ Content Completion Matrix Generated

**Summary Stats**:
- Total files tracked: 25
- PASS: 1 (4.0%) - Portugal DNV post only
- FAIL: 24 (96.0%) - Need expansion to meet editorial targets
- OVER: 0 (0.0%)

**Breakdown by Content Type**:
- Route posts: 6/6 need work (Spain, Germany, Thailand, Malta, Costa Rica all below 900 words)
- Comparison/rejected: 2/2 need work (both below 1000 words)
- Regional hubs: 3/3 need work (Europe, Asia, Americas all below 900 words)
- Trap posts: 4/4 need work (all below 700 words)
- Visa route pages: 6/6 need work (all below 900 words)
- Guides: 4/4 need work (all below 400 words)

**Key Finding**: Only 1 file (Portugal DNV post) currently meets editorial targets. 96% of content needs expansion.

### 3. ✅ Monetization Eligibility Matrix Generated

**Affiliate-Eligible Routes** (Genki GREEN/YELLOW):
- ✅ Costa Rica Digital Nomad Visa → Genki GREEN
- ✅ Portugal E11 Remote Work Visa → Genki GREEN

**Non-Eligible Routes** (Genki RED/UNKNOWN/NOT_REQUIRED):
- ❌ Spain DNV → Genki RED (deductible + coverage cap fails)
- ❌ Germany Freelance Visa → Genki UNKNOWN (product type unclear)
- ❌ Malta Nomad Residency → Genki UNKNOWN (payment cadence unclear)
- ❌ Thailand DTV → Genki NOT_REQUIRED (insurance not mandatory)

**Monetization Strategy**:
- **Affiliate CTAs allowed**: Costa Rica + Portugal content only (2/6 routes = 33%)
- **Non-affiliate CTAs**: Spain, Germany, Malta, Thailand (use official links with "non-affiliate" disclosure)
- **High-traffic non-monetizable pages**: Candidates for ads/lead-gen (if traffic warrants)

### 4. ✅ Prioritization List (Top 6 Pages to Rewrite First)

Ranked by proxy scoring (word count gap + route importance + monetization potential):

1. **content/posts/costa-rica-dn-insurance.md** (Score: 132.0)
   - Gap: 603 words to minimum
   - Monetization: ✅ Genki affiliate eligible
   - Route importance: High (route post)

2. **content/visas/thailand/digital-nomad-visa-dtv/thai-e-visa/index.md** (Score: 121.8)
   - Gap: 646 words to minimum
   - Route importance: Highest (visa route page)

3. **content/visas/malta/nomad-residence-permit/residency-malta-agency/index.md** (Score: 118.3)
   - Gap: 615 words to minimum
   - Route importance: Highest (visa route page)

4. **content/visas/germany/freelance-visa-national-d/embassy-london/index.md** (Score: 117.0)
   - Gap: 603 words to minimum
   - Route importance: Highest (visa route page)

5. **content/posts/malta-nomad-insurance.md** (Score: 115.4)
   - Gap: 679 words to minimum
   - Route importance: High (route post)

6. **content/visas/costa-rica/digital-nomad-visa/executive-decree-43619/index.md** (Score: 113.3)
   - Gap: 570 words to minimum
   - Monetization: ✅ Genki affiliate eligible
   - Route importance: Highest (visa route page)

**Note**: Portugal DNV content excluded from prioritization (already meets targets).

### 5. ✅ Editorial Enforcement Tools Created

**Created Files**:
- `tools/editorial_targets.json` - Per-file [min, max] word count ranges for all 25 files
- `tools/check_editorial_targets.py` - Enforcement script (reuses `word_count()` from `seo_audit.py`)
- `tools/generate_baseline_audit.py` - Complete baseline audit generator (matrices + prioritization)

**Usage**:
```bash
# Check editorial compliance
python3 tools/check_editorial_targets.py
# Exit 1 if any file outside [min, max] range, Exit 0 if all pass

# Regenerate audit matrices
python3 tools/generate_baseline_audit.py
# Outputs: completion matrix, monetization matrix, prioritization list
```

**Integration Point**: `tools/check_editorial_targets.py` can be added to CI workflow after content rewrites complete.

## Next Steps (Task 2)

With baseline audit complete, proceed to **Task 2: Hub/Spoke Link Matrix + Per-Page Link Targets**.

Task 2 will define:
- Internal linking architecture (hub pages → spoke pages)
- Per-page link targets (how many internal links each page should have)
- Link matrix specification (which pages link to which)

This linking architecture will then be implemented during content rewrites (Tasks 3-8).

## Acceptance Criteria Status

- [x] `python3 tools/lint_content.py` → exit 0
- [x] `python3 tools/seo_audit.py --config tools/seo_thresholds.json` → exit 0
- [x] Completion matrix produced ✓ or ✗ per file
- [x] Monetization eligibility matrix: Genki compliance per route + where affiliate CTA allowed
- [x] Prioritization list: top 6 pages to update first
- [x] `tools/editorial_targets.json` created
- [x] `tools/check_editorial_targets.py` created and runnable

**Task 1: COMPLETE** ✅
