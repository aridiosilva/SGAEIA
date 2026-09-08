from pathlib import Path
from fastapi import FastAPI
from pydantic import BaseModel, Field
from .registry import AgentRegistry
from .models import Intent, RiskContext, MonitorDecision
from .service import AuthorizationService

ROOT = Path(__file__).resolve().parents[2]
registry = AgentRegistry.from_yaml_dir(ROOT / "specs" / "agents")
service = AuthorizationService(registry)
app = FastAPI(title="SGAEIA Control API", version="0.3.2")

class AuthorizationRequest(BaseModel):
    agent_id: str
    operation: str
    resource: str
    trace_id: str
    delegation_depth: int = 0
    offline: bool = False
    critical: bool = False
    physical_actuation: bool = False
    human_approvals: int = 0
    creator_id: str | None = None
    approver_id: str | None = None
    privilege: int = Field(0, ge=0, le=5)
    data_sensitivity: int = Field(0, ge=0, le=5)
    tool_power: int = Field(0, ge=0, le=5)
    network_reach: int = Field(0, ge=0, le=5)
    delegation: int = Field(0, ge=0, le=5)
    impact: int = Field(0, ge=0, le=5)
    behavior_anomaly: int = Field(0, ge=0, le=5)
    target_kind: str = "resource"
    self_affecting_change: bool = False
    reasoning_only_authorization: bool = False
    observed_runtime_seconds: int = Field(0, ge=0)
    observed_tool_calls: int = Field(0, ge=0)
    observed_network_reach: int = Field(0, ge=0, le=5)
    delegation_chain: tuple[str, ...] = ()
    monitor_assurance: int = Field(5, ge=0, le=5)
    containment_assurance: int = Field(5, ge=0, le=5)
    recovery_assurance: int = Field(5, ge=0, le=5)
    aggregate_impact: int = Field(0, ge=0, le=5)
    monitor_id: str | None = None
    monitor_allow: bool = False
    monitor_valid: bool = False
    monitor_policy_version: str = "unknown"
    monitor_observed_effect: str = ""
    monitor_divergence_detected: bool = False

@app.get("/health")
def health(): return {"status":"ok","registered_agents":len(registry._agents)}

@app.post("/v1/authorize")
def authorize(req: AuthorizationRequest):
    intent = Intent(**{k:getattr(req,k) for k in ["agent_id","operation","resource","trace_id","delegation_depth","offline","critical","physical_actuation","human_approvals","creator_id","approver_id","target_kind","self_affecting_change","reasoning_only_authorization","observed_runtime_seconds","observed_tool_calls","observed_network_reach","delegation_chain"]})
    ctx = RiskContext(**{k:getattr(req,k) for k in ["privilege","data_sensitivity","tool_power","network_reach","delegation","impact","behavior_anomaly","monitor_assurance","containment_assurance","recovery_assurance","aggregate_impact"]})
    monitor = None
    if req.monitor_id:
        monitor = MonitorDecision(req.monitor_id, req.monitor_allow, req.monitor_valid,
            req.monitor_policy_version, req.monitor_observed_effect,
            req.monitor_divergence_detected)
    decision, ev = service.authorize(intent,ctx,monitor)
    return {"allow":decision.allow,"action":decision.action,"risk_score":decision.risk_score,"reasons":decision.reasons,"evidence":ev.__dict__}
