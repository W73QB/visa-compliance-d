# Contributing to VisaFact

Thanks for your interest in improving VisaFact. This project is compliance-first: **no source, no claim**.

## Quick start

- Validate data: `py tools/validate.py`
- Build mappings: `py tools/build_mappings.py`
- Build UI index: `py tools/build_index.py`
- Sync static bundle: `py tools/sync_hugo_static.py`
- Lint content: `py tools/lint_content.py`
- Run tests: `powershell -NoProfile -File tools/tests/ui_compliance_tests.ps1`

## Add a new visa

1. Add an official source file under `sources/`.
2. Create a `.meta.json` with `source_id`, `url`, `retrieved_at`, `sha256`, and `local_path`.
3. Add `data/visas/<COUNTRY>/<VISA>/<ROUTE>/<DATE>/visa_facts.json`.
4. Validate: `py tools/validate.py --visa path/to/visa_facts.json`.
5. Rebuild mappings and index.

## Add a new product

1. Add an official product evidence file under `sources/`.
2. Create a `.meta.json` with `source_id`, `url`, `retrieved_at`, `sha256`, and `local_path`.
3. Add `data/products/<PROVIDER>/<PRODUCT>/<DATE>/product_facts.json`.
4. Validate: `py tools/validate.py --product path/to/product_facts.json`.
5. Rebuild mappings and index.

## Update sources

- If any evidence changes, update the source file and its `.meta.json` SHA256.
- Bump `last_verified` in visa or product facts.

## Content requirements

Content under `content/posts`, `content/guides`, `content/visas`, `content/traps` must include:
- What the authority requires
- How we evaluate
- Check in the engine (must include `snapshot=` in the link)
- Disclaimer
- Affiliate disclosure

## Testing

Run all tests before submitting:
```
py tools/validate.py
py tools/build_mappings.py
py tools/build_index.py
py tools/sync_hugo_static.py
py tools/lint_content.py
powershell -NoProfile -File tools/tests/ui_compliance_tests.ps1
```

## Commit messages

Use prefixes: `feat:`, `fix:`, `test:`, `docs:`, `ci:`, `security:`.

## Do not commit generated artifacts

Do not commit:
- `static/`
- `data/snapshots/`
- `tools/logs/`
