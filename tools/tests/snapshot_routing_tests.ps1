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

$ui = Get-Content -Raw -Path "ui/index.html"
Assert-True ($ui -like "*snapshot=*" ) "UI references snapshot query param"
Assert-True ($ui -like "*snapshots/*" ) "UI builds data URL under snapshots/"
Assert-True ($ui -like '*searchParams.set("snapshot"*' ) "Deep link preserves snapshot param"

if ($failed) {
  Write-Error "One or more checks failed."
  exit 1
}

Write-Host "All checks passed." -ForegroundColor Green
