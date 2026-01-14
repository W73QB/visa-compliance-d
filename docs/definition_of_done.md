# Definition of Done (DoD)

A release is considered production-ready only if all checks below pass.

## Build and data pipeline
- `py tools/validate.py` passes
- `py tools/build_mappings.py` passes
- `py tools/build_index.py` passes
- `py tools/sync_hugo_static.py` passes
- `py tools/lint_content.py` passes
- PowerShell tests in `tools/tests/` pass

## Site endpoints
- `/` (home)
- `/posts/`
- `/methodology/`
- `/disclaimer/`
- `/affiliate-disclosure/`
- `/ui/`
- `/data/ui_index.json`
- `/sources/<file>`

## Release gates
- Sync fails if required assets are missing
- Static bundle verification passes
- Smoke checks pass locally and after deploy
