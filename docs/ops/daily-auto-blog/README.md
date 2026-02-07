# Daily Auto Blog Operations Runbook

## State Files

- `docs/ops/daily-auto-blog/state/seen_topics.json`: canonical dedup ledger.
- `docs/ops/daily-auto-blog/state/run-status.json`: run history for monitoring.
- `docs/ops/daily-auto-blog/state/pending_topics.json`: open PR dedup safety state.

## Rollback Procedure

1. Close bad draft PR and delete branch `auto/daily-blog/YYYY-MM-DD`.
2. If merged, revert the merge commit or the specific post commit.
3. Remove affected topic key from `seen_topics.json` only after rollback is confirmed.
4. Re-run pipeline for the same date with fixed config/evidence.

## Monitoring

- Trigger issue escalation when there are 2 or more consecutive non-PASS statuses in `run-status.json`.
- Include run manifest summary and failure reason in issue body.
