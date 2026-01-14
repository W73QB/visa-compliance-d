# Compliance Stability Gates Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add fail-hard sync, bundle verification, smoke checks, and CI gates so deploys cannot ship missing data/evidence.

**Architecture:** Add small Python/PowerShell guard scripts with env overrides for testability, enforce Hugo version pin in CI, and update Hugo menu links to avoid baseURL/subpath breakage. Tests live in `tools/tests/` and are invoked by CI before deploy.

**Tech Stack:** Python 3, PowerShell, Hugo, GitHub Actions, JSON.

---

### Task 0: Create a dedicated worktree (required for execution)

**Files:**
- Create: `D:\visa-compliance-d-worktrees\stability-gates` (example path)

**Step 1: Create worktree**
Run: `git worktree add ..\visa-compliance-d-worktrees\stability-gates -b feat/stability-gates`
Expected: new worktree directory created.

**Step 2: Enter worktree**
Run: `cd ..\visa-compliance-d-worktrees\stability-gates`
Expected: working directory is the new worktree.

**Step 3: Commit (optional)**
No commit in this task.

---

### Task 1: Add Definition of Done doc

**Files:**
- Create: `docs/definition_of_done.md`

**Step 1: Write the doc**
Create `docs/definition_of_done.md` with:
```markdown
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
```

**Step 2: Verify file exists**
Run: `Test-Path docs/definition_of_done.md`
Expected: `True`.

**Step 3: Commit**
Run:
```bash
git add docs/definition_of_done.md
git commit -m "docs: add definition of done"
```

---

### Task 2: Add requirements.txt

**Files:**
- Create: `requirements.txt`

**Step 1: Write requirements**
Create `requirements.txt` with:
```
jsonschema==4.19.2
```

**Step 2: Install deps**
Run: `pip install -r requirements.txt`
Expected: jsonschema installs successfully.

**Step 3: Commit**
Run:
```bash
git add requirements.txt
git commit -m "chore: add python requirements"
```

---

### Task 3: Make sync_hugo_static fail-hard + add tests

**Files:**
- Modify: `tools/sync_hugo_static.py`
- Create: `tools/tests/sync_hugo_static_tests.ps1`

**Step 1: Write the failing test**
Create `tools/tests/sync_hugo_static_tests.ps1` with:
```powershell
$ErrorActionPreference = "Stop"
$failed = $false

function Assert-True {
  param([bool]$Condition, [string]$Message)
  if (-not $Condition) {
    Write-Host "FAIL: $Message" -ForegroundColor Red
    $script:failed = $true
  } else {
    Write-Host "PASS: $Message" -ForegroundColor Green
  }
}

function New-TempRoot {
  $root = Join-Path $env:TEMP ([System.Guid]::NewGuid().ToString())
  New-Item -ItemType Directory -Path $root | Out-Null
  return $root
}

function Write-MinimalFiles {
  param([string]$Root)
  New-Item -ItemType Directory -Path (Join-Path $Root "ui") | Out-Null
  Set-Content -Path (Join-Path $Root "ui/index.html") -Value "<html></html>"
  New-Item -ItemType Directory -Path (Join-Path $Root "data") | Out-Null
  Set-Content -Path (Join-Path $Root "data/ui_index.json") -Value "{}"
  New-Item -ItemType Directory -Path (Join-Path $Root "sources") | Out-Null
  Set-Content -Path (Join-Path $Root "sources/test.txt") -Value "ok"
}

Write-Host "sync_hugo_static fail-hard checks..." -ForegroundColor Cyan

try {
  # Missing ui should fail
  $root1 = New-TempRoot
  New-Item -ItemType Directory -Path (Join-Path $root1 "data") | Out-Null
  Set-Content -Path (Join-Path $root1 "data/ui_index.json") -Value "{}"
  $env:SYNC_ROOT = $root1
  $proc1 = Start-Process -FilePath "py" -ArgumentList "tools/sync_hugo_static.py" -Wait -PassThru
  Assert-True ($proc1.ExitCode -ne 0) "sync fails when ui/ is missing"

  # Missing ui_index.json should fail
  $root2 = New-TempRoot
  New-Item -ItemType Directory -Path (Join-Path $root2 "ui") | Out-Null
  Set-Content -Path (Join-Path $root2 "ui/index.html") -Value "<html></html>"
  $env:SYNC_ROOT = $root2
  $proc2 = Start-Process -FilePath "py" -ArgumentList "tools/sync_hugo_static.py" -Wait -PassThru
  Assert-True ($proc2.ExitCode -ne 0) "sync fails when data/ui_index.json is missing"

  # RELEASE_BUILD requires sources
  $root3 = New-TempRoot
  Write-MinimalFiles -Root $root3
  Remove-Item -Recurse -Force (Join-Path $root3 "sources")
  $env:SYNC_ROOT = $root3
  $env:RELEASE_BUILD = "1"
  $proc3 = Start-Process -FilePath "py" -ArgumentList "tools/sync_hugo_static.py" -Wait -PassThru
  Assert-True ($proc3.ExitCode -ne 0) "sync fails in release mode when sources/ missing"
  $env:RELEASE_BUILD = ""

  # Happy path
  $root4 = New-TempRoot
  Write-MinimalFiles -Root $root4
  $env:SYNC_ROOT = $root4
  $proc4 = Start-Process -FilePath "py" -ArgumentList "tools/sync_hugo_static.py" -Wait -PassThru
  Assert-True ($proc4.ExitCode -eq 0) "sync succeeds when required inputs exist"
}
finally {
  Remove-Item -Recurse -Force $root1, $root2, $root3, $root4 -ErrorAction SilentlyContinue
}

if ($failed) {
  Write-Error "One or more checks failed."
  exit 1
}

Write-Host "All checks passed." -ForegroundColor Green
```

