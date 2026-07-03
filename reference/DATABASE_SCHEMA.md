# DATABASE_SCHEMA.md

> Version: 2.0
>
> This document defines the database architecture, schema design, naming conventions and persistence rules.
>
> Business rules are documented in `PROJECT_SPEC.md`.
>
> API contracts are documented in `API_REFERENCE.md`.

---

# Database Overview

Database Engine

```
PostgreSQL
```

ORM

```
SQLAlchemy Async
```

Migration Tool

```
Alembic
```

---

# Database Goals

The database should be:

- reliable;
- normalized;
- scalable;
- secure;
- performant;
- maintainable.

---

# Architecture

```
Application

↓

Service Layer

↓

Repository Layer

↓

SQLAlchemy

↓

PostgreSQL
```

Only repositories communicate with the database.

---

# Naming Conventions

Tables

```
snake_case
plural
```

Examples

```
events

participations

organizers

users

imports
```

---

Columns

```
snake_case
```

Examples

```
created_at

updated_at

start_date

event_type
```

---

Primary Keys

Every table should use

```
id
```

UUID or BIGINT depending on project requirements.

---

Foreign Keys

Use descriptive names.

Examples

```
event_id

user_id

organizer_id

import_id
```

---

Timestamp Fields

Every business table should contain:

```
created_at

updated_at
```

Soft-delete tables may additionally contain:

```
deleted_at
```

---

# Core Tables

Primary entities:

```
events

participations

organizers

users

imports
```

Reference tables may include:

```
event_categories

event_types

permissions

roles
```

---

# Relationships

Typical relationships:

```
Organizer

↓

Events

1:N
```

```
Event

↓

Participation

1:N
```

```
User

↓

Imports

1:N
```

Relationships should be enforced using foreign keys.

---

# Normalization

The schema should satisfy at least Third Normal Form (3NF).

Avoid:

- duplicated values;
- repeating groups;
- denormalized business data.

Denormalization should only be introduced for measured performance improvements.

---

# Constraints

Use database constraints whenever possible.

Supported constraints:

- PRIMARY KEY
- FOREIGN KEY
- UNIQUE
- CHECK
- NOT NULL

Business integrity should not rely solely on application code.

---

# Unique Constraints

Examples:

```
email

username

slug
```

Composite unique constraints may be used where appropriate.

---

# Foreign Keys

Foreign keys should enforce referential integrity.

Avoid orphan records.

Define explicit delete behavior.

Example:

```
CASCADE

RESTRICT

SET NULL
```

Choose behavior based on business requirements.

---

# Indexing

Indexes should exist for:

- primary keys;
- foreign keys;
- frequently filtered columns;
- search columns;
- ordering columns.

Avoid unnecessary indexes.

---

# Composite Indexes

Use composite indexes for common filtering patterns.

Example

```
(status, created_at)

(category, date)

(organizer_id, status)
```

Composite indexes should reflect real query patterns.

---

# Transactions

Every multi-step write operation should execute inside a transaction.

Examples:

- event creation;
- Excel import;
- bulk updates;
- user management.

Rollback immediately on failure.

---

# Views

Database views may be used for:

- reporting;
- dashboards;
- aggregated statistics.

Views should not replace business logic.

---

# Materialized Views

Materialized views may be used for:

- heavy statistics;
- reporting;
- dashboards.

Refresh strategy should be documented.

---

# Stored Functions

Database functions should be used only when database execution provides clear benefits.

Examples:

- aggregation;
- reporting;
- reusable SQL logic.

Avoid implementing business workflows inside SQL functions.

---

# Triggers

Triggers should remain minimal.

Appropriate use cases:

- timestamps;
- audit logging;
- derived values.

Avoid complex business logic inside triggers.

---

# Soft Delete

If soft delete is required:

```
deleted_at
```

should be preferred over boolean flags.

Application queries should exclude deleted records by default.

---

# Audit Data

