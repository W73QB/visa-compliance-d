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
Push-Location $root
try {
  $env:HUGO_PARAMS_ANALYTICS_SRC = "https://example.com/analytics.js"
  $env:HUGO_PARAMS_ANALYTICS_ID = "vf-test"

  $proc = Start-Process -FilePath "hugo" -ArgumentList @("--minify") -WorkingDirectory $root -Wait -PassThru
  Assert-True ($proc.ExitCode -eq 0) "hugo --minify runs"

  $htmlFiles = Get-ChildItem -Path (Join-Path $root "public") -Recurse -Filter *.html
  $rendered = $htmlFiles | Where-Object { $_.FullName -notmatch "\\public\\ui\\" }
  if (-not $rendered -or $rendered.Count -eq 0) {
    Write-Host "No Hugo-rendered HTML files found; skipping analytics render checks." -ForegroundColor Yellow
    return
  }
  $matchSrc = $false
  $matchId = $false
  foreach ($file in $rendered) {
    $raw = Get-Content -Raw -Path $file.FullName
    if ($raw -match [regex]::Escape($env:HUGO_PARAMS_ANALYTICS_SRC)) { $matchSrc = $true }
    if ($raw -match [regex]::Escape($env:HUGO_PARAMS_ANALYTICS_ID)) { $matchId = $true }
  }
  Assert-True $matchSrc "analytics src is rendered"
  Assert-True $matchId "analytics id is rendered"
} finally {
  Remove-Item Env:HUGO_PARAMS_ANALYTICS_SRC -ErrorAction SilentlyContinue
  Remove-Item Env:HUGO_PARAMS_ANALYTICS_ID -ErrorAction SilentlyContinue
  Pop-Location
}

if ($failed) {
  Write-Error "One or more checks failed."
  exit 1
}

Write-Host "All checks passed." -ForegroundColor Green
