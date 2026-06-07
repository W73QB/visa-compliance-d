# Traffic Reconciliation - Week 0 (2026-02-08)

Purpose: reconcile visible differences between Search Console, Cloudflare Web Analytics, and GA4/GTM instrumentation before using traffic numbers for monetization KPIs.

## 1) Source Snapshots Used

- GSC performance screenshot (3 months):
  - Clicks: `0`
  - Impressions: `65`
  - CTR: `0%`
  - Avg position: `3.8`
- Cloudflare Web Traffic screenshot (previous 30 days):
  - Total unique visitors: `2.19k`
  - Maximum unique/day: `232`
  - Minimum unique/day: `0`
  - Example tooltip point: `78` unique visitors (02/08 -> 02/09, GMT+7)
- Cloudflare Web Analytics screenshot (last 24h):
  - Visits: `2`
  - Page views: `10`
  - Page load time: `695ms`
  - Core Web Vitals: LCP/INP/CLS all green

## 2) Why The Numbers Differ

These systems answer different questions and use different counting rules:

- GSC counts only Google Search result interactions (impressions/clicks on Google SERP).
- Cloudflare counts edge-observed web traffic (can include direct/referral and some non-human traffic depending settings).
- GA4 (via GTM) counts browser events after script loads and consent gates pass.

Conclusion: `GSC clicks = 0` can coexist with non-zero Cloudflare unique visitors.

## 3) Bot-Filter and Scope Rules (for Phase A)

Use these rules before publishing any KPI baseline:

1. SEO acquisition baseline = GSC Web Search only.
2. Product funnel baseline (`run_check`, `click_affiliate`) = GA4 events only.
3. Cloudflare metrics are context/supporting signals, not conversion denominator.
4. If bot filtering configuration is unknown, mark Cloudflare traffic as provisional.

## 4) Reconciled Week 0 Interpretation

- SEO intent is currently low-volume: Google impressions exist but clicks are zero.
- Site performance is healthy (CWV and load time), so discoverability/snippet match is likely the current bottleneck.
- Immediate KPI focus should be:
  - Improve SERP snippet CTR (title/description updates + content-query alignment)
  - Validate GA4 funnel events and export baseline counts for `run_check` and `click_affiliate`

## 5) Action Checklist (Next 72h)

- [ ] Export GA4 event counts for last 7 days: `run_check`, `click_affiliate`, `open_evidence`, `copy_link`.
- [ ] Export GSC query/page report for same window and compare against updated metadata pages.
- [ ] Confirm Cloudflare bot setting state (enabled/disabled) and annotate report.
- [ ] Freeze one baseline table with all three systems and clear definitions.

## 6) Data Dictionary For Team

- **SEO visibility**: GSC impressions.
- **SEO traffic**: GSC clicks.
- **On-site engagement**: GA4 `run_check`.
- **Outbound monetization action**: GA4 `click_affiliate`.
- **Operational traffic context**: Cloudflare unique visitors/visits/page views.
