package sgaeia.delegation

default allow := false

allow if {
  input.parent.delegation_allowed
  input.depth <= input.parent.max_depth
  every cap in input.child_requested_capabilities {
    cap in input.parent_delegated_capabilities
  }
}
