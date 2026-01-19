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
$wf = Join-Path $root ".github/workflows/source-monitor.yml"
$wfPr = Join-Path $root ".github/workflows/source-monitor-pr.yml"

Assert-True (Test-Path $wf) "source-monitor workflow exists"
$wfText = Get-Content -Raw -Path $wf
Assert-True ($wfText -match "--write-status") "source-monitor writes status"
Assert-True ($wfText -match "--report-md") "source-monitor writes report"

Assert-True (Test-Path $wfPr) "source-monitor PR workflow exists"
$wfPrText = Get-Content -Raw -Path $wfPr
Assert-True ($wfPrText -match "create-pull-request") "PR workflow creates PR"
Assert-True ($wfPrText -match "create-issue-from-file") "PR workflow creates issue"

if ($failed) {
  Write-Error "One or more checks failed."
  exit 1
}

Write-Host "All checks passed." -ForegroundColor Green
