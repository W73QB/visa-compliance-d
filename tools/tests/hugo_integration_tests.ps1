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

Write-Host "Hugo config checks..." -ForegroundColor Cyan
Assert-True (Test-Path "hugo.toml") "hugo.toml exists"
if (Test-Path "hugo.toml") {
  $hugo = Get-Content -Raw -Path "hugo.toml"
  Assert-True ($hugo -like "*https://visafact.org/*") "baseURL is set to visafact.org"
  Assert-True ($hugo -like '*theme = "PaperMod"*') "theme is PaperMod"
  Assert-True ($hugo -like '*name = "Checker"*') "menu includes Checker"
  Assert-True ($hugo -like '*url = "ui/"*') "checker menu uses relative url"
  Assert-True ($hugo -like '*pageRef = "posts"*') "menu uses pageRef for posts"
  Assert-True ($hugo -like '*pageRef = "methodology"*') "menu uses pageRef for methodology"
  Assert-True ($hugo -like '*pageRef = "disclaimer"*') "menu uses pageRef for disclaimer"
  Assert-True ($hugo -like '*pageRef = "affiliate-disclosure"*') "menu uses pageRef for affiliate disclosure"
}

Write-Host "Content checks..." -ForegroundColor Cyan
Assert-True (Test-Path "content/methodology/_index.md") "methodology section exists"
Assert-True (Test-Path "content/disclaimer/_index.md") "disclaimer section exists"
Assert-True (Test-Path "content/affiliate-disclosure/_index.md") "affiliate disclosure section exists"
Assert-True (Test-Path "content/posts/hello.md") "hello post exists"

Write-Host "Static sync checks..." -ForegroundColor Cyan
if (Test-Path "tools/sync_hugo_static.py") {
  $sync = Start-Process -FilePath "py" -ArgumentList "tools/sync_hugo_static.py" -Wait -PassThru
  Assert-True ($sync.ExitCode -eq 0) "sync_hugo_static.py runs successfully"
} else {
  Assert-True $false "sync_hugo_static.py exists"
}

Assert-True (Test-Path "static/ui/index.html") "static/ui/index.html exists"
Assert-True (Test-Path "static/data/ui_index.json") "static/data/ui_index.json exists"
Assert-True (Test-Path "static/sources/CR_Decreto_43619_2026-01-12.md") "static/sources contains snapshots"

if ($failed) {
  Write-Error "One or more checks failed."
  exit 1
}

Write-Host "All checks passed." -ForegroundColor Green
