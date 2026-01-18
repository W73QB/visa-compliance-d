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
$uiIndex = Join-Path $root "data/ui_index.json"

$proc = Start-Process -FilePath "py" -ArgumentList @("tools/build_index.py") -WorkingDirectory $root -Wait -PassThru
Assert-True ($proc.ExitCode -eq 0) "build_index runs"

Assert-True (Test-Path $uiIndex) "ui_index.json exists"
$data = Get-Content -Raw -Path $uiIndex | ConvertFrom-Json

Assert-True ($null -ne $data.source_status) "source_status present"
Assert-True ($null -ne $data.source_status.needs_review_source_ids) "needs_review_source_ids present"

$hasLastVerified = $false
foreach ($m in $data.mappings) {
  if ($m.PSObject.Properties.Name -contains "last_verified") { $hasLastVerified = $true; break }
}
Assert-True ($hasLastVerified) "mapping has last_verified"

if ($failed) {
  Write-Error "One or more checks failed."
  exit 1
}

Write-Host "All checks passed." -ForegroundColor Green
