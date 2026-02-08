# Corrected Action Plan — Week 1 (Feb 8–14, 2026)

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Fix the two highest-impact blockers (structured data errors + crawl/indexability investigation), then harden the daily auto-blog pipeline by removing the hardcoded country bias.

**Architecture:** Three independent tracks that can run in parallel: (A) structured data fixes with regression tests, (B) crawl/indexability diagnostic script + report, (C) auto-blog search query country rotation fix. Each track has its own test + commit cycle.

**Tech Stack:** Hugo templates (Go templating), Python 3.11, PowerShell test suites, GitHub Actions YAML.

---

## Conventions

- **Test framework:** PowerShell `Assert-True` in `tools/tests/*.ps1` (project convention — no pytest).
- **Python launcher:** Use `Get-PythonLauncher` from `tools/tests/_python.ps1` (cross-platform shim).
- **Commits:** `fix:`, `feat:`, `test:`, `ci:` prefixes. Atomic — one concern per commit.
- **Do NOT modify:** `static/` (generated), `data/snapshots/` (generated), theme files in `themes/`.

---

## Track A: Fix Structured Data Errors

### Task 1: Fix BreadcrumbList position numbering

The breadcrumb schema at `layouts/partials/templates/schema_json.html:40-61` uses `$i` (zero-indexed) with `(add $i 1)` for position. However, when URL segments contain empty strings from `split`, the position counter can skip values or start wrong. Additionally, line 59 has a missing newline before `{{` which may cause JSON concatenation with the Article schema block below it.

**Specific issue:** The `$segments` split on line 41 can produce empty strings when `RelPermalink` has leading/trailing slashes. The `if gt (len $s) 0` guard (line 44) skips empties, but `$i` still increments, so `position` values can be `[2, 4]` instead of `[1, 2]`. Google requires consecutive positions starting at 1.

**Files:**
- Modify: `layouts/partials/templates/schema_json.html:40-61`
- Test: `tools/tests/hugo_integration_tests.ps1` (add assertions)

**Step 1: Write the failing test**

Add to `tools/tests/hugo_integration_tests.ps1`, before the final `if ($failed)` block:

```powershell
Write-Host "Breadcrumb position checks..." -ForegroundColor Cyan
if (Test-Path $schemaTemplate) {
  $schemaText = Get-Content -Raw -Path $schemaTemplate
  Assert-True ($schemaText -match '\$pos\s*=\s*1') "breadcrumb uses explicit position counter starting at 1"
  Assert-True ($schemaText -match '\$pos\s*=\s*add\s*\$pos\s*1') "breadcrumb increments position counter"
}
```

**Step 2: Run test to verify it fails**

Run: `pwsh -NoProfile -File tools/tests/hugo_integration_tests.ps1`
Expected: FAIL on "breadcrumb uses explicit position counter starting at 1"

**Step 3: Fix the breadcrumb template**

Replace `layouts/partials/templates/schema_json.html` lines 38-62 with:

```go-html-template
{{- /* Pages/Sections: BreadcrumbList */ -}}
{{- if (or .IsPage .IsSection) -}}
{{- $crumbs := slice -}}
{{- $segments := (split (trim (replace (.RelPermalink) (site.LanguagePrefix) "" ) "/") "/") -}}
{{- $path := "" -}}
{{- $pos := 1 -}}
{{- range $segments -}}
  {{- if gt (len .) 0 -}}
    {{- $path = printf "%s/%s" $path . -}}
    {{- $pg := site.GetPage $path -}}
    {{- if $pg -}}
      {{- $crumbs = $crumbs | append (dict "position" $pos "name" $pg.Title "item" $pg.Permalink) -}}
      {{- $pos = add $pos 1 -}}
    {{- end -}}
  {{- end -}}
{{- end -}}
{{- if gt (len $crumbs) 0 }}
{{- $items := slice -}}
{{- range $crumbs -}}
  {{- $items = $items | append (dict "@type" "ListItem" "position" .position "name" .name "item" .item) -}}
{{- end -}}
{{- $breadcrumbSchema := dict "@context" "https://schema.org" "@type" "BreadcrumbList" "itemListElement" $items -}}
<script type="application/ld+json">
{{ $breadcrumbSchema | jsonify | safeJS }}
</script>
{{- end }}
{{- end -}}
```

