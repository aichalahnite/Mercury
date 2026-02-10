# 🚀 DevSecOps Implementation Guide for Mercury Backend

## Overview
Ce guide explique comment appliquer complètement DevSecOps sur le backend Mercury.

---

## Part 1: Understanding DevSecOps

### Qu'est-ce que DevSecOps?
**DevSecOps = Development + Security + Operations**

Au lieu d'attendre que la sécurité soit vérifié à la fin (après développement), DevSecOps **intègre la sécurité à chaque étape** :

```
Sans DevSecOps:    Code → Deploy → (Security Check) → Fix Issues ❌
Avec DevSecOps:    Code (SCAN) → Deploy (SCAN) → Run (SCAN) ✅
```

### Les 4 Niveaux de DevSecOps

#### **Level 1: Shift-Left (Développeur Local)**
- **Quand**: Avant que le code ne soit poussé
- **Qui**: Le développeur
- **Outils**: Pre-commit hooks
  - Bandit (SAST) - détecte les vulnérabilités Python
  - Gitleaks - empêche les secrets dans le code
  - Black - formate le code
- **Résultat**: Le commit est bloqué si problème ❌

**Mercury Status**: ✅ Configuré dans `.pre-commit-config.yaml`

---

#### **Level 2: Continuous Integration (Pull Request)**
- **Quand**: Quand le code est pushé / PR créée
- **Qui**: GitHub Actions (automatique)
- **Outils**: 
  - Pylint - linting
  - Pytest - unit tests
  - Code coverage analysis
- **Résultat**: PR ne peut pas être mergée si tests échouent ❌

**Mercury Status**: ✅ Configuré dans `.github/workflows/ci.yml`

---

#### **Level 3: DevSecOps Pipeline (PR → Merge)**
- **Quand**: Avant que le PR soit mergé
- **Qui**: GitHub Actions (automatique)
- **Outils**:
  - Bandit (SAST) - trouver les bugs de sécurité
  - Safety (SCA) - scanner les dépendances vulnérables
  - Gitleaks (Secrets) - détecter les secrets
  - Trivy (Container) - scanner l'image Docker
  - Syft (SBOM) - générer la nomenclature des composants
  - OWASP ZAP (DAST) - test dynamique
  - OPA (Policy-as-Code) - appliquer les règles de sécurité
- **Résultat**: Aucune vulnérabilité critique n'atteint main ❌

**Mercury Status**: ✅ Configuré dans `.github/workflows/devsecops.yml`

---

#### **Level 4: Secure Deployment (CD)**
- **Quand**: Lors du déploiement en production
- **Qui**: CD pipeline
- **Outils**:
  - Vault (Secrets éphémères) - aucun secret en dur
  - Immutable artifacts - images Docker signées
  - Runtime monitoring
- **Résultat**: Production ultra-sécurisée ✅

**Mercury Status**: 🔄 À configurer

---

## Part 2: Implementation Checklist

### Phase 1: Local Development (Developer Machine)

#### 1.1 Setup Pre-Commit Hooks ✅

**Status**: Configuré  
**File**: `.pre-commit-config.yaml`

**Pour activer localement**:
```bash
cd /workspaces/Mercury
pip install pre-commit
pre-commit install
```

**Test**:
```bash
# Modifiez n'importe quel fichier Python et faites un commit
git add <file>
git commit -m "test"
# → Bandit et Gitleaks vont s'exécuter automatiquement
```

**Si les hooks sont bloquants**:
- Corrigez le code OU
- Utilisez `git commit --no-verify` (⚠️ non recommandé)

---

#### 1.2 Add Security Tools to Requirements ✅

**Status**: Recommandé  
**Action**: Ajouter à `backend/requirements.txt` ou new `backend/requirements-dev.txt`

```plaintext
# Security Tools
bandit>=1.7.5
safety>=2.3.5
pylint>=2.15.0
black>=24.0.0
```

**ou mieux encore, créez un fichier séparé**:

`backend/requirements-dev.txt`:
```plaintext
-r requirements.txt

# Testing
pytest>=7.0
pytest-cov>=4.0
pytest-django>=4.5

# Linting & Formatting
pylint>=2.15.0
black>=24.0.0
flake8>=5.0

# Security Scanning
bandit>=1.7.5
safety>=2.3.5
pip-audit>=2.4.0
```

