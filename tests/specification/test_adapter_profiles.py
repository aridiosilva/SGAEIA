from pathlib import Path
import csv
import yaml

ROOT = Path(__file__).resolve().parents[2]
ADAPTER_DIR = ROOT / "specs" / "integrations" / "adapters"


def load_profiles():
    return [yaml.safe_load(p.read_text()) for p in sorted(ADAPTER_DIR.glob("*.adapter.yaml"))]


def test_adapter_profiles_are_complete_and_bound_to_existing_ports():
    ports = {
        yaml.safe_load(p.read_text())["metadata"]["id"]
        for p in (ROOT / "specs" / "integrations" / "ports").glob("*.port.yaml")
    }
    profiles = load_profiles()
    assert len(profiles) >= 9
    for doc in profiles:
        assert doc["kind"] == "AdapterProfile"
        assert doc["metadata"]["portId"] in ports
        assert doc["spec"]["targetConformance"] in {"IPS-C1", "IPS-C2", "IPS-C3"}
        assert doc["spec"]["verification"] in {"contract-harness", "live-environment", "independent-assurance"}
        assert doc["spec"]["evidence"]
        assert doc["spec"]["failureMode"] != "fail-open"


def test_adapter_matrix_covers_every_adapter_profile():
    profile_ids = {d["metadata"]["id"] for d in load_profiles()}
    with (ROOT / "specs" / "integrations" / "adapter-conformance-matrix.csv").open() as f:
        rows = list(csv.DictReader(f))
    assert {r["adapter_id"] for r in rows} == profile_ids


def test_same_port_can_have_multiple_conformant_substitutes():
    by_port = {}
    for d in load_profiles():
        by_port.setdefault(d["metadata"]["portId"], []).append(d["metadata"]["id"])
    assert {"ADP-NATS-BUS", "ADP-KAFKA-BUS"}.issubset(set(by_port["IP-BUS"]))
    assert {"ADP-K8S-EDGE", "ADP-K3S-EDGE"}.issubset(set(by_port["IP-EDGE"]))


def test_deployment_profiles_select_known_adapters_without_duplicate_ports():
    known={d["metadata"]["id"]: d["metadata"]["portId"] for d in load_profiles()}
    profiles=list((ROOT / "specs" / "integrations" / "deployment-profiles").glob("*.yaml"))
    assert profiles
    for p in profiles:
        doc=yaml.safe_load(p.read_text())
        selected=doc["spec"]["adapters"]
        assert len(selected)==len(set(selected))
        for port_id, adapter_id in selected.items():
            assert adapter_id in known
            assert known[adapter_id] == port_id
