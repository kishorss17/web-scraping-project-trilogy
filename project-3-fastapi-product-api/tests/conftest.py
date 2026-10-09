"""
Pytest configuration and client fixtures
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import get_settings

settings = get_settings()


@pytest.fixture(scope="session")
def client():
    """Session-scoped test client running lifespan events."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="session")
def auth_headers():
    """Headers for authorized write operations."""
    return {"X-API-Key": settings.API_KEY}
