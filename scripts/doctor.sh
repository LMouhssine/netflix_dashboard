#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo "Project: $PWD"

if [ ! -f venv/bin/activate ]; then
  echo "venv: missing (run ./scripts/setup.sh)" >&2
  exit 1
fi

source venv/bin/activate

echo -n "python: "; python -c "import sys; print(sys.executable)"
echo -n "pip: "; python -m pip -V
echo -n "django: "; python -c "import django; print(django.get_version())" || echo "not installed"
echo -n "NETFLIX_CSV_PATH: "; python -c "import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE','netflix_dashboard.settings'); import django; django.setup(); from django.conf import settings; print(settings.NETFLIX_CSV_PATH)" || true
