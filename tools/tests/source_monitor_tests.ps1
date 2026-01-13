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
$fixtures = Join-Path $root "tools/tests/fixtures/source_monitor"
$sourcesDir = Join-Path $fixtures "sources"
$fixtureDir = Join-Path $fixtures "fixtures"
$out1 = Join-Path $fixtures "out1.json"
$out2 = Join-Path $fixtures "out2.json"
$fixturePath = Join-Path $fixtureDir "TEST_SOURCE.txt"
$original = Get-Content -Raw -Path $fixturePath

try {
  $proc = Start-Process -FilePath "py" -ArgumentList @("tools/check_source_changes.py", "--sources-dir", $sourcesDir, "--fixture-dir", $fixtureDir, "--output", $out1) -WorkingDirectory $root -Wait -PassThru
  Assert-True ($proc.ExitCode -eq 0) "source check runs"
  $report1 = Get-Content -Raw -Path $out1 | ConvertFrom-Json
  Assert-True ($report1.changed.Count -eq 0) "no changes when fixture matches"

  Add-Content -Path $fixturePath -Value "x"
  $proc2 = Start-Process -FilePath "py" -ArgumentList @("tools/check_source_changes.py", "--sources-dir", $sourcesDir, "--fixture-dir", $fixtureDir, "--output", $out2) -WorkingDirectory $root -Wait -PassThru
  Assert-True ($proc2.ExitCode -eq 0) "source check runs after mutation"
  $report2 = Get-Content -Raw -Path $out2 | ConvertFrom-Json
  Assert-True ($report2.changed.Count -eq 1) "change detected"
} finally {
  Set-Content -Path $fixturePath -Value $original
  Remove-Item -LiteralPath $out1, $out2 -Force -ErrorAction SilentlyContinue
}

if ($failed) {
  Write-Error "One or more checks failed."
  exit 1
}

Write-Host "All checks passed." -ForegroundColor Green
