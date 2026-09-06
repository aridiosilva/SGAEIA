from __future__ import annotations

from typing import Any
from ..contracts import AdapterMetadata, AdapterResult, BaseIntegrationAdapter
from ..transports import JsonTransport


class KubernetesEdgeAdapter(BaseIntegrationAdapter):
    """SGAEIA IP-EDGE adapter for Kubernetes/K3s admission, quarantine and safe degradation."""

    fail_mode = "degrade-authority"

    def __init__(self, transport: JsonTransport, *, implementation_version: str = "1.37.0"):
        self.transport = transport
        self._quarantined: set[str] = set()
        self.metadata = AdapterMetadata(
            "ADP-K8S-EDGE", "IP-EDGE", "Kubernetes/K3s", implementation_version,
            "0.3.0", "IPS-C1-harness", "critical"
        )

    def admit(self, subject_id: str, workload: dict[str, Any], *, trace_id: str, critical: bool = False) -> AdapterResult:
        if subject_id in self._quarantined:
            allow, data, reason = False, {}, "workload_quarantined"
        else:
            try:
                data = self.transport("admit", {"subject_id": subject_id, "workload": workload, "critical": critical, "trace_id": trace_id})
                allow = bool(data.get("allow", False)) and (not critical or bool(data.get("attested", False)))
                reason = None if allow else "admission_or_attestation_denied"
            except ConnectionError:
                allow, data, reason = False, {}, "edge_control_plane_unavailable"
        decision = "ALLOW" if allow else "DENY"
        ev = self._evidence(trace_id=trace_id, subject_id=subject_id, decision_or_result=decision, operation="admit")
        return AdapterResult(allow, decision, data, ev, reason)

    def revoke(self, subject_id: str, *, trace_id: str) -> AdapterResult:
        self._quarantined.add(subject_id)
        try:
            self.transport("quarantine", {"subject_id": subject_id, "trace_id": trace_id})
        except ConnectionError:
            pass
        ev = self._evidence(trace_id=trace_id, subject_id=subject_id, decision_or_result="QUARANTINED", operation="quarantine")
        return AdapterResult(True, "QUARANTINED", {}, ev)

    def health(self) -> dict[str, Any]:
        return {"status": "configured", "port": self.metadata.port_id, "fail_mode": self.fail_mode}
