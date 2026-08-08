---
title: "Belize Long Stay Permit - Long Stay Permit (Department of Immigration)"
visa_id: "BZ_LONGSTAY_IMMIG_2026"
last_verified: "2026-06-15"
date: "2026-06-15"
source_ids: ["BZ_LONGSTAY_IMMIG_2026"]
description: "Official insurance requirements for Belize Long Stay Permit via Long Stay Permit (Department of Immigration)"
faq:
  - question: "What insurance does the Belize Long Stay Permit require?"
    answer: "The Department of Immigration requires proof of travel insurance with a minimum health coverage of USD 50,000."
  - question: "How is the USD 50,000 threshold compared to product limits?"
    answer: "The engine converts the USD 50,000 threshold and each product's documented limit to a common currency before comparing, so a product clears the requirement only when its documented limit converts to at least USD 50,000."
  - question: "Which products are UNKNOWN and why?"
    answer: "Products whose documents state no overall coverage limit (the Spanish health policies) stay UNKNOWN rather than being assumed to clear the USD 50,000 floor."
---

## Belize Long Stay Permit

**Route:** Long Stay Permit (Department of Immigration)  
**Authority:** Belize Ministry of Immigration, Governance and Labour  
**Last Verified:** 2026-06-15

## Requirements

| Requirement | Operator | Value | Evidence |
| --- | --- | --- | --- |
| `insurance.mandatory` | `==` | Yes | *Long Stay Permit, required documents*: "Proof of travel insurance with a minimum health coverage of USD $50,000...." ([source](/sources/BZ_LONGSTAY_IMMIG_2026-06-15.html)) |
| `insurance.min_coverage` | `>=` | 50000 | *Long Stay Permit, required documents*: "Proof of travel insurance with a minimum health coverage of USD $50,000...." ([source](/sources/BZ_LONGSTAY_IMMIG_2026-06-15.html)) |

## Source Documents

- **BZ_LONGSTAY_IMMIG_2026**: [Local copy](/sources/BZ_LONGSTAY_IMMIG_2026-06-15.html) | [Original](https://immigration.gov.bz/permits/long-stay-permit/) | Retrieved: 2026-06-15

## Related reading

- [Belize Long Stay Permit insurance requirements](/posts/belize-long-stay-insurance/)
- [Digital nomad insurance in the Americas](/posts/digital-nomad-insurance-americas/)
- [How to read compliance results](/guides/how-to-read-results/)

## What the authority requires

The points below are taken directly from the official source for the Belize Long Stay Permit (Long Stay Permit (Department of Immigration)) route. Each one is recorded with a source identifier and a locator so it can be traced back to the original document. Where the source is silent on a point, the engine records UNKNOWN instead of inferring an answer.

- The authority requires that insurance is mandatory.
- The authority requires that the medical coverage meets the stated minimum of at least 50000.

This route is defined by a small number of explicit insurance points, which keeps the evidence trail short but also unusually clear. A concise official requirement still has to be matched precisely: a product is only GREEN here when its documented terms line up with the wording above, and a route with few stated rules does not imply that any policy will be accepted. Where the authority is silent, the engine deliberately holds the status at UNKNOWN or NOT_REQUIRED rather than reading extra conditions into the source, so the page reflects exactly what the document states and nothing more. Applicants on routes like this one should still keep the underlying policy wording on hand, because a consular officer may ask to see how each stated point is met even when the published checklist is short.

## How we evaluate

Every requirement is compared against the documented specification of each insurance product using an automated rule engine. A product is marked GREEN for a requirement only when product evidence explicitly satisfies it; a conflict produces RED; and absent evidence produces UNKNOWN rather than a guess. The route status is the combination of its per-requirement outcomes.

- Rule `insurance.mandatory == Yes` GREEN on a match, RED on a conflict, UNKNOWN if unproven.
- Rule `insurance.min_coverage >= 50000` GREEN at or above the threshold, RED below it, UNKNOWN if unstated.

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

**What insurance does the Belize Long Stay Permit require?**  
The Department of Immigration requires proof of travel insurance with a minimum health coverage of USD 50,000.

**How is the USD 50,000 threshold compared to product limits?**  
The engine converts the USD 50,000 threshold and each product's documented limit to a common currency before comparing, so a product clears the requirement only when its documented limit converts to at least USD 50,000.

**Which products are UNKNOWN and why?**  
Products whose documents state no overall coverage limit (the Spanish health policies) stay UNKNOWN rather than being assumed to clear the USD 50,000 floor.

## Check in the engine

Run a specific product against this route in the compliance checker: [Open Checker](/ui/?visa=BZ_LONGSTAY_IMMIG_2026&snapshot=2026-06-13). The checker shows the per-requirement outcome and the evidence behind each one.

## Disclaimer

This page is not legal advice. VisaFact provides evidence-based compliance checking only, and final visa decisions are made by government authorities. A GREEN result reflects documented evidence on the snapshot date; it does not ensure that a visa application will succeed. Always confirm the current requirements with the issuing authority before submitting an application.

## Affiliate disclosure

If affiliate links appear on related pages, they are shown only after the compliance result and never change the evaluation, which is generated independently from the official evidence.

## Evidence log

Each entry pairs a requirement with the source identifier and locator it was drawn from:

- `insurance.mandatory` <- BZ_LONGSTAY_IMMIG_2026 (Long Stay Permit, required documents): "Proof of travel insurance with a minimum health coverage of USD $50,000."
- `insurance.min_coverage` <- BZ_LONGSTAY_IMMIG_2026 (Long Stay Permit, required documents): "Proof of travel insurance with a minimum health coverage of USD $50,000."


{{< checker_cta visa="BZ_LONGSTAY_IMMIG_2026" snapshot="2026-06-13" >}}
