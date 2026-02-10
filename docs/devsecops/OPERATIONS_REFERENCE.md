# 📋 DevSecOps Operations Reference

## Quick Command Reference

### 🖥️ Local Development

#### Setup (First Time)
```bash
cd /workspaces/Mercury

# Install pre-commit framework
pip install pre-commit

# Activate hooks
pre-commit install

# Install dev tools
pip install -r backend/requirements-dev.txt
```

#### Before Every Commit
```bash
# Run all security checks locally
pre-commit run --all-files

# Or run specific tools:
cd backend

# 1. Code SAST (Static Analysis)
bandit -r . -ll

# 2. Dependency scanning
safety check -r requirements.txt

# 3. Code linting
pylint $(find . -name "*.py" -type f | head -10)

# 4. Unit tests
pytest tests/ -v --cov=.

# 5. Code formatting
black .
```

#### Commit Workflow
```bash
# 1. Write code
vim backend/users/views.py

# 2. Pre-commit runs automatically
git add .
git commit -m "Add user validation"
# → If issues: fix them and retry
# → If OK: commit succeeds ✅

# 3. Push to GitHub
git push origin backend
```

---

### 🔄 GitHub Actions (Automated)

**No action needed** - runs automatically on push

#### Where to See Results
1. Go to **GitHub → Actions tab**
2. Find your workflow run
3. Click to see details

#### Jobs that Run:

| Job | When | Tools | Blocks if |
|-----|------|-------|-----------|
| **CI** | Every push | Pylint, Pytest | Test fails |
| **SAST** | Every push | Bandit, Safety | CRITICAL found |
| **Secrets** | Every push | Gitleaks | Secrets found |
| **Container** | Every push | Trivy, Syft | CRITICAL vuln |
| **DAST** | Every push | OWASP ZAP | HIGH+ found |
| **OPA** | Every push | Policy checks | Rule failed |

---

### 📊 Viewing Security Reports

#### Local Reports
```bash
# Pre-commit reports
ls reports/precommit/

# Bandit findings
cat reports/precommit/bandit-YYYYMMDD-HHMMSS.json

# Gitleaks findings
cat reports/precommit/gitleaks-YYYYMMDD-HHMMSS.json
```

#### GitHub Reports
**Actions → [Workflow Name] → [Run ID] → [Click Job]**

---

## Configuration Files Explained

### 1. `.pre-commit-config.yaml`
**What**: Local hooks that run before commit  
**Where**: Root directory  
**Tools**:
- Bandit (finds security issues)
- Gitleaks (finds secrets)
- Black (formats code)

**To change**:
```yaml
# Edit .pre-commit-config.yaml
repos:

- repo: https://github.com/pycqa/bandit
  rev: 1.7.5
  hooks:
    - id: bandit
      name: Bandit SAST
      args: ['-ll', '-r', 'backend']  # Change severity level
```

### 2. `.github/workflows/ci.yml`
**What**: CI pipeline - linting & testing  
**When**: Every push  
**Tools**:
- Pylint (code quality)
- Pytest (unit tests)

**To change**:
```yaml
- name: Unit Tests
  run: pytest backend/tests --cov=backend
  # Add more test flags as needed
```

### 3. `.github/workflows/devsecops.yml`
**What**: Security scanning pipeline  
**When**: Every push/PR  
**Tools**:
- Bandit (SAST)
- Safety (Dependencies)
- Gitleaks (Secrets)
- Trivy (Container)
- Syft (SBOM)
- OWASP ZAP (DAST)
- OPA (Policy)

**To change**:
```yaml
- name: Bandit (SAST)
  run: bandit -r backend -ll -iii  # Change severity
```

### 4. `policy/docker.rego`
**What**: Docker security policies  
**Enforces**:
- No root user
- Must have HEALTHCHECK

**Example policy**: Add to enforce non-root
```rego
deny[msg] {
  input.config.User == "root"
  msg := "Must not run as root"
}
```

### 5. `policy/cicd.rego`
**What**: CI/CD pipeline policies  
**Enforces**:
- No critical vulnerabilities
- No secrets in commits

### 6. `backend/Dockerfile`
**What**: Container security  
**Already implements**:
- ✅ Non-root user
- ✅ Minimal image (slim)
- ✅ No cache
- ✅ Health checks ready

---

## Fixing Common Issues

### Issue #1: Bandit found "issue" but it's false positive

**Solution**: Add `# nosec` comment
```python
# BEFORE (flagged by Bandit)
user_input = input()
exec(user_input)

# AFTER (ignored)
user_input = input()
exec(user_input)  # nosec
```

### Issue #2: Safety report says dependency is vulnerable

**Solution**: Update dependency
```bash
pip install --upgrade vulnerable-package

# Or pin to safe version
pip install vulnerable-package==2.5.0  # if 2.5.0+ is safe
```

