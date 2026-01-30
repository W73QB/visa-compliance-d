---
title: "Understanding compliance statuses (GREEN, YELLOW, RED, UNKNOWN)"
date: 2026-01-30
description: "Evidence-based explanation of VisaFact compliance statuses."
tags: ["guides", "compliance", "methodology"]
faq:
  - question: "Why does UNKNOWN appear so often?"
    answer: "UNKNOWN means we could not find official evidence for a requirement, so we do not guess."
  - question: "Is NOT_REQUIRED the same as GREEN?"
    answer: "No. NOT_REQUIRED means the authority does not require insurance at all; GREEN means all requirements are satisfied."
---

## What the authority requires

Compliance statuses are anchored to official requirements. For example:
- Spain DNV requires unlimited coverage with no deductible (source_id: `BLS_ES_DNV_LONDON_2026`).
- Germany D visas reject travel insurance (source_id: `DE_D_VISA_HEALTH_INSURANCE_2026`).
- Thailand DTV does not list insurance as a requirement (source_id: `TH_MFA_DTV_2026`).

## How we evaluate

The engine compares VisaFacts and ProductFacts. If a requirement is violated, the status is RED. If evidence is missing, the status is UNKNOWN. If insurance is not required, the status is NOT_REQUIRED. See /methodology/ for rule details.

## Status definitions with evidence-based examples

- **GREEN:** All requirements confirmed by evidence. Example: ASISA Health Residents for Portugal DNV (source_id: `VFS_PT_E11_CHINA_2025`).
- **YELLOW:** Partial concern based on evidence. Example: Costa Rica DN vs SafetyWing where full-period coverage is required but monthly subscriptions can be cancelled (source_id: `CR_DECREE_43619_2026`).
- **RED:** One or more requirements conflict with evidence. Example: Spain DNV vs SafetyWing because Spain requires unlimited coverage and no deductible (source_id: `BLS_ES_DNV_LONDON_2026`).
- **UNKNOWN:** Evidence missing for one or more requirements. Example: Germany freelance visa vs Genki where the travel-insurance classification is not documented by evidence.
- **NOT_REQUIRED:** The authority does not require insurance. Example: Thailand DTV (source_id: `TH_MFA_DTV_2026`).

If you see UNKNOWN, treat it as a prompt to gather more documents from the insurer or check if the authority has updated its checklist since the last snapshot.

## Check in the engine

Example link with snapshot:

`/ui/?visa=CR_DN_DECREE_43619_2026&product=SAFETYWING_NOMAD_2026&snapshot=releases/2026-01-15`

## Related reading

- [How to read compliance results](/guides/how-to-read-results/)
- [Spain DNV requirements](/visas/spain/digital-nomad-visa/consulate-via-bls-london/)

## Disclaimer

Not legal advice. Compliance results are evidence-based snapshots.

## Affiliate disclosure

If a link is shown after results, it does not influence the evidence-based outcome.