**Step 2: Run the test (expect FAIL)**
Run: `pwsh -File tools/tests/sync_hugo_static_tests.ps1`
Expected: FAIL because script does not fail-hard yet.

**Step 3: Implement fail-hard in sync_hugo_static.py**
Update `tools/sync_hugo_static.py` to:
```python
import os
import sys
import shutil
from pathlib import Path

ROOT = Path(os.environ.get("SYNC_ROOT", Path(__file__).parent.parent))


def copy_tree(src: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    static = ROOT / "static"
    static.mkdir(exist_ok=True)

    ui_src = ROOT / "ui"
    if not ui_src.exists():
        fail("Missing ui/ directory")
    copy_tree(ui_src, static / "ui")

    index_src = ROOT / "data" / "ui_index.json"
    if not index_src.exists():
        fail("Missing data/ui_index.json")
    copy_file(index_src, static / "data" / "ui_index.json")

    sources_src = ROOT / "sources"
    release = os.environ.get("RELEASE_BUILD", "").lower() in {"1", "true", "yes"}
    if sources_src.exists():
        copy_tree(sources_src, static / "sources")
    elif release:
        fail("Missing sources/ directory in release mode")

    snapshots_src = ROOT / "data" / "snapshots"
    if snapshots_src.exists():
        copy_tree(snapshots_src, static / "snapshots")

    print("Synced UI/data/sources into static/ for Hugo")


if __name__ == "__main__":
    main()
```

**Step 4: Run the test (expect PASS)**
Run: `pwsh -File tools/tests/sync_hugo_static_tests.ps1`
Expected: PASS.

**Step 5: Commit**
Run:
```bash
git add tools/sync_hugo_static.py tools/tests/sync_hugo_static_tests.ps1
git commit -m "test: add sync_hugo_static fail-hard checks"
```

---

### Task 4: Add verify_static_bundle.py + tests

**Files:**
- Create: `tools/verify_static_bundle.py`
- Create: `tools/tests/verify_static_bundle_tests.ps1`

