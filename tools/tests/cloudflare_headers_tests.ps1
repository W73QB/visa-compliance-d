$ErrorActionPreference = "Stop"
$failed = $false

function Assert-True {
  param([bool]$Condition, [string]$Message)
  if (-not $Condition) { Write-Host "FAIL: $Message" -ForegroundColor Red; $script:failed = $true }
  else { Write-Host "PASS: $Message" -ForegroundColor Green }
}

$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$docPath = Join-Path $root "docs/ops/cloudflare-security-cache.md"
Assert-True (Test-Path $docPath) "docs/ops/cloudflare-security-cache.md exists"

$doc = Get-Content -Raw -Path $docPath
$required = @(
  "Content-Security-Policy",
  "X-Frame-Options",
  "X-Content-Type-Options",
  "Referrer-Policy",
  "Permissions-Policy",
  "cache rules",
  "ui_index.json",
  "bypass"
)

foreach ($item in $required) {
  Assert-True ($doc -match [regex]::Escape($item)) "doc mentions $item"
}

if ($failed) { Write-Error "Cloudflare doc checks failed."; exit 1 }
Write-Host "All checks passed." -ForegroundColor Green
