$ErrorActionPreference = "Stop"
$root = (Resolve-Path "$PSScriptRoot/../..").Path

. "$PSScriptRoot/_python.ps1"
$python = Get-PythonLauncher

$proc = Start-Process -FilePath $python -ArgumentList "tools/check_internal_links.py" -WorkingDirectory $root -Wait -PassThru -NoNewWindow
if ($proc.ExitCode -ne 0) {
  throw "internal link integrity check failed"
}

Write-Host "Internal link integrity tests passed." -ForegroundColor Green
