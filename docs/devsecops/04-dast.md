# Dynamic Application Security Testing (DAST)

## Objective
Test the running application for real attack vectors.

## Setup
- Ephemeral backend container
- Ephemeral PostgreSQL database
- No production secrets

## Tool
OWASP ZAP (Baseline Scan)

## Attacks Detected
- XSS
- SQL Injection
- Security Misconfigurations

## Failure Policy
Medium+ issues block deployment
