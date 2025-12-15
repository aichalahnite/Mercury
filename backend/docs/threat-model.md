# Threat Model – Mercury Backend

## Assets
- User credentials
- Emails
- Database records
- API tokens

## Entry Points
- REST API (port 8000)
- PostgreSQL
- SMTP (future)

## Threats
| Threat | Risk | Mitigation |
|------|-----|------------|
| SQL Injection | High | ORM + input validation |
| Credential leakage | High | Secrets scanning + env vars |
| Container escape | Medium | Non-root + cap_drop |
| Supply chain attack | High | Safety + Trivy + SBOM |
| API abuse | Medium | Rate limiting + auth |

## Trust Boundaries
- Internet → API
- API → Database
- API → Mail service
