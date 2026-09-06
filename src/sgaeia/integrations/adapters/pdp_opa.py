from __future__ import annotations

from typing import Any
from ..contracts import AdapterMetadata, AdapterResult, BaseIntegrationAdapter
from ..transports import JsonTransport


class OpaPdpAdapter(BaseIntegrationAdapter):
    """SGAEIA IP-PDP adapter for OPA/Rego or an OPA-compatible policy facade."""

    fail_mode = "fail-closed"

    def __init__(self, transport: JsonTransport, *, implementation_version: str = "1.16.2"):
        self.transport = transport
        self._emergency_denies: set[str] = set()
        self.metadata = AdapterMetadata(
            "ADP-OPA-PDP", "IP-PDP", "Open Policy Agent", implementation_version,
            "0.3.0", "IPS-C1-harness", "critical"
        )

    def evaluate(self, subject_id: str, request: dict[str, Any], *, trace_id: str) -> AdapterResult:
        if subject_id in self._emergency_denies:
            ev = self._evidence(trace_id=trace_id, subject_id=subject_id, decision_or_result="DENY", operation="evaluate")
            return AdapterResult(False, "DENY", {"obligations": []}, ev, "emergency_deny")
        try:
            data = self.transport("evaluate", {"subject_id": subject_id, "trace_id": trace_id, "input": request})
            allow = bool(data.get("allow", False))
            decision = str(data.get("decision", "ALLOW" if allow else "DENY")).upper()
            allow = allow and decision not in {"DENY", "QUARANTINE", "REVOKE"}
        except ConnectionError:
            data, allow, decision = {"obligations": []}, False, "DENY"
        ev = self._evidence(trace_id=trace_id, subject_id=subject_id, decision_or_result=decision, operation="evaluate")
        return AdapterResult(allow, decision, data, ev, None if allow else "policy_denied_or_unavailable")

    def revoke(self, subject_id: str, *, trace_id: str) -> AdapterResult:
        self._emergency_denies.add(subject_id)
        ev = self._evidence(trace_id=trace_id, subject_id=subject_id, decision_or_result="REVOKED", operation="emergency-deny")
        return AdapterResult(True, "REVOKED", {}, ev)

    def health(self) -> dict[str, Any]:
        return {"status": "configured", "port": self.metadata.port_id, "fail_mode": self.fail_mode}
