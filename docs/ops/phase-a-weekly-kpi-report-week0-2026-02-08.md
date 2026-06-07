# Phase A Weekly KPI Report - Week 0 Baseline Lock (2026-02-08)

Prepared from `docs/ops/phase-a-weekly-kpi-report-template.md`.

## 1) Report Metadata

- Week range: 2026-02-02 to 2026-02-08
- Report owner: Growth + Analytics
- Review date: 2026-02-08
- Phase objective this week: Lock baseline and prepare partner activation without scope creep.
- GTM container in source: `GTM-N4JLPLC2`
- GA4 Measurement ID (documented): `G-6BLK7YFGMS`

## 2) Executive Snapshot

- Current paid offers live: 1 (`GENKI_TRAVELER_2026`)
- Pending approvals: 0 (to be initiated in CP2)
- Biggest win this week: Phase A v2 scope narrowed and templates operationalized.
- Biggest risk this week: Partner terms and approvals not yet locked.
- Overall status: On track

### 2A) Screenshot Baseline (Current External Signals)

| Source | Window | Key values | Interpretation |
|---|---|---|---|
| Google Search Console | 3 months | 0 clicks, 65 impressions, CTR 0%, avg position 3.8 | SEO visibility exists but traffic from Google Search is near zero |
| Cloudflare Web Traffic | Previous 30 days | 2.19k unique visitors, max/day 232, min/day 0 | Site receives traffic outside Google Search; requires source reconciliation |
| Cloudflare Web Analytics | Last 24h | 2 visits, 10 page views, load time 695ms | Performance is healthy; current sample size is very small |

## 3) Core Funnel KPIs (Baseline vs Current)

Baseline should be the 7-day period before Phase A launch.

| KPI | Baseline | Current Week | Delta | Target | Status |
|---|---:|---:|---:|---:|---|
| `run_check` events | Runtime metric (not stored in repo) | Runtime metric (not stored in repo) | `((Current-Baseline)/Baseline)` | Baseline locked | Waiting GA4 export |
| `click_affiliate` events | Runtime metric (not stored in repo) | Runtime metric (not stored in repo) | `((Current-Baseline)/Baseline)` | Baseline locked | Waiting GA4 export |
| OACR (`click_affiliate / run_check`) | Derived from GA4 export | Derived from GA4 export | `Current-Baseline` | +15% by end of Phase A | Waiting GA4 export |
| CTA-visible checks | TBD | TBD | `((Current-Baseline)/Baseline)` | Increase week-over-week | Pending data |
| Paid-offer coverage (count) | 1 | 1 | 0 | >=2 live + 1 pending | At risk |

### 3A) GA4 Configuration Filled From Source

| Item | Value | Evidence |
|---|---|---|
| GTM container | `GTM-N4JLPLC2` | `hugo.toml`, `ui/index.html`, `docs/analytics/ga4-postdeploy-checklist.md` |
| Measurement ID | `G-6BLK7YFGMS` | `docs/analytics/ga4-postdeploy-checklist.md` |
| Consent gating | EU/UK requires cookie consent before loading GTM | `ui/index.html` (`vfAnalyticsAllowed`), `layouts/partials/extend_head.html` |
| Event transport | `window.trackEvent` -> `dataLayer.push({ event, ...params })` | `ui/index.html`, `layouts/partials/gtm.html` |
| Optional analytics script | Supported via env/config (`HUGO_PARAMS_ANALYTICS_SRC`, `HUGO_PARAMS_ANALYTICS_ID`) | `layouts/partials/analytics.html`, `tools/tests/analytics_tests.ps1` |
| Legacy GA partial | Disabled (comment placeholder only) | `layouts/partials/google_analytics.html` |

### 3B) Implemented Event Hooks in Source

| Event | Params | Implemented in source | Notes |
|---|---|---|---|
| `select_visa` | `visa_id` | Yes | Fired on visa dropdown change |
| `select_product` | `product_id` | Yes | Fired on product dropdown change |
| `run_check` | `visa_id`, `product_id`, `status` | Yes | Fired after rendering check result |
| `open_evidence` | `source_id` | Yes | Fired from evidence buttons |
| `open_snapshot` | `snapshot_id` | Yes | Fired when snapshot modal/link opens |
| `copy_link` | `url` | Yes | Fired after copy action |
| `click_affiliate` | `product_id`, `url` | Yes | Fired on affiliate CTA click |
| `notify_changes` | `visa_id` | No | Listed in docs but not implemented in UI source |

## 4) Partner and Product Performance

