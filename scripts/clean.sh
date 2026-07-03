#!/usr/bin/env bash
set -euo pipefail

echo "==> Cleaning backend artifacts..."
find backend -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find backend -type f -name "*.pyc" -delete
rm -rf backend/.venv
rm -rf backend/*.egg-info

echo "==> Cleaning frontend artifacts..."
rm -rf frontend/.next
rm -rf frontend/node_modules

echo "==> Clean complete"
