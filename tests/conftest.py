import os
from unittest.mock import AsyncMock

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)

from database import Base, get_db
from main import app

# -----------------------------
# Test Database Configuration
# -----------------------------
TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/test_db",
)

# -----------------------------
# Test Engine & Session Factory
# -----------------------------
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
)

TestingSessionLocal = async_sessionmaker(
    bind=test_engine,
    expire_on_commit=False,
)


# -----------------------------
# Database Lifecycle
# -----------------------------
@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await test_engine.dispose()


# -----------------------------
# Database Session Fixture
# -----------------------------
@pytest_asyncio.fixture
async def db_session():
    async with TestingSessionLocal() as session:
        yield session


# -----------------------------
# FastAPI Dependency Override
# -----------------------------
async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


# -----------------------------
# HTTP Client Fixture
# -----------------------------
@pytest_asyncio.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client


# -----------------------------
# Mock Repository Fixtures
# -----------------------------
@pytest.fixture
def task_repository():
    return AsyncMock()


@pytest.fixture
def user_repository():
    return AsyncMock()


@pytest.fixture
def project_repository():
    return AsyncMock()
