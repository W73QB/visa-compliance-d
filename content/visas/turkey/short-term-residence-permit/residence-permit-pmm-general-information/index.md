---
title: "Turkey Short-Term Residence Permit - Residence permit (PMM general information)"
visa_id: "TR_RESIDENCE_PMM_2026"
last_verified: "2026-06-15"
date: "2026-06-15"
source_ids: ["TR_RESIDENCE_PMM_2026"]
description: "Official insurance requirements for Turkey Short-Term Residence Permit via Residence permit (PMM general information)"
faq:
  - question: "What insurance does a Turkish residence permit require?"
    answer: "The Presidency of Migration Management states that the duration of your health insurance must cover the requested duration of the residence permit, and lists acceptable types including private health insurance."
  - question: "Is there a minimum coverage amount?"
    answer: "The official general-information page states no minimum coverage figure for private health insurance, so the engine encodes none and models only that insurance is mandatory and must cover the full permit duration."
  - question: "Why is SafetyWing YELLOW while other products are GREEN?"
    answer: "The insurance must cover the requested duration of the permit. A month-to-month subscription that can lapse does not assure full-period coverage, so it is YELLOW; full-period policies are GREEN."
---

## Turkey Short-Term Residence Permit

**Route:** Residence permit (PMM general information)  
**Authority:** Presidency of Migration Management of Turkey (PMM, Goc Idaresi)  
**Last Verified:** 2026-06-15

## Requirements

| Requirement | Operator | Value | Evidence |
| --- | --- | --- | --- |
| `insurance.mandatory` | `==` | Yes | *Health insurance requirement*: "Health insurance requirement Duration of your insurance must cover the requested..." ([source](/sources/TR_RESIDENCE_PMM_2026-06-15.html)) |
| `insurance.must_cover_full_period` | `==` | Yes | *Health insurance requirement*: "Duration of your insurance must cover the requested duration of residence permit..." ([source](/sources/TR_RESIDENCE_PMM_2026-06-15.html)) |

## Source Documents

- **TR_RESIDENCE_PMM_2026**: [Local copy](/sources/TR_RESIDENCE_PMM_2026-06-15.html) | [Original](https://en.goc.gov.tr/general-information41) | Retrieved: 2026-06-15

## Related reading

- [Turkey residence permit insurance requirements](/posts/turkey-residence-permit-insurance/)
- [Digital nomad insurance in Europe](/posts/digital-nomad-insurance-europe/)
- [How to read compliance results](/guides/how-to-read-results/)

## What the authority requires

The points below are taken directly from the official source for the Turkey Short-Term Residence Permit (Residence permit (PMM general information)) route. Each one is recorded with a source identifier and a locator so it can be traced back to the original document. Where the source is silent on a point, the engine records UNKNOWN instead of inferring an answer.

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

**What insurance does a Turkish residence permit require?**  
The Presidency of Migration Management states that the duration of your health insurance must cover the requested duration of the residence permit, and lists acceptable types including private health insurance.

**Is there a minimum coverage amount?**  
The official general-information page states no minimum coverage figure for private health insurance, so the engine encodes none and models only that insurance is mandatory and must cover the full permit duration.

**Why is SafetyWing YELLOW while other products are GREEN?**  
The insurance must cover the requested duration of the permit. A month-to-month subscription that can lapse does not assure full-period coverage, so it is YELLOW; full-period policies are GREEN.

## Check in the engine

Run a specific product against this route in the compliance checker: [Open Checker](/ui/?visa=TR_RESIDENCE_PMM_2026&snapshot=2026-06-13). The checker shows the per-requirement outcome and the evidence behind each one.

## Disclaimer

This page is not legal advice. VisaFact provides evidence-based compliance checking only, and final visa decisions are made by government authorities. A GREEN result reflects documented evidence on the snapshot date; it does not ensure that a visa application will succeed. Always confirm the current requirements with the issuing authority before submitting an application.

## Affiliate disclosure

If affiliate links appear on related pages, they are shown only after the compliance result and never change the evaluation, which is generated independently from the official evidence.

## Evidence log

Each entry pairs a requirement with the source identifier and locator it was drawn from:

- `insurance.mandatory` <- TR_RESIDENCE_PMM_2026 (Health insurance requirement): "Health insurance requirement Duration of your insurance must cover the requested duration of residen"
- `insurance.must_cover_full_period` <- TR_RESIDENCE_PMM_2026 (Health insurance requirement): "Duration of your insurance must cover the requested duration of residence permit."


{{< checker_cta visa="TR_RESIDENCE_PMM_2026" snapshot="2026-06-13" >}}
