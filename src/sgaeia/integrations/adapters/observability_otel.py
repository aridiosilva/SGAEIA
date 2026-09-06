from __future__ import annotations

from typing import Any
from ..contracts import AdapterMetadata, AdapterResult, BaseIntegrationAdapter
from ..transports import JsonTransport


class OpenTelemetryAdapter(BaseIntegrationAdapter):
    """SGAEIA IP-OBS adapter for OpenTelemetry Collector pipelines."""

    fail_mode = "buffer-and-retry"

    def __init__(self, transport: JsonTransport, *, implementation_version: str = "0.160.0", max_buffer: int = 1000):
        self.transport = transport
        self.max_buffer = max_buffer
        self.buffer: list[dict[str, Any]] = []
        self._revoked: set[str] = set()
        self.metadata = AdapterMetadata(
            "ADP-OTEL-OBS", "IP-OBS", "OpenTelemetry Collector", implementation_version,
            "0.3.0", "IPS-C1-harness", "high"
        )

    def emit(self, subject_id: str, event: dict[str, Any], *, trace_id: str) -> AdapterResult:
        payload = {"subject_id": subject_id, "trace_id": trace_id, "event": event}
        if subject_id in self._revoked:
            decision, success, reason = "DENY", False, "telemetry_subject_revoked"
        else:
            try:
                self.transport("emit", payload)
                decision, success, reason = "EMITTED", True, None
            except ConnectionError:
                if len(self.buffer) >= self.max_buffer:
                    decision, success, reason = "BUFFER_FULL", False, "telemetry_buffer_full"
                else:
                    self.buffer.append(payload)
                    decision, success, reason = "BUFFERED", True, "collector_unavailable"
        ev = self._evidence(trace_id=trace_id, subject_id=subject_id, decision_or_result=decision, operation="emit")
        return AdapterResult(success, decision, {"buffer_depth": len(self.buffer)}, ev, reason)

    def revoke(self, subject_id: str, *, trace_id: str) -> AdapterResult:
        self._revoked.add(subject_id)
        ev = self._evidence(trace_id=trace_id, subject_id=subject_id, decision_or_result="REVOKED", operation="revoke")
        return AdapterResult(True, "REVOKED", {}, ev)

    def health(self) -> dict[str, Any]:
        return {"status": "configured", "buffer_depth": len(self.buffer), "port": self.metadata.port_id}
