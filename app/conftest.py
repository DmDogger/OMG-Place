from unittest.mock import AsyncMock
import pytest
from faker import Faker
from fastapi.testclient import TestClient

from app.core.exceptions import ProductNotFound
from app.main import app


Faker.seed(100)


@pytest.fixture(scope='session')
def fake() -> Faker:
    return Faker()

@pytest.fixture(scope='session')
def expected_product_data(fake: Faker) -> dict:
    return {
        'name': fake.sentence(nb_words=5),
        'description': fake.text(max_nb_chars=150),
        'price': str(fake.pyfloat(left_digits=3, right_digits=2, positive=True)),
        'image_url': fake.image_url(),
        'stock': fake.pyint(min_value=1, max_value=500),
        'is_active': True,
        'category_id': fake.pyint(min_value=1, max_value=10),
        'rating': float(fake.pyfloat(min_value=1.0, max_value=5.0, positive=True))
    }


@pytest.fixture(scope='session')
def mock_product_service(expected_product_data) -> AsyncMock:
    mock_service = AsyncMock()

    mock_service.find_active_product.return_value = expected_product_data
    return mock_service

@pytest.fixture(scope='session')
def mock_not_found_error() -> AsyncMock:
    mock_service = AsyncMock()
    mock_service.find_active_product.side_effect = ProductNotFound()
    return mock_service


@pytest.fixture(scope='module')
def client(mock_product_service: AsyncMock) -> TestClient:
    with TestClient(app) as client:
        yield client
