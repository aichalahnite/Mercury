# Secrets Management

## Principles
- No secrets in Git
- No secrets in Docker images
- No long-lived secrets

## Environments

### Local
.env (gitignored)

### CI
GitHub Secrets (masked)

### Production
HashiCorp Vault + GitHub OIDC

## Result
Secrets exist only in memory and expire automatically
