graph LR
    A["🖥️ Developer<br/>(Local Machine)"] -->|"write code"| B["📝 Code<br/>(Backend Files)"]
    
    B -->|"pre-commit<br/>hooks trigger"| C["🔐 SHIFT-LEFT<br/>(Local Security)"]
    
    C -->|"✅ Bandit<br/>✅ Gitleaks<br/>✅ Black"| D{"Issues?"}
    
    D -->|"❌ YES"| E["🚫 BLOCKED<br/>Developer fixes"]
    E -->|"fix code"| B
    
    D -->|"✅ NO"| F["📤 git push<br/>to GitHub"]
    
    F -->|"trigger"| G["🔄 CI Pipeline<br/>(GitHub Actions)"]
    G -->|"✅ Pylint<br/>✅ Pytest<br/>✅ Coverage"| H{"Tests Pass?"}
    
    H -->|"❌ NO"| I["🚫 BLOCKED<br/>PR Comment"]
    I -->|"fix"| B
    
    H -->|"✅ YES"| J["✅ CI SUCCESS"]
    
    J -->|"trigger"| K["🛡️ DevSecOps<br/>Pipeline"]
    
    K -->|"SAST"| K1["Bandit<br/>Safety"]
    K -->|"Secrets"| K2["Gitleaks"]
    K -->|"Container"| K3["Trivy<br/>Syft"]
    K -->|"Dynamic"| K4["OWASP ZAP"]
    K -->|"Policies"| K5["OPA"]
    
    K1 & K2 & K3 & K4 & K5 -->|"Any CRITICAL?"| L{"Vulnerabilities?"}
    
    L -->|"❌ YES"| M["🚫 BLOCKED<br/>Fix before merge"]
    M -->|"fix"| B
    
    L -->|"✅ NO"| N["✅ MERGE<br/>to main"]
    
    N -->|"trigger"| O["📦 Build & Deploy"]
    O -->|"Vault Secrets<br/>Signed Image"| P["🚀 Production<br/>(Secure)"]
    
    style C fill:#90EE90
    style G fill:#87CEEB
    style K fill:#FFB6C1
    style P fill:#FFD700
