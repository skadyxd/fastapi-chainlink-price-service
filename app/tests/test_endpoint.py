import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock

from app.main import app_fastapi
from app.services.chainlink_service import ChainlinkService
from app.dependencies import get_chainlink_service

client = TestClient(app_fastapi)


@pytest.fixture
def mock_chainlink_service():
    mock_service = MagicMock(spec=ChainlinkService)
    return mock_service


@pytest.fixture(autouse=True)
def override_dependencies(mock_chainlink_service):
    app_fastapi.dependency_overrides[get_chainlink_service] = lambda: mock_chainlink_service
    yield
    app_fastapi.dependency_overrides = {}


def test_get_nearest_price_success(mock_chainlink_service):
    mock_chainlink_service.get_chainlink_price_at_timestamp.return_value = 2500.75

    timestamp = 1736443823
    response = client.get(f"/prices/nearest/{timestamp}")

    assert response.status_code == 200
    assert response.json() == {"price": 2500.75}
    mock_chainlink_service.get_chainlink_price_at_timestamp.assert_called_once_with(timestamp)


def test_get_nearest_price_invalid_timestamp(mock_chainlink_service):
    timestamp = "str_timestamp"
    response = client.get(f"/prices/nearest/{timestamp}")

    assert response.status_code == 422


def test_get_nearest_price_not_found(mock_chainlink_service):
    mock_chainlink_service.get_chainlink_price_at_timestamp.side_effect = ValueError("Item not found")

    timestamp = 1609459200
    response = client.get(f"/prices/nearest/{timestamp}")

    assert response.status_code == 400
    mock_chainlink_service.get_chainlink_price_at_timestamp.assert_called_once_with(timestamp)


def test_get_nearest_price_internal_error(mock_chainlink_service):
    mock_chainlink_service.get_chainlink_price_at_timestamp.side_effect = Exception("Internal error")

    timestamp = 1609459200
    response = client.get(f"/prices/nearest/{timestamp}")

    assert response.status_code == 500
    mock_chainlink_service.get_chainlink_price_at_timestamp.assert_called_once_with(timestamp)