---

### Phase 2: CI/CD Pipeline (GitHub Actions)

#### 2.1 CI Pipeline ✅

**Status**: Configuré  
**File**: `.github/workflows/ci.yml`

**Que fait-il**:
1. ✅ Installe les dépendances
2. ✅ Lint le code (Pylint)
3. ✅ Exécute les tests unitaires (Pytest)

**Comment voir les résultats**:
1. Push code on GitHub
2. Allez à **Actions** → cherchez votre workflow
3. Regardez les logs

---

#### 2.2 DevSecOps Pipeline ✅

**Status**: Configuré  
**File**: `.github/workflows/devsecops.yml`

**Ce qu'il scanne**:

| Scan | Outil | Détecte | Bloque si |
|------|-------|---------|-----------|
| SAST | Bandit | Injection SQL, RCE, etc. | HIGH, CRITICAL |
| SCA | Safety | Dépendances vulnérables | CRITICAL |
| Secrets | Gitleaks | Secrets hardcodés | Secrets trouvés |
| Container | Trivy | OS vulns + package vulns | CRITICAL |
| SBOM | Syft | Liste composants | ✅ Info only |
| DAST | OWASP ZAP | Vulns à l'exécution | HIGH, CRITICAL |
| Policies | OPA | Violations des règles | Règles échouées |

**Exemple**: Dépendance vulnérable
```bash
# Quelqu'un ajoute 'requests==2.20.0' qui a CVE
requirements.txt: requests==2.20.0  ❌
↓
Safety chèque → trouve CVE ❌
↓
DevSecOps workflow échoue ❌
↓
PR ne peut pas être merger ❌ 
↓
Dépendance doit être mise à jour
```

---

### Phase 3: Policy-as-Code (OPA)

#### 3.1 Docker Policy ✅

**Status**: Configuré  
**File**: `policy/docker.rego`

**Règles appliquées**:
1. ❌ Pas d'exécution en tant que `root`
2. ❌ Doit avoir HEALTHCHECK

**Vérifier**: `backend/Dockerfile` respecte les règles:
```dockerfile
USER appuser  # ✅ Non-root
# ✅ Dockerfile a pas d'erreur
```

---

#### 3.2 CI/CD Policy 🔄

**Status**: Partiellement configuré  
**File**: `policy/cicd.rego`

**À améliorer**:
```rego
package cicd.security

# Pas d'images non-signées
deny[msg] {
  input.image_signed == false
  msg := "Docker image must be signed"
}

# Pas de secrets en variables
deny[msg] {
  input.env_has_secrets == true
  msg := "Secrets must not be in environment variables"
}

# Uniquement les registries de confiance
deny[msg] {
  not startswith(input.registry, "gcr.io/")
  not startswith(input.registry, "docker.io/myorg/")
  msg := "Only trusted registries allowed"
}
```

---

### Phase 4: Deployment & Vault (À faire)

#### 4.1 Setup HashiCorp Vault 🔄

**For ephemeral secrets**:

```bash
# 1. Start Vault locally
docker run -d --name vault -p 8200:8200 vault

# 2. Initialize and unseal
vault operator init
vault operator unseal

# 3. Create secrets
vault kv put secret/mercury/db password=xxxxx
vault kv put secret/mercury/api-key key=xxxxx
```

#### 4.2 Update CD Workflow 🔄

File: `.github/workflows/cd.yml`

```yaml
name: Secure Deployment

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      # ✅ Get secrets from Vault (not hardcoded!)
      - name: Get Secrets from Vault
        uses: hashicorp/vault-action@v2
        with:
          url: ${{ secrets.VAULT_ADDR }}
          method: jwt
          role: github-actions
          jwtPayload: ${{ secrets.VAULT_JWT }}
          secrets: |
            secret/data/mercury/db password | DB_PASSWORD ;
            secret/data/mercury/api-key key | API_KEY
      
      # ✅ Deploy with secrets from Vault
      - name: Deploy to Production
        run: |
          docker build -t mercury-backend:${{ github.sha }} .
          docker push gcr.io/myproject/mercury-backend:${{ github.sha }}
          # Deploy with Vault-injected secrets
        env:
          DB_PASSWORD: ${{ env.DB_PASSWORD }}
          API_KEY: ${{ env.API_KEY }}
```

