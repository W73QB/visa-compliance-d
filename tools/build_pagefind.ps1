$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$publicDir = Join-Path $root "public"

if (-not (Test-Path $publicDir)) {
  Write-Error "public/ not found. Run Hugo build first."
  exit 1
}

$cmd = Get-Command npx -ErrorAction SilentlyContinue
if (-not $cmd) {
  Write-Error "npx not found. Install Node.js to run Pagefind."
  exit 1
}

Push-Location $root
try {
  # Exclude evidence copies from index by ignoring their DOM via selectors
  & $cmd.Source -y pagefind --site $publicDir --exclude-selectors "#evidence-sources,.vf-evidence"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
} finally {
  Pop-Location
}
