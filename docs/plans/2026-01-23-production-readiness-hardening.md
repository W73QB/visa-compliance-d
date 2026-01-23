# Production Readiness Hardening Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Eliminate remaining production readiness gaps by normalizing legal content encoding and documenting/verifying Cloudflare security headers and caching.

**Architecture:** Use @test-driven-development to add regression coverage for encoding and ops docs. Keep GitHub Pages as the origin; configure headers and cache policy at Cloudflare and store exact rules in a runbook so changes are auditable and repeatable. Use @verification-before-completion before any "done" claims.

**Tech Stack:** Hugo content, PowerShell tests (`tools/tests/*.ps1`), Cloudflare dashboard rules, GitHub Actions.

---

## Prerequisites

- Create a dedicated worktree per @brainstorming using @using-git-worktrees.

### Task 1: Lock down legal page encoding

**Files:**
- Modify: `tools/tests/content_encoding_tests.ps1`
- Modify: `content/disclaimer/_index.md`

**Step 1: Write the failing test**

Add an ASCII-only guard inside the foreach loop, just before the BOM assertion:

```powershell
  $nonAscii = @($bytes | Where-Object { $_ -gt 0x7E })
  Assert-True ($nonAscii.Count -eq 0) "$p has ASCII-only content"
```

**Step 2: Run test to verify it fails**

Run: `powershell -NoProfile -File tools/tests/content_encoding_tests.ps1`
Expected: FAIL with "content/disclaimer/_index.md has ASCII-only content" and/or "has no BOM".

**Step 3: Write minimal implementation**

Update `content/disclaimer/_index.md` to remove the UTF-8 BOM and fix the mojibake line:

```markdown
Disclaimer (Not legal advice)

...

We are not your lawyers, and using this site does not create a lawyer-client relationship.
```

Save the file as UTF-8 without BOM.

**Step 4: Run test to verify it passes**

Run: `powershell -NoProfile -File tools/tests/content_encoding_tests.ps1`
Expected: PASS.

**Step 5: Commit**

```bash
git add tools/tests/content_encoding_tests.ps1 content/disclaimer/_index.md
git commit -m "fix: normalize disclaimer encoding"
```

### Task 2: Add Cloudflare security headers and cache runbook

**Files:**
- Create: `tools/tests/cloudflare_headers_tests.ps1`
- Create: `docs/ops/cloudflare-security-cache.md`

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
$docPath = Join-Path $root "docs/ops/cloudflare-security-cache.md"
Assert-True (Test-Path $docPath) "docs/ops/cloudflare-security-cache.md exists"

$doc = Get-Content -Raw -Path $docPath
$required = @(
  "Content-Security-Policy",
  "X-Frame-Options",
  "X-Content-Type-Options",
  "Referrer-Policy",
  "Permissions-Policy",
  "cache rules",
  "ui_index.json",
  "bypass"
)

foreach ($item in $required) {
  Assert-True ($doc -match [regex]::Escape($item)) "doc mentions $item"
}

if ($failed) { Write-Error "Cloudflare doc checks failed."; exit 1 }
Write-Host "All checks passed." -ForegroundColor Green
```

**Step 2: Run test to verify it fails**

Run: `powershell -NoProfile -File tools/tests/cloudflare_headers_tests.ps1`
Expected: FAIL with "docs/ops/cloudflare-security-cache.md exists".

**Step 3: Write minimal implementation**

Create `docs/ops/cloudflare-security-cache.md` with:

```markdown
# Cloudflare Security Headers and Cache Rules

## Purpose
Define the required response headers and cache rules for the GitHub Pages origin behind Cloudflare.

## Security headers (Rules > Transform Rules > Modify Response Header)
Apply to all responses:

X-Frame-Options: DENY
X-Content-Type-Options: nosniff
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=(), microphone=(), camera=()
Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; img-src 'self' data:; connect-src 'self'; base-uri 'self'; frame-ancestors 'none'; object-src 'none'

Notes:
- `script-src` includes 'unsafe-inline' because ui/index.html uses inline scripts and an onclick handler.
- If inline scripts are moved to external files, remove 'unsafe-inline' and tighten CSP.

## Cache rules (Rules > Cache Rules)
Order matters. Put bypass rules above cache rules.

1) Bypass HTML
- If URI Path ends with `.html` -> Bypass cache

2) Bypass ui_index.json
- If URI Path ends with `/ui_index.json` -> Bypass cache

3) Cache assets
- If URI Path ends with `.css` -> Cache 4 hours
- If URI Path ends with `.js` -> Cache 4 hours
- If URI Path ends with `.woff2` -> Cache 1 year
- If URI Path ends with `.png` or `.jpg` or `.svg` -> Cache 1 year

## Manual verification
- `curl -I https://visafact.org/ui/` includes the security headers above.
- `curl -I https://visafact.org/data/ui_index.json` shows `cf-cache-status: BYPASS`.
- `curl -I https://visafact.org/ui/style.css` shows `cf-cache-status: HIT` or `MISS` with a cache TTL.
```

**Step 4: Run test to verify it passes**

Run: `powershell -NoProfile -File tools/tests/cloudflare_headers_tests.ps1`
Expected: PASS.

**Step 5: Commit**

```bash
git add tools/tests/cloudflare_headers_tests.ps1 docs/ops/cloudflare-security-cache.md
git commit -m "docs: add Cloudflare headers and cache runbook"
```

## Rollout (manual)

1. Apply Cloudflare rules using the runbook in `docs/ops/cloudflare-security-cache.md`.
2. Verify with the curl commands in the runbook.
