.PHONY: dev prod test lint format migrate migrate-init db-shell logs clean build

dev:
	docker compose -f docker/docker-compose.yml -f docker/docker-compose.override.yml up --build

prod:
	docker compose -f docker/docker-compose.yml -f docker/docker-compose.prod.yml up -d

test:
	cd backend && .venv/bin/pytest --cov=app --cov-report=term-missing -v

lint:
	cd backend && .venv/bin/ruff check app/ tests/

format:
	cd backend && .venv/bin/ruff format app/ tests/

migrate:
	cd backend && .venv/bin/alembic upgrade head

migrate-init:
	cd backend && .venv/bin/alembic revision --autogenerate -m "$(msg)"

db-shell:
	docker compose -f docker/docker-compose.yml exec postgres psql -U postgres -d event_aggregator

logs:
	docker compose -f docker/docker-compose.yml logs -f

clean:
	./scripts/clean.sh

build:
	docker compose -f docker/docker-compose.yml build
