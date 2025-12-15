# DevSecOps Pipeline

This pipeline enforces security gates.

## Stages

### SAST
- Tool: Bandit
- Blocks insecure patterns

### Dependency Security
- Tool: Safety
- Detects vulnerable dependencies

### Secrets Detection
- Tool: Gitleaks
- Prevents secret leakage

### Container Security
- Tool: Trivy
- Scans OS + dependencies

### SBOM
- Tool: Syft
- Enables auditability

## Security Gate Behavior
HIGH or CRITICAL findings → build fails