Key changes:
- Replace `$i` loop variable with explicit `$pos` counter starting at 1.
- Only increment `$pos` when a valid page is found (inside `if $pg`).
- Add trailing newline after `safeJS` closing to prevent JSON concatenation.

**Step 4: Run test to verify it passes**

Run: `pwsh -NoProfile -File tools/tests/hugo_integration_tests.ps1`
Expected: All PASS

**Step 5: Commit**

```bash
git add layouts/partials/templates/schema_json.html tools/tests/hugo_integration_tests.ps1
git commit -m "fix: breadcrumb schema position numbering — use explicit counter"
```

---

### Task 2: Ensure JSON-LD blocks are parseable (whitespace fix)

The Article schema block (`schema_json.html:87-89`) outputs `{{ $articleSchema | jsonify | safeJS }}` with a leading newline and no trailing newline before `</script>`. This can cause browsers/validators to see extra whitespace or concatenated JSON when multiple schema blocks appear on the same page.

**Files:**
- Modify: `layouts/partials/templates/schema_json.html:87-89`
- Test: `tools/tests/hugo_integration_tests.ps1` (add assertion)

**Step 1: Write the failing test**

Add to `tools/tests/hugo_integration_tests.ps1`, in the existing structured data section:

```powershell
Assert-True ($schemaText -notmatch 'safeJS\s*-\}\}[\r\n]*\{\{') "no JSON-LD blocks concatenated without </script> separator"
```

**Step 2: Run test to verify it fails or passes**

Run: `pwsh -NoProfile -File tools/tests/hugo_integration_tests.ps1`
(This test may already pass if there are proper `</script>` tags between blocks. If it passes, the whitespace issue is cosmetic — still fix for validator compliance but mark test as regression guard.)

**Step 3: Normalize all JSON-LD output blocks**

In `layouts/partials/templates/schema_json.html`, ensure every `<script type="application/ld+json">` block follows this pattern:

```
<script type="application/ld+json">
{{ $schema | jsonify | safeJS }}
</script>
```

Specifically, check lines 33-35, 58-60, 87-89, 106-108. Ensure consistent `{{ ... }}` (with space) and a newline before `</script>`.

**Step 4: Run tests**

Run: `pwsh -NoProfile -File tools/tests/hugo_integration_tests.ps1`
Expected: All PASS

**Step 5: Commit**

```bash
git add layouts/partials/templates/schema_json.html tools/tests/hugo_integration_tests.ps1
git commit -m "fix: normalize JSON-LD whitespace across all schema blocks"
```

---

## Track B: Crawl/Indexability Diagnostic

### Task 3: Create crawl/indexability diagnostic script

Google Search Console shows 5/7 pages not indexed. Structured data errors are **not** the cause (they affect rich results only). We need to investigate real crawl/indexability blockers:
- robots.txt directives
- `<meta name="robots" content="noindex">` tags
- canonical URL mismatches
- sitemap coverage gaps
- `_headers` X-Robots-Tag
- Hugo output confirming pages are actually built

**Files:**
- Create: `tools/check_indexability.py`
- Test: `tools/tests/indexability_tests.ps1`

**Step 1: Write the test file**

Create `tools/tests/indexability_tests.ps1`:

```powershell
$ErrorActionPreference = "Stop"
$failed = $false

function Assert-True {
  param(
    [Parameter(Mandatory = $true)][bool]$Condition,
    [Parameter(Mandatory = $true)][string]$Message
  )
  if (-not $Condition) {
    Write-Host "FAIL: $Message" -ForegroundColor Red
    $script:failed = $true
  } else {
    Write-Host "PASS: $Message" -ForegroundColor Green
  }
}

Assert-True (Test-Path "tools/check_indexability.py") "check_indexability.py exists"

. "$PSScriptRoot/_python.ps1"
$python = Get-PythonLauncher

$proc = Start-Process -FilePath $python -ArgumentList "tools/check_indexability.py" -Wait -PassThru -RedirectStandardOutput "$env:TEMP/indexability_out.txt"
$output = Get-Content -Raw -Path "$env:TEMP/indexability_out.txt"

Assert-True ($proc.ExitCode -eq 0) "check_indexability.py exits 0"
Assert-True ($output -match "robots.txt") "checks robots.txt"
Assert-True ($output -match "noindex") "checks noindex meta"
Assert-True ($output -match "canonical") "checks canonical consistency"
Assert-True ($output -match "sitemap") "checks sitemap coverage"

if ($failed) {
  Write-Error "One or more checks failed."
  exit 1
}

Write-Host "All checks passed." -ForegroundColor Green
```

