# Shift-Left Security

## Objective
Prevent vulnerabilities before code is merged.

## Implementation

### Pre-Commit Hooks
Executed locally before every commit.

| Tool | Control |
|----|----|
| Bandit | Python SAST |
| Gitleaks | Secrets detection |
| Black | Formatting standard |

### Why Shift-Left?
- Cheaper to fix
- Faster feedback
- Prevents security debt

### Failure Behavior
- Commit is blocked
- Developer must fix before commit
