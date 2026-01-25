$ErrorActionPreference = "Stop"
$failed = $false

function Assert-True {
  param([bool]$Condition, [string]$Message)
  if (-not $Condition) { Write-Host "FAIL: $Message" -ForegroundColor Red; $script:failed = $true }
  else { Write-Host "PASS: $Message" -ForegroundColor Green }
}

$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Push-Location $root
try {
  $proc = Start-Process -FilePath "python" -ArgumentList "tools/sync_hugo_static.py" -Wait -PassThru
  Assert-True ($proc.ExitCode -eq 0) "sync_hugo_static.py runs"

  $headers = Join-Path $root "static/_headers"
  Assert-True (Test-Path $headers) "static/_headers exists"
} finally {
  Pop-Location
}

if ($failed) { Write-Error "Header tests failed."; exit 1 }
Write-Host "All checks passed." -ForegroundColor Green
