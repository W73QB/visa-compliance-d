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

Write-Host "smoke.py checks..." -ForegroundColor Cyan

# Happy path
$root = New-TempRoot
New-Item -ItemType Directory -Path (Join-Path $root "data") | Out-Null
New-Item -ItemType Directory -Path (Join-Path $root "sources") | Out-Null
Set-Content -Path (Join-Path $root "sources/source.txt") -Value "ok"
@"
{
  "mappings": [
    {
      "reasons": [
        { "evidence": [ { "source_id": "SRC1" } ] }
      ]
    }
  ],
  "sources_by_id": {
    "SRC1": { "local_path": "sources/source.txt" }
  }
}
"@ | Set-Content -Path (Join-Path $root "data/ui_index.json")
$env:SMOKE_ROOT = $root
$env:SMOKE_INDEX_PATH = (Join-Path $root "data/ui_index.json")
$proc1 = Start-Process -FilePath "py" -ArgumentList "tools/smoke.py" -Wait -PassThru
Assert-True ($proc1.ExitCode -eq 0) "smoke passes when evidence path exists"

# Failure when evidence missing
Remove-Item -Force (Join-Path $root "sources/source.txt")
$proc2 = Start-Process -FilePath "py" -ArgumentList "tools/smoke.py" -Wait -PassThru
Assert-True ($proc2.ExitCode -ne 0) "smoke fails when evidence file missing"
$env:SMOKE_ROOT = ""
$env:SMOKE_INDEX_PATH = ""

if ($failed) {
  Write-Error "One or more checks failed."
  exit 1
}

Write-Host "All checks passed." -ForegroundColor Green
