
# Compliance Next-Phase Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add release snapshots with reproducible UI links, content/offer linting, CTA rules, and source-change monitoring with CI support.

**Architecture:** Build release snapshots into `data/snapshots/releases/<id>` with a manifest verifier, update the UI to load `ui_index.json` from a `snapshot=` query param when present, and add Python lint/validation scripts for content and offers. Add a scheduled workflow that checks remote sources and opens a GitHub issue when they change, while keeping CI green and publishing snapshots to Hugo via `static/snapshots/`.

**Tech Stack:** Python 3.11+, PowerShell test scripts, Hugo, GitHub Actions, static HTML/JS.

---

### Task 1: Add snapshot manifest verifier

**Files:**
- Create: `tools/verify_snapshot_manifest.py`
- Test: `tools/tests/verify_snapshot_manifest_tests.ps1`

**Step 1: Write the failing test**

```powershell
$ErrorActionPreference = "Stop"
$failed = $false

function Assert-True {
  param([bool]$Condition, [string]$Message)
  if (-not $Condition) { Write-Host "FAIL: $Message" -ForegroundColor Red; $script:failed = $true }
  else { Write-Host "PASS: $Message" -ForegroundColor Green }
}

$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$snapshotId = "ZZ_VERIFY_TEST_" + (Get-Random -Minimum 10000 -Maximum 99999)
$env:SNAPSHOT_ID = $snapshotId
$env:SNAPSHOT_ROOT = Join-Path $root "data/.snapshots_verify_test"
$snapshotDir = Join-Path $env:SNAPSHOT_ROOT $snapshotId

function Cleanup {
  if (Test-Path $env:SNAPSHOT_ROOT) {
    Get-ChildItem -Recurse -Force -Path $env:SNAPSHOT_ROOT | ForEach-Object { try { $_.Attributes = "Normal" } catch {} }
    Remove-Item -LiteralPath $env:SNAPSHOT_ROOT -Recurse -Force
  }
  Remove-Item Env:SNAPSHOT_ID -ErrorAction SilentlyContinue
  Remove-Item Env:SNAPSHOT_ROOT -ErrorAction SilentlyContinue
}

try {
  $proc = Start-Process -FilePath "py" -ArgumentList "tools/build_snapshot.py" -WorkingDirectory $root -Wait -PassThru
  Assert-True ($proc.ExitCode -eq 0) "build_snapshot.py runs"

  $proc2 = Start-Process -FilePath "py" -ArgumentList @("tools/verify_snapshot_manifest.py", "--snapshot-dir", $snapshotDir) -WorkingDirectory $root -Wait -PassThru
  Assert-True ($proc2.ExitCode -eq 0) "verify_snapshot_manifest.py passes on fresh snapshot"

  # Corrupt a file to ensure verifier fails
  Add-Content -Path (Join-Path $snapshotDir "ui_index.json") -Value " "
  $proc3 = Start-Process -FilePath "py" -ArgumentList @("tools/verify_snapshot_manifest.py", "--snapshot-dir", $snapshotDir) -WorkingDirectory $root -Wait -PassThru
  Assert-True ($proc3.ExitCode -ne 0) "verify_snapshot_manifest.py fails on mismatch"
} finally {
  Cleanup
}

if ($failed) { Write-Error "One or more checks failed."; exit 1 }
Write-Host "All checks passed." -ForegroundColor Green
```

**Step 2: Run test to verify it fails**

Run: `powershell -NoProfile -File tools/tests/verify_snapshot_manifest_tests.ps1`
Expected: FAIL because `tools/verify_snapshot_manifest.py` does not exist yet.

**Step 3: Write minimal implementation**

