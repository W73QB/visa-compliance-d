---
title: "Bulgaria Long-stay Visa D - Long-stay Visa D (whole period of stay) - Ministry of Foreign Affairs"
visa_id: "BG_LONGSTAYD_MFA_2026"
last_verified: "2026-06-17"
source_ids: ["BG_LONGSTAY_MFA_2026"]
description: "Official insurance requirements for Bulgaria Long-stay Visa D via Long-stay Visa D (whole period of stay) - Ministry of Foreign Affairs"
faq:
  - question: "What insurance does a Bulgaria long-stay Visa D require?"
    answer: "The Ministry of Foreign Affairs requires an insurance policy for the whole period of stay, issued by an insurance company licensed in the European Union, with a minimum amount of coverage of 30,000 euros, covering repatriation costs, emergency medical care and emergency hospital treatment."
  - question: "Why is only AXA Schengen Europe Travel GREEN for this route?"
    answer: "The policy must be issued by an insurer licensed in the European Union. AXA Schengen Europe Travel documents an insurer authorized by the National Bank of Belgium with 100,000 euros of medical cover, hospitalization and repatriation; the other products do not document an EU insurance licence, so the engine records UNKNOWN rather than assuming a provider qualifies."
  - question: "Is the 30,000 euro figure the Schengen short-stay rule?"
    answer: "No. The 30,000 euro minimum is stated on the Ministry of Foreign Affairs Visa D (long-term) document for the national long-stay visa, alongside the whole-period and EU-licence conditions, so the engine encodes it for this national route."
---

## Bulgaria Long-stay Visa D

**Route:** Long-stay Visa D (whole period of stay) - Ministry of Foreign Affairs  
**Authority:** Ministry of Foreign Affairs of the Republic of Bulgaria (mfa.bg)  
**Last Verified:** 2026-06-17

## Requirements

| Requirement | Operator | Value | Evidence |
| --- | --- | --- | --- |
| `insurance.mandatory` | `==` | Yes | *VISA D (long term), Documents required in all cases, item 5*: "Insurance policy (and copy) for the whole period of stay, issued by an Insurance..." ([source](/sources/BG_LONGSTAY_MFA_2026-06-17.pdf)) |
| `insurance.min_coverage` | `>=` | 30000 | *VISA D (long term), Documents required in all cases, item 5*: "with a minimum amount of coverage of 30,000 euros..." ([source](/sources/BG_LONGSTAY_MFA_2026-06-17.pdf)) |
| `insurance.must_cover_full_period` | `==` | Yes | *VISA D (long term), Documents required in all cases, item 5*: "Insurance policy (and copy) for the whole period of stay..." ([source](/sources/BG_LONGSTAY_MFA_2026-06-17.pdf)) |
| `insurance.eu_licensed_insurer` | `==` | Yes | *VISA D (long term), Documents required in all cases, item 5*: "issued by an Insurance Company with a license to carry out insurance activities ..." ([source](/sources/BG_LONGSTAY_MFA_2026-06-17.pdf)) |

## Source Documents

