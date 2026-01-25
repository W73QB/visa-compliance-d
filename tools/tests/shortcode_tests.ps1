$ErrorActionPreference = "Stop"
$failed = $false

function Assert-True {
  param(
    [Parameter(Mandatory = $true)][bool]$Condition,
    [Parameter(Mandatory = $true)][string]$Message
  )
  if (-not $Condition) { Write-Host "FAIL: $Message" -ForegroundColor Red; $script:failed = $true }
  else { Write-Host "PASS: $Message" -ForegroundColor Green }
}

$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Push-Location $root
try {
  $proc = Start-Process -FilePath "hugo" -ArgumentList @("--minify", "-D") -WorkingDirectory $root -Wait -PassThru
  Assert-True ($proc.ExitCode -eq 0) "hugo --minify -D runs"

  $html = Join-Path $root "public/templates/checker-cta-test/index.html"
  Assert-True (Test-Path $html) "checker cta test page rendered"

  $raw = Get-Content -Raw -Path $html
  $hrefs = Select-String -InputObject $raw -Pattern 'href="([^"]+)"' -AllMatches | ForEach-Object { $_.Matches } | ForEach-Object { $_.Groups[1].Value }
  $cta = $hrefs | Where-Object { $_ -match "/ui/" }
  $ok = $false
  foreach ($h in $cta) {
    if ($h -match "visa=ES_DNV_BLS_LONDON_2026" -and $h -match "snapshot=latest") { $ok = $true }
  }
  Assert-True $ok "checker_cta generates visa+snapshot query"
} finally {
  Pop-Location
}

if ($failed) { Write-Error "Shortcode tests failed."; exit 1 }
Write-Host "All checks passed." -ForegroundColor Green