```python
import argparse
import hashlib
import json
import sys
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify(snapshot_dir: Path) -> int:
    manifest_path = snapshot_dir / "manifest.json"
    if not manifest_path.exists():
        print(f"[ERROR] Missing manifest: {manifest_path}")
        return 1
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    errors = 0
    for entry in manifest.get("files", []):
        rel = entry.get("path")
        expected = entry.get("sha256")
        if not rel or not expected:
            print("[ERROR] manifest entry missing path/sha256")
            errors += 1
            continue
        path = snapshot_dir / rel
        if not path.exists():
            print(f"[ERROR] Missing file: {rel}")
            errors += 1
            continue
        actual = sha256(path)
        if actual.lower() != str(expected).lower():
            print(f"[ERROR] SHA mismatch: {rel}")
            errors += 1

    if errors:
        print(f"[FAIL] {errors} error(s) found")
        return 1

    print("[OK] manifest verified")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--snapshot-dir", required=True)
    args = parser.parse_args()
    sys.exit(verify(Path(args.snapshot_dir)))


if __name__ == "__main__":
    main()
```

**Step 4: Run test to verify it passes**

Run: `powershell -NoProfile -File tools/tests/verify_snapshot_manifest_tests.ps1`
Expected: PASS lines and exit code 0.

**Step 5: Commit**

```bash
git add tools/verify_snapshot_manifest.py tools/tests/verify_snapshot_manifest_tests.ps1
git commit -m "test: add snapshot manifest verifier"
```
### Task 2: Add release snapshot builder

**Files:**
- Create: `tools/build_release_snapshot.py`
- Test: `tools/tests/release_snapshot_tests.ps1`

**Step 1: Write the failing test**

```powershell
$ErrorActionPreference = "Stop"
$failed = $false

function Assert-True {
  param([bool]$Condition, [string]$Message)
  if (-not $Condition) { Write-Host "FAIL: $Message" -ForegroundColor Red; $script:failed = $true }
  else { Write-Host "PASS: $Message" -ForegroundColor Green }
}

$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$releaseId = "REL_TEST_" + (Get-Random -Minimum 10000 -Maximum 99999)
$releaseDir = Join-Path $root ("data/snapshots/releases/" + $releaseId)

try {
  $proc = Start-Process -FilePath "py" -ArgumentList @("tools/build_release_snapshot.py", "--release-id", $releaseId) -WorkingDirectory $root -Wait -PassThru
  Assert-True ($proc.ExitCode -eq 0) "build_release_snapshot.py runs"
  Assert-True (Test-Path $releaseDir) "release snapshot directory exists"
  Assert-True (Test-Path (Join-Path $releaseDir "manifest.json")) "release snapshot has manifest"

  $proc2 = Start-Process -FilePath "py" -ArgumentList @("tools/verify_snapshot_manifest.py", "--snapshot-dir", $releaseDir) -WorkingDirectory $root -Wait -PassThru
  Assert-True ($proc2.ExitCode -eq 0) "release manifest verifies"
} finally {
  if (Test-Path $releaseDir) { Remove-Item -LiteralPath $releaseDir -Recurse -Force }
}

if ($failed) { Write-Error "One or more checks failed."; exit 1 }
Write-Host "All checks passed." -ForegroundColor Green
```

**Step 2: Run test to verify it fails**

Run: `powershell -NoProfile -File tools/tests/release_snapshot_tests.ps1`
Expected: FAIL because `tools/build_release_snapshot.py` does not exist yet.

**Step 3: Write minimal implementation**

```python
import argparse
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--release-id", required=True)
    args = parser.parse_args()

    release_id = args.release_id
    release_root = ROOT / "data" / "snapshots" / "releases"
    release_root.mkdir(parents=True, exist_ok=True)

    env = os.environ.copy()
    env["SNAPSHOT_ID"] = release_id
    env["SNAPSHOT_ROOT"] = str(release_root)

    # Rebuild ui_index.json with the release snapshot id.
    subprocess.run([sys.executable, "tools/build_index.py"], check=True, env=env, cwd=ROOT)

    # Build snapshot into data/snapshots/releases/<release-id>
    subprocess.run([sys.executable, "tools/build_snapshot.py"], check=True, env=env, cwd=ROOT)

    print(f"Release snapshot built: {release_root / release_id}")


if __name__ == "__main__":
    main()
```

**Step 4: Run test to verify it passes**

Run: `powershell -NoProfile -File tools/tests/release_snapshot_tests.ps1`
Expected: PASS lines and exit code 0.

**Step 5: Commit**

```bash
git add tools/build_release_snapshot.py tools/tests/release_snapshot_tests.ps1
git commit -m "feat: add release snapshot builder"
```
### Task 3: Wire release snapshots into CI (manual)

