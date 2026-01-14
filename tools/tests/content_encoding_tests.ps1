$ErrorActionPreference = "Stop"
$failed = $false

function Assert-True {
  param([bool]$Condition, [string]$Message)
  if (-not $Condition) { Write-Host "FAIL: $Message" -ForegroundColor Red; $script:failed = $true }
  else { Write-Host "PASS: $Message" -ForegroundColor Green }
}

Write-Host "Content encoding checks..." -ForegroundColor Cyan

$paths = @(
  "content/methodology/_index.md",
  "content/disclaimer/_index.md",
  "content/affiliate-disclosure/_index.md"
)

foreach ($p in $paths) {
  $raw = Get-Content -Raw -Path $p
  Assert-True (-not ($raw -match "\u0192\?")) "$p has no broken encoding sequence '\u0192?'"
  Assert-True (-not ($raw -match "\uFFFD")) "$p has no replacement character"
  Assert-True (-not ($raw.StartsWith([char]0xFEFF))) "$p has no BOM"
}

if ($failed) { Write-Error "Encoding checks failed."; exit 1 }
Write-Host "All checks passed." -ForegroundColor Green
