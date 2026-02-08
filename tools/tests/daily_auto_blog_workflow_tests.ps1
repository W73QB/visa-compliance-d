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
$wfPath = Join-Path $root ".github/workflows/daily-auto-blog.yml"
Assert-True (Test-Path $wfPath) "daily workflow file exists"

if (Test-Path $wfPath) {
  $wf = Get-Content -Raw -Path $wfPath
  Assert-True ($wf -match "cron:\s*'0 9 \* \* \*'") "explicit UTC cron"
  Assert-True ($wf -match "workflow_dispatch") "workflow_dispatch enabled"
  Assert-True ($wf -match "cancel-in-progress:\s*false") "cancel-in-progress false"
  Assert-True ($wf -match "actions/checkout@v4") "checkout pinned"
  Assert-True ($wf -match "actions/setup-python@v5") "setup-python pinned"
  Assert-True ($wf -match "actions/cache@v4") "cache pinned"
  Assert-True ($wf -match "pip install jsonschema pyyaml") "python deps installed"
  Assert-True ($wf -match "peter-evans/create-issue-from-file@v5") "issue action pinned"
  Assert-True ($wf -match "peter-evans/create-pull-request@v6") "pr action pinned"
  Assert-True ($wf -match "content/posts/\*\*") "add-paths includes posts"
  Assert-True ($wf -match "run-status.json") "add-paths includes run-status"
  Assert-True ($wf -match "seen_topics.json") "add-paths includes seen topics"
  Assert-True ($wf -match "docs/ops/daily-auto-blog/runs/\*\*") "add-paths includes runs path"
  Assert-True ($wf -match "--runs-dir docs/ops/daily-auto-blog/runs") "run command uses explicit runs-dir"
  Assert-True ($wf -match "continue-on-error:\s*true") "pipeline step continues on error"
  Assert-True ($wf -match "daily_auto_blog.py update-status") "workflow persists status explicitly"
  Assert-True ($wf -match "Detect stale snapshot links") "workflow checks stale snapshots"
  Assert-True ($wf -match "stale_snapshots") "workflow exports stale snapshot metric"
  Assert-True ($wf -match "Detect aging draft PRs") "workflow checks aging draft PRs"
  Assert-True ($wf -match "aged_prs") "workflow exports draft PR aging metric"
  Assert-True ($wf -match "Append monitoring summary") "workflow appends monitoring summary"
  Assert-True ($wf -match "steps\.streak\.outputs\.alert == 'true'\s*\|\|\s*steps\.stale\.outputs\.stale_snapshots != '0'\s*\|\|\s*steps\.pr_aging\.outputs\.aged_prs != '0'") "issue trigger includes stale and aging signals"
}

if ($failed) {
  Write-Error "One or more checks failed."
  exit 1
}

Write-Host "All checks passed." -ForegroundColor Green
