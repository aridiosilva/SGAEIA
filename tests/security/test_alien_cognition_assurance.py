from datetime import datetime, timedelta, timezone

from sgaeia.assurance import OperationPolicy, TrustedAuthorizationContext, TrustedContextProvider
from sgaeia.collective import AgentContribution
from sgaeia.delegation import DelegationGrant
from sgaeia.models import Agent, HumanApproval, Intent, MonitorDecision, ObservedEffect
from sgaeia.policy import PolicyEngine
from sgaeia.registry import AgentRegistry
from sgaeia.service import AuthorizationService


def agent(**changes):
    values = dict(id="agent-a", owner="owner", klass="L3", autonomy="A2",
                  trust_zone="ATZ-3", spiffe_id="spiffe://sgaeia/agent-a",
                  capabilities=frozenset({"code.write", "deploy.execute"}),
                  max_delegation_depth=2, capability_assurance_level=4)
    values.update(changes)
    return Agent(**values)


def policy(**changes):
    values = dict(monitor_assurance=4, containment_assurance=4, recovery_assurance=4)
    values.update(changes)
    return OperationPolicy(**values)


def context(op_policy=None, **changes):
    values = dict(source="sgaeia-control-plane", issued_at=datetime.now(timezone.utc).isoformat(),
                  trusted=True, policy=op_policy or policy())
    values.update(changes)
    return TrustedAuthorizationContext(**values)


def monitor(intent, **changes):
    now = datetime.now(timezone.utc)
    values = dict(monitor_id="monitor-b", subject_agent_id=intent.agent_id,
                  trace_id=intent.trace_id, operation=intent.operation, resource=intent.resource,
                  allow=True, valid=True, policy_version="rc2",
                  issued_at=(now-timedelta(minutes=1)).isoformat(),
                  expires_at=(now+timedelta(minutes=5)).isoformat(),
                  signature_valid=True, trust_domain="monitoring")
    values.update(changes)
    return MonitorDecision(**values)


def approval(intent, **changes):
    now = datetime.now(timezone.utc)
    values = dict(approver_id="human-b", subject_agent_id=intent.agent_id,
                  trace_id=intent.trace_id, operation=intent.operation, resource=intent.resource,
                  informed=True, valid=True, revocable_before_effect=True,
                  issued_at=(now-timedelta(minutes=1)).isoformat(),
                  expires_at=(now+timedelta(minutes=5)).isoformat(), signature_valid=True)
    values.update(changes)
    return HumanApproval(**values)


def test_untrusted_context_fails_closed():
    intent = Intent("agent-a", "code.write", "repo", "t0")
    decision = PolicyEngine().authorize(agent(), intent,
        TrustedAuthorizationContext("client", "", False, policy()))
    assert not decision.allow and "untrusted_authorization_context" in decision.reasons


def test_reasoning_cannot_authorize_action():
    intent = Intent("agent-a", "code.write", "repo", "t1")
    decision = PolicyEngine().authorize(agent(), intent,
        context(policy(reasoning_only_authorization=True)))
    assert not decision.allow and "reasoning_is_non_authoritative" in decision.reasons


def test_protected_target_is_derived_server_side():
    provider = TrustedContextProvider({"code.write": policy()})
    intent = Intent("agent-a", "code.write", "monitor:primary", "t2", target_kind="resource")
    decision = PolicyEngine().authorize(agent(), intent, provider.resolve(intent, agent()))
    assert not decision.allow and "protected_control_change_requires_governed_path" in decision.reasons


def test_criticality_cannot_be_weakened_by_intent():
    provider = TrustedContextProvider({"deploy.execute": policy(critical=True)})
    intent = Intent("agent-a", "deploy.execute", "prod", "t3", critical=False)
    decision = PolicyEngine().authorize(agent(), intent, provider.resolve(intent, agent()))
    assert not decision.allow and "independent_monitor_required" in decision.reasons


def test_unregistered_monitor_is_denied():
    intent = Intent("agent-a", "deploy.execute", "prod", "t4")
    candidate = monitor(intent)
    decision = PolicyEngine().authorize(agent(), intent,
        context(policy(critical=True), monitor=candidate, monitor_registered=False))
    assert not decision.allow and "monitor_not_registered" in decision.reasons


def test_registered_bound_monitor_allows_critical_action():
    intent = Intent("agent-a", "deploy.execute", "prod", "t5")
    decision = PolicyEngine().authorize(agent(), intent,
        context(policy(critical=True), monitor=monitor(intent), monitor_registered=True))
    assert decision.allow