---

## Part 3: Running Everything Locally

### 3.1 Simulate Pre-Commit Locally

```bash
cd /workspaces/Mercury

# Install tools
pip install bandit safety gitleaks

# Run manually
bandit -r backend -ll
safety check -r backend/requirements.txt
gitleaks detect --source .
```

### 3.2 Simulate GitHub Actions Locally

Using **act** to run workflows locally:

```bash
# Install act
brew install act  # macOS
# or
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | bash

# Run CI workflow
act push -j ci

# Run DevSecOps workflow  
act push -j sast
act push -j container
act push -j dast
```

---

## Part 4: Monitoring & Reporting

### 4.1 Security Reports Location

```
/workspaces/Mercury/reports/
├── precommit/          # Pre-commit hook results
│   ├── bandit-*.json
│   └── gitleaks-*.json
├── ci/                 # CI test results
│   ├── pylint.json
│   └── coverage.json
├── devsecops/          # Full security scan
│   ├── bandit.json
│   ├── safety.json
│   ├── trivy.json
│   ├── sbom.json
│   └── zap.json
└── metrics.csv         # Trend analysis
```

### 4.2 Create Dashboard (Optional)

Tools:
- **Grafana** - visualize metrics
- **DefectDojo** - centralize findings
- **Snyk** - continuous monitoring

---

## Part 5: Best Practices

| Pratique | Avantage | Implémentation |
|----------|----------|------------------|
| **Fail-Fast** | Détecter tôt = moins cher à fixer | Pre-commit + CI force-push-blocks |
| **Zero-Trust** | Chaque étape validée indépendamment | Chaque job GitHub Actions vérifie tout |
| **Policy-as-Code** | Règles versionées + auditables | OPA policies dans `/policy` |
| **Artifact Signing** | Garantir intégrité | Docker Content Trust ou Cosign |
| **Ephemeral Secrets** | Jamais en dur | Vault injection au déploiement |
| **SBOM** | Supply chain visibility | Syft génère doc/sbom.json |
| **DAST** | Test réaliste | OWASP ZAP scanne app running |
| **Metrics** | Data-driven security | Safety/Bandit → JSON → trends |

---

## Part 6: Troubleshooting

### Problem: Pre-commit hooks fail

**Solution**:
```bash
# Update pre-commit
pre-commit autoupdate

# Run on all files
pre-commit run --all-files
```

### Problem: Bandit/Safety findings in main branch

**Solution**: Fix before deployment
```bash
# Fix issue
git checkout backend/<file>
# or upgrade dependency
pip install --upgrade <package>
```

### Problem: Workflow timeout in DevSecOps

**Solution**: Optimize
```yaml
# Parallelize jobs in GitHub Actions
# Use matrix for multiple Python versions
# Cache Docker layers
# Use smaller base images
```

---

## Part 7: Checklists for Daily Use

### For Developers (Before Push)

- [ ] Run: `pre-commit run --all-files`
- [ ] Run: `pytest backend/tests`
- [ ] Ensure no new vulnerabilities in `pip install`s
- [ ] Check no secrets in code via Gitleaks

### For CI Pipeline

- [ ] All tests pass
- [ ] Code coverage maintained (>80%)
- [ ] No HIGH/CRITICAL issues from Bandit

### For DevSecOps Pipeline

- [ ] No CRITICAL vulnerabilities from Safety
- [ ] No secrets from Gitleaks
- [ ] Docker image passes Trivy scan
- [ ] OPA policies pass
- [ ] DAST finds no HIGH+ issues

### Before Production Deployment

- [ ] All security gates passed
- [ ] SBOM generated
- [ ] Secrets from Vault only (never hardcoded)
- [ ] Image signed (Docker Content Trust)
- [ ] Deployment logged for audit

---

## Conclusion

Your Mercury backend now has **production-grade DevSecOps**:

✅ **Prevention** (Shift-Left)  
✅ **Detection** (CI/CD)  
✅ **Enforcement** (Policy-as-Code)  
✅ **Response** (Automated blocks)  

**Next Step**: Deploy to production using Vault + signed images.

