# TEST_CASES.md

> Version: 2.0
>
> This document defines the testing strategy, quality assurance process and validation requirements.
>
> Engineering rules are documented in `ENGINEERING.md`.

---

# Testing Philosophy

Testing verifies business behavior rather than implementation details.

Tests should provide confidence that the application behaves correctly under expected and unexpected conditions.

Every critical feature should be covered by automated tests.

---

# Testing Goals

Testing should ensure:

- correctness;
- stability;
- maintainability;
- regression prevention;
- confidence during refactoring.

---

# Testing Pyramid

```
                E2E

        Integration Tests

          Unit Tests
```

Most tests should be unit tests.

End-to-end tests should cover only critical user workflows.

---

# Testing Levels

The project uses four testing levels:

- Unit Tests
- Integration Tests
- API Tests
- End-to-End Tests

Each level validates a different responsibility.

---

# Unit Tests

Purpose:

Validate isolated business logic.

Unit tests should:

- execute quickly;
- avoid network access;
- avoid database access;
- avoid external dependencies.

Typical targets:

- utility functions;
- validators;
- services;
- business rules.

---

# Integration Tests

Purpose:

Validate interaction between multiple modules.

Examples:

- Service + Repository
- Repository + Database
- API + Authentication

Integration tests should use realistic application behavior.

---

# API Tests

Purpose:

Validate REST API contracts.

Every endpoint should verify:

- request validation;
- authentication;
- authorization;
- response format;
- error handling;
- status codes.

---

# End-to-End Tests

Purpose:

Validate complete user workflows.

Examples:

- login;
- event creation;
- event editing;
- participation;
- Excel import.

Only critical user journeys should use E2E tests.

---

# Frontend Testing

Frontend tests should verify:

- rendering;
- user interaction;
- form validation;
- loading states;
- error states;
- accessibility.

Avoid testing implementation details.

---

# Backend Testing

Backend tests should verify:

- business logic;
- permissions;
- validation;
- transactions;
- repositories;
- API contracts.

---

# Database Testing

Database tests should verify:

- migrations;
- constraints;
- indexes;
- foreign keys;
- transactions.

Never assume schema correctness without tests.

---

# Security Testing

Critical security features should verify:

- authentication;
- authorization;
- permission checks;
- invalid JWT;
- expired JWT;
- forbidden access.

---

# File Upload Testing

Validate:

- valid files;
- invalid extensions;
- invalid MIME types;
- oversized files;
- corrupted files.

---

# Validation Testing

Every validation rule should have tests for:

- valid input;
- invalid input;
- missing required values;
- invalid formats;
- edge cases.

---

# Error Handling Tests

Verify:

- predictable errors;
- correct HTTP status;
- useful messages;
- no internal information leakage.

---

# Pagination Tests

Verify:

- page size;
- page boundaries;
- sorting;
- filtering.

---

# Search Tests

Validate:

- exact matches;
- partial matches;
- case-insensitive search;
- empty results.

---

# Performance Tests

Performance tests should verify:

- response time;
- large datasets;
- pagination performance;
- import performance.

---

# Regression Tests

Whenever a bug is fixed,

add a regression test.

The same bug should never appear twice.

---

# Mocking

Mock only external dependencies.

Examples:

- external APIs;
- SMTP;
- cloud storage;
- payment providers.

Avoid mocking business logic.

---

# Test Fixtures

Fixtures should be:

- reusable;
- deterministic;
- isolated;
- easy to understand.

Avoid large shared fixtures.

---

# Test Data

Use realistic data.

Avoid meaningless placeholders.

Good:

- valid events;
- realistic dates;
- meaningful names.

---

# Naming

Test names should describe behavior.

Good

```
should_create_event

should_reject_duplicate_participation

should_return_404_for_missing_event
```

Avoid generic names.

---

# Test Independence

Tests should never depend on execution order.

Every test should be executable independently.

---

# Coverage Philosophy

Coverage measures confidence,

not quality.

Aim to cover business-critical behavior rather than every line.

---

# Critical Coverage

High priority:

- authentication;
- authorization;
- business rules;
- event management;
- participation;
- imports.

---

# Manual Testing

Before release verify:

- responsive layout;
- accessibility;
- navigation;
- forms;
- uploads;
- error handling.

---

# Smoke Tests

After deployment verify:

- application starts;
- database connected;
- API available;
- authentication works;
- frontend loads.

---

# Release Checklist

Before release verify:

✓ Unit Tests pass

✓ Integration Tests pass

✓ API Tests pass

✓ E2E Tests pass

✓ No regressions

✓ Build successful

✓ Documentation updated

✓ Manual verification completed

---

# AI Validation Checklist

When code is generated by an AI assistant verify:

- architecture preserved;
- business logic correct;
- no duplicated code;
- strong typing maintained;
- validation complete;
- authorization correct;
- error handling complete;
- tests updated.

Never assume generated code is correct without verification.

---

# Testing Principles

Always:

- test business behavior;
- keep tests deterministic;
- isolate failures;
- write readable assertions;
- prevent regressions.

Never:

- test implementation details;
- depend on execution order;
- duplicate test logic;
- ignore failing tests.