Critical operations may be audited.

Audit records should contain:

- entity;
- operation;
- timestamp;
- actor;
- previous values (when applicable).

Audit history should be immutable.

---

# Backup Strategy

Backups should include:

- schema;
- data;
- migrations.

Backups should be verified periodically.

---

# Migration Strategy

Schema changes must be managed through Alembic.

Never modify production schema manually.

Every migration should be:

- reversible;
- deterministic;
- version-controlled.

---

# Database Security

Restrict direct database access.

Application credentials should use least privilege.

Never expose database credentials in source code.

---

# Performance Guidelines

Optimize:

- indexes;
- query plans;
- joins;
- pagination;
- filtering.

Avoid:

- SELECT \*
- N+1 queries
- unnecessary joins
- full table scans on large datasets

---

# Database Checklist

Before modifying the schema verify:

✓ Foreign keys defined

✓ Constraints applied

✓ Indexes created

✓ Migration generated

✓ Migration tested

✓ Queries optimized

✓ Naming conventions preserved

✓ Referential integrity maintained

---

# Entity Definitions

This section defines the logical database schema.

Field names may vary depending on implementation, but responsibilities should remain consistent.

---

# events

Purpose

Stores all university events.

---

## Columns

| Column            | Type          | Required | Description        |
| ----------------- | ------------- | -------- | ------------------ |
| id                | UUID / BIGINT | ✓        | Primary key        |
| title             | VARCHAR       | ✓        | Event title        |
| short_description | TEXT          |          | Short description  |
| description       | TEXT          | ✓        | Full description   |
| category_id       | FK            | ✓        | Event category     |
| organizer_id      | FK            | ✓        | Event organizer    |
| start_date        | DATE          | ✓        | Event date         |
| start_time        | TIME          |          | Start time         |
| end_time          | TIME          |          | End time           |
| location          | VARCHAR       | ✓        | Event location     |
| image_url         | TEXT          |          | Preview image      |
| registration_url  | TEXT          |          | Registration page  |
| status            | ENUM          | ✓        | Event status       |
| created_at        | TIMESTAMP     | ✓        | Creation timestamp |
| updated_at        | TIMESTAMP     | ✓        | Last modification  |

---

## Relationships

```
events

↓

participations

1:N
```

```
organizers

↓

events

1:N
```

---

## Indexes

Recommended indexes

```
(status)

(start_date)

(category_id)

(organizer_id)

(status, start_date)

(category_id, start_date)
```

---

## Constraints

- title NOT NULL
- category_id NOT NULL
- organizer_id NOT NULL
- start_date NOT NULL

---

# participations

Purpose

Stores visitor participation.

---

## Columns

| Column     | Type      | Required |
| ---------- | --------- | -------- |
| id         | UUID      | ✓        |
| event_id   | FK        | ✓        |
| session_id | VARCHAR   | ✓        |
| status     | ENUM      | ✓        |
| created_at | TIMESTAMP | ✓        |

---

## Constraints

Unique:

```
(event_id, session_id)
```

This prevents duplicate participation.

---

## Relationships

```
events

↓

participations

1:N
```

---

## Indexes

```
(event_id)

(session_id)

(status)

(event_id, status)
```

---

# organizers

Purpose

Stores event organizers.

---

## Columns

| Column     | Type      |
| ---------- | --------- |
| id         | UUID      |
| name       | VARCHAR   |
| department | VARCHAR   |
| email      | VARCHAR   |
| phone      | VARCHAR   |
| website    | VARCHAR   |
| created_at | TIMESTAMP |
| updated_at | TIMESTAMP |

---

## Relationships

```
organizers

↓

events

1:N
```

---

## Indexes

```
(name)

(department)
```

---

# users

Purpose

Stores authenticated users.

---

## Columns

