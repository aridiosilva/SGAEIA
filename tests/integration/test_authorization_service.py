from sgaeia.registry import AgentRegistry
from sgaeia.models import Agent, Intent
from sgaeia.assurance import OperationPolicy, TrustedContextProvider
from sgaeia.service import AuthorizationService

def test_authorization_emits_evidence():
    reg=AgentRegistry(); reg.register(Agent("a","o","L1","A1","ATZ-2","spiffe://x/a",frozenset({"read"}),frozenset(),False,0,True,capability_assurance_level=1))
    contexts=TrustedContextProvider({"read":OperationPolicy(monitor_assurance=1,containment_assurance=1,recovery_assurance=1)})
    decision,ev=AuthorizationService(reg,contexts=contexts).authorize(Intent("a","read","r","trace-1"))
    assert decision.allow
    assert ev.trace_id=="trace-1" and ev.evidence_id
    decision2,ev2=AuthorizationService(reg,contexts=contexts).authorize(Intent("a","read","r","trace-2"))
    assert decision2.allow and ev2.previous_digest==""

def test_authorization_service_chains_evidence_digests():
    reg=AgentRegistry(); reg.register(Agent("a","o","L1","A1","ATZ-2","spiffe://x/a",frozenset({"read"}),frozenset(),False,0,True,capability_assurance_level=1))
    contexts=TrustedContextProvider({"read":OperationPolicy(monitor_assurance=1,containment_assurance=1,recovery_assurance=1)})
    service=AuthorizationService(reg,contexts=contexts)
    _,first=service.authorize(Intent("a","read","r","chain-1"))
    _,second=service.authorize(Intent("a","read","r","chain-2"))
    assert second.previous_digest==first.digest
    assert first.digest!=second.digest
