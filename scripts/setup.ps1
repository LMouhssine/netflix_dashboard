Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
  throw "Python not found on PATH. Install Python 3 and restart the terminal."
}

if (-not (Test-Path ".\venv\Scripts\Activate.ps1")) {
  python -m venv venv
}

. .\venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if (-not (Test-Path ".\.env")) {
  Copy-Item ".\.env.example" ".\.env"
  Write-Host "Created .env from .env.example"
}

python manage.py migrate
Write-Host "Setup complete. Next: scripts\run.ps1"
