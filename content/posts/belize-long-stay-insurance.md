---
title: "Belize Long Stay Permit insurance requirements (evidence-based)"
date: 2026-06-13
description: "Evidence-based summary of the insurance requirement for Belize's Long Stay Permit: proof of travel insurance with a minimum health coverage of USD 50,000, per the Department of Immigration."
tags: ["belize", "long-stay-permit", "insurance", "compliance"]
faq:
  - question: "What insurance does the Belize Long Stay Permit require?"
    answer: "The Department of Immigration requires proof of travel insurance with a minimum health coverage of USD 50,000."
  - question: "How is the USD 50,000 threshold compared to product limits?"
    answer: "The engine converts the USD 50,000 threshold and each product's documented limit to a common currency before comparing, so a product clears the requirement only when its documented limit converts to at least USD 50,000."
  - question: "Which products are UNKNOWN and why?"
    answer: "Products whose documents state no overall coverage limit (the Spanish health policies) stay UNKNOWN rather than being assumed to clear the USD 50,000 floor."
---

## Short answer

Belize's Long Stay Permit requires proof of travel insurance with a minimum health coverage of USD 50,000 (Source: `BZ_LONGSTAY_IMMIG_2026`, Belize Department of Immigration; verified 2026-06-13). The engine models two rules: insurance is mandatory, and the documented coverage limit must meet the USD 50,000 threshold.

## Key findings at a glance

| Item | Value |
|---|---|
| Route | Belize Long Stay Permit |
| Authority | Belize Ministry of Immigration, Governance and Labour |
| Evidence verified | 2026-06-13 |
| Snapshot | 2026-06-13 |
| Modeled rules | Insurance mandatory; minimum coverage USD 50,000 |

## What the authority requires

- Proof of travel insurance is a required document. (Source: `BZ_LONGSTAY_IMMIG_2026`; verified 2026-06-13)
- The insurance must have a minimum health coverage of USD 50,000. (Source: `BZ_LONGSTAY_IMMIG_2026`; verified 2026-06-13)

Normalized requirements table:

| Requirement | Source URL | Locator | Verified date |
|---|---|---|---|
| Insurance is mandatory | https://immigration.gov.bz/permits/long-stay-permit/ | Long Stay Permit, required documents | 2026-06-13 |
| Minimum coverage USD 50,000 | https://immigration.gov.bz/permits/long-stay-permit/ | Long Stay Permit, required documents | 2026-06-13 |

## Verified requirements (PASS/FAIL/UNKNOWN)

| Requirement | Status | Evidence |
|---|---|---|
| Insurance is mandatory | PASS | Department of Immigration required documents |
| Minimum coverage USD 50,000 | PASS for products whose documented limit converts to at least USD 50,000; UNKNOWN otherwise | "minimum health coverage of USD $50,000" |

## How we evaluate

The checker compares each modeled requirement against product evidence. Two rules are encoded from the Department of Immigration page: insurance is mandatory, and the documented coverage limit must meet the USD 50,000 threshold. Because the threshold is in USD, the engine is currency-aware: it converts both the threshold and each product's documented limit to a common currency before comparing. A product whose documented limit converts to at least USD 50,000 is GREEN; a product whose documents state no overall limit stays UNKNOWN rather than being assumed to clear it, following the UNKNOWN > Wrong principle. See /methodology/ for the full logic.

## Proof package checklist

- A travel insurance certificate stating a health coverage limit of at least USD 50,000.
- A certificate showing the policy holder, policy number and coverage dates.
- Proof of residence and the remaining Long Stay Permit documents.

## FAQ

**Q: How much coverage is required?**
**A:** A minimum health coverage of USD 50,000 (Source: `BZ_LONGSTAY_IMMIG_2026`; verified 2026-06-13).

**Q: How does the USD amount compare to my policy?**
**A:** The engine converts both to a common currency, so only a documented limit at or above USD 50,000 clears it.

**Q: Why are some products UNKNOWN?**
**A:** Products that document no overall limit are not assumed to clear the floor.

## Check in the engine

Use [the compliance checker](/ui/) with the current snapshot for this route:

{{< checker_cta visa="BZ_LONGSTAY_IMMIG_2026" product="GENKI_TRAVELER_2026" snapshot="2026-06-13" >}}

## Related reading

- [Belize Long Stay Permit requirements (route page)](/visas/belize/long-stay-permit/long-stay-permit-department-of-immigration/)
- [Digital nomad insurance in the Americas](/posts/digital-nomad-insurance-americas/)
- [How to read compliance results](/guides/how-to-read-results/)

## Where to find compliant insurance for the Belize Long Stay Permit

The official requirement is a documented health coverage limit of at least USD 50,000. In the current snapshot, Genki Traveler, Genki Native, SafetyWing and World Nomads show GREEN: each documents a limit that converts to at least USD 50,000. The Spanish health products show UNKNOWN because their documents state no overall limit to compare.

- [Genki Traveler](https://genki.world/) — paid link. We may earn a commission if you purchase through this link.

> Use the compliance checker to confirm the current GREEN products for this route before you buy.

## Disclaimer + Affiliate disclosure

Not legal advice. Compliance results are evidence-based snapshots.

If an affiliate link is present, it appears only after results and does not change the compliance outcome. The Genki link above is a paid affiliate link.

Last updated: 2026-06-13

## Evidence log

- Source: BZ_LONGSTAY_IMMIG_2026
