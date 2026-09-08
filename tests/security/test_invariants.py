from datetime import datetime, timezone
from sgaeia.models import Agent, Intent, RiskContext
from sgaeia.assurance import OperationPolicy, TrustedAuthorizationContext
from sgaeia.policy import PolicyEngine

def mk(**kw):
    base=dict(id="a",owner="o",klass="L2",autonomy="A2",trust_zone="ATZ-3",spiffe_id="spiffe://x/a",capabilities=frozenset({"read","actuator.write"}),denied_capabilities=frozenset(),delegation_allowed=False,max_delegation_depth=0,kill_switch_required=True,enabled=True,identity_valid=True,attested=True)
    base.update(kw); return Agent(**base)

def intent(**kw):
    base=dict(agent_id="a",operation="read",resource="r",trace_id="t")
    base.update(kw); return Intent(**base)

def ctx(intent_obj=None, **kw):
    i=intent_obj or intent()
    p=OperationPolicy(
        critical=i.critical, physical_actuation=i.physical_actuation,
        monitor_assurance=5, containment_assurance=5, recovery_assurance=5,
        risk=RiskContext())
    base=dict(source="sgaeia-control-plane",issued_at=datetime.now(timezone.utc).isoformat(),trusted=True,policy=p,offline=i.offline)
    base.update(kw); return TrustedAuthorizationContext(**base)

def test_unknown_agent_denied():
    i=intent(); d=PolicyEngine().authorize(None,i,ctx(i))
    assert not d.allow

def test_invalid_identity_denied():
    i=intent(); d=PolicyEngine().authorize(mk(identity_valid=False),i,ctx(i))
    assert not d.allow and "invalid_identity" in d.reasons

def test_l4_a5_denied():
    i=intent(); d=PolicyEngine().authorize(mk(klass="L4",autonomy="A5"),i,ctx(i))
    assert not d.allow and "forbidden_l4_a5" in d.reasons

def test_offline_critical_denied():
    i=intent(offline=True,critical=True); d=PolicyEngine().authorize(mk(),i,ctx(i))
    assert not d.allow and "offline_critical_action_denied" in d.reasons

def test_sod_violation_denied():
    i=intent(critical=True,creator_id="same",approver_id="same"); d=PolicyEngine().authorize(mk(),i,ctx(i))
    assert not d.allow

def test_physical_action_requires_l4():
    i=intent(operation="actuator.write",physical_actuation=True); d=PolicyEngine().authorize(mk(klass="L2"),i,ctx(i))
    assert not d.allow and "physical_actuation_requires_l4_classification" in d.reasons
