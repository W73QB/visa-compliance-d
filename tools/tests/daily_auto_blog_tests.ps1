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
$tmp = Join-Path $root "data/.daily_auto_blog_tests"
if (Test-Path $tmp) { Remove-Item -LiteralPath $tmp -Recurse -Force }
New-Item -ItemType Directory -Path $tmp -Force | Out-Null

# --- Contracts ---
$configPath = Join-Path $root "tools/daily_auto_blog_config.json"
$claimSchemaPath = Join-Path $root "tools/schemas/daily_claim_map.schema.json"
$fmSchemaPath = Join-Path $root "tools/schemas/daily_front_matter.schema.json"
$promptPath = Join-Path $root "docs/prompts/daily-auto-blog.md"

Assert-True (Test-Path $configPath) "config exists"
Assert-True (Test-Path $claimSchemaPath) "claim schema exists"
Assert-True (Test-Path $fmSchemaPath) "front matter schema exists"
Assert-True (Test-Path $promptPath) "prompt exists"

# --- Sitemap parsing ---
$sitemap = Join-Path $root "tools/tests/fixtures/daily_auto_blog/sitemap_urlset.xml"
$sitemapOut = Join-Path $tmp "index.json"
$proc = Start-Process -FilePath $python -ArgumentList @("tools/daily_auto_blog.py", "index", "--sitemap", $sitemap, "--output", $sitemapOut) -WorkingDirectory $root -Wait -PassThru
Assert-True ($proc.ExitCode -eq 0) "index command exits 0"
Assert-True (Test-Path $sitemapOut) "index output exists"

$indexObj = Get-Content -Raw -Path $sitemapOut | ConvertFrom-Json
Assert-True ($indexObj.Count -gt 0) "index has parsed URLs"

$malformed = Join-Path $root "tools/tests/fixtures/daily_auto_blog/sitemap_malformed.xml"
$malOut = Join-Path $tmp "index-malformed.json"
$procMalformed = Start-Process -FilePath $python -ArgumentList @("tools/daily_auto_blog.py", "index", "--sitemap", $malformed, "--output", $malOut) -WorkingDirectory $root -Wait -PassThru
Assert-True ($procMalformed.ExitCode -ne 0) "malformed sitemap fails gracefully"

# --- Search + quota ---
$searchFixture = Join-Path $root "tools/tests/fixtures/daily_auto_blog/search_results.json"
$searchOut = Join-Path $tmp "candidates.json"
$searchProc = Start-Process -FilePath $python -ArgumentList @("tools/daily_auto_blog.py", "search", "--input-json", $searchFixture, "--output", $searchOut, "--query", "spain-dnv-insurance", "--date", "2026-02-06", "--state-dir", $tmp, "--config", $configPath) -WorkingDirectory $root -Wait -PassThru
Assert-True ($searchProc.ExitCode -eq 0) "search fixture mode exits 0"
Assert-True (Test-Path $searchOut) "search output exists"

$searchObj = Get-Content -Raw -Path $searchOut | ConvertFrom-Json
Assert-True ($searchObj.status -eq "PASS") "search status PASS"
Assert-True ($searchObj.items.Count -gt 0) "search has candidates"
Assert-True ($null -ne $searchObj.items[0].freshness) "search populates freshness"

$oldCseKey = $env:GOOGLE_CSE_API_KEY
$oldCseId = $env:GOOGLE_CSE_ID
$env:GOOGLE_CSE_API_KEY = ""
$env:GOOGLE_CSE_ID = ""
$missingSecretsOut = Join-Path $tmp "candidates-missing-secrets.json"
$missingSecretsProc = Start-Process -FilePath $python -ArgumentList @("tools/daily_auto_blog.py", "search", "--output", $missingSecretsOut, "--query", "spain-dnv-insurance", "--date", "2026-02-06", "--state-dir", $tmp, "--config", $configPath) -WorkingDirectory $root -Wait -PassThru
Assert-True ($missingSecretsProc.ExitCode -eq 0) "search missing secrets exits 0"
$missingSecretsObj = Get-Content -Raw -Path $missingSecretsOut | ConvertFrom-Json
Assert-True ($missingSecretsObj.status -eq "SKIP_MISSING_SECRET") "search missing secrets returns SKIP_MISSING_SECRET"
$env:GOOGLE_CSE_API_KEY = $oldCseKey
$env:GOOGLE_CSE_ID = $oldCseId

