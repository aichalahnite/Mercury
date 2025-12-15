# Security Policy

## Reporting Vulnerabilities
Please report security issues privately.

## Security Controls
- SAST: Bandit
- Dependency scanning: Safety
- Container scanning: Trivy
- Secrets scanning: Gitleaks
- DAST: OWASP ZAP
- SBOM: Syft

## CI Security Gates
Builds fail on:
- High/Critical CVEs
- Hardcoded secrets
- Security misconfigurations
