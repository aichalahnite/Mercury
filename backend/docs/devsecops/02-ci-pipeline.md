# CI Pipeline

## Purpose
Validate code quality and correctness.

## Stages
1. Linting (Pylint)
2. Unit Tests (Pytest)

## Characteristics
- Fast (< 2 min)
- No secrets
- Runs on every push / PR

## Failure Policy
- Any failure blocks merge