$quotaState = Join-Path $tmp "quota-test"
New-Item -ItemType Directory -Path $quotaState -Force | Out-Null
$quotaFile = Join-Path $quotaState "quota_usage.json"
$cacheFile = Join-Path $quotaState "search_cache.json"
Set-Content -Path $quotaFile -Encoding UTF8 -Value '{"daily":{"2026-02-06":100}}'
Set-Content -Path $cacheFile -Encoding UTF8 -Value '{}'
$quotaOut = Join-Path $tmp "candidates-quota.json"
$quotaProc = Start-Process -FilePath $python -ArgumentList @("tools/daily_auto_blog.py", "search", "--input-json", $searchFixture, "--output", $quotaOut, "--query", "spain-dnv-insurance", "--date", "2026-02-06", "--state-dir", $quotaState, "--config", $configPath) -WorkingDirectory $root -Wait -PassThru
Assert-True ($quotaProc.ExitCode -eq 0) "search quota guard exits 0"
$quotaObj = Get-Content -Raw -Path $quotaOut | ConvertFrom-Json
Assert-True ($quotaObj.status -eq "SKIP_QUOTA_EXHAUSTED") "quota reached returns SKIP_QUOTA_EXHAUSTED"

Set-Content -Path $cacheFile -Encoding UTF8 -Value '{"spain-dnv-insurance":[{"title":"cached","link":"https://example.gov","credibility_score":100,"freshness":10}]}'
$quotaCacheOut = Join-Path $tmp "candidates-quota-cache.json"
$quotaCacheProc = Start-Process -FilePath $python -ArgumentList @("tools/daily_auto_blog.py", "search", "--output", $quotaCacheOut, "--query", "spain-dnv-insurance", "--date", "2026-02-06", "--state-dir", $quotaState, "--config", $configPath) -WorkingDirectory $root -Wait -PassThru
Assert-True ($quotaCacheProc.ExitCode -eq 0) "search quota cache fallback exits 0"
$quotaCacheObj = Get-Content -Raw -Path $quotaCacheOut | ConvertFrom-Json
Assert-True ($quotaCacheObj.status -eq "PASS") "quota cache fallback returns PASS"

# --- Selection + dedup ---
$selectedOut = Join-Path $tmp "selected.json"
$selectProc = Start-Process -FilePath $python -ArgumentList @("tools/daily_auto_blog.py", "select", "--index", $sitemapOut, "--candidates", $searchOut, "--output", $selectedOut, "--state-dir", $tmp, "--config", $configPath) -WorkingDirectory $root -Wait -PassThru
Assert-True ($selectProc.ExitCode -eq 0) "select exits 0"
Assert-True (Test-Path $selectedOut) "selected output exists"
$selectedObj = Get-Content -Raw -Path $selectedOut | ConvertFrom-Json
Assert-True ($selectedObj.status -eq "PASS") "select status PASS"

$lowCandidates = Join-Path $tmp "candidates-low.json"
Set-Content -Path $lowCandidates -Encoding UTF8 -Value '{"status":"PASS","items":[{"title":"low","link":"https://example.com","snippet":"x","source_host":"example.com","credibility_score":10,"score_reason":"untrusted","freshness":0}]}'
$selectedLow = Join-Path $tmp "selected-low.json"
$selectLowProc = Start-Process -FilePath $python -ArgumentList @("tools/daily_auto_blog.py", "select", "--index", $sitemapOut, "--candidates", $lowCandidates, "--output", $selectedLow, "--state-dir", $tmp, "--config", $configPath) -WorkingDirectory $root -Wait -PassThru
Assert-True ($selectLowProc.ExitCode -eq 0) "select low candidate exits 0"
$selectedLowObj = Get-Content -Raw -Path $selectedLow | ConvertFrom-Json
Assert-True ($selectedLowObj.status -eq "SKIP_NO_CANDIDATE") "select returns SKIP_NO_CANDIDATE"

