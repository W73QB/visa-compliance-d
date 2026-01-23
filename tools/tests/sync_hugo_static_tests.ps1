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

function New-TempRoot {
  $temp = $env:TEMP
  if (-not $temp) {
    $temp = [System.IO.Path]::GetTempPath()
  }
  $root = Join-Path $temp ([System.Guid]::NewGuid().ToString())
  New-Item -ItemType Directory -Path $root | Out-Null
  return $root
}

function Write-MinimalFiles {
  param(
    [string]$Root,
    [switch]$IncludeCss
  )
  New-Item -ItemType Directory -Path (Join-Path $Root "ui") | Out-Null
  Set-Content -Path (Join-Path $Root "ui/index.html") -Value "<html></html>"
  if ($IncludeCss) {
    Set-Content -Path (Join-Path $Root "ui/style.css") -Value "body{}"
  }
  New-Item -ItemType Directory -Path (Join-Path $Root "data") | Out-Null
  Set-Content -Path (Join-Path $Root "data/ui_index.json") -Value "{}"
  New-Item -ItemType Directory -Path (Join-Path $Root "sources") | Out-Null
  Set-Content -Path (Join-Path $Root "sources/test.txt") -Value "ok"
}

Write-Host "sync_hugo_static fail-hard checks..." -ForegroundColor Cyan

try {
  # Missing ui should fail
  $root1 = New-TempRoot
  New-Item -ItemType Directory -Path (Join-Path $root1 "data") | Out-Null
  Set-Content -Path (Join-Path $root1 "data/ui_index.json") -Value "{}"
  $env:SYNC_ROOT = $root1
  $proc1 = Start-Process -FilePath "py" -ArgumentList "tools/sync_hugo_static.py" -Wait -PassThru
  Assert-True ($proc1.ExitCode -ne 0) "sync fails when ui/ is missing"

  # Missing ui_index.json should fail
  $root2 = New-TempRoot
  New-Item -ItemType Directory -Path (Join-Path $root2 "ui") | Out-Null
  Set-Content -Path (Join-Path $root2 "ui/index.html") -Value "<html></html>"
  $env:SYNC_ROOT = $root2
  $proc2 = Start-Process -FilePath "py" -ArgumentList "tools/sync_hugo_static.py" -Wait -PassThru
  Assert-True ($proc2.ExitCode -ne 0) "sync fails when data/ui_index.json is missing"

  # Missing ui/style.css should fail
  $rootCss = New-TempRoot
  Write-MinimalFiles -Root $rootCss -IncludeCss
  Remove-Item -Path (Join-Path $rootCss "ui/style.css")
  $env:SYNC_ROOT = $rootCss
  $procCss = Start-Process -FilePath "py" -ArgumentList "tools/sync_hugo_static.py" -Wait -PassThru
  Assert-True ($procCss.ExitCode -ne 0) "sync fails when ui/style.css is missing"

  # RELEASE_BUILD requires sources
  $root3 = New-TempRoot
  Write-MinimalFiles -Root $root3 -IncludeCss
  Remove-Item -Recurse -Force (Join-Path $root3 "sources")
  $env:SYNC_ROOT = $root3
  $env:RELEASE_BUILD = "1"
  $proc3 = Start-Process -FilePath "py" -ArgumentList "tools/sync_hugo_static.py" -Wait -PassThru
  Assert-True ($proc3.ExitCode -ne 0) "sync fails in release mode when sources/ missing"
  $env:RELEASE_BUILD = ""

  # Happy path
  $root4 = New-TempRoot
  Write-MinimalFiles -Root $root4 -IncludeCss
  $env:SYNC_ROOT = $root4
  $proc4 = Start-Process -FilePath "py" -ArgumentList "tools/sync_hugo_static.py" -Wait -PassThru
  Assert-True ($proc4.ExitCode -eq 0) "sync succeeds when required inputs exist"
}
finally {
  @($root1, $root2, $root3, $root4, $rootCss) |
    Where-Object { $_ -and $_.Trim() -ne "" } |
    ForEach-Object { Remove-Item -Recurse -Force $_ -ErrorAction SilentlyContinue }
}

if ($failed) {
  Write-Error "One or more checks failed."
  exit 1
}

Write-Host "All checks passed." -ForegroundColor Green
