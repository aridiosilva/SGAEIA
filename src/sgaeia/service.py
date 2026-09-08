from pathlib import Path
from .registry import AgentRegistry
from .policy import PolicyEngine
from .assurance import TrustedContextProvider
from .models import Intent, ObservedEffect
from .evidence import make_evidence

class AuthorizationService:
    def __init__(self, registry: AgentRegistry, policy: PolicyEngine | None = None,
                 contexts: TrustedContextProvider | None = None):
        self.registry = registry
        self.policy = policy or PolicyEngine()
        self.contexts = contexts or TrustedContextProvider()
        self._last_digest = ""
        self.effect_evidence = []

    def authorize(self, intent: Intent):
        agent = self.registry.get(intent.agent_id)
        context = self.contexts.resolve(intent, agent)
        decision = self.policy.authorize(agent, intent, context)
        ev = make_evidence(trace_id=intent.trace_id, agent_id=intent.agent_id,
                           operation=intent.operation, resource=intent.resource,
                           decision=decision.action, risk_score=decision.risk_score,
                           reasons=list(decision.reasons),
                           monitor_id=context.monitor.monitor_id if context.monitor else "",
                           policy_version=context.monitor.policy_version if context.monitor else "unknown",
                           proposed_action=f"{intent.operation}:{intent.resource}",
                           observed_effect="", previous_digest=self._last_digest)
        self._last_digest = ev.digest
        return decision, ev

    def reconcile_effect(self, intent: Intent, effect: ObservedEffect):
        if not effect.signature_valid:
            outcome = (False, "effect_observer_signature_invalid")
        elif (effect.subject_agent_id, effect.trace_id, effect.operation, effect.resource) != (
                intent.agent_id, intent.trace_id, intent.operation, intent.resource):
            outcome = (False, "effect_binding_mismatch")
        elif effect.expected_effect != effect.observed_effect:
            self.policy.kill_switch.revoke(intent.agent_id)
            outcome = (False, "action_effect_divergence")
        else:
            outcome = (True, "effect_reconciled")
        ev = make_evidence(
            trace_id=intent.trace_id, agent_id=intent.agent_id,
            operation=f"{intent.operation}.effect_reconciliation", resource=intent.resource,
            decision="RECONCILED" if outcome[0] else "DENY_REVOKE", risk_score=0,
            reasons=[outcome[1]], monitor_id=effect.observer_id,
            proposed_action=effect.expected_effect, observed_effect=effect.observed_effect,
            previous_digest=self._last_digest)
        self._last_digest = ev.digest
        self.effect_evidence.append(ev)
        return outcome