# --- Evidence ---
$evidenceOut = Join-Path $tmp "evidence.md"
$claimMapOut = Join-Path $tmp "claim_map.json"
$evidenceProc = Start-Process -FilePath $python -ArgumentList @("tools/daily_auto_blog.py", "evidence", "--selected", $selectedOut, "--output", $evidenceOut, "--claim-map", $claimMapOut, "--date", "2026-02-06") -WorkingDirectory $root -Wait -PassThru
Assert-True ($evidenceProc.ExitCode -eq 0) "evidence exits 0"
Assert-True (Test-Path $evidenceOut) "evidence output exists"
Assert-True (Test-Path $claimMapOut) "claim map output exists"
$claimMapObj = Get-Content -Raw -Path $claimMapOut | ConvertFrom-Json
Assert-True ($claimMapObj.claims.Count -gt 0) "claim map has claim entries"
Assert-True ($claimMapObj.claims[0].verification_status -eq "VERIFIED") "evidence emits VERIFIED claim"

# --- Draft write + QA ---
$draftFixture = Join-Path $root "tools/tests/fixtures/daily_auto_blog/draft.md"
$postOut = Join-Path $tmp "italy-elective-insurance.md"
$writeProc = Start-Process -FilePath $python -ArgumentList @("tools/daily_auto_blog.py", "write", "--evidence", $evidenceOut, "--claim-map", $claimMapOut, "--output", $postOut, "--date", "2026-02-06", "--config", $configPath, "--dry-run", "--fixture", $draftFixture, "--front-matter-schema", $fmSchemaPath) -WorkingDirectory $root -Wait -PassThru
Assert-True ($writeProc.ExitCode -eq 0) "write exits 0"
Assert-True (Test-Path $postOut) "post output exists"

$badClaimFixture = Join-Path $tmp "draft-bad-claim.md"
$draftText = Get-Content -Raw -Path $draftFixture
Set-Content -Path $badClaimFixture -Encoding UTF8 -Value ($draftText + "`nUnknown claim id C999 should fail.`n")
$badClaimOut = Join-Path $tmp "post-bad-claim.md"
$writeBadClaimProc = Start-Process -FilePath $python -ArgumentList @("tools/daily_auto_blog.py", "write", "--evidence", $evidenceOut, "--claim-map", $claimMapOut, "--output", $badClaimOut, "--date", "2026-02-06", "--config", $configPath, "--dry-run", "--fixture", $badClaimFixture, "--front-matter-schema", $fmSchemaPath) -WorkingDirectory $root -Wait -PassThru
Assert-True ($writeBadClaimProc.ExitCode -eq 8) "write fails on unknown claim references"

$badFmFixture = Join-Path $tmp "draft-bad-fm.md"
$badFm = @"
---
title: Missing FAQ
date: "2026-02-06"
description: x
tags: [visa]
---

## short answer

snapshot=2026-02-06

## key findings at a glance

## what the authority requires

## verified requirements

## how we evaluate

## proof package checklist

## common rejection traps

## faq

## check in the engine

## disclaimer

## affiliate disclosure

## evidence log
"@
Set-Content -Path $badFmFixture -Encoding UTF8 -Value $badFm
$badFmOut = Join-Path $tmp "post-bad-fm.md"
$writeBadFmProc = Start-Process -FilePath $python -ArgumentList @("tools/daily_auto_blog.py", "write", "--evidence", $evidenceOut, "--claim-map", $claimMapOut, "--output", $badFmOut, "--date", "2026-02-06", "--config", $configPath, "--dry-run", "--fixture", $badFmFixture, "--front-matter-schema", $fmSchemaPath) -WorkingDirectory $root -Wait -PassThru
Assert-True ($writeBadFmProc.ExitCode -eq 4) "write rejects invalid front matter schema"

