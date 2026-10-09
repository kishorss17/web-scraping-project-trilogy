"""
Tests for Catalog Analytics & Aggregation endpoints
"""
from fastapi.testclient import TestClient


def test_analytics_overview(client: TestClient):
    response = client.get("/api/v1/analytics/overview")
    assert response.status_code == 200
    data = response.json()
    assert data["total_products"] > 0
    assert data["avg_price"] > 0
    assert data["min_price"] >= 0
    assert data["max_price"] >= data["min_price"]
    assert data["total_categories"] > 0


def test_analytics_categories(client: TestClient):
    response = client.get("/api/v1/analytics/categories?limit=10")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    first = data[0]
    assert "category" in first
    assert "count" in first
    assert "avg_price" in first


def test_analytics_price_distribution(client: TestClient):
    response = client.get("/api/v1/analytics/price-distribution")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 4
    total_pct = sum(item["percentage"] for item in data)
    # Total percentage should approximate ~100%
    assert 95.0 <= total_pct <= 105.0


def test_analytics_top_rated(client: TestClient):
    response = client.get("/api/v1/analytics/top-rated?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 5
    if len(data) > 1:
        assert data[0]["rating"] >= data[-1]["rating"]