| Column        | Type      |
| ------------- | --------- |
| id            | UUID      |
| username      | VARCHAR   |
| email         | VARCHAR   |
| password_hash | TEXT      |
| role_id       | FK        |
| is_active     | BOOLEAN   |
| created_at    | TIMESTAMP |
| updated_at    | TIMESTAMP |
| last_login    | TIMESTAMP |

---

## Constraints

Unique

```
username

email
```

---

## Relationships

```
roles

↓

users

1:N
```

---

## Indexes

```
(email)

(username)

(role_id)
```

---

# roles

Purpose

Stores application roles.

---

## Columns

| Column      | Type     |
| ----------- | -------- |
| id          | SMALLINT |
| name        | VARCHAR  |
| description | TEXT     |

---

Example roles

```
Administrator

Editor
```

---

# permissions

Purpose

Stores available permissions.

---

## Columns

| Column      | Type     |
| ----------- | -------- |
| id          | SMALLINT |
| name        | VARCHAR  |
| description | TEXT     |

---

# role_permissions

Purpose

Many-to-many relationship.

```
roles

↓

role_permissions

↓

permissions
```

---

# imports

Purpose

Stores Excel import history.

---

## Columns

| Column        | Type      |
| ------------- | --------- |
| id            | UUID      |
| filename      | VARCHAR   |
| imported_rows | INTEGER   |
| failed_rows   | INTEGER   |
| duration      | INTEGER   |
| status        | ENUM      |
| created_by    | FK        |
| created_at    | TIMESTAMP |

---

## Relationships

```
users

↓

imports

1:N
```

---

# Audit Tables

Recommended audit tables

```
audit_logs

login_history

import_logs
```

---

# Enumerations

Recommended enums

EventStatus

```
draft

published

completed

archived
```

ParticipationStatus

```
registered

confirmed

cancelled
```

ImportStatus

```
processing

completed

failed
```

UserRole

```
administrator

editor
```

---

# Common Fields

Every business table should include

```
id

created_at

updated_at
```

Soft-delete tables additionally include

```
deleted_at
```

---

# Schema Rules

Every table should:

- have a primary key;
- use foreign keys;
- contain timestamps;
- use indexes where appropriate;
- avoid duplicated data.

The schema should remain normalized.

---

# Naming Rules

Tables

```
plural

snake_case
```

Columns

```
snake_case
```

Foreign Keys

```
entity_id
```

Primary Keys

```
id
```

Timestamps

```
created_at

updated_at

deleted_at
```

The naming convention should remain consistent across the entire schema.

---

# SQL Best Practices

This section defines engineering standards for working with PostgreSQL.

These rules apply to all database operations.

---

# Query Philosophy

Database queries should be:

- predictable;
- efficient;
- indexed;
- maintainable;
- easy to review.

Correctness always has higher priority than optimization.

---

# SELECT Rules

Select only the required columns.

Good

```sql
SELECT id, title
FROM events;
```

Avoid

```sql
SELECT *
FROM events;
```

Fetching unnecessary data increases memory usage and network traffic.

---

# WHERE Clauses

Always filter using indexed columns whenever possible.

Good examples:

- id
- status
- created_at
- category_id

Avoid filtering on non-indexed large text columns.

---

# JOIN Strategy

Prefer explicit joins.

Good

```sql
INNER JOIN organizers
    ON organizers.id = events.organizer_id
```

Avoid unnecessary joins.

Join only the tables required for the current query.

---

# N+1 Queries

Avoid N+1 query patterns.

Bad

```
Load Events

↓

For every Event

↓

Load Organizer
```

Preferred

```
Load Events

↓

JOIN Organizer
```

Or use ORM eager loading.

---

# Pagination

Never return unlimited collections.

Use:

- LIMIT
- OFFSET

or

cursor pagination.

Example

```sql
LIMIT 20
OFFSET 0
```

---

# Ordering

Always define ordering for paginated queries.

Example

```sql
ORDER BY created_at DESC
```

Avoid relying on implicit ordering.

---

# Filtering

