from dataclasses import dataclass

@dataclass(frozen=True)
class AgentContribution:
    agent_id: str
    capabilities: frozenset[str]
    operation_fragment: str
    impact: int = 0

def evaluate_collective_action(contributions: tuple[AgentContribution, ...],
                               prohibited_capability_sets: tuple[frozenset[str], ...],
                               aggregate_impact_limit: int) -> tuple[bool, str]:
    agent_ids = [item.agent_id for item in contributions]
    if len(agent_ids) != len(set(agent_ids)):
        return False, "duplicate_or_cyclic_participant"
    aggregate_caps: set[str] = set()
    for item in contributions:
        aggregate_caps.update(item.capabilities)
    if any(set(blocked).issubset(aggregate_caps) for blocked in prohibited_capability_sets):
        return False, "collective_privilege_aggregation"
    if sum(item.impact for item in contributions) > aggregate_impact_limit:
        return False, "aggregate_impact_exceeded"
    return True, "collective_action_allowed"