def test_monitor_replay_binding_is_denied():
    intent = Intent("agent-a", "deploy.execute", "prod", "t6")
    decision = PolicyEngine().authorize(agent(), intent,
        context(policy(critical=True), monitor=monitor(intent, trace_id="old-trace"), monitor_registered=True))
    assert not decision.allow and "monitor_binding_mismatch" in decision.reasons


def test_missing_assurance_defaults_fail_closed():
    intent = Intent("agent-a", "code.write", "repo", "t7")
    decision = PolicyEngine().authorize(agent(autonomy="A1"), intent, context(OperationPolicy()))
    assert not decision.allow and "autonomy_exceeds_assurance_ceiling" in decision.reasons


def test_runtime_counters_come_from_trusted_context():
    intent = Intent("agent-a", "code.write", "repo", "t8", observed_tool_calls=0)
    decision = PolicyEngine().authorize(agent(max_tool_calls=50), intent,
        context(observed_tool_calls=51))
    assert not decision.allow and "tool_call_budget_exceeded" in decision.reasons


def test_self_affecting_change_requires_registered_approval():
    intent = Intent("agent-a", "code.write", "repo", "t9")
    missing = PolicyEngine().authorize(agent(), intent, context(policy(self_affecting_change=True)))
    valid = PolicyEngine().authorize(agent(), intent,
        context(policy(self_affecting_change=True), approval=approval(intent), approval_registered=True))
    assert not missing.allow and valid.allow


def test_delegation_chain_is_integrated_and_invalid_expiry_denies():
    intent = Intent("agent-a", "code.write", "repo", "t10", delegation_chain=("g1",))
    grant = DelegationGrant("g1", "agent-a", "child", frozenset({"code.write"}), "repo", "bad-date",
                            signature_valid=True)
    decision = PolicyEngine().authorize(agent(), intent, context(delegation_chain=(grant,)))
    assert not decision.allow and "delegation_expiry_invalid" in decision.reasons


def test_collective_privilege_aggregation_is_integrated():
    intent = Intent("agent-a", "code.write", "repo", "t11")
    contributions = (AgentContribution("a", frozenset({"credential.read"}), "read", 2),
                     AgentContribution("b", frozenset({"external.write"}), "send", 2))
    decision = PolicyEngine().authorize(agent(), intent, context(
        collective_contributions=contributions,
        prohibited_capability_sets=(frozenset({"credential.read", "external.write"}),),
        aggregate_impact_limit=10))
    assert not decision.allow and "collective_privilege_aggregation" in decision.reasons


def test_collective_task_cycle_is_denied():
    intent = Intent("agent-a", "code.write", "repo", "t11-cycle")
    contributions = (
        AgentContribution("a", frozenset({"read"}), "read", depends_on=frozenset({"b"})),
        AgentContribution("b", frozenset({"write"}), "write", depends_on=frozenset({"a"})),
    )
    decision = PolicyEngine().authorize(agent(), intent, context(
        collective_contributions=contributions, aggregate_impact_limit=10))
    assert not decision.allow and "collective_task_cycle" in decision.reasons


def test_post_effect_divergence_revokes_agent():
    reg = AgentRegistry(); reg.register(agent())
    service = AuthorizationService(reg, contexts=TrustedContextProvider({"deploy.execute": policy()}))
    intent = Intent("agent-a", "deploy.execute", "prod", "t12")
    effect = ObservedEffect("observer-c", "agent-a", "t12", "deploy.execute", "prod",
                            "deployment:v1", "deployment:v2", True)
    ok, reason = service.reconcile_effect(intent, effect)
    assert not ok and reason == "action_effect_divergence"
    assert service.policy.kill_switch.is_revoked("agent-a")


def test_post_effect_record_must_match_authorized_trace():
    reg = AgentRegistry(); reg.register(agent())
    service = AuthorizationService(reg, contexts=TrustedContextProvider({"deploy.execute": policy()}))
    intent = Intent("agent-a", "deploy.execute", "prod", "t13")
    effect = ObservedEffect("observer-c", "agent-a", "different-trace", "deploy.execute",
                            "prod", "deployment:v1", "deployment:v1", True)
    ok, reason = service.reconcile_effect(intent, effect)
    assert not ok and reason == "effect_binding_mismatch"
