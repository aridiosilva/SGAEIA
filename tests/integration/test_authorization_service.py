from sgaeia.registry import AgentRegistry
from sgaeia.models import Agent, Intent, RiskContext
from sgaeia.service import AuthorizationService

def test_authorization_emits_evidence():
    reg=AgentRegistry(); reg.register(Agent("a","o","L1","A1","ATZ-2","spiffe://x/a",frozenset({"read"}),frozenset(),False,0,True))
    decision,ev=AuthorizationService(reg).authorize(Intent("a","read","r","trace-1"),RiskContext())
    assert decision.allow
    assert ev.trace_id=="trace-1" and ev.evidence_id
