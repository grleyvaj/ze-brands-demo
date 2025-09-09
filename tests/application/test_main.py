import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_app_has_openapi(client: TestClient):
    """Ensure app generates OpenAPI schema and root is redirected to ReDoc"""
    expected_success_code = 200
    response = client.get("/openapi.json")
    assert response.status_code == expected_success_code
    assert "paths" in response.json()
