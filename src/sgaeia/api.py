from pathlib import Path
from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict
from .registry import AgentRegistry
from .models import Intent
from .service import AuthorizationService
from .assurance import TrustedContextProvider

ROOT = Path(__file__).resolve().parents[2]
registry = AgentRegistry.from_yaml_dir(ROOT / "specs" / "agents")
contexts = TrustedContextProvider.from_yaml(ROOT / "specs" / "policies" / "operation-policies.yaml")
service = AuthorizationService(registry, contexts=contexts)
app = FastAPI(title="SGAEIA Control API", version="0.3.2-rc2")

class AuthorizationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    agent_id: str
    operation: str
    resource: str
    trace_id: str
    delegation_chain: tuple[str, ...] = ()

@app.get("/health")
def health(): return {"status":"ok","registered_agents":len(registry._agents)}

@app.post("/v1/authorize")
def authorize(req: AuthorizationRequest):
    intent = Intent(req.agent_id, req.operation, req.resource, req.trace_id,
                    delegation_chain=req.delegation_chain)
    decision, ev = service.authorize(intent)
    return {"allow":decision.allow,"action":decision.action,"risk_score":decision.risk_score,"reasons":decision.reasons,"evidence":ev.__dict__}