**Files:**
- Modify: `.github/workflows/pages.yml`
- Modify: `.github/workflows/ui-compliance.yml`

**Step 1: Write the failing test (workflow string check)**

Add to `tools/tests/ui_compliance_tests.ps1`:

```powershell
$pages = Get-Content -Raw -Path ".github/workflows/pages.yml"
Assert-True ($pages -like "*workflow_dispatch*") "pages workflow supports manual release builds"
Assert-True ($pages -like "*build_release_snapshot.py*") "pages workflow runs release snapshot when requested"
```

**Step 2: Run test to verify it fails**

Run: `powershell -NoProfile -File tools/tests/ui_compliance_tests.ps1`
Expected: FAIL because pages.yml has no release snapshot step.

**Step 3: Write minimal implementation**

Update `.github/workflows/pages.yml`:

```yaml
on:
  push:
    branches: ["main"]
  workflow_dispatch:
    inputs:
      release_id:
        description: "Release snapshot id (e.g., 2026-01-12)"
        required: false
        default: ""
```

Add a step before Hugo build:

```yaml
      - name: Build release snapshot (optional)
        if: ${{ inputs.release_id != '' }}
        run: |
          $env:SNAPSHOT_ID = "${{ inputs.release_id }}"
          python tools/build_release_snapshot.py --release-id "${{ inputs.release_id }}"
```

Add to `.github/workflows/ui-compliance.yml`:

```yaml
      - name: Run release snapshot tests
        run: powershell -NoProfile -File tools/tests/release_snapshot_tests.ps1
      - name: Run manifest verify tests
        run: powershell -NoProfile -File tools/tests/verify_snapshot_manifest_tests.ps1
```

**Step 4: Run test to verify it passes**

Run: `powershell -NoProfile -File tools/tests/ui_compliance_tests.ps1`
Expected: PASS lines for workflow checks.

**Step 5: Commit**

```bash
git add .github/workflows/pages.yml .github/workflows/ui-compliance.yml tools/tests/ui_compliance_tests.ps1
git commit -m "ci: add manual release snapshot support"
```
### Task 4: Snapshot-aware UI data loading + deep links

**Files:**
- Modify: `ui/index.html`
- Test: `tools/tests/snapshot_routing_tests.ps1`

**Step 1: Write the failing test**

```powershell
$ErrorActionPreference = "Stop"
$failed = $false

function Assert-True {
  param([bool]$Condition, [string]$Message)
  if (-not $Condition) { Write-Host "FAIL: $Message" -ForegroundColor Red; $script:failed = $true }
  else { Write-Host "PASS: $Message" -ForegroundColor Green }
}

$ui = Get-Content -Raw -Path "ui/index.html"
Assert-True ($ui -like "*snapshot=*" ) "UI references snapshot query param"
Assert-True ($ui -like "*snapshots/*" ) "UI builds data URL under snapshots/"
Assert-True ($ui -like "*searchParams.set(\"snapshot\"*" ) "Deep link preserves snapshot param"

if ($failed) { Write-Error "One or more checks failed."; exit 1 }
Write-Host "All checks passed." -ForegroundColor Green
```

**Step 2: Run test to verify it fails**

Run: `powershell -NoProfile -File tools/tests/snapshot_routing_tests.ps1`
Expected: FAIL because UI has no snapshot param logic.

**Step 3: Write minimal implementation**

Update `ui/index.html`:

```html
<script>
const SNAPSHOT_PARAM = new URLSearchParams(location.search).get("snapshot");

function resolveDataUrl(pathname, snapshot) {
  const path = String(pathname || "").replace(/\\/g, "/");
  const safeSnapshot = snapshot ? snapshot.replace(/^\/+/, "") : "";
  if (safeSnapshot) {
    if (path.endsWith("/ui/index.html") || path.endsWith("/ui/")) {
      return "../snapshots/" + safeSnapshot + "/ui_index.json";
    }
    return "snapshots/" + safeSnapshot + "/ui_index.json";
  }
  if (path.endsWith("/ui/index.html") || path.endsWith("/ui/")) {
    return "../data/ui_index.json";
  }
  return "data/ui_index.json";
}

const DATA_URL = resolveDataUrl(location.pathname, SNAPSHOT_PARAM);
</script>
```

