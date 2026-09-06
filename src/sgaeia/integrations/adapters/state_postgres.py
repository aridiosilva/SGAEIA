from __future__ import annotations

from typing import Any
from ..contracts import AdapterMetadata, AdapterResult, BaseIntegrationAdapter
from ..transports import JsonTransport


class PostgreSQLStateAdapter(BaseIntegrationAdapter):
    """SGAEIA IP-STATE adapter for governed state persisted in PostgreSQL."""

    fail_mode = "read-only"

    def __init__(self, transport: JsonTransport, *, implementation_version: str = "18.6"):
        self.transport = transport
        self._revoked: set[str] = set()
        self.metadata = AdapterMetadata(
            "ADP-POSTGRES-STATE", "IP-STATE", "PostgreSQL", implementation_version,
            "0.3.0", "IPS-C1-harness", "high"
        )

    def write(self, subject_id: str, key: str, value: Any, *, trace_id: str) -> AdapterResult:
        if subject_id in self._revoked:
            success, decision, data, reason = False, "DENY", {}, "writer_revoked"
        else:
            try:
                data = self.transport("write", {"subject_id": subject_id, "key": key, "value": value, "trace_id": trace_id})
                success, decision, reason = bool(data.get("written", True)), "WRITTEN", None
            except ConnectionError:
                success, decision, data, reason = False, "READ_ONLY", {}, "state_backend_unavailable"
        ev = self._evidence(trace_id=trace_id, subject_id=subject_id, decision_or_result=decision, operation="write")
        return AdapterResult(success, decision, data, ev, reason)

    def read(self, subject_id: str, key: str, *, trace_id: str) -> AdapterResult:
        try:
            data = self.transport("read", {"subject_id": subject_id, "key": key, "trace_id": trace_id})
            success, decision, reason = True, "READ", None
        except ConnectionError:
            data, success, decision, reason = {}, False, "UNAVAILABLE", "state_backend_unavailable"
        ev = self._evidence(trace_id=trace_id, subject_id=subject_id, decision_or_result=decision, operation="read")
        return AdapterResult(success, decision, data, ev, reason)

    def revoke(self, subject_id: str, *, trace_id: str) -> AdapterResult:
        self._revoked.add(subject_id)
        ev = self._evidence(trace_id=trace_id, subject_id=subject_id, decision_or_result="REVOKED", operation="revoke-writer")
        return AdapterResult(True, "REVOKED", {}, ev)

    def health(self) -> dict[str, Any]:
        return {"status": "configured", "port": self.metadata.port_id, "fail_mode": self.fail_mode}
