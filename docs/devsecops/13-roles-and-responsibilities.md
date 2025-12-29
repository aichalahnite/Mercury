# 👥 DevSecOps Roles & Responsibilities – Mercury Project

DevSecOps is not just about tools and automation—it is a **culture** that requires clear roles and responsibilities.  
This document outlines the key roles in the Mercury DevSecOps pipeline and their responsibilities.

---

## 1. Developer

**Responsibilities:**
- Write secure, high-quality code
- Follow pre-commit hooks for SAST, formatting, and linting
- Respond to vulnerabilities flagged in CI/CD pipelines
- Integrate security into unit and integration tests
- Collaborate with Security Engineers on threat modeling

**Key Contribution:**  
Shift-left security—developers are the **first line of defense**.

---

## 2. DevOps / Platform Engineer

**Responsibilities:**
- Design and maintain CI/CD pipelines
- Automate builds, tests, and deployments
- Integrate security tools into the pipeline (Bandit, Trivy, Gitleaks, OWASP ZAP)
- Ensure reproducible and immutable infrastructure
- Manage secrets lifecycle via Vault or similar tools

**Key Contribution:**  
Ensures **continuous, automated, and secure delivery** of software.

---

## 3. Security / DevSecOps Engineer

**Responsibilities:**
- Define security policies and enforce them via Policy-as-Code (OPA)
- Conduct SAST, DAST, and container security reviews
- Monitor and respond to pipeline alerts and security failures
- Guide developers and DevOps engineers on vulnerability remediation
- Evaluate third-party dependencies for supply chain risks

**Key Contribution:**  
Acts as the **security guardian**, embedding protection into every stage.

---

## 4. Product Owner / Project Lead

**Responsibilities:**
- Prioritize security requirements alongside functional requirements
- Approve risk acceptance for non-critical vulnerabilities
- Support a culture of security within the development team
- Ensure compliance with internal policies and external regulations

**Key Contribution:**  
Balances **business objectives with security needs**, enabling informed decision-making.

---

## 5. Summary

- DevSecOps is a **shared responsibility**; tools like GitHub Actions or Jenkins are only enablers.  
- Security is **everyone’s job**, from coding to deployment.  
- Clear roles and responsibilities help Mercury achieve **automation, compliance, and security maturity**.

> **Takeaway:** DevSecOps is **culture first, tools second.**
