# Expansion Roadmap — 5 Priority Routes (2026)

_Produced from keyword research (2026-06-07) and repo audit. Routes chosen from Priority A keywords where: (1) insurance is mandatory per authority sources, (2) specific coverage attributes are documentable, (3) products in the current repo are plausibly GREEN, (4) no existing visa page covers the route, (5) search demand signal confirmed in top-3 SERP positions._

> **Deviation note (vs original plan):** The original plan hard-coded 10 keywords (greece, indonesia, italy, croatia, estonia, japan, colombia, albania, portugal-d7, spain-nlv). During execution the keyword set was adjusted based on actual SERP results: croatia, estonia, albania, and portugal-d7 were dropped in favour of netherlands-DAFT, mexico, vietnam, and panama, which surfaced clearer mandatory-insurance signals. Final route selection (Greece, Japan, Colombia, Spain NLV, Italy) was re-prioritised on the same 5 criteria rather than on the plan's original A/B/C labels — Japan and Colombia were Priority B and Spain NLV Priority C in the original plan. Spain NLV and Italy were favoured because they map onto insurers/products that already show GREEN in the repo (Spanish-authorized carriers for NLV; worldwide products clearing the €30k Italian minimum), giving the clearest path to a verifiable GREEN affiliate route. "Products likely GREEN" below remain estimates until `data/mappings/` is built and run.

---

## Selected pick: URL Structure Option C

**Option C: Both hub (country-level `content/visas/<country>/` group page) AND detail (authority-level `content/visas/<country>/<visa-type>/<authority>/index.md`) pages.**

**Rationale**: This matches the existing repo pattern exactly. Every current country has both a group page (`content/visas/spain/digital-nomad-visa/_index.md`) and one or more authority-level pages (`content/visas/spain/digital-nomad-visa/consulate-via-bls-london/index.md`). Each country also has a paired blog post (`content/posts/spain-dnv-insurance/`). Deviating from this pattern would create structural inconsistency in the Hugo site and break the existing linking conventions. Option A (detail only) would miss the hub-level SEO signal; Option B (hub only) would miss the per-route evidence specificity that makes visafact.org distinct from competitors.

---

## The 5 selected routes

### Route 1: Greece Digital Nomad Visa — Consulate route

| Field | Value |
|---|---|
| Visa ID | `GR_DNV_CONSULATE_2026` |
| Country | Greece |
| Visa type | Digital Nomad Visa (DNV) |
| Authority | Greek consulate (general) |
| Year | 2026 |
| Data path | `data/visas/GR/DNV/consulate/2026-01-01/visa_facts.json` |
| Content path (detail) | `content/visas/greece/digital-nomad-visa/consulate/index.md` |
| Content path (hub) | `content/visas/greece/digital-nomad-visa/_index.md` |
| Post path | `content/posts/greece-dnv-insurance.md` |
| Insurance mandatory | YES — private health insurance from authorized provider required, valid full duration |
| Coverage attributes documented | Medical emergencies, hospitalization, repatriation; authorized in Greece; comprehensive coverage equivalent to public healthcare standards |
| Products likely GREEN | SafetyWing Nomad Insurance (covers 175+ countries including Greece, $250k coverage, no deductible outside US), Genki Traveler (€1M coverage, worldwide including Greece), WorldNomads Explorer |
| Priority keyword | "greece digital nomad visa insurance" |
| SERP gap | None of the top 3 URLs is a dedicated compliance-checker tool; all are narrative guides |
| Evidence to obtain | Official Greek consulate checklist or GSEE/Ministry of Digital Governance document listing insurance requirements with locator |

---

### Route 2: Japan Digital Nomad Visa — Consulate route

