from __future__ import annotations

from typing import Any
from ..contracts import AdapterMetadata, AdapterResult, BaseIntegrationAdapter
from ..transports import JsonTransport


class KafkaBusAdapter(BaseIntegrationAdapter):
    """SGAEIA IP-BUS adapter for Apache Kafka event/control streams."""

    fail_mode = "buffer-and-retry"

    def __init__(self, transport: JsonTransport, *, implementation_version: str = "4.3.1", max_buffer: int = 1000):
        self.transport = transport
        self.max_buffer = max_buffer
        self.buffer: list[dict[str, Any]] = []
        self._revoked: set[str] = set()
        self.metadata = AdapterMetadata(
            "ADP-KAFKA-BUS", "IP-BUS", "Apache Kafka", implementation_version,
            "0.3.0", "IPS-C1-harness", "high"
        )

    def publish(self, subject_id: str, topic: str, message: dict[str, Any], *, trace_id: str) -> AdapterResult:
        payload = {"subject_id": subject_id, "topic": topic, "message": message, "trace_id": trace_id}
        if subject_id in self._revoked:
            decision, success, reason = "DENY", False, "publisher_revoked"
        else:
            try:
                data = self.transport("publish", payload)
                accepted = bool(data.get("accepted", True))
                decision, success, reason = ("PUBLISHED", True, None) if accepted else ("DENY", False, "bus_rejected")
            except ConnectionError:
                if len(self.buffer) >= self.max_buffer:
                    decision, success, reason = "BUFFER_FULL", False, "bus_buffer_full"
                else:
                    self.buffer.append(payload)
                    decision, success, reason = "BUFFERED", True, "bus_unavailable"
        ev = self._evidence(trace_id=trace_id, subject_id=subject_id, decision_or_result=decision, operation="publish")
        return AdapterResult(success, decision, {"buffer_depth": len(self.buffer)}, ev, reason)

    def revoke(self, subject_id: str, *, trace_id: str) -> AdapterResult:
        self._revoked.add(subject_id)
        ev = self._evidence(trace_id=trace_id, subject_id=subject_id, decision_or_result="REVOKED", operation="revoke-publisher")
        return AdapterResult(True, "REVOKED", {}, ev)

    def health(self) -> dict[str, Any]:
        return {"status": "configured", "buffer_depth": len(self.buffer), "port": self.metadata.port_id}
