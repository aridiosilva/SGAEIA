from sgaeia.models import Agent, Intent, RiskContext
from sgaeia.policy import PolicyEngine

def test_tool_abuse_without_capability_is_denied():
    a=Agent("a","o","L2","A2","ATZ-3","spiffe://x/a",frozenset({"invoice.read"}),frozenset({"external.network.write"}),False,0,True)
    i=Intent("a","external.network.write","internet","redteam-1")
    d=PolicyEngine().authorize(a,i,RiskContext(tool_power=5,network_reach=5))
    assert not d.allow

def test_high_anomalous_risk_cannot_silently_execute():
    a=Agent("a","o","L3","A2","ATZ-4","spiffe://x/a",frozenset({"payment.execute"}),frozenset(),False,0,True)
    i=Intent("a","payment.execute","payment:1","redteam-2",critical=True)
    d=PolicyEngine().authorize(a,i,RiskContext(privilege=5,data_sensitivity=4,tool_power=5,network_reach=4,impact=5,behavior_anomaly=5))
    assert not d.allow
    assert d.action in {"REQUIRE_APPROVAL","QUARANTINE","DENY_REVOKE"}
