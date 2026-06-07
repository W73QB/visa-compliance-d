# 90-Day Implementation Roadmap — 5 Priority Routes

_Week-by-week execution plan for publishing the 5 routes selected in `expansion_roadmap.md`. All file paths are absolute. Today: 2026-06-07. Week 1 starts 2026-06-09 (Monday)._

---

## Overview

| Week | Dates | Focus | Route | Deliverable |
|---|---|---|---|---|
| 1 | Jun 09–13 | Evidence acquisition | Greece DNV | Source document obtained and saved |
| 2 | Jun 16–20 | Data build | Greece DNV | visa_facts.json + product mappings |
| 3 | Jun 23–27 | Content publishing | Greece DNV | Visa page + hub page + post live |
| 4 | Jun 30–Jul 04 | Evidence acquisition | Japan DNV | Source document obtained and saved |
| 5 | Jul 07–11 | Data build | Japan DNV | visa_facts.json + product mappings |
| 6 | Jul 14–18 | Content publishing | Japan DNV | Visa page + hub page + post live |
| 7 | Jul 21–25 | Evidence acquisition | Colombia DNV | Source document obtained and saved |
| 8 | Jul 28–Aug 01 | Data build | Colombia DNV | visa_facts.json + product mappings |
| 9 | Aug 04–08 | Content publishing | Colombia DNV | Visa page + hub page + post live |
| 10 | Aug 11–15 | Evidence + data build | Spain NLV | Source + visa_facts.json + mappings |
| 11 | Aug 18–22 | Content publishing | Spain NLV | Visa page + hub page + post |
| 12 | Aug 25–29 | Evidence + data + content | Italy Freelance | All deliverables (simpler requirement) |

---

## Week 1 (Jun 09–13) — Greece DNV: Evidence acquisition

**Goal**: Locate, download, and register the official Greek consulate insurance requirement document.

**Tasks**:
1. Find the official Greek Ministry of Digital Governance or consulate requirements page for the Digital Nomad Visa (Law 4825/2021 article 18 or subsequent circular).
2. Download the source document (PDF or HTML) to `/Users/admin/visa-compliance-d/sources/GR_DNV_CONSULATE_2026-[DATE].[ext]`.
3. Create the meta file at `/Users/admin/visa-compliance-d/sources/GR_DNV_CONSULATE_2026-[DATE].[ext].meta.json` with fields: `source_id`, `sha256`, `local_path`, `url`, `verified_date`.
4. Run `py tools/validate.py` to confirm the meta file passes schema.

**Output files**:
- `/Users/admin/visa-compliance-d/sources/GR_DNV_CONSULATE_2026-[DATE].[ext]`
- `/Users/admin/visa-compliance-d/sources/GR_DNV_CONSULATE_2026-[DATE].[ext].meta.json`

**Acceptance**: `py tools/validate.py` exits 0; source_id is `GR_DNV_CONSULATE_2026`.

---

## Week 2 (Jun 16–20) — Greece DNV: Data build

**Goal**: Create the visa data file and all product compliance mappings for the Greece DNV route.

**Tasks**:
1. Create directory `/Users/admin/visa-compliance-d/data/visas/GR/DNV/consulate/2026-01-01/`.
2. Write `visa_facts.json` using the structure from `/Users/admin/visa-compliance-d/data/visas/ES/DNV/bls-london/2026-01-12/visa_facts.json` as reference.
3. For each of the 7 active products (ASISA, DKV, GenericInsurer, Genki, SafetyWing, Sanitas, WorldNomads), evaluate compliance against the Greece DNV requirements and create mapping files at `/Users/admin/visa-compliance-d/data/mappings/GR_DNV_CONSULATE_2026__<PRODUCT_ID>.json`.
4. Run `py tools/build_mappings.py` and `py tools/build_index.py`; confirm no errors.
5. Run `py tools/validate.py`; confirm 0 errors.