Update snapshot display and deep-linking:

```javascript
$("snapshotId").textContent = SNAPSHOT_PARAM || INDEX.snapshot_id || "-";

const url = new URL(location.href);
if (SNAPSHOT_PARAM) url.searchParams.set("snapshot", SNAPSHOT_PARAM);
```

**Step 4: Run test to verify it passes**

Run: `powershell -NoProfile -File tools/tests/snapshot_routing_tests.ps1`
Expected: PASS lines and exit code 0.

**Step 5: Commit**

```bash
git add ui/index.html tools/tests/snapshot_routing_tests.ps1
git commit -m "feat: add snapshot-aware UI data loading"
```
### Task 5: Add compliance-first content template

**Files:**
- Create: `content/templates/compliance-post-template.md`

**Step 1: Write the template file**

```markdown
---
title: "[Visa] Compliance Update"
date: 2026-01-13
description: "Evidence-based compliance verification summary."
tags: ["compliance", "visa"]
---

## What the authority requires

- Cite official rule(s) with source excerpts.

## How we evaluate

- Link: /methodology/

## Check in the engine

- Deep link: /ui/?visa=...&product=...&snapshot=releases/YYYY-MM-DD

## Disclaimer

Not legal advice. Compliance results are evidence-based snapshots.

## Affiliate disclosure

If an affiliate link is present, it appears only after results and does not change the compliance outcome.
```

**Step 2: Commit**

```bash
git add content/templates/compliance-post-template.md
git commit -m "docs: add compliance-first post template"
```

### Task 6: Add content lint script + tests + CI hook

**Files:**
- Create: `tools/lint_content.py`
- Test: `tools/tests/content_lint_tests.ps1`
- Modify: `.github/workflows/ui-compliance.yml`
- Modify: `.github/workflows/pages.yml`

**Step 1: Write the failing test**

```powershell
$ErrorActionPreference = "Stop"
$failed = $false

function Assert-True {
  param([bool]$Condition, [string]$Message)
  if (-not $Condition) { Write-Host "FAIL: $Message" -ForegroundColor Red; $script:failed = $true }
  else { Write-Host "PASS: $Message" -ForegroundColor Green }
}

$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$tempDir = Join-Path $root "data/.content_lint_test"
New-Item -ItemType Directory -Path $tempDir | Out-Null

$badPath = Join-Path $tempDir "bad.md"
Set-Content -Path $badPath -Value "# Missing sections and says best"

$goodPath = Join-Path $tempDir "good.md"
@"
---
title: "Test"
---

## What the authority requires

Text.

## How we evaluate

/methodology/

## Check in the engine

/ui/?visa=xx&product=yy&snapshot=releases/2026-01-12

## Disclaimer

Not legal advice.

## Affiliate disclosure

Disclosure text.
"@ | Set-Content -Path $goodPath

$proc = Start-Process -FilePath "py" -ArgumentList @("tools/lint_content.py", "--path", $badPath) -WorkingDirectory $root -Wait -PassThru
Assert-True ($proc.ExitCode -ne 0) "lint fails for missing blocks"

$proc2 = Start-Process -FilePath "py" -ArgumentList @("tools/lint_content.py", "--path", $goodPath) -WorkingDirectory $root -Wait -PassThru
Assert-True ($proc2.ExitCode -eq 0) "lint passes for valid post"

Remove-Item -LiteralPath $tempDir -Recurse -Force

if ($failed) { Write-Error "One or more checks failed."; exit 1 }
Write-Host "All checks passed." -ForegroundColor Green
```

**Step 2: Run test to verify it fails**

Run: `powershell -NoProfile -File tools/tests/content_lint_tests.ps1`
Expected: FAIL because `tools/lint_content.py` does not exist.

**Step 3: Write minimal implementation**

