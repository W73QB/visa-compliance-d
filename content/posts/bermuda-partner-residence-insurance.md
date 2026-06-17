---
title: "Bermuda partner residence insurance requirements (evidence-based)"
date: 2026-06-15
description: "Evidence-based summary of the health insurance requirement for Bermuda partner residence: private health insurance for the duration of the intended stay, per the Department of Immigration."
tags: ["bermuda", "partner-residence", "insurance", "compliance"]
faq:
  - question: "What insurance does a Bermuda partner residence require?"
    answer: "The Department of Immigration requires applicants to have private health insurance coverage for the duration of their intended stay in Bermuda."
  - question: "Why does SafetyWing show YELLOW?"
    answer: "The coverage must last the whole intended stay. SafetyWing is a monthly subscription, so the engine flags YELLOW for the full-period requirement; full-period policies such as Genki Native and the Spanish health insurers are GREEN."
  - question: "Is there a minimum amount?"
    answer: "The guidelines state no coverage amount, so the engine encodes none and models that insurance is mandatory and must cover the whole stay."
---

## Short answer

A Bermuda partner residence application requires applicants to have private health insurance coverage for the duration of their intended stay in Bermuda (Source: `BM_PARTNERRESIDENCE_GOVBM_2026`, Government of Bermuda Department of Immigration; verified 2026-06-16). The guidelines state no coverage amount, so the engine models two rules: insurance is mandatory, and it must cover the whole stay.

## Key findings at a glance

| Item | Value |
|---|---|
| Route | Bermuda Partner Residence |
| Authority | Government of Bermuda, Department of Immigration |
| Evidence verified | 2026-06-16 |
| Snapshot | 2026-06-13 |
| Modeled rules | Insurance mandatory; must cover the whole stay |

## What the authority requires

- Private health insurance coverage is required. (Source: `BM_PARTNERRESIDENCE_GOVBM_2026`; verified 2026-06-16)
- It must cover the duration of the intended stay in Bermuda. (Source: `BM_PARTNERRESIDENCE_GOVBM_2026`; verified 2026-06-16)
- The guidelines state no coverage amount, so that stays UNKNOWN.

Normalized requirements table:

| Requirement | Source URL | Locator | Verified date |
|---|---|---|---|
| Insurance is mandatory | https://www.gov.bm/sites/default/files/2025-09/Partner-Residence-Application-Guidelines.pdf | General Rules and Criteria, Health Insurance | 2026-06-16 |
| Covers the whole stay | https://www.gov.bm/sites/default/files/2025-09/Partner-Residence-Application-Guidelines.pdf | General Rules and Criteria, Health Insurance | 2026-06-16 |

## Verified requirements (PASS/FAIL/UNKNOWN)

| Requirement | Status | Evidence |
|---|---|---|
| Insurance is mandatory | PASS | Dept of Immigration: "Applicants must have private health insurance coverage..." |
| Covers the whole stay | PASS for full-period policies; YELLOW for monthly subscriptions | "...for the duration of their intended stay in Bermuda" |
| Minimum coverage amount | UNKNOWN | Not stated |

## How we evaluate

The checker compares each modeled requirement against product evidence. Two rules are encoded from the partner residence guidelines: insurance is mandatory, and it must cover the duration of the intended stay. A monthly subscription does not by itself establish full-period coverage, so the engine flags it YELLOW; full-period policies are GREEN. No coverage amount is encoded because the guidelines state none, following the UNKNOWN > Wrong principle. See /methodology/ for the full logic.

## Proof package checklist

- A private health insurance policy covering the whole intended stay in Bermuda.
- A certificate showing the policy holder, policy number and coverage dates.
- The remaining partner residence documents (relationship evidence, financial means, police certificate).

## FAQ

**Q: What is required?**
**A:** Private health insurance for the duration of the intended stay (Source: `BM_PARTNERRESIDENCE_GOVBM_2026`; verified 2026-06-16).

**Q: Why is SafetyWing YELLOW?**
**A:** It is a monthly subscription, so the engine flags the full-period requirement; full-period policies are GREEN.

**Q: Is there a minimum amount?**
**A:** The guidelines state none, so the engine encodes no figure.

## Check in the engine

Use [the compliance checker](/ui/) with the current snapshot for this route:

{{< checker_cta visa="BM_PARTNERRESIDENCE_GOVBM_2026" product="GENKI_NATIVE_2026" snapshot="2026-06-13" >}}

## Related reading

- [Bermuda partner residence requirements (route page)](/visas/bermuda/partner-residence/partner-residence-application-department-of-immigration/)
- [Digital nomad insurance in the Americas](/posts/digital-nomad-insurance-americas/)
- [How to read compliance results](/guides/how-to-read-results/)

## Where to find compliant insurance for Bermuda partner residence

The requirement is private health insurance for the whole intended stay, with no amount specified. In the current snapshot, full-period policies show GREEN, including Genki Native and the Spanish health insurers; SafetyWing shows YELLOW because it is a monthly subscription that does not establish full-period coverage by itself.

- [Genki Native](https://genki.world/with/visafact) — paid link. We may earn a commission if you purchase through this link.

Affiliate disclosure: the Genki link above is an affiliate link; we may earn a commission at no extra cost to you, and it does not change the evidence-based compliance result. See [affiliate disclosure](https://visafact.org/affiliate-disclosure/).

> Use the compliance checker to confirm the current GREEN products for this route before you buy.

## Disclaimer + Affiliate disclosure

Not legal advice. Compliance results are evidence-based snapshots.

If an affiliate link is present, it appears only after results and does not change the compliance outcome. The Genki link above is a paid affiliate link.

Last updated: 2026-06-15

## Evidence log

- Source: BM_PARTNERRESIDENCE_GOVBM_2026