$qaProc = Start-Process -FilePath $python -ArgumentList @("tools/daily_auto_blog.py", "qa", "--path", $postOut, "--claim-map", $claimMapOut, "--config", $configPath) -WorkingDirectory $root -Wait -PassThru
Assert-True ($qaProc.ExitCode -eq 0) "qa exits 0"

# --- Run orchestrator ---
$runsDir = Join-Path $tmp "runs-store"
$runPost = Join-Path $tmp "run-post.md"
$runProc = Start-Process -FilePath $python -ArgumentList @("tools/daily_auto_blog.py", "run", "--date", "2026-02-06", "--config", $configPath, "--state-dir", $tmp, "--runs-dir", $runsDir, "--sitemap", $sitemap, "--search-input-json", $searchFixture, "--dry-run", "--draft-fixture", $draftFixture, "--output-post", $runPost) -WorkingDirectory $root -Wait -PassThru
Assert-True ($runProc.ExitCode -eq 0) "run exits 0"
$manifestPath = Join-Path $runsDir "2026-02-06/run_manifest.json"
Assert-True (Test-Path $manifestPath) "run manifest exists in runs dir"

$manifestObj = Get-Content -Raw -Path $manifestPath | ConvertFrom-Json
Assert-True ($manifestObj.status -eq "PASS") "run manifest status PASS"
Assert-True ($null -ne $manifestObj.config_hash) "manifest includes config hash"
Assert-True ($null -ne $manifestObj.code_version) "manifest includes code version"

$runResumeProc = Start-Process -FilePath $python -ArgumentList @("tools/daily_auto_blog.py", "run", "--date", "2026-02-06", "--config", $configPath, "--state-dir", $tmp, "--runs-dir", $runsDir, "--sitemap", $sitemap, "--search-input-json", $searchFixture, "--dry-run", "--draft-fixture", $draftFixture, "--output-post", $runPost) -WorkingDirectory $root -Wait -PassThru
Assert-True ($runResumeProc.ExitCode -eq 0) "rerun same date resumes safely"

$searchUnknown = Join-Path $tmp "search-unknown.json"
Set-Content -Path $searchUnknown -Encoding UTF8 -Value '{"items":[{"title":"Unknown source","link":"","snippet":"x","source_host":""}]}'
$configUnknownPath = Join-Path $tmp "config-threshold-zero.json"
$configObj = Get-Content -Raw -Path $configPath | ConvertFrom-Json
$configObj.source_scoring.threshold = 0
($configObj | ConvertTo-Json -Depth 20) | Set-Content -Path $configUnknownPath -Encoding UTF8
$runUnknownPost = Join-Path $tmp "run-unknown-post.md"
$runUnknownProc = Start-Process -FilePath $python -ArgumentList @("tools/daily_auto_blog.py", "run", "--date", "2026-02-08", "--config", $configUnknownPath, "--state-dir", $tmp, "--runs-dir", $runsDir, "--sitemap", $sitemap, "--search-input-json", $searchUnknown, "--dry-run", "--draft-fixture", $draftFixture, "--output-post", $runUnknownPost) -WorkingDirectory $root -Wait -PassThru
Assert-True ($runUnknownProc.ExitCode -eq 0) "run unknown evidence exits 0"
$manifestUnknown = Join-Path $runsDir "2026-02-08/run_manifest.json"
$manifestUnknownObj = Get-Content -Raw -Path $manifestUnknown | ConvertFrom-Json
Assert-True ($manifestUnknownObj.status -eq "SKIP_NO_VERIFIED_EVIDENCE") "run skips when no verified evidence"
Assert-True (-not (Test-Path $runUnknownPost)) "run skip does not write post"

if (Test-Path $tmp) { Remove-Item -LiteralPath $tmp -Recurse -Force }

if ($failed) {
  Write-Error "One or more checks failed."
  exit 1
}

Write-Host "All checks passed." -ForegroundColor Green
