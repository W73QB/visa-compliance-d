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
  & $cmd.Source -y pagefind --source $publicDir
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
} finally {
  Pop-Location
}
