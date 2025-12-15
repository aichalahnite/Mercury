package docker.security

deny[msg] {
  input.config.User == "root"
  msg := "Docker image must not run as root"
}

deny[msg] {
  not input.config.Healthcheck
  msg := "Docker image must define HEALTHCHECK"
}
