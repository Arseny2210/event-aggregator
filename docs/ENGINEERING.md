# ENGINEERING.md

> Version: 2.0
>
> This document defines the engineering standards for the entire project.
>
> Every implementation must comply with these rules.
>
> Project architecture is defined in `PROJECT_SPEC.md`.
>
> UI rules are defined in `DESIGN.md`.
>
> API contracts are defined in `reference/API_REFERENCE.md`.

---

# 1. Engineering Philosophy

The primary objective is to produce production-ready software.

Every implementation should prioritize:

1. Correctness
2. Simplicity
3. Maintainability
4. Security
5. Readability
6. Performance

Never sacrifice maintainability for short-term convenience.

---

# Core Principles

The project follows these engineering principles:

- Single Responsibility Principle (SRP)
- Open/Closed Principle (OCP)
- Liskov Substitution Principle (LSP)
- Interface Segregation Principle (ISP)
- Dependency Inversion Principle (DIP)
- DRY (Don't Repeat Yourself)
- KISS (Keep It Simple)
- YAGNI (You Aren't Gonna Need It)

---

# General Rules

Every implementation must be:

- deterministic;
- readable;
- testable;
- reusable;
- explicit;
- strongly typed.

Avoid hidden behavior.

Avoid unnecessary abstraction.

Avoid overengineering.

---

# Development Mindset

Before writing code:

- understand the problem;
- inspect the existing implementation;
- identify reusable logic;
- minimize the scope of changes.

Never start coding without understanding the surrounding codebase.

---

# Code Quality Standards

Good code is:

- easy to understand;
- easy to modify;
- easy to test;
- easy to review.

Code should optimize for future maintainability rather than minimal line count.

---

# Single Responsibility

Every module should have exactly one reason to change.

Examples:

Good:

```
EventService

EventRepository

EventValidator
```

Bad:

```
EventService

↓

validation

↓

authentication

↓

logging

↓

database

↓

notifications
```

Large multi-purpose modules should be split.

---

# Separation of Concerns

Separate:

- presentation;
- business logic;
- persistence;
- infrastructure.

Each concern belongs to exactly one layer.

---

# Reuse Before Creation

Before creating new code, always search for:

- components;
- hooks;
- services;
- repositories;
- utilities;
- validators;
- DTOs;
- schemas.

If a suitable implementation already exists:

Reuse it.

Never duplicate functionality.

---

# Incremental Changes

Prefer extending existing implementations over rewriting them.

Small changes are easier to:

- review;
- test;
- maintain;
- debug.

Avoid unnecessary rewrites.

---

# Predictability

Code should behave exactly as expected.

Avoid:

- implicit behavior;
- hidden side effects;
- unexpected mutations;
- surprising APIs.

---

# Explicitness

Prefer explicit code over clever code.

Good:

```
const isPublished = event.status === "published";
```

Avoid:

```
if (!!event?.status?.length)
```

Readable code is preferred.

---

# Strong Typing

Always use explicit types.

Avoid:

- any
- unknown (unless necessary)
- implicit typing in public APIs

Types should describe business intent.

---

# Immutability

Prefer immutable data structures.

Avoid mutating existing objects whenever possible.

Prefer:

```
return {
    ...event,
    title
};
```

Instead of:

```
event.title = title;
```

---

# Composition

Prefer composition over inheritance.

Reusable functions are preferred over large base classes.

---

# Pure Functions

Whenever possible, functions should:

- have deterministic output;
- avoid side effects;
- avoid global state.

Pure functions are easier to test.

---

# Naming

Names should clearly describe responsibility.

Good:

```
createEvent()

updateEvent()

deleteEvent()

validateImport()
```

Avoid vague names.

Bad:

```
process()

handle()

doWork()

execute()
```

---

# Consistency

The same concept should always use the same naming.

Example:

If "Event" is used everywhere,

do not introduce:

- Activity
- Meeting
- Record
- Entry

for the same entity.

Consistency improves maintainability.

---

# Simplicity

Choose the simplest solution that fully satisfies the requirements.

Avoid designing for hypothetical future problems.

---

# Engineering Decision Order

Whenever multiple solutions exist, choose according to:

1. Correctness
2. Simplicity
3. Maintainability
4. Readability
5. Performance

Never optimize performance before correctness.

---

# Definition of Good Engineering

A solution is considered good when it is:

- correct;
- maintainable;
- testable;
- understandable;
- reusable;
- consistent with the architecture.

If one of these conditions is missing,

the solution should be reconsidered.

---

# 2. Repository Structure

The repository must remain predictable.

Every directory should have a single responsibility.

The project should be easy to navigate without additional documentation.

---

# Root Structure

```
frontend/
backend/

docs/
reference/

docker/
nginx/

.github/
```

The repository root should contain only top-level modules and project configuration.

Avoid placing implementation files in the root directory.

---

# Frontend Structure

```
app/

components/

features/

hooks/

services/

stores/

schemas/

types/

utils/

styles/

assets/
```

Every directory has a clearly defined purpose.

---

# Backend Structure

```
api/

routers/

services/

repositories/

models/

schemas/

core/

middleware/

dependencies/

tasks/

utils/

database/

tests/
```

Business logic must remain independent from infrastructure.

---

# Documentation Structure

```
docs/

PROJECT_SPEC.md

ENGINEERING.md

DESIGN.md

DEPLOYMENT.md
```

Reference documentation belongs in:

```
reference/

API_REFERENCE.md

DATABASE_SCHEMA.md

TEST_CASES.md
```

---

# Feature Organization

Business functionality should be grouped by feature rather than file type whenever practical.

Example:

```
features/

event/

calendar/

participation/

admin/
```

Each feature may contain:

- components;
- hooks;
- services;
- schemas;
- types;
- tests.

---

# Directory Responsibilities

Every directory should have one purpose.

Example:

components/

↓

Reusable UI

hooks/

↓

Custom React hooks

services/

↓

API communication

stores/

↓

Client state

utils/

↓

Generic utilities

types/

↓

Shared types

schemas/

↓

Validation

---

# Module Size

Small modules are preferred.

If a file becomes difficult to understand,

split it.

Recommended limits:

- Components ≈ 300 lines
- Hooks ≈ 200 lines
- Services ≈ 300 lines
- Utilities ≈ 150 lines

These are guidelines rather than hard limits.

---

# File Naming

Use descriptive names.

Good:

```
event-service.ts

calendar-grid.tsx

create-event.ts

event-validator.ts
```

Avoid:

```
helpers.ts

utils2.ts

temp.ts

new.ts
```

Names should describe responsibility.

---

# Component Naming

React components use PascalCase.

Example:

```
EventCard

CalendarGrid

ImportDialog

ParticipationButton
```

One component per file.

---

# Hook Naming

Hooks always start with:

```
use
```

Examples:

```
useEvents

useCalendar

useFilters

useParticipation
```

Hooks should expose a clean public API.

---

# Service Naming

Services describe business actions.

Examples:

```
event.service.ts

import.service.ts

statistics.service.ts
```

Services should never represent UI behavior.

---

# Utility Naming

Utilities should describe exactly what they do.

Examples:

```
format-date.ts

generate-slug.ts

sort-events.ts

validate-file.ts
```

Avoid generic utility files.

---

# Type Organization

Shared business types belong in:

```
types/
```

Feature-specific types remain inside the feature.

Avoid global types unless genuinely shared.

---

# Schema Organization

Validation schemas belong in:

```
schemas/
```

Feature-specific schemas remain inside the feature.

Validation should never be scattered across multiple locations.

---

# Imports

Prefer absolute imports whenever supported.

Group imports in the following order:

1. External libraries

2. Internal shared modules

3. Feature modules

4. Relative imports

Separate groups with a blank line.

---

# Import Rules

Never import across unrelated features.

Dependencies should always move toward lower layers.

Example:

Good

```
Feature

↓

Shared Component
```

Avoid

```
Feature A

↓

Feature B

↓

Feature C
```

Independent features should remain isolated.

---

# Circular Dependencies

Circular imports are prohibited.

The dependency graph should remain acyclic.

If circular dependencies appear,

extract shared logic into a common module.

---

# Shared Code

Only place code inside shared directories when multiple features genuinely use it.

Avoid creating "shared" modules prematurely.

---

# Configuration Files

Configuration should remain centralized.

Examples:

```
.env

tsconfig.json

eslint.config.js

tailwind.config.ts

next.config.ts
```

Avoid duplicating configuration across modules.

---

# Environment Variables

Environment variables should be accessed through centralized configuration modules.

Never access process.env directly throughout the application.

---

# Assets

Assets should be organized by type.

Example:

```
assets/

images/

icons/

fonts/
```

Large media files should not be committed unless necessary.

---

# Static Files

Public assets belong in:

```
public/
```

Avoid mixing generated and static resources.

---

# Temporary Files

Temporary files should never be committed.

Examples:

- logs
- cache
- generated exports
- uploaded temporary files

Use `.gitignore` appropriately.

---

# Repository Cleanliness

The repository should never contain:

- unused files;
- duplicate implementations;
- obsolete modules;
- experimental code;
- commented-out production code.

Remove unused code instead of hiding it.

---

# File Creation Checklist

Before creating a new file ask:

- Does a similar file already exist?
- Can an existing file be extended?
- Can logic be extracted instead?
- Will another developer immediately understand why this file exists?

If the answer is "no",

do not create the file.

---

# Repository Goals

The repository should always remain:

- organized;
- predictable;
- discoverable;
- maintainable;
- scalable.

Every engineer should understand the project structure without additional explanation.

---

# 3. Frontend Engineering Rules

This section defines mandatory engineering standards for the frontend application.

Every frontend implementation must comply with these rules.

---

# General Principles

Frontend code must be:

- predictable;
- reusable;
- maintainable;
- strongly typed;
- accessible;
- performant.

Avoid unnecessary complexity.

---

# Single Responsibility

Each component should solve one problem.

Good:

```
EventCard

CalendarGrid

ImportDialog
```

Avoid:

```
Dashboard

↓

Calendar

↓

Statistics

↓

Modal

↓

Settings

↓

API Requests

↓

Forms
```

Large components should be decomposed.

---

# Component Responsibilities

Components are responsible only for:

- rendering;
- user interaction;
- event handling.

Components must never:

- implement business logic;
- communicate directly with databases;
- perform authorization;
- duplicate backend validation.

---

# Component Size

Prefer small components.

Recommended size:

- UI Component: ≤ 200 lines
- Feature Component: ≤ 300 lines

If a component becomes difficult to understand,

split it.

---

# Component Composition

Prefer composing small components.

Good

```
EventPage

↓

EventHeader

↓

EventContent

↓

ParticipationSection

↓

RelatedEvents
```

Avoid one component rendering an entire application page.

---

# Server Components

Use Server Components whenever possible.

Server Components should:

- fetch initial data;
- render static content;
- reduce JavaScript bundle size.

Avoid unnecessary Client Components.

---

# Client Components

Use Client Components only when interaction is required.

Examples:

- forms;
- dialogs;
- dropdowns;
- animations;
- drag & drop.

Everything else should remain server-side.

---

# Custom Hooks

Move reusable logic into hooks.

Hooks may contain:

- state;
- effects;
- API interaction;
- derived values.

Hooks must not render UI.

---

# Hook Rules

A hook should expose a simple API.

Good

```
const {

events,

loading,

error,

refresh

} = useEvents();
```

Avoid exposing implementation details.

---

# React State

Keep component state minimal.

State should represent:

- UI state;
- temporary input;
- interaction state.

Derived values should not be stored.

---

# Derived State

Prefer computed values.

Good

```
const activeEvents =
events.filter(...)
```

Avoid storing duplicated state.

---

# Global State

Only truly global data belongs inside Zustand.

Examples:

- theme;
- sidebar;
- preferences;
- current user;
- active filters.

Avoid storing server responses globally.

---

# React Query

All server state belongs inside React Query.

Examples:

- events;
- organizers;
- statistics;
- imports.

Never duplicate query data inside Zustand.

---

# Mutations

Mutations should use React Query.

Every mutation should:

- invalidate affected queries;
- handle loading;
- handle errors;
- return normalized data.

---

# Forms

Every form should use:

- React Hook Form
- Zod

Validation rules should match backend validation.

---

# Validation

Client validation improves UX.

Backend validation guarantees correctness.

Never rely solely on frontend validation.

---

# API Communication

Components must never call fetch() directly.

Always use:

```
Component

↓

Hook

↓

Service

↓

API Client
```

Every HTTP request passes through the API layer.

---

# Side Effects

Side effects belong inside:

- hooks;
- effects;
- services.

Avoid side effects during rendering.

---

# Rendering

Rendering should remain deterministic.

The same props should always produce the same UI.

Avoid random behavior.

---

# Conditional Rendering

Prefer explicit conditions.

Good

```
if (!event) return null;
```

Avoid deeply nested ternary operators.

---

# Lists

Every rendered list requires stable keys.

Never use array index when a stable identifier exists.

---

# Keys

Good

```
key={event.id}
```

Avoid

```
key={index}
```

---

# Memoization

Use memoization only when profiling demonstrates benefit.

Avoid premature optimization.

---

# Effects

Every effect should have a clear purpose.

Effects should never synchronize duplicated state.

Avoid unnecessary useEffect.

If logic can be calculated during rendering,

do not use an effect.

---

# Styling

Use Tailwind utility classes.

Avoid inline styles.

Avoid duplicated utility combinations.

Frequently reused styles should become reusable components.

---

# Responsive Design

Design mobile-first.

Support:

- mobile;
- tablet;
- desktop.

Avoid fixed dimensions whenever possible.

---

# Images

Always optimize images.

Prefer:

- next/image
- lazy loading
- responsive sizes

Avoid large unoptimized assets.

---

# Accessibility

Interactive elements must support:

- keyboard navigation;
- focus indicators;
- semantic HTML;
- screen readers.

Buttons must remain buttons.

Links must remain links.

---

# Error Boundaries

Unexpected rendering failures should not crash the entire application.

Use Error Boundaries where appropriate.

---

# Loading States

Every async operation should provide visual feedback.

Examples:

- Skeleton
- Spinner
- Progress Bar

Never leave users without feedback.

---

# Empty States

Every collection should support an empty state.

Examples:

- no events;
- no search results;
- no statistics.

Avoid blank screens.

---

# Performance

Reduce unnecessary renders.

Prefer:

- lazy loading;
- code splitting;
- streaming;
- server rendering;
- image optimization.

Optimize only after measuring.

---

# TypeScript

Never use:

```
any
```

Avoid:

```
ts-ignore
```

Prefer explicit interfaces.

Types should describe business concepts.

---

# File Organization

One component per file.

One hook per file.

One responsibility per module.

Avoid utility files containing unrelated functions.

---

# Code Duplication

If logic appears twice,

extract it.

Prefer shared hooks and reusable components.

---

# Frontend Checklist

Before completing any frontend task verify:

- component responsibility is clear;
- no business logic inside UI;
- no duplicated state;
- no direct fetch();
- React Query used correctly;
- Zustand used only for client state;
- forms validated;
- types complete;
- responsive layout works;
- accessibility preserved;
- unnecessary renders avoided.

---

# 4. Backend Engineering Rules

This section defines mandatory engineering standards for the backend application.

All backend code must comply with these rules.

---

# General Principles

The backend is the single source of truth.

Business rules belong exclusively to the backend.

Never trust client-side validation.

---

# Layer Responsibilities

The backend follows strict layered architecture.

```
Router

↓

Service

↓

Repository

↓

Database
```

Layers must never be skipped.

---

# Router Rules

Routers are responsible only for:

- request parsing;
- dependency injection;
- authentication;
- response serialization;
- HTTP status codes.

Routers must never:

- contain business logic;
- execute SQL;
- access repositories directly;
- manipulate transactions.

Routers should remain thin.

---

# Service Rules

Services contain all business logic.

Services are responsible for:

- validation;
- authorization;
- business rules;
- orchestration;
- transactions;
- communication between repositories.

Services should remain framework-independent whenever possible.

---

# Repository Rules

Repositories interact with the database.

Responsibilities:

- CRUD operations;
- filtering;
- sorting;
- pagination;
- query optimization.

Repositories must never:

- validate business rules;
- perform authorization;
- return HTTP responses.

---

# ORM Rules

SQLAlchemy models represent persistence only.

Models should not contain:

- business logic;
- API serialization;
- validation;
- permissions.

Models describe database structure.

---

# DTO Rules

Never expose ORM models outside the repository layer.

Always return DTOs.

```
Database Model

↓

DTO

↓

API Response
```

DTOs define the public API contract.

---

# Pydantic Rules

Use Pydantic for:

- request validation;
- response serialization;
- configuration.

Separate schemas by purpose.

Example:

```
EventCreate

EventUpdate

EventResponse

EventFilter
```

Avoid using one schema for multiple responsibilities.

---

# Dependency Injection

Always use dependency injection.

Inject:

- repositories;
- services;
- database sessions;
- current user;
- configuration.

Avoid creating dependencies manually.

---

# Business Validation

Business validation belongs only inside services.

Examples:

- duplicate registration;
- event publication;
- permission checks;
- participation limits.

Repositories must not perform business validation.

---

# Database Validation

Database constraints provide the final validation layer.

Use:

- foreign keys;
- unique constraints;
- check constraints;
- indexes.

Never rely only on application logic.

---

# Transactions

Use transactions whenever multiple write operations occur.

Examples:

- Excel import;
- event deletion;
- bulk updates;
- administrator creation.

Rollback immediately if any operation fails.

---

# Query Optimization

Repositories should:

- minimize queries;
- avoid N+1 problems;
- select only required fields;
- paginate large datasets.

Optimize queries before adding caching.

---

# Pagination

Collections should never return unlimited results.

Support:

- page;
- page size;
- ordering;
- filtering.

---

# Search

Search should be:

- indexed;
- case-insensitive;
- efficient;
- paginated.

Avoid full table scans whenever possible.

---

# Exception Handling

Handle expected exceptions explicitly.

Examples:

- validation failure;
- duplicate data;
- resource not found;
- authentication failure;
- authorization failure.

Unexpected exceptions should be logged.

---

# Error Responses

Every API error should provide:

- HTTP status;
- machine-readable error code;
- human-readable message.

Response format must remain consistent.

---

# Logging

Log important backend events:

- authentication;
- authorization failures;
- event creation;
- updates;
- deletion;
- imports;
- background jobs;
- unexpected exceptions.

Sensitive information must never be logged.

---

# Authentication

Authentication verifies identity.

Responsibilities:

- verify JWT;
- load current user;
- reject invalid tokens.

Authentication does not determine permissions.

---

# Authorization

Authorization verifies permissions.

Always validate:

- role;
- ownership;
- business permissions.

Never trust client-provided roles.

---

# Background Tasks

Background jobs should be:

- idempotent;
- retryable;
- isolated;
- observable.

Long-running tasks must never block HTTP requests.

---

# File Processing

Before processing uploaded files:

Validate:

- extension;
- MIME type;
- file size;
- content.

Reject invalid files immediately.

---

# Caching

Cache only frequently accessed data.

Invalidate cache immediately after data modification.

Avoid stale business data.

---

# Configuration

Access configuration through centralized settings.

Avoid reading environment variables directly throughout the application.

---

# Security

Protect against:

- SQL Injection;
- XSS;
- CSRF (when applicable);
- brute-force attacks;
- path traversal;
- unsafe file uploads.

Every external input must be validated.

---

# Async Programming

Use asynchronous operations for:

- database access;
- external APIs;
- file processing;
- background communication.

Avoid blocking operations inside async endpoints.

---

# API Stability

Public API contracts should remain stable.

Avoid breaking changes unless explicitly planned.

Prefer backward-compatible evolution.

---

# Code Duplication

Business logic must exist only once.

If logic appears in multiple services,

extract a reusable abstraction.

---

# Backend Checklist

Before completing any backend task verify:

- router contains no business logic;
- services contain business rules;
- repositories only access data;
- DTOs are used correctly;
- transactions are safe;
- validation is complete;
- authorization is enforced;
- logging is appropriate;
- API responses are consistent;
- no duplicated logic exists.

---

# 5. Code Quality Standards

This section defines universal engineering rules that apply to every language, framework and module in this repository.

These rules are mandatory for both frontend and backend development.

---

# Readability

Code is written for humans first.

Optimize for readability before brevity.

Prefer explicit code over clever solutions.

Every engineer should understand the implementation without additional explanation.

---

# Simplicity

Always implement the simplest solution that satisfies the requirements.

Avoid:

- unnecessary abstractions;
- speculative architecture;
- premature optimization;
- overly generic solutions.

Simple code is easier to maintain.

---

# Function Design

A function should perform one task.

Good functions are:

- small;
- predictable;
- testable;
- reusable.

Avoid functions with multiple unrelated responsibilities.

---

# Function Size

Recommended guidelines:

- Small helper: ≤ 20 lines
- Business function: ≤ 50 lines
- Complex orchestration: ≤ 100 lines

If a function becomes difficult to understand,

split it.

---

# Function Parameters

Keep parameter lists short.

Prefer:

```
createEvent(eventData)
```

Instead of:

```
createEvent(
    title,
    description,
    date,
    location,
    organizer,
    ...
)
```

Use objects when multiple values belong together.

---

# Return Values

Functions should return predictable values.

Avoid returning different types depending on execution path.

Good:

```
EventResponse
```

Avoid:

```
Event

↓

null

↓

boolean

↓

string
```

---

# Naming Conventions

Names should describe intent.

Variables

```
event

user

statistics
```

Functions

```
createEvent()

publishEvent()

calculateStatistics()
```

Booleans

```
isPublished

hasPermission

canEdit
```

Collections

```
events

users

statistics
```

Avoid abbreviations unless universally understood.

---

# Variable Scope

Keep variables as close as possible to where they are used.

Avoid long-lived mutable variables.

---

# Magic Values

Avoid unexplained literals.

Good

```
MAX_UPLOAD_SIZE
```

Avoid

```
5242880
```

Business constants should be centralized.

---

# Comments

Code should explain itself.

Comments should explain:

- why;
- business context;
- non-obvious decisions.

Comments should not describe obvious code.

Good

```
// Prevent duplicate participation across browser sessions.
```

Avoid

```
// Increment i
i++
```

---

# Error Handling

Handle expected failures explicitly.

Do not silently ignore exceptions.

Every failure should either:

- be handled;
- be propagated;
- be logged.

---

# Logging

Logs should provide useful operational information.

Good logs answer:

- what happened;
- where;
- why.

Avoid excessive logging.

Never log:

- passwords;
- tokens;
- secrets;
- private data.

---

# Defensive Programming

Validate all external input.

Assume:

- requests may be invalid;
- files may be corrupted;
- users may provide unexpected values.

Fail safely.

---

# Null Handling

Avoid deep optional chains.

Prefer explicit guards.

Good

```
if (!event) return;
```

Avoid relying on undefined behavior.

---

# Duplication

Never duplicate business logic.

If identical logic appears twice,

extract it.

One implementation.

Multiple usages.

---

# Dependencies

Every dependency must have a clear purpose.

Before adding a package ask:

- Can existing tools solve this?
- Is maintenance acceptable?
- Is the dependency actively maintained?

Prefer fewer dependencies.

---

# Refactoring

Refactor only when it improves:

- readability;
- maintainability;
- simplicity.

Avoid refactoring unrelated code while implementing features.

---

# Breaking Changes

Avoid breaking public interfaces.

When unavoidable:

- document changes;
- update consumers;
- preserve backward compatibility when possible.

---

# Dead Code

Remove:

- unused functions;
- unused variables;
- obsolete files;
- commented-out production code.

Dead code increases maintenance cost.

---

# Temporary Code

Avoid leaving:

- TODO without issue reference;
- debug statements;
- console output;
- temporary workarounds.

Production code should remain clean.

---

# Code Review Principles

Every change should be reviewed against:

- correctness;
- architecture;
- readability;
- duplication;
- performance;
- security.

Code quality is more important than implementation speed.

---

# Self Review Checklist

Before considering a task complete verify:

- implementation is correct;
- architecture is preserved;
- naming is clear;
- no duplicated logic;
- no dead code;
- no unnecessary complexity;
- error handling is complete;
- logging is appropriate;
- types are correct;
- documentation remains accurate.

---

# Engineering Mindset

When solving problems:

Understand first.

Design second.

Implement third.

Optimize last.

Never reverse this order.

---

# Golden Rules

Always:

- reuse existing code;
- preserve architecture;
- write explicit code;
- keep modules small;
- prefer composition;
- validate inputs;
- use strong typing;
- think about long-term maintainability.

Never:

- duplicate business logic;
- bypass architecture;
- create unnecessary abstractions;
- ignore validation;
- trust client input;
- optimize prematurely;
- introduce hidden side effects.

---

# 6. Development Workflow

Every engineering task follows the same lifecycle.

```
Understand

↓

Analyze

↓

Plan

↓

Implement

↓

Validate

↓

Review

↓

Complete
```

Never skip any step.

---

# Task Analysis

Before writing code:

- understand the requirement;
- inspect affected modules;
- identify existing implementation;
- determine architectural impact;
- identify reusable components.

Never modify code blindly.

---

# Implementation Planning

Before implementation determine:

- affected files;
- affected modules;
- API changes;
- database changes;
- testing requirements;
- migration requirements.

Prefer the smallest possible change.

---

# Development Rules

Every implementation should:

- preserve architecture;
- minimize code changes;
- reuse existing modules;
- remain strongly typed;
- avoid unnecessary dependencies.

Never rewrite working code without a clear reason.

---

# Git Workflow

Every change should be isolated.

Recommended workflow:

```
Feature

↓

Implementation

↓

Testing

↓

Self Review

↓

Commit
```

Large unrelated changes should never be committed together.

---

# Commit Principles

Each commit should represent one logical change.

Good examples:

```
Add event filtering

Fix participation validation

Refactor event repository
```

Avoid generic commit messages.

Bad examples:

```
update

fix

changes

misc
```

---

# Pull Request Principles

A pull request should contain:

- one logical feature;
- one logical bug fix;
- one architectural improvement.

Avoid mixing unrelated work.

---

# Review Checklist

Every change should be reviewed for:

- correctness;
- architecture;
- readability;
- maintainability;
- duplication;
- security;
- performance.

Review before considering the task complete.

---

# Regression Prevention

Before merging verify:

- existing functionality still works;
- no public API was broken;
- business rules remain unchanged;
- validation still works;
- permissions remain correct.

---

# Testing Philosophy

Testing validates business behavior.

Do not test implementation details.

Prefer testing observable outcomes.

---

# Testing Levels

The project supports multiple testing levels.

Unit Tests

Validate individual functions.

Integration Tests

Validate interaction between modules.

API Tests

Validate endpoint behavior.

End-to-End Tests

Validate complete user workflows.

---

# What Should Be Tested

Critical functionality includes:

- authentication;
- authorization;
- event creation;
- event editing;
- participation;
- Excel import;
- statistics;
- permissions.

Business-critical functionality must always be covered.

---

# Validation Before Completion

Before completing any task verify:

Build

✓ Successful

Type Checking

✓ Successful

Lint

✓ Successful

Tests

✓ Successful

Manual Validation

✓ Successful

---

# Manual Verification

Always confirm:

- UI behaves correctly;
- API returns expected data;
- validation works;
- errors are handled correctly;
- loading states appear correctly.

---

# Performance Verification

Before completion verify:

- no unnecessary renders;
- no duplicated requests;
- no obvious performance regressions;
- bundle size remains reasonable.

---

# Security Verification

Verify:

- authorization remains enforced;
- sensitive data is protected;
- validation is complete;
- file uploads remain secure.

---

# Documentation

Whenever behavior changes:

Update documentation.

Documentation should never become outdated.

---

# Release Readiness

A feature is release-ready only if:

- implementation is complete;
- tests pass;
- documentation is updated;
- review is complete;
- architecture remains consistent.

---

# Definition of Done

A task is considered complete only when:

✓ Requirements implemented

✓ Architecture preserved

✓ No duplicated logic

✓ No unnecessary files

✓ No dead code

✓ Strong typing maintained

✓ Validation complete

✓ Error handling complete

✓ Security preserved

✓ Build successful

✓ Tests successful

✓ Documentation updated

✓ Self review completed

Only after every condition is satisfied may the task be considered finished.

---

# 7. AI Agent Rules

This section defines mandatory rules for AI-assisted development.

These rules override default model behavior whenever conflicts occur.

---

# Primary Objective

Generate production-quality code while preserving the existing architecture.

Never optimize for speed over correctness.

---

# Before Writing Code

Always:

- inspect existing implementation;
- understand architecture;
- identify reusable code;
- determine affected modules.

Never generate code without context.

---

# Before Creating Files

Always ask:

- Does this file already exist?
- Can an existing file be extended?
- Can existing logic be reused?
- Is a new file truly necessary?

Prefer modifying existing files.

---

# Before Creating Components

Search for existing:

- components;
- hooks;
- services;
- utilities;
- schemas;
- types.

Duplicate implementations are prohibited.

---

# Before Creating Business Logic

Always search for an existing service.

Business logic must never exist in multiple locations.

---

# Before Adding Dependencies

Ask:

- Is this dependency necessary?
- Can existing libraries solve the problem?
- Will this increase maintenance cost?

Prefer existing project dependencies.

---

# Allowed Changes

Prefer:

- extending;
- improving;
- reusing;
- simplifying.

Avoid replacing entire modules.

---

# Forbidden Actions

Never:

- rewrite working architecture;
- rename modules without reason;
- move files unnecessarily;
- duplicate business logic;
- duplicate API calls;
- duplicate validation;
- create unnecessary abstractions;
- introduce breaking changes;
- bypass documented architecture.

---

# React Rules

Never:

- fetch directly inside components;
- store server state inside Zustand;
- place business logic inside UI;
- duplicate React Query cache.

Always use:

Component

↓

Hook

↓

Service

↓

API

---

# Backend Rules

Never:

- execute SQL inside routers;
- perform authorization inside repositories;
- return ORM models directly;
- skip service layer.

Always use:

Router

↓

Service

↓

Repository

↓

Database

---

# Validation Rules

Always validate:

- request;
- business rules;
- database constraints.

Never trust frontend validation.

---

# Refactoring Rules

Refactor only when:

- complexity decreases;
- readability improves;
- duplication is removed;
- architecture improves.

Avoid cosmetic refactoring.

---

# Performance Rules

Optimize only after measuring.

Avoid premature optimization.

Readability has higher priority.

---

# File Creation Rules

New files should exist only when:

- responsibility is independent;
- existing files cannot be extended;
- architecture becomes clearer.

Avoid unnecessary fragmentation.

---

# Code Generation Rules

Generated code should be:

- explicit;
- readable;
- strongly typed;
- production-ready;
- maintainable.

Avoid placeholder implementations.

Avoid incomplete TODOs.

---

# Error Handling Rules

Expected failures should be handled explicitly.

Unexpected failures should:

- be logged;
- preserve consistency;
- avoid exposing internals.

---

# Architecture Preservation

The existing architecture is considered correct unless explicitly instructed otherwise.

Do not redesign the project.

Do not replace existing patterns.

Do not migrate frameworks.

---

# Engineering Priorities

Always prioritize:

1. Correctness
2. Architecture
3. Maintainability
4. Readability
5. Simplicity
6. Performance

---

# Final Verification

Before completing any task verify:

✓ Requirements implemented

✓ Existing architecture preserved

✓ No duplicated logic

✓ No unnecessary files

✓ Strong typing maintained

✓ Validation complete

✓ Build passes

✓ Tests pass

✓ Documentation remains accurate

If any item fails,

the task is not complete.

During implementation:

Never change architecture
unless explicitly requested.

Never refactor approved code.

Never introduce alternative solutions.

Never optimize implementation
unless requested.

Never modify files during review.

Review is read-only.

If lint reveals issues:

Fix only the reported issue.

Do not perform additional refactoring.

Database Rules

- Always use AsyncSession.
- Always use SQLAlchemy 2.0 style.
- Never use synchronous ORM APIs.
- Never change expire_on_commit=False unless explicitly requested.
