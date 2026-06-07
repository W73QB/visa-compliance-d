# Content QA Checklist (CI-Aligned)

Use this checklist before merging content changes.

## 1) Scope

This checklist applies to content in:
- `content/posts/**`
- `content/visas/**`
- `content/guides/**`
- `content/traps/**`

Primary rule sources:
- `tools/lint_content.py`
- `tools/seo_audit.py`
- `tools/seo_thresholds.json`
- `.github/workflows/pages.yml`

## 2) Required blocks (lint gate)

For non-`_index.md` files, content must include all blocks below:
- `what the authority requires`
- `how we evaluate`
- `check in the engine`
- `disclaimer`
- `affiliate disclosure`
- `evidence log`

For `_index.md` files, `evidence log` is not required.

## 3) Banned words (lint gate)

Do not use these words in content body:
- `best`
- `recommend`
- `recommended`
- `guarantee`
- `guaranteed`
- `100%`
- `approved`
- `surely`

## 4) Snapshot deep-link rule (lint gate)

At least one deep link must contain `snapshot=`.

Notes:
- Lint requires `snapshot=` string presence.
- `snapshot=releases/YYYY-MM-DD` is recommended for stable published references.

## 5) SEO audit gates (mandatory in CI)

### 5.1 Minimum word count
- Enforced by `tools/seo_audit.py` with thresholds in `tools/seo_thresholds.json`.
- Default threshold exists, plus stricter per-file overrides.

### 5.2 Required links by content type
- Rules are defined in `tools/seo_thresholds.json` under `required_links`.
- Example: posts must include `/ui/` and at least one qualifying internal path per rule.

### 5.3 FAQ requirement is explicit per-file
- `require_faq` is a fixed list in `tools/seo_thresholds.json`.
- Current list length: 18 files.

### 5.4 Include and exclude globs matter
- `include_globs` controls what files are audited.
- `exclude_globs` intentionally excludes specific files (for example `content/posts/hello.md`, `content/templates/*.md`, `content/legal/**`).
- Important nuance: visas audit pattern is `content/visas/**/index.md` (not `_index.md`).

## 6) Internal links gate (mandatory in CI)

`tools/check_internal_links.py` is a required CI step and must pass.

This is not optional.

## 7) Pre-merge command checklist

Run all commands locally before merge:

```bash
python3 tools/lint_content.py
python3 tools/seo_audit.py --config tools/seo_thresholds.json
python3 tools/check_internal_links.py
```

Optional but recommended:

```bash
pwsh -NoProfile -File tools/tests/content_lint_tests.ps1
pwsh -NoProfile -File tools/tests/seo_audit_tests.ps1
```

## 8) Done criteria

Ship only when all are true:
- Lint passes.
- SEO audit passes.
- Internal link check passes.
- Required blocks are present.
- No banned words.
- `snapshot=` deep link exists.
- FAQ front matter is present for files listed in `require_faq`.
