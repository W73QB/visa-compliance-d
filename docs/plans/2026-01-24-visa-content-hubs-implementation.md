# Visa Content Hubs Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Generate SEO-friendly, evidence-based content hubs for all visa routes under `content/visas/` without introducing new claims.

**Architecture:** Use a data-driven build script to render hub markdown from `data/visas/**/visa_facts.json` and `sources/*.meta.json`. Add PowerShell tests that assert hubs exist and include evidence links. Keep hub overview pages summary-only; route pages contain evidence details.

**Tech Stack:** Python, Hugo content, PowerShell tests (`tools/tests/*.ps1`), JSON data.

**Critical Requirement:** Generated content MUST include lint-required blocks per `tools/lint_content.py`:
- "what the authority requires"
- "how we evaluate"
- "check in the engine"
- "disclaimer"
- "affiliate disclosure"
- `snapshot=` in deep links

---

## Prerequisites

- All tests passing
- Theme submodule initialized
- 6 visa_facts.json files exist in `data/visas/`

---

## Task 1: Create hub generator script with tests

**Files:**
- Create: `tools/build_content_hubs.py`
- Create: `tools/tests/visa_hubs_tests.ps1`

### Step 1: Write the failing test

Create `tools/tests/visa_hubs_tests.ps1`:

```powershell
$ErrorActionPreference = "Stop"
$failed = $false

function Assert-True {
  param([Parameter(Mandatory=$true)][bool]$Condition, [Parameter(Mandatory=$true)][string]$Message)
  if (-not $Condition) { Write-Host "FAIL: $Message" -ForegroundColor Red; $script:failed = $true }
  else { Write-Host "PASS: $Message" -ForegroundColor Green }
}

$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)

# Phase 1: Script exists
$scriptPath = Join-Path $root "tools/build_content_hubs.py"
Assert-True (Test-Path $scriptPath) "build_content_hubs.py exists"

if ($failed) { Write-Error "Visa hub checks failed."; exit 1 }
Write-Host "All checks passed." -ForegroundColor Green
```

### Step 2: Run test to verify it fails

```bash
export PATH="$PWD/.bin:$PATH" && pwsh -NoProfile -File tools/tests/visa_hubs_tests.ps1
```

Expected: FAIL (script does not exist)

### Step 3: Write minimal implementation

Create `tools/build_content_hubs.py`:

