---
title: "Brazil Digital Nomad Visa (VITEM XIV) insurance requirements (evidence-based)"
date: 2026-06-12
description: "Evidence-based summary of the health insurance requirement for Brazil's Digital Nomad Visa (VITEM XIV): a policy valid in Brazilian territory, per the gov.br consular checklist."
tags: ["brazil", "digital-nomad", "vitem-xiv", "insurance", "compliance"]
faq:
  - question: "What insurance does the Brazil Digital Nomad Visa (VITEM XIV) require?"
    answer: "The gov.br consular checklist requires a health insurance policy valid in Brazilian territory (seguro de saude valido no territorio brasileiro)."
  - question: "Is a minimum coverage amount an official requirement?"
    answer: "No. The official consular checklist states only that the policy must be valid in Brazilian territory; it sets no coverage amount, so the engine leaves any figure UNKNOWN."
  - question: "Why are most travel-medical policies UNKNOWN for this route?"
    answer: "Their policy documents do not state that coverage is valid in Brazilian territory, so the engine records UNKNOWN instead of assuming a foreign policy is valid in Brazil."
---

## Short answer

Brazil's Digital Nomad Visa (VITEM XIV) requires a health insurance policy valid in Brazilian territory: the official consular checklist lists "Seguro de saude valido no territorio brasileiro" among the required documents (Source: `BR_DNV_LISBOA_2026`, gov.br Consulado-Geral do Brasil em Lisboa; verified 2026-06-13). The checklist states no coverage amount and no other policy attributes, so the checker models two rules — insurance is mandatory, and the policy must document validity in Brazilian territory — and leaves everything else UNKNOWN.

## Key findings at a glance

| Item | Value |
|---|---|
| Route | Brazil Digital Nomad Visa, Visto Temporario XIV (VITEM XIV) |
| Authority | Ministerio das Relacoes Exteriores (gov.br), Consulado-Geral em Lisboa |
| Evidence verified | 2026-06-13 |
| Snapshot | 2026-06-13 |
| Modeled rules | Insurance mandatory; policy valid in Brazilian territory |

## What the authority requires

- A health insurance policy is one of the required documents for the VITEM XIV application. (Source: `BR_DNV_LISBOA_2026`; verified 2026-06-13)
- The policy must be valid in Brazilian territory. (Source: `BR_DNV_LISBOA_2026`; verified 2026-06-13)
- The official checklist states no coverage amount, no deductible rule and no insurer-authorization list, so those stay UNKNOWN.

Normalized requirements table:

| Requirement | Source URL | Locator | Verified date |
|---|---|---|---|
| Insurance is mandatory | https://www.gov.br/mre/pt-br/consulado-lisboa/servicos-consulares/vistos-destinados-a-estrangeiros-para-entrada-no-brasil/visto-temporario-xiv-2013-nomade-digital-vitem-xiv | Required documents, item 4 | 2026-06-13 |
| Policy valid in Brazilian territory | https://www.gov.br/mre/pt-br/consulado-lisboa/servicos-consulares/vistos-destinados-a-estrangeiros-para-entrada-no-brasil/visto-temporario-xiv-2013-nomade-digital-vitem-xiv | Required documents, item 4 | 2026-06-13 |

## Verified requirements (PASS/FAIL/UNKNOWN)

| Requirement | Status | Evidence |
|---|---|---|
| Insurance is mandatory | PASS | gov.br consular checklist, item 4 |
| Policy valid in Brazilian territory | PASS only for products documenting Brazil coverage; UNKNOWN otherwise | Checklist: "Seguro de saude valido no territorio brasileiro" |
| Minimum coverage amount | UNKNOWN | Not stated in the official checklist |

## How we evaluate

The checker compares each modeled requirement against product evidence. Two rules are encoded from the gov.br consular checklist: insurance is mandatory, and the policy must be valid in Brazilian territory. A product is only credited with Brazil validity when its own documentation states coverage that includes Brazil; the engine does not assume that a worldwide or home-country policy is valid in Brazilian territory. Products whose documents are silent about Brazil stay UNKNOWN rather than GREEN — the UNKNOWN > Wrong principle. See /methodology/ for the full logic.

Note for travelers comparing sources: some third-party guides quote coverage amounts for this visa. The official consular checklist used here states no figure, so the engine encodes none.

## Proof package checklist

- A health insurance certificate whose territory of coverage explicitly includes Brazil.
- Policy holder name, policy number and coverage dates matching the application.
- The remaining VITEM XIV documents per the consular checklist (digital-nomad declaration, work contract or service agreement with a foreign employer, proof of foreign-source income, criminal record certificate).
- After arrival, registration with the Policia Federal within 90 days, per the same checklist.

## FAQ

**Q: What insurance is required?**
**A:** A health insurance policy valid in Brazilian territory (Source: `BR_DNV_LISBOA_2026`; verified 2026-06-13).

**Q: Is there an official minimum coverage amount?**
**A:** No. The official checklist states no figure, so the engine leaves the amount UNKNOWN.

**Q: Why is Genki Native GREEN while travel-medical products are UNKNOWN?**
**A:** Genki Native's documentation states global coverage including Brazil; the other products' documents do not state Brazil validity, so they stay UNKNOWN.

## Check in the engine

Use [the compliance checker](/ui/) with the current snapshot for this route:

{{< checker_cta visa="BR_DNV_LISBOA_2026" product="GENKI_NATIVE_2026" snapshot="2026-06-13" >}}

## Related reading

- [Brazil VITEM XIV requirements (route page)](/visas/brazil/digital-nomad-visa-vitem-xiv/visto-temporario-xiv-gov-br-lisboa/)
- [Digital nomad insurance in the Americas](/posts/digital-nomad-insurance-americas/)
- [How to read compliance results](/guides/how-to-read-results/)

## Where to find compliant insurance for the Brazil Digital Nomad Visa

The official requirement is a health policy valid in Brazilian territory, so what matters is documented Brazil coverage, not a price or a brand. In the current snapshot, Genki Native shows GREEN: it is an international health policy whose documentation states global coverage that includes Brazil. The travel-medical products show UNKNOWN because their documents do not state validity in Brazilian territory.

- [Genki Native](https://genki.world/products/native) — paid link. We may earn a commission if you purchase through this link.

> Use the compliance checker to confirm the current GREEN products for this route before you buy.

## Disclaimer + Affiliate disclosure

Not legal advice. Compliance results are evidence-based snapshots.

If an affiliate link is present, it appears only after results and does not change the compliance outcome. The Genki link above is a paid affiliate link.

Last updated: 2026-06-13

## Evidence log

- Source: BR_DNV_LISBOA_2026
