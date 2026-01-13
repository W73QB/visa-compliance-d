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

function Is-Sorted {
  param([string[]]$Items)
  if (-not $Items) { return $true }
  $sorted = $Items | Sort-Object
  return ($Items -join ",") -eq ($sorted -join ",")
}

Write-Host "UI compliance checks..." -ForegroundColor Cyan

$ui = Get-Content -Raw -Path "ui/index.html"
$ui = $ui.TrimStart([char]0xFEFF)

Assert-True ($ui -like "*const DATA_URL*") "DATA_URL is computed dynamically"
Assert-True ($ui -like "*location.pathname*") "DATA_URL uses location.pathname"

Assert-True ($ui -like "*function escapeHtml*") "escapeHtml helper exists"
Assert-True (-not ($ui -match '\$\{ev\.locator')) "openModal does not inject locator without escaping"
Assert-True (-not ($ui -match '\$\{ev\.excerpt')) "openModal does not inject excerpt without escaping"
Assert-True (-not ($ui -match '\$\{r\.text')) "renderReasons does not inject reason text without escaping"
Assert-True (-not ($ui -match '\$\{meta\.title')) "renderRequirements does not inject title without escaping"

$bytes = Get-Content -Encoding Byte -Path "ui/index.html"
$nonAsciiBytes = @($bytes | Where-Object { $_ -gt 127 })
Assert-True ($nonAsciiBytes.Count -eq 0) "ui/index.html contains only ASCII characters"

Write-Host "Index build checks..." -ForegroundColor Cyan
$index = Get-Content -Raw -Path "data/ui_index.json" | ConvertFrom-Json

$hasSourcesById = $index.PSObject.Properties.Name -contains "sources_by_id"
Assert-True $hasSourcesById "ui_index.json contains sources_by_id"
if ($hasSourcesById) {
  $sourceKeys = $index.sources_by_id.PSObject.Properties.Name
  Assert-True ($sourceKeys -contains "CR_DECREE_43619_2026") "sources_by_id includes known source metadata"
  Assert-True ($sourceKeys -contains "SAFETYWING_WEBSITE_2026") "sources_by_id includes SafetyWing product source"
  Assert-True ($sourceKeys -contains "GENERIC_WEBSITE_2026") "sources_by_id includes GenericInsurer product source"
}

$visaIds = @($index.visas | ForEach-Object { $_.id })
$productIds = @($index.products | ForEach-Object { $_.id })
Assert-True (Is-Sorted $visaIds) "visas are sorted by id"
Assert-True (Is-Sorted $productIds) "products are sorted by id"

Write-Host "CI workflow checks..." -ForegroundColor Cyan
$workflowPath = ".github/workflows/ui-compliance.yml"
Assert-True (Test-Path $workflowPath) "CI workflow file exists"
if (Test-Path $workflowPath) {
  $workflow = Get-Content -Raw -Path $workflowPath
  Assert-True ($workflow -like "*ui_compliance_tests.ps1*") "CI workflow runs ui compliance tests"
}

if ($failed) {
  Write-Error "One or more checks failed."
  exit 1
}

Write-Host "All checks passed." -ForegroundColor Green
