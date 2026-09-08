from fastapi.testclient import TestClient

from sgaeia.api import app


client = TestClient(app)


def request(**changes):
    payload = {
        "agent_id": "invoice-agent-prod-01",
        "operation": "invoices.read",
        "resource": "invoice:1",
        "trace_id": "api-trace-1",
    }
    payload.update(changes)
    return payload


def test_api_allows_registered_low_risk_operation_from_trusted_policy():
    response = client.post("/v1/authorize", json=request())
    assert response.status_code == 200
    assert response.json()["allow"] is True


def test_api_rejects_client_supplied_criticality():
    response = client.post("/v1/authorize", json=request(critical=False))
    assert response.status_code == 422


def test_api_rejects_client_supplied_monitor_decision():
    response = client.post("/v1/authorize", json=request(
        monitor_id="invented-monitor", monitor_allow=True, monitor_valid=True))
    assert response.status_code == 422


def test_api_rejects_client_supplied_assurance_and_budget_counters():
    response = client.post("/v1/authorize", json=request(
        monitor_assurance=5, containment_assurance=5,
        recovery_assurance=5, observed_tool_calls=0))
    assert response.status_code == 422
