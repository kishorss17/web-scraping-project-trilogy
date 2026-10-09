"""
Integration tests for Products Catalog endpoints
"""
from fastapi.testclient import TestClient


def test_list_products_pagination(client: TestClient):
    response = client.get("/api/v1/products?page=1&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert data["page"] == 1
    assert data["page_size"] == 10
    assert len(data["items"]) <= 10
    assert data["total"] > 0
    assert data["has_next"] is True


def test_list_products_category_filter(client: TestClient):
    response = client.get("/api/v1/products?category=Travel")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] > 0
    for item in data["items"]:
        assert item["category"].lower() == "travel"


def test_list_products_price_filter(client: TestClient):
    response = client.get("/api/v1/products?min_price=20&max_price=30")
    assert response.status_code == 200
    data = response.json()
    for item in data["items"]:
        assert 20.0 <= item["price"] <= 30.0


def test_search_products(client: TestClient):
    response = client.get("/api/v1/products/search?q=Himalayas")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert any("Himalayas" in item["title"] for item in data["items"])


def test_get_single_product_not_found(client: TestClient):
    response = client.get("/api/v1/products/non-existent-sku-xyz-999999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_product_crud_lifecycle(client: TestClient, auth_headers: dict):
    test_sku = "test-automated-product-999"

    # 1. Attempt create without API key -> 401
    unauth_resp = client.post("/api/v1/products", json={
        "product_id": test_sku,
        "title": "Automated Test Book",
        "price": 29.99
    })
    assert unauth_resp.status_code == 401

    # 2. Attempt create with wrong API key -> 403
    forbidden_resp = client.post(
        "/api/v1/products",
        json={"product_id": test_sku, "title": "Test Book", "price": 29.99},
        headers={"X-API-Key": "wrong-key"}
    )
    assert forbidden_resp.status_code == 403

    # 3. Create product with valid API key -> 201
    create_resp = client.post(
        "/api/v1/products",
        json={
            "product_id": test_sku,
            "title": "Automated Test Book",
            "price": 29.99,
            "category": "Science Fiction",
            "rating": 4.5,
            "availability": "In stock (10 available)"
        },
        headers=auth_headers
    )
    assert create_resp.status_code == 201
    created_data = create_resp.json()
    assert created_data["product_id"] == test_sku
    assert created_data["price"] == 29.99

    # 4. Fetch the created product -> 200
    fetch_resp = client.get(f"/api/v1/products/{test_sku}")
    assert fetch_resp.status_code == 200
    assert fetch_resp.json()["title"] == "Automated Test Book"

    # 5. Patch price -> 200
    patch_resp = client.patch(
        f"/api/v1/products/{test_sku}",
        json={"price": 19.99, "availability": "In stock (5 available)"},
        headers=auth_headers
    )
    assert patch_resp.status_code == 200
    assert patch_resp.json()["price"] == 19.99

    # 6. Delete product -> 200
    delete_resp = client.delete(f"/api/v1/products/{test_sku}", headers=auth_headers)
    assert delete_resp.status_code == 200
    assert delete_resp.json()["success"] is True

    # 7. Verify deletion -> 404
    verify_resp = client.get(f"/api/v1/products/{test_sku}")
    assert verify_resp.status_code == 404
