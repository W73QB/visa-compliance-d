# Phase A Affiliate Partner Scorecard - SafetyWing

Prepared from `docs/ops/phase-a-affiliate-partner-scorecard-template.md`.

## 1) Candidate Identity

- Partner name: SafetyWing
- Program name: SafetyWing Ambassador Program
- Program URL: https://safetywing.com/ambassador
- Network or direct (CJ, Kwanko, direct, other): Direct
- Account manager name/email: TBD (request during onboarding)
- Date evaluated: 2026-02-08
- Evaluator: OpenCode

## 2) Program Terms Snapshot

- Commission model (CPA/CPL/quote-based/revshare): Revenue-share style on completed applications
- Stated commission rate: Approximately 10% of total premium amount (public page wording)
- Cookie window: Not publicly specified on ambassador landing page
- Payout threshold: Not publicly specified on ambassador landing page
- Payout cadence: Not publicly specified on ambassador landing page
- Payment method: Not publicly specified on ambassador landing page
- Geo restrictions: No hard geo restriction found on ambassador landing page; verify in terms
- Language restrictions: Not clearly specified
- Brand or content restrictions: Not clearly specified on public ambassador page

## 3) Compliance and Policy Fit

- Requires strict disclaimer text: Unknown (must confirm in partner terms)
- Insurance marketing restrictions identified: Unknown (must confirm in partner terms)
- Deep link allowed: Likely yes via referral link, verify in terms
- Quote widget allowed: Unknown
- Any legal or regulatory blocker for current site: No blocker identified yet, pending terms review
- Notes: Must receive written terms before GO, including disclosure requirements and prohibited claims.

## 4) Visibility Fit with Current Engine

Use `data/ui_index.json` and `ui/index.html` gate logic to estimate real visibility.

| Product ID | GREEN | YELLOW | RED | UNKNOWN | NOT_REQUIRED | CTA-eligible share (GREEN+YELLOW) |
|---|---:|---:|---:|---:|---:|---:|
| SAFETYWING_NOMAD_2026 | 1 | 1 | 3 | 0 | 1 | 33.3% |

- High-priority visa routes where CTA can actually show: `CR_DN_DECREE_43619_2026` (YELLOW), `PT_DNV_VFS_CHINA_2026` (GREEN)
- High-traffic routes currently blocked (RED/UNKNOWN/NOT_REQUIRED): `ES_DNV_BLS_LONDON_2026`, `DE_FREELANCE_EMBASSY_LONDON_2026`, `MT_NOMAD_RESIDENCY_2026`, `TH_DTV_MFA_2026`
- Is this partner still viable with current visibility? Yes, but only as controlled Phase A candidate with low visibility share

## 5) Tracking and Attribution Fit

- Supports standard outbound tracking and UTM policy: Yes on our side (`click_affiliate` is implemented via GTM container `GTM-N4JLPLC2`)
- Attribution method clear (cookie, code, quote ID, server-side): No, unclear from public ambassador page
- Dispute process for missing commissions documented: Unknown from public page
- Test click and attribution verification plan defined: Yes (UAT click + first conversion confirmation)
- Notes: GA4 measurement used in project docs is `G-6BLK7YFGMS`; request partner-side attribution details and dispute workflow in writing before scaling traffic.

## 6) Risk Check

- Known payout complaints from credible sources: Some (single Trustpilot complaint found, not corroborated)
- Source quality of risk evidence (official/network/community): Low confidence for systemic issue
- Dependency risk (single network approval bottleneck): Low (direct program)
- Time-to-approval risk: Medium
- Overall execution risk: Medium

## 7) Weighted Scoring (100 points)

Score each dimension from 0-10, then multiply by weight.

| Dimension | Weight | Raw (0-10) | Weighted |
|---|---:|---:|---:|
| Affiliate availability and approval probability | 20 | 7 | 14.0 |
| Geo and audience fit | 15 | 8 | 12.0 |
| CTA visibility fit (GREEN+YELLOW share) | 20 | 3 | 6.0 |
| Unit economics (commission + cookie + threshold) | 15 | 6 | 9.0 |
| Compliance and legal fit | 10 | 7 | 7.0 |
| Operational reliability (payment/support SLA) | 10 | 5 | 5.0 |
| Integration effort and speed | 10 | 9 | 9.0 |
| **Total** | **100** |  | **62.0/100** |

## 8) Decision Rule

- **GO**: total >= 75 and no critical blocker.
- **HOLD**: total 60-74 or one unresolved blocker.
- **NO-GO**: total < 60 or critical blocker.

Decision: **HOLD** (promote to GO after written term confirmation and visibility-aware launch plan).

## 9) Immediate Action Plan (for GO or HOLD)

| Action | Owner | Due Date | Status |
|---|---|---|---|
| Submit ambassador application | Growth | 2026-02-09 | Planned |
| Request written terms (cookie, payout threshold, payout cadence, claim restrictions) | Growth | 2026-02-10 | Planned |
| Confirm disclosure text requirements and update copy if required | Content/Legal | 2026-02-11 | Planned |
| Verify first tracked click and first attributable conversion | Analytics | 2026-02-14 | Planned |

## 10) Evidence Links

- Official program page: https://safetywing.com/ambassador
- Official onboarding entry: https://safetywing.com/ambassador/signup
- Internal visibility source: `data/ui_index.json`
- Internal gate logic: `ui/index.html` (`renderOffer`)
- Offer source: `data/offers/offers.json`
- Notes on unresolved questions: Cookie duration and payout operations are not visible on the public ambassador page.