```python
import argparse
import re
import sys
from pathlib import Path

REQUIRED_BLOCKS = [
    "what the authority requires",
    "how we evaluate",
    "check in the engine",
    "disclaimer",
    "affiliate disclosure",
]

BANNED_WORDS = ["best", "recommend", "recommended", "guarantee", "guaranteed", "100%", "approved", "surely"]


def lint_text(text: str) -> list[str]:
    errors = []
    lower = text.lower()
    for block in REQUIRED_BLOCKS:
        if block not in lower:
            errors.append(f"missing block: {block}")
    if "snapshot=" not in lower:
        errors.append("missing snapshot= in deep link")
    for word in BANNED_WORDS:
        if re.search(rf"\b{re.escape(word)}\b", lower):
            errors.append(f"banned word: {word}")
    return errors


def lint_file(path: Path) -> int:
    text = path.read_text(encoding="utf-8", errors="replace")
    errors = lint_text(text)
    if errors:
        print(f"[ERROR] {path}")
        for err in errors:
            print("  ", err)
        return 1
    print(f"[OK] {path}")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str, help="Single markdown file to lint")
    parser.add_argument("--root", type=str, default="content", help="Root content directory")
    args = parser.parse_args()

    if args.path:
        sys.exit(lint_file(Path(args.path)))

    root = Path(args.root)
    failures = 0
    for path in root.rglob("*.md"):
        failures += lint_file(path)
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
```

**Step 4: Run test to verify it passes**

Run: `powershell -NoProfile -File tools/tests/content_lint_tests.ps1`
Expected: PASS lines and exit code 0.

**Step 5: Add CI steps**

In `.github/workflows/ui-compliance.yml` add:

```yaml
      - name: Lint content
        run: py tools/lint_content.py
```

In `.github/workflows/pages.yml` add (before Hugo build):

```yaml
      - name: Lint content
        run: python tools/lint_content.py
```

**Step 6: Commit**

```bash
git add tools/lint_content.py tools/tests/content_lint_tests.ps1 .github/workflows/ui-compliance.yml .github/workflows/pages.yml
git commit -m "test: add content linting"
```
### Task 7: Add offers schema + validation + tests

**Files:**
- Create: `schemas/offers.schema.json`
- Create: `data/offers/offers.json`
- Modify: `tools/validate.py`
- Test: `tools/tests/offers_tests.ps1`

**Step 1: Write the failing test**

```powershell
$ErrorActionPreference = "Stop"
$failed = $false

function Assert-True {
  param([bool]$Condition, [string]$Message)
  if (-not $Condition) { Write-Host "FAIL: $Message" -ForegroundColor Red; $script:failed = $true }
  else { Write-Host "PASS: $Message" -ForegroundColor Green }
}

$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$tempDir = Join-Path $root "data/.offers_test"
New-Item -ItemType Directory -Path $tempDir | Out-Null

$bad = Join-Path $tempDir "bad.json"
@"
{
  "offers": [
    {"product_id": "P1", "affiliate_url": "https://example.com", "label": "Best offer"}
  ]
}
"@ | Set-Content -Path $bad

$proc = Start-Process -FilePath "py" -ArgumentList @("tools/validate.py", "--offers", $bad) -WorkingDirectory $root -Wait -PassThru
Assert-True ($proc.ExitCode -ne 0) "validate fails for banned words"

$good = Join-Path $tempDir "good.json"
@"
{
  "offers": [
    {"product_id": "P1", "affiliate_url": "https://example.com", "label": "Get quote", "disclosure": "Affiliate link"}
  ]
}
"@ | Set-Content -Path $good

$proc2 = Start-Process -FilePath "py" -ArgumentList @("tools/validate.py", "--offers", $good) -WorkingDirectory $root -Wait -PassThru
Assert-True ($proc2.ExitCode -eq 0) "validate passes for good offer"

Remove-Item -LiteralPath $tempDir -Recurse -Force

if ($failed) { Write-Error "One or more checks failed."; exit 1 }
Write-Host "All checks passed." -ForegroundColor Green
```

**Step 2: Run test to verify it fails**

Run: `powershell -NoProfile -File tools/tests/offers_tests.ps1`
Expected: FAIL because `--offers` is not supported.

**Step 3: Write minimal implementation**

