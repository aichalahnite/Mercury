# ⚖️ Security Exceptions & Risk Acceptance – Mercury Project

In any production system, **not all vulnerabilities can or should block deployment**.  
This document outlines the **risk acceptance framework** applied in the Mercury DevSecOps pipeline.

---

## 1. Purpose

The purpose of a risk acceptance process is to:

- Identify vulnerabilities that are **low-risk or not immediately exploitable**  
- Allow business continuity without compromising **critical security**  
- Document decisions for **auditability and accountability**  

> This aligns with real-world enterprise security practices.

---

## 2. Severity Thresholds

Vulnerabilities are categorized by severity:

| Severity | Description | Action in Pipeline |
|----------|------------|-----------------|
| Critical | Exploitable, high impact | Block build / fail gate |
| High | Major vulnerability, needs attention | Block build / fail gate |
| Medium | Potentially risky, low likelihood | Log warning, optional approval |
| Low | Minimal impact | Allow deployment, document |

**Pipeline implementation example:**  

- Trivy / Safety / Bandit outputs **severity levels**  
- Jenkins / GitHub Actions / GitLab CI can **fail the pipeline** only for Critical and High  
- Medium and Low can be **reviewed manually**  

---

## 3. Manual Risk Approval

Some vulnerabilities require **human judgment** before deployment:

1. Security Engineer or DevSecOps lead reviews flagged issues  
2. Risk is assessed based on:
   - Exploitability
   - Business impact
   - Mitigation alternatives  
3. Approval is recorded in pipeline logs or ticketing system (e.g., Jira)

**Example:**  
- Medium vulnerability in a test-only module  
- Reviewed and approved → deployment allowed

---

## 4. Documentation & Auditability

All accepted risks are **documented**:

- Vulnerability description  
- Reason for acceptance  
- Approval date & approver  
- Mitigation plan or future remediation timeline  

> This ensures transparency and accountability for internal and external audits.

---

## 5. Integration with Mercury DevSecOps Pipeline

- **Critical / High** → Security gates automatically block deployment  
- **Medium / Low** → Flagged for review; deployment can proceed with approval  
- **Tools involved:** Bandit, Safety, Trivy, Gitleaks, OPA policies  

This creates a **balanced approach** between security and business agility.

---

## 6. Conclusion

The risk acceptance process allows Mercury to:

- Maintain **continuous delivery**  
- Enforce **security where it matters most**  
- Document all security exceptions for **compliance and audits**  

> Proper risk acceptance is a hallmark of **mature DevSecOps practices**.