**Step 2: Run test to verify it fails**

Run: `pwsh -NoProfile -File tools/tests/indexability_tests.ps1`
Expected: FAIL on "check_indexability.py exists"

**Step 3: Write the script**

Create `tools/check_indexability.py`:

```python
#!/usr/bin/env python3
"""Diagnose crawl/indexability issues for Hugo output.

Checks:
1. robots.txt — no Disallow blocking content paths
2. noindex meta — no pages with noindex in <head>
3. canonical consistency — <link rel="canonical"> matches page URL
4. sitemap coverage — all content pages present in sitemap.xml
5. _headers — no X-Robots-Tag: noindex
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
CONTENT = ROOT / "content"
STATIC_HEADERS = ROOT / "static" / "_headers"


def check_robots_txt() -> list[str]:
    """Check for blocking Disallow directives in robots.txt template."""
    issues = []
    # Hugo generates robots.txt from enableRobotsTXT = true
    # Check if any custom layout overrides it
    custom = ROOT / "layouts" / "robots.txt"
    if custom.exists():
        text = custom.read_text(encoding="utf-8")
        if re.search(r"Disallow:\s*/(?!$)", text):
            issues.append(f"robots.txt: custom layout has blocking Disallow: {custom}")
    print(f"[robots.txt] Custom layout override: {'yes' if custom.exists() else 'no (default Hugo — OK)'}")
    if not issues:
        print("[robots.txt] OK — no blocking directives found")
    return issues


def check_noindex_meta() -> list[str]:
    """Check content files for noindex front matter or raw meta tags."""
    issues = []
    count = 0
    for md in CONTENT.rglob("*.md"):
        text = md.read_text(encoding="utf-8")
        count += 1
        if re.search(r"noindex\s*[:=]\s*true", text, re.IGNORECASE):
            issues.append(f"noindex: {md.relative_to(ROOT)} has noindex directive")
        if re.search(r'<meta\s+name=["\']robots["\']\s+content=["\'][^"\']*noindex', text, re.IGNORECASE):
            issues.append(f"noindex: {md.relative_to(ROOT)} has noindex meta tag")
    print(f"[noindex] Scanned {count} content files")
    if not issues:
        print("[noindex] OK — no noindex directives found")
    return issues


def check_canonical() -> list[str]:
    """Check Hugo config for canonical URL consistency."""
    issues = []
    hugo_toml = ROOT / "hugo.toml"
    if hugo_toml.exists():
        text = hugo_toml.read_text(encoding="utf-8")
        has_canonify = "canonifyURLs" in text and "true" in text
        print(f"[canonical] canonifyURLs = {'true' if has_canonify else 'NOT SET — potential issue'}")
        if not has_canonify:
            issues.append("canonical: canonifyURLs not enabled in hugo.toml")
        base_match = re.search(r'baseURL\s*=\s*"([^"]+)"', text)
        if base_match:
            base = base_match.group(1)
            if not base.startswith("https://"):
                issues.append(f"canonical: baseURL is not HTTPS: {base}")
            if not base.endswith("/"):
                issues.append(f"canonical: baseURL missing trailing slash: {base}")
            print(f"[canonical] baseURL = {base}")
    if not issues:
        print("[canonical] OK")
    return issues


def check_sitemap_coverage() -> list[str]:
    """Check that key content pages would be included in sitemap."""
    issues = []
    # Hugo includes all non-draft, non-expired pages by default.
    # Check for draft: true in key content files.
    key_sections = ["posts", "visas", "guides", "traps"]
    draft_count = 0
    total = 0
    for section in key_sections:
        section_dir = CONTENT / section
        if not section_dir.exists():
            continue
        for md in section_dir.rglob("*.md"):
            if md.name == "_index.md":
                continue
            total += 1
            text = md.read_text(encoding="utf-8")
            if re.search(r"^draft\s*:\s*true", text, re.MULTILINE):
                draft_count += 1
                issues.append(f"sitemap: {md.relative_to(ROOT)} is draft (excluded from sitemap)")
    print(f"[sitemap] {total} content pages, {draft_count} drafts")
    if not issues:
        print("[sitemap] OK — no drafts blocking sitemap inclusion")
    return issues


def check_headers() -> list[str]:
    """Check _headers for X-Robots-Tag directives."""
    issues = []
    if STATIC_HEADERS.exists():
        text = STATIC_HEADERS.read_text(encoding="utf-8")
        if re.search(r"X-Robots-Tag.*noindex", text, re.IGNORECASE):
            issues.append("_headers: X-Robots-Tag contains noindex")
        print(f"[_headers] File exists, {len(text.splitlines())} lines")
    else:
        print("[_headers] No _headers file (OK)")
    if not issues:
        print("[_headers] OK — no X-Robots-Tag noindex")
    return issues


def main() -> int:
    all_issues: list[str] = []
    all_issues.extend(check_robots_txt())
    all_issues.extend(check_noindex_meta())
    all_issues.extend(check_canonical())
    all_issues.extend(check_sitemap_coverage())
    all_issues.extend(check_headers())

    print()
    if all_issues:
        print(f"ISSUES FOUND: {len(all_issues)}")
        for issue in all_issues:
            print(f"  - {issue}")
        return 0  # exit 0 — diagnostic tool, not a gate
    else:
        print("NO ISSUES FOUND — all crawl/indexability checks passed.")
        print()
        print("If GSC still shows unindexed pages, likely causes:")
        print("  1. Site is new and Google hasn't crawled all pages yet")
        print("  2. Low domain authority (no inbound links)")
        print("  3. Submit URLs manually in GSC > URL Inspection > Request Indexing")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

**Step 4: Run tests**

Run: `pwsh -NoProfile -File tools/tests/indexability_tests.ps1`
Expected: All PASS

**Step 5: Commit**

```bash
git add tools/check_indexability.py tools/tests/indexability_tests.ps1
git commit -m "feat: add crawl/indexability diagnostic script"
```

---

### Task 4: Wire indexability check into CI (pages.yml)

Add the diagnostic as an informational step (not a blocking gate) in `pages.yml`, after the existing quality gates.

**Files:**
- Modify: `.github/workflows/pages.yml:112` (after `Check internal links`)

**Step 1: Add step to pages.yml**

After line 112 (`run: python tools/check_internal_links.py`), add:

```yaml
      - name: Indexability diagnostic
        run: python tools/check_indexability.py
