"""Minimal composition example for the SGAEIA Adapter Conformance Framework."""
from sgaeia.integrations import AdapterRegistry
from sgaeia.integrations.adapters import SpireIdentityAdapter, OpaPdpAdapter


def transport(operation, payload):
    if operation == "verify":
        return {"valid": True, "spiffe_id": "spiffe://example.org/agent/demo"}
    if operation == "evaluate":
        return {"allow": True, "decision": "ALLOW", "obligations": []}
    return {"accepted": True}


registry = AdapterRegistry([
    SpireIdentityAdapter(transport),
    OpaPdpAdapter(transport),
])

print(registry.inventory())
