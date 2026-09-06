from __future__ import annotations

from typing import Any
from ..contracts import AdapterMetadata, AdapterResult, BaseIntegrationAdapter
from ..transports import JsonTransport


class SpireIdentityAdapter(BaseIntegrationAdapter):
    """SGAEIA IP-IDENTITY adapter for a SPIFFE/SPIRE-compatible identity service.

    The injected transport can target a thin enterprise facade over SPIRE Workload API,
    a sidecar, or a test double. SGAEIA does not embed SPIRE-specific authority semantics.
    """

    fail_mode = "fail-closed"

    def __init__(self, transport: JsonTransport, *, implementation_version: str = "1.15.2"):
        self.transport = transport
        self._revoked: set[str] = set()
        self.metadata = AdapterMetadata(
            "ADP-SPIRE-IDENTITY", "IP-IDENTITY", "SPIFFE/SPIRE", implementation_version,
            "0.3.0", "IPS-C1-harness", "critical"
        )

    def verify(self, subject_id: str, *, trace_id: str) -> AdapterResult:
        if subject_id in self._revoked:
            ev = self._evidence(trace_id=trace_id, subject_id=subject_id, decision_or_result="DENY", operation="verify")
            return AdapterResult(False, "DENY", {}, ev, "identity_revoked")
        try:
            data = self.transport("verify", {"subject_id": subject_id, "trace_id": trace_id})
            valid = bool(data.get("valid")) and str(data.get("spiffe_id", "")).startswith("spiffe://")
        except ConnectionError:
            valid, data = False, {}
        decision = "ALLOW" if valid else "DENY"
        ev = self._evidence(trace_id=trace_id, subject_id=subject_id, decision_or_result=decision, operation="verify")
        return AdapterResult(valid, decision, data, ev, None if valid else "identity_unverifiable")

    def revoke(self, subject_id: str, *, trace_id: str) -> AdapterResult:
        self._revoked.add(subject_id)
        try:
            self.transport("revoke", {"subject_id": subject_id, "trace_id": trace_id})
        except ConnectionError:
            pass  # local deny-list preserves fail-closed revocation semantics
        ev = self._evidence(trace_id=trace_id, subject_id=subject_id, decision_or_result="REVOKED", operation="revoke")
        return AdapterResult(True, "REVOKED", {}, ev)

    def health(self) -> dict[str, Any]:
        return {"status": "configured", "port": self.metadata.port_id, "fail_mode": self.fail_mode}
