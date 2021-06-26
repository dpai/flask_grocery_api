import pytest
from grocery_api.app import create_app
from grocery_api.config import TestingConfig

@pytest.fixture
def client():
    app = create_app(TestingConfig)

    with app.test_client() as client:
        yield client