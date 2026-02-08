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

$root = (Resolve-Path "$PSScriptRoot/../..").Path
$wfPath = Join-Path $root ".github/workflows/pages.yml"
Assert-True (Test-Path $wfPath) "pages workflow exists"

if (Test-Path $wfPath) {
  $wf = Get-Content -Raw -Path $wfPath
  Assert-True ($wf -match "Run tests") "workflow has Run tests step"
  Assert-True ($wf -match "Lint content") "workflow has lint step"
  Assert-True ($wf -match "Check editorial targets") "workflow has editorial targets step"
  Assert-True ($wf -match "Run SEO audit gate") "workflow has SEO gate step"
  Assert-True ($wf -match "Check internal links") "workflow has internal link gate step"
  Assert-True ($wf -match "Build Hugo \(with log\)") "workflow has build step"
  Assert-True ($wf -match "mapping_status_distribution_tests\.ps1") "workflow runs mapping status distribution test"

  $idxRunTests = $wf.IndexOf("- name: Run tests")
  $idxLint = $wf.IndexOf("- name: Lint content")
  $idxEditorial = $wf.IndexOf("- name: Check editorial targets")
  $idxSeo = $wf.IndexOf("- name: Run SEO audit gate")
  $idxLinks = $wf.IndexOf("- name: Check internal links")
  $idxBuild = $wf.IndexOf("- name: Build Hugo (with log)")

  $ordered = ($idxRunTests -ge 0 -and $idxLint -gt $idxRunTests -and $idxEditorial -gt $idxLint -and $idxSeo -gt $idxEditorial -and $idxLinks -gt $idxSeo -and $idxBuild -gt $idxLinks)
  Assert-True $ordered "quality gates run before build in expected order"
  Assert-True (-not ($wf -match "continue-on-error:\s*true")) "pages workflow has no continue-on-error bypass"
}

if ($failed) {
  Write-Error "Pages workflow gate checks failed."
  exit 1
}

Write-Host "All checks passed." -ForegroundColor Green
