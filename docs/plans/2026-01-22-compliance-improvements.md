# Compliance Improvements Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Improve maintainability and performance by hardening UI ASCII hygiene, adding a build-time UI asset pipeline, modularizing the mapping rules, and adding scoped/skip-unchanged mapping builds.

**Architecture:** Split mapping evaluation into a thin engine plus rule functions in separate modules, keeping output JSON stable. Replace Tailwind CDN with a local build step that outputs static CSS and keeps JS in its own file for clearer ownership. Use @test-driven-development for each change and @systematic-debugging if a test fails unexpectedly.

**Tech Stack:** Python 3.x tools, PowerShell tests, Hugo static output, Tailwind CLI standalone binary, vanilla JS.

---

### Task 1: Enforce ASCII control hygiene in UI HTML

**Files:**
- Modify: `tools/tests/ui_compliance_tests.ps1`
- Modify: `ui/index.html`

**Step 1: Write the failing test**

Add a control-byte guard after the existing ASCII check:

```powershell
$bytes = [System.IO.File]::ReadAllBytes("ui/index.html")
$nonAsciiBytes = @($bytes | Where-Object { $_ -gt 127 })
Assert-True ($nonAsciiBytes.Count -eq 0) "ui/index.html contains only ASCII characters"

$allowedControls = @(9, 10, 13)
$badControlBytes = @(
  $bytes | Where-Object { (($_ -lt 32) -or ($_ -eq 127)) -and ($_ -notin $allowedControls) }
)
Assert-True ($badControlBytes.Count -eq 0) "ui/index.html has no ASCII control chars (except tab/lf/cr)"
```

**Step 2: Run test to verify it fails**

Run: `powershell -NoProfile -File tools/tests/ui_compliance_tests.ps1`  
Expected: FAIL with "ui/index.html has no ASCII control chars (except tab/lf/cr)"

**Step 3: Write minimal implementation**

Replace the NUL-containing regex line with ASCII escape characters:

```html
  if (/[\x00-\x1f\x7f]/.test(s)) return "#";
```

**Step 4: Run tests to verify it passes**

Run: `powershell -NoProfile -File tools/tests/ui_compliance_tests.ps1`  
Expected: PASS

**Step 5: Commit**

```bash
git add ui/index.html tools/tests/ui_compliance_tests.ps1
git commit -m "fix: enforce ascii control char guard in ui"
```

---

### Task 2: Extract UI JS into `ui/app.js`

**Files:**
- Create: `ui/app.js`
- Modify: `ui/index.html`
- Modify: `tools/tests/ui_compliance_tests.ps1`

**Step 1: Write the failing test**

Update the UI compliance test to load `ui/app.js` and assert JS-only checks there:

```powershell
$ui = Get-Content -Raw -Path "ui/index.html"
$ui = $ui.TrimStart([char]0xFEFF)
$uiJs = Get-Content -Raw -Path "ui/app.js"

Assert-True ($ui -like '*src="./app.js"*') "UI loads app.js"
Assert-True ($uiJs -like "*const DATA_URL*") "DATA_URL is computed dynamically"
Assert-True ($uiJs -like "*location.pathname*") "DATA_URL uses location.pathname"
Assert-True ($uiJs -like "*function escapeHtml*") "escapeHtml helper exists"
Assert-True ($uiJs -like "*function sanitizeUrl*") "sanitizeUrl helper exists"
Assert-True ($uiJs -like '*startsWith("//")*') "sanitizeUrl blocks protocol-relative URLs"
Assert-True ($uiJs -like "*file:*") "sanitizeUrl blocks file: scheme"
Assert-True ($uiJs -like "*javascript*") "sanitizeUrl blocks javascript: scheme"
Assert-True (-not ($uiJs -match '\$\{ev\.locator')) "openModal does not inject locator without escaping"
Assert-True (-not ($uiJs -match '\$\{ev\.excerpt')) "openModal does not inject excerpt without escaping"
Assert-True (-not ($uiJs -match '\$\{r\.text')) "renderReasons does not inject reason text without escaping"
Assert-True (-not ($uiJs -match '\$\{meta\.title')) "renderRequirements does not inject title without escaping"
```

