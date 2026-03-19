#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

source venv/bin/activate

if [ $# -eq 0 ]; then
  python manage.py import_netflix
else
  python manage.py import_netflix --path "$1"
fi
