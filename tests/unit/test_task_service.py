import pytest
from unittest.mock import AsyncMock, Mock, patch
from fastapi import HTTPException

from task_service import TaskService


# =========================
# Fixtures
# =========================


@pytest.fixture
def task_service(task_repository, user_repository, project_repository):
    return TaskService(
        repository=task_repository,
        user_repository=user_repository,
        project_repository=project_repository,
    )


# =========================
# Tests
# =========================


@pytest.mark.asyncio
async def test_create_task_user_not_found(task_service, user_repository):
    # Given
    user_repository.get_by_id.return_value = None

    # When / Then
    with pytest.raises(HTTPException) as exc_info:
        await task_service.create_task(title="Test Task", user_id=999, project_id=1)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User not found"


@pytest.mark.asyncio
async def test_create_task_project_not_found(
    task_service, user_repository, project_repository
):
    # Given
    user_repository.get_by_id.return_value = Mock()
    project_repository.get_by_id.return_value = None

    # When / Then
    with pytest.raises(HTTPException) as exc_info:
        await task_service.create_task(title="Test Task", user_id=1, project_id=999)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Project not found"


@pytest.mark.asyncio
async def test_create_task_success(
    task_service, task_repository, user_repository, project_repository
):
    # Given
    user_repository.get_by_id.return_value = Mock()
    project_repository.get_by_id.return_value = Mock()

    fake_task = Mock()
    fake_task.id = 1
    fake_task.title = "Test Task"
    fake_task.user_id = 1
    fake_task.project_id = 1

    task_repository.create.return_value = fake_task

    # Mock external Redis event publisher
    with patch("task_service.publish_event", new_callable=AsyncMock) as mock_publish:
        # When
        result = await task_service.create_task(
            title="Test Task", user_id=1, project_id=1
        )

        # Then - returned task is correct
        assert result == fake_task

        # Then - repository was called correctly
        task_repository.create.assert_awaited_once()

        # Then - event was published
        mock_publish.assert_awaited_once_with(
            "task_created",
            {
                "event": "task_created",
                "task_id": 1,
                "title": "Test Task",
                "user_id": 1,
                "project_id": 1,
            },
        )
