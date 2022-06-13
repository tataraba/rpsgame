import random

import pytest
from app.main import get_app
from fastapi.testclient import TestClient


@pytest.fixture
def app():
    return TestClient(get_app())