| Field | Value |
|---|---|
| Visa ID | `JP_DNV_CONSULATE_2026` |
| Country | Japan |
| Visa type | Digital Nomad Visa (DNV) |
| Authority | Japanese consulate (general) |
| Year | 2026 |
| Data path | `data/visas/JP/DNV/consulate/2026-01-01/visa_facts.json` |
| Content path (detail) | `content/visas/japan/digital-nomad-visa/consulate/index.md` |
| Content path (hub) | `content/visas/japan/digital-nomad-visa/_index.md` |
| Post path | `content/posts/japan-dnv-insurance.md` |
| Insurance mandatory | YES — private health insurance mandatory; no eligibility for Japan National Health Insurance |
| Coverage attributes documented | Minimum ¥10 million medical treatment coverage; must cover Japan explicitly; death, injury, and illness; policy certificate and summary required |
| Products likely GREEN | SafetyWing Nomad Insurance (~$250k ≈ ¥37M, exceeds ¥10M threshold; Japan in coverage territory), Genki Traveler (€1M ≈ ¥160M, worldwide coverage including Japan) |
| Priority keyword | "japan digital nomad visa insurance" |
| SERP gap | Genki and SafetyWing each have dedicated Japan landing pages; no neutral compliance-checker tool in top 3 |
| Evidence to obtain | Chicago Japanese consulate PDF (DIGITAL NOMAD REQUIREMENTS, https://www.chicago.us.emb-japan.go.jp/Consular/visa/downloadable/nomad.pdf) or equivalent official source; locator to specific line item |

---

### Route 3: Colombia Digital Nomad Visa — Cancillería route

| Field | Value |
|---|---|
| Visa ID | `CO_DNV_CANCILLERIA_2026` |
| Country | Colombia |
| Visa type | Digital Nomad Visa (DNV) |
| Authority | Cancillería de Colombia |
| Year | 2026 |
| Data path | `data/visas/CO/DNV/cancilleria/2026-01-01/visa_facts.json` |
| Content path (detail) | `content/visas/colombia/digital-nomad-visa/cancilleria/index.md` |
| Content path (hub) | `content/visas/colombia/digital-nomad-visa/_index.md` |
| Post path | `content/posts/colombia-dnv-insurance.md` |
| Insurance mandatory | YES — private health insurance ("All-Risk") valid in Colombia required; travel insurance NOT accepted as of 2026 |
| Coverage attributes documented | Colombia explicitly named in policy; accident, illness, maternity, disability, hospitalization, death, repatriation; minimum 1-year validity; duration matching visa period |
| Products likely GREEN | Genki Traveler (worldwide including Colombia, no specific Colombia exclusion documented), SafetyWing Nomad Insurance (175+ countries, Colombia included) |
| Priority keyword | "colombia digital nomad visa insurance" |
| SERP gap | Top results are visa guide sites and Genki's own landing page; no neutral per-product compliance tool |
| Evidence to obtain | Cancillería resolution or official checklist document naming "All-Risk" insurance; locator to specific article or annex |

---

### Route 4: Spain Non-Lucrative Visa — Consulate route

| Field | Value |
|---|---|
| Visa ID | `ES_NLV_CONSULATE_2026` |
| Country | Spain |
| Visa type | Non-Lucrative Visa (NLV) |
| Authority | Spanish consulate (general) |
| Year | 2026 |
| Data path | `data/visas/ES/NLV/consulate/2026-01-01/visa_facts.json` |
| Content path (detail) | `content/visas/spain/non-lucrative-visa/consulate/index.md` |
| Content path (hub) | `content/visas/spain/non-lucrative-visa/_index.md` |
| Post path | `content/posts/spain-nlv-insurance.md` |
| Insurance mandatory | YES — Spanish-authorized carrier (DGSFP authorized), no copayments, no deductibles, no waiting periods, nationwide coverage, €30k+ coverage |
| Coverage attributes documented | No copays (sin copagos), no waiting periods (sin carencias), nationwide Spain coverage, hospitalization + surgical + outpatient + emergency + repatriation, DGSFP authorization required |
| Products likely GREEN | ASISA, DKV, Sanitas (same carriers as Spain DNV route — data already partially present in repo) |
| Priority keyword | "spain non-lucrative visa insurance" |
| SERP gap | healthinsuranceforspanishvisas.com dominates top results; no compliance-checker tool in top 3; visafact.org currently covers DNV but not NLV |
| Evidence to obtain | Official Spanish consulate NLV checklist with insurance item; DGSFP authorization confirmation; locator to specific requirement item |

---

### Route 5: Italy Self-Employment Visa — Consulate route

| Field | Value |
|---|---|
| Visa ID | `IT_FREELANCE_CONSULATE_2026` |
| Country | Italy |
| Visa type | Self-Employment Visa (Lavoro Autonomo) |
| Authority | Italian consulate (general) |
| Year | 2026 |
| Data path | `data/visas/IT/FREELANCE/consulate/2026-01-01/visa_facts.json` |
| Content path (detail) | `content/visas/italy/self-employment-visa/consulate/index.md` |
| Content path (hub) | `content/visas/italy/self-employment-visa/_index.md` |
| Post path | `content/posts/italy-freelance-insurance.md` |
| Insurance mandatory | YES — private health insurance mandatory; minimum €30,000 coverage; covers first 30 days from entry; replaceable with SSN registration after residence permit obtained |
| Coverage attributes documented | Minimum €30,000 for hospital and medical expenses; covers urgent medical care and hospitalization; valid from entry date |
| Products likely GREEN | SafetyWing Nomad Insurance ($250k coverage, worldwide), Genki Traveler (€1M coverage, worldwide), WorldNomads Explorer (worldwide coverage for short stays) |
| Priority keyword | "italy self-employed visa insurance" |
| SERP gap | Top results are general visa guides; no compliance-checker tool in top 3; Italy freelance/self-employment is underserved in the tool space |
| Evidence to obtain | Italian consulate self-employment visa checklist; official LEXIA or consulate circular stating €30,000 minimum with page/item locator |

---

## URL structure implementation plan (Option C)

For each of the 5 routes, create:

```
content/visas/<country>/              ← country hub (_index.md if not existing)
content/visas/<country>/<visa-type>/  ← visa-type group page (_index.md)
content/visas/<country>/<visa-type>/<authority>/
  └── index.md                        ← authority-level compliance page
content/posts/<country>-<visa-slug>-insurance.md  ← hub blog post
data/visas/<CC>/<VISA>/<authority>/<date>/
  └── visa_facts.json                 ← canonical data (requires future implementation)
data/mappings/<VISA_ID>__<PRODUCT_ID>.json   ← per-product compliance mapping (future)
```

All pages must include `snapshot="releases/2026-01-15"` in every `{{< checker_cta >}}` shortcode until a newer release snapshot is published. When a newer snapshot is available, update this value across all generated pages.