**Step 1: Write the failing test**
Create `tools/tests/verify_static_bundle_tests.ps1` with:
```powershell
$ErrorActionPreference = "Stop"
$failed = $false

function Assert-True {
  param([bool]$Condition, [string]$Message)
  if (-not $Condition) {
    Write-Host "FAIL: $Message" -ForegroundColor Red
    $script:failed = $true
  } else {
    Write-Host "PASS: $Message" -ForegroundColor Green
  }
}

function New-TempRoot {
  $root = Join-Path $env:TEMP ([System.Guid]::NewGuid().ToString())
  New-Item -ItemType Directory -Path $root | Out-Null
  return $root
}

Write-Host "verify_static_bundle checks..." -ForegroundColor Cyan

# Happy path on repo
$proc1 = Start-Process -FilePath "py" -ArgumentList "tools/verify_static_bundle.py" -Wait -PassThru
Assert-True ($proc1.ExitCode -eq 0) "verify passes on current repo"

# Failure on empty sources and empty files
$root = New-TempRoot
New-Item -ItemType Directory -Path (Join-Path $root "static/ui") | Out-Null
New-Item -ItemType Directory -Path (Join-Path $root "static/data") | Out-Null
New-Item -ItemType Directory -Path (Join-Path $root "static/sources") | Out-Null
Set-Content -Path (Join-Path $root "static/ui/index.html") -Value ""
Set-Content -Path (Join-Path $root "static/data/ui_index.json") -Value "{}"
$env:VERIFY_ROOT = $root
$proc2 = Start-Process -FilePath "py" -ArgumentList "tools/verify_static_bundle.py" -Wait -PassThru
Assert-True ($proc2.ExitCode -ne 0) "verify fails on empty bundle"
$env:VERIFY_ROOT = ""

if ($failed) {
  Write-Error "One or more checks failed."
  exit 1
}

Write-Host "All checks passed." -ForegroundColor Green
```

**Step 2: Run the test (expect FAIL)**
Run: `pwsh -File tools/tests/verify_static_bundle_tests.ps1`
Expected: FAIL because script does not exist yet.

**Step 3: Implement verify_static_bundle.py**
Create `tools/verify_static_bundle.py` with:
```python
import os
import sys
from pathlib import Path

ROOT = Path(os.environ.get("VERIFY_ROOT", Path(__file__).parent.parent))


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def require_file(path: Path, label: str) -> None:
    if not path.exists():
        fail(f"Missing {label}: {path}")
    if path.stat().st_size == 0:
        fail(f"Empty {label}: {path}")


def main() -> None:
    ui = ROOT / "static" / "ui" / "index.html"
    index = ROOT / "static" / "data" / "ui_index.json"
    sources_dir = ROOT / "static" / "sources"

    require_file(ui, "ui index")
    require_file(index, "ui index json")

    if not sources_dir.exists():
        fail("Missing static/sources directory")

    sources = [p for p in sources_dir.rglob("*") if p.is_file()]
    if not sources:
        fail("No source files found in static/sources")

    print("Static bundle verification passed")


if __name__ == "__main__":
    main()
```

**Step 4: Run the test (expect PASS)**
Run: `pwsh -File tools/tests/verify_static_bundle_tests.ps1`
Expected: PASS.

**Step 5: Commit**
Run:
```bash
git add tools/verify_static_bundle.py tools/tests/verify_static_bundle_tests.ps1
git commit -m "test: add static bundle verification"
```

---

### Task 5: Add smoke.py + tests

**Files:**
- Create: `tools/smoke.py`
- Create: `tools/tests/smoke_tests.ps1`