```python
#!/usr/bin/env python3
"""Generate visa content hubs from visa_facts.json data."""

from pathlib import Path
import json
import re
import os
from datetime import datetime, timezone

ROOT = Path(__file__).parent.parent
VISAS = ROOT / "data" / "visas"
SOURCES = ROOT / "sources"
OUT = ROOT / "content" / "visas"


def slugify(value: str) -> str:
    """Convert string to URL-safe slug."""
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value or "unknown"


def load_sources() -> dict:
    """Load all source metadata from sources/*.meta.json."""
    sources = {}
    for p in SOURCES.rglob("*.meta.json"):
        try:
            meta = json.loads(p.read_text(encoding="utf-8"))
            source_id = meta.get("source_id")
            if source_id:
                sources[source_id] = meta
        except (json.JSONDecodeError, IOError):
            continue
    return sources


def get_lint_required_blocks(visa_id: str, visa_name: str, snapshot_id: str) -> str:
    """Return the required content blocks for lint_content.py compliance."""
    return f"""
## What the authority requires

See the requirements table above. All requirements are extracted directly from official sources with evidence excerpts.

## How we evaluate

We compare these official requirements against insurance product specifications using our automated rule engine. Each requirement is matched to a product fact with evidence.

## Check in the engine

Try the compliance checker: [Open Checker](/ui/?visa={visa_id}&snapshot={snapshot_id})

## Disclaimer

This is not legal advice. VisaFact provides evidence-based compliance checking only. Final visa decisions are made by government authorities. A GREEN result does not guarantee visa approval.

## Affiliate disclosure

If affiliate links appear, they are shown only after compliance results and do not influence the compliance evaluation in any way.
"""


def get_root_lint_blocks(snapshot_id: str) -> str:
    """Return lint-required blocks for root index (no specific visa)."""
    return f"""
## What the authority requires

This page lists all visa types with insurance requirements. Select a visa to see specific requirements.

## How we evaluate

We compare official visa requirements against insurance product specifications using our automated rule engine.

## Check in the engine

Try the compliance checker: [Open Checker](/ui/?snapshot={snapshot_id})

## Disclaimer

This is not legal advice. VisaFact provides evidence-based compliance checking only. Final visa decisions are made by government authorities. A GREEN result does not guarantee visa approval.

## Affiliate disclosure

If affiliate links appear, they are shown only after compliance results and do not influence the compliance evaluation in any way.
"""


def render_overview(country_slug: str, visa_slug: str, visa_name: str,
                    country_name: str, routes: list, snapshot_id: str) -> str:
    """Render the overview _index.md for a visa type."""
    lines = [
        "---",
        f'title: "{country_name} {visa_name}"',
        f'visa_group: "{country_slug}-{visa_slug}"',
        f'description: "Insurance requirements for {country_name} {visa_name} - evidence-based compliance checker"',
        "---",
        "",
        f"# {country_name} {visa_name} Requirements",
        "",
        "All requirements below are derived from official sources. Missing evidence means UNKNOWN.",
        "",
        "## Routes",
        "",
        "| Authority | Route | Last Verified | Details |",
        "| --- | --- | --- | --- |",
    ]

    for route in routes:
        lines.append(
            f"| {route['authority']} | {route['route']} | {route['last_verified']} | "
            f"[View requirements]({route['link']}) |"
        )

    # Add required lint blocks
    first_visa_id = routes[0]["visa_id"] if routes else f"{country_slug.upper()}_{visa_slug.upper()}"
    lines.append(get_lint_required_blocks(first_visa_id, visa_name, snapshot_id))

    lines.append("")
    lines.append('{{< vf-cta href="/ui/" label="Open Compliance Checker" >}}')
    lines.append("")

    return "\n".join(lines)

def render_root_index(groups: dict, snapshot_id: str) -> str:
    """Render the root visas index page."""
    lines = [
        "---",
        'title: "Visa Requirements"',
        'description: "Evidence-based visa insurance requirements by country and visa type"',
        "---",
        "",
        "# Visa Requirements by Country",
        "",
        "Browse requirements by country and visa type. All requirements are sourced from official evidence.",
        "",
        "## Countries",
        "",
    ]
    for (country_slug, visa_slug), routes in sorted(groups.items()):
        country_name = routes[0]["country"]
        visa_name = routes[0]["visa_name"]
        lines.append(f"- [{country_name} {visa_name}](/visas/{country_slug}/{visa_slug}/)")

    # Add required lint blocks (no specific visa for root index)
    lines.append(get_root_lint_blocks(snapshot_id))

    lines.append("")
    lines.append('{{< vf-cta href="/ui/" label="Open Compliance Checker" >}}')
    lines.append("")
    return "\n".join(lines)


def render_detail(visa: dict, sources: dict, snapshot_id: str) -> None:
    """Render a detail page for a specific visa route."""
    country_slug = slugify(visa["country"])
    visa_slug = slugify(visa["visa_name"])
    authority_slug = slugify(visa["route"])
    visa_id = visa["id"]

    # Get source IDs from visa sources array
    source_ids = [s["source_id"] for s in visa.get("sources", [])]

    lines = [
        "---",
        f'title: "{visa["country"]} {visa["visa_name"]} - {visa["route"]}"',
        f'visa_id: "{visa_id}"',
        f'last_verified: "{visa.get("last_verified", "")}"',
        f'source_ids: {json.dumps(source_ids)}',
        f'description: "Official insurance requirements for {visa["country"]} {visa["visa_name"]} via {visa["route"]}"',
        "---",
        "",
        f"# {visa['country']} {visa['visa_name']}",
        "",
        f"**Route:** {visa['route']}  ",
        f"**Authority:** {visa.get('authority', visa['route'])}  ",
        f"**Last Verified:** {visa.get('last_verified', 'Unknown')}",
        "",
        "## Requirements",
        "",
        "| Requirement | Operator | Value | Evidence |",
        "| --- | --- | --- | --- |",
    ]

    for req in visa.get("requirements", []):
        key = req.get("key", "")
        op = req.get("op", "")
        value = req.get("value", "")

        # Format value for display
        if isinstance(value, bool):
            value_str = "Yes" if value else "No"
        else:
            value_str = str(value)

        # Build evidence string
        evidence_items = []
        for ev in req.get("evidence", []):
            sid = ev.get("source_id", "")
            locator = ev.get("locator", "")
            excerpt = ev.get("excerpt", "")
            excerpt = excerpt.replace("|", "\\|").replace("\n", " ")

            # Try to get local path from sources metadata
            meta = sources.get(sid, {})
            local_path = meta.get("local_path", "")

            if local_path:
                evidence_items.append(f'*{locator}*: "{excerpt[:80]}..." ([source](/{local_path}))')
            else:
                evidence_items.append(f'*{locator}*: "{excerpt[:80]}..." (source_id: {sid})')

        evidence = " ".join(evidence_items) if evidence_items else "*No evidence recorded*"
        lines.append(f"| `{key}` | `{op}` | {value_str} | {evidence} |")

    # Add source documents section
    lines.append("")
    lines.append("## Source Documents")
    lines.append("")

    for src in visa.get("sources", []):
        sid = src.get("source_id", "")
        url = src.get("url", "")
        local_path = src.get("local_path", "")
        retrieved = src.get("retrieved_at", "")[:10] if src.get("retrieved_at") else ""

        if local_path:
            lines.append(f"- **{sid}**: [Local copy](/{local_path}) | [Original]({url}) | Retrieved: {retrieved}")
        else:
            lines.append(f"- **{sid}**: [Original]({url}) | Retrieved: {retrieved}")

    # Add required lint blocks
    lines.append(get_lint_required_blocks(visa_id, visa["visa_name"], snapshot_id))

    lines.append("")
    lines.append('{{< vf-cta href="/ui/" label="Open Compliance Checker" >}}')
    lines.append("")

    # Write file
    out_dir = OUT / country_slug / visa_slug / authority_slug
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "index.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Generated: {out_dir / 'index.md'}")


def main():
    """Main entry point."""
    sources = load_sources()
    snapshot_id = os.environ.get("SNAPSHOT_ID") or datetime.now(timezone.utc).date().isoformat()
    visas = []

    for p in VISAS.rglob("visa_facts.json"):
        try:
            visas.append(json.loads(p.read_text(encoding="utf-8")))
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Failed to load {p}: {e}")
            continue

    if not visas:
        print("No visa_facts.json files found.")
        return

    # Group visas by country+visa_name for overview pages
    grouped = {}
    for visa in visas:
        country_slug = slugify(visa["country"])
        visa_slug = slugify(visa["visa_name"])
        authority_slug = slugify(visa["route"])
        key = (country_slug, visa_slug)

        grouped.setdefault(key, []).append({
            "authority": visa.get("authority", visa["route"]),
            "route": visa.get("route", ""),
            "last_verified": visa.get("last_verified", ""),
            "link": f"/visas/{country_slug}/{visa_slug}/{authority_slug}/",
            "country": visa["country"],
            "visa_name": visa["visa_name"],
            "visa_id": visa["id"],
        })

        # Render detail page
        render_detail(visa, sources, snapshot_id)

    # Render overview pages
    for (country_slug, visa_slug), routes in grouped.items():
        country_name = routes[0]["country"]
        visa_name = routes[0]["visa_name"]
        out_dir = OUT / country_slug / visa_slug
        out_dir.mkdir(parents=True, exist_ok=True)

        content = render_overview(country_slug, visa_slug, visa_name, country_name, routes, snapshot_id)
        (out_dir / "_index.md").write_text(content, encoding="utf-8")
        print(f"Generated: {out_dir / '_index.md'}")

    # Render root visas index
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "_index.md").write_text(render_root_index(grouped, snapshot_id), encoding="utf-8")
    print(f"Generated: {OUT / '_index.md'}")

    print(f"\nGenerated {len(visas)} detail pages and {len(grouped)} overview pages.")


if __name__ == "__main__":
    main()
```

