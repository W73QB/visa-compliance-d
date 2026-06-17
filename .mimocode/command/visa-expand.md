---
description: "Full visa expansion pipeline: validate data, rebuild mappings, build index, build content hubs, sync Hugo, and verify. Pass a COUNTRY_CODE or ROUTE_ID to scope the pipeline."
---

# Visa Expansion Pipeline

Execute the full build pipeline for a new or updated visa route.

## Input

`$ARGUMENTS` — one of:
- A 2-letter country code (e.g., `GR`, `PL`, `TW`)
- A full route ID (e.g., `GR_DNV_MFA_2026`)
- Empty (runs the full pipeline unscoped)

## Steps

### 1. Validate data

```bash
python3 tools/validate.py 2>&1 | tail -5
```

If validation fails, stop and report errors. Do not proceed.

### 2. Build mappings

```bash
python3 tools/build_mappings.py 2>&1 | tail -5
```

If a ROUTE_ID was provided, filter the output to that route's mapping files:

```bash
for f in data/mappings/${ROUTE_ID}__*.json; do
  python3 -c "import json; d=json.load(open('$f')); print(d['product_id'], d.get('status') or d.get('overall_status'))"
done | sort | uniq -c | sort -rn
```

If a COUNTRY_CODE was provided, filter to that country:

```bash
for f in data/mappings/${COUNTRY_CODE}_*__*.json; do
  python3 -c "import json; d=json.load(open('$f')); print(d['product_id'], d.get('status') or d.get('overall_status'))"
done | sort | uniq -c | sort -rn
```

### 3. Build index

```bash
python3 tools/build_index.py 2>&1 | tail -1
```

### 4. Build content hubs

```bash
SNAPSHOT_ID=$(date +%Y-%m-%d) python3 tools/build_content_hubs.py 2>&1 | tail -1
```

### 5. Sync Hugo static

```bash
python3 tools/sync_hugo_static.py 2>&1 | tail -1
```

### 6. Run tests (if available)

```bash
command -v pwsh >/dev/null && pwsh -NoProfile -File tools/tests/ui_compliance_tests.ps1 2>&1 | tail -5 || echo "pwsh not available, skipping tests"
```

### 7. Clean churned content (after expansion)

When a new country was added, unrelated `content/visas/` files may have been regenerated with different slugs. Restore them:

```bash
# Keep only the target country's changes
git status --porcelain | grep -v "${COUNTRY_CODE_Lower}" | grep "content/visas" | awk '{print $2}' | xargs git checkout -- 2>/dev/null
```

If a ROUTE_ID was provided, use the country prefix from it.

### 8. Show final diff

```bash
git diff --stat
git diff --name-only
```

### 9. Commit and push (if user requests)

```bash
git add -A && git commit -m "feat: expand ${ROUTE_ID_OR_COUNTRY} visa route" && git push
```

## Notes

- The `SNAPSHOT_ID` env var controls the snapshot date for content hub generation.
- After push, the GitHub Pages deploy workflow triggers automatically. Use `gh run watch` to monitor.
- The `tools/lint_content.py` script can be run separately for editorial checks.