Create `schemas/offers.schema.json`:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Offers",
  "type": "object",
  "required": ["offers"],
  "properties": {
    "offers": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["product_id", "affiliate_url", "label"],
        "properties": {
          "product_id": { "type": "string" },
          "affiliate_url": { "type": "string" },
          "label": { "type": "string" },
          "disclosure": { "type": "string" }
        }
      }
    }
  }
}
```

Create `data/offers/offers.json` (example):

```json
{
  "offers": [
    {
      "product_id": "SW_TRAVEL_2026",
      "affiliate_url": "https://example.com/quote",
      "label": "Get quote",
      "disclosure": "Affiliate link. Results are evidence-based."
    }
  ]
}
```

Update `tools/validate.py`:

```python
offers_schema = json.loads((SCHEMAS / "offers.schema.json").read_text(encoding="utf-8"))

BANNED_OFFER_WORDS = ["best", "recommend", "recommended", "guarantee", "guaranteed", "100%", "approved", "surely"]

def check_offer_language(data, path):
    global errors
    for offer in data.get("offers", []):
        text = (offer.get("label", "") + " " + offer.get("disclosure", "")).lower()
        for word in BANNED_OFFER_WORDS:
            if re.search(rf"\b{re.escape(word)}\b", text):
                print(f"[ERROR] Offers: {path}")
                print("  ", f"Banned word in offer: {word}")
                errors += 1
                break

# add argparse
parser.add_argument("--offers", type=str, help="Path to a single offers JSON to validate")

# in main dispatch
elif args.offers:
    validate_file(Path(args.offers), offers_schema, "Offers")
    check_offer_language(json.loads(Path(args.offers).read_text(encoding="utf-8")), Path(args.offers))
else:
    validate_files(DATA / "offers", offers_schema, "Offers")
    # iterate each file to check banned words
```

**Step 4: Run test to verify it passes**

Run: `powershell -NoProfile -File tools/tests/offers_tests.ps1`
Expected: PASS lines and exit code 0.

**Step 5: Commit**

```bash
git add schemas/offers.schema.json data/offers/offers.json tools/validate.py tools/tests/offers_tests.ps1
git commit -m "feat: add offers schema and validation"
```
### Task 8: Build index offers + CTA rules in UI

**Files:**
- Modify: `tools/build_index.py`
- Modify: `ui/index.html`
- Modify: `tools/tests/ui_compliance_tests.ps1`

**Step 1: Write the failing test (UI + index)**

Add to `tools/tests/ui_compliance_tests.ps1`:

```powershell
Assert-True ($ui -like "*offerCta*") "UI has offer CTA container"
Assert-True ($ui -like "*Affiliate*" ) "UI renders affiliate disclosure"
Assert-True ($ui -like "*status === \"RED\"*" ) "UI hides CTA for RED"

$hasOffers = $index.PSObject.Properties.Name -contains "offers_by_product"
Assert-True $hasOffers "ui_index.json contains offers_by_product"
```

**Step 2: Run test to verify it fails**

Run: `powershell -NoProfile -File tools/tests/ui_compliance_tests.ps1`
Expected: FAIL because UI and index do not include offers.

**Step 3: Write minimal implementation**

Update `tools/build_index.py`:

```python
OFFERS = ROOT / "data" / "offers"

def load_offers(folder):
    offers = []
    for p in sorted(folder.rglob("*.json")):
        if p.name.startswith("."):
            continue
        data = json.loads(p.read_text(encoding="utf-8"))
        offers.extend(data.get("offers", []))
    return offers

offers = load_offers(OFFERS) if OFFERS.exists() else []
offers_by_product = {o.get("product_id"): o for o in offers if o.get("product_id")}

# include in data
"offers": offers,
"offers_by_product": offers_by_product,
```

Update `ui/index.html` (add CTA container near result footer):

```html
<div id="offerCta" class="mt-6 hidden">
  <div class="p-4 rounded-lg border border-border-soft dark:border-border-dark bg-white dark:bg-gray-800">
    <div id="offerMessage" class="text-sm text-text-primary dark:text-white font-semibold"></div>
    <a id="offerLink" class="mt-3 inline-flex items-center gap-2 px-4 py-2 bg-primary hover:bg-primary-hover text-white text-sm font-semibold rounded-lg" target="_blank" rel="noopener" href="#">Get quote</a>
    <div id="offerDisclosure" class="mt-2 text-xs text-text-secondary dark:text-gray-400">Affiliate link.</div>
  </div>
