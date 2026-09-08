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
    max_runtime_seconds: int = 900
    max_tool_calls: int = 50
    max_network_reach: int = 2
    capability_assurance_level: int = 5

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
    target_kind: str = "resource"
    self_affecting_change: bool = False
    reasoning_only_authorization: bool = False
    observed_runtime_seconds: int = 0
    observed_tool_calls: int = 0
    observed_network_reach: int = 0
    delegation_chain: tuple[str, ...] = ()

@dataclass(frozen=True)
class RiskContext:
    privilege: int = 0
    data_sensitivity: int = 0
    tool_power: int = 0
    network_reach: int = 0
    delegation: int = 0
    impact: int = 0
    behavior_anomaly: int = 0
    monitor_assurance: int = 5
    containment_assurance: int = 5
    recovery_assurance: int = 5
    aggregate_impact: int = 0

@dataclass(frozen=True)
class MonitorDecision:
    monitor_id: str
    allow: bool
    valid: bool = True
    policy_version: str = "unknown"
    observed_effect: str = ""
    divergence_detected: bool = False

@dataclass(frozen=True)
class HumanApproval:
    approver_id: str
    informed: bool = False
    valid: bool = False
    revocable_before_effect: bool = False
