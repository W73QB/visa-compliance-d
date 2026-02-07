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

. "$PSScriptRoot/_python.ps1"
$python = Get-PythonLauncher

$root = (Resolve-Path "$PSScriptRoot/../..").Path
$tmp = Join-Path $root "data/.daily_auto_blog_e2e"
if (Test-Path $tmp) { Remove-Item -LiteralPath $tmp -Recurse -Force }
New-Item -ItemType Directory -Path $tmp -Force | Out-Null

$configPath = Join-Path $root "tools/daily_auto_blog_config.json"
$sitemap = Join-Path $root "tools/tests/fixtures/daily_auto_blog/sitemap_urlset.xml"
$searchFixture = Join-Path $root "tools/tests/fixtures/daily_auto_blog/search_results.json"
$draftFixture = Join-Path $root "tools/tests/fixtures/daily_auto_blog/draft.md"
$postOut = Join-Path $tmp "e2e-post.md"
$runsDir = Join-Path $tmp "runs"

$proc = Start-Process -FilePath $python -ArgumentList @("tools/daily_auto_blog.py", "run", "--date", "2026-02-07", "--config", $configPath, "--state-dir", $tmp, "--runs-dir", $runsDir, "--sitemap", $sitemap, "--search-input-json", $searchFixture, "--dry-run", "--draft-fixture", $draftFixture, "--output-post", $postOut) -WorkingDirectory $root -Wait -PassThru
Assert-True ($proc.ExitCode -eq 0) "run e2e exits 0"

$manifest = Join-Path $runsDir "2026-02-07/run_manifest.json"
Assert-True (Test-Path $manifest) "manifest exists"
Assert-True (Test-Path $postOut) "post created"

$manifestObj = Get-Content -Raw -Path $manifest | ConvertFrom-Json
Assert-True ($manifestObj.status -eq "PASS") "manifest status PASS"

if (Test-Path $tmp) { Remove-Item -LiteralPath $tmp -Recurse -Force }

if ($failed) {
  Write-Error "One or more checks failed."
  exit 1
}

Write-Host "All checks passed." -ForegroundColor Green
