---
title: "South Korea Workation (Digital Nomad) Visa (F-1-D) - F-1-D Pilot Program (MOFA Los Angeles)"
visa_id: "KR_F1D_MOFA_LA_2026"
last_verified: "2026-06-15"
source_ids: ["KR_F1D_MOFA_LA_2026"]
description: "Official insurance requirements for South Korea Workation (Digital Nomad) Visa (F-1-D) via F-1-D Pilot Program (MOFA Los Angeles)"
faq:
  - question: "What insurance does the Korea F-1-D Workation visa require?"
    answer: "The Ministry of Foreign Affairs requires insurance that covers more than 100 million won (about USD 76,000) for hospital treatment and evacuation to the home country during the stay in Korea."
  - question: "How is the 100 million won threshold compared to product limits?"
    answer: "The engine converts the 100 million won threshold and each product's documented limit to a common currency before comparing, so a product clears the requirement only when its documented limit converts to at least the won threshold."
  - question: "Is the evacuation (repatriation) part modeled separately?"
    answer: "No. The requirement states a single amount covering both hospital treatment and evacuation, so the engine models the coverage amount and the post notes that the policy must also cover repatriation."
---

## South Korea Workation (Digital Nomad) Visa (F-1-D)

**Route:** F-1-D Pilot Program (MOFA Los Angeles)  
**Authority:** Ministry of Foreign Affairs of the Republic of Korea (Consulate General, Los Angeles)  
**Last Verified:** 2026-06-15

## Requirements

| Requirement | Operator | Value | Evidence |
| --- | --- | --- | --- |
| `insurance.mandatory` | `==` | Yes | *Required Documents, item 8 (Certificate of Medical Insurance Subscription)*: "Certificate of Medical Insurance Subscription : A person who has insurance that ..." ([source](/sources/KR_F1D_MOFA_LA_2026-06-15.html)) |
| `insurance.min_coverage` | `>=` | 100000000 | *Required Documents, item 8 (Certificate of Medical Insurance Subscription)*: "insurance that covers more than 100 million won(approx. USD 76,000) for hospital..." ([source](/sources/KR_F1D_MOFA_LA_2026-06-15.html)) |

## Source Documents

- **KR_F1D_MOFA_LA_2026**: [Local copy](/sources/KR_F1D_MOFA_LA_2026-06-15.html) | [Original](https://overseas.mofa.go.kr/us-losangeles-en/brd/m_26385/view.do?seq=12) | Retrieved: 2026-06-15

## Related reading

- [Korea Workation (F-1-D) visa insurance requirements](/posts/korea-workation-visa-insurance/)
- [Digital nomad insurance in Asia](/posts/digital-nomad-insurance-asia/)
- [How to read compliance results](/guides/how-to-read-results/)

## What the authority requires

The points below are taken directly from the official source for the South Korea Workation (Digital Nomad) Visa (F-1-D) (F-1-D Pilot Program (MOFA Los Angeles)) route. Each one is recorded with a source identifier and a locator so it can be traced back to the original document. Where the source is silent on a point, the engine records UNKNOWN instead of inferring an answer.

- The authority requires that insurance is mandatory.
- The authority requires that the medical coverage meets the stated minimum of at least 100000000.

This route is defined by a small number of explicit insurance points, which keeps the evidence trail short but also unusually clear. A concise official requirement still has to be matched precisely: a product is only GREEN here when its documented terms line up with the wording above, and a route with few stated rules does not imply that any policy will be accepted. Where the authority is silent, the engine deliberately holds the status at UNKNOWN or NOT_REQUIRED rather than reading extra conditions into the source, so the page reflects exactly what the document states and nothing more. Applicants on routes like this one should still keep the underlying policy wording on hand, because a consular officer may ask to see how each stated point is met even when the published checklist is short.

## How we evaluate

Every requirement is compared against the documented specification of each insurance product using an automated rule engine. A product is marked GREEN for a requirement only when product evidence explicitly satisfies it; a conflict produces RED; and absent evidence produces UNKNOWN rather than a guess. The route status is the combination of its per-requirement outcomes.

- Rule `insurance.mandatory == Yes` GREEN on a match, RED on a conflict, UNKNOWN if unproven.
- Rule `insurance.min_coverage >= 100000000` GREEN at or above the threshold, RED below it, UNKNOWN if unstated.

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

**What insurance does the Korea F-1-D Workation visa require?**  
The Ministry of Foreign Affairs requires insurance that covers more than 100 million won (about USD 76,000) for hospital treatment and evacuation to the home country during the stay in Korea.

**How is the 100 million won threshold compared to product limits?**  
The engine converts the 100 million won threshold and each product's documented limit to a common currency before comparing, so a product clears the requirement only when its documented limit converts to at least the won threshold.

**Is the evacuation (repatriation) part modeled separately?**  
No. The requirement states a single amount covering both hospital treatment and evacuation, so the engine models the coverage amount and the post notes that the policy must also cover repatriation.

## Check in the engine

Run a specific product against this route in the compliance checker: [Open Checker](/ui/?visa=KR_F1D_MOFA_LA_2026&snapshot=2026-06-13). The checker shows the per-requirement outcome and the evidence behind each one.

## Disclaimer

This page is not legal advice. VisaFact provides evidence-based compliance checking only, and final visa decisions are made by government authorities. A GREEN result reflects documented evidence on the snapshot date; it does not ensure that a visa application will succeed. Always confirm the current requirements with the issuing authority before submitting an application.

## Affiliate disclosure

If affiliate links appear on related pages, they are shown only after the compliance result and never change the evaluation, which is generated independently from the official evidence.

## Evidence log

Each entry pairs a requirement with the source identifier and locator it was drawn from:

- `insurance.mandatory` <- KR_F1D_MOFA_LA_2026 (Required Documents, item 8 (Certificate of Medical Insurance Subscription)): "Certificate of Medical Insurance Subscription : A person who has insurance that covers more than 100"
- `insurance.min_coverage` <- KR_F1D_MOFA_LA_2026 (Required Documents, item 8 (Certificate of Medical Insurance Subscription)): "insurance that covers more than 100 million won(approx. USD 76,000) for hospital treatment and evacu"


{{< checker_cta visa="KR_F1D_MOFA_LA_2026" snapshot="2026-06-13" >}}
