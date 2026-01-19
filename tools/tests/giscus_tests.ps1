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
$contentDir = Join-Path $root "content/posts"
$testFile = Join-Path $contentDir "giscus-test.md"

$frontMatter = @"
---
title: "Giscus Test"
date: 2026-01-19
giscus: true
---
Test content.
"@

try {
  New-Item -ItemType Directory -Force -Path $contentDir | Out-Null
  Set-Content -Path $testFile -Value $frontMatter -Encoding utf8

  $env:HUGO_PARAMS_GISCUS_REPO = "owner/repo"
  $env:HUGO_PARAMS_GISCUS_REPO_ID = "repoid"
  $env:HUGO_PARAMS_GISCUS_CATEGORY = "General"
  $env:HUGO_PARAMS_GISCUS_CATEGORY_ID = "catid"
  $env:HUGO_PARAMS_GISCUS_MAPPING = "pathname"

  $proc = Start-Process -FilePath "hugo" -ArgumentList @("--minify") -WorkingDirectory $root -Wait -PassThru
  Assert-True ($proc.ExitCode -eq 0) "hugo --minify runs"

  $html = Join-Path $root "public/posts/giscus-test/index.html"
  Assert-True (Test-Path $html) "giscus test page exists"
  if (Test-Path $html) {
    $raw = Get-Content -Raw -Path $html
    Assert-True ($raw -match "giscus.app/client.js") "giscus script rendered"
  }
} finally {
  Remove-Item $testFile -ErrorAction SilentlyContinue
  Remove-Item Env:HUGO_PARAMS_GISCUS_REPO -ErrorAction SilentlyContinue
  Remove-Item Env:HUGO_PARAMS_GISCUS_REPO_ID -ErrorAction SilentlyContinue
  Remove-Item Env:HUGO_PARAMS_GISCUS_CATEGORY -ErrorAction SilentlyContinue
  Remove-Item Env:HUGO_PARAMS_GISCUS_CATEGORY_ID -ErrorAction SilentlyContinue
  Remove-Item Env:HUGO_PARAMS_GISCUS_MAPPING -ErrorAction SilentlyContinue
}

if ($failed) {
  Write-Error "One or more checks failed."
  exit 1
}

Write-Host "All checks passed." -ForegroundColor Green
