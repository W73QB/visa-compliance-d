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

$pages = Get-Content -Raw -Path ".github/workflows/pages.yml"
$ui = Get-Content -Raw -Path ".github/workflows/ui-compliance.yml"

Assert-True ($pages -match "fetch-depth:\s*0") "pages workflow fetch-depth 0"
Assert-True ($ui -match "fetch-depth:\s*0") "ui-compliance workflow fetch-depth 0"

if ($failed) {
  Write-Error "One or more checks failed."
  exit 1
}

Write-Host "All checks passed." -ForegroundColor Green
