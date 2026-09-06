from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any
from .contracts import AdapterEvidence, BaseIntegrationAdapter


REQUIRED_EVIDENCE_FIELDS = {
    "trace_id", "port_id", "subject_id", "decision_or_result", "timestamp", "implementation_id"
}


@dataclass(frozen=True)
class ConformanceCheck:
    name: str
    passed: bool
    detail: str


@dataclass(frozen=True)
class ConformanceReport:
    adapter_id: str
    port_id: str
    target_level: str
    checks: tuple[ConformanceCheck, ...]

    @property
    def passed(self) -> bool:
        return all(c.passed for c in self.checks)

    def to_dict(self) -> dict[str, Any]:
        return {
            "adapter_id": self.adapter_id,
            "port_id": self.port_id,
            "target_level": self.target_level,
            "passed": self.passed,
            "checks": [asdict(c) for c in self.checks],
        }


def check_evidence(evidence: AdapterEvidence, *, expected_port: str) -> ConformanceCheck:
    doc = evidence.to_dict()
    present = {k for k, v in doc.items() if v not in (None, "")}
    missing = REQUIRED_EVIDENCE_FIELDS - present
    ok = not missing and evidence.port_id == expected_port and len(evidence.digest) == 64
    return ConformanceCheck("evidence-attribution", ok, "ok" if ok else f"missing/mismatch: {sorted(missing)}")


def metadata_checks(adapter: BaseIntegrationAdapter, port_manifest: dict[str, Any], *, target_level: str = "IPS-C1") -> ConformanceReport:
    port_id = port_manifest["metadata"]["id"]
    checks = (
        ConformanceCheck("port-id", adapter.metadata.port_id == port_id, f"adapter={adapter.metadata.port_id}, spec={port_id}"),
        ConformanceCheck("implementation-identified", bool(adapter.metadata.implementation and adapter.metadata.implementation_version), "implementation and version declared"),
        ConformanceCheck("safe-failure-mode", adapter.fail_mode != "fail-open", f"fail_mode={adapter.fail_mode}"),
        ConformanceCheck("health-contract", isinstance(adapter.health(), dict), "health returns structured data"),
    )
    return ConformanceReport(adapter.metadata.adapter_id, port_id, target_level, checks)
