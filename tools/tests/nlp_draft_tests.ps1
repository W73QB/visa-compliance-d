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
$fixture = Join-Path $root "tools/tests/fixtures/nlp_draft/sample.pdf"
$outPath = Join-Path $root "tools/tests/fixtures/nlp_draft/output.json"

try {
  $proc = Start-Process -FilePath "py" -ArgumentList @(
    "tools/nlp_draft_mappings.py",
    "--input", $fixture,
    "--output", $outPath,
    "--source-id", "TEST_SOURCE"
  ) -WorkingDirectory $root -Wait -PassThru
  Assert-True ($proc.ExitCode -eq 0) "nlp draft script runs"

  Assert-True (Test-Path $outPath) "output json exists"
  if (Test-Path $outPath) {
    $data = Get-Content -Raw -Path $outPath | ConvertFrom-Json
    Assert-True ($null -ne $data.suggested_changes) "suggested_changes present"
    Assert-True ($null -ne $data.evidence_snippets) "evidence_snippets present"
  }
} finally {
  Remove-Item $outPath -ErrorAction SilentlyContinue
}

if ($failed) {
  Write-Error "One or more checks failed."
  exit 1
}

Write-Host "All checks passed." -ForegroundColor Green
