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

if ($failed) { Write-Error "Visa hub checks failed."; exit 1 }
Write-Host "All checks passed." -ForegroundColor Green