| Product ID | Partner | Paid Status | CTA-visible checks | Clicks | OACR | Notes |
|---|---|---|---:|---:|---:|---|
| GENKI_TRAVELER_2026 | Genki | Paid live | TBD | TBD | TBD | Treat as active only after payout verification refresh |
| SAFETYWING_NOMAD_2026 | SafetyWing | Non-affiliate | TBD | TBD | TBD | Primary candidate for Phase A conversion |
| WORLDNOMADS_EXPLORER_2026 | World Nomads | Non-affiliate | TBD | TBD | TBD | Primary candidate; CJ onboarding dependency |
| DKV_VISADO_2026 | DKV | Non-affiliate | TBD | TBD | TBD | CPL model via network may be geo-limited |
| SANITAS_MAS_SALUD_SIN_COPAGO_2026 | Sanitas | Non-affiliate | TBD | TBD | TBD | No strong public affiliate evidence yet |
| ASISA_HEALTH_RESIDENTS_2026 | ASISA | Non-affiliate | TBD | TBD | TBD | Keep as secondary backup |

## 5) Visibility Health (Mapping Gate Impact)

Use current mapping distribution to explain why some products underperform.

| Product ID | GREEN | YELLOW | RED | UNKNOWN | NOT_REQUIRED | CTA-eligible share |
|---|---:|---:|---:|---:|---:|---:|
| GENKI_TRAVELER_2026 | 2 | 0 | 1 | 2 | 1 | 33.3% |
| SAFETYWING_NOMAD_2026 | 1 | 1 | 3 | 0 | 1 | 33.3% |
| WORLDNOMADS_EXPLORER_2026 | 2 | 0 | 2 | 1 | 1 | 33.3% |
| DKV_VISADO_2026 | 3 | 0 | 1 | 1 | 1 | 50.0% |
| SANITAS_MAS_SALUD_SIN_COPAGO_2026 | 2 | 0 | 1 | 2 | 1 | 33.3% |
| ASISA_HEALTH_RESIDENTS_2026 | 3 | 0 | 0 | 2 | 1 | 50.0% |

## 6) Top Traffic Intent Buckets

| Landing page or route | Traffic share | Main visa intent | Current monetization result | Action next week |
|---|---:|---|---|---|
| `ui/` checker entry | TBD (analytics) | mixed | 1 paid product available | Tag top entry paths and map to product CTR |
| `/visas/` high-intent pages | TBD (analytics) | visa-specific | mostly non-affiliate exits | Add deep-link to CTA-eligible product pairs |
| `/posts/` long-tail guides | TBD (analytics) | informational | weak outbound monetization | Insert controlled checker CTA blocks |

## 7) Compliance and Data Quality Checks

- Disclosure text correct for all live paid offers: Pass (current data)
- Region/legal pages aligned with current offer wording: Pass (spot-check complete)
- Tracking QA completed (source-level): Pass
- Tracking QA completed (GTM Preview + GA4 Realtime runtime): Pending this week
- Data build and validation pass (`validate.py`, `build_index.py`): Pending this week
- UI compliance tests pass: Pending this week

Notes:
- Event hooks for `run_check` and `click_affiliate` are implemented in source; numeric KPI values still require GA4 export.

## 8) Experiments and Learnings

| Experiment | Hypothesis | Result | Keep/Drop | Next step |
|---|---|---|---|---|
| Partner-first activation (no UI expansion) | Narrow scope improves execution speed | In progress | Keep | Finish SafetyWing + World Nomads onboarding |
| Visibility-first prioritization | CTA-eligible share predicts monetization upside | In progress | Keep | Use share in partner scoring gates |

## 9) Risks, Blockers, and Mitigations

| Risk or blocker | Severity | Owner | Mitigation | ETA |
|---|---|---|---|---|
| Partner approval delay (especially CJ path) | High | Growth | Start applications in parallel and track SLA daily | 2026-02-15 |
| Incomplete partner terms (cookie/payout details) | High | Growth | Require written terms before traffic scaling | 2026-02-12 |
| Visibility constraints limit click volume | Medium | Product | Prioritize CTA-eligible visa/product pairs | 2026-02-13 |
| KPI baseline not fully exported yet | Medium | Analytics | Export GA4 7-day baseline and freeze sheet | 2026-02-10 |

## 10) Next Week Focus (No Scope Creep)

1. Submit and follow up SafetyWing + World Nomads onboarding and get written terms.
2. Freeze baseline metrics from GA4/GTM and publish first full KPI update.
3. Convert at least one non-affiliate offer to paid and verify event-to-attribution chain.

## 11) Go/No-Go Decision

- Continue current plan: Yes
- If No, what changes next week: N/A
- Requested support or decisions needed: Legal review turnaround within 24h when partner terms arrive.

## 12) Data Sources Used

- `data/offers/offers.json`
- `data/ui_index.json`
- `ui/index.html` (gate and event logic)
- `hugo.toml` (GTM container id)
- `layouts/partials/gtm.html`
- `layouts/partials/extend_head.html`
- `docs/analytics/ga4-events.md`
- `docs/analytics/ga4-postdeploy-checklist.md`
- Analytics event exports or dashboard snapshots (pending pull for baseline lock)
- Test outputs for validation and UI compliance (pending run this week)
- `docs/ops/traffic-reconciliation-week0-2026-02-08.md`
