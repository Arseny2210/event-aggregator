#!/usr/bin/env bash
set -euo pipefail

echo "==> Formatting backend..."
cd backend
ruff format app/
cd ..

echo ""
echo "==> Formatting frontend..."
cd frontend
npx prettier --write "src/**/*.{ts,tsx,css}"
cd ..
