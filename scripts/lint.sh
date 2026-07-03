#!/usr/bin/env bash
set -euo pipefail

echo "==> Linting backend..."
cd backend
ruff check app/
cd ..

echo ""
echo "==> Linting frontend..."
cd frontend
npx eslint src/
cd ..
