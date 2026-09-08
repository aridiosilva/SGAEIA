from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
import yaml

from .collective import AgentContribution
from .delegation import DelegationGrant
from .models import Agent, HumanApproval, Intent, MonitorDecision, RiskContext

PROTECTED_TARGETS = {"policy", "monitor", "evidence", "identity", "kill_switch"}


@dataclass(frozen=True)
class OperationPolicy:
    critical: bool = False
    physical_actuation: bool = False
    target_kind: str = "resource"
    self_affecting_change: bool = False
    reasoning_only_authorization: bool = False
    monitor_assurance: int = 0
    containment_assurance: int = 0
    recovery_assurance: int = 0
    risk: RiskContext = field(default_factory=RiskContext)
    expected_effect: str = ""


@dataclass(frozen=True)
class TrustedAuthorizationContext:
    source: str
    issued_at: str
    trusted: bool
    policy: OperationPolicy
    offline: bool = False
    observed_runtime_seconds: int = 0
    observed_tool_calls: int = 0
    observed_network_reach: int = 0
    monitor: MonitorDecision | None = None
    monitor_registered: bool = False
    approval: HumanApproval | None = None
    approval_registered: bool = False
    delegation_chain: tuple[DelegationGrant, ...] = ()
    delegation_error: str = ""
    collective_contributions: tuple[AgentContribution, ...] = ()
    prohibited_capability_sets: tuple[frozenset[str], ...] = ()
    aggregate_impact_limit: int = 0


class TrustedContextProvider:
    """Server-side reference authority for security-relevant context.

    Client payloads select an intent and credential identifiers only.  The
    provider resolves the actual policy, monitor, approval, counters and grants
    from trusted stores.  Production adapters replace these in-memory stores.
    """

    def __init__(self, policies: dict[str, OperationPolicy] | None = None):
        self.policies = policies or {}
        self.monitors: dict[str, MonitorDecision] = {}
        self.approvals: dict[str, HumanApproval] = {}
        self.grants: dict[str, DelegationGrant] = {}
        self.runtime_counters: dict[str, tuple[int, int, int]] = {}
        self.offline = False

    @classmethod
    def from_yaml(cls, path: str | Path) -> "TrustedContextProvider":
        document = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
        policies: dict[str, OperationPolicy] = {}
        for operation, item in document.get("operations", {}).items():
            assurance = item.get("assurance", {})
            risk = item.get("risk", {})
            policies[operation] = OperationPolicy(
                critical=bool(item.get("critical", False)),
                physical_actuation=bool(item.get("physicalActuation", False)),
                target_kind=item.get("targetKind", "resource"),
                self_affecting_change=bool(item.get("selfAffectingChange", False)),
                reasoning_only_authorization=bool(item.get("reasoningOnlyAuthorization", False)),
                monitor_assurance=int(assurance.get("monitor", 0)),
                containment_assurance=int(assurance.get("containment", 0)),
                recovery_assurance=int(assurance.get("recovery", 0)),
                risk=RiskContext(**{key: int(value) for key, value in risk.items()}),
                expected_effect=item.get("expectedEffect", ""),
            )
        return cls(policies)

    def resolve(self, intent: Intent, agent: Agent | None) -> TrustedAuthorizationContext:
        policy = self.policies.get(intent.operation, OperationPolicy())
        # Protected-resource classification is server-derived and cannot be
        # weakened by a client-supplied target_kind.
        resource_kind = intent.resource.split(":", 1)[0]
        if resource_kind in PROTECTED_TARGETS and policy.target_kind == "resource":
            policy = OperationPolicy(**{**policy.__dict__, "target_kind": resource_kind})
        grants: list[DelegationGrant] = []
        missing = ""
        for grant_id in intent.delegation_chain:
            grant = self.grants.get(grant_id)
            if grant is None:
                missing = "unknown_delegation_grant"
                break
            grants.append(grant)
        runtime, tools, network = self.runtime_counters.get(intent.trace_id, (0, 0, 0))
        return TrustedAuthorizationContext(
            source="sgaeia-control-plane", issued_at=datetime.now(timezone.utc).isoformat(),
            trusted=True, policy=policy, offline=self.offline,
            observed_runtime_seconds=runtime, observed_tool_calls=tools,
            observed_network_reach=network, monitor=self.monitors.get(intent.trace_id),
            monitor_registered=intent.trace_id in self.monitors,
            approval=self.approvals.get(intent.trace_id),
            approval_registered=intent.trace_id in self.approvals,
            delegation_chain=tuple(grants),
            delegation_error=missing,
        )
