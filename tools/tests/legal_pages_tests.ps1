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
  "content/legal/apac/affiliate-disclosure.md"
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
