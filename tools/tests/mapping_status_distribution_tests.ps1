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

$root = (Resolve-Path "$PSScriptRoot/../..").Path
$mappingDir = Join-Path $root "data/mappings"

Assert-True (Test-Path $mappingDir) "mappings directory exists"

$mappingFiles = @(Get-ChildItem -Path $mappingDir -Filter "*.json" -File)
Assert-True ($mappingFiles.Count -gt 0) "mapping json files exist"

$allowed = @("GREEN", "UNKNOWN", "RED", "NOT_REQUIRED", "YELLOW")
$counts = @{}
foreach ($s in $allowed) { $counts[$s] = 0 }

foreach ($file in $mappingFiles) {
  $obj = Get-Content -Raw -Path $file.FullName | ConvertFrom-Json
  $status = [string]$obj.status
  Assert-True ($allowed -contains $status) "$($file.Name) uses allowed status"
  if ($allowed -contains $status) {
    $counts[$status] = [int]$counts[$status] + 1
  }
}

$total = 0
foreach ($s in $allowed) { $total += [int]$counts[$s] }
Assert-True ($total -eq $mappingFiles.Count) "status distribution sums to mapping file count"

# Repository currently contains at least one YELLOW status; keep this explicit so reporting cannot omit it.
Assert-True ([int]$counts["YELLOW"] -ge 1) "YELLOW status is represented in mapping distribution"

if ($failed) {
  Write-Error "Mapping status distribution checks failed."
  exit 1
}

Write-Host "All checks passed." -ForegroundColor Green
