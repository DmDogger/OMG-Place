from fastapi.testclient import TestClient
from unittest.mock import AsyncMock
from app.main import app


def test_get_product_success(
        client: TestClient,
        expected_product_data: dict,
        mock_product_service: AsyncMock
):
    def override_service():
        return mock_product_service

    response = client.get('/products/search/5')

    assert response.status_code == 200
    assert response.json() == expected_product_data
    assert response.headers['content-type'] == 'application/json'

def test_get_product_unsuccess(
        client: TestClient,
        mock_product_service: AsyncMock
):
    response = client.get('/products/search/404')

    assert response.status_code == 404