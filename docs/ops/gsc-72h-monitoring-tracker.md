# GSC 72-Hour Monitoring Tracker

Use this tracker for the first 72 hours after week-1 merge and manual indexing requests.

## Baseline Snapshot (T0)

- Timestamp (UTC): `2026-02-08 06:51`
- PR merged: `#50` (`0e97a3f1c3e4d24776fbedd4559589c9a2499442`)
- Clicks: `0`
- Indexed pages: `2`
- Not indexed pages: `5`
- Breadcrumb errors: `1`
- Unparsable structured data errors: `1`

## Checkpoint Schedule

- T+24h
- T+48h
- T+72h

## Metrics Log

| Checkpoint | Timestamp (UTC) | Clicks | Indexed | Not Indexed | Breadcrumb Errors | Unparsable SD Errors | Notes |
|---|---|---:|---:|---:|---:|---:|---|
| T+24h | _pending_ |  |  |  |  |  |  |
| T+48h | _pending_ |  |  |  |  |  |  |
| T+72h | _pending_ |  |  |  |  |  |  |

## Decision Rules

- If `Breadcrumb Errors` and `Unparsable SD Errors` both stay unchanged by T+72h, open follow-up bug for schema output inspection against live-rendered HTML.
- If `Indexed` does not increase by T+72h, run indexability diagnostic again and recheck canonical/sitemap/robots assumptions.
- If clicks remain `0`, keep monitoring weekly; do not treat as immediate regression without impression trend context.