**Step 2: Run test to verify it fails**

Run: `powershell -NoProfile -File tools/tests/ui_compliance_tests.ps1`  
Expected: FAIL with missing `ui/app.js` or missing script tag.

**Step 3: Write minimal implementation**

1) In `ui/index.html`, replace the inline `<script>...</script>` block that contains the app logic (starts with `const DATA_URL = ...` and ends with `init();`) with:

```html
  <script src="./app.js" defer></script>
```

2) Create `ui/app.js` by pasting the removed script block verbatim (no logic changes).

**Step 4: Run tests to verify it passes**

Run: `powershell -NoProfile -File tools/tests/ui_compliance_tests.ps1`  
Expected: PASS

**Step 5: Commit**

```bash
git add ui/index.html ui/app.js tools/tests/ui_compliance_tests.ps1
git commit -m "refactor: extract ui logic into app.js"
```

---

### Task 3: Replace Tailwind CDN with a local build step

**Files:**
- Create: `tools/build_ui_assets.py`
- Create: `tailwind.config.js`
- Create: `ui/tailwind.css`
- Create: `tools/tests/ui_assets_tests.ps1`
- Modify: `ui/index.html`
- Modify: `tools/tests/ui_compliance_tests.ps1`
- Modify: `.github/workflows/ui-compliance.yml`
- Modify: `.gitignore`

**Step 1: Write the failing test**

Add a new UI asset build test:

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

Write-Host "UI asset build checks..." -ForegroundColor Cyan
$proc = Start-Process -FilePath "py" -ArgumentList "tools/build_ui_assets.py" -Wait -PassThru -NoNewWindow
Assert-True ($proc.ExitCode -eq 0) "build_ui_assets.py runs successfully"

$cssPath = "ui/assets/tailwind.css"
Assert-True (Test-Path $cssPath) "tailwind.css is generated"
$css = Get-Content -Raw -Path $cssPath
Assert-True ($css.Length -gt 0) "tailwind.css is not empty"

if ($failed) {
  Write-Error "One or more checks failed."
  exit 1
}

Write-Host "All checks passed." -ForegroundColor Green
```

Update UI compliance checks to enforce local CSS and remove CDN:

```powershell
Assert-True ($ui -notlike "*cdn.tailwindcss.com*") "UI does not use Tailwind CDN"
Assert-True ($ui -like '*href="./assets/tailwind.css"*') "UI loads built Tailwind CSS"
```

**Step 2: Run test to verify it fails**

Run: `powershell -NoProfile -File tools/tests/ui_assets_tests.ps1`  
Expected: FAIL because `build_ui_assets.py` is missing.

**Step 3: Write minimal implementation**

Create `tools/build_ui_assets.py`:

```python
import os
import platform
import stat
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent.parent
TAILWIND_VERSION = "v3.4.17"
VENDOR_DIR = ROOT / "tools" / "vendor"
VENDOR_DIR.mkdir(parents=True, exist_ok=True)

def tailwind_asset_name() -> str:
    system = platform.system().lower()
    machine = platform.machine().lower()
    is_arm = machine in {"arm64", "aarch64"}
    if system == "windows":
        return "tailwindcss-windows-x64.exe"
    if system == "darwin":
        return "tailwindcss-macos-arm64" if is_arm else "tailwindcss-macos-x64"
    return "tailwindcss-linux-arm64" if is_arm else "tailwindcss-linux-x64"

def tailwind_binary_path() -> Path:
    name = "tailwindcss.exe" if platform.system().lower() == "windows" else "tailwindcss"
    return VENDOR_DIR / name

def ensure_tailwind() -> Path:
    binary = tailwind_binary_path()
    if binary.exists():
        return binary
    asset = tailwind_asset_name()
    url = f"https://github.com/tailwindlabs/tailwindcss/releases/download/{TAILWIND_VERSION}/{asset}"
    tmp = binary.with_suffix(".download")
    with urllib.request.urlopen(url) as response, tmp.open("wb") as handle:
        handle.write(response.read())
    tmp.chmod(tmp.stat().st_mode | stat.S_IEXEC)
    tmp.replace(binary)
    return binary

