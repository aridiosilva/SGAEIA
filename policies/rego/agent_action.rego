package sgaeia.agent_action

default allow := false

deny contains "unknown_or_disabled_agent" if {
  not input.agent.registered
}

deny contains "invalid_identity" if {
  not input.agent.identity_valid
}

deny contains "forbidden_l4_a5" if {
  input.agent.class == "L4"
  input.agent.autonomy == "A5"
}

deny contains "capability_not_granted" if {
  not input.operation in input.agent.capabilities
}

deny contains "delegation_depth_exceeded" if {
  input.delegation_depth > input.agent.max_delegation_depth
}

deny contains "offline_critical_action" if {
  input.offline
  input.critical
}

allow if {
  count(deny) == 0
  input.risk_score < 61
}