**Output files**:
- `/Users/admin/visa-compliance-d/data/visas/GR/DNV/consulate/2026-01-01/visa_facts.json`
- `/Users/admin/visa-compliance-d/data/mappings/GR_DNV_CONSULATE_2026__ASISA_HEALTH_RESIDENTS_2026.json`
- `/Users/admin/visa-compliance-d/data/mappings/GR_DNV_CONSULATE_2026__DKV_VISADO_2026.json`
- `/Users/admin/visa-compliance-d/data/mappings/GR_DNV_CONSULATE_2026__GENKI_TRAVELER_2026.json`
- `/Users/admin/visa-compliance-d/data/mappings/GR_DNV_CONSULATE_2026__SAFETYWING_NOMAD_2026.json`
- `/Users/admin/visa-compliance-d/data/mappings/GR_DNV_CONSULATE_2026__SANITAS_MAS_SALUD_SIN_COPAGO_2026.json`
- `/Users/admin/visa-compliance-d/data/mappings/GR_DNV_CONSULATE_2026__WORLDNOMADS_EXPLORER_2026.json`
- `/Users/admin/visa-compliance-d/data/mappings/GR_DNV_CONSULATE_2026__GENERIC_EXPAT_COMPLETE_2026.json`

**Acceptance**: `py tools/validate.py` exits 0; checker UI shows Greece route with at least 1 GREEN.

---

## Week 3 (Jun 23–27) — Greece DNV: Content publishing

**Goal**: Publish the authority-level visa page, the hub page, and the blog post for Greece DNV.

**Tasks**:
1. Create `/Users/admin/visa-compliance-d/content/visas/greece/` directory structure.
2. Write `/Users/admin/visa-compliance-d/content/visas/greece/digital-nomad-visa/_index.md` (hub page) using the Spain hub page at `/Users/admin/visa-compliance-d/content/visas/spain/digital-nomad-visa/_index.md` as structural reference.
3. Write `/Users/admin/visa-compliance-d/content/visas/greece/digital-nomad-visa/consulate/index.md` using `docs/expansion/content_template_visa.md` with visa_id=`GR_DNV_CONSULATE_2026`.
4. Write `/Users/admin/visa-compliance-d/content/posts/greece-dnv-insurance.md` using `docs/expansion/content_template_post.md`.
5. Run `py tools/lint_content.py`; confirm 0 errors for all 3 files.
6. Run the banned-word audit grep (see expansion plan Verification Strategy) against all published content files; confirm 0 matches.
7. Confirm `snapshot="releases/2026-01-15"` present in all `{{< checker_cta >}}` calls.
8. Run `py tools/sync_hugo_static.py` and test Hugo build locally.

**Output files**:
- `/Users/admin/visa-compliance-d/content/visas/greece/digital-nomad-visa/_index.md`
- `/Users/admin/visa-compliance-d/content/visas/greece/digital-nomad-visa/consulate/index.md`
- `/Users/admin/visa-compliance-d/content/posts/greece-dnv-insurance.md`

**Acceptance**: `py tools/lint_content.py` exits 0; Hugo build succeeds; checker shows Greece route in UI.

---

## Week 4 (Jun 30–Jul 04) — Japan DNV: Evidence acquisition

**Goal**: Locate and register the official Japanese consulate insurance requirement document.