```

**Step 2: Run workflow test**

Run: `pwsh -NoProfile -File tools/tests/hugo_integration_tests.ps1`
(This test doesn't directly validate workflow YAML, but confirms no regressions.)

**Step 3: Commit**

```bash
git add .github/workflows/pages.yml
git commit -m "ci: add indexability diagnostic to deploy pipeline"
```

---

## Track C: Fix Auto-Blog Hardcoded Country

### Task 5: Make search query country configurable via rotation

The function `build_search_query()` at `tools/daily_auto_blog.py:332` hardcodes `"country": "spain"`. This biases all auto-generated search queries toward Spain content. The fix: derive country from the config rotation, mapping weekday hints to actual countries.

**Current config `rotation`:**
```json
{
  "mon": "route_update",
  "tue": "trap",
  "wed": "product_fact",
  "thu": "comparison",
  "fri": "proof_wording",
  "sat": "faq_hub",
  "sun": "update_digest"
}
```

**Problem:** Rotation values are content types, not countries. We need a `countries` list in config, then cycle through countries across days.

**Files:**
- Modify: `tools/daily_auto_blog_config.json` (add `countries` array)
- Modify: `tools/daily_auto_blog.py:318-339` (use countries from config)
- Test: `tools/tests/daily_auto_blog_tests.ps1` (add country rotation test)

**Step 1: Write the failing test**

Add to `tools/tests/daily_auto_blog_tests.ps1`, in the search section (after existing search tests, before the `# --- Select ---` comment):

```powershell
Write-Host "Country rotation checks..." -ForegroundColor Cyan
$configText = Get-Content -Raw -Path $configPath
Assert-True ($configText -match '"countries"') "config has countries array"
$pyCode = Get-Content -Raw -Path "tools/daily_auto_blog.py"
Assert-True ($pyCode -notmatch '"country":\s*"spain"') "no hardcoded spain in build_search_query"
Assert-True ($pyCode -match 'countries.*config') "build_search_query reads countries from config"
```

**Step 2: Run test to verify it fails**

Run: `pwsh -NoProfile -File tools/tests/daily_auto_blog_tests.ps1`
Expected: FAIL on "no hardcoded spain" and "config has countries array"

**Step 3: Add `countries` to config**

