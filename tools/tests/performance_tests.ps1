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

Write-Host "Performance budget tests..." -ForegroundColor Cyan

$uiSize = (Get-Item "ui/index.html").Length
Assert-True ($uiSize -lt 102400) "ui/index.html under 100KB ($uiSize bytes)"

$indexSize = (Get-Item "data/ui_index.json").Length
Assert-True ($indexSize -lt 512000) "ui_index.json under 500KB ($indexSize bytes)"

if ($failed) {
  Write-Error "One or more checks failed."
  exit 1
}

Write-Host "All checks passed." -ForegroundColor Green
