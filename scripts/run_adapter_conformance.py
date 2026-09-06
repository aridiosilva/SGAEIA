from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import json
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sgaeia.integrations.adapters import (
    KafkaBusAdapter, K3sEdgeAdapter, KubernetesEdgeAdapter, NatsBusAdapter,
    OpaPdpAdapter, OpenTelemetryAdapter, PostgreSQLStateAdapter,
    SpireIdentityAdapter, IstioMeshAdapter,
)
from sgaeia.integrations.conformance import check_evidence, metadata_checks


def transport(operation, payload):
    if operation == "verify": return {"valid": True, "spiffe_id": "spiffe://example.org/conformance/subject", "attested": True}
    if operation == "evaluate": return {"allow": True, "decision": "ALLOW", "obligations": []}
    if operation == "authorize-egress": return {"allow": True, "mtls": True}
    if operation == "admit": return {"allow": True, "attested": True}
    if operation == "write": return {"written": True}
    if operation == "read": return {"value": "ok"}
    if operation == "publish": return {"accepted": True}
    return {"accepted": True}


def load_port(port_id):
    for p in (ROOT / "specs/integrations/ports").glob("*.port.yaml"):
        doc = yaml.safe_load(p.read_text())
        if doc["metadata"]["id"] == port_id: return doc
    raise KeyError(port_id)


adapters = [
    SpireIdentityAdapter(transport), OpaPdpAdapter(transport), IstioMeshAdapter(transport),
    OpenTelemetryAdapter(transport), NatsBusAdapter(transport), KafkaBusAdapter(transport),
    PostgreSQLStateAdapter(transport), KubernetesEdgeAdapter(transport), K3sEdgeAdapter(transport),
]

results=[]
for a in adapters:
    report=metadata_checks(a, load_port(a.metadata.port_id), target_level="IPS-C1")
    if a.metadata.port_id == "IP-IDENTITY": r=a.verify("subject", trace_id="cf-identity")
    elif a.metadata.port_id == "IP-PDP": r=a.evaluate("subject", {}, trace_id="cf-pdp")
    elif a.metadata.port_id == "IP-MESH": r=a.authorize_egress("subject","service",trace_id="cf-mesh")
    elif a.metadata.port_id == "IP-OBS": r=a.emit("subject",{"event":"cf"},trace_id="cf-obs")
    elif a.metadata.port_id == "IP-BUS": r=a.publish("subject","cf.events",{},trace_id=f"cf-{a.metadata.adapter_id.lower()}")
    elif a.metadata.port_id == "IP-STATE": r=a.write("subject","k","v",trace_id="cf-state")
    elif a.metadata.port_id == "IP-EDGE": r=a.admit("subject",{},trace_id=f"cf-{a.metadata.adapter_id.lower()}")
    else: raise AssertionError(a.metadata.port_id)
    evcheck=check_evidence(r.evidence, expected_port=a.metadata.port_id)
    item=report.to_dict()
    item["checks"].append({"name":evcheck.name,"passed":evcheck.passed,"detail":evcheck.detail})
    item["passed"] = item["passed"] and evcheck.passed and r.success
    results.append(item)

out={
    "format":"SGAEIA-Adapter-Conformance-Report",
    "version":"0.3.2",
    "generated_at":datetime.now(timezone.utc).isoformat(),
    "scope":"offline contract harness / IPS-C1; not live-product certification",
    "passed":all(x["passed"] for x in results),
    "adapters":results,
}
path=ROOT/"evidence/adapter-conformance.generated.json"
path.write_text(json.dumps(out,indent=2)+"\n")
print(f"ADAPTER CONFORMANCE {'PASSED' if out['passed'] else 'FAILED'}: {len(results)} profiles -> {path.relative_to(ROOT)}")
raise SystemExit(0 if out["passed"] else 1)
