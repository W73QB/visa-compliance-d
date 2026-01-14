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
  $bytes = [System.IO.File]::ReadAllBytes($p)
  $hasBom = ($bytes.Length -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF)
  Assert-True (-not ($raw -match "\u0192\?")) "$p has no broken encoding sequence '\u0192?'"
  Assert-True (-not ($raw -match "\uFFFD")) "$p has no replacement character"
  Assert-True (-not $hasBom) "$p has no BOM"
}

if ($failed) { Write-Error "Encoding checks failed."; exit 1 }
Write-Host "All checks passed." -ForegroundColor Green
