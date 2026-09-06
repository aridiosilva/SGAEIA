from __future__ import annotations

from typing import Any
from ..contracts import AdapterMetadata, AdapterResult, BaseIntegrationAdapter
from ..transports import JsonTransport


class IstioMeshAdapter(BaseIntegrationAdapter):
    """SGAEIA IP-MESH adapter for Istio/Envoy or compatible zero-trust mesh control."""

    fail_mode = "fail-closed"

    def __init__(self, transport: JsonTransport, *, implementation_version: str = "1.31.0"):
        self.transport = transport
        self._blocked: set[str] = set()
        self.metadata = AdapterMetadata(
            "ADP-ISTIO-MESH", "IP-MESH", "Istio/Envoy", implementation_version,
            "0.3.0", "IPS-C1-harness", "critical"
        )

    def authorize_egress(self, subject_id: str, destination: str, *, trace_id: str) -> AdapterResult:
        if subject_id in self._blocked:
            allow, data = False, {}
        else:
            try:
                data = self.transport("authorize-egress", {"subject_id": subject_id, "destination": destination, "trace_id": trace_id})
                allow = bool(data.get("allow", False)) and bool(data.get("mtls", False))
            except ConnectionError:
                allow, data = False, {}
        decision = "ALLOW" if allow else "DENY"
        ev = self._evidence(trace_id=trace_id, subject_id=subject_id, decision_or_result=decision, operation="authorize-egress")
        return AdapterResult(allow, decision, data, ev, None if allow else "mesh_policy_or_mtls_failure")

    def revoke(self, subject_id: str, *, trace_id: str) -> AdapterResult:
        self._blocked.add(subject_id)
        ev = self._evidence(trace_id=trace_id, subject_id=subject_id, decision_or_result="REVOKED", operation="block-workload")
        return AdapterResult(True, "REVOKED", {}, ev)

    def health(self) -> dict[str, Any]:
        return {"status": "configured", "port": self.metadata.port_id, "fail_mode": self.fail_mode}
