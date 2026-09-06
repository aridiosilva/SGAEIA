from .models import Agent

def validate_delegation(parent: Agent, requested_caps: set[str], depth: int) -> tuple[bool,str]:
    if not parent.delegation_allowed:
        return False, "delegation_disabled"
    if depth > parent.max_delegation_depth:
        return False, "delegation_depth_exceeded"
    if not requested_caps.issubset(set(parent.capabilities)):
        return False, "delegation_would_increase_authority"
    if requested_caps & set(parent.denied_capabilities):
        return False, "delegation_contains_denied_capability"
    return True, "delegation_valid"