def main() -> int:
    input_css = ROOT / "ui" / "tailwind.css"
    output_css = ROOT / "ui" / "assets" / "tailwind.css"
    config = ROOT / "tailwind.config.js"
    if not input_css.exists():
        print("ERROR: missing ui/tailwind.css", file=sys.stderr)
        return 1
    if not config.exists():
        print("ERROR: missing tailwind.config.js", file=sys.stderr)
        return 1
    output_css.parent.mkdir(parents=True, exist_ok=True)
    binary = ensure_tailwind()
    cmd = [
        str(binary),
        "-c",
        str(config),
        "-i",
        str(input_css),
        "-o",
        str(output_css),
        "--minify",
    ]
    return subprocess.call(cmd)

if __name__ == "__main__":
    raise SystemExit(main())
```

Create `tailwind.config.js` (move the inline config values from `ui/index.html`):

```javascript
module.exports = {
  content: ["./ui/index.html", "./ui/app.js"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        "primary": "#1e3a5f",
        "primary-hover": "#152a45",
        "accent": "#c9a227",
        "accent-hover": "#b8921f",
        "background-light": "#faf8f5",
        "background-dark": "#0f1419",
        "surface-light": "#ffffff",
        "surface-dark": "#1a232e",
        "border-soft": "#e8e4df",
        "border-dark": "#2d3748",
        "success-green": "#059669",
        "warning-yellow": "#d97706",
        "error-red": "#dc2626",
        "unknown-gray": "#6b7280",
        "info-blue": "#0369a1",
        "text-primary": "#1a1a1a",
        "text-secondary": "#525252"
      },
      fontFamily: {
        "display": ["'DM Serif Display'", "Georgia", "serif"],
        "body": ["'Plus Jakarta Sans'", "system-ui", "sans-serif"]
      },
      borderRadius: {
        "DEFAULT": "0.5rem",
        "lg": "1rem",
        "xl": "1.5rem"
      }
    }
  }
};
```

Create `ui/tailwind.css`:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

Update `ui/index.html`:
- Remove the Tailwind CDN `<script src="https://cdn.tailwindcss.com?...">`.
- Remove the `<script id="tailwind-config">...</script>` block.
- Add a stylesheet link in the `<head>`:

```html
  <link rel="stylesheet" href="./assets/tailwind.css"/>
```

Update `.gitignore` to avoid committing the generated CSS:

```
ui/assets/tailwind.css
```

Add the new test to CI by inserting a step in `.github/workflows/ui-compliance.yml` (before UI compliance tests):

```yaml
      - name: Build UI assets
        run: powershell -NoProfile -File tools/tests/ui_assets_tests.ps1
```

**Step 4: Run tests to verify it passes**

Run:
`powershell -NoProfile -Command "& { ./tools/tests/ui_assets_tests.ps1; ./tools/tests/ui_compliance_tests.ps1 }"`  
Expected: PASS

**Step 5: Commit**

```bash
git add tools/build_ui_assets.py tailwind.config.js ui/tailwind.css ui/index.html tools/tests/ui_assets_tests.ps1 tools/tests/ui_compliance_tests.ps1 .github/workflows/ui-compliance.yml .gitignore
git commit -m "feat: add local tailwind build pipeline for ui"
```

---

### Task 4: Modularize mapping rules into a dedicated engine

**Files:**
- Create: `tools/mapping_engine.py`
- Create: `tools/mapping_rules.py`
- Create: `tools/tests/fixtures/mapping_engine_api_test.py`
- Create: `tools/tests/mapping_engine_api_tests.ps1`
- Modify: `tools/build_mappings.py`

**Step 1: Write the failing test**

Create `tools/tests/fixtures/mapping_engine_api_test.py`:

```python
from tools.mapping_engine import evaluate

