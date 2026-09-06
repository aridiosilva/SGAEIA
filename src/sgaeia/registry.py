from __future__ import annotations
from pathlib import Path
import yaml
from .models import Agent

class AgentRegistry:
    def __init__(self):
        self._agents: dict[str, Agent] = {}

    def register(self, agent: Agent) -> None:
        if not agent.id or not agent.owner:
            raise ValueError("agent id and owner are required")
        if not agent.spiffe_id.startswith("spiffe://"):
            raise ValueError("workload identity must be a SPIFFE-style URI in this reference")
        if not agent.kill_switch_required:
            raise ValueError("kill switch is mandatory")
        self._agents[agent.id] = agent

    def get(self, agent_id: str) -> Agent | None:
        return self._agents.get(agent_id)

    @classmethod
    def from_yaml_dir(cls, directory: str | Path) -> "AgentRegistry":
        reg = cls()
        for p in Path(directory).glob("*.yaml"):
            doc = yaml.safe_load(p.read_text(encoding="utf-8"))
            if not isinstance(doc, dict) or doc.get("kind") != "Agent":
                continue
            md, spec = doc["metadata"], doc["spec"]
            reg.register(Agent(
                id=md["id"], owner=md["owner"], klass=spec["class"], autonomy=spec["autonomy"],
                trust_zone=spec["trustZone"], spiffe_id=spec["identity"]["spiffeId"],
                capabilities=frozenset(spec["capabilities"].get("allow", [])),
                denied_capabilities=frozenset(spec["capabilities"].get("deny", [])),
                delegation_allowed=spec["delegation"]["allowed"],
                max_delegation_depth=spec["delegation"]["maxDepth"],
                kill_switch_required=spec["killSwitch"]["required"],
            ))
        return reg
