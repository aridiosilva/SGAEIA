from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from .assurance import PROTECTED_TARGETS, TrustedAuthorizationContext
from .collective import evaluate_collective_action
from .delegation import validate_delegation_chain
from .models import Agent, Intent, MonitorDecision, HumanApproval, AUTONOMY_LEVEL
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

    @staticmethod
    def _active_window(issued_at: str, expires_at: str) -> bool:
        try:
            issued = datetime.fromisoformat(issued_at.replace("Z", "+00:00"))
            expires = datetime.fromisoformat(expires_at.replace("Z", "+00:00"))
        except (AttributeError, TypeError, ValueError):
            return False
        if issued.tzinfo is None or expires.tzinfo is None:
            return False
        now = datetime.now(timezone.utc)
        return issued <= now < expires

    def _monitor_valid(self, monitor: MonitorDecision | None, registered: bool,
                       agent: Agent, intent: Intent) -> tuple[bool, str]:
        if monitor is None: return False, "independent_monitor_required"
        if not registered: return False, "monitor_not_registered"
        if not monitor.valid or not monitor.signature_valid: return False, "monitor_decision_invalid"
        if monitor.monitor_id == agent.id: return False, "monitor_not_independent"
        if monitor.subject_agent_id != agent.id: return False, "monitor_subject_mismatch"
        if (monitor.trace_id, monitor.operation, monitor.resource) != (intent.trace_id, intent.operation, intent.resource):
            return False, "monitor_binding_mismatch"
        if not self._active_window(monitor.issued_at, monitor.expires_at): return False, "monitor_expired_or_not_yet_valid"
        if not monitor.allow: return False, "monitor_denied"
        return True, "monitor_valid"

    def _approval_valid(self, approval: HumanApproval | None, registered: bool,
                        agent: Agent, intent: Intent) -> tuple[bool, str]:
        if approval is None: return False, "human_approval_required"
        if not registered: return False, "approver_not_registered"
        if not (approval.valid and approval.informed and approval.revocable_before_effect and approval.signature_valid):
            return False, "human_approval_invalid"
        if approval.approver_id == agent.id: return False, "approver_not_independent"
        if approval.subject_agent_id != agent.id: return False, "approval_subject_mismatch"
        if (approval.trace_id, approval.operation, approval.resource) != (intent.trace_id, intent.operation, intent.resource):
            return False, "approval_binding_mismatch"
        if not self._active_window(approval.issued_at, approval.expires_at): return False, "approval_expired_or_not_yet_valid"
        return True, "approval_valid"

    def authorize(self, agent: Agent | None, intent: Intent,
                  ctx: TrustedAuthorizationContext) -> Decision:
        reasons: list[str] = []
        if agent is None:
            return Decision(False, "DENY", 100, ("unknown_agent",))
        if not isinstance(ctx, TrustedAuthorizationContext) or not ctx.trusted or ctx.source != "sgaeia-control-plane":
            return Decision(False, "DENY", 100, ("untrusted_authorization_context",))
        policy = ctx.policy
        if not agent.enabled or self.kill_switch.is_revoked(agent.id): reasons.append("agent_disabled_or_revoked")
        if not agent.identity_valid: reasons.append("invalid_identity")
        if not agent.spiffe_id.startswith("spiffe://"): reasons.append("invalid_workload_identity")
        if agent.klass in {"L3","L4"} and not agent.attested: reasons.append("critical_agent_attestation_failed")
        if agent.klass == "L4" and agent.autonomy == "A5": reasons.append("forbidden_l4_a5")
        if intent.operation not in agent.capabilities: reasons.append("capability_not_granted")
        if intent.operation in agent.denied_capabilities: reasons.append("capability_explicitly_denied")
        if ctx.delegation_error: reasons.append(ctx.delegation_error)
        if intent.delegation_chain:
            valid, reason = validate_delegation_chain(agent, ctx.delegation_chain, intent.operation, intent.resource)
            if not valid: reasons.append(reason)
        if ctx.offline and policy.critical: reasons.append("offline_critical_action_denied")
        if policy.physical_actuation and agent.klass != "L4": reasons.append("physical_actuation_requires_l4_classification")
        if policy.reasoning_only_authorization: reasons.append("reasoning_is_non_authoritative")
        if policy.target_kind in PROTECTED_TARGETS:
            reasons.append("protected_control_change_requires_governed_path")
        if ctx.observed_runtime_seconds > agent.max_runtime_seconds: reasons.append("runtime_budget_exceeded")
        if ctx.observed_tool_calls > agent.max_tool_calls: reasons.append("tool_call_budget_exceeded")
        if ctx.observed_network_reach > agent.max_network_reach: reasons.append("network_reach_budget_exceeded")
        if ctx.collective_contributions:
            ok, reason = evaluate_collective_action(ctx.collective_contributions,
                ctx.prohibited_capability_sets, ctx.aggregate_impact_limit)
            if not ok: reasons.append(reason)

        assurance_ceiling = min(policy.monitor_assurance, policy.containment_assurance,
                                policy.recovery_assurance, agent.capability_assurance_level)
        if AUTONOMY_LEVEL.get(agent.autonomy, 99) > assurance_ceiling:
            reasons.append("autonomy_exceeds_assurance_ceiling")

        if policy.critical:
            ok, reason = self._monitor_valid(ctx.monitor, ctx.monitor_registered, agent, intent)
            if not ok: reasons.append(reason)

        score = self.risk.score(agent, policy.risk)
        disp = self.risk.disposition(score)

        if reasons:
            return Decision(False, "DENY", score, tuple(reasons))
        if disp in {"DENY_REVOKE","QUARANTINE"}:
            return Decision(False, disp, score, ("risk_threshold",))
        approval_required = disp == "REQUIRE_APPROVAL" or policy.self_affecting_change or (agent.klass == "L4" and policy.physical_actuation)
        if approval_required:
            ok, reason = self._approval_valid(ctx.approval, ctx.approval_registered, agent, intent)
            if not ok: return Decision(False, "REQUIRE_APPROVAL", score, (reason,))
        return Decision(True, disp, score, ("policy_satisfied",))
