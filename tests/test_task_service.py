import pytest
from unittest.mock import AsyncMock
from fastapi import HTTPException

from task_service import TaskService


@pytest.mark.asyncio
async def test_create_task_user_not_found():

    task_repository = AsyncMock()
    user_repository = AsyncMock()
    project_repository = AsyncMock()

    user_repository.get_by_id.return_value = None

    service = TaskService(
        repository=task_repository,
        user_repository=user_repository,
        project_repository=project_repository
    )

    with pytest.raises(HTTPException) as exc_info:
        await service.create_task(
            title="Test Task",
            user_id=999,
            project_id=1
        )

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User not found"


@pytest.mark.asyncio
async def test_create_task_project_not_found():

    task_repository = AsyncMock()
    user_repository = AsyncMock()
    project_repository = AsyncMock()

    user_repository.get_by_id.return_value = object()

    project_repository.get_by_id.return_value = None

    service = TaskService(
        repository=task_repository,
        user_repository=user_repository,
        project_repository=project_repository
    )

    with pytest.raises(HTTPException) as exc_info:
        await service.create_task(
            title="Test Task",
            user_id=1,
            project_id=999
        )

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Project not found"


@pytest.mark.asyncio
async def test_create_task_success():

    task_repository = AsyncMock()
    user_repository = AsyncMock()
    project_repository = AsyncMock()

    user_repository.get_by_id.return_value = object()

    project_repository.get_by_id.return_value = object()

    fake_task = object()

    task_repository.create.return_value = fake_task

    service = TaskService(
        repository=task_repository,
        user_repository=user_repository,
        project_repository=project_repository
    )

    result = await service.create_task(
        title="Test Task",
        user_id=1,
        project_id=1
    )

    assert result == fake_task