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
$snapshotId = "ZZ_SNAPSHOT_TEST_" + (Get-Random -Minimum 10000 -Maximum 99999)
$env:SNAPSHOT_ID = $snapshotId
$snapshotRoot = Join-Path $root "data/.snapshots_test"
$env:SNAPSHOT_ROOT = $snapshotRoot
$snapshotDir = Join-Path $snapshotRoot $snapshotId

function Remove-SnapshotDir {
  param([string]$Path)
  if (-not (Test-Path $Path)) { return }
  Get-ChildItem -Recurse -Force -Path $Path | ForEach-Object {
    try { $_.Attributes = "Normal" } catch {}
  }
  Remove-Item -LiteralPath $Path -Recurse -Force
}

try {
  $proc = Start-Process -FilePath "py" -ArgumentList "tools/build_snapshot.py" -WorkingDirectory $root -Wait -PassThru
  Assert-True ($proc.ExitCode -eq 0) "build_snapshot.py runs successfully"

  Assert-True (Test-Path $snapshotDir) "snapshot directory exists"
  Assert-True (Test-Path (Join-Path $snapshotDir "visas")) "snapshot includes visas/"
  Assert-True (Test-Path (Join-Path $snapshotDir "products")) "snapshot includes products/"
  Assert-True (Test-Path (Join-Path $snapshotDir "mappings")) "snapshot includes mappings/"
  Assert-True (Test-Path (Join-Path $snapshotDir "ui_index.json")) "snapshot includes ui_index.json"
  Assert-True (Test-Path (Join-Path $snapshotDir "manifest.json")) "snapshot includes manifest.json"

  $manifest = Get-Content -Raw -Path (Join-Path $snapshotDir "manifest.json") | ConvertFrom-Json
  Assert-True ($manifest.snapshot_id -eq $snapshotId) "manifest snapshot_id matches"
  $uiEntry = $manifest.files | Where-Object { $_.path -eq "ui_index.json" }
  Assert-True ($null -ne $uiEntry) "manifest includes ui_index.json entry"
} finally {
  try {
    Remove-SnapshotDir -Path $snapshotRoot
  } catch {
    Write-Host "WARN: Failed to clean snapshot test directory." -ForegroundColor Yellow
  }
  Remove-Item Env:SNAPSHOT_ID -ErrorAction SilentlyContinue
  Remove-Item Env:SNAPSHOT_ROOT -ErrorAction SilentlyContinue
}

if ($failed) {
  Write-Error "One or more checks failed."
  exit 1
}

Write-Host "All checks passed." -ForegroundColor Green
