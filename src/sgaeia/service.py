from pathlib import Path
from .registry import AgentRegistry
from .policy import PolicyEngine
from .models import Intent, RiskContext, MonitorDecision
from .evidence import make_evidence

class AuthorizationService:
    def __init__(self, registry: AgentRegistry, policy: PolicyEngine | None = None):
        self.registry = registry
        self.policy = policy or PolicyEngine()

    def authorize(self, intent: Intent, risk_context: RiskContext,
                  monitor: MonitorDecision | None = None):
        agent = self.registry.get(intent.agent_id)
        decision = self.policy.authorize(agent, intent, risk_context, monitor)
        ev = make_evidence(trace_id=intent.trace_id, agent_id=intent.agent_id,
                           operation=intent.operation, resource=intent.resource,
                           decision=decision.action, risk_score=decision.risk_score,
                           reasons=list(decision.reasons),
                           monitor_id=monitor.monitor_id if monitor else "",
                           policy_version=monitor.policy_version if monitor else "unknown",
                           proposed_action=f"{intent.operation}:{intent.resource}",
                           observed_effect=monitor.observed_effect if monitor else "")
        return decision, ev
