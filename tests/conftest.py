import pytest
from unittest.mock import AsyncMock


@pytest.fixture
def task_repository():
    return AsyncMock()


@pytest.fixture
def user_repository():
    return AsyncMock()


@pytest.fixture
def project_repository():
    return AsyncMock()