from sgaeia.models import Agent, Intent, RiskContext
from sgaeia.policy import PolicyEngine

def mk(**kw):
    base=dict(id="a",owner="o",klass="L2",autonomy="A2",trust_zone="ATZ-3",spiffe_id="spiffe://x/a",capabilities=frozenset({"read","actuator.write"}),denied_capabilities=frozenset(),delegation_allowed=False,max_delegation_depth=0,kill_switch_required=True,enabled=True,identity_valid=True,attested=True)
    base.update(kw); return Agent(**base)

def intent(**kw):
    base=dict(agent_id="a",operation="read",resource="r",trace_id="t")
    base.update(kw); return Intent(**base)

def test_unknown_agent_denied():
    d=PolicyEngine().authorize(None,intent(),RiskContext())
    assert not d.allow

def test_invalid_identity_denied():
    d=PolicyEngine().authorize(mk(identity_valid=False),intent(),RiskContext())
    assert not d.allow and "invalid_identity" in d.reasons

def test_l4_a5_denied():
    d=PolicyEngine().authorize(mk(klass="L4",autonomy="A5"),intent(),RiskContext())
    assert not d.allow and "forbidden_l4_a5" in d.reasons

def test_offline_critical_denied():
    d=PolicyEngine().authorize(mk(),intent(offline=True,critical=True),RiskContext())
    assert not d.allow and "offline_critical_action_denied" in d.reasons

def test_sod_violation_denied():
    d=PolicyEngine().authorize(mk(),intent(critical=True,creator_id="same",approver_id="same"),RiskContext())
    assert not d.allow and "segregation_of_duties_violation" in d.reasons

def test_physical_action_requires_l4():
    d=PolicyEngine().authorize(mk(klass="L2"),intent(operation="actuator.write",physical_actuation=True),RiskContext())
    assert not d.allow and "physical_actuation_requires_l4_classification" in d.reasons
