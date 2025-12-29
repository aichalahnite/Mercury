# 📊 DevSecOps Metrics – Mercury Project

This document presents the **key metrics** used to measure the effectiveness and maturity of the DevSecOps pipeline implemented in the Mercury backend project. Metrics provide **quantitative insights** into security, reliability, and development efficiency.

---

## 1. Mean Time to Detect (MTTD)

**Definition:**  
The average time taken to detect vulnerabilities or security issues in the codebase or pipeline.

**Purpose:**  
- Measures how quickly the system identifies issues.  
- Reflects the effectiveness of automated SAST, SCA, and secrets scans.

**Example (Conceptual):**  
- Average detection time for critical issues using Bandit, Safety, and Gitleaks: **2 hours**  
- Average detection time for container vulnerabilities (Trivy): **30 minutes**

---

## 2. Mean Time to Remediate (MTTR)

**Definition:**  
The average time taken to fix vulnerabilities or security issues once detected.

**Purpose:**  
- Shows the efficiency of the development and security teams in responding to threats.  
- Helps evaluate whether policies and automated gates accelerate remediation.

**Example (Conceptual):**  
- Time from vulnerability detection to code patch: **1 day**  
- Time from failed security gate to merge approval: **6 hours**

---

## 3. Security Gate Success Rate / Build Blocking

**Definition:**  
The percentage of builds blocked due to security violations or failing DevSecOps gates.

**Purpose:**  
- Reflects the strictness and enforcement of security policies.  
- Helps teams understand the impact of automated security on delivery.

**Example (Conceptual):**  
- Total builds in a month: 50  
- Builds blocked by high/critical vulnerabilities: 8  
- Security gate success rate: **84%**  

---

## 4. Vulnerability Trend (Before / After)

**Definition:**  
Tracks the number and severity of vulnerabilities over time.

**Purpose:**  
- Demonstrates improvements in code quality and security posture.  
- Shows the effect of DevSecOps automation in reducing risks.

**Example (Conceptual Graph Idea):**  
| Month | Critical | High | Medium | Low |
|-------|---------|------|--------|-----|
| Jan   | 10      | 25   | 40     | 15  |
| Feb   | 7       | 20   | 35     | 10  |
| Mar   | 3       | 12   | 25     | 5   |

> Shows clear reduction in critical and high-severity vulnerabilities.

---

## 5. Notes

- Metrics should be **updated regularly** and reflected in reports or dashboards.  
- Screenshots of pipeline runs, security scans, and dashboards can complement these metrics.  
- These metrics are **tool-agnostic** and transferable to Jenkins, GitLab CI, or GitHub Actions.

---

**Conclusion:**  
The metrics above provide a **quantitative view of the Mercury DevSecOps pipeline**, demonstrating **security maturity, process effectiveness, and continuous improvement**.
