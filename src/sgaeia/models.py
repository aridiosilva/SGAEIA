from __future__ import annotations
from dataclasses import dataclass, field
from typing import Iterable

CLASS_LEVEL = {"L0":0,"L1":1,"L2":2,"L3":3,"L4":4}
AUTONOMY_LEVEL = {"A0":0,"A1":1,"A2":2,"A3":3,"A4":4,"A5":5}

@dataclass(frozen=True)
class Agent:
    id: str
    owner: str
    klass: str
    autonomy: str
    trust_zone: str
    spiffe_id: str
    capabilities: frozenset[str] = field(default_factory=frozenset)
    denied_capabilities: frozenset[str] = field(default_factory=frozenset)
    delegation_allowed: bool = False
    max_delegation_depth: int = 0
    kill_switch_required: bool = True
    enabled: bool = True
    identity_valid: bool = True
    attested: bool = True

@dataclass(frozen=True)
class Intent:
    agent_id: str
    operation: str
    resource: str
    trace_id: str
    delegation_depth: int = 0
    offline: bool = False
    critical: bool = False
    physical_actuation: bool = False
    human_approvals: int = 0
    creator_id: str | None = None
    approver_id: str | None = None

@dataclass(frozen=True)
class RiskContext:
    privilege: int = 0
    data_sensitivity: int = 0
    tool_power: int = 0
    network_reach: int = 0
    delegation: int = 0
    impact: int = 0
    behavior_anomaly: int = 0