def main() -> int:
    visa = {
        "id": "ES_DNV_TEST_2026",
        "country": "Spain",
        "requirements": [
            {
                "key": "insurance.no_deductible",
                "value": True,
                "evidence": {"source_id": "TEST", "locator": "L1", "excerpt": "E", "url": "https://example.com"}
            }
        ],
    }
    product = {
        "id": "GENERIC_TEST_2026",
        "specs": {"deductible": {"amount": 100}}
    }
    result = evaluate(visa, product)
    if result["status"] != "RED":
        raise SystemExit("Expected RED for deductible")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
```

Create `tools/tests/mapping_engine_api_tests.ps1`:

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

Write-Host "Mapping engine API tests..." -ForegroundColor Cyan
$proc = Start-Process -FilePath "py" -ArgumentList "tools/tests/fixtures/mapping_engine_api_test.py" -Wait -PassThru -NoNewWindow
Assert-True ($proc.ExitCode -eq 0) "mapping_engine.evaluate returns expected status"

if ($failed) {
  Write-Error "One or more checks failed."
  exit 1
}

Write-Host "All checks passed." -ForegroundColor Green
```

**Step 2: Run test to verify it fails**

Run: `powershell -NoProfile -File tools/tests/mapping_engine_api_tests.ps1`  
Expected: FAIL because `tools/mapping_engine.py` does not exist yet.

**Step 3: Write minimal implementation**

Create `tools/mapping_rules.py`:

