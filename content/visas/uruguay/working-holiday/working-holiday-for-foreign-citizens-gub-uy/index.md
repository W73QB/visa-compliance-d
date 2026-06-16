---
title: "Uruguay Working Holiday - Working Holiday for foreign citizens (gub.uy)"
visa_id: "UY_WORKINGHOLIDAY_GUBUY_2026"
last_verified: "2026-06-16"
source_ids: ["UY_WORKINGHOLIDAY_GUBUY_2026"]
description: "Official insurance requirements for Uruguay Working Holiday via Working Holiday for foreign citizens (gub.uy)"
faq:
  - question: "What insurance does the Uruguay Working Holiday require?"
    answer: "The Government of Uruguay requires the applicant to have comprehensive health insurance (un seguro de salud integral)."
  - question: "Why are the Spanish health insurers GREEN here?"
    answer: "The requirement is comprehensive cover with no territory or amount. Products that document comprehensive coverage (Genki Native and the Spanish health insurers) are GREEN; travel-medical products that do not establish comprehensive cover stay UNKNOWN."
  - question: "Is there a minimum amount or territory requirement?"
    answer: "The page states no amount and no territory, so the engine models only that insurance is mandatory and comprehensive."
---

## Uruguay Working Holiday

**Route:** Working Holiday for foreign citizens (gub.uy)  
**Authority:** Ministerio de Relaciones Exteriores - Direccion de Migracion Internacional (gub.uy)  
**Last Verified:** 2026-06-16

## Requirements

| Requirement | Operator | Value | Evidence |
| --- | --- | --- | --- |
| `insurance.mandatory` | `==` | Yes | *Requisitos, Seguro medico*: "Seguro medico. Contar con un seguro de salud integral...." ([source](/sources/UY_WORKINGHOLIDAY_GUBUY_2026-06-16.html)) |
| `insurance.comprehensive` | `==` | Yes | *Requisitos, Seguro medico*: "Contar con un seguro de salud integral...." ([source](/sources/UY_WORKINGHOLIDAY_GUBUY_2026-06-16.html)) |

## Source Documents

- **UY_WORKINGHOLIDAY_GUBUY_2026**: [Local copy](/sources/UY_WORKINGHOLIDAY_GUBUY_2026-06-16.html) | [Original](https://www.gub.uy/tramites/vacaciones-trabajo-working-holiday-vacaciones-trabajo-working-holiday-ciudadanos-extranjeros) | Retrieved: 2026-06-16

## Related reading

- [Uruguay Working Holiday insurance requirements](/posts/uruguay-working-holiday-insurance/)
- [Digital nomad insurance in the Americas](/posts/digital-nomad-insurance-americas/)
- [How to read compliance results](/guides/how-to-read-results/)

## What the authority requires

The points below are taken directly from the official source for the Uruguay Working Holiday (Working Holiday for foreign citizens (gub.uy)) route. Each one is recorded with a source identifier and a locator so it can be traced back to the original document. Where the source is silent on a point, the engine records UNKNOWN instead of inferring an answer.

- The authority requires that insurance is mandatory.
- The authority requires that the coverage is comprehensive.

This route is defined by a small number of explicit insurance points, which keeps the evidence trail short but also unusually clear. A concise official requirement still has to be matched precisely: a product is only GREEN here when its documented terms line up with the wording above, and a route with few stated rules does not imply that any policy will be accepted. Where the authority is silent, the engine deliberately holds the status at UNKNOWN or NOT_REQUIRED rather than reading extra conditions into the source, so the page reflects exactly what the document states and nothing more. Applicants on routes like this one should still keep the underlying policy wording on hand, because a consular officer may ask to see how each stated point is met even when the published checklist is short.

## How we evaluate

Every requirement is compared against the documented specification of each insurance product using an automated rule engine. A product is marked GREEN for a requirement only when product evidence explicitly satisfies it; a conflict produces RED; and absent evidence produces UNKNOWN rather than a guess. The route status is the combination of its per-requirement outcomes.

- Rule `insurance.mandatory == Yes` GREEN on a match, RED on a conflict, UNKNOWN if unproven.
- Rule `insurance.comprehensive == Yes` GREEN on a match, RED on a conflict, UNKNOWN if unproven.

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

**What insurance does the Uruguay Working Holiday require?**  
The Government of Uruguay requires the applicant to have comprehensive health insurance (un seguro de salud integral).

**Why are the Spanish health insurers GREEN here?**  
The requirement is comprehensive cover with no territory or amount. Products that document comprehensive coverage (Genki Native and the Spanish health insurers) are GREEN; travel-medical products that do not establish comprehensive cover stay UNKNOWN.

**Is there a minimum amount or territory requirement?**  
The page states no amount and no territory, so the engine models only that insurance is mandatory and comprehensive.

## Check in the engine

Run a specific product against this route in the compliance checker: [Open Checker](/ui/?visa=UY_WORKINGHOLIDAY_GUBUY_2026&snapshot=2026-06-13). The checker shows the per-requirement outcome and the evidence behind each one.

## Disclaimer

This page is not legal advice. VisaFact provides evidence-based compliance checking only, and final visa decisions are made by government authorities. A GREEN result reflects documented evidence on the snapshot date; it does not ensure that a visa application will succeed. Always confirm the current requirements with the issuing authority before submitting an application.

## Affiliate disclosure

If affiliate links appear on related pages, they are shown only after the compliance result and never change the evaluation, which is generated independently from the official evidence.

## Evidence log

Each entry pairs a requirement with the source identifier and locator it was drawn from:

- `insurance.mandatory` <- UY_WORKINGHOLIDAY_GUBUY_2026 (Requisitos, Seguro medico): "Seguro medico. Contar con un seguro de salud integral."
- `insurance.comprehensive` <- UY_WORKINGHOLIDAY_GUBUY_2026 (Requisitos, Seguro medico): "Contar con un seguro de salud integral."


{{< checker_cta visa="UY_WORKINGHOLIDAY_GUBUY_2026" snapshot="2026-06-13" >}}
