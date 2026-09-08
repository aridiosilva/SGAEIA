# Alien Cognition and Architectural Assurance

## Normative premise

SGAEIA SHALL treat model outputs, explanations and reasoning traces as untrusted
inputs. This premise does not assert consciousness. It acknowledges that learned
strategies may remain opaque, may generalize unexpectedly and may differ from
their verbal description.

## Control loop

1. A registered agent proposes a typed intent.
2. The PEP intercepts it before external effect.
3. The PDP evaluates identity, capability, delegation, budgets, risk and protected targets.
4. An independent monitor evaluates critical actions and expected effects.
5. Human approval is requested when required by risk and autonomy policy.
6. Execution occurs through a bounded adapter.
7. Observed effects are correlated with intent and monitor expectation.
8. Divergence triggers deny, quarantine, revocation or rollback.
9. Evidence is retained without granting the controlled agent deletion authority.

## Trusted context boundary

The requesting agent supplies only the intended operation, resource, trace and
references to registered delegation grants. Criticality, protected-target
classification, risk, assurance, runtime counters, monitor decisions and human
approvals SHALL be resolved by the SGAEIA control plane. Unknown fields at the
public authorization boundary are rejected. Missing assurance is zero assurance;
it never inherits maximum trust.

Monitor decisions and human approvals SHALL be registered, signature-valid,
time-bounded and bound to the same subject agent, trace, operation and resource.
An identifier chosen by the requesting agent is not evidence of independence.

## Pre-action and post-effect separation

Authorization and effect reconciliation are distinct phases. A pre-action
decision cannot claim knowledge of an effect that has not occurred. After
execution, a separately identified observer submits a signed, bound effect
record. Divergence causes denial of reconciliation and immediate revocation in
the reference implementation. Both decisions are added to the local digest
chain.

## Capability-gated autonomy

The effective autonomy ceiling is the minimum of model capability assurance,
monitoring assurance, containment assurance and recovery assurance. Loss or
staleness of any required assurance input SHALL preserve or reduce authority.

## Recursive change governance

Changes affecting agent capabilities, model configuration, policy, monitoring,
evidence or containment SHALL use a separately governed path. The proposing
agent cannot be the sole approver or deployer. Production admission requires
staged validation, rollback and preserved evidence.

## Reference implementation boundary

The in-memory trusted-context, monitor, approval and grant stores demonstrate
the required separation of duties. Production deployments SHALL replace them
with authenticated control-plane adapters and cryptographic verification. The
local digest chain detects record mutation when retained as a whole, but does
not claim external anchoring, durable append-only storage or independent
signature assurance.
