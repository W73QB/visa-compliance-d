# Repository Guidelines

## Project Structure & Module Organization
- `ui/index.html`: Single-page compliance checker UI (HTML/JS/CSS).
- `data/`: Canonical data (`visas/`, `products/`, `mappings/`, `offers/`) and `ui_index.json` (built).
- `sources/`: Official evidence files plus `*.meta.json` with `source_id`, `sha256`, `local_path`.
- `schemas/`: JSON schemas for validation.
- `tools/`: Python build/validation scripts and `tools/tests/*.ps1`.
- `content/`: Hugo content (posts and legal pages). `static/` is generated output.
- `.github/workflows/`: CI, Pages deploy, source monitoring.

## Build, Test, and Development Commands
- `py tools/validate.py` — validate all JSON data against schemas.
- `py tools/build_mappings.py` — build compliance mappings.
- `py tools/build_index.py` — build `data/ui_index.json`.
- `py tools/build_snapshot.py` — create daily snapshot under `data/snapshots/`.
- `py tools/build_release_snapshot.py --release-id YYYY-MM-DD` — release snapshot.
- `py tools/sync_hugo_static.py` — sync UI/data/sources into `static/`.
- `py tools/lint_content.py` — lint blog content (posts/visas/guides/traps only).
- `hugo server -D` — run local Hugo site.
- `pwsh -File tools/build_hugo.ps1` — build Hugo with log (CI).
- Tests: `powershell -NoProfile -File tools/tests/ui_compliance_tests.ps1` (see other `*_tests.ps1`).

## Coding Style & Naming Conventions
- **UI:** Keep `ui/index.html` ASCII-only, use `escapeHtml()` for text and `sanitizeUrl()` for links.
- **JS:** camelCase for functions/vars, UPPER_SNAKE_CASE for constants.
- **JSON:** snake_case keys; IDs like `ES_DNV_BLS_LONDON_2026`.
- **Indentation:** 2 spaces in HTML/JS; UTF-8 files.

## Testing Guidelines
- Tests live in `tools/tests/` and are PowerShell scripts named `*_tests.ps1`.
- New behavior should add/extend a test script.
- CI runs linting, snapshot tests, and UI compliance checks.

## Commit & Pull Request Guidelines
- Use concise prefixes seen in history: `feat:`, `fix:`, `test:`, `docs:`, `ci:`, `security:`.
- PRs should note **what changed**, **tests run**, and **data/schema impacts**.
- Do not commit generated artifacts (`static/`, `data/snapshots/`, `tools/logs/`).

## Security & Data Integrity
- Product evidence **must** reference a valid source with `sha256` and `local_path` (enforced by `tools/validate.py`).
- Use snapshots for reproducible results; keep release snapshots versioned and verifiable.
