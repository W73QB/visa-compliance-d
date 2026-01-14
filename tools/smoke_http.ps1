param(
  [Parameter(Mandatory = $true)][string]$BaseUrl
)

$ErrorActionPreference = "Stop"
$failed = $false

function Assert-True {
  param([bool]$Condition, [string]$Message)
  if (-not $Condition) {
    Write-Host "FAIL: $Message" -ForegroundColor Red
    $script:failed = $true
  } else {
    Write-Host "PASS: $Message" -ForegroundColor Green
  }
}

function Get-Ok {
  param([string]$Url)
  try {
    return Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 30
  } catch {
    Write-Host "ERROR: $Url -> $($_.Exception.Message)" -ForegroundColor Red
    $script:failed = $true
    return $null
  }
}

$base = $BaseUrl.TrimEnd("/")

Write-Host "Smoke HTTP checks..." -ForegroundColor Cyan

$ui = Get-Ok "$base/ui/"
if ($ui) { Assert-True ($ui.StatusCode -eq 200) "/ui/ returns 200" }

$index = Get-Ok "$base/data/ui_index.json"
if ($index) {
  Assert-True ($index.StatusCode -eq 200) "/data/ui_index.json returns 200"
  $json = $index.Content | ConvertFrom-Json
  $first = $json.sources_by_id.PSObject.Properties[0].Value
  if ($null -ne $first -and $first.local_path) {
    $src = Get-Ok ("$base/" + $first.local_path.TrimStart("/"))
    if ($src) { Assert-True ($src.StatusCode -eq 200) "source file returns 200" }
  } else {
    Assert-True $false "ui_index.json has at least one source"
  }
}

if ($failed) {
  Write-Error "One or more checks failed."
  exit 1
}

Write-Host "All checks passed." -ForegroundColor Green
