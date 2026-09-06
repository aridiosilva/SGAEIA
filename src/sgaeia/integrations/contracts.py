from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import hashlib
import json
import uuid
from typing import Any


@dataclass(frozen=True)
class AdapterMetadata:
    adapter_id: str
    port_id: str
    implementation: str
    implementation_version: str
    adapter_version: str
    conformance_level: str
    criticality: str


@dataclass(frozen=True)
class AdapterEvidence:
    evidence_id: str
    timestamp: str
    trace_id: str
    port_id: str
    subject_id: str
    decision_or_result: str
    implementation_id: str
    implementation_version: str
    adapter_id: str
    operation: str
    digest: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class AdapterResult:
    success: bool
    decision: str
    data: dict[str, Any]
    evidence: AdapterEvidence
    reason: str | None = None


class BaseIntegrationAdapter(ABC):
    """Stable semantic boundary between SGAEIA and replaceable technology.

    Concrete adapters may use HTTP, Unix sockets, gRPC proxies, event buses or local
    libraries.  The contract deliberately exposes semantics rather than vendor APIs.
    """

    metadata: AdapterMetadata
    fail_mode: str = "fail-closed"

    def _evidence(
        self,
        *,
        trace_id: str,
        subject_id: str,
        decision_or_result: str,
        operation: str,
    ) -> AdapterEvidence:
        payload = {
            "trace_id": trace_id,
            "port_id": self.metadata.port_id,
            "subject_id": subject_id,
            "decision_or_result": decision_or_result,
            "implementation_id": self.metadata.implementation,
            "implementation_version": self.metadata.implementation_version,
            "adapter_id": self.metadata.adapter_id,
            "operation": operation,
        }
        digest = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
        return AdapterEvidence(
            evidence_id=str(uuid.uuid4()),
            timestamp=datetime.now(timezone.utc).isoformat(),
            trace_id=trace_id,
            port_id=self.metadata.port_id,
            subject_id=subject_id,
            decision_or_result=decision_or_result,
            implementation_id=self.metadata.implementation,
            implementation_version=self.metadata.implementation_version,
            adapter_id=self.metadata.adapter_id,
            operation=operation,
            digest=digest,
        )

    @abstractmethod
    def health(self) -> dict[str, Any]:
        """Return non-secret health/capability information."""

    @abstractmethod
    def revoke(self, subject_id: str, *, trace_id: str) -> AdapterResult:
        """Revoke or disable authority represented by this adapter's port."""
