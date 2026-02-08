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

## Exit Codes

### `daily_auto_blog.py write`

| Code | Meaning | Operator Action |
|---|---|---|
| 0 | Success | None |
| 2 | Output already exists and overwrite disabled | Re-run with resume-safe settings or choose a new output path |
| 3 | Missing LLM credential | Set provider API key (`NVIDIA_API_KEY`/`NGC_API_KEY` or `OPENAI_API_KEY`) |
| 4 | Front matter invalid | Fix front matter fields to match schema |
| 5 | Required blocks/banned words validation failed | Fix markdown sections and prohibited terms |
| 6 | Missing/invalid `checker_cta` shortcode snapshot | Fix shortcode format and run-date snapshot |
| 7 | Word count out of configured range | Revise content length |
| 8 | Unknown claim reference IDs in body | Align references with `claim_map.json` |
| 10 | LLM budget exceeded | Increase budget or reduce retries/max tokens |
| 11 | LLM/API request failed after retries | Check network/provider status and retry |
| 12 | FAQ style validation failed | Use required `**Q:**` / `**A:**` format |

### `daily_auto_blog.py run`

| Code | Meaning | Operator Action |
|---|---|---|
| 0 | Run completed or deterministic SKIP status recorded in manifest | Inspect `run_manifest.json` and `run-status.json` for PASS/SKIP reason |
| 1 | Fatal step failure (index/write/qa/editorial-target) | Use manifest `steps[]`, `write_failure_rc`, and status reason to triage |

### Run Status Values (`run-status.json`)

| Status | Meaning |
|---|---|
| PASS | Full pipeline success |
| FAIL | Fatal failure in one or more required steps |
| SKIP_NO_VERIFIED_EVIDENCE | Candidate found but claim map has no VERIFIED evidence |
| SKIP_NO_CANDIDATE_FALLBACK | Primary and fallback candidate selection failed |
