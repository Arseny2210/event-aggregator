# DEPLOYMENT.md

> Version: 2.0
>
> This document defines deployment, infrastructure and production requirements.
>
> Application architecture is documented in `PROJECT_SPEC.md`.
>
> Engineering standards are documented in `ENGINEERING.md`.

---

# Deployment Philosophy

The deployment process must be:

- reproducible;
- automated;
- predictable;
- secure;
- environment-independent.

Production deployments should require minimal manual intervention.

---

# Supported Environments

The project supports the following environments:

- local
- development
- staging
- production

Every environment should behave consistently.

Configuration should be the only difference.

---

# Infrastructure Overview

The recommended production infrastructure is:

```
Internet

↓

Nginx

↓

Frontend (Next.js)

↓

Backend (FastAPI)

↓

Redis

↓

PostgreSQL

↓

Background Workers
```

Each service should remain independently deployable.

---

# Containerization

Every service should run inside Docker.

Typical containers:

- frontend
- backend
- postgres
- redis
- worker
- nginx

Services should communicate through internal Docker networking.

---

# Docker Principles

Containers should be:

- stateless;
- isolated;
- reproducible;
- lightweight.

Avoid storing persistent application data inside containers.

---

# Docker Compose

Docker Compose is recommended for:

- local development;
- testing;
- staging environments.

Production deployments may use Docker Compose or container orchestration platforms.

---

# Environment Variables

Configuration must use environment variables.

Typical configuration includes:

- database connection;
- Redis connection;
- JWT secrets;
- API URLs;
- upload paths;
- logging configuration.

Secrets must never be committed.

---

# Secrets Management

Secrets include:

- JWT_SECRET
- DATABASE_URL
- REDIS_URL
- API_KEYS
- SMTP_PASSWORD

Secrets must be managed outside the repository.

---

# Static Assets

Static assets should be served efficiently.

Prefer:

- CDN
- browser caching
- compression

Avoid unnecessary asset duplication.

---

# File Storage

Application uploads should be stored outside the application container.

Possible storage:

- local volume
- object storage
- cloud storage

Containers should remain disposable.

---

# Reverse Proxy

Nginx is responsible for:

- HTTPS
- compression
- caching
- request forwarding
- static asset delivery

Business logic must never exist inside the proxy.

---

# HTTPS

Production deployments must use HTTPS.

HTTP should redirect automatically to HTTPS.

TLS certificates should be renewed automatically whenever possible.

---

# Logging

Application logs should remain structured.

Log categories include:

- application
- access
- errors
- background workers

Logs should never contain sensitive information.

---

# Monitoring

Production monitoring should include:

- application health;
- response time;
- error rate;
- worker status;
- database status;
- storage usage.

---

# Health Checks

Every service should expose a health endpoint.

Health checks should verify:

- service availability;
- database connection;
- Redis connection;
- required dependencies.

---

# Backups

Regular backups should include:

- PostgreSQL
- uploaded files
- configuration (where appropriate)

Backups should be tested periodically.

---

# Deployment Checklist

Before deployment verify:

- build succeeds;
- tests pass;
- migrations are ready;
- environment variables are configured;
- secrets are available;
- health checks pass.

---

# Rollback Strategy

Every deployment should support rollback.

Rollback should:

- restore previous application version;
- preserve user data;
- restore service availability quickly.

---

# Production Checklist

Production deployments require:

✓ HTTPS enabled

✓ Environment configured

✓ Secrets configured

✓ Database migrations completed

✓ Health checks available

✓ Logging enabled

✓ Monitoring enabled

✓ Backups configured

✓ Error tracking enabled

✓ Successful smoke tests

Deployment is complete only after all checks pass.
