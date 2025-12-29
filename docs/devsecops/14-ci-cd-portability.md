
# 🔄 CI/CD Pipeline Portability – Mercury Project

While the Mercury DevSecOps pipeline is implemented using **GitHub Actions**, the design is **tool-agnostic** and can be **ported to Jenkins or GitLab CI/CD** with minimal changes.  

This demonstrates that the **DevSecOps concepts are independent of a specific CI/CD platform**.

---

## 1. Stage Mapping

The pipeline is organized in logical stages:

| Mercury GitHub Actions | Conceptual Stage | Jenkins / GitLab CI Mapping |
|-----------------------|----------------|----------------------------|
| Pre-commit Hooks      | Shift-left security | Pre-commit + static analysis jobs |
| CI Pipeline           | Build & test   | Build and test stages/jobs |
| SAST + SCA            | Code & dependency scanning | Same tools executed in Jenkinsfile or `.gitlab-ci.yml` |
| Secrets Scan          | Detect secrets | Same tools, same configuration |
| Container Scan + SBOM | Container security & compliance | Same steps, run as Jenkins/GitLab jobs |
| DAST                  | Dynamic application testing | Same steps, run as Jenkins/GitLab jobs |
| Policy-as-Code (OPA)  | Policy enforcement | Same Rego policies executed in pipeline |
| Secure CD             | Deployment with short-lived secrets | Same logic in Jenkins/GitLab |

> Each GitHub Actions workflow **maps 1-to-1** to a stage in Jenkins or GitLab CI/CD.

---

## 2. Tool Consistency

- All security tools (Bandit, Safety, Gitleaks, Trivy, OWASP ZAP, OPA, Vault) remain **identical**.  
- Only the **pipeline syntax** changes (YAML vs Groovy vs GitLab YAML).  
- No conceptual change is needed; only minor adaptation for:
  - Runner agents
  - Pipeline triggers
  - Secrets injection

---

## 3. Academic Value

Including this note shows:

- Understanding of **CI/CD concepts over specific tools**  
- Ability to **transfer knowledge to enterprise pipelines**  
- Readiness to **defend tool choices** in academic or professional settings

> This section directly addresses potential questions like:  
> *“Why not Jenkins or GitLab?”*

---

## 4. Conclusion

Mercury’s DevSecOps pipeline is **flexible, portable, and conceptually tool-agnostic**, demonstrating that security automation is **platform-independent** while remaining fully enforceable.