**Step 1: Write the failing test**
Create `tools/tests/smoke_tests.ps1` with:
```powershell
$ErrorActionPreference = "Stop"
$failed = $false

function Assert-True {
  param([bool]$Condition, [string]$Message)
  if (-not $Condition) {
    Write-Host "FAIL: $Message" -ForegroundColor Red
    $script:failed = $true
  } else {
    Write-Host "PASS: $Message" -ForegroundColor Green
  }
}

function New-TempRoot {
  $root = Join-Path $env:TEMP ([System.Guid]::NewGuid().ToString())
  New-Item -ItemType Directory -Path $root | Out-Null
  return $root
}

Write-Host "smoke.py checks..." -ForegroundColor Cyan

# Happy path
$root = New-TempRoot
New-Item -ItemType Directory -Path (Join-Path $root "data") | Out-Null
New-Item -ItemType Directory -Path (Join-Path $root "sources") | Out-Null
Set-Content -Path (Join-Path $root "sources/source.txt") -Value "ok"
@"
{
  "mappings": [
    {
      "reasons": [
        { "evidence": [ { "source_id": "SRC1" } ] }
      ]
    }
  ],
  "sources_by_id": {
    "SRC1": { "local_path": "sources/source.txt" }
  }
}
"@ | Set-Content -Path (Join-Path $root "data/ui_index.json")
$env:SMOKE_ROOT = $root
$env:SMOKE_INDEX_PATH = (Join-Path $root "data/ui_index.json")
$proc1 = Start-Process -FilePath "py" -ArgumentList "tools/smoke.py" -Wait -PassThru
Assert-True ($proc1.ExitCode -eq 0) "smoke passes when evidence path exists"

# Failure when evidence missing
Remove-Item -Force (Join-Path $root "sources/source.txt")
$proc2 = Start-Process -FilePath "py" -ArgumentList "tools/smoke.py" -Wait -PassThru
Assert-True ($proc2.ExitCode -ne 0) "smoke fails when evidence file missing"
$env:SMOKE_ROOT = ""
$env:SMOKE_INDEX_PATH = ""

if ($failed) {
  Write-Error "One or more checks failed."
  exit 1
}

Write-Host "All checks passed." -ForegroundColor Green
```

**Step 2: Run the test (expect FAIL)**
Run: `pwsh -File tools/tests/smoke_tests.ps1`
Expected: FAIL because script does not exist yet.

**Step 3: Implement smoke.py**
Create `tools/smoke.py` with:
```python
import json
import os
import sys
from pathlib import Path

ROOT = Path(os.environ.get("SMOKE_ROOT", Path(__file__).parent.parent))
INDEX_PATH = Path(os.environ.get("SMOKE_INDEX_PATH", ROOT / "data" / "ui_index.json"))


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    if not INDEX_PATH.exists():
        fail(f"Missing ui_index.json at {INDEX_PATH}")

    data = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    mappings = data.get("mappings", [])
    sources_by_id = data.get("sources_by_id", {})

    if not mappings:
        fail("No mappings found in ui_index.json")

    chosen = None
    for mapping in mappings:
        for reason in mapping.get("reasons", []) or []:
            if reason.get("evidence"):
                chosen = mapping
                break
        if chosen:
            break

    if not chosen:
        fail("No mapping with evidence found")

    for reason in chosen.get("reasons", []) or []:
        for ev in reason.get("evidence", []) or []:
            source_id = ev.get("source_id")
            if not source_id:
                fail("Evidence missing source_id")
            meta = sources_by_id.get(source_id)
            if not meta:
                fail(f"Missing sources_by_id for {source_id}")
            local_path = meta.get("local_path")
            if not local_path:
                fail(f"Missing local_path for {source_id}")
            evidence_path = ROOT / local_path
            if not evidence_path.exists():
                fail(f"Evidence file not found: {evidence_path}")

    print("Smoke check passed")


if __name__ == "__main__":
    main()
```

**Step 4: Run the test (expect PASS)**
Run: `pwsh -File tools/tests/smoke_tests.ps1`
Expected: PASS.

**Step 5: Commit**
Run:
```bash
git add tools/smoke.py tools/tests/smoke_tests.ps1
git commit -m "test: add smoke evidence checks"
```

---

### Task 6: Pin Hugo version + CI tests gating

**Files:**
- Modify: `.github/workflows/pages.yml`
- Modify: `tools/tests/ui_compliance_tests.ps1`

**Step 0: Preflight check (local)**
Run: `hugo version`
Expected: prints current Hugo version (e.g., `hugo v0.121.1 ...`).

**Step 1: Write failing test**
Update `tools/tests/ui_compliance_tests.ps1` to add:
```powershell
if (Test-Path $pagesPath) {
  $pages = Get-Content -Raw -Path $pagesPath
  Assert-True ($pages -notlike '*hugo-version: "latest"*') "pages workflow does not use Hugo latest"
  Assert-True ($pages -like '*hugo-version: "0.121.1"*') "pages workflow pins Hugo version"
}
```

**Step 2: Run the test (expect FAIL)**
Run: `pwsh -File tools/tests/ui_compliance_tests.ps1`
Expected: FAIL because pages.yml uses latest.