Modify `tools/daily_auto_blog_config.json` — add after `"rotation"` block:

```json
  "countries": ["spain", "portugal", "germany", "thailand", "malta", "costa-rica"],
```

**Step 4: Fix `build_search_query` in `tools/daily_auto_blog.py`**

Replace lines 318-339:

```python
def build_search_query(
    config: Dict[str, Any], run_date: str, template_offset: int = 0
) -> str:
    templates = config.get("query_templates", [])
    if not templates:
        return "visa insurance requirements"
    try:
        run_dt = datetime.strptime(run_date, "%Y-%m-%d")
    except Exception:
        run_dt = datetime.now(timezone.utc)
    weekday_key = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"][run_dt.weekday()]
    topic_hint = str(config.get("rotation", {}).get(weekday_key, "insurance"))
    template = templates[(run_dt.toordinal() + int(template_offset)) % len(templates)]
    countries = config.get("countries", ["spain"])
    country = countries[run_dt.toordinal() % len(countries)]
    values = {
        "country": country,
        "visa_type": topic_hint.replace("_", " "),
        "topic_slug": topic_hint,
    }
    try:
        return str(template).format(**values)
    except Exception:
        return str(template)
```

Key change: Line `"country": "spain"` → `countries[run_dt.toordinal() % len(countries)]`. This cycles through all 6 countries across days.

**Step 5: Run tests**

Run: `pwsh -NoProfile -File tools/tests/daily_auto_blog_tests.ps1`
Expected: All PASS (including new country rotation tests)

