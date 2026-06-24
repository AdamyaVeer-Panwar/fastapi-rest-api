import pytest
from fastapi.testclient import TestClient

from main import app
from database import get_db


@pytest.fixture
def client(db_session):

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()