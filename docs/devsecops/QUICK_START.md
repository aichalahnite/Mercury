# ⚡ DevSecOps Quick Start - 5 Minutes Setup

## 🎯 Objectif
Mettre en place DevSecOps sur le backend Mercury en 5 minutes.

---

## Step 1: Install Pre-Commit (Local Security) - 1 min

```bash
cd /workspaces/Mercury

# Install pre-commit framework
pip install pre-commit

# Activate hooks on this repo
pre-commit install

# Test it
pre-commit run --all-files
```

**What it does**:
- ✅ Scans tous les fichiers Python pour vulnérabilités (Bandit)
- ✅ Empêche les secrets d'être pushés (Gitleaks)
- ✅ Formate le code (Black)

---

## Step 2: Setup Security Tools for Testing - 1 min

```bash
cd /workspaces/Mercury/backend

# Install scanning tools
pip install bandit safety pylint
```

---

## Step 3: Test Your Code Locally - 1 min

### Test #1: Scan for Security Issues (SAST)
```bash
cd /workspaces/Mercury/backend

bandit -r . -ll
```

**Output should show**: `No issues identified` ✅

---

### Test #2: Scan for Vulnerable Dependencies (SCA)
```bash
safety check -r requirements.txt
```

**Output should show**: `[OK]` or list any vulnerabilities

---

### Test #3: Run Unit Tests
```bash
cd /workspaces/Mercury/backend

pytest tests/ -v
```

**Output**: Green checkmarks = all tests pass ✅

---

### Test #4: Lint Code Quality
```bash
pylint $(find . -name "*.py" -type f | head -20)
```

**Output**: Score reported (higher is better)

---

## Step 4: GitHub Actions Setup - 2 min

The workflows are **already configured** in:
- `.github/workflows/ci.yml` - Unit tests & linting
- `.github/workflows/devsecops.yml` - Security scanning

### To activate:
1. Go to **GitHub settings** → **Actions** → **General**
2. Check: "Allow all actions"
3. Push code to GitHub

---

## Step 5: Make Your First Secure Commit

```bash
# Make a sample change
echo "# Safety note" >> backend/README.md

# Try to commit
git add backend/README.md
git commit -m "Add safety docs"
```

**Expected**:
- Bandit runs ✅
- Black formats (if needed)
- Gitleaks checks for secrets
- If all pass → commit succeeds ✅

---

## 🔐 Now Your Backend is Protected By:

| Layer | Tools | Trigger |
|-------|-------|---------|
| **Developer** | Bandit + Gitleaks + Black | Every commit |
| **CI** | Pytest + Pylint | Every push |
| **DevSecOps** | Bandit + Safety + Trivy + OPA | Every PR |
| **Deployment** | Vault secrets | Every deploy |

---

## 📊 Monitoring Results

### Where to see results:

#### **1. Local Pre-Commit**
```bash
cat reports/precommit/bandit-*.json
cat reports/precommit/gitleaks-*.json
```

#### **2. GitHub CI**
Go to: **Your Repo** → **Actions** → **CI Pipeline**

#### **3. GitHub DevSecOps**
Go to: **Your Repo** → **Actions** → **DevSecOps Pipeline**

---

## ⚠️ Common Issues

### Issue: "pre-commit not in PATH"
```bash
# Install globally
pip install --user pre-commit
```

### Issue: Bandit finds "issues"
**Most are false positives**. To suppress:
```python
# Add #nosec comment
output = subprocess.Popen(['ls'], stdout=subprocess.PIPE)  # nosec
```

### Issue: GitHub Actions failing
**Check logs**: Click on the failing job → expand to see details

---

## ✅ Validation Checklist

- [ ] `pre-commit install` completed
- [ ] `bandit -r backend -ll` → No issues ✅
- [ ] `safety check` → OK ✅
- [ ] `pytest` → All pass ✅
- [ ] Can push to GitHub without errors ✅

---

## 🎓 Learn More

- **Pre-Commit**: [pre-commit.com](https://pre-commit.com)
- **Bandit**: [github.com/PyCQA/bandit](https://github.com/PyCQA/bandit)
- **Safety**: [github.com/pyupio/safety](https://github.com/pyupio/safety)
- **OPA**: [www.openpolicyagent.org](https://www.openpolicyagent.org)

---

🚀 **You now have production-grade security automation!**