</div>
```

Add JS logic:

```javascript
function renderOffer(mapping, productId) {
  const status = (mapping?.status || "UNKNOWN").toUpperCase();
  const offer = INDEX.offers_by_product ? INDEX.offers_by_product[productId] : null;

  const box = $("offerCta");
  const message = $("offerMessage");
  const link = $("offerLink");
  const disclosure = $("offerDisclosure");

  box.classList.add("hidden");
  link.href = "#";

  if (status === "RED" || status === "UNKNOWN") return;
  if (status === "NOT_REQUIRED") {
    message.textContent = "Insurance is optional for this visa.";
    disclosure.textContent = "No affiliate link shown.";
    box.classList.remove("hidden");
    link.classList.add("hidden");
    return;
  }
  if (!offer) return;

  link.classList.remove("hidden");
  link.textContent = offer.label || "Get quote";
  link.href = offer.affiliate_url;
  disclosure.textContent = offer.disclosure || "Affiliate link. Results are evidence-based.";

  if (status === "YELLOW") {
    message.textContent = "Caution: operational risk. Affiliate link shown for convenience.";
  } else {
    message.textContent = "Meets listed requirements based on evidence.";
  }

  box.classList.remove("hidden");
}

// call from renderResult()
renderOffer(mapping, productId);
```

**Step 4: Run test to verify it passes**

Run: `powershell -NoProfile -File tools/tests/ui_compliance_tests.ps1`
Expected: PASS lines and exit code 0.

**Step 5: Commit**

```bash
git add tools/build_index.py ui/index.html tools/tests/ui_compliance_tests.ps1
git commit -m "feat: add offers to UI and index"
```
### Task 9: Add source monitoring script + tests

**Files:**
- Create: `tools/check_source_changes.py`
- Test: `tools/tests/source_monitor_tests.ps1`
- Create: `tools/tests/fixtures/source_monitor/sources/TEST_SOURCE.meta.json`
- Create: `tools/tests/fixtures/source_monitor/fixtures/TEST_SOURCE.txt`

**Step 1: Write the failing test**

```powershell
$ErrorActionPreference = "Stop"
$failed = $false

function Assert-True {
  param([bool]$Condition, [string]$Message)
  if (-not $Condition) { Write-Host "FAIL: $Message" -ForegroundColor Red; $script:failed = $true }
  else { Write-Host "PASS: $Message" -ForegroundColor Green }
}

$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$fixtures = Join-Path $root "tools/tests/fixtures/source_monitor"
$sourcesDir = Join-Path $fixtures "sources"
$fixtureDir = Join-Path $fixtures "fixtures"
$out1 = Join-Path $fixtures "out1.json"
$out2 = Join-Path $fixtures "out2.json"

$proc = Start-Process -FilePath "py" -ArgumentList @("tools/check_source_changes.py", "--sources-dir", $sourcesDir, "--fixture-dir", $fixtureDir, "--output", $out1) -WorkingDirectory $root -Wait -PassThru
Assert-True ($proc.ExitCode -eq 0) "source check runs"
$report1 = Get-Content -Raw -Path $out1 | ConvertFrom-Json
Assert-True ($report1.changed.Count -eq 0) "no changes when fixture matches"

# mutate fixture to simulate change
Add-Content -Path (Join-Path $fixtureDir "TEST_SOURCE.txt") -Value "x"
$proc2 = Start-Process -FilePath "py" -ArgumentList @("tools/check_source_changes.py", "--sources-dir", $sourcesDir, "--fixture-dir", $fixtureDir, "--output", $out2) -WorkingDirectory $root -Wait -PassThru
Assert-True ($proc2.ExitCode -eq 0) "source check runs after mutation"
$report2 = Get-Content -Raw -Path $out2 | ConvertFrom-Json
Assert-True ($report2.changed.Count -eq 1) "change detected"

