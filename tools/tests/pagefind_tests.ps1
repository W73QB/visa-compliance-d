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
$shell = Get-Command pwsh -ErrorAction SilentlyContinue
if (-not $shell) { $shell = Get-Command powershell -ErrorAction SilentlyContinue }
if (-not $shell) {
  Write-Error "PowerShell not found."
  exit 1
}
$proc = Start-Process -FilePath $shell.Source -ArgumentList @("-File", "tools/build_hugo.ps1") -WorkingDirectory $root -Wait -PassThru
Assert-True ($proc.ExitCode -eq 0) "build_hugo runs"

$pagefindDir = Join-Path $root "public/pagefind"
Assert-True (Test-Path $pagefindDir) "public/pagefind exists"

if ($failed) {
  Write-Error "One or more checks failed."
  exit 1
}

Write-Host "All checks passed." -ForegroundColor Green
