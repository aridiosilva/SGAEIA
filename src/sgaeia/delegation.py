from dataclasses import dataclass
from datetime import datetime, timezone
from .models import Agent

@dataclass(frozen=True)
class DelegationGrant:
    grant_id: str
    parent_agent_id: str
    child_agent_id: str
    capabilities: frozenset[str]
    purpose: str
    expires_at: str
    parent_grant_id: str | None = None

def validate_delegation_chain(agent: Agent, chain: tuple[DelegationGrant, ...],
                              required_capability: str, purpose: str,
                              now: datetime | None = None) -> tuple[bool, str]:
    now = now or datetime.now(timezone.utc)
    if len(chain) > agent.max_delegation_depth:
        return False, "delegation_chain_too_long"
    seen: set[str] = set()
    effective = set(agent.capabilities)
    expected_parent = agent.id
    for grant in chain:
        if grant.grant_id in seen:
            return False, "delegation_cycle_detected"
        seen.add(grant.grant_id)
        if grant.parent_agent_id != expected_parent:
            return False, "delegation_provenance_broken"
        if grant.purpose != purpose:
            return False, "delegation_purpose_mismatch"
        expires = datetime.fromisoformat(grant.expires_at.replace("Z", "+00:00"))
        if expires <= now:
            return False, "delegation_expired"
        if not set(grant.capabilities).issubset(effective):
            return False, "delegation_would_increase_authority"
        effective.intersection_update(grant.capabilities)
        expected_parent = grant.child_agent_id
    if required_capability not in effective:
        return False, "required_capability_not_delegated"
    return True, "delegation_chain_valid"

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
