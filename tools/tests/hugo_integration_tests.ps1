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

Write-Host "Hugo config checks..." -ForegroundColor Cyan
Assert-True (Test-Path "hugo.toml") "hugo.toml exists"
if (Test-Path "hugo.toml") {
  $hugo = Get-Content -Raw -Path "hugo.toml"
  Assert-True ($hugo -like "*https://visafact.org/*") "baseURL is set to visafact.org"
  Assert-True ($hugo -like '*theme = "PaperMod"*') "theme is PaperMod"
  Assert-True ($hugo -like '*enableRobotsTXT = true*') "robots.txt generation enabled"
  Assert-True ($hugo -like '*canonifyURLs = true*') "canonical URLs enabled"
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

Write-Host "Indexability checks..." -ForegroundColor Cyan
$keyContent = @(
  "content/posts/spain-dnv-insurance/index.md",
  "content/posts/germany-freelance-insurance.md",
  "content/posts/thailand-dtv-insurance.md",
  "content/visas/spain/digital-nomad-visa/consulate-via-bls-london/index.md"
)
foreach ($p in $keyContent) {
  Assert-True (Test-Path $p) "$p exists"
  if (Test-Path $p) {
    $raw = Get-Content -Raw -Path $p
    Assert-True (-not ($raw -match '(?m)^robots:\s*noindex')) "$p is not marked noindex"
  }
}

Write-Host "Structured data checks..." -ForegroundColor Cyan
$schemaTemplate = "layouts/partials/templates/schema_json.html"
Assert-True (Test-Path $schemaTemplate) "schema_json template exists"
if (Test-Path $schemaTemplate) {
  $schemaText = Get-Content -Raw -Path $schemaTemplate
  Assert-True ($schemaText -match '"@type"\s*"FAQPage"') "FAQPage schema is defined"
  Assert-True ($schemaText -match '\.Params\.faq') "FAQ schema reads front matter faq"
  Assert-True ($schemaText -match 'if and \.question \.answer') "FAQ schema validates question and answer"
}

$faqPost = "content/posts/portugal-dnv-insurance.md"
Assert-True (Test-Path $faqPost) "reference FAQ post exists"
if (Test-Path $faqPost) {
  $faqText = Get-Content -Raw -Path $faqPost
  Assert-True ($faqText -match '(?m)^faq:' ) "reference post has faq front matter"
  Assert-True ($faqText -match '## FAQ') "reference post has visible FAQ section"
}

Write-Host "Static sync checks..." -ForegroundColor Cyan
if (Test-Path "tools/sync_hugo_static.py") {
  $sync = Start-Process -FilePath $python -ArgumentList "tools/sync_hugo_static.py" -Wait -PassThru
  Assert-True ($sync.ExitCode -eq 0) "sync_hugo_static.py runs successfully"
} else {
  Assert-True $false "sync_hugo_static.py exists"
}

Assert-True (Test-Path "static/ui/index.html") "static/ui/index.html exists"
Assert-True (Test-Path "static/data/ui_index.json") "static/data/ui_index.json exists"
Assert-True (Test-Path "static/sources/CR_Decreto_43619_2026-01-12.md") "static/sources contains snapshots"

Write-Host "SEO regression checks..." -ForegroundColor Cyan
Assert-True (Test-Path "content/templates/_index.md") "templates section control file exists"
if (Test-Path "content/templates/_index.md") {
  $templatesIndex = Get-Content -Raw -Path "content/templates/_index.md"
  Assert-True ($templatesIndex -match '(?m)^robotsNoIndex:\s*true') "templates section sets robotsNoIndex true"
  Assert-True ($templatesIndex -match '(?m)^sitemap:\s*$') "templates section declares sitemap block"
  Assert-True ($templatesIndex -match '(?m)^\s*disable:\s*true') "templates section disables sitemap"
  Assert-True ($templatesIndex -match '(?m)^build:\s*$') "templates section declares build block"
  Assert-True ($templatesIndex -match '(?m)^\s*render:\s*never') "templates section sets build.render never"
  Assert-True ($templatesIndex -match '(?m)^\s*list:\s*never') "templates section sets build.list never"
}

$hugoCmd = Get-Command hugo -ErrorAction SilentlyContinue
if ($hugoCmd) {
  $hugoBuild = Start-Process -FilePath $hugoCmd.Source -ArgumentList "--minify", "--cleanDestinationDir" -Wait -PassThru -NoNewWindow
  Assert-True ($hugoBuild.ExitCode -eq 0) "hugo clean build succeeds for SEO regression checks"

  Assert-True (-not (Test-Path "public/templates/index.html")) "templates section index is not rendered"
  Assert-True (-not (Test-Path "public/templates/page/1/index.html")) "templates pagination is not rendered"
  Assert-True (-not (Test-Path "public/templates/compliance-post-template/index.html")) "template detail page is not rendered"

  Assert-True (Test-Path "public/sitemap.xml") "public sitemap exists after clean build"
  if (Test-Path "public/sitemap.xml") {
    $sitemapRaw = Get-Content -Raw -Path "public/sitemap.xml"
    Assert-True ($sitemapRaw -notlike "*/templates/*") "sitemap excludes templates"
    Assert-True ($sitemapRaw -notlike "*/tags/*") "sitemap excludes tags"
    Assert-True ($sitemapRaw -notlike "*/categories/*") "sitemap excludes categories"
    Assert-True ($sitemapRaw -like "*https://visafact.org/ui/*") "sitemap includes /ui/"
  }
} else {
  Write-Host "SKIP: hugo command not available for rendered output regression checks" -ForegroundColor Yellow
}

if ($failed) {
  Write-Error "One or more checks failed."
  exit 1
}

Write-Host "All checks passed." -ForegroundColor Green
