---
title: "How to Read VisaFact Results"
date: 2026-01-15
description: "A quick guide to interpreting evidence-based compliance results."
tags: ["guide", "compliance"]
faq:
  - question: "What does UNKNOWN mean?"
    answer: "UNKNOWN means the evidence does not confirm one or more requirements."
  - question: "Is GREEN an approval?"
    answer: "No. GREEN means evidence matches requirements, not a visa approval."
  - question: "What is a snapshot date?"
    answer: "It is the date the evidence was verified. Use it to confirm how current the requirements are."
  - question: "Why do results change over time?"
    answer: "Results can change when authority requirements or product evidence change."
---

## Short answer

VisaFact results are evidence-based. GREEN means all requirements are verified by evidence; RED means a requirement conflicts with evidence; UNKNOWN means evidence is missing; YELLOW means partial evidence; NOT_REQUIRED means the authority does not require insurance. Always read results alongside the snapshot date and the authority source (Sources: `BLS_ES_DNV_LONDON_2026`, `VFS_PT_E11_CHINA_2025`, `TH_MFA_DTV_2026`).

## Key findings at a glance

| Status | Meaning | What to do next |
|---|---|---|
| GREEN | Evidence confirms all requirements | Keep the certificate for submission |
| YELLOW | Partial evidence | Ask for missing clauses or documents |
| RED | Evidence conflicts with a requirement | Choose a different policy or route |
| UNKNOWN | Evidence missing | Request explicit proof from insurer |
| NOT_REQUIRED | Insurance not listed | Keep optional proof if desired |

## What the authority requires

We only list requirements that are stated by the official authority for the route. For example:

- Spain DNV requires unlimited coverage, no deductible/co-pay/moratorium, and Spain authorization. (Source: `BLS_ES_DNV_LONDON_2026`, page 2, item 9; verified 2026-01-12)
- Portugal E11 requires medical expenses, urgent assistance, and repatriation coverage. (Source: `VFS_PT_E11_CHINA_2025`, page 1; verified 2026-01-15)
- Thailand DTV does not list insurance as a requirement. (Source: `TH_MFA_DTV_2026`, verified 2026-01-12)

## How we evaluate

We compare VisaFacts against ProductFacts using a rule engine. If a requirement is explicitly contradicted, the result is RED. If evidence is missing, the result is UNKNOWN rather than inferred. YELLOW indicates partial evidence. NOT_REQUIRED applies only when the authority does not list insurance. See /methodology/ for full logic.

## How to read the result card

1. **Check the status color.** This tells you whether evidence matches requirements.
2. **Open the evidence panel.** Confirm the requirement wording and the product facts.
3. **Look for missing clauses.** If the product certificate lacks a clause, expect UNKNOWN.
4. **Verify the snapshot date.** Evidence can change; use the date to assess freshness.
5. **Compare to your certificate.** The checker only matches what is explicitly documented.

## Check in the engine

Use [the compliance checker](/ui/) with a route and product. Example:

- [/ui/?visa=ES_DNV_BLS_LONDON_2026&product=ASISA_HEALTH_RESIDENTS_2026&snapshot=releases/2026-01-16](/ui/?visa=ES_DNV_BLS_LONDON_2026&product=ASISA_HEALTH_RESIDENTS_2026&snapshot=releases/2026-01-16)

## Related reading

- [Spain DNV insurance hub](/posts/spain-dnv-insurance/)
- [Spain DNV requirements (route page)](/visas/spain/digital-nomad-visa/consulate-via-bls-london/)
- [Spain DNV insurance mistakes](/traps/spain-dnv-insurance-mistakes/)
- [Digital nomad insurance in Europe](/posts/digital-nomad-insurance-europe/)
- [Methodology](/methodology/)

## Disclaimer + Affiliate disclosure

Not legal advice. Compliance results are evidence-based snapshots.

If a link is shown after results, it does not influence the evidence-based outcome.

Last updated: 2026-02-05

## Evidence log

- Source: BLS_ES_DNV_LONDON_2026
- Source: VFS_PT_E11_CHINA_2025
- Source: TH_MFA_DTV_2026
