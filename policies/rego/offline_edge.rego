package sgaeia.offline_edge

default allow := false

allow if {
  input.offline == true
  input.operation in input.cached_safe_operations
  input.risk_score < 41
  input.critical == false
}
