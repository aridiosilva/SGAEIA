from __future__ import annotations
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import hashlib, json, uuid

@dataclass(frozen=True)
class Evidence:
    evidence_id: str
    timestamp: str
    trace_id: str
    agent_id: str
    operation: str
    resource: str
    decision: str
    risk_score: int
    reasons: tuple[str, ...]
    digest: str


def make_evidence(*, trace_id: str, agent_id: str, operation: str, resource: str,
                  decision: str, risk_score: int, reasons: list[str]) -> Evidence:
    payload = {"trace_id":trace_id,"agent_id":agent_id,"operation":operation,"resource":resource,
               "decision":decision,"risk_score":risk_score,"reasons":reasons}
    digest = hashlib.sha256(json.dumps(payload,sort_keys=True).encode()).hexdigest()
    return Evidence(str(uuid.uuid4()), datetime.now(timezone.utc).isoformat(), trace_id, agent_id,
                    operation, resource, decision, risk_score, tuple(reasons), digest)
