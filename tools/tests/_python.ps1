function Get-PythonLauncher {
  $candidates = @("py", "python3", "python")
  foreach ($c in $candidates) {
    if (Get-Command $c -ErrorAction SilentlyContinue) { return $c }
  }
  throw "python launcher not found (tried: py, python3, python)"
}
