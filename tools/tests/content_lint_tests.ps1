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
$tempDir = Join-Path $root "data/.content_lint_test"
New-Item -ItemType Directory -Path $tempDir | Out-Null

$badPath = Join-Path $tempDir "bad.md"
Set-Content -Path $badPath -Value "# Missing sections and says best"

$goodPath = Join-Path $tempDir "good.md"
@"
---
title: "Test"
---

## What the authority requires

Text.

## How we evaluate

/methodology/

## Check in the engine

/ui/?visa=xx&product=yy&snapshot=releases/2026-01-12

## Disclaimer

Not legal advice.

## Affiliate disclosure

Disclosure text.
"@ | Set-Content -Path $goodPath

$proc = Start-Process -FilePath "py" -ArgumentList @("tools/lint_content.py", "--path", $badPath) -WorkingDirectory $root -Wait -PassThru
Assert-True ($proc.ExitCode -ne 0) "lint fails for missing blocks"

$proc2 = Start-Process -FilePath "py" -ArgumentList @("tools/lint_content.py", "--path", $goodPath) -WorkingDirectory $root -Wait -PassThru
Assert-True ($proc2.ExitCode -eq 0) "lint passes for valid post"

Remove-Item -LiteralPath $tempDir -Recurse -Force

if ($failed) {
  Write-Error "One or more checks failed."
  exit 1
}

Write-Host "All checks passed." -ForegroundColor Green
