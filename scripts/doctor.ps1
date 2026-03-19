Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

Write-Host "Project:" (Get-Location)

if (-not (Test-Path ".\venv\Scripts\Activate.ps1")) {
  Write-Host "venv: missing (run scripts\setup.ps1)" -ForegroundColor Yellow
  exit 1
}

. .\venv\Scripts\Activate.ps1

Write-Host "python:" (python -c "import sys; print(sys.executable)")
Write-Host "pip:" (python -m pip -V)

try {
  $dj = python -c "import django; print(django.get_version())"
  Write-Host "django:" $dj
} catch {
  Write-Host "django: not installed" -ForegroundColor Red
}

try {
  $csv = python -c "import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE','netflix_dashboard.settings'); import django; django.setup(); from django.conf import settings; print(settings.NETFLIX_CSV_PATH)"
  Write-Host "NETFLIX_CSV_PATH:" $csv
  if (Test-Path $csv) {
    Write-Host "csv exists: yes"
  } else {
    Write-Host "csv exists: no" -ForegroundColor Yellow
  }
} catch {
  Write-Host "NETFLIX_CSV_PATH: unavailable (settings import failed)" -ForegroundColor Yellow
}

try {
  $listening = Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue | Select-Object -First 1
  if ($null -ne $listening) {
    Write-Host "port 8000: listening (pid $($listening.OwningProcess))"
  } else {
    Write-Host "port 8000: not listening"
  }
} catch {
  Write-Host "port 8000: check failed"
}