**Tasks**:
1. Download the Chicago Japanese consulate PDF (https://www.chicago.us.emb-japan.go.jp/Consular/visa/downloadable/nomad.pdf) or equivalent consulate circular.
2. Save to `/Users/admin/visa-compliance-d/sources/JP_DNV_CONSULATE_2026-[DATE].pdf`.
3. Create meta file at `/Users/admin/visa-compliance-d/sources/JP_DNV_CONSULATE_2026-[DATE].pdf.meta.json`.
4. Verify the ¥10,000,000 minimum and explicit Japan coverage requirement are confirmed at a specific page/item locator.
5. Run `py tools/validate.py`; confirm no errors.

**Output files**:
- `/Users/admin/visa-compliance-d/sources/JP_DNV_CONSULATE_2026-[DATE].pdf`
- `/Users/admin/visa-compliance-d/sources/JP_DNV_CONSULATE_2026-[DATE].pdf.meta.json`

**Acceptance**: `py tools/validate.py` exits 0; source_id is `JP_DNV_CONSULATE_2026`; ¥10M minimum locator confirmed.

---

## Week 5 (Jul 07–11) — Japan DNV: Data build

**Goal**: Create visa data and compliance mappings for Japan DNV.

**Tasks** (same pattern as Week 2 for Greece):
1. Create `/Users/admin/visa-compliance-d/data/visas/JP/DNV/consulate/2026-01-01/`.
2. Write `visa_facts.json`. Key encoding note: the ¥10M threshold is a numeric minimum that must be expressed in the mapping evaluation; SafetyWing ($250k ≈ ¥37M) and Genki Traveler (€1M ≈ ¥160M) each exceed the threshold when converted at current rates — document the conversion assumption and its date.
3. Create mapping files for all 7 products. ASISA / DKV / Sanitas are expected RED (Spanish-only authorization); SafetyWing and Genki expected GREEN (worldwide coverage including Japan, coverage exceeds ¥10M).
4. Run `py tools/build_mappings.py`, `py tools/build_index.py`, `py tools/validate.py`; confirm 0 errors.

**Output files** (same pattern as Week 2, prefix `JP_DNV_CONSULATE_2026`):
- `/Users/admin/visa-compliance-d/data/visas/JP/DNV/consulate/2026-01-01/visa_facts.json`
- `/Users/admin/visa-compliance-d/data/mappings/JP_DNV_CONSULATE_2026__GENKI_TRAVELER_2026.json`
- `/Users/admin/visa-compliance-d/data/mappings/JP_DNV_CONSULATE_2026__SAFETYWING_NOMAD_2026.json`
- `/Users/admin/visa-compliance-d/data/mappings/JP_DNV_CONSULATE_2026__WORLDNOMADS_EXPLORER_2026.json`
- `/Users/admin/visa-compliance-d/data/mappings/JP_DNV_CONSULATE_2026__ASISA_HEALTH_RESIDENTS_2026.json`
- `/Users/admin/visa-compliance-d/data/mappings/JP_DNV_CONSULATE_2026__DKV_VISADO_2026.json`
- `/Users/admin/visa-compliance-d/data/mappings/JP_DNV_CONSULATE_2026__SANITAS_MAS_SALUD_SIN_COPAGO_2026.json`
- `/Users/admin/visa-compliance-d/data/mappings/JP_DNV_CONSULATE_2026__GENERIC_EXPAT_COMPLETE_2026.json`

**Acceptance**: `py tools/validate.py` exits 0; Japan route shows GREEN for SafetyWing and Genki.

---

## Week 6 (Jul 14–18) — Japan DNV: Content publishing

**Goal**: Publish Japan DNV visa page, hub page, and post.

**Output files**:
- `/Users/admin/visa-compliance-d/content/visas/japan/digital-nomad-visa/_index.md`
- `/Users/admin/visa-compliance-d/content/visas/japan/digital-nomad-visa/consulate/index.md`
- `/Users/admin/visa-compliance-d/content/posts/japan-dnv-insurance.md`

**Acceptance**: Same checks as Week 3 (lint, banned-word grep, snapshot presence, Hugo build).

---

## Week 7 (Jul 21–25) — Colombia DNV: Evidence acquisition

**Goal**: Locate and register the official Cancillería de Colombia insurance requirement document.

**Tasks**:
1. Find the Cancillería de Colombia Digital Nomad Visa resolution or requirements page (Resolution 5477 or subsequent update).
2. Download the source document and save to `/Users/admin/visa-compliance-d/sources/CO_DNV_CANCILLERIA_2026-[DATE].[ext]`.
3. Confirm "All-Risk" insurance requirement and Colombia-specific coverage language are at a specific locator.
4. Create meta file and run `py tools/validate.py`.

**Output files**:
- `/Users/admin/visa-compliance-d/sources/CO_DNV_CANCILLERIA_2026-[DATE].[ext]`
- `/Users/admin/visa-compliance-d/sources/CO_DNV_CANCILLERIA_2026-[DATE].[ext].meta.json`

**Acceptance**: `py tools/validate.py` exits 0; "All-Risk" language confirmed at locator.

---

## Week 8 (Jul 28–Aug 01) — Colombia DNV: Data build

**Output files** (prefix `CO_DNV_CANCILLERIA_2026`):
- `/Users/admin/visa-compliance-d/data/visas/CO/DNV/cancilleria/2026-01-01/visa_facts.json`
- `/Users/admin/visa-compliance-d/data/mappings/CO_DNV_CANCILLERIA_2026__GENKI_TRAVELER_2026.json`
- `/Users/admin/visa-compliance-d/data/mappings/CO_DNV_CANCILLERIA_2026__SAFETYWING_NOMAD_2026.json`
- `/Users/admin/visa-compliance-d/data/mappings/CO_DNV_CANCILLERIA_2026__WORLDNOMADS_EXPLORER_2026.json`
- `/Users/admin/visa-compliance-d/data/mappings/CO_DNV_CANCILLERIA_2026__ASISA_HEALTH_RESIDENTS_2026.json`
- `/Users/admin/visa-compliance-d/data/mappings/CO_DNV_CANCILLERIA_2026__DKV_VISADO_2026.json`
- `/Users/admin/visa-compliance-d/data/mappings/CO_DNV_CANCILLERIA_2026__SANITAS_MAS_SALUD_SIN_COPAGO_2026.json`
- `/Users/admin/visa-compliance-d/data/mappings/CO_DNV_CANCILLERIA_2026__GENERIC_EXPAT_COMPLETE_2026.json`

**Acceptance**: `py tools/validate.py` exits 0; Colombia route shows GREEN for Genki and SafetyWing.

---

## Week 9 (Aug 04–08) — Colombia DNV: Content publishing

**Output files**:
- `/Users/admin/visa-compliance-d/content/visas/colombia/digital-nomad-visa/_index.md`
- `/Users/admin/visa-compliance-d/content/visas/colombia/digital-nomad-visa/cancilleria/index.md`
- `/Users/admin/visa-compliance-d/content/posts/colombia-dnv-insurance.md`

**Acceptance**: Same checks as Week 3 and Week 6.

---

## Week 10 (Aug 11–15) — Spain NLV: Evidence + data build (combined, faster due to Spain familiarity)

**Goal**: Acquire source, build data files for Spain NLV. Spain NLV requirements are similar to Spain DNV; the main differences are that no specific consulate route is listed and ASISA/DKV/Sanitas are expected GREEN.

**Tasks**:
1. Download the Spanish consulate NLV checklist (equivalent to the BLS London checklist used for DNV) and save to `/Users/admin/visa-compliance-d/sources/ES_NLV_CONSULATE_2026-[DATE].[ext]`.
2. Create `/Users/admin/visa-compliance-d/data/visas/ES/NLV/consulate/2026-01-01/visa_facts.json`.
3. Create mapping files (prefix `ES_NLV_CONSULATE_2026`); ASISA, DKV, Sanitas expected GREEN; SafetyWing/Genki/WorldNomads expected RED (not Spanish-authorized carriers).
4. Run `py tools/build_mappings.py`, `py tools/build_index.py`, `py tools/validate.py`.

**Output files**:
- `/Users/admin/visa-compliance-d/sources/ES_NLV_CONSULATE_2026-[DATE].[ext]`
- `/Users/admin/visa-compliance-d/sources/ES_NLV_CONSULATE_2026-[DATE].[ext].meta.json`
- `/Users/admin/visa-compliance-d/data/visas/ES/NLV/consulate/2026-01-01/visa_facts.json`
- `/Users/admin/visa-compliance-d/data/mappings/ES_NLV_CONSULATE_2026__ASISA_HEALTH_RESIDENTS_2026.json`
- `/Users/admin/visa-compliance-d/data/mappings/ES_NLV_CONSULATE_2026__DKV_VISADO_2026.json`
- `/Users/admin/visa-compliance-d/data/mappings/ES_NLV_CONSULATE_2026__SANITAS_MAS_SALUD_SIN_COPAGO_2026.json`
- `/Users/admin/visa-compliance-d/data/mappings/ES_NLV_CONSULATE_2026__GENKI_TRAVELER_2026.json`
- `/Users/admin/visa-compliance-d/data/mappings/ES_NLV_CONSULATE_2026__SAFETYWING_NOMAD_2026.json`
- `/Users/admin/visa-compliance-d/data/mappings/ES_NLV_CONSULATE_2026__WORLDNOMADS_EXPLORER_2026.json`
- `/Users/admin/visa-compliance-d/data/mappings/ES_NLV_CONSULATE_2026__GENERIC_EXPAT_COMPLETE_2026.json`

**Acceptance**: `py tools/validate.py` exits 0; Spain NLV route shows GREEN for ASISA/DKV/Sanitas.

---

## Week 11 (Aug 18–22) — Spain NLV: Content publishing

**Output files**:
- `/Users/admin/visa-compliance-d/content/visas/spain/non-lucrative-visa/_index.md`
- `/Users/admin/visa-compliance-d/content/visas/spain/non-lucrative-visa/consulate/index.md`
- `/Users/admin/visa-compliance-d/content/posts/spain-nlv-insurance.md`

**Acceptance**: Same checks as prior publishing weeks; confirm no duplicate of Spain DNV content is introduced.

---

## Week 12 (Aug 25–29) — Italy Self-Employment Visa: All deliverables

**Goal**: Complete evidence, data, and content for Italy in one week. Requirement is simpler (€30k minimum, 30 days, worldwide products qualify).

**Tasks**:
1. Download Italian consulate self-employment visa checklist and save to `/Users/admin/visa-compliance-d/sources/IT_FREELANCE_CONSULATE_2026-[DATE].[ext]`.
2. Create meta file; run `py tools/validate.py`.
3. Create `/Users/admin/visa-compliance-d/data/visas/IT/FREELANCE/consulate/2026-01-01/visa_facts.json`.
4. Create mapping files (prefix `IT_FREELANCE_CONSULATE_2026`); SafetyWing, Genki, WorldNomads expected GREEN ($250k / €1M / per-trip coverage all exceed €30k minimum); ASISA/DKV/Sanitas expected UNKNOWN (Italian authorization not documented in current product evidence).
5. Run `py tools/build_mappings.py`, `py tools/build_index.py`, `py tools/validate.py`.
6. Write content files and run all publication checks.

**Output files**:
- `/Users/admin/visa-compliance-d/sources/IT_FREELANCE_CONSULATE_2026-[DATE].[ext]`
- `/Users/admin/visa-compliance-d/sources/IT_FREELANCE_CONSULATE_2026-[DATE].[ext].meta.json`
- `/Users/admin/visa-compliance-d/data/visas/IT/FREELANCE/consulate/2026-01-01/visa_facts.json`
- `/Users/admin/visa-compliance-d/data/mappings/IT_FREELANCE_CONSULATE_2026__SAFETYWING_NOMAD_2026.json`
- `/Users/admin/visa-compliance-d/data/mappings/IT_FREELANCE_CONSULATE_2026__GENKI_TRAVELER_2026.json`
- `/Users/admin/visa-compliance-d/data/mappings/IT_FREELANCE_CONSULATE_2026__WORLDNOMADS_EXPLORER_2026.json`
- `/Users/admin/visa-compliance-d/data/mappings/IT_FREELANCE_CONSULATE_2026__ASISA_HEALTH_RESIDENTS_2026.json`
- `/Users/admin/visa-compliance-d/data/mappings/IT_FREELANCE_CONSULATE_2026__DKV_VISADO_2026.json`
- `/Users/admin/visa-compliance-d/data/mappings/IT_FREELANCE_CONSULATE_2026__SANITAS_MAS_SALUD_SIN_COPAGO_2026.json`
- `/Users/admin/visa-compliance-d/data/mappings/IT_FREELANCE_CONSULATE_2026__GENERIC_EXPAT_COMPLETE_2026.json`
- `/Users/admin/visa-compliance-d/content/visas/italy/self-employment-visa/_index.md`
- `/Users/admin/visa-compliance-d/content/visas/italy/self-employment-visa/consulate/index.md`
- `/Users/admin/visa-compliance-d/content/posts/italy-freelance-insurance.md`

**Acceptance**: `py tools/validate.py` exits 0; Italy route shows GREEN for SafetyWing, Genki, WorldNomads; Hugo build succeeds; lint exits 0.

---

## Cross-route checklist (apply to every publishing week)

- [ ] `py tools/validate.py` exits 0
- [ ] `py tools/lint_content.py` exits 0
- [ ] Banned-word audit grep (expansion plan Verification Strategy) against all new content files returns 0 matches
- [ ] `grep -c 'snapshot="releases/2026-01-15"'` returns ≥ 1 per content file with `checker_cta`
- [ ] All 5 required sections present: "What the authority requires", "How we evaluate", "Check in the engine", "Disclaimer + Affiliate disclosure"
- [ ] Affiliate links present only if at least one GREEN mapping file exists for the route
- [ ] Hugo build (`pwsh -File tools/build_hugo.ps1`) exits 0
- [ ] New visa ID appears in `data/ui_index.json` after `py tools/build_index.py`

---

## Route cross-reference table

| Visa ID | expansion_roadmap.md Route | 90_day_roadmap.md Weeks |
|---|---|---|
| `GR_DNV_CONSULATE_2026` | Route 1 | 1–3 |
| `JP_DNV_CONSULATE_2026` | Route 2 | 4–6 |
| `CO_DNV_CANCILLERIA_2026` | Route 3 | 7–9 |
| `ES_NLV_CONSULATE_2026` | Route 4 | 10–11 |
| `IT_FREELANCE_CONSULATE_2026` | Route 5 | 12 |
