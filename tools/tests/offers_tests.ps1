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
$tempDir = Join-Path $root "data/.offers_test"
New-Item -ItemType Directory -Path $tempDir | Out-Null

$bad = Join-Path $tempDir "bad.json"
@"
{
  "offers": [
    {"product_id": "P1", "affiliate_url": "https://example.com", "label": "Best offer"}
  ]
}
"@ | Set-Content -Path $bad

$proc = Start-Process -FilePath "py" -ArgumentList @("tools/validate.py", "--offers", $bad) -WorkingDirectory $root -Wait -PassThru
Assert-True ($proc.ExitCode -ne 0) "validate fails for banned words"

$good = Join-Path $tempDir "good.json"
@"
{
  "offers": [
    {"product_id": "P1", "affiliate_url": "https://example.com", "label": "Get quote", "disclosure": "Affiliate link"}
  ]
}
"@ | Set-Content -Path $good

$proc2 = Start-Process -FilePath "py" -ArgumentList @("tools/validate.py", "--offers", $good) -WorkingDirectory $root -Wait -PassThru
Assert-True ($proc2.ExitCode -eq 0) "validate passes for good offer"

Remove-Item -LiteralPath $tempDir -Recurse -Force

if ($failed) {
  Write-Error "One or more checks failed."
  exit 1
}

Write-Host "All checks passed." -ForegroundColor Green