### Step 4: Run test to verify it passes

```bash
export PATH="$PWD/.bin:$PATH" && pwsh -NoProfile -File tools/tests/visa_hubs_tests.ps1
```

Expected: PASS

### Step 5: Commit

```bash
git add tools/build_content_hubs.py tools/tests/visa_hubs_tests.ps1
git commit -m "feat: add visa content hub generator script"
```

---

## Task 2: Generate content hubs and verify

**Files:**
- Modify: `tools/tests/visa_hubs_tests.ps1`
- Create: `content/visas/**/*.md` (generated)

### Step 1: Extend the test

Update `tools/tests/visa_hubs_tests.ps1` to run generator and verify content:

```powershell
$ErrorActionPreference = "Stop"
$failed = $false

function Assert-True {
  param([Parameter(Mandatory=$true)][bool]$Condition, [Parameter(Mandatory=$true)][string]$Message)
  if (-not $Condition) { Write-Host "FAIL: $Message" -ForegroundColor Red; $script:failed = $true }
  else { Write-Host "PASS: $Message" -ForegroundColor Green }
}

$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)

# Phase 1: Script exists
$scriptPath = Join-Path $root "tools/build_content_hubs.py"
Assert-True (Test-Path $scriptPath) "build_content_hubs.py exists"

# Phase 2: Verify generated content
$visaFacts = Get-ChildItem -Path (Join-Path $root "data/visas") -Recurse -Filter "visa_facts.json"
Assert-True ($visaFacts.Count -gt 0) "Found visa_facts.json files"

$rootIndex = Join-Path $root "content/visas/_index.md"
Assert-True (Test-Path $rootIndex) "Root visas index exists"

foreach ($file in $visaFacts) {
  $json = Get-Content -Raw -Path $file.FullName | ConvertFrom-Json
  $country = ($json.country.ToLower() -replace "[^a-z0-9]+", "-").Trim("-")
  $visa = ($json.visa_name.ToLower() -replace "[^a-z0-9]+", "-").Trim("-")
  $authority = ($json.route.ToLower() -replace "[^a-z0-9]+", "-").Trim("-")

  $overview = Join-Path $root ("content/visas/{0}/{1}/_index.md" -f $country, $visa)
  $detail = Join-Path $root ("content/visas/{0}/{1}/{2}/index.md" -f $country, $visa, $authority)

  Assert-True (Test-Path $overview) "Overview exists for $($json.id)"
  Assert-True (Test-Path $detail) "Detail exists for $($json.id)"

  if (Test-Path $detail) {
    $md = Get-Content -Raw -Path $detail

    # Check required sections
    Assert-True ($md -match "## Requirements") "Detail has Requirements section for $($json.id)"
    Assert-True ($md -match "## Source Documents") "Detail has Source Documents section for $($json.id)"

    # Check lint-required blocks
    Assert-True ($md -match "## What the authority requires") "Detail has 'What the authority requires' for $($json.id)"
    Assert-True ($md -match "## How we evaluate") "Detail has 'How we evaluate' for $($json.id)"
    Assert-True ($md -match "## Check in the engine") "Detail has 'Check in the engine' for $($json.id)"
    Assert-True ($md -match "## Disclaimer") "Detail has 'Disclaimer' for $($json.id)"
    Assert-True ($md -match "## Affiliate disclosure") "Detail has 'Affiliate disclosure' for $($json.id)"
    Assert-True ($md -match "snapshot=") "Detail has snapshot= in deep link for $($json.id)"
  }
}

# Phase 3: Verify lint passes
$lintProc = Start-Process -FilePath "py" -ArgumentList "tools/lint_content.py" -WorkingDirectory $root -Wait -PassThru
Assert-True ($lintProc.ExitCode -eq 0) "lint_content.py passes for all content including generated hubs"

if ($failed) { Write-Error "Visa hub checks failed."; exit 1 }
Write-Host "All checks passed." -ForegroundColor Green
```

