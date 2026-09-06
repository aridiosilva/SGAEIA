from __future__ import annotations

from collections.abc import Iterable
from .contracts import BaseIntegrationAdapter


class AdapterRegistry:
    def __init__(self, adapters: Iterable[BaseIntegrationAdapter] = ()): 
        self._adapters: dict[str, BaseIntegrationAdapter] = {}
        for adapter in adapters:
            self.register(adapter)

    def register(self, adapter: BaseIntegrationAdapter) -> None:
        key = adapter.metadata.port_id
        if key in self._adapters:
            raise ValueError(f"adapter already registered for {key}")
        self._adapters[key] = adapter

    def get(self, port_id: str) -> BaseIntegrationAdapter | None:
        return self._adapters.get(port_id)

    def require(self, port_id: str) -> BaseIntegrationAdapter:
        adapter = self.get(port_id)
        if adapter is None:
            raise KeyError(f"no adapter registered for {port_id}")
        return adapter

    def inventory(self) -> list[dict[str, str]]:
        return [
            {
                "port_id": a.metadata.port_id,
                "adapter_id": a.metadata.adapter_id,
                "implementation": a.metadata.implementation,
                "implementation_version": a.metadata.implementation_version,
                "conformance_level": a.metadata.conformance_level,
            }
            for a in sorted(self._adapters.values(), key=lambda x: x.metadata.port_id)
        ]
