#!/usr/bin/env bash
set -euo pipefail

echo "==> Installing frontend dependencies..."
cd frontend
npm install
cd ..

echo "==> Setting up Python virtual environment..."
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cd ..

echo "==> Copying environment templates..."
if [ ! -f backend/.env ]; then
    cp backend/.env.example backend/.env
    echo "    Created backend/.env"
fi
if [ ! -f frontend/.env.local ]; then
    cp frontend/.env.example frontend/.env.local
    echo "    Created frontend/.env.local"
fi

echo "==> Setup complete"
