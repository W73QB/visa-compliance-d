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

Write-Host "Mapping engine rule tests..." -ForegroundColor Cyan

# Run build_mappings and check output
$proc = Start-Process -FilePath "py" -ArgumentList "tools/build_mappings.py" -Wait -PassThru -NoNewWindow
Assert-True ($proc.ExitCode -eq 0) "build_mappings.py runs successfully"

# Check Spain DNV vs SafetyWing mapping has RED status (unauthorized)
$mapping = Get-Content "data/mappings/ES_DNV_BLS_LONDON_2026__SAFETYWING_NOMAD_2026.json" | ConvertFrom-Json
Assert-True ($mapping.status -eq "RED") "SafetyWing unauthorized in Spain produces RED"

# Check reasons contain authorization failure
$hasAuthReason = $mapping.reasons | Where-Object { $_.text -like "*authorized*" }
Assert-True ($null -ne $hasAuthReason) "Mapping includes authorization failure reason"

if ($failed) {
  Write-Error "One or more checks failed."
  exit 1
}

Write-Host "All checks passed." -ForegroundColor Green
# Test comprehensive requirement (missing should be tracked)
$mapping = Get-Content "data/mappings/ES_DNV_BLS_LONDON_2026__GENERIC_EXPAT_COMPLETE_2026.json" | ConvertFrom-Json
$hasCompMissing = $mapping.missing | Where-Object { $_ -eq "specs.comprehensive" }
Assert-True ($null -ne $hasCompMissing) "Missing comprehensive spec is tracked"
# Test public health system risks coverage requirement (missing should be tracked)
$mapping = Get-Content "data/mappings/ES_DNV_BLS_LONDON_2026__GENERIC_EXPAT_COMPLETE_2026.json" | ConvertFrom-Json
$hasPublicRisk = $mapping.missing | Where-Object { $_ -eq "specs.covers_public_health_system_risks" }
Assert-True ($null -ne $hasPublicRisk) "Missing public health system risks coverage is tracked"
