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
$productDir = Join-Path $root "data/products/ZZ_TEST/Invalid/2026-01-13"
$productPath = Join-Path $productDir "product_facts.json"
$metaPath = Join-Path $root "sources/ZZ_TEST_SOURCE_2026-01-13.meta.json"
$localPath = Join-Path $root "sources/ZZ_TEST_SOURCE_2026-01-13.md"
$sourceId = "ZZ_TEST_SOURCE_2026"

New-Item -ItemType Directory -Force -Path $productDir | Out-Null

try {
  $baseProduct = Get-Content -Raw -Path "data/products/SafetyWing/Nomad-Insurance/2026-01-12/product_facts.json" | ConvertFrom-Json
  $baseProduct.id = "ZZ_TEST_PRODUCT_2026"
  $baseProduct.provider = "ZZ_Test"
  $baseProduct.product_name = "Invalid Product"
  $baseProduct.evidence = @(@{ source_id = $sourceId; locator = "Test locator"; excerpt = "Test excerpt" })
  $baseProduct.specs.jurisdiction_facts = @{}
  $baseProduct | ConvertTo-Json -Depth 10 | Set-Content -Path $productPath -Encoding ASCII

  $meta = @{
    source_id = $sourceId
    url = "https://example.com/test"
    retrieved_at = "2026-01-13T00:00:00Z"
    sha256 = "deadbeef"
    local_path = "sources/ZZ_TEST_SOURCE_2026-01-13.md"
  }
  $meta | ConvertTo-Json -Depth 5 | Set-Content -Path $metaPath -Encoding ASCII

  $proc = Start-Process -FilePath "py" -ArgumentList "tools/validate.py" -WorkingDirectory $root -Wait -PassThru
  Assert-True ($proc.ExitCode -ne 0) "validate fails when local_path missing"

  Set-Content -Path $localPath -Value "test content" -Encoding ASCII
  $proc = Start-Process -FilePath "py" -ArgumentList "tools/validate.py" -WorkingDirectory $root -Wait -PassThru
  Assert-True ($proc.ExitCode -ne 0) "validate fails when sha256 mismatches"

  $meta.sha256 = ""
  $meta | ConvertTo-Json -Depth 5 | Set-Content -Path $metaPath -Encoding ASCII
  $proc = Start-Process -FilePath "py" -ArgumentList "tools/validate.py" -WorkingDirectory $root -Wait -PassThru
  Assert-True ($proc.ExitCode -ne 0) "validate fails when sha256 missing"

  $sha = (Get-FileHash -Algorithm SHA256 $localPath).Hash.ToLower()
  $meta.sha256 = $sha
  $meta | ConvertTo-Json -Depth 5 | Set-Content -Path $metaPath -Encoding ASCII
  $proc = Start-Process -FilePath "py" -ArgumentList "tools/validate.py" -WorkingDirectory $root -Wait -PassThru
  Assert-True ($proc.ExitCode -eq 0) "validate passes when sha256 matches"
} finally {
  if (Test-Path $productPath) { Remove-Item -Force $productPath }
  if (Test-Path $productDir) { Remove-Item -Force -Recurse $productDir }
  if (Test-Path $metaPath) { Remove-Item -Force $metaPath }
  if (Test-Path $localPath) { Remove-Item -Force $localPath }
}

if ($failed) {
  Write-Error "One or more checks failed."
  exit 1
}

Write-Host "All checks passed." -ForegroundColor Green
