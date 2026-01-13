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

Write-Host "Gitignore checks..." -ForegroundColor Cyan
Assert-True (Test-Path ".gitignore") ".gitignore exists"
if (Test-Path ".gitignore") {
  $gitignore = Get-Content -Raw -Path ".gitignore"
  Assert-True ($gitignore -like "*.hugo_build.lock*") "ignores .hugo_build.lock"
  Assert-True ($gitignore -like "*public/*") "ignores public/"
  Assert-True ($gitignore -like "*hugo.exe*") "ignores hugo.exe"
  Assert-True ($gitignore -like "*tools/logs/*") "ignores tools/logs/"
}

Write-Host "Build log checks..." -ForegroundColor Cyan
Assert-True (Test-Path "tools/build_hugo.ps1") "build_hugo.ps1 exists"

Assert-True (Test-Path "tools/logs/hugo-build.log") "hugo-build.log exists"
if (Test-Path "tools/logs/hugo-build.log") {
  $log = Get-Content -Raw -Path "tools/logs/hugo-build.log"
  $size = (Get-Item "tools/logs/hugo-build.log").Length
  Assert-True ($size -gt 0) "hugo-build.log is not empty"
  Assert-True ($log -like "*Build timestamp:*") "log includes build timestamp"
  Assert-True ($log -like "*Hugo version:*") "log includes Hugo version"
  Assert-True ($log -like "*Build command:*") "log includes build command"
  Assert-True ($log -like "*Exit code: 0*") "log includes successful exit code"
}

if ($failed) {
  Write-Error "One or more checks failed."
  exit 1
}

Write-Host "All checks passed." -ForegroundColor Green
