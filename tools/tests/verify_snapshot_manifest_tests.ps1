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
$snapshotId = "ZZ_VERIFY_TEST_" + (Get-Random -Minimum 10000 -Maximum 99999)
$env:SNAPSHOT_ID = $snapshotId
$env:SNAPSHOT_ROOT = Join-Path $root "data/.snapshots_verify_test"
$snapshotDir = Join-Path $env:SNAPSHOT_ROOT $snapshotId

function Cleanup {
  if (Test-Path $env:SNAPSHOT_ROOT) {
    Get-ChildItem -Recurse -Force -Path $env:SNAPSHOT_ROOT | ForEach-Object {
      try { $_.Attributes = "Normal" } catch {}
    }
    Remove-Item -LiteralPath $env:SNAPSHOT_ROOT -Recurse -Force
  }
  Remove-Item Env:SNAPSHOT_ID -ErrorAction SilentlyContinue
  Remove-Item Env:SNAPSHOT_ROOT -ErrorAction SilentlyContinue
}

try {
  $proc = Start-Process -FilePath "py" -ArgumentList "tools/build_snapshot.py" -WorkingDirectory $root -Wait -PassThru
  Assert-True ($proc.ExitCode -eq 0) "build_snapshot.py runs"

  $proc2 = Start-Process -FilePath "py" -ArgumentList @("tools/verify_snapshot_manifest.py", "--snapshot-dir", $snapshotDir) -WorkingDirectory $root -Wait -PassThru
  Assert-True ($proc2.ExitCode -eq 0) "verify_snapshot_manifest.py passes on fresh snapshot"

  Add-Content -Path (Join-Path $snapshotDir "ui_index.json") -Value " "
  $proc3 = Start-Process -FilePath "py" -ArgumentList @("tools/verify_snapshot_manifest.py", "--snapshot-dir", $snapshotDir) -WorkingDirectory $root -Wait -PassThru
  Assert-True ($proc3.ExitCode -ne 0) "verify_snapshot_manifest.py fails on mismatch"
} finally {
  Cleanup
}

if ($failed) {
  Write-Error "One or more checks failed."
  exit 1
}

Write-Host "All checks passed." -ForegroundColor Green
