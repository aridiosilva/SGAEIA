from sgaeia.models import Agent, RiskContext
from sgaeia.risk_engine import RiskEngine

def agent():
    return Agent("a","owner","L2","A2","ATZ-3","spiffe://example/a",frozenset({"read"}),frozenset(),False,0,True)

def test_risk_is_bounded():
    score=RiskEngine().score(agent(),RiskContext(5,5,5,5,5,5,5))
    assert 0 <= score <= 100

def test_low_risk_disposition():
    score=RiskEngine().score(agent(),RiskContext())
    assert RiskEngine.disposition(score) in {"ALLOW","ALLOW_MONITORED"}
