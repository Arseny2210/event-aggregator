#!/usr/bin/env bash
set -euo pipefail

COMPOSE_FILES="-f docker/docker-compose.yml -f docker/docker-compose.prod.yml"

echo "==> Pulling latest images..."
docker compose $COMPOSE_FILES pull

echo "==> Running database migrations..."
docker compose $COMPOSE_FILES run --rm migrate

echo "==> Starting services..."
docker compose $COMPOSE_FILES up -d --remove-orphans

echo "==> Waiting for health checks..."
sleep 10

echo "==> Verifying health..."
curl -sf http://localhost/health || echo "WARNING: Health check failed"

echo "==> Deployment complete"
