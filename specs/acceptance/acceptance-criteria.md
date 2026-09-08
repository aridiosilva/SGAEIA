# Acceptance Criteria

## AC-001 Unknown agent
Given an unregistered agent, when it requests any operation, then authorization MUST be denied.

## AC-002 Invalid identity
Given a registered agent with invalid workload identity state, when it requests an allowed capability, then authorization MUST be denied.

## AC-003 Capability enforcement
Given a valid agent, when it requests an operation outside its allow-list or inside its deny-list, then authorization MUST be denied.

## AC-004 Delegation containment
Given a parent agent, when requested delegated capabilities are not a subset of the parent's granted capabilities, then delegation MUST be denied.

## AC-005 L4 autonomy ceiling
Given an L4 agent configured at A5, any sensitive authorization MUST be denied until configuration is corrected.

## AC-006 Offline fail-secure
Given offline mode and a critical operation, authorization MUST be denied unless a domain-specific approved safety profile explicitly supersedes the reference rule.

## AC-007 Segregation of duties
Given a critical transaction where creator and approver identities are the same, authorization MUST be denied.

## AC-008 Physical actuation classification
Given a physical actuation request by a non-L4 agent, authorization MUST be denied.

## AC-009 High risk
Given a risk score above the configured autonomous threshold, the system MUST require approval, quarantine or deny rather than silently execute.

## AC-010 Evidence
Every authorization result MUST include a trace id, evidence id, decision, risk score, reasons and integrity digest.

## AC-011 Adapter binding
Given a production adapter profile, it MUST bind to an existing Integration Port and declare implementation/version, assurance target, failure mode and evidence requirements.

## AC-012 Vendor-neutral substitution
Given two adapters for the same Integration Port, both MUST be testable against the same port-level semantic conformance rules regardless of vendor-specific API differences.

## AC-013 Assurance scope
Given a local contract-harness result, the project MUST identify it as harness-level evidence and MUST NOT represent it as live-product IPS-C2/C3 certification.

## AC-014 Adapter fail-safe
Given loss of a critical adapter dependency, the resulting behavior MUST NOT increase authority, bypass policy or silently discard required critical evidence.

## AC-015 Untrusted reasoning
Given an otherwise permitted operation relying only on model reasoning or explanation for authorization, the operation MUST be denied.

## AC-016 Independent monitoring
Given a critical action, authorization MUST require a valid monitor decision whose identity differs from the controlled agent.

## AC-017 Capability-gated autonomy
Given an autonomy level above monitoring, containment or recovery assurance, authorization MUST fail closed or reduce autonomy before execution.

## AC-018 Protected control plane
Given ordinary agent authority, attempts to modify policy, monitoring, evidence, identity or kill-switch controls MUST be denied.

## AC-019 Collective authority
Given a set of individually permissible agent contributions whose combined capabilities form a prohibited set, the collective action MUST be denied.

## AC-020 Bounded execution
Given runtime, tool-call or network-reach consumption above an agent budget, the action MUST be denied or quarantined.