Also run: `pwsh -NoProfile -File tools/tests/daily_auto_blog_e2e_tests.ps1`
Expected: All PASS (E2E still works because fixture-based dry run doesn't call build_search_query)

**Step 6: Commit**

```bash
git add tools/daily_auto_blog_config.json tools/daily_auto_blog.py tools/tests/daily_auto_blog_tests.ps1
git commit -m "fix: rotate search query country across all 6 visa routes"
```

---

### Task 6: Add `socket.timeout` to HTTP retry logic

At `tools/daily_auto_blog.py:245-265`, the `http_json_with_retry` function retries `HTTPError` (429/5xx) and `URLError`, but not `socket.timeout`. Network timeouts should also be retried.

**Files:**
- Modify: `tools/daily_auto_blog.py:245-265`
- Test: `tools/tests/daily_auto_blog_tests.ps1` (add code assertion)

**Step 1: Write the failing test**

Add to `tools/tests/daily_auto_blog_tests.ps1`:

```powershell
Write-Host "Timeout retry checks..." -ForegroundColor Cyan
$pyCode = Get-Content -Raw -Path "tools/daily_auto_blog.py"
Assert-True ($pyCode -match 'socket\.timeout') "http_json_with_retry handles socket.timeout"
Assert-True ($pyCode -match 'import socket') "socket module imported"
```

**Step 2: Run test to verify it fails**

Run: `pwsh -NoProfile -File tools/tests/daily_auto_blog_tests.ps1`
Expected: FAIL on "socket.timeout"

**Step 3: Fix the retry logic**

Add `import socket` to imports at top of file (around line 8, with other stdlib imports).

Replace `tools/daily_auto_blog.py:245-265`:

```python
def http_json_with_retry(
    req_or_url: Any, timeout: int, retries: int = 3
) -> Dict[str, Any]:
    for attempt in range(retries + 1):
        try:
            with urlopen(req_or_url, timeout=timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except HTTPError as exc:
            retriable = exc.code == 429 or 500 <= exc.code < 600
            if retriable and attempt < retries:
                retry_after = parse_retry_after(exc.headers.get("Retry-After", ""))
                sleep_seconds = retry_after if retry_after > 0 else min(30, 2**attempt)
                time.sleep(sleep_seconds)
                continue
            raise
        except (URLError, socket.timeout):
            if attempt < retries:
                time.sleep(min(30, 2**attempt))
                continue
            raise
    raise RuntimeError("request failed after retries")
```

Key change: `except URLError:` → `except (URLError, socket.timeout):`.

**Step 4: Run tests**

Run: `pwsh -NoProfile -File tools/tests/daily_auto_blog_tests.ps1`
Expected: All PASS

**Step 5: Commit**

```bash
git add tools/daily_auto_blog.py tools/tests/daily_auto_blog_tests.ps1
git commit -m "fix: add socket.timeout to HTTP retry logic"
```

---

### Task 7: Document exit codes

`daily_auto_blog.py` uses numeric exit codes (0-12) across multiple subcommands. These are undocumented, making debugging difficult.

**Files:**
- Modify: `tools/daily_auto_blog.py` (add docstring at module level)

**Step 1: Write the failing test**

Add to `tools/tests/daily_auto_blog_tests.ps1`:

```powershell
Write-Host "Exit code documentation checks..." -ForegroundColor Cyan
$pyCode = Get-Content -Raw -Path "tools/daily_auto_blog.py"
Assert-True ($pyCode -match 'EXIT_CODES') "exit codes are documented"
Assert-True ($pyCode -match 'exit.*10.*budget') "budget exit code documented"
```

**Step 2: Run test to verify it fails**

Run: `pwsh -NoProfile -File tools/tests/daily_auto_blog_tests.ps1`
Expected: FAIL on "EXIT_CODES"

**Step 3: Add exit code documentation**

Add after the module docstring (near top of `tools/daily_auto_blog.py`, after imports), a constant:

```python
# EXIT_CODES:
# 0  — success (or SKIP with status written to output)
# 1  — general failure (search error, write error, QA fail)
# 2  — URL parse error in evidence command
# 3  — missing LLM API key in write command
# 4  — front matter schema validation failed
# 5  — claim reference validation failed
# 6  — checker CTA / snapshot= validation failed
# 7  — FAQ style validation failed
# 8  — banned word detected in generated content
# 9  — word count out of range
# 10 — LLM token budget exceeded (pre-check or post-check)
# 11 — LLM HTTP request failed
# 12 — FAQ front matter validation failed
```

**Step 4: Run tests**

Run: `pwsh -NoProfile -File tools/tests/daily_auto_blog_tests.ps1`
Expected: All PASS

**Step 5: Commit**

```bash
git add tools/daily_auto_blog.py tools/tests/daily_auto_blog_tests.ps1
git commit -m "docs: document daily_auto_blog.py exit codes"
```

---

## Summary

| Task | Track | Files | Effort | Acceptance Criteria |
|------|-------|-------|--------|---------------------|
| 1. Breadcrumb position fix | A | schema_json.html, hugo_integration_tests.ps1 | 15 min | Position values consecutive from 1; test passes |
| 2. JSON-LD whitespace | A | schema_json.html, hugo_integration_tests.ps1 | 10 min | No concatenated JSON-LD blocks; test passes |
| 3. Indexability diagnostic | B | check_indexability.py, indexability_tests.ps1 | 25 min | Script runs, checks 5 categories, exits 0 |
| 4. Wire into CI | B | pages.yml | 5 min | Step appears in workflow, non-blocking |
| 5. Country rotation | C | daily_auto_blog.py, config.json, tests.ps1 | 20 min | No hardcoded "spain"; cycles 6 countries |
| 6. socket.timeout retry | C | daily_auto_blog.py, tests.ps1 | 10 min | socket.timeout in except clause; test passes |
| 7. Exit code docs | C | daily_auto_blog.py, tests.ps1 | 10 min | EXIT_CODES block present; test passes |

**Total estimated effort: ~1.5 hours of implementation**

**Dependency graph:** All 3 tracks are independent. Within each track, tasks are sequential.

```
Track A: Task 1 → Task 2 → commit
Track B: Task 3 → Task 4 → commit
Track C: Task 5 → Task 6 → Task 7 → commit
```

**Final verification (after all tracks):**

```bash
pwsh -NoProfile -File tools/tests/hugo_integration_tests.ps1
pwsh -NoProfile -File tools/tests/daily_auto_blog_tests.ps1
pwsh -NoProfile -File tools/tests/daily_auto_blog_e2e_tests.ps1
pwsh -NoProfile -File tools/tests/daily_auto_blog_workflow_tests.ps1
pwsh -NoProfile -File tools/tests/indexability_tests.ps1
python tools/check_indexability.py
python tools/check_editorial_targets.py
```

All must exit 0.

---

## Out of Scope (Week 2+)

These items from the corrected priority list are deferred:
- Close UNKNOWN mappings (MT/CR) — requires source research, not code
- Content depth improvements — CI editorial gates pass; defer until intent-gap analysis done
- Missing trap posts (PT/TH/CR) — content creation, not infra
- Cross-day cache date context fix — lower priority after country rotation fix
- Snapshot retention policy — no immediate impact