### Issue #3: Pre-commit hooks take too long

**Solution**: Skip for large files
```yaml
# In .pre-commit-config.yaml
- id: bandit
  exclude: "^(tests/|migrations/)"  # Don't scan tests
```

### Issue #4: GitHub Actions timeout

**Solution**: Run in parallel
```yaml
jobs:
  sast:
    runs-on: ubuntu-latest
    # Fast job
  
  container:
    runs-on: ubuntu-latest
    needs: sast
    # Depends on sast
```

---

## Daily Workflow Summary

### For Every Code Change:

```bash
# 1. Make changes
vim backend/users/models.py

# 2. Run checks locally (automatic with pre-commit)
git add backend/users/models.py
git commit -m "Add user profile picture support"
# → Bandit runs automatically
# → Gitleaks runs automatically
# → Black reformats if needed
# ✅ If all pass, commit succeeds

# 3. Push to GitHub
git push origin feature/user-profile

# 4. Check GitHub Actions (after push)
# → Go to Actions tab
# → Watch CI workflow (2-3 min)
# → Watch DevSecOps workflow (5-10 min)
# ✅ If all green, create PR

# 5. Merge when all checks pass
```

---

## Tools Summary

| Tool | Purpose | Runs | Failure Impact |
|------|---------|------|-----------------|
| **Bandit** | SAST (code issues) | Local + CI + DevSecOps | Blocks commit/merge |
| **Gitleaks** | Detects secrets | Local + DevSecOps | Blocks commit/merge |
| **Black** | Code formatter | Local | Auto-fixes |
| **Pylint** | Code quality | CI | Comment on PR |
| **Pytest** | Unit tests | CI + DevSecOps | Blocks merge |
| **Safety** | Dependency scan | DevSecOps | Blocks merge |
| **Trivy** | Container scan | DevSecOps | Blocks merge |
| **Syft** | SBOM generation | DevSecOps | Info only |
| **OWASP ZAP** | Dynamic testing | DevSecOps | Blocks merge if HIGH+ |
| **OPA** | Policy enforcement | DevSecOps | Blocks merge if violated |

---

## Understanding the Security Levels

### Level 1: Shift-Left (Local)
- **When**: Before you push code
- **Who**: You (developer)
- **Cost of fix**: Cheapest ⭐
- **Tools**: Pre-commit hooks
- **Action if fail**: Must fix before commit

### Level 2: Continuous Integration
- **When**: When you push code
- **Who**: GitHub Actions (automatic)
- **Cost of fix**: Cheap ⭐⭐
- **Tools**: Pylint, Pytest
- **Action if fail**: PR gets comments

### Level 3: DevSecOps
- **When**: Before merge to main
- **Who**: GitHub Actions (automatic)
- **Cost of fix**: Expensive ⭐⭐⭐
- **Tools**: Bandit, Safety, Trivy, OWASP ZAP, OPA
- **Action if fail**: Blocks merge until fixed

### Level 4: Production Deployment
- **When**: During deployment
- **Who**: CD pipeline (automatic)
- **Cost of fix**: Very expensive ⭐⭐⭐⭐
- **Tools**: Vault (secrets), signed images, monitoring
- **Action if fail**: Blocks deployment

---

## Performance Tips

### Speed Up Pre-commit
```bash
# Only scan changed files (default)
pre-commit run

# Skip during merge
git commit -m "Merge PR" --no-verify
```

### Speed Up Tests
```bash
# Run tests in parallel
pytest -n auto

# Run only changed tests
pytest --lf  # last failed
pytest --ff  # failed first
```

### Speed Up Bandit
```bash
# Only high-confidence issues
bandit -r . -ll  # -ll = medium+ confidence
```

---

## Emergency Procedures

### If sensitive data was accidentally committed:

```bash
# 1. Check if found by Gitleaks
git log --all --pretty=format: --name-only | sort -u

# 2. Use git-filter-branch to remove (careful!)
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch secret_file.txt' \
  --prune-empty

# 3. Force push
git push --force-with-lease

# 4. Rotate credentials/secrets immediately
```

### If vulnerable dependency is in production:

```bash
# 1. Check version
pip list | grep vulnerable-package

# 2. Update
pip install --upgrade vulnerable-package

# 3. Test locally
pytest

# 4. Push fix
git commit -m "Security: upgrade vulnerable-package"
git push

# 5. Deploy
```

---

## Additional Resources

- [DevSecOps Full Documentation](./IMPLEMENTATION_GUIDE.md)
- [Quick Start (5 minutes)](./QUICK_START.md)
- [Threat Model](../threat-model.md)
- [Architecture](../2.%20architecture.md)

---

**Last Updated**: February 2026  
**DevSecOps Status**: ✅ Fully Operational