**Step 3: Pin Hugo version in pages.yml**
Update the Hugo setup step to:
```yaml
      - name: Setup Hugo
        uses: peaceiris/actions-hugo@v3
        with:
          hugo-version: "0.121.1"
          extended: true
```

**Step 4: Commit (pin Hugo only)**
Run:
```bash
git add .github/workflows/pages.yml tools/tests/ui_compliance_tests.ps1
git commit -m "ci: pin hugo version"
```

**Step 5: Add test step in CI**
Add a step in `pages.yml` after sync and before build:
```yaml
      - name: Run tests
        run: |
          pwsh -File tools/tests/ui_compliance_tests.ps1
          pwsh -File tools/tests/validate_product_sources_tests.ps1
          pwsh -File tools/tests/snapshot_tests.ps1
          pwsh -File tools/tests/snapshot_routing_tests.ps1
          pwsh -File tools/tests/release_snapshot_tests.ps1
          pwsh -File tools/tests/verify_snapshot_manifest_tests.ps1
          pwsh -File tools/tests/offers_tests.ps1
          pwsh -File tools/tests/content_lint_tests.ps1
          pwsh -File tools/tests/source_monitor_tests.ps1
          pwsh -File tools/tests/hugo_integration_tests.ps1
          pwsh -File tools/tests/sync_hugo_static_tests.ps1
          pwsh -File tools/tests/verify_static_bundle_tests.ps1
          pwsh -File tools/tests/smoke_tests.ps1
```

**Step 6: Run the test (expect PASS)**
Run: `pwsh -File tools/tests/ui_compliance_tests.ps1`
Expected: PASS.

**Step 7: Commit (add CI gating)**
Run:
```bash
git add .github/workflows/pages.yml
git commit -m "ci: run full test suite before deploy"
```

---

### Task 7: Update Hugo menu links to avoid baseURL/subpath issues

**Files:**
- Modify: `hugo.toml`
- Modify: `tools/tests/hugo_integration_tests.ps1`

**Step 1: Write failing test**
Update `tools/tests/hugo_integration_tests.ps1` to assert pageRef usage and relative url:
```powershell
if (Test-Path "hugo.toml") {
  $hugo = Get-Content -Raw -Path "hugo.toml"
  Assert-True ($hugo -like '*pageRef = "posts"*') "menu uses pageRef for posts"
  Assert-True ($hugo -like '*pageRef = "methodology"*') "menu uses pageRef for methodology"
  Assert-True ($hugo -like '*pageRef = "disclaimer"*') "menu uses pageRef for disclaimer"
  Assert-True ($hugo -like '*pageRef = "affiliate-disclosure"*') "menu uses pageRef for affiliate disclosure"
  Assert-True ($hugo -like '*url = "ui/"*') "checker menu uses relative url"
}
```

**Step 2: Run the test (expect FAIL)**
Run: `pwsh -File tools/tests/hugo_integration_tests.ps1`
Expected: FAIL with current menu config.

**Step 3: Update hugo.toml**
Replace menu block with:
```toml
[menu]
  [[menu.main]]
    name = "Checker"
    url = "ui/"
    weight = 1
  [[menu.main]]
    name = "Blog"
    pageRef = "posts"
    weight = 2
  [[menu.main]]
    name = "Methodology"
    pageRef = "methodology"
    weight = 3
  [[menu.main]]
    name = "Disclaimer"
    pageRef = "disclaimer"
    weight = 4
  [[menu.main]]
    name = "Affiliate"
    pageRef = "affiliate-disclosure"
    weight = 5
```

**Step 4: Run the test (expect PASS)**
Run: `pwsh -File tools/tests/hugo_integration_tests.ps1`
Expected: PASS.

**Step 5: Commit**
Run:
```bash
git add hugo.toml tools/tests/hugo_integration_tests.ps1
git commit -m "fix: harden hugo menu links"
```

---

### Task 8: Add smoke_http.ps1 (post-deploy verification)

**Files:**
- Create: `tools/smoke_http.ps1`

