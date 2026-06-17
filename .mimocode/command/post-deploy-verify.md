---
description: "Verify a visa route made it to production after deploy. Checks the live ui_index.json for expected visas and country counts."
---

# Post-Deploy Verify

After a GitHub Pages deploy completes, verify the new visa data is live.

## Input

`$ARGUMENTS` — one of:
- A 2-letter country code (e.g., `GR`, `PL`, `TW`)
- A full route ID (e.g., `GR_DNV_MFA_2026`)
- Empty (shows overall visa count and country count)

## Steps

### 1. Fetch production index

```bash
ts=$(date +%s)
curl -s "https://visafact.org/data/ui_index.json?cb=$ts" -o /tmp/p.json
```

### 2. Verify

If a ROUTE_ID was provided:

```bash
python3 -c "
import json
d = json.load(open('/tmp/p.json'))
v = [x['id'] for x in d['visas']]
print('total visas:', len(v))
print('route present:', '${ROUTE_ID}' in v)
print('countries:', len(set(x['id'][:2] for x in d['visas'])))
"
```

If a COUNTRY_CODE was provided:

```bash
python3 -c "
import json
d = json.load(open('/tmp/p.json'))
v = [x['id'] for x in d['visas']]
country_visas = [x for x in v if x.startswith('${COUNTRY_CODE}_')]
print('total visas:', len(v))
print('${COUNTRY_CODE} visas:', len(country_visas))
print('countries:', len(set(x['id'][:2] for x in d['visas'])))
for vid in country_visas:
    print(' -', vid)
"
```

If empty:

```bash
python3 -c "
import json
d = json.load(open('/tmp/p.json'))
v = [x['id'] for x in d['visas']]
print('total visas:', len(v))
print('countries:', len(set(x['id'][:2] for x in d['visas'])))
"
```

### 3. Compare with local

```bash
python3 -c "
import json
local = json.load(open('data/ui_index.json'))
prod = json.load(open('/tmp/p.json'))
lv = set(x['id'] for x in local['visas'])
pv = set(x['id'] for x in prod['visas'])
missing = lv - pv
extra = pv - lv
if missing: print('MISSING from prod:', missing)
if extra: print('EXTRA in prod:', extra)
if not missing and not extra: print('LOCAL AND PROD MATCH')
"
```

## Notes

- The cache-buster `?cb=$ts` prevents CDN caching from returning stale data.
- If the deploy is still in progress, the prod index may lag behind. Check with `gh run list --workflow=pages.yml --limit 1` first.
- The comparison script handles the case where local has more visas than prod (deploy not yet complete) or prod has more (upstream changes).
