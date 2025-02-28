"""Conftest for the tests."""

from typing import Generator

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="module")  # type: ignore
def client() -> Generator:
    """Test client for the application."""
    with TestClient(app) as c:
        yield c