if ($failed) { Write-Error "One or more checks failed."; exit 1 }
Write-Host "All checks passed." -ForegroundColor Green
```

**Step 2: Run test to verify it fails**

Run: `powershell -NoProfile -File tools/tests/source_monitor_tests.ps1`
Expected: FAIL because the script and fixtures do not exist.

**Step 3: Write minimal implementation**

Create fixtures:

`tools/tests/fixtures/source_monitor/sources/TEST_SOURCE.meta.json`

```json
{
  "source_id": "TEST_SOURCE",
  "url": "https://example.com",
  "sha256": "PLACEHOLDER"
}
```

Compute sha256 for fixture content and replace PLACEHOLDER with the hash of `tools/tests/fixtures/source_monitor/fixtures/TEST_SOURCE.txt`.

`tools/tests/fixtures/source_monitor/fixtures/TEST_SOURCE.txt`

```
Example content for source monitoring.
```

Create `tools/check_source_changes.py`:

```python
import argparse
import hashlib
import json
import sys
import urllib.request
from pathlib import Path


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fetch_bytes(url: str) -> bytes:
    with urllib.request.urlopen(url, timeout=20) as resp:
        return resp.read()


def load_sources(sources_dir: Path) -> list[dict]:
    items = []
    for path in sources_dir.rglob("*.meta.json"):
        try:
            items.append(json.loads(path.read_text(encoding="utf-8")))
        except Exception:
            continue
    return items


def resolve_fixture_bytes(fixture_dir: Path, source_id: str) -> bytes:
    path = fixture_dir / f"{source_id}.txt"
    if not path.exists():
        path = fixture_dir / f"{source_id}.bin"
    return path.read_bytes()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sources-dir", default="sources")
    parser.add_argument("--fixture-dir", default="")
    parser.add_argument("--output", default="")
    args = parser.parse_args()

    sources_dir = Path(args.sources_dir)
    fixture_dir = Path(args.fixture_dir) if args.fixture_dir else None

    changed = []
    for meta in load_sources(sources_dir):
        source_id = meta.get("source_id")
        url = meta.get("url")
        expected = str(meta.get("sha256") or "")
        if not source_id or not url or not expected:
            continue
        try:
            data = resolve_fixture_bytes(fixture_dir, source_id) if fixture_dir else fetch_bytes(url)
            actual = sha256_bytes(data)
            if actual.lower() != expected.lower():
                changed.append({"source_id": source_id, "url": url, "sha256": actual})
        except Exception as exc:
            print(f"[WARN] {source_id}: {exc}")

    report = {"changed": changed}
    output = json.dumps(report, indent=2)
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
    else:
        print(output)

    sys.exit(0)


if __name__ == "__main__":
    main()
```

**Step 4: Run test to verify it passes**

Run: `powershell -NoProfile -File tools/tests/source_monitor_tests.ps1`
Expected: PASS lines and exit code 0.

**Step 5: Commit**

```bash
git add tools/check_source_changes.py tools/tests/source_monitor_tests.ps1 tools/tests/fixtures/source_monitor
git commit -m "feat: add source monitoring script"
```
### Task 10: Add scheduled workflow to open issues

**Files:**
- Create: `.github/workflows/source-monitor.yml`

**Step 1: Write the workflow**

```yaml
name: source-monitor

on:
  schedule:
    - cron: "0 9 * * 1" # weekly Monday UTC
  workflow_dispatch:

permissions:
  contents: read
  issues: write

jobs:
  monitor:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Run source check
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          python tools/check_source_changes.py --output source-report.json
      - name: Upload report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: source-report
          path: source-report.json
```

**Step 2: Commit**

```bash
git add .github/workflows/source-monitor.yml
git commit -m "ci: add scheduled source monitor"
```

---

Notes:
- If any tests fail, follow @superpowers:systematic-debugging before changing implementation.
- Keep snapshots and generated artifacts out of git; they are published via Hugo static output.

Plan complete and saved to `docs/plans/2026-01-13-compliance-next-phase.md`. Two execution options:

1. Subagent-Driven (this session) - I dispatch fresh subagent per task, review between tasks, fast iteration
2. Parallel Session (separate) - Open new session with executing-plans, batch execution with checkpoints

Which approach?
