#!/usr/bin/env bash
# Development utility: run lint, format check, and tests in one go.
# Usage: ./scripts/check.sh
set -euo pipefail

# Activate the virtual environment if it exists and isn't already active.
if [[ -z "${VIRTUAL_ENV:-}" && -f .venv/bin/activate ]]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi

echo "==> ruff check"
ruff check .

echo "==> ruff format --check"
ruff format --check .

echo "==> pytest"
python -m pytest

echo "All checks passed."