**Step 1: Write the script**
Create `tools/smoke_http.ps1` with:
```powershell
param(
  [Parameter(Mandatory = $true)][string]$BaseUrl
)

$ErrorActionPreference = "Stop"
$failed = $false

function Assert-True {
  param([bool]$Condition, [string]$Message)
  if (-not $Condition) {
    Write-Host "FAIL: $Message" -ForegroundColor Red
    $script:failed = $true
  } else {
    Write-Host "PASS: $Message" -ForegroundColor Green
  }
}

function Get-Ok {
  param([string]$Url)
  try {
    return Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 30
  } catch {
    Write-Host "ERROR: $Url -> $($_.Exception.Message)" -ForegroundColor Red
    $script:failed = $true
    return $null
  }
}

$base = $BaseUrl.TrimEnd("/")

Write-Host "Smoke HTTP checks..." -ForegroundColor Cyan

$ui = Get-Ok "$base/ui/"
if ($ui) { Assert-True ($ui.StatusCode -eq 200) "/ui/ returns 200" }

$index = Get-Ok "$base/data/ui_index.json"
if ($index) {
  Assert-True ($index.StatusCode -eq 200) "/data/ui_index.json returns 200"
  $json = $index.Content | ConvertFrom-Json
  $first = $json.sources_by_id.PSObject.Properties[0].Value
  if ($null -ne $first -and $first.local_path) {
    $src = Get-Ok ("$base/" + $first.local_path.TrimStart("/"))
    if ($src) { Assert-True ($src.StatusCode -eq 200) "source file returns 200" }
  } else {
    Assert-True $false "ui_index.json has at least one source"
  }
}

if ($failed) {
  Write-Error "One or more checks failed."
  exit 1
}

Write-Host "All checks passed." -ForegroundColor Green
```

**Step 2: Dry run (expect parameter error)**
Run: `pwsh -File tools/smoke_http.ps1`
Expected: PowerShell complains BaseUrl is mandatory.

**Step 3: Commit**
Run:
```bash
git add tools/smoke_http.ps1
git commit -m "test: add post-deploy smoke http script"
```

---

### Task 9: Create 1-2 pillar posts that pass lint

**Files:**
- Create: `content/posts/<visa-1>.md`
- Create: `content/posts/<visa-2>.md`
- Reference: `content/templates/compliance-post-template.md`

**Step 1: Draft post #1**
Create a post by copying the template and filling all required sections. Example skeleton:
```markdown
---
title: "Spain DNV insurance requirements (evidence-based)"
date: 2026-01-14
---

## what the authority requires
[Summarize requirements with evidence references]

## how we evaluate
[Explain mapping logic for this visa]

## check in the engine
[Link to /ui/ with snapshot=YYYY-MM-DD]

## disclaimer
[Required disclaimer text]

## affiliate disclosure
[Required disclosure text]
```

**Step 2: Draft post #2**
Repeat for a second visa (or skip if you only want one pillar post).

**Step 3: Run lint**
Run: `py tools/lint_content.py`
Expected: PASS.

**Step 4: Commit**
Run:
```bash
git add content/posts
git commit -m "docs: add initial pillar posts"
```

---

### Task 10: Final verification (local)

**Files:**
- No changes

**Step 1: Run pipeline**
Run:
```bash
py tools/validate.py
py tools/build_mappings.py
py tools/build_index.py
py tools/sync_hugo_static.py
py tools/lint_content.py
pwsh -File tools/tests/ui_compliance_tests.ps1
pwsh -File tools/tests/sync_hugo_static_tests.ps1
pwsh -File tools/tests/verify_static_bundle_tests.ps1
pwsh -File tools/tests/smoke_tests.ps1
```
Expected: all commands exit 0.

**Step 2: Commit (if any uncommitted changes)**
Run: `git status -sb` and commit remaining edits.

---

# Execution Handoff

Plan complete and saved to `docs/plans/2026-01-14-stability-gates-implementation-plan.md`.

Two execution options:
1. Subagent-Driven (this session) - I dispatch fresh subagent per task, review between tasks, fast iteration
2. Parallel Session (separate) - Open new session with executing-plans, batch execution with checkpoints

Which approach?
