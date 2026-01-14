$ErrorActionPreference = "Stop"
$failed = $false

function Assert-True {
  param([bool]$Condition, [string]$Message)
  if (-not $Condition) {
    Write-Host "FAIL: $Message" -ForegroundColor Red
    $script:failed = $true
  } else {
    Write-Host "PASS: $Message" -ForegroundColor Green
  }
}

function New-TempRoot {
  $root = Join-Path $env:TEMP ([System.Guid]::NewGuid().ToString())
  New-Item -ItemType Directory -Path $root | Out-Null
  return $root
}

Write-Host "verify_static_bundle checks..." -ForegroundColor Cyan

# Happy path on repo
$proc1 = Start-Process -FilePath "py" -ArgumentList "tools/verify_static_bundle.py" -Wait -PassThru
Assert-True ($proc1.ExitCode -eq 0) "verify passes on current repo"

# Failure on empty sources and empty files
$root = New-TempRoot
New-Item -ItemType Directory -Path (Join-Path $root "static/ui") | Out-Null
New-Item -ItemType Directory -Path (Join-Path $root "static/data") | Out-Null
New-Item -ItemType Directory -Path (Join-Path $root "static/sources") | Out-Null
Set-Content -Path (Join-Path $root "static/ui/index.html") -Value ""
Set-Content -Path (Join-Path $root "static/data/ui_index.json") -Value "{}"
$env:VERIFY_ROOT = $root
$proc2 = Start-Process -FilePath "py" -ArgumentList "tools/verify_static_bundle.py" -Wait -PassThru
Assert-True ($proc2.ExitCode -ne 0) "verify fails on empty bundle"
$env:VERIFY_ROOT = ""

if ($failed) {
  Write-Error "One or more checks failed."
  exit 1
}

Write-Host "All checks passed." -ForegroundColor Green