```python
def get_req(visa, key):
    for req in visa["requirements"]:
        if req["key"] == key:
            return req
    return None

def product_spec(product, path):
    cur = product["specs"]
    for part in path.split("."):
        if cur is None or part not in cur:
            return None
        cur = cur[part]
    return cur

def rule_insurance_mandatory(visa, product):
    req = get_req(visa, "insurance.mandatory")
    if req and req["value"] is False:
        return {
            "visa_id": visa["id"],
            "product_id": product["id"],
            "status": "NOT_REQUIRED",
            "reasons": [
                {
                    "text": "Visa does not require insurance",
                    "evidence": req["evidence"]
                }
            ],
            "missing": []
        }
    return None

def rule_travel_insurance_accepted(visa, product, ctx):
    req = get_req(visa, "insurance.travel_insurance_accepted")
    if req and req["value"] is False:
        ptype = product_spec(product, "type")
        if ptype is None:
            ctx["status"] = "UNKNOWN"
            ctx["missing"].append("specs.type")
        elif "travel" in ptype:
            ctx["status"] = "RED"
            ctx["reasons"].append({
                "text": "Travel insurance is not accepted for this visa",
                "evidence": req["evidence"]
            })

def rule_authorized_in_spain(visa, product, ctx):
    req = get_req(visa, "insurance.authorized_in_spain")
    if req and req["value"] is True:
        country = visa.get("id", "").upper()[:2]
        if country == "ES":
            jf = product_spec(product, f"jurisdiction_facts.{country}.authorized")
            if jf is None:
                if ctx["status"] == "GREEN":
                    ctx["status"] = "UNKNOWN"
                ctx["missing"].append(f"specs.jurisdiction_facts.{country}.authorized")
            elif jf is False:
                ctx["status"] = "RED"
                ctx["reasons"].append({
                    "text": f"Insurer not authorized to operate in {visa.get('country', 'jurisdiction')}",
                    "evidence": req["evidence"]
                })

def rule_no_deductible(visa, product, ctx):
    req = get_req(visa, "insurance.no_deductible")
    if req and req["value"] is True:
        ded = product_spec(product, "deductible.amount")
        if ded is None:
            ctx["status"] = "UNKNOWN"
            ctx["missing"].append("specs.deductible.amount")
        elif ded > 0:
            ctx["status"] = "RED"
            ctx["reasons"].append({
                "text": f"Visa requires zero deductible but product has {ded}",
                "evidence": req["evidence"]
            })

def rule_comprehensive(visa, product, ctx):
    req = get_req(visa, "insurance.comprehensive")
    if req and req["value"] is True:
        comprehensive = product_spec(product, "comprehensive")
        if comprehensive is None:
            if ctx["status"] == "GREEN":
                ctx["status"] = "UNKNOWN"
            ctx["missing"].append("specs.comprehensive")
        elif comprehensive is False:
            ctx["status"] = "RED"
            ctx["reasons"].append({
                "text": "Comprehensive coverage required",
                "evidence": req["evidence"]
            })

def rule_public_health_risks(visa, product, ctx):
    req = get_req(visa, "insurance.covers_public_health_system_risks")
    if req and req["value"] is True:
        covers = product_spec(product, "covers_public_health_system_risks")
        if covers is None:
            if ctx["status"] == "GREEN":
                ctx["status"] = "UNKNOWN"
            ctx["missing"].append("specs.covers_public_health_system_risks")
        elif covers is False:
            ctx["status"] = "RED"
            ctx["reasons"].append({
                "text": "Visa requires coverage of public health system risks",
                "evidence": req["evidence"]
            })

def rule_unlimited_coverage(visa, product, ctx):
    req = get_req(visa, "insurance.unlimited_coverage")
    if req and req["value"] is True:
        limit = product_spec(product, "overall_limit")
        unlimited = product_spec(product, "unlimited")
        if unlimited is True:
            return
        if limit is None and unlimited is None:
            if ctx["status"] == "GREEN":
                ctx["status"] = "UNKNOWN"
            ctx["missing"].append("specs.overall_limit or specs.unlimited")
        elif unlimited is False or (limit is not None and limit < 10000000):
            ctx["status"] = "RED"
            ctx["reasons"].append({
                "text": f"Unlimited coverage required, product has limit of {limit}",
                "evidence": req["evidence"]
            })

def rule_no_copayment(visa, product, ctx):
    req = get_req(visa, "insurance.no_copayment")
    if req and req["value"] is True:
        copay = product_spec(product, "copay")
        if copay is None:
            if ctx["status"] == "GREEN":
                ctx["status"] = "UNKNOWN"
            ctx["missing"].append("specs.copay")
        elif copay is True:
            ctx["status"] = "RED"
            ctx["reasons"].append({
                "text": "No co-payments required, product has co-payments",
                "evidence": req["evidence"]
            })

def rule_no_moratorium(visa, product, ctx):
    req = get_req(visa, "insurance.no_moratorium")
    if req and req["value"] is True:
        moratorium = product_spec(product, "moratorium_days")
        if moratorium is None:
            if ctx["status"] == "GREEN":
                ctx["status"] = "UNKNOWN"
            ctx["missing"].append("specs.moratorium_days")
        elif moratorium > 0:
            ctx["status"] = "RED"
            ctx["reasons"].append({
                "text": f"No moratorium required, product has {moratorium} day waiting period",
                "evidence": req["evidence"]
            })

def rule_min_coverage(visa, product, ctx):
    req = get_req(visa, "insurance.min_coverage")
    if req:
        limit = product_spec(product, "overall_limit")
        if limit is None:
            ctx["status"] = "UNKNOWN"
            ctx["missing"].append("specs.overall_limit")
        elif limit < req["value"]:
            ctx["status"] = "RED"
            ctx["reasons"].append({
                "text": f"Minimum coverage {req['value']} required, product has {limit}",
                "evidence": req["evidence"]
            })

def rule_monthly_payments_accepted(visa, product, ctx):
    req = get_req(visa, "insurance.monthly_payments_accepted")
    if req and req["value"] is False:
        cadence = product_spec(product, "payment_cadence")
        if cadence is None:
            ctx["status"] = "UNKNOWN"
            ctx["missing"].append("specs.payment_cadence")
        elif cadence in ["monthly", "every_4_weeks"]:
            ctx["status"] = "RED"
            ctx["reasons"].append({
                "text": "Monthly payments not accepted by visa authority",
                "evidence": req["evidence"]
            })

def rule_must_cover_full_period(visa, product, ctx):
    req = get_req(visa, "insurance.must_cover_full_period")
    if req and req["value"] is True:
        cadence = product_spec(product, "payment_cadence")
        if cadence in ["monthly", "every_4_weeks"]:
            if ctx["status"] == "GREEN":
                ctx["status"] = "YELLOW"
            ctx["reasons"].append({
                "text": "Visa requires coverage for full legal stay, monthly subscriptions can be cancelled",
                "evidence": req["evidence"]
            })

RULES = [
    rule_travel_insurance_accepted,
    rule_authorized_in_spain,
    rule_no_deductible,
    rule_comprehensive,
    rule_public_health_risks,
    rule_unlimited_coverage,
    rule_no_copayment,
    rule_no_moratorium,
    rule_min_coverage,
    rule_monthly_payments_accepted,
    rule_must_cover_full_period,
]
```

