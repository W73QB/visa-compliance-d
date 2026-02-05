---
title: "Digital nomad insurance requirements (Americas - verified subset)"
date: 2026-01-16
description: "Evidence-based summary of verified insurance requirements for Americas routes in this dataset."
tags: ["digital-nomad", "insurance", "americas", "compliance"]
faq:
  - question: "What is the minimum coverage in the Americas routes listed?"
    answer: "Costa Rica requires at least US $50,000 in medical coverage; other Americas routes are not yet verified in this dataset."
  - question: "Why are some product matches RED or UNKNOWN in the Americas?"
    answer: "RED means product evidence conflicts with a requirement; UNKNOWN means a requirement is not confirmed by evidence."
  - question: "Does the policy need to cover the entire stay?"
    answer: "Yes for Costa Rica. The decree requires coverage for the full authorized legal stay period."
  - question: "Can requirements change during the year?"
    answer: "Yes. Always compare the evidence date to your application date and re-check the official decree or checklist."
---

## Short answer

The verified Americas subset in this dataset is Costa Rica Digital Nomad Visa. Executive Decree 43619 requires health insurance with at least US $50,000 in medical coverage and coverage for the full authorized legal stay period (Source: `CR_DECREE_43619_2026`, locator: Article 9; verified 2026-01-12).

## Key findings at a glance

| Item | Value |
|---|---|
| Route covered | Costa Rica Digital Nomad Visa |
| Evidence verified | 2026-01-12 |
| Snapshot | releases/2026-01-15 |
| Minimum coverage | US $50,000 (medical expenses) |
| Coverage duration | Full authorized legal stay |

## What the authority requires

- Health insurance is mandatory for the digital nomad visa. (Source: `CR_DECREE_43619_2026`, locator: Article 9; verified 2026-01-12)
- Minimum medical coverage is US $50,000 for illnesses in Costa Rica. (Source: `CR_DECREE_43619_2026`, locator: Article 9 - Minimum Coverage Amount; verified 2026-01-12)
- The policy must cover the entire authorized legal stay period. (Source: `CR_DECREE_43619_2026`, locator: Article 9 - Coverage Duration; verified 2026-01-12)

Normalized requirements table:

| Requirement | Source URL | Locator | Verified date |
|---|---|---|---|
| Health insurance is mandatory | http://www.pgrweb.go.cr/scij/Busqueda/Normativa/Normas/nrm_texto_completo.aspx?nValor1=1&nValor2=97374&nValor3=131405 | Article 9 | 2026-01-12 |
| Minimum medical coverage US $50,000 | http://www.pgrweb.go.cr/scij/Busqueda/Normativa/Normas/nrm_texto_completo.aspx?nValor1=1&nValor2=97374&nValor3=131405 | Article 9 - Minimum Coverage Amount | 2026-01-12 |
| Policy covers full authorized stay | http://www.pgrweb.go.cr/scij/Busqueda/Normativa/Normas/nrm_texto_completo.aspx?nValor1=1&nValor2=97374&nValor3=131405 | Article 9 - Coverage Duration | 2026-01-12 |

## Verified requirements (PASS/FAIL/UNKNOWN)

| Requirement | Status | Evidence |
|---|---|---|
| Health insurance is mandatory | PASS | Executive Decree 43619, Article 9 |
| Minimum medical coverage >= US $50,000 | PASS | Executive Decree 43619, Article 9 |
| Policy covers full authorized stay | PASS | Executive Decree 43619, Article 9 |

## How we evaluate

The checker looks for explicit evidence of the minimum coverage amount and coverage duration. If product documents do not state US $50,000 or do not show coverage for the full authorized stay, the result is UNKNOWN rather than inferred. Missing proof is never treated as compliance. See /methodology/ for evaluation logic and the UNKNOWN > Wrong principle.

In practice, the two most common gaps are missing coverage amounts and unclear dates. If the policy summary only describes coverage generically, the checker cannot confirm the US $50,000 minimum or the full-stay duration requirement. The evidence-first rule prevents the system from guessing.

## Proof package checklist

- Policy certificate or document showing minimum medical coverage of US $50,000. (Source: `CR_DECREE_43619_2026`)
- Policy dates or wording that clearly show coverage for the full authorized legal stay. (Source: `CR_DECREE_43619_2026`)
- If coverage limits or dates are on a separate endorsement, include that page so the minimum amount and duration are explicit.

## Common rejection traps

- Submitting a policy that omits the US $50,000 minimum coverage amount.
- Coverage dates that do not match the full authorized stay period.
- INFERENCE: Policies that describe coverage generally but omit the minimum amount or duration can lead to UNKNOWN results.
- INFERENCE: Using a certificate without a coverage amount even when the insurer has a limit on file.

## FAQ

**Q: What is the minimum coverage in the Americas routes listed?**
**A:** Costa Rica requires at least US $50,000 in medical coverage (Source: `CR_DECREE_43619_2026`, Article 9; verified 2026-01-12). This is the only verified Americas route in the current dataset.

**Q: Why are some product matches RED or UNKNOWN in the Americas?**
**A:** RED means product evidence conflicts with a requirement; UNKNOWN means a requirement is not confirmed by evidence.

**Q: Does the policy need to cover the entire stay?**
**A:** Yes. The decree states the policy must cover the full authorized legal stay period (Source: `CR_DECREE_43619_2026`, Article 9; verified 2026-01-12).

**Q: Can requirements change during the year?**
**A:** Yes. Always compare the evidence date to your application date and re-check the official decree or checklist.

## Check in the engine

Use [the compliance checker](/ui/) for route-specific results. Example link:

- [/ui/?visa=CR_DN_DECREE_43619_2026&product=GENKI_TRAVELER_2026&snapshot=releases/2026-01-15](/ui/?visa=CR_DN_DECREE_43619_2026&product=GENKI_TRAVELER_2026&snapshot=releases/2026-01-15)

## Mapping results summary

As of snapshot `releases/2026-01-15`, example product outcomes for Costa Rica are:

| Route | SafetyWing | World Nomads | Genki |
|---|---|---|---|
| Costa Rica DN | YELLOW | GREEN | GREEN |

YELLOW indicates partial evidence in the current snapshot. It often means the policy meets some requirements but lacks explicit documentation for the minimum amount or full-stay duration.

If you see YELLOW or UNKNOWN, open the route page and compare the authority wording to your policy certificate. The checker is intentionally conservative when amounts or dates are not explicit.

## Related reading

- [Costa Rica digital nomad insurance hub](/posts/costa-rica-dn-insurance/)
- [Costa Rica digital nomad visa requirements](/visas/costa-rica/digital-nomad-visa/executive-decree-43619/)
- [Costa Rica digital nomad visa hub](/visas/costa-rica/digital-nomad-visa/)
- [How to read compliance results](/guides/how-to-read-results/)
- [How to choose DNV insurance](/guides/how-to-choose-dnv-insurance/)

## Disclaimer + Affiliate disclosure

Not legal advice. Compliance results are evidence-based snapshots.

If an affiliate link is present, it appears only after results and does not change the compliance outcome.

Last updated: 2026-02-05

## Evidence log

- Source: CR_DECREE_43619_2026
