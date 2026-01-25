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
  $htmlFiles += (Join-Path $root "public/posts/hello/index.html")
  $htmlFiles = $htmlFiles | Where-Object { Test-Path $_ }

  Assert-True ($htmlFiles.Count -gt 0) "Sample HTML files exist"

  $types = @{}
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
        }
      } elseif ($data.'@type') {
        foreach ($t in @($data.'@type')) { $types[$t] = $true }
      }
    }
  }

  Assert-True ($types.ContainsKey("WebSite")) "WebSite schema present"
  Assert-True ($types.ContainsKey("BreadcrumbList")) "BreadcrumbList schema present"
  Assert-True ($types.ContainsKey("Article") -or $types.ContainsKey("BlogPosting")) "Article/BlogPosting schema present"
  Assert-True ($types.ContainsKey("Organization") -or $types.ContainsKey("Person")) "Publisher schema present"
  # FAQ only if page has faq; optional, so not asserted strictly

} finally {
  Pop-Location
}

if ($failed) { Write-Error "Schema tests failed."; exit 1 }
Write-Host "All checks passed." -ForegroundColor Green
