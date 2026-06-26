import pytest

from user_repository import UserRepository
from models import User


@pytest.mark.asyncio
async def test_create_user(db_session):
    repository = UserRepository(db_session)

    user = User(name="Adamya", email="adamya@example.com")

    created_user = await repository.create(user)

    assert created_user.id is not None
    assert created_user.name == "Adamya"
    assert created_user.email == "adamya@example.com"
