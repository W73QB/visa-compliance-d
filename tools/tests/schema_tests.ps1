$ErrorActionPreference = "Stop"
$failed = $false

function Assert-True {
  param(
    [Parameter(Mandatory = $true)][bool]$Condition,
    [Parameter(Mandatory = $true)][string]$Message
  )
  if (-not $Condition) { Write-Host "FAIL: $Message" -ForegroundColor Red; $script:failed = $true }
  else { Write-Host "PASS: $Message" -ForegroundColor Green }
}

$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Push-Location $root
try {
  $proc = Start-Process -FilePath "hugo" -ArgumentList @("--minify") -WorkingDirectory $root -Wait -PassThru
  Assert-True ($proc.ExitCode -eq 0) "hugo --minify runs"

  $htmlFiles = @()
  $htmlFiles += (Join-Path $root "public/index.html")
  $samplePosts = Get-ChildItem -Path (Join-Path $root "public/posts") -Directory |
    Where-Object { $_.Name -ne "page" }
  foreach ($samplePost in $samplePosts) {
    $htmlFiles += (Join-Path $samplePost.FullName "index.html")
  }
  $htmlFiles = $htmlFiles | Where-Object { Test-Path $_ }

  Assert-True ($htmlFiles.Count -gt 0) "Sample HTML files exist"

  $types = @{}
  $breadcrumbItems = @()
  foreach ($file in $htmlFiles) {
    $raw = Get-Content -Raw -Path $file
    $matches = Select-String -InputObject $raw -Pattern '(?s)<script type=["'']?application/ld\+json["'']?>(.*?)</script>' -AllMatches
    foreach ($m in $matches) {
      $json = $m.Matches.Groups[1].Value
      # handle cases where JSON-LD is wrapped/escaped
      if ($json.StartsWith('"') -and $json.EndsWith('"')) {
        $json = $json.Trim('"')
        $json = $json -replace '\\"','"'
      }
      try {
        $data = $json | ConvertFrom-Json
      } catch {
        Write-Host "FAIL: invalid JSON-LD in $file" -ForegroundColor Red
        $script:failed = $true
        continue
      }

      if ($data.'@graph') {
        foreach ($item in $data.'@graph') {
          if ($item.'@type') {
            foreach ($t in @($item.'@type')) { $types[$t] = $true }
          }
          if ($item.'@type' -eq "BreadcrumbList" -and $item.itemListElement) {
            $breadcrumbItems += @($item.itemListElement)
          }
        }
      } elseif ($data.'@type') {
        foreach ($t in @($data.'@type')) { $types[$t] = $true }
        if ($data.'@type' -eq "BreadcrumbList" -and $data.itemListElement) {
          $breadcrumbItems += @($data.itemListElement)
        }
      }
    }
  }

  Assert-True ($types.ContainsKey("WebSite")) "WebSite schema present"
  Assert-True ($types.ContainsKey("BreadcrumbList")) "BreadcrumbList schema present"
  $hasArticleType = ($types.ContainsKey("Article") -or $types.ContainsKey("BlogPosting"))
  if (-not $hasArticleType) {
    foreach ($file in $htmlFiles) {
      $raw = Get-Content -Raw -Path $file
      if ($raw -match '"@type"\s*:\s*"(Article|BlogPosting)"') {
        $hasArticleType = $true
        break
      }
    }
  }
  Assert-True $hasArticleType "Article/BlogPosting schema present"
  Assert-True ($types.ContainsKey("Organization") -or $types.ContainsKey("Person")) "Publisher schema present"
  Assert-True ($breadcrumbItems.Count -gt 0) "Breadcrumb schema has itemListElement entries"

  if ($breadcrumbItems.Count -gt 0) {
    $homeCrumb = $breadcrumbItems | Where-Object {
      $_.item -like "https://visafact.org/"
    }
    Assert-True ($null -ne $homeCrumb -and $homeCrumb.Count -ge 1) "Breadcrumb includes Home item"

    $positions = @($breadcrumbItems | ForEach-Object { [int]$_.position } | Sort-Object -Unique)
    $isSequential = $true
    for ($i = 0; $i -lt $positions.Count; $i++) {
      if ($positions[$i] -ne ($i + 1)) {
        $isSequential = $false
        break
      }
    }
    Assert-True $isSequential "Breadcrumb positions are sequential"
  }
  # FAQ only if page has faq; optional, so not asserted strictly

} finally {
  Pop-Location
}

if ($failed) { Write-Error "Schema tests failed."; exit 1 }
Write-Host "All checks passed." -ForegroundColor Green
