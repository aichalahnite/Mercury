package docker.security

deny contains msg if {
  input[0].Config.User == ""  # empty means root
  msg := "Docker image must not run as root"
}

deny contains msg if {
  not input[0].Config.Healthcheck
  msg := "Docker image must define HEALTHCHECK"
}
