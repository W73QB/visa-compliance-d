---
title: "Understanding compliance statuses (GREEN, YELLOW, RED, UNKNOWN)"
date: 2026-01-30
description: "Evidence-based explanation of VisaFact compliance statuses."
tags: ["guides", "compliance", "methodology"]
faq:
  - question: "Why does UNKNOWN appear so often?"
    answer: "UNKNOWN means we could not find official evidence for a requirement, so we do not guess."
  - question: "Is NOT_REQUIRED the same as GREEN?"
    answer: "No. NOT_REQUIRED means the authority does not require insurance; GREEN means all requirements are satisfied."
  - question: "What does YELLOW mean in practice?"
    answer: "YELLOW indicates partial evidence: some requirements are verified, others are missing or unclear."
  - question: "Does GREEN ensure visa approval?"
    answer: "No. GREEN only means evidence matches the listed requirements; final decisions are made by authorities."
---

## Short answer

VisaFact uses five statuses to summarize how product evidence matches official requirements: GREEN, YELLOW, RED, UNKNOWN, and NOT_REQUIRED. These statuses are evidence-first, meaning we only confirm what is explicitly documented by the authority and the product evidence (Sources: `BLS_ES_DNV_LONDON_2026`, `DE_D_VISA_HEALTH_INSURANCE_2026`, `TH_MFA_DTV_2026`, `VFS_PT_E11_CHINA_2025`, `CR_DECREE_43619_2026`).

## Key findings at a glance

| Status | What it means | Example |
|---|---|---|
| GREEN | All requirements verified | Portugal E11 with clear travel insurance coverage types |
| YELLOW | Partial evidence | Costa Rica DN with missing duration proof |
| RED | Evidence conflicts with a requirement | Spain DNV vs coverage caps |
| UNKNOWN | Missing evidence | Germany D visa with no statutory-equivalence proof |
| NOT_REQUIRED | No insurance requirement listed | Thailand DTV Workcation |


## What the authority requires

Statuses are anchored to official authority requirements. Examples from current evidence:

- Spain DNV requires insurer authorization in Spain and unlimited coverage with no deductible/co-pay/moratorium. (Source: `BLS_ES_DNV_LONDON_2026`, locator: page 2, item 9; verified 2026-01-12)
- Germany D visas require statutory-level health insurance; travel insurance is not sufficient. (Source: `DE_D_VISA_HEALTH_INSURANCE_2026`, locator: Health insurance requirements for national (category D) visas; verified 2026-01-15)
- Thailand DTV does not list insurance as a requirement. (Source: `TH_MFA_DTV_2026`, locator: Complete requirements list for all DTV categories; verified 2026-01-12)
- Portugal E11 requires travel insurance covering medical expenses, urgent assistance, and repatriation. (Source: `VFS_PT_E11_CHINA_2025`, locator: page 1, General Requirements; verified 2026-01-15)
- Costa Rica DN requires at least USD 50,000 coverage and full-stay duration. (Source: `CR_DECREE_43619_2026`, locator: Article 9; verified 2026-01-12)

## How we evaluate

The engine compares VisaFacts against ProductFacts. If evidence explicitly contradicts a requirement, the status is RED. If evidence is missing, the status is UNKNOWN. YELLOW indicates partial evidence: some requirements are confirmed and others are missing or unclear. NOT_REQUIRED means the authority does not list insurance in its requirements. See /methodology/ for rule logic and the UNKNOWN > Wrong principle.

## Status definitions with evidence-based examples

- **GREEN:** All listed requirements are verified. Example: Portugal E11 where product evidence lists medical expenses, urgent assistance, and repatriation (Source: `VFS_PT_E11_CHINA_2025`).
- **YELLOW:** Some requirements are verified but others are missing. Example: Costa Rica DN when the policy lists USD 50,000 but does not show full-stay coverage (Source: `CR_DECREE_43619_2026`).
- **RED:** Evidence conflicts with at least one requirement. Example: Spain DNV vs policies with coverage caps (Source: `BLS_ES_DNV_LONDON_2026`).
- **UNKNOWN:** Evidence missing for one or more requirements. Example: Germany D visa where statutory-equivalence wording is not present (Source: `DE_D_VISA_HEALTH_INSURANCE_2026`).
- **NOT_REQUIRED:** Insurance is not listed as required. Example: Thailand DTV (Source: `TH_MFA_DTV_2026`).

## How to use the status in decisions

1. Start with the official checklist and verify the evidence date.
2. Use GREEN only when all requirements are explicitly documented.
3. Treat YELLOW and UNKNOWN as a prompt to collect more documentation.
4. Treat RED as a direct conflict with the authority requirement.
5. Treat NOT_REQUIRED as a route-specific status, not an advice to skip coverage.

## Check in the engine

Use [the compliance checker](/ui/) with a current snapshot. Example:

- [/ui/?visa=CR_DN_DECREE_43619_2026&product=SAFETYWING_NOMAD_2026&snapshot=releases/2026-01-15](/ui/?visa=CR_DN_DECREE_43619_2026&product=SAFETYWING_NOMAD_2026&snapshot=releases/2026-01-15)

## Related reading

- [Thailand DTV insurance hub](/posts/thailand-dtv-insurance/)
- [Thailand DTV requirements (route page)](/visas/thailand/digital-nomad-visa-dtv/thai-e-visa/)
- [How to read compliance results](/guides/how-to-read-results/)
- [Digital nomad insurance in Asia](/posts/digital-nomad-insurance-asia/)

## Disclaimer + Affiliate disclosure

Not legal advice. Compliance results are evidence-based snapshots.

If a link is shown after results, it does not influence the evidence-based outcome.

Last updated: 2026-02-05

## Evidence log

- Source: BLS_ES_DNV_LONDON_2026
- Source: DE_D_VISA_HEALTH_INSURANCE_2026
- Source: TH_MFA_DTV_2026
- Source: VFS_PT_E11_CHINA_2025
- Source: CR_DECREE_43619_2026