### Step 2: Run test to verify it fails

```bash
export PATH="$PWD/.bin:$PATH" && pwsh -NoProfile -File tools/tests/visa_hubs_tests.ps1
```

Expected: FAIL (content/visas missing and lint fails)

### Step 3: Run the generator

```bash
py tools/build_content_hubs.py
```

### Step 4: Run test to verify it passes

```bash
export PATH="$PWD/.bin:$PATH" && pwsh -NoProfile -File tools/tests/visa_hubs_tests.ps1
```

Expected: PASS (all content generated with lint-compliant blocks)

### Step 5: Verify Hugo builds

```bash
hugo --minify
```

Expected: No errors, visa pages appear in public/visas/

### Step 6: Commit

```bash
git add content/visas tools/tests/visa_hubs_tests.ps1
git commit -m "feat: generate visa content hubs with lint-compliant blocks"
```

---

## Task 3: Add to CI workflow

**Files:**
- Modify: `.github/workflows/pages.yml`
- Modify: `tools/tests/visa_hubs_tests.ps1`

### Step 1: Extend test to check CI

Add to `tools/tests/visa_hubs_tests.ps1`:

```powershell
# Phase 5: Verify CI includes hub generation
$pagesYml = Get-Content -Raw -Path (Join-Path $root ".github/workflows/pages.yml")
Assert-True ($pagesYml -match "build_content_hubs.py") "CI runs build_content_hubs.py"
```

