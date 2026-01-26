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

Assert-True ($ui -like "*application/ld+json*") "UI includes JSON-LD structured data"
Assert-True ($ui -like "*aria-live*") "UI has aria-live region"
Assert-True ($ui -like "*Skip to main content*") "UI has skip link"
Assert-True ($ui -like "*Needs Review*") "UI includes needs review badge"
Assert-True ($ui -like "*Last Verified*") "UI includes last verified label"

Assert-True ($ui -like "*const DATA_URL*") "DATA_URL is computed dynamically"
Assert-True ($ui -like "*location.pathname*") "DATA_URL uses location.pathname"
Assert-True ($ui -like "*dataLayer.push*") "UI defines dataLayer tracking"

Assert-True ($ui -like "*function escapeHtml*") "escapeHtml helper exists"
Assert-True ($ui -like "*function sanitizeUrl*") "sanitizeUrl helper exists"
Assert-True ($ui -like '*startsWith("//")*') "sanitizeUrl blocks protocol-relative URLs"
Assert-True ($ui -like "*file:*") "sanitizeUrl blocks file: scheme"
Assert-True ($ui -like "*javascript*") "sanitizeUrl blocks javascript: scheme"
Assert-True (-not ($ui -match '\$\{ev\.locator')) "openModal does not inject locator without escaping"
Assert-True (-not ($ui -match '\$\{ev\.excerpt')) "openModal does not inject excerpt without escaping"
Assert-True (-not ($ui -match '\$\{r\.text')) "renderReasons does not inject reason text without escaping"
Assert-True (-not ($ui -match '\$\{meta\.title')) "renderRequirements does not inject title without escaping"
Assert-True ($ui -like "*snapshotId*") "UI includes snapshotId field"
Assert-True ($ui -like "*Synthetic source*") "UI labels synthetic sources"
Assert-True ($ui -like '*href="../methodology/"*') "UI footer links to methodology"
Assert-True ($ui -like '*href="../disclaimer/"*') "UI footer links to disclaimer"
Assert-True ($ui -like '*href="../affiliate-disclosure/"*') "UI footer links to affiliate disclosure"

$bytes = [System.IO.File]::ReadAllBytes("ui/index.html")
$nonAsciiBytes = @($bytes | Where-Object { $_ -gt 127 })
Assert-True ($nonAsciiBytes.Count -eq 0) "ui/index.html contains only ASCII characters"

$node = Get-Command node -ErrorAction SilentlyContinue
if ($node) {
  $tmp = New-TemporaryFile
  $nodeScript = @'
const fs = require("fs");
const html = fs.readFileSync("ui/index.html", "utf8");
const parts = html.split("<script>");
let parsed = 0;
for (let i = 1; i < parts.length; i += 1) {
  const part = parts[i];
  const end = part.indexOf("</script>");
  if (end === -1) continue;
  const code = part.slice(0, end).trim();
  if (!code) continue;
  parsed += 1;
  try {
    new Function(code);
  } catch (err) {
    console.error("SCRIPT_PARSE_ERROR", err && err.message ? err.message : err);
    process.exit(1);
  }
}
if (parsed === 0) {
  console.error("NO_INLINE_SCRIPT");
  process.exit(1);
}
'@
  Set-Content -Path $tmp -Value $nodeScript -Encoding UTF8
  $proc = Start-Process node -ArgumentList $tmp -Wait -PassThru -NoNewWindow
  Remove-Item $tmp -ErrorAction SilentlyContinue
  Assert-True ($proc.ExitCode -eq 0) "UI inline scripts parse without syntax errors"
} else {
  Write-Host "SKIP: node not available for UI script parse check" -ForegroundColor Yellow
}

Write-Host "Index build checks..." -ForegroundColor Cyan
$index = Get-Content -Raw -Path "data/ui_index.json" | ConvertFrom-Json

$hasSourcesById = $index.PSObject.Properties.Name -contains "sources_by_id"
Assert-True $hasSourcesById "ui_index.json contains sources_by_id"
if ($hasSourcesById) {
  $sourceKeys = $index.sources_by_id.PSObject.Properties.Name
  Assert-True ($sourceKeys -contains "CR_DECREE_43619_2026") "sources_by_id includes known source metadata"
  Assert-True ($sourceKeys -contains "SAFETYWING_WEBSITE_2026") "sources_by_id includes SafetyWing product source"
  Assert-True ($sourceKeys -contains "GENERIC_WEBSITE_2026") "sources_by_id includes GenericInsurer product source"
  Assert-True (-not [string]::IsNullOrEmpty($index.sources_by_id.SAFETYWING_WEBSITE_2026.sha256)) "SafetyWing source has SHA256"
  Assert-True (-not [string]::IsNullOrEmpty($index.sources_by_id.GENERIC_WEBSITE_2026.sha256)) "GenericInsurer source has SHA256"
  Assert-True ($index.sources_by_id.SAFETYWING_WEBSITE_2026.synthetic -eq $true) "SafetyWing source marked synthetic"
  Assert-True ($index.sources_by_id.GENERIC_WEBSITE_2026.synthetic -eq $true) "GenericInsurer source marked synthetic"
}
Assert-True ($index.PSObject.Properties.Name -contains "snapshot_id") "ui_index.json includes snapshot_id"

Assert-True ($ui -like "*offerCta*") "UI has offer CTA container"
Assert-True ($ui -like "*Affiliate*") "UI renders affiliate disclosure"
Assert-True ($ui -like '*status === "RED"*') "UI hides CTA for RED"
Assert-True ($ui -like "*data-cta-disclosure*") "CTA disclosure container exists"
Assert-True ($ui -like "*Ad label*") "UI renders Ad label near CTA"
Assert-True ($ui -like "*vf-region-select*") "UI has region selector"

$hasOffers = $index.PSObject.Properties.Name -contains "offers_by_product"
Assert-True $hasOffers "ui_index.json contains offers_by_product"

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

$pagesPath = ".github/workflows/pages.yml"
Assert-True (Test-Path $pagesPath) "Pages workflow file exists"
if (Test-Path $pagesPath) {
  $pages = Get-Content -Raw -Path $pagesPath
  Assert-True ($pages -notlike '*hugo-version: "latest"*') "pages workflow does not use Hugo latest"
  Assert-True ($pages -like '*hugo-version: "0.146.0"*') "pages workflow pins Hugo version"

  Assert-True ($pages -like "*workflow_dispatch*") "pages workflow supports manual release builds"
  Assert-True ($pages -like "*build_release_snapshot.py*") "pages workflow runs release snapshot when requested"
}

if ($failed) {
  Write-Error "One or more checks failed."
  exit 1
}

Write-Host "All checks passed." -ForegroundColor Green
