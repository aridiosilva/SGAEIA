from __future__ import annotations

from .edge_kubernetes import KubernetesEdgeAdapter
from ..contracts import AdapterMetadata
from ..transports import JsonTransport


class K3sEdgeAdapter(KubernetesEdgeAdapter):
    """Edge-optimized SGAEIA IP-EDGE profile for K3s."""

    def __init__(self, transport: JsonTransport, *, implementation_version: str = "1.36.x+k3s"):
        super().__init__(transport, implementation_version=implementation_version)
        self.metadata = AdapterMetadata(
            "ADP-K3S-EDGE", "IP-EDGE", "K3s", implementation_version,
            "0.3.0", "IPS-C1-harness", "critical"
        )
