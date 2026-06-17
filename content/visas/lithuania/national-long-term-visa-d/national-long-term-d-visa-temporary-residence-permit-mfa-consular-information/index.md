---
title: "Lithuania National (long-term) Visa D - National long-term (D) visa / temporary residence permit - MFA Consular Information"
visa_id: "LT_LONGSTAYD_URM_2026"
last_verified: "2026-06-17"
source_ids: ["LT_LONGSTAYD_URM_2026"]
description: "Official insurance requirements for Lithuania National (long-term) Visa D via National long-term (D) visa / temporary residence permit - MFA Consular Information"
faq:
  - question: "What insurance does a Lithuania national (D) visa require?"
    answer: "The MFA Consular Information page (Resolution No 230 of 1 March 2005) requires health insurance valid for the whole period of stay, with a minimum amount of EUR 5,792 for a long-term (D) visa or temporary residence permit, covering basic medical assistance costs and return for health reasons."
  - question: "Is the minimum EUR 30,000?"
    answer: "No. EUR 30,000 is the minimum for a short-term (C) visa. For a long-term (D) visa or temporary residence permit the stated minimum is EUR 5,792, so the engine encodes EUR 5,792 for this national route."
  - question: "Which products are GREEN?"
    answer: "Products that document a limit at or above EUR 5,792 and cover the whole period are GREEN (Genki Native, Genki Traveler, AXA Schengen Europe Travel, World Nomads). Monthly subscriptions such as SafetyWing show YELLOW because cover can lapse; products with no documented limit stay UNKNOWN."
---

## Lithuania National (long-term) Visa D

**Route:** National long-term (D) visa / temporary residence permit - MFA Consular Information  
**Authority:** Ministry of Foreign Affairs of the Republic of Lithuania (Consular Information)  
**Last Verified:** 2026-06-17

## Requirements

| Requirement | Operator | Value | Evidence |
| --- | --- | --- | --- |
| `insurance.mandatory` | `==` | Yes | *Health Insurance (Resolution No 230 of 1 March 2005)*: "This Resolution requires that aliens who arrive in the Republic of Lithuania or ..." ([source](/sources/LT_LONGSTAYD_URM_2026-06-17.png)) |
| `insurance.min_coverage` | `>=` | 5792 | *Health Insurance, minimum amount of health insurance*: "The minimum amount of health insurance in respect of a single alien shall be: EU..." ([source](/sources/LT_LONGSTAYD_URM_2026-06-17.png)) |
| `insurance.must_cover_full_period` | `==` | Yes | *Health Insurance, validity*: "A health insurance contract shall be valid throughout the period of the alien's ..." ([source](/sources/LT_LONGSTAYD_URM_2026-06-17.png)) |

## Source Documents

- **LT_LONGSTAYD_URM_2026**: [Local copy](/sources/LT_LONGSTAYD_URM_2026-06-17.png) | [Original](https://keliauk.urm.lt/en/entry-to-lithuania/health-insurance) | Retrieved: 2026-06-17

## Related reading

- [Lithuania national (D) visa insurance requirements](/posts/lithuania-national-d-insurance/)
- [Digital nomad insurance in Europe](/posts/digital-nomad-insurance-europe/)
- [How to read compliance results](/guides/how-to-read-results/)

## What the authority requires

The points below are taken directly from the official source for the Lithuania National (long-term) Visa D (National long-term (D) visa / temporary residence permit - MFA Consular Information) route. Each one is recorded with a source identifier and a locator so it can be traced back to the original document. Where the source is silent on a point, the engine records UNKNOWN instead of inferring an answer.

- The authority requires that insurance is mandatory.
- The authority requires that the medical coverage meets the stated minimum of at least 5792.
- The authority requires that the policy covers the full authorized stay.

## How we evaluate

Every requirement is compared against the documented specification of each insurance product using an automated rule engine. A product is marked GREEN for a requirement only when product evidence explicitly satisfies it; a conflict produces RED; and absent evidence produces UNKNOWN rather than a guess. The route status is the combination of its per-requirement outcomes.

- Rule `insurance.mandatory == Yes` GREEN on a match, RED on a conflict, UNKNOWN if unproven.
- Rule `insurance.min_coverage >= 5792` GREEN at or above the threshold, RED below it, UNKNOWN if unstated.
- Rule `insurance.must_cover_full_period == Yes` GREEN on a match, RED on a conflict, UNKNOWN if unproven.

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

**What insurance does a Lithuania national (D) visa require?**  
The MFA Consular Information page (Resolution No 230 of 1 March 2005) requires health insurance valid for the whole period of stay, with a minimum amount of EUR 5,792 for a long-term (D) visa or temporary residence permit, covering basic medical assistance costs and return for health reasons.

**Is the minimum EUR 30,000?**  
No. EUR 30,000 is the minimum for a short-term (C) visa. For a long-term (D) visa or temporary residence permit the stated minimum is EUR 5,792, so the engine encodes EUR 5,792 for this national route.

**Which products are GREEN?**  
Products that document a limit at or above EUR 5,792 and cover the whole period are GREEN (Genki Native, Genki Traveler, AXA Schengen Europe Travel, World Nomads). Monthly subscriptions such as SafetyWing show YELLOW because cover can lapse; products with no documented limit stay UNKNOWN.

## Check in the engine

Run a specific product against this route in the compliance checker: [Open Checker](/ui/?visa=LT_LONGSTAYD_URM_2026&snapshot=2026-06-13). The checker shows the per-requirement outcome and the evidence behind each one.

## Disclaimer

This page is not legal advice. VisaFact provides evidence-based compliance checking only, and final visa decisions are made by government authorities. A GREEN result reflects documented evidence on the snapshot date; it does not ensure that a visa application will succeed. Always confirm the current requirements with the issuing authority before submitting an application.

## Affiliate disclosure

If affiliate links appear on related pages, they are shown only after the compliance result and never change the evaluation, which is generated independently from the official evidence.

## Evidence log

Each entry pairs a requirement with the source identifier and locator it was drawn from:

- `insurance.mandatory` <- LT_LONGSTAYD_URM_2026 (Health Insurance (Resolution No 230 of 1 March 2005)): "This Resolution requires that aliens who arrive in the Republic of Lithuania or who seek to receive "
- `insurance.min_coverage` <- LT_LONGSTAYD_URM_2026 (Health Insurance, minimum amount of health insurance): "The minimum amount of health insurance in respect of a single alien shall be: EUR 5 792: ... in case"
- `insurance.must_cover_full_period` <- LT_LONGSTAYD_URM_2026 (Health Insurance, validity): "A health insurance contract shall be valid throughout the period of the alien's stay in the Republic"


{{< checker_cta visa="LT_LONGSTAYD_URM_2026" snapshot="2026-06-13" >}}
