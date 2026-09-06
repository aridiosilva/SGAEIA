from pathlib import Path
import csv
import yaml

ROOT = Path(__file__).resolve().parents[2]
INT = ROOT / "specs" / "integrations"

REQUIRED_CONTRACTS = {"functional", "security", "audit", "failure", "revocation"}


def load_ports():
    return [yaml.safe_load(p.read_text()) for p in sorted((INT / "ports").glob("*.port.yaml"))]


def test_all_ports_have_five_contract_dimensions():
    ports = load_ports()
    assert len(ports) >= 10
    for port in ports:
        assert port["kind"] == "IntegrationPort"
        assert REQUIRED_CONTRACTS.issubset(port["spec"]["contracts"])
        for key in REQUIRED_CONTRACTS:
            assert port["spec"]["contracts"][key]


def test_all_ports_require_evidence_and_revocation():
    for port in load_ports():
        assert port["spec"]["evidence"]["required"] is True
        assert port["spec"]["revocation"]["supported"] is True
        assert port["spec"]["revocation"]["maxPropagationSeconds"] >= 0


def test_critical_ports_never_fail_open():
    for port in load_ports():
        if port["metadata"].get("criticality") == "critical":
            assert port["spec"]["failureMode"] != "domain-specific"
            failure_text = " ".join(port["spec"]["contracts"]["failure"]).lower()
            assert not ("increase autonomy" in failure_text and ("must not" not in failure_text and "never" not in failure_text))


def test_openapi_baseline_is_3_2_0():
    docs = list((INT / "openapi").glob("*.openapi.yaml"))
    assert docs
    for p in docs:
        doc = yaml.safe_load(p.read_text())
        assert doc["openapi"] == "3.2.0"
        assert doc.get("paths") is not None


def test_asyncapi_baseline_is_3_1_0():
    docs = list((INT / "asyncapi").glob("*.asyncapi.yaml"))
    assert docs
    for p in docs:
        doc = yaml.safe_load(p.read_text())
        assert doc["asyncapi"] == "3.1.0"
        assert doc.get("channels")
        assert doc.get("operations")


def test_conformance_matrix_covers_every_port():
    ports = {p["metadata"]["id"] for p in load_ports()}
    with (INT / "conformance-matrix.csv").open() as f:
        rows = list(csv.DictReader(f))
    assert {r["port_id"] for r in rows} == ports
