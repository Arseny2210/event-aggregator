# Event Aggregator

A production-ready university events platform for discovering, managing, and participating in academic activities.

## Architecture

```
Frontend (Next.js)  →  REST API  →  Backend (FastAPI)  →  PostgreSQL
                                                                  ↑
                                                              Redis
                                                                  ↑
                                                            Celery Workers
```

## Repository Structure

```
frontend/     — Next.js application (App Router, TypeScript, Tailwind CSS)
backend/      — FastAPI application (Python, SQLAlchemy Async, Pydantic v2)
docs/         — Project specification and design documents
reference/    — API reference, database schema, test cases
docker/       — Dockerfiles and Docker Compose configuration
scripts/      — Development and utility scripts
.github/      — CI/CD workflows
```

## Quickstart

See `docs/DEPLOYMENT.md` for detailed setup instructions.

```sh
# Development setup
./scripts/setup.sh
./scripts/dev.sh
```

## Documentation

- `docs/PROJECT_SPEC.md` — Full project specification
- `docs/ENGINEERING.md` — Engineering standards
- `docs/DESIGN.md` — UI/UX design guidelines
- `docs/DEPLOYMENT.md` — Deployment and infrastructure
- `reference/API_REFERENCE.md` — REST API contracts
- `reference/DATABASE_SCHEMA.md` — Database schema
- `reference/TEST_CASES.md` — Testing strategy
- `CLAUDE.md` — AI agent operating instructions
