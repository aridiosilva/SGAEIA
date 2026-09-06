module sgaeia

abstract sig Class {}
one sig L0,L1,L2,L3,L4 extends Class {}
abstract sig Autonomy {}
one sig A0,A1,A2,A3,A4,A5 extends Autonomy {}

sig Capability {}

sig Agent {
  klass: one Class,
  autonomy: one Autonomy,
  caps: set Capability,
  delegatesTo: set Agent,
  delegatedCaps: Agent -> set Capability
}

fact NoSelfDelegation {
  no a: Agent | a in a.delegatesTo
}

fact DelegationDoesNotIncreaseAuthority {
  all parent, child: Agent |
    child in parent.delegatesTo implies parent.delegatedCaps[child] in parent.caps
}

pred ForbiddenL4A5[a: Agent] {
  a.klass = L4 and a.autonomy = A5
}

assert NoDelegatedCapabilityOutsideParent {
  all parent, child: Agent |
    child in parent.delegatesTo implies no (parent.delegatedCaps[child] - parent.caps)
}

check NoDelegatedCapabilityOutsideParent for 6 Agent, 8 Capability

run { some a: Agent | ForbiddenL4A5[a] } for 5 Agent
