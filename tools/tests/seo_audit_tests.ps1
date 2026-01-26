$ErrorActionPreference = "Stop"
$root = (Resolve-Path "$PSScriptRoot/../..").Path

$proc = Start-Process -FilePath "py" -ArgumentList "tools/seo_audit.py --config tools/seo_thresholds.json" -WorkingDirectory $root -Wait -PassThru -NoNewWindow

if ($proc.ExitCode -ne 0) {
  throw "seo_audit failed (expected to fail before content updates)"
}
