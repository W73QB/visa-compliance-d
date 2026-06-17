---
title: "Korea Workation (F-1-D) visa insurance requirements (evidence-based)"
date: 2026-06-13
description: "Evidence-based summary of the medical insurance requirement for South Korea's F-1-D Workation (Digital Nomad) visa: coverage of more than 100 million won for treatment and evacuation, per the Ministry of Foreign Affairs."
tags: ["south-korea", "workation", "digital-nomad", "f-1-d", "insurance", "compliance"]
faq:
  - question: "How much insurance does the Korea F-1-D Workation visa require?"
    answer: "The Ministry of Foreign Affairs requires insurance that covers more than 100 million won (about USD 76,000) for hospital treatment and evacuation to the home country during the stay in Korea."
  - question: "How is the won threshold compared to product limits?"
    answer: "The engine converts the 100 million won threshold and each product's documented limit to a common currency before comparing, so a product clears the requirement only when its documented limit converts to at least the won threshold."
  - question: "Is repatriation modeled as a separate rule?"
    answer: "No. The requirement states a single amount covering both hospital treatment and evacuation, so the engine models the coverage amount; the policy must also cover repatriation."
---

## Short answer

South Korea's F-1-D Workation (Digital Nomad) visa requires insurance that covers more than 100 million won (about USD 76,000) for hospital treatment and evacuation to the home country during the stay in Korea (Source: `KR_F1D_MOFA_LA_2026`, Ministry of Foreign Affairs, Consulate General in Los Angeles; verified 2026-06-13). The engine models two rules: insurance is mandatory, and the coverage amount must meet the won threshold.

## Key findings at a glance

| Item | Value |
|---|---|
| Route | South Korea F-1-D Workation (Digital Nomad) visa |
| Authority | Ministry of Foreign Affairs of the Republic of Korea (consular) |
| Evidence verified | 2026-06-13 |
| Snapshot | 2026-06-13 |
| Modeled rules | Insurance mandatory; minimum coverage 100 million won |

## What the authority requires

- A Certificate of Medical Insurance Subscription is a required document. (Source: `KR_F1D_MOFA_LA_2026`; verified 2026-06-13)
- The insurance must cover more than 100 million won for hospital treatment and evacuation to the home country during the stay in Korea. (Source: `KR_F1D_MOFA_LA_2026`; verified 2026-06-13)

Normalized requirements table:

| Requirement | Source URL | Locator | Verified date |
|---|---|---|---|
| Insurance is mandatory | https://overseas.mofa.go.kr/us-losangeles-en/brd/m_26385/view.do?seq=12 | Required Documents, item 8 | 2026-06-13 |
| Minimum coverage 100 million won | https://overseas.mofa.go.kr/us-losangeles-en/brd/m_26385/view.do?seq=12 | Required Documents, item 8 | 2026-06-13 |

## Verified requirements (PASS/FAIL/UNKNOWN)

| Requirement | Status | Evidence |
|---|---|---|
| Insurance is mandatory | PASS | MOFA required-documents list, item 8 |
| Minimum coverage 100 million won | PASS for products whose documented limit converts to at least the won threshold; UNKNOWN where no limit is documented | MOFA: "covers more than 100 million won ... for hospital treatment and evacuation" |

## How we evaluate

The checker compares each modeled requirement against product evidence. Two rules are encoded from the MOFA required-documents list: insurance is mandatory, and the documented coverage limit must meet the 100 million won threshold. Because the threshold is stated in won, the engine is currency-aware: it converts both the won threshold and each product's documented limit to a common currency before comparing. A product whose documented limit converts to at least the won threshold is GREEN; a product whose documents state no overall limit stays UNKNOWN rather than being assumed to clear it.

The requirement states one amount covering both hospital treatment and evacuation (repatriation). The engine models the amount; confirm your policy also covers evacuation to your home country, since that wording is part of the same requirement. This follows the UNKNOWN > Wrong principle. See /methodology/ for the full logic.

## Proof package checklist

- A Certificate of Medical Insurance Subscription stating a coverage limit above 100 million won.
- Confirmation the policy covers both hospital treatment and evacuation to your home country.
- Coverage dates spanning your stay in Korea.

## FAQ

**Q: How much coverage is required?**
**A:** More than 100 million won for treatment and evacuation (Source: `KR_F1D_MOFA_LA_2026`; verified 2026-06-13).

**Q: How does the won amount compare to my policy?**
**A:** The engine converts both to a common currency before comparing, so only a documented limit at or above the won threshold clears it.

**Q: Is evacuation a separate rule?**
**A:** No. It is part of the same amount-based requirement; the engine models the amount and the policy must also cover repatriation.

## Check in the engine

Use [the compliance checker](/ui/) with the current snapshot for this route:

{{< checker_cta visa="KR_F1D_MOFA_LA_2026" product="GENKI_TRAVELER_2026" snapshot="2026-06-13" >}}

## Related reading

- [Korea Workation (F-1-D) requirements (route page)](/visas/south-korea/workation-digital-nomad-visa-f-1-d/f-1-d-pilot-program-mofa-los-angeles/)
- [Digital nomad insurance in Asia](/posts/digital-nomad-insurance-asia/)
- [How to read compliance results](/guides/how-to-read-results/)

## Where to find compliant insurance for the Korea Workation visa

The official requirement is a documented coverage limit above 100 million won (about USD 76,000) covering treatment and evacuation. In the current snapshot, Genki Traveler, Genki Native, SafetyWing and World Nomads show GREEN: each documents a limit that converts to at least the won threshold. The Spanish health products show UNKNOWN because their documents state no overall limit to compare.

- [Genki Traveler](https://genki.world/with/visafact) — paid link. We may earn a commission if you purchase through this link.

Affiliate disclosure: the Genki link above is an affiliate link; we may earn a commission at no extra cost to you, and it does not change the evidence-based compliance result. See [affiliate disclosure](https://visafact.org/affiliate-disclosure/).

> Use the compliance checker to confirm the current GREEN products for this route before you buy.

## Disclaimer + Affiliate disclosure

Not legal advice. Compliance results are evidence-based snapshots.

If an affiliate link is present, it appears only after results and does not change the compliance outcome. The Genki link above is a paid affiliate link.

Last updated: 2026-06-13

## Evidence log

- Source: KR_F1D_MOFA_LA_2026
