from sgaeia.models import Agent
from sgaeia.delegation import validate_delegation

def test_delegation_cannot_increase_authority():
    a=Agent("a","o","L2","A2","ATZ-3","spiffe://x/a",frozenset({"read"}),frozenset(),True,1,True)
    ok,reason=validate_delegation(a,{"read","admin"},1)
    assert not ok and reason=="delegation_would_increase_authority"