### Step 2: Run test to verify it fails

```bash
export PATH="$PWD/.bin:$PATH" && pwsh -NoProfile -File tools/tests/visa_hubs_tests.ps1
```

Expected: FAIL (CI not updated yet)

### Step 3: Update CI workflow

Insert into `.github/workflows/pages.yml` after `python tools/validate.py` and before `python tools/build_mappings.py`:

```yaml
      - name: Build content hubs
        run: python tools/build_content_hubs.py
```

Full context:
```yaml
      - name: Validate + build mappings + build index + snapshot + sync static
        run: |
          SNAPSHOT_ID=$(date -u +%F)
          export SNAPSHOT_ID
          python tools/validate.py
          python tools/build_content_hubs.py
          python tools/build_mappings.py
          python tools/build_index.py
          python tools/build_snapshot.py
          python tools/sync_hugo_static.py
```

### Step 4: Run test to verify it passes

```bash
export PATH="$PWD/.bin:$PATH" && pwsh -NoProfile -File tools/tests/visa_hubs_tests.ps1
```

Expected: PASS

### Step 5: Commit

```bash
git add .github/workflows/pages.yml tools/tests/visa_hubs_tests.ps1
git commit -m "ci: add visa content hub generation to pages workflow"
```

---

## Task 4: Add hubs to menu (optional)

**Files:**
- Modify: `hugo.toml`

### Step 1: Add visas menu item

```toml
[[menu.main]]
  name = "Visas"
  pageRef = "visas"
  weight = 2
```

Reorder existing items:
```toml
[menu]
  [[menu.main]]
    name = "Checker"
    url = "ui/"
    weight = 1
  [[menu.main]]
    name = "Visas"
    pageRef = "visas"
    weight = 2
  [[menu.main]]
    name = "Blog"
    pageRef = "posts"
    weight = 3
  [[menu.main]]
    name = "Methodology"
    pageRef = "methodology"
    weight = 4
  [[menu.main]]
    name = "Disclaimer"
    pageRef = "disclaimer"
    weight = 5
  [[menu.main]]
    name = "Affiliate"
    pageRef = "affiliate-disclosure"
    weight = 6
```

### Step 2: Commit

```bash
git add hugo.toml
git commit -m "feat: add Visas section to main menu"
```

---

## Verification Checklist

Before claiming completion:

- [ ] `pwsh -File tools/tests/visa_hubs_tests.ps1` passes
- [ ] `py tools/lint_content.py` passes (no errors in content/visas/)
- [ ] `py tools/validate.py` passes
- [ ] `hugo --minify` builds without errors
- [ ] Generated pages appear at `/visas/`, `/visas/{country}/{visa}/`, and `/visas/{country}/{visa}/{route}/`
- [ ] All required lint blocks present in every generated page
- [ ] Deep links include `snapshot=` parameter

---

## Expected Output

After implementation:

```
content/visas/
├── _index.md                            # Root index
├── spain/
│   └── digital-nomad-visa/
│       ├── _index.md                    # Overview
│       └── consulate-via-bls-london/
│           └── index.md                 # Detail with requirements
├── portugal/
│   └── digital-nomad-visa/
│       ├── _index.md
│       └── vfs-china/
│           └── index.md
├── germany/
│   └── freelance-visa/
│       ├── _index.md
│       └── embassy-london/
│           └── index.md
├── costa-rica/
│   └── digital-nomad/
│       ├── _index.md
│       └── law/
│           └── index.md
├── malta/
│   └── nomad-residence-permit/
│       ├── _index.md
│       └── residency/
│           └── index.md
└── thailand/
    └── destination-thailand-visa/
        ├── _index.md
        └── mfa/
            └── index.md
```

Each detail page contains:
- Requirements table with evidence excerpts
- Source document links
- All 5 lint-required blocks
- Deep link with `snapshot=` parameter
- CTA to compliance checker
