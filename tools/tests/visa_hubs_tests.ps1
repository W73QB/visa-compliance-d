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

# Phase 4: Verify CI includes hub generation
$pagesYmlPath = Join-Path $root ".github/workflows/pages.yml"
if (Test-Path $pagesYmlPath) {
  $pagesYml = Get-Content -Raw -Path $pagesYmlPath
  Assert-True ($pagesYml -match "build_content_hubs.py") "CI runs build_content_hubs.py"
} else {
  Assert-True $false "pages.yml missing"
}

if ($failed) { Write-Error "Visa hub checks failed."; exit 1 }
Write-Host "All checks passed." -ForegroundColor Green
