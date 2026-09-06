from __future__ import annotations
from dataclasses import dataclass
from .models import Agent, Intent, RiskContext
from .risk_engine import RiskEngine
from .kill_switch import KillSwitch

@dataclass(frozen=True)
class Decision:
    allow: bool
    action: str
    risk_score: int
    reasons: tuple[str, ...]

class PolicyEngine:
    def __init__(self, risk_engine: RiskEngine | None = None, kill_switch: KillSwitch | None = None):
        self.risk = risk_engine or RiskEngine()
        self.kill_switch = kill_switch or KillSwitch()

    def authorize(self, agent: Agent | None, intent: Intent, ctx: RiskContext) -> Decision:
        reasons: list[str] = []
        if agent is None:
            return Decision(False, "DENY", 100, ("unknown_agent",))
        if not agent.enabled or self.kill_switch.is_revoked(agent.id): reasons.append("agent_disabled_or_revoked")
        if not agent.identity_valid: reasons.append("invalid_identity")
        if not agent.spiffe_id.startswith("spiffe://"): reasons.append("invalid_workload_identity")
        if agent.klass in {"L3","L4"} and not agent.attested: reasons.append("critical_agent_attestation_failed")
        if agent.klass == "L4" and agent.autonomy == "A5": reasons.append("forbidden_l4_a5")
        if intent.operation not in agent.capabilities: reasons.append("capability_not_granted")
        if intent.operation in agent.denied_capabilities: reasons.append("capability_explicitly_denied")
        if intent.delegation_depth > agent.max_delegation_depth: reasons.append("delegation_depth_exceeded")
        if intent.creator_id and intent.approver_id and intent.creator_id == intent.approver_id and intent.critical:
            reasons.append("segregation_of_duties_violation")
        if intent.offline and intent.critical: reasons.append("offline_critical_action_denied")
        if intent.physical_actuation and agent.klass != "L4": reasons.append("physical_actuation_requires_l4_classification")

        score = self.risk.score(agent, ctx)
        disp = self.risk.disposition(score)

        if reasons:
            return Decision(False, "DENY", score, tuple(reasons))
        if disp in {"DENY_REVOKE","QUARANTINE"}:
            return Decision(False, disp, score, ("risk_threshold",))
        if disp == "REQUIRE_APPROVAL" and intent.human_approvals < 1:
            return Decision(False, "REQUIRE_APPROVAL", score, ("human_approval_required",))
        if agent.klass == "L4" and intent.physical_actuation and intent.human_approvals < 1:
            return Decision(False, "REQUIRE_APPROVAL", score, ("l4_physical_action_requires_approval",))
        return Decision(True, disp, score, ("policy_satisfied",))