- **BG_LONGSTAY_MFA_2026**: [Local copy](/sources/BG_LONGSTAY_MFA_2026-06-17.pdf) | [Original](https://www.mfa.bg/upload/99380/2_Visa_D.pdf) | Retrieved: 2026-06-17

## Related reading

- [Bulgaria long-stay Visa D insurance requirements](/posts/bulgaria-long-stay-visa-insurance/)
- [Digital nomad insurance in Europe](/posts/digital-nomad-insurance-europe/)
- [How to read compliance results](/guides/how-to-read-results/)

## What the authority requires

The points below are taken directly from the official source for the Bulgaria Long-stay Visa D (Long-stay Visa D (whole period of stay) - Ministry of Foreign Affairs) route. Each one is recorded with a source identifier and a locator so it can be traced back to the original document. Where the source is silent on a point, the engine records UNKNOWN instead of inferring an answer.

- The authority requires that insurance is mandatory.
- The authority requires that the medical coverage meets the stated minimum of at least 30000.
- The authority requires that the policy covers the full authorized stay.
- The authority requires that eu licensed insurer.

## How we evaluate

Every requirement is compared against the documented specification of each insurance product using an automated rule engine. A product is marked GREEN for a requirement only when product evidence explicitly satisfies it; a conflict produces RED; and absent evidence produces UNKNOWN rather than a guess. The route status is the combination of its per-requirement outcomes.

- Rule `insurance.mandatory == Yes` GREEN on a match, RED on a conflict, UNKNOWN if unproven.
- Rule `insurance.min_coverage >= 30000` GREEN at or above the threshold, RED below it, UNKNOWN if unstated.
- Rule `insurance.must_cover_full_period == Yes` GREEN on a match, RED on a conflict, UNKNOWN if unproven.
- Rule `insurance.eu_licensed_insurer == Yes` GREEN on a match, RED on a conflict, UNKNOWN if unproven.

## How each compliance status is decided for this route

GREEN means every recorded requirement is satisfied by product evidence. RED means at least one requirement is contradicted by the product evidence. YELLOW means the evidence is partial: some requirements are met while others lack full proof. UNKNOWN means a requirement exists but the product evidence does not address it, so no claim is made. NOT_REQUIRED means the authority does not impose an insurance requirement for the route, which is itself an evidence-based finding drawn from the official document. A GREEN result reflects the evidence on the snapshot date and is not an assurance of a visa outcome, which always rests with the issuing authority.

## Reading the evidence and snapshots

Each requirement above links to a primary source through a source identifier and a locator (for example a page number, article, or section). The underlying documents are listed under Source Documents and are stored alongside this dataset so the wording can be checked directly. Results are tied to a dated snapshot (`2026-06-13`): a deep link to a past snapshot returns the same verdict even if the authority later changes its rules, which keeps every decision reproducible and auditable.

## Proof package checklist

Before applying for this route, prepare the following so the policy can be checked against each requirement:

- A policy certificate that states the coverage limits, any deductible or co-payment, and the covered period.
- Written confirmation of the insurer's status where the route requires authorization in a specific country.
- Documentation that the coverage spans the full authorized stay rather than a partial term.
- The official source wording for the route, so each clause can be matched to the requirements above.

## Common questions

**What insurance does a Bulgaria long-stay Visa D require?**  
The Ministry of Foreign Affairs requires an insurance policy for the whole period of stay, issued by an insurance company licensed in the European Union, with a minimum amount of coverage of 30,000 euros, covering repatriation costs, emergency medical care and emergency hospital treatment.

**Why is only AXA Schengen Europe Travel GREEN for this route?**  
The policy must be issued by an insurer licensed in the European Union. AXA Schengen Europe Travel documents an insurer authorized by the National Bank of Belgium with 100,000 euros of medical cover, hospitalization and repatriation; the other products do not document an EU insurance licence, so the engine records UNKNOWN rather than assuming a provider qualifies.

**Is the 30,000 euro figure the Schengen short-stay rule?**  
No. The 30,000 euro minimum is stated on the Ministry of Foreign Affairs Visa D (long-term) document for the national long-stay visa, alongside the whole-period and EU-licence conditions, so the engine encodes it for this national route.

## Check in the engine

Run a specific product against this route in the compliance checker: [Open Checker](/ui/?visa=BG_LONGSTAYD_MFA_2026&snapshot=2026-06-13). The checker shows the per-requirement outcome and the evidence behind each one.

## Disclaimer

This page is not legal advice. VisaFact provides evidence-based compliance checking only, and final visa decisions are made by government authorities. A GREEN result reflects documented evidence on the snapshot date; it does not ensure that a visa application will succeed. Always confirm the current requirements with the issuing authority before submitting an application.

## Affiliate disclosure

If affiliate links appear on related pages, they are shown only after the compliance result and never change the evaluation, which is generated independently from the official evidence.

## Evidence log

Each entry pairs a requirement with the source identifier and locator it was drawn from:

- `insurance.mandatory` <- BG_LONGSTAY_MFA_2026 (VISA D (long term), Documents required in all cases, item 5): "Insurance policy (and copy) for the whole period of stay, issued by an Insurance Company with a lice"
- `insurance.min_coverage` <- BG_LONGSTAY_MFA_2026 (VISA D (long term), Documents required in all cases, item 5): "with a minimum amount of coverage of 30,000 euros"
- `insurance.must_cover_full_period` <- BG_LONGSTAY_MFA_2026 (VISA D (long term), Documents required in all cases, item 5): "Insurance policy (and copy) for the whole period of stay"
- `insurance.eu_licensed_insurer` <- BG_LONGSTAY_MFA_2026 (VISA D (long term), Documents required in all cases, item 5): "issued by an Insurance Company with a license to carry out insurance activities on the territory of "


{{< checker_cta visa="BG_LONGSTAYD_MFA_2026" snapshot="2026-06-13" >}}
