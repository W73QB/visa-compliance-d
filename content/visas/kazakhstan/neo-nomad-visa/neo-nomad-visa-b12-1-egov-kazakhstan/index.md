---
title: "Kazakhstan Neo Nomad Visa - Neo Nomad Visa B12-1 (eGov Kazakhstan)"
visa_id: "KZ_NEONOMAD_EGOV_2026"
last_verified: "2026-06-15"
source_ids: ["KZ_NEONOMAD_EGOV_2026"]
description: "Official insurance requirements for Kazakhstan Neo Nomad Visa via Neo Nomad Visa B12-1 (eGov Kazakhstan)"
faq:
  - question: "What insurance does the Kazakhstan Neo Nomad Visa require?"
    answer: "The eGov visa classification states the Neo Nomad Visa (B12-1) requires medical insurance covering the requested validity period of the visa."
  - question: "Is there a minimum amount or territory requirement?"
    answer: "The official page states only that the insurance must cover the requested validity period, with no amount or territory, so the engine models insurance as mandatory and full-period."
  - question: "Why is SafetyWing YELLOW while other products are GREEN?"
    answer: "The cover must run for the requested validity period of the visa. A month-to-month subscription that can lapse does not assure that, so it is YELLOW; full-period policies are GREEN."
---

## Kazakhstan Neo Nomad Visa

**Route:** Neo Nomad Visa B12-1 (eGov Kazakhstan)  
**Authority:** Government of the Republic of Kazakhstan (eGov)  
**Last Verified:** 2026-06-15

## Requirements

| Requirement | Operator | Value | Evidence |
| --- | --- | --- | --- |
| `insurance.mandatory` | `==` | Yes | *Neo Nomad Visa (B12-1) required documents, item 4*: "medical insurance covering the requested validity period of the visa...." ([source](/sources/KZ_NEONOMAD_EGOV_2026-06-15.html)) |
| `insurance.must_cover_full_period` | `==` | Yes | *Neo Nomad Visa (B12-1) required documents, item 4*: "medical insurance covering the requested validity period of the visa...." ([source](/sources/KZ_NEONOMAD_EGOV_2026-06-15.html)) |

## Source Documents

- **KZ_NEONOMAD_EGOV_2026**: [Local copy](/sources/KZ_NEONOMAD_EGOV_2026-06-15.html) | [Original](https://egov.kz/cms/en/articles/for_foreigners/visa_classification) | Retrieved: 2026-06-15

## Related reading

- [Kazakhstan Neo Nomad Visa insurance requirements](/posts/kazakhstan-neo-nomad-insurance/)
- [Digital nomad insurance in Asia](/posts/digital-nomad-insurance-asia/)
- [How to read compliance results](/guides/how-to-read-results/)

## What the authority requires

The points below are taken directly from the official source for the Kazakhstan Neo Nomad Visa (Neo Nomad Visa B12-1 (eGov Kazakhstan)) route. Each one is recorded with a source identifier and a locator so it can be traced back to the original document. Where the source is silent on a point, the engine records UNKNOWN instead of inferring an answer.

- The authority requires that insurance is mandatory.
- The authority requires that the policy covers the full authorized stay.

This route is defined by a small number of explicit insurance points, which keeps the evidence trail short but also unusually clear. A concise official requirement still has to be matched precisely: a product is only GREEN here when its documented terms line up with the wording above, and a route with few stated rules does not imply that any policy will be accepted. Where the authority is silent, the engine deliberately holds the status at UNKNOWN or NOT_REQUIRED rather than reading extra conditions into the source, so the page reflects exactly what the document states and nothing more. Applicants on routes like this one should still keep the underlying policy wording on hand, because a consular officer may ask to see how each stated point is met even when the published checklist is short.

## How we evaluate

Every requirement is compared against the documented specification of each insurance product using an automated rule engine. A product is marked GREEN for a requirement only when product evidence explicitly satisfies it; a conflict produces RED; and absent evidence produces UNKNOWN rather than a guess. The route status is the combination of its per-requirement outcomes.

- Rule `insurance.mandatory == Yes` GREEN on a match, RED on a conflict, UNKNOWN if unproven.
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

**What insurance does the Kazakhstan Neo Nomad Visa require?**  
The eGov visa classification states the Neo Nomad Visa (B12-1) requires medical insurance covering the requested validity period of the visa.

**Is there a minimum amount or territory requirement?**  
The official page states only that the insurance must cover the requested validity period, with no amount or territory, so the engine models insurance as mandatory and full-period.

**Why is SafetyWing YELLOW while other products are GREEN?**  
The cover must run for the requested validity period of the visa. A month-to-month subscription that can lapse does not assure that, so it is YELLOW; full-period policies are GREEN.

## Check in the engine

Run a specific product against this route in the compliance checker: [Open Checker](/ui/?visa=KZ_NEONOMAD_EGOV_2026&snapshot=2026-06-13). The checker shows the per-requirement outcome and the evidence behind each one.

## Disclaimer

This page is not legal advice. VisaFact provides evidence-based compliance checking only, and final visa decisions are made by government authorities. A GREEN result reflects documented evidence on the snapshot date; it does not ensure that a visa application will succeed. Always confirm the current requirements with the issuing authority before submitting an application.

## Affiliate disclosure

If affiliate links appear on related pages, they are shown only after the compliance result and never change the evaluation, which is generated independently from the official evidence.

## Evidence log

Each entry pairs a requirement with the source identifier and locator it was drawn from:

- `insurance.mandatory` <- KZ_NEONOMAD_EGOV_2026 (Neo Nomad Visa (B12-1) required documents, item 4): "medical insurance covering the requested validity period of the visa."
- `insurance.must_cover_full_period` <- KZ_NEONOMAD_EGOV_2026 (Neo Nomad Visa (B12-1) required documents, item 4): "medical insurance covering the requested validity period of the visa."


{{< checker_cta visa="KZ_NEONOMAD_EGOV_2026" snapshot="2026-06-13" >}}