Create `tools/mapping_engine.py`:

```python
from dataclasses import dataclass, field

from tools.mapping_rules import RULES, rule_insurance_mandatory

@dataclass
class EvaluationContext:
    status: str = "GREEN"
    reasons: list = field(default_factory=list)
    missing: list = field(default_factory=list)

    def as_dict(self):
        return {
            "status": self.status,
            "reasons": self.reasons,
            "missing": self.missing,
        }

def evaluate(visa, product):
    not_required = rule_insurance_mandatory(visa, product)
    if not_required:
        return not_required

    ctx = EvaluationContext()
    ctx_map = {
        "status": ctx.status,
        "reasons": ctx.reasons,
        "missing": ctx.missing,
    }

    for rule in RULES:
        rule(visa, product, ctx_map)

    ctx.status = ctx_map["status"]
    ctx.reasons = ctx_map["reasons"]
    ctx.missing = ctx_map["missing"]

    if ctx.status == "GREEN" and ctx.missing:
        ctx.status = "UNKNOWN"

    return {
        "visa_id": visa["id"],
        "product_id": product["id"],
        "status": ctx.status,
        "reasons": ctx.reasons,
        "missing": ctx.missing,
    }
```

Update `tools/build_mappings.py` to use the new engine:

```python
import json
from pathlib import Path

from tools.mapping_engine import evaluate

ROOT = Path(__file__).parent.parent
VISAS = ROOT / "data" / "visas"
PRODUCTS = ROOT / "data" / "products"
MAPPINGS = ROOT / "data" / "mappings"

MAPPINGS.mkdir(exist_ok=True)

def load_all(folder):
    files = []
    for p in folder.rglob("*.json"):
        files.append(json.loads(p.read_text(encoding="utf-8")))
    return files

visas = load_all(VISAS)
products = load_all(PRODUCTS)

for visa in visas:
    for product in products:
        result = evaluate(visa, product)
        out = MAPPINGS / f"{visa['id']}__{product['id']}.json"
        out.write_text(json.dumps(result, indent=2), encoding="utf-8")
        print("Built", out)
```

**Step 4: Run tests to verify it passes**

Run: `powershell -NoProfile -File tools/tests/mapping_engine_api_tests.ps1`  
Expected: PASS

**Step 5: Commit**

```bash
git add tools/mapping_engine.py tools/mapping_rules.py tools/build_mappings.py tools/tests/fixtures/mapping_engine_api_test.py tools/tests/mapping_engine_api_tests.ps1
git commit -m "refactor: split mapping engine and rules"
```

---

### Task 5: Add scoped mapping builds and skip-unchanged writes

**Files:**
- Modify: `tools/build_mappings.py`
- Modify: `tools/tests/mapping_engine_tests.ps1`

**Step 1: Write the failing test**

Extend `tools/tests/mapping_engine_tests.ps1` with filtered build and skip-unchanged checks:

