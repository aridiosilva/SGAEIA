from sgaeia.collective import AgentContribution, evaluate_collective_action
from sgaeia.models import Agent, Intent, MonitorDecision, RiskContext
from sgaeia.policy import PolicyEngine

def agent(**changes):
    values = dict(id="agent-a", owner="owner", klass="L3", autonomy="A2",
                  trust_zone="ATZ-3", spiffe_id="spiffe://sgaeia/agent-a",
                  capabilities=frozenset({"code.write", "deploy.execute"}),
                  max_delegation_depth=2)
    values.update(changes)
    return Agent(**values)

def test_reasoning_cannot_authorize_action():
    intent = Intent("agent-a", "code.write", "repo", "t1", reasoning_only_authorization=True)
    decision = PolicyEngine().authorize(agent(), intent, RiskContext())
    assert not decision.allow and "reasoning_is_non_authoritative" in decision.reasons

def test_agent_cannot_modify_protected_monitor():
    intent = Intent("agent-a", "code.write", "monitor", "t2", target_kind="monitor")
    decision = PolicyEngine().authorize(agent(), intent, RiskContext())
    assert not decision.allow and "protected_control_change_requires_governed_path" in decision.reasons

def test_critical_action_requires_independent_monitor():
    intent = Intent("agent-a", "deploy.execute", "prod", "t3", critical=True, human_approvals=1)
    missing = PolicyEngine().authorize(agent(), intent, RiskContext())
    same_agent = PolicyEngine().authorize(agent(), intent, RiskContext(), MonitorDecision("agent-a", True))
    valid = PolicyEngine().authorize(agent(), intent, RiskContext(), MonitorDecision("monitor-b", True))
    assert not missing.allow
    assert not same_agent.allow
    assert valid.allow

def test_action_effect_divergence_fails_closed():
    intent = Intent("agent-a", "deploy.execute", "prod", "t4", critical=True, human_approvals=1)
    monitor = MonitorDecision("monitor-b", True, divergence_detected=True)
    decision = PolicyEngine().authorize(agent(), intent, RiskContext(), monitor)
    assert not decision.allow and "action_effect_divergence" in decision.reasons

def test_autonomy_is_capped_by_assurance():
    intent = Intent("agent-a", "code.write", "repo", "t5")
    decision = PolicyEngine().authorize(agent(autonomy="A4"), intent,
        RiskContext(monitor_assurance=2, containment_assurance=4, recovery_assurance=3))
    assert not decision.allow and "autonomy_exceeds_assurance_ceiling" in decision.reasons

def test_execution_budgets_fail_closed():
    intent = Intent("agent-a", "code.write", "repo", "t6", observed_tool_calls=51)
    decision = PolicyEngine().authorize(agent(max_tool_calls=50), intent, RiskContext())
    assert not decision.allow and "tool_call_budget_exceeded" in decision.reasons

def test_collective_privilege_aggregation_is_denied():
    contributions = (
        AgentContribution("a", frozenset({"credential.read"}), "read", 2),
        AgentContribution("b", frozenset({"external.write"}), "send", 2),
    )
    ok, reason = evaluate_collective_action(contributions,
        (frozenset({"credential.read", "external.write"}),), 10)
    assert not ok and reason == "collective_privilege_aggregation"
