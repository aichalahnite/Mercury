# 🛡️ Mercury – Enterprise DevSecOps Architecture

Mercury is a security-first backend application that demonstrates a **complete, production-grade DevSecOps lifecycle**.

Security is implemented **by design**, **automated**, and **enforced** at every stage of the software delivery process.

➡️ **Start here:** `docs/devsecops/00-overview.md`

---

## DevSecOps Principles Applied

- Shift-Left Security
- Least Privilege
- Zero Trust CI/CD
- Policy-as-Code
- Immutable Infrastructure
- Ephemeral Credentials
- Continuous Security Validation

---

## High-Level Workflow

Developer
├─ Pre-Commit Security Hooks
├─ CI Pipeline
├─ DevSecOps Pipeline
├─ Policy Enforcement (OPA)
├─ DAST (Live App + Test DB)
├─ Secure CD (Vault)
└─ Production

yaml
Copy code

---

## Key Technologies

| Area | Tools |
|----|----|
| CI | GitHub Actions |
| SAST | Bandit |
| SCA | Safety |
| Secrets | Gitleaks |
| Containers | Docker, Trivy |
| DAST | OWASP ZAP |
| Policy | OPA |
| Secrets Mgmt | Vault |
| SBOM | Syft |

---

## Documentation

📁 Full technical documentation is available in:  
➡️ **`docs/devsecops/`**

---

## Security Contact

Security issues should be reported privately.