```powershell
$root = Resolve-Path "."
$tmpDir = Join-Path $root "tools/tests/fixtures/tmp_mappings"
if (Test-Path $tmpDir) { Remove-Item -Recurse -Force $tmpDir }
New-Item -ItemType Directory -Path $tmpDir | Out-Null

$proc = Start-Process -FilePath "py" -ArgumentList @(
  "tools/build_mappings.py",
  "--visa-id", "ES_DNV_BLS_LONDON_2026",
  "--product-id", "SAFETYWING_NOMAD_2026",
  "--output-dir", $tmpDir
) -Wait -PassThru -NoNewWindow
Assert-True ($proc.ExitCode -eq 0) "build_mappings supports filtered build"

$mappingPath = Join-Path $tmpDir "ES_DNV_BLS_LONDON_2026__SAFETYWING_NOMAD_2026.json"
Assert-True (Test-Path $mappingPath) "Filtered build writes expected mapping"

$firstWrite = (Get-Item $mappingPath).LastWriteTimeUtc
Start-Sleep -Seconds 1

$proc2 = Start-Process -FilePath "py" -ArgumentList @(
  "tools/build_mappings.py",
  "--visa-id", "ES_DNV_BLS_LONDON_2026",
  "--product-id", "SAFETYWING_NOMAD_2026",
  "--output-dir", $tmpDir,
  "--skip-unchanged"
) -Wait -PassThru -NoNewWindow
Assert-True ($proc2.ExitCode -eq 0) "skip-unchanged run succeeds"

$secondWrite = (Get-Item $mappingPath).LastWriteTimeUtc
Assert-True ($secondWrite -eq $firstWrite) "skip-unchanged avoids rewriting identical file"
```

**Step 2: Run test to verify it fails**

Run: `powershell -NoProfile -File tools/tests/mapping_engine_tests.ps1`  
Expected: FAIL with unrecognized arguments.

**Step 3: Write minimal implementation**

Update `tools/build_mappings.py` to accept CLI arguments and skip unchanged writes:

```python
import argparse
import json
from pathlib import Path

from tools.mapping_engine import evaluate

ROOT = Path(__file__).parent.parent
VISAS = ROOT / "data" / "visas"
PRODUCTS = ROOT / "data" / "products"

def load_all(folder):
    files = []
    for p in folder.rglob("*.json"):
        files.append(json.loads(p.read_text(encoding="utf-8")))
    return files

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--visa-id")
    parser.add_argument("--product-id")
    parser.add_argument("--output-dir", default=str(ROOT / "data" / "mappings"))
    parser.add_argument("--skip-unchanged", action="store_true")
    return parser.parse_args()

def main():
    args = parse_args()
    mappings_dir = Path(args.output_dir)
    mappings_dir.mkdir(parents=True, exist_ok=True)

    visas = load_all(VISAS)
    products = load_all(PRODUCTS)

    if args.visa_id:
        visas = [v for v in visas if v["id"] == args.visa_id]
    if args.product_id:
        products = [p for p in products if p["id"] == args.product_id]
    if not visas:
        raise SystemExit("No visas matched filters.")
    if not products:
        raise SystemExit("No products matched filters.")

    for visa in visas:
        for product in products:
            result = evaluate(visa, product)
            payload = json.dumps(result, indent=2)
            out = mappings_dir / f"{visa['id']}__{product['id']}.json"
            if args.skip_unchanged and out.exists():
                if out.read_text(encoding="utf-8") == payload:
                    print("Skipped", out)
                    continue
            out.write_text(payload, encoding="utf-8")
            print("Built", out)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
```

**Step 4: Run tests to verify it passes**

Run: `powershell -NoProfile -File tools/tests/mapping_engine_tests.ps1`  
Expected: PASS

**Step 5: Commit**

```bash
git add tools/build_mappings.py tools/tests/mapping_engine_tests.ps1
git commit -m "feat: add scoped mapping builds and skip-unchanged"
```

---

### Task 6: Document new UI and mapping build commands

**Files:**
- Modify: `CONTRIBUTING.md`

**Step 1: Write the failing test**

Add a doc lint note to the quick start list (no automated test needed). In this plan, treat "missing doc update" as failing by inspection.

**Step 2: Run test to verify it fails**

Run: `rg -n "build_ui_assets.py" CONTRIBUTING.md`  
Expected: No matches.

**Step 3: Write minimal implementation**

Add the new build command and test to the Quick start and Testing sections:

```markdown
- Build UI assets: `py tools/build_ui_assets.py`
```

And under "Testing":

```markdown
py tools/build_ui_assets.py
powershell -NoProfile -File tools/tests/ui_assets_tests.ps1
```

**Step 4: Run tests to verify it passes**

Run: `rg -n "build_ui_assets.py" CONTRIBUTING.md`  
Expected: Lines found.

**Step 5: Commit**

```bash
git add CONTRIBUTING.md
git commit -m "docs: document ui asset build step"
```