Filtering should happen inside SQL whenever practical.

Avoid filtering large collections in application code.

---

# Aggregation

Prefer database aggregation.

Good

```sql
COUNT()

SUM()

AVG()

MIN()

MAX()
```

Avoid loading large datasets solely to calculate aggregates.

---

# Transactions

Every business operation affecting multiple records should execute inside a transaction.

Typical examples:

- Excel import
- Bulk updates
- User creation
- Event publication

Either every operation succeeds or none of them do.

---

# Transaction Scope

Keep transactions as short as possible.

Avoid:

- external API calls;
- file processing;
- long computations;

inside transactions.

---

# Locking

Use row-level locking only when required.

Avoid unnecessary table locks.

Lock the smallest possible dataset.

---

# Isolation Levels

Use PostgreSQL default isolation unless stronger guarantees are required.

Increase isolation only when justified by business requirements.

---

# Index Strategy

Indexes should exist for:

- primary keys;
- foreign keys;
- frequently searched columns;
- ordering columns;
- filtering columns.

Review indexes periodically.

---

# Composite Indexes

Composite indexes should reflect actual query patterns.

Good examples

```
(status, created_at)

(category_id, start_date)

(organizer_id, status)
```

Avoid creating indexes that are never used.

---

# Partial Indexes

Consider partial indexes for frequently filtered subsets.

Example

```sql
WHERE status = 'published'
```

Only use after measuring performance.

---

# Full-Text Search

For large text searches prefer PostgreSQL Full-Text Search.

Avoid repeated LIKE queries on large datasets.

---

# Query Analysis

Analyze slow queries using

```sql
EXPLAIN
```

or

```sql
EXPLAIN ANALYZE
```

Optimization should always be based on measurements.

---

# Performance Guidelines

Prefer:

- indexed lookups;
- efficient joins;
- aggregation in SQL;
- pagination;
- batching.

Avoid:

- full table scans;
- nested loops on large datasets;
- repeated identical queries.

---

# Alembic Philosophy

Every schema modification must be performed through Alembic.

Never modify production schema manually.

---

# Migration Rules

Each migration should:

- perform one logical change;
- be reversible;
- be deterministic;
- preserve existing data.

Avoid combining unrelated schema changes.

---

# Migration Naming

Migration names should describe the change.

Good

```
create_events_table

add_event_status

create_import_history

add_indexes_to_participation
```

Avoid generic names.

---

# Upgrade

Upgrade scripts should:

- create new structures;
- migrate data when necessary;
- preserve compatibility.

---

# Downgrade

Every migration should support rollback whenever practical.

Rollback should restore the previous schema safely.

---

# Data Migrations

Separate schema migrations from large data migrations whenever possible.

Large data transformations should be repeatable.

---

# Schema Evolution

Prefer additive changes.

Examples

Good

- add column
- add table
- add index

Avoid destructive changes without migration planning.

---

# Constraint Management

Use constraints to enforce integrity.

Examples

- NOT NULL
- UNIQUE
- CHECK
- FOREIGN KEY

Application validation complements database constraints.

---

# ENUM Management

When using ENUM types:

- avoid unnecessary values;
- document changes;
- migrate carefully.

Changing ENUM values in production requires planning.

---

# Backup Before Migration

Before executing production migrations ensure:

- backup completed;
- rollback plan prepared;
- migration tested.

---

# Migration Checklist

Before applying a migration verify:

✓ Upgrade succeeds

✓ Downgrade succeeds

✓ Existing data preserved

✓ Constraints valid

✓ Indexes created

✓ Queries unaffected

✓ No breaking changes

---

# Database Performance Checklist

Before considering database work complete verify:

✓ No unnecessary SELECT \*

✓ Queries indexed

✓ Pagination implemented

✓ Foreign keys defined

✓ Constraints applied

✓ Transactions correct

✓ Slow queries analyzed

✓ Migrations tested

✓ Naming conventions preserved
