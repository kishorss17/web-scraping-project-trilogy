"""
Unit tests for Health and Root endpoints
"""
from fastapi.testclient import TestClient


def test_root_endpoint(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "Rubick" in data["message"]
    assert data["version"] == "1.0.0"
    assert "/docs" in data["docs_url"]
    assert "X-Process-Time-Ms" in response.headers


def test_health_check(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["healthy", "degraded"]
    assert data["database_connected"] is True
    assert data["products_count"] > 0
    assert data["response_time_ms"] >= 0
