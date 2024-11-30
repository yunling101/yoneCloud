connect {
  enabled = false
}

acl {
  enabled = true
  default_policy = "deny"
  down_policy = "extend-cache"
}

bootstrap = true