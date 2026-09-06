from __future__ import annotations

from pathlib import Path
import yaml

from sgaeia.integrations.adapters import (
    KafkaBusAdapter,
    K3sEdgeAdapter,
    KubernetesEdgeAdapter,
    NatsBusAdapter,
    OpaPdpAdapter,
    OpenTelemetryAdapter,
    PostgreSQLStateAdapter,
    SpireIdentityAdapter,
    IstioMeshAdapter,
)
from sgaeia.integrations.conformance import check_evidence, metadata_checks

ROOT = Path(__file__).resolve().parents[2]


def ok_transport(operation, payload):
    if operation == "verify":
        return {"valid": True, "spiffe_id": "spiffe://example.org/agent/test", "attested": True}
    if operation == "evaluate":
        return {"allow": True, "decision": "ALLOW", "obligations": []}
    if operation == "authorize-egress":
        return {"allow": True, "mtls": True}
    if operation == "admit":
        return {"allow": True, "attested": True}
    if operation == "write":
        return {"written": True}
    if operation == "read":
        return {"value": "x"}
    if operation == "publish":
        return {"accepted": True}
    return {"accepted": True}


def down_transport(operation, payload):
    raise ConnectionError("simulated dependency outage")


def port(port_id: str):
    for p in (ROOT / "specs" / "integrations" / "ports").glob("*.port.yaml"):
        doc = yaml.safe_load(p.read_text())
        if doc["metadata"]["id"] == port_id:
            return doc
    raise AssertionError(f"missing {port_id}")


def test_identity_and_pdp_fail_closed():
    identity = SpireIdentityAdapter(down_transport)
    result = identity.verify("agent-a", trace_id="t-identity")
    assert result.success is False and result.decision == "DENY"

    pdp = OpaPdpAdapter(down_transport)
    result = pdp.evaluate("agent-a", {"critical": True}, trace_id="t-pdp")
    assert result.success is False and result.decision == "DENY"


def test_mesh_requires_mtls_and_fails_closed():
    mesh = IstioMeshAdapter(lambda op, payload: {"allow": True, "mtls": False})
    assert mesh.authorize_egress("agent-a", "payments.internal", trace_id="t-mesh").decision == "DENY"
    assert IstioMeshAdapter(down_transport).authorize_egress("agent-a", "x", trace_id="t-down").decision == "DENY"


def test_observability_and_bus_buffer_on_dependency_loss():
    obs = OpenTelemetryAdapter(down_transport)
    result = obs.emit("agent-a", {"event": "decision"}, trace_id="t-obs")
    assert result.success and result.decision == "BUFFERED" and result.data["buffer_depth"] == 1

    for adapter in (NatsBusAdapter(down_transport), KafkaBusAdapter(down_transport)):
        result = adapter.publish("agent-a", "governance.events", {"event": "x"}, trace_id="t-bus")
        assert result.success and result.decision == "BUFFERED" and result.data["buffer_depth"] == 1


def test_state_degrades_to_read_only_on_write_failure():
    state = PostgreSQLStateAdapter(down_transport)
    result = state.write("agent-a", "key", "value", trace_id="t-state")
    assert result.success is False
    assert result.decision == "READ_ONLY"


def test_edge_admission_fails_secure_and_revocation_is_local_immediate():
    for adapter in (KubernetesEdgeAdapter(ok_transport), K3sEdgeAdapter(ok_transport)):
        allowed = adapter.admit("workload-a", {"image": "signed"}, trace_id="t-edge", critical=True)
        assert allowed.success is True
        adapter.revoke("workload-a", trace_id="t-revoke")
        denied = adapter.admit("workload-a", {"image": "signed"}, trace_id="t-edge2", critical=True)
        assert denied.success is False and denied.decision == "DENY"


def test_every_reference_adapter_matches_its_port_metadata_and_emits_attributable_evidence():
    adapters_and_results = [
        (SpireIdentityAdapter(ok_transport), lambda a: a.verify("agent-a", trace_id="t1")),
        (OpaPdpAdapter(ok_transport), lambda a: a.evaluate("agent-a", {}, trace_id="t2")),
        (IstioMeshAdapter(ok_transport), lambda a: a.authorize_egress("agent-a", "svc", trace_id="t3")),
        (OpenTelemetryAdapter(ok_transport), lambda a: a.emit("agent-a", {"x": 1}, trace_id="t4")),
        (NatsBusAdapter(ok_transport), lambda a: a.publish("agent-a", "topic", {}, trace_id="t5")),
        (KafkaBusAdapter(ok_transport), lambda a: a.publish("agent-a", "topic", {}, trace_id="t6")),
        (PostgreSQLStateAdapter(ok_transport), lambda a: a.write("agent-a", "k", "v", trace_id="t7")),
        (KubernetesEdgeAdapter(ok_transport), lambda a: a.admit("agent-a", {}, trace_id="t8")),
        (K3sEdgeAdapter(ok_transport), lambda a: a.admit("agent-a", {}, trace_id="t9")),
    ]
    for adapter, invoke in adapters_and_results:
        report = metadata_checks(adapter, port(adapter.metadata.port_id))
        assert report.passed, report.to_dict()
        result = invoke(adapter)
        evidence_check = check_evidence(result.evidence, expected_port=adapter.metadata.port_id)
        assert evidence_check.passed, evidence_check.detail


def test_revocation_blocks_future_authority_for_security_critical_adapters():
    identity = SpireIdentityAdapter(ok_transport)
    identity.revoke("agent-a", trace_id="r1")
    assert identity.verify("agent-a", trace_id="r2").decision == "DENY"

    pdp = OpaPdpAdapter(ok_transport)
    pdp.revoke("agent-a", trace_id="r3")
    assert pdp.evaluate("agent-a", {}, trace_id="r4").decision == "DENY"

    mesh = IstioMeshAdapter(ok_transport)
    mesh.revoke("agent-a", trace_id="r5")
    assert mesh.authorize_egress("agent-a", "svc", trace_id="r6").decision == "DENY"
