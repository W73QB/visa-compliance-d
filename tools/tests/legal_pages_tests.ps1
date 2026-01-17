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

$paths = @(
  "content/legal/us/affiliate-disclosure.md",
  "content/legal/eu-uk/affiliate-disclosure.md",
  "content/legal/ca/affiliate-disclosure.md",
  "content/legal/apac/affiliate-disclosure.md",
  "content/legal/us/privacy.md",
  "content/legal/eu-uk/privacy.md",
  "content/legal/ca/privacy.md",
  "content/legal/apac/privacy.md",
  "content/privacy/_index.md",
  "layouts/partials/cookie_banner.html"
)

foreach ($p in $paths) {
  $full = Join-Path $root $p
  Assert-True (Test-Path $full) "$p exists"
}

$headPath = Join-Path $root "layouts/partials/extend_head.html"
if (Test-Path $headPath) {
  $head = Get-Content -Raw -Path $headPath
  Assert-True ($head -like "*vf_analytics_allowed*") "analytics gating script exists"
}

if ($failed) {
  Write-Error "One or more checks failed."
  exit 1
}

Write-Host "All checks passed." -ForegroundColor Green
