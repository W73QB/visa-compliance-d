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
  "content/legal/us/terms.md",
  "content/legal/eu-uk/terms.md",
  "content/legal/ca/terms.md",
  "content/legal/apac/terms.md",
  "content/legal/us/refund.md",
  "content/legal/eu-uk/refund.md",
  "content/legal/ca/refund.md",
  "content/legal/apac/refund.md",
  "content/terms/_index.md",
  "content/refund/_index.md",
  "content/reports/premium/_index.md",
  "data/payments/payment_links.json"
)

foreach ($p in $paths) {
  $full = Join-Path $root $p
  Assert-True (Test-Path $full) "$p exists"
}

if ($failed) {
  Write-Error "One or more checks failed."
  exit 1
}

Write-Host "All checks passed." -ForegroundColor Green
