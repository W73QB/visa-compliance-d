# Phase A Weekly KPI Report Template

Use this report every week during Phase A to prove impact, detect blockers early, and keep scope focused.

## 1) Report Metadata

- Week range:
- Report owner:
- Review date:
- Phase objective this week:

## 2) Executive Snapshot

- Current paid offers live:
- Pending approvals:
- Biggest win this week:
- Biggest risk this week:
- Overall status: On track / At risk / Off track

## 3) Core Funnel KPIs (Baseline vs Current)

Baseline should be the 7-day period before Phase A launch.

| KPI | Baseline | Current Week | Delta | Target | Status |
|---|---:|---:|---:|---:|---|
| `run_check` events | | | | | |
| `click_affiliate` events | | | | | |
| OACR (`click_affiliate / run_check`) | | | | | |
| CTA-visible checks | | | | | |
| Paid-offer coverage (count) | | | | | |

## 4) Partner and Product Performance

| Product ID | Partner | Paid Status | CTA-visible checks | Clicks | OACR | Notes |
|---|---|---|---:|---:|---:|---|
| | | | | | | |

## 5) Visibility Health (Mapping Gate Impact)

Use current mapping distribution to explain why some products underperform.

| Product ID | GREEN | YELLOW | RED | UNKNOWN | NOT_REQUIRED | CTA-eligible share |
|---|---:|---:|---:|---:|---:|---:|
| | | | | | | |

## 6) Top Traffic Intent Buckets

| Landing page or route | Traffic share | Main visa intent | Current monetization result | Action next week |
|---|---:|---|---|---|
| | | | | |

## 7) Compliance and Data Quality Checks

- Disclosure text correct for all live paid offers: Pass/Fail
- Region/legal pages aligned with current offer wording: Pass/Fail
- Tracking QA completed (GTM/GA4 debug sample): Pass/Fail
- Data build and validation pass (`validate.py`, `build_index.py`): Pass/Fail
- UI compliance tests pass: Pass/Fail

Notes:

## 8) Experiments and Learnings

| Experiment | Hypothesis | Result | Keep/Drop | Next step |
|---|---|---|---|---|
| | | | | |

## 9) Risks, Blockers, and Mitigations

| Risk or blocker | Severity | Owner | Mitigation | ETA |
|---|---|---|---|---|
| | | | | |

## 10) Next Week Focus (No Scope Creep)

List exactly 3 priorities. Do not include Phase B/C items.

1.
2.
3.

## 11) Go/No-Go Decision

- Continue current plan: Yes/No
- If No, what changes next week:
- Requested support or decisions needed:

## 12) Data Sources Used

- `data/offers/offers.json`
- `data/ui_index.json`
- `ui/index.html` (gate and event logic)
- Analytics event exports or dashboard snapshots
- Test outputs for validation and UI compliance
