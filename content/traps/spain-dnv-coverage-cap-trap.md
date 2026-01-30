---
title: "Spain DNV: coverage cap trap"
date: 2026-01-30
description: "Evidence-based warning about coverage limits that fail Spain DNV requirements."
tags: ["spain", "dnv", "trap", "compliance"]
faq:
  - question: "Why do coverage caps fail Spain DNV checks?"
    answer: "Spain requires unlimited coverage; any stated cap conflicts with the checklist."
  - question: "Which products are most at risk?"
    answer: "Products with explicit coverage limits are flagged RED for Spain DNV in the checker."
---

## What the authority requires

The BLS London checklist for Spain DNV requires **comprehensive, full and unlimited insurance coverage** with no excess or co-payments (source_id: `BLS_ES_DNV_LONDON_2026`, page 2 item 9).

## How we evaluate

We compare the authority requirement for unlimited coverage against product evidence. If a product has a stated coverage limit, the checker returns RED for Spain DNV.

## The trap

Several travel or nomad products document explicit coverage limits. For example:
- SafetyWing lists a $250,000 coverage limit (source_id: `SAFETYWING_WEBSITE_2026`).
- World Nomads Explorer lists $150,000 emergency medical coverage (source_id: `WORLDNOMADS_COMPARE_2026`).
- Genki Traveler lists a EUR 1,000,000 coverage limit (source_id: `GENKI_TRAVELER_COVERAGE_2026`).

These limits conflict with the Spain checklist requirement for unlimited coverage.

## How to avoid this

Choose a policy that explicitly states unlimited coverage and no caps in the policy wording. If the policy summary lists a maximum amount, ask the insurer for a document that clarifies unlimited coverage or select a different product before applying.

## Check in the engine

Example link with snapshot:

`/ui/?visa=ES_DNV_BLS_LONDON_2026&product=SAFETYWING_NOMAD_2026&snapshot=releases/2026-01-16`

## Disclaimer

Not legal advice. Compliance results are evidence-based snapshots.

## Affiliate disclosure

If a link is shown after results, it does not influence the evidence-based outcome.
