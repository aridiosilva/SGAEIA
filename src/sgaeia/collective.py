from dataclasses import dataclass

@dataclass(frozen=True)
class AgentContribution:
    agent_id: str
    capabilities: frozenset[str]
    operation_fragment: str
    impact: int = 0
    depends_on: frozenset[str] = frozenset()

def evaluate_collective_action(contributions: tuple[AgentContribution, ...],
                               prohibited_capability_sets: tuple[frozenset[str], ...],
                               aggregate_impact_limit: int) -> tuple[bool, str]:
    agent_ids = [item.agent_id for item in contributions]
    if len(agent_ids) != len(set(agent_ids)):
        return False, "duplicate_participant"
    known = set(agent_ids)
    graph = {item.agent_id: set(item.depends_on) for item in contributions}
    if any(not dependencies.issubset(known) for dependencies in graph.values()):
        return False, "unknown_task_dependency"
    visiting: set[str] = set()
    visited: set[str] = set()
    def cyclic(node: str) -> bool:
        if node in visiting: return True
        if node in visited: return False
        visiting.add(node)
        if any(cyclic(parent) for parent in graph[node]): return True
        visiting.remove(node)
        visited.add(node)
        return False
    if any(cyclic(node) for node in graph):
        return False, "collective_task_cycle"
    aggregate_caps: set[str] = set()
    for item in contributions:
        aggregate_caps.update(item.capabilities)
    if any(set(blocked).issubset(aggregate_caps) for blocked in prohibited_capability_sets):
        return False, "collective_privilege_aggregation"
    if sum(item.impact for item in contributions) > aggregate_impact_limit:
        return False, "aggregate_impact_exceeded"
    return True, "collective_action_allowed"
