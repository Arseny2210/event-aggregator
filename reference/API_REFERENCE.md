# API_REFERENCE.md

> Version: 2.0
>
> This document defines the REST API contract.
>
> It contains endpoint specifications, request/response formats, authentication requirements and error handling.
>
> Business logic is documented in `PROJECT_SPEC.md`.

---

# API Principles

The REST API is the only communication channel between the frontend and backend.

Clients must never access the database directly.

Every endpoint must return predictable responses.

---

# Base URL

```
/api/v1
```

All endpoints should be versioned.

---

# Request Format

Request body:

```
JSON
```

File uploads:

```
multipart/form-data
```

Query parameters:

```
URL Query
```

---

# Response Format

Successful response

```json
{
	"success": true,
	"data": {},
	"meta": {}
}
```

---

Error response

```json
{
	"success": false,
	"error": {
		"code": "VALIDATION_ERROR",
		"message": "Validation failed."
	}
}
```

The response format should remain consistent across the entire API.

---

# Authentication

Protected endpoints require:

```
Authorization

Bearer <JWT_TOKEN>
```

Public endpoints do not require authentication.

---

# HTTP Status Codes

Common responses:

```
200 OK

201 Created

204 No Content

400 Bad Request

401 Unauthorized

403 Forbidden

404 Not Found

409 Conflict

422 Validation Error

500 Internal Server Error
```

---

# Resource Naming

Resources use plural nouns.

Examples:

```
/events

/organizers

/imports

/users

/statistics
```

Avoid verbs in endpoint names.

---

# REST Conventions

Create

```
POST /events
```

Read

```
GET /events
```

Read One

```
GET /events/{id}
```

Update

```
PUT /events/{id}
```

Partial Update

```
PATCH /events/{id}
```

Delete

```
DELETE /events/{id}
```

---

# Pagination

Collection endpoints support:

```
?page=

&page_size=

&sort=

&order=
```

Large datasets must always be paginated.

---

# Filtering

Collections may support:

```
category

date

status

search

organizer

type
```

Filters should be combinable.

---

# Sorting

Supported sorting:

```
date

title

created_at

updated_at

popularity
```

---

# API Versioning

All public APIs must remain versioned.

Current version:

```
v1
```

Breaking changes require a new version.

---

# Endpoint Categories

The API is organized into the following domains:

- Authentication
- Events
- Participation
- Organizers
- Statistics
- Imports
- Administration

---

# Authentication API

## Login

```
POST /auth/login
```

Purpose:

Authenticate user.

---

## Logout

```
POST /auth/logout
```

Purpose:

Terminate session.

---

## Refresh Token

```
POST /auth/refresh
```

Purpose:

Issue a new access token.

---

## Current User

```
GET /auth/me
```

Purpose:

Return authenticated user information.

---

# Events API

## List Events

```
GET /events
```

Returns paginated event collection.

Supports:

- filtering
- sorting
- pagination
- search

---

## Get Event

```
GET /events/{id}
```

Returns a single event.

---

## Create Event

```
POST /events
```

Authentication required.

---

## Update Event

```
PUT /events/{id}
```

Authentication required.

---

## Partial Update

```
PATCH /events/{id}
```

Authentication required.

---

## Delete Event

```
DELETE /events/{id}
```

Authentication required.

---

# Participation API

## Register

```
POST /events/{id}/participation
```

Creates participation.

Duplicate registrations are prohibited.

---

## Cancel Participation

```
DELETE /events/{id}/participation
```

Removes participation.

---

## Participation Statistics

```
GET /events/{id}/participation
```

Returns participation statistics.

---

# Organizer API

## List Organizers

```
GET /organizers
```

---

## Get Organizer

```
GET /organizers/{id}
```

---

## Create Organizer

```
POST /organizers
```

---

## Update Organizer

```
PUT /organizers/{id}
```

---

## Delete Organizer

```
DELETE /organizers/{id}
```

---

# Import API

## Upload Excel

```
POST /imports
```

Accepts:

```
multipart/form-data
```

---

## Import History

```
GET /imports
```

Returns import history.

---

## Import Report

```
GET /imports/{id}
```

Returns detailed import results.

---

# Statistics API

## Dashboard Statistics

```
GET /statistics
```

Returns application statistics.

---

## Event Statistics

```
GET /statistics/events
```

---

## Participation Statistics

```
GET /statistics/participation
```

---

# Administration API

Administrative endpoints require administrator privileges.

Examples:

```
GET /admin/users

POST /admin/users

PUT /admin/users/{id}

DELETE /admin/users/{id}
```

---

# Validation Errors

Validation errors should identify:

- field
- rule
- message

Example

```json
{
	"success": false,
	"error": {
		"code": "VALIDATION_ERROR",
		"fields": [
			{
				"field": "title",
				"message": "Title is required."
			}
		]
	}
}
```

---

# Error Codes

Standard error codes:

```
VALIDATION_ERROR

UNAUTHORIZED

FORBIDDEN

NOT_FOUND

CONFLICT

FILE_UPLOAD_ERROR

IMPORT_ERROR

INTERNAL_ERROR
```

---

# API Guarantees

Every endpoint must:

- validate input;
- enforce authorization;
- return consistent responses;
- return DTOs only;
- never expose database models.

---

# API Design Rules

Always:

- use REST conventions;
- return meaningful HTTP status codes;
- paginate collections;
- validate requests;
- keep responses predictable.

Never:

- expose internal exceptions;
- expose SQL errors;
- expose stack traces;
- return ORM models.
