---
title: "Bermuda Partner Residence - Partner Residence application (Department of Immigration)"
visa_id: "BM_PARTNERRESIDENCE_GOVBM_2026"
last_verified: "2026-06-16"
date: "2026-06-16"
source_ids: ["BM_PARTNERRESIDENCE_GOVBM_2026"]
description: "Official insurance requirements for Bermuda Partner Residence via Partner Residence application (Department of Immigration)"
faq:
  - question: "What insurance does a Bermuda partner residence require?"
    answer: "The Department of Immigration requires applicants to have private health insurance coverage for the duration of their intended stay in Bermuda."
  - question: "Why does SafetyWing show YELLOW?"
    answer: "The coverage must last the whole intended stay. SafetyWing is a monthly subscription, so the engine flags YELLOW for the full-period requirement; full-period policies such as Genki Native and the Spanish health insurers are GREEN."
  - question: "Is there a minimum amount?"
    answer: "The guidelines state no coverage amount, so the engine encodes none and models that insurance is mandatory and must cover the whole stay."
---

## Bermuda Partner Residence

**Route:** Partner Residence application (Department of Immigration)  
**Authority:** Government of Bermuda, Department of Immigration  
**Last Verified:** 2026-06-16

## Requirements

| Requirement | Operator | Value | Evidence |
| --- | --- | --- | --- |
| `insurance.mandatory` | `==` | Yes | *General Rules and Criteria, Health Insurance*: "Applicants must have private health insurance coverage for the duration of their..." ([source](/sources/BM_PARTNERRESIDENCE_GOVBM_2026-06-16.pdf)) |
| `insurance.must_cover_full_period` | `==` | Yes | *General Rules and Criteria, Health Insurance*: "Applicants must have private health insurance coverage for the duration of their..." ([source](/sources/BM_PARTNERRESIDENCE_GOVBM_2026-06-16.pdf)) |

## Source Documents

- **BM_PARTNERRESIDENCE_GOVBM_2026**: [Local copy](/sources/BM_PARTNERRESIDENCE_GOVBM_2026-06-16.pdf) | [Original](https://www.gov.bm/sites/default/files/2025-09/Partner-Residence-Application-Guidelines.pdf) | Retrieved: 2026-06-16

## Related reading

- [Bermuda partner residence insurance requirements](/posts/bermuda-partner-residence-insurance/)
- [Digital nomad insurance in the Americas](/posts/digital-nomad-insurance-americas/)
- [How to read compliance results](/guides/how-to-read-results/)

## What the authority requires

The points below are taken directly from the official source for the Bermuda Partner Residence (Partner Residence application (Department of Immigration)) route. Each one is recorded with a source identifier and a locator so it can be traced back to the original document. Where the source is silent on a point, the engine records UNKNOWN instead of inferring an answer.

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

**What insurance does a Bermuda partner residence require?**  
The Department of Immigration requires applicants to have private health insurance coverage for the duration of their intended stay in Bermuda.

**Why does SafetyWing show YELLOW?**  
The coverage must last the whole intended stay. SafetyWing is a monthly subscription, so the engine flags YELLOW for the full-period requirement; full-period policies such as Genki Native and the Spanish health insurers are GREEN.

**Is there a minimum amount?**  
The guidelines state no coverage amount, so the engine encodes none and models that insurance is mandatory and must cover the whole stay.

## Check in the engine

Run a specific product against this route in the compliance checker: [Open Checker](/ui/?visa=BM_PARTNERRESIDENCE_GOVBM_2026&snapshot=2026-06-13). The checker shows the per-requirement outcome and the evidence behind each one.

## Disclaimer

This page is not legal advice. VisaFact provides evidence-based compliance checking only, and final visa decisions are made by government authorities. A GREEN result reflects documented evidence on the snapshot date; it does not ensure that a visa application will succeed. Always confirm the current requirements with the issuing authority before submitting an application.

## Affiliate disclosure

If affiliate links appear on related pages, they are shown only after the compliance result and never change the evaluation, which is generated independently from the official evidence.

## Evidence log

Each entry pairs a requirement with the source identifier and locator it was drawn from:

- `insurance.mandatory` <- BM_PARTNERRESIDENCE_GOVBM_2026 (General Rules and Criteria, Health Insurance): "Applicants must have private health insurance coverage for the duration of their intended stay in Be"
- `insurance.must_cover_full_period` <- BM_PARTNERRESIDENCE_GOVBM_2026 (General Rules and Criteria, Health Insurance): "Applicants must have private health insurance coverage for the duration of their intended stay in Be"


{{< checker_cta visa="BM_PARTNERRESIDENCE_GOVBM_2026" snapshot="2026-06-13" >}}
