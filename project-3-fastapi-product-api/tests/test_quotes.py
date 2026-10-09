"""
Tests for Quotes endpoints (Project 2 Selenium scraper integration)
"""
from fastapi.testclient import TestClient


def test_list_quotes(client: TestClient):
    response = client.get("/api/v1/quotes?page=1&page_size=5")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert data["page"] == 1
    assert data["page_size"] == 5


def test_random_quote(client: TestClient):
    response = client.get("/api/v1/quotes/random")
    # Might be 200 if quotes exist, or 404 if quotes collection is empty
    assert response.status_code in [200, 404]
    if response.status_code == 200:
        data = response.json()
        assert "text" in data
        assert "author" in data


def test_quote_tags(client: TestClient):
    response = client.get("/api/v1/quotes/tags?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
