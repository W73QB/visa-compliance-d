$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$logDir = Join-Path $PSScriptRoot "logs"
$logPath = Join-Path $logDir "hugo-build.log"

New-Item -ItemType Directory -Force -Path $logDir | Out-Null

$hugoExe = Join-Path $root "hugo.exe"
$hugoCmd = $null
if (Test-Path $hugoExe) {
  $hugoCmd = $hugoExe
} else {
  $cmd = Get-Command hugo -ErrorAction SilentlyContinue
  if ($cmd) { $hugoCmd = $cmd.Source }
}

if (-not $hugoCmd) {
  Write-Error "Hugo not found. Install Hugo Extended or place hugo.exe in repo root."
  exit 1
}

Push-Location $root
try {
  $timestamp = Get-Date -Format "yyyy-MM-ddTHH:mm:ssK"
  $version = & $hugoCmd version
  Set-Content -Path $logPath -Value "Build timestamp: $timestamp"
  Add-Content -Path $logPath -Value "Hugo version: $version"
  Add-Content -Path $logPath -Value "Build command: $hugoCmd --minify"
  Add-Content -Path $logPath -Value "--- Hugo build output ---"

  $prevEap = $ErrorActionPreference
  $prevNative = $null
  if ($PSVersionTable.PSVersion.Major -ge 7) {
    $prevNative = $PSNativeCommandUseErrorActionPreference
    $PSNativeCommandUseErrorActionPreference = $false
  }
  $ErrorActionPreference = "Continue"
  & $hugoCmd --minify 2>&1 | Tee-Object -FilePath $logPath -Append
  $ErrorActionPreference = $prevEap
  if ($PSVersionTable.PSVersion.Major -ge 7 -and $null -ne $prevNative) {
    $PSNativeCommandUseErrorActionPreference = $prevNative
  }
  $exitCode = $LASTEXITCODE
  Add-Content -Path $logPath -Value "Exit code: $exitCode"

  if ($exitCode -ne 0) {
    Write-Error "Hugo build failed with exit code $exitCode"
    exit $exitCode
  }

  & (Join-Path $PSScriptRoot "build_pagefind.ps1")
  if ($LASTEXITCODE -ne 0) {
    Write-Error "Pagefind build failed with exit code $LASTEXITCODE"
    exit $LASTEXITCODE
  }
  Write-Host "Log written to $logPath"
} finally {
  Pop-Location
}
