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
$releaseId = "REL_TEST_" + (Get-Random -Minimum 10000 -Maximum 99999)
$releaseDir = Join-Path $root ("data/snapshots/releases/" + $releaseId)

function Remove-ReleaseDir {
  param([string]$Path)
  if (-not (Test-Path $Path)) { return }
  Get-ChildItem -Recurse -Force -Path $Path | ForEach-Object {
    try { $_.Attributes = "Normal" } catch {}
  }
  Get-ChildItem -Recurse -Force -File -Path $Path | ForEach-Object {
    try { Remove-Item -LiteralPath $_.FullName -Force } catch {}
  }
  Get-ChildItem -Recurse -Force -Directory -Path $Path | Sort-Object FullName -Descending | ForEach-Object {
    try { Remove-Item -LiteralPath $_.FullName -Force } catch {}
  }
  try { Remove-Item -LiteralPath $Path -Force } catch {}
}

try {
  $proc = Start-Process -FilePath "py" -ArgumentList @("tools/build_release_snapshot.py", "--release-id", $releaseId) -WorkingDirectory $root -Wait -PassThru
  Assert-True ($proc.ExitCode -eq 0) "build_release_snapshot.py runs"
  Assert-True (Test-Path $releaseDir) "release snapshot directory exists"
  Assert-True (Test-Path (Join-Path $releaseDir "manifest.json")) "release snapshot has manifest"

  $proc2 = Start-Process -FilePath "py" -ArgumentList @("tools/verify_snapshot_manifest.py", "--snapshot-dir", $releaseDir) -WorkingDirectory $root -Wait -PassThru
  Assert-True ($proc2.ExitCode -eq 0) "release manifest verifies"
} finally {
  Remove-ReleaseDir -Path $releaseDir
}

if ($failed) {
  Write-Error "One or more checks failed."
  exit 1
}

Write-Host "All checks passed." -ForegroundColor Green
