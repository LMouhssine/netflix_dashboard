Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

param(
  [string]$Path = ""
)

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

. .\venv\Scripts\Activate.ps1

if ([string]::IsNullOrWhiteSpace($Path)) {
  python manage.py import_netflix
} else {
  python manage.py import_netflix --path $Path
}
