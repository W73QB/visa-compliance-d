$ErrorActionPreference = "Stop"
$root = (Resolve-Path "$PSScriptRoot/../..").Path

$python = "py"
if (-not (Get-Command $python -ErrorAction SilentlyContinue)) {
  if (Get-Command "python3" -ErrorAction SilentlyContinue) {
    $python = "python3"
  } elseif (Get-Command "python" -ErrorAction SilentlyContinue) {
    $python = "python"
  } else {
    throw "python launcher not found (tried: py, python3, python)"
  }
}

$proc = Start-Process -FilePath $python -ArgumentList "tools/seo_audit.py --config tools/seo_thresholds.json" -WorkingDirectory $root -Wait -PassThru -NoNewWindow

if ($proc.ExitCode -ne 0) {
  throw "seo_audit failed (expected to pass)"
}
