"""Technology-neutral integration contracts and adapter conformance support."""

from .contracts import AdapterEvidence, AdapterMetadata, AdapterResult, BaseIntegrationAdapter
from .registry import AdapterRegistry

__all__ = [
    "AdapterEvidence",
    "AdapterMetadata",
    "AdapterResult",
    "BaseIntegrationAdapter",
    "AdapterRegistry",
]
