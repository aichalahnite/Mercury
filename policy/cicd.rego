package cicd.security

deny[msg] {
  input.trivy.critical > 0
  msg := "Critical vulnerabilities found"
}

deny[msg] {
  input.secrets_detected == true
  msg := "Secrets detected in repository"
}